#!/usr/bin/env python3
"""t2t_reader.py: a troop to task matrix (xlsx or csv) into the sand table plan file, so the page walks it by the clock.

Usage:
  python3 t2t_reader.py <matrix.xlsx|matrix.csv> [--sheet "v12 Your plan"] [--plan <existing>.sandtable.json] [--out <name>.sandtable.json] [--rehearsal] [--report <name>.t2t.md]

Reads the planner's matrix the way the page does (the page's t2t.js is the reference; this is its Python twin): a Unit column, time
columns X, X+0:30 ... with a Clock row, one row per unit (squad leader, fire team with its strength in parentheses, gun team, MACO gate,
LP/OP, PC, PSgt), a Milestones row and a Security row. In a cell it reads only the planner's own shorthand: "2 sec, 2 dig: task",
"(2 on MACO)", a row name's "(2 on LP/OP 0030 to 0900)" as a standing pair between those clock times, DAY, NIGHT or FT PATROL and
"Leads ... patrol" as the whole row out, STAND TO, and on a leader's row "terrain model", "brief", "debrief", "planning". A blank cell
continues the last entry. Nothing else is inferred. Source for the matrix itself: B3M0830XQ-DM Annex C (priorities of work married to a
timeline from X, by unit). Writes plan["t2t"] into a new or existing plan file; with --rehearsal also one phase per milestone and one
event per slot with a change (the page's Build rehearsal does the same); --report writes a markdown check sheet: rows, links the page
will look for by name, the security count per slot beside the planner's own row."""
import argparse, csv, json, os, re, sys, random, string

GROUP_RE = re.compile(r"^(\d+(?:st|nd|rd|th)\s+(?:squad|sqd|plt|platoon))", re.I)

def clean(s):
    return re.sub(r"\s+", " ", "" if s is None else str(s).replace("\n", " / ")).strip()

def hhmm(s):
    m = re.fullmatch(r"(\d{2})(\d{2})", clean(s))
    return int(m.group(1)) * 60 + int(m.group(2)) if m else None

def clock_minutes(cols):
    out, last, day = [], None, 0
    for c in cols:
        m = hhmm(c)
        if m is None:
            out.append(None); continue
        if last is not None and m < last: day += 1440
        last = m; out.append(m + day)
    return out

def row_kind(unit):
    u = unit.lower()
    if re.search(r"squad leader|\bsl\b", u): return "sl"
    if re.search(r"\bft\b|fire team", u): return "ft"
    if re.search(r"\bgun\b|m240|\bmg\b", u): return "gun"
    if re.search(r"maco|gate", u): return "gate"
    if re.search(r"lp/?op", u): return "lpop"
    if re.search(r"^pc\b|platoon commander", u): return "pc"
    if re.search(r"^psgt|platoon sergeant", u): return "psgt"
    if re.search(r"sketch", u): return "note"
    if re.search(r"^milestone", u): return "milestones"
    if re.search(r"^security", u): return "security"
    if re.search(r"^computed|^position\b|^standard\b|primary|supplementary skirm", u): return "skip"
    return "other"

def row_header(unit):
    name = clean(unit); h = {"name": name, "strength": None, "standing": []}
    m = re.search(r"\((\d+)\)", name)
    if m: h["strength"] = int(m.group(1))
    for mm in re.finditer(r"\((\d+)\s+on\s+(LP/?OP|MACO|gate|patrol)(?:\s+(?:from\s+)?(\d{4})(?:\s+to\s+(\d{4}))?)?\)", name, re.I):
        to = "lpop" if re.match(r"lp", mm.group(2), re.I) else ("patrol" if re.match(r"patrol", mm.group(2), re.I) else "gate")
        h["standing"].append({"n": int(mm.group(1)), "to": to, "from": hhmm(mm.group(3)) if mm.group(3) else None, "until": hhmm(mm.group(4)) if mm.group(4) else None})
    short = re.sub(r"\s*\([^)]*\)", "", name); short = re.sub(r"\s+/\s.*$", "", short); short = re.sub(r",\s*\d+\s*hr.*$", "", short, flags=re.I).strip()
    h["short"] = short
    return h

def parse_cell(text, kind):
    t = clean(text); c = {"text": t, "sec": None, "dig": None, "away": [], "all": None, "leaderAt": None, "standTo": False, "patrol": False}
    if not t: return c
    u = t.lower()
    if "stand to" in u: c["standTo"] = True; c["all"] = "line"
    sd = re.search(r"(\d+)\s*(?:on\s+)?sec(?:urity)?\s*,\s*(\d+)\s*dig", t, re.I)
    if sd: c["sec"], c["dig"] = int(sd.group(1)), int(sd.group(2))
    else:
        s1 = re.search(r"(\d+)\s*(?:on\s+)?sec(?:urity)?\b", t, re.I)
        if s1: c["sec"] = int(s1.group(1))
        d1 = re.search(r"(\d+)\s*dig", t, re.I)
        if d1: c["dig"] = int(d1.group(1))
    for m in re.finditer(r"\((\d+)\s+on\s+(MACO|gate|LP/?OP|patrol)\)", t, re.I):
        c["away"].append({"n": int(m.group(1)), "to": "lpop" if re.match(r"lp", m.group(2), re.I) else ("patrol" if re.match(r"patrol", m.group(2), re.I) else "gate")})
    if re.search(r"\b(night|day|ft|security|squad|sqd)\s+patrol\b", t, re.I) or re.search(r"^(leads|lead)\b.*patrol", t, re.I):
        c["patrol"] = True; c["all"] = "patrol"
    if kind in ("sl", "pc", "psgt"):
        if "terrain model" in u: c["leaderAt"] = "tm"
        elif re.search(r"\b(brief|debrief|planning|plan)\b", u): c["leaderAt"] = "cp"
        if re.search(r"leads|lead\b", u) and "patrol" in u: c["leaderAt"] = "patrol"
    return c

def parse_grid(grid):
    rows = [[clean(c) for c in r] for r in grid]
    hi = next((i for i, r in enumerate(rows) if r and re.fullmatch(r"unit", r[0] or "", re.I) and any(re.match(r"^X(\+|$)", c, re.I) for c in r)), -1)
    if hi < 0: hi = next((i for i, r in enumerate(rows) if r and re.fullmatch(r"unit", r[0] or "", re.I)), -1)
    if hi < 0: return {"error": "no Unit header row with X columns"}
    header = rows[hi]; ncol = len(header); clock = None
    if hi + 1 < len(rows) and rows[hi + 1] and re.match(r"^clock", rows[hi + 1][0] or "", re.I): clock = (rows[hi + 1] + [""] * ncol)[1:ncol]
    cols = [{"x": h, "clock": (clock[i] if clock else None)} for i, h in enumerate(header[1:ncol])]
    out = {"x": clock[0] if clock else None, "slots": len(cols), "cols": cols, "rows": [], "milestones": [], "security": [], "notes": []}
    group = None
    for i in range(hi + (2 if clock else 1), len(rows)):
        r = rows[i] + [""] * ncol
        if not any(r): continue
        unit = r[0]
        if not unit: continue
        kind = row_kind(unit)
        if kind == "milestones": out["milestones"] = r[1:ncol]; continue
        if kind == "security": out["security"] = r[1:ncol]; continue
        if kind == "skip": continue
        h = row_header(unit); gm = GROUP_RE.match(h["name"])
        if kind == "sl" and gm: group = re.sub(r"squad", "Sqd", gm.group(1), flags=re.I)
        row = {"id": "r%d" % (len(out["rows"]) + 1), "unit": h["name"], "short": h["short"], "kind": kind, "group": (group if kind == "ft" else (re.sub(r"squad", "Sqd", gm.group(1), flags=re.I) if gm else None)), "strength": h["strength"], "standing": h["standing"], "cells": [parse_cell(r[j], kind) for j in range(1, ncol)]}
        out["rows"].append(row)
    out["clockMin"] = clock_minutes([c["clock"] or "" for c in cols])
    return out

def eff_cell(row, i):
    for k in range(min(i, len(row["cells"]) - 1), -1, -1):
        if row["cells"][k]["text"]: return row["cells"][k]
    return parse_cell("", row["kind"])

def row_state(t2t, row, i):
    c = eff_cell(row, i); S = row["strength"]
    st = {"text": c["text"], "standTo": c["standTo"], "away": [], "sec": c["sec"], "dig": c["dig"], "leaderAt": c["leaderAt"], "patrol": c["patrol"]}
    clock = t2t["clockMin"][i] if t2t.get("clockMin") else None
    x0 = t2t["clockMin"][0] if t2t.get("clockMin") and t2t["clockMin"][0] is not None else 0
    for sd in row["standing"]:
        on = True
        if clock is not None and sd["from"] is not None:
            f = sd["from"]
            while f < x0: f += 1440
            u = sd["until"]
            if u is not None:
                while u <= f: u += 1440
                on = f <= clock < u
            else: on = clock >= f
        if on: st["away"].append({"n": sd["n"], "to": sd["to"], "standing": True})
    for a in c["away"]: st["away"].append({"n": a["n"], "to": a["to"]})
    if c["patrol"] and S is not None:
        already = sum(a["n"] for a in st["away"]); st["away"].append({"n": max(0, S - already), "to": "patrol", "all": True})
    if c["leaderAt"] and row["kind"] in ("sl", "pc", "psgt"): st["away"].append({"n": 1, "to": c["leaderAt"], "leader": True})
    st["awayN"] = sum(a["n"] for a in st["away"]); st["present"] = None if S is None else max(0, S - st["awayN"])
    if c["standTo"] and S is not None: st["sec"] = st["present"]
    return st

def security(t2t, i):
    sec = present = total = 0
    for row in t2t["rows"]:
        if row["kind"] == "gate":
            if row["strength"] is not None and eff_cell(row, i)["text"]: sec += row["strength"]
            continue
        if row["kind"] == "lpop": continue
        if row["strength"] is None or row["kind"] in ("sl", "pc", "psgt"): continue
        st = row_state(t2t, row, i); total += row["strength"]
        on_patrol = sum(a["n"] for a in st["away"] if a["to"] in ("patrol", "lpop")); present += max(0, row["strength"] - on_patrol)
        sec += 0 if st["sec"] is None else min(st["sec"], max(0, row["strength"] - on_patrol))
    return {"sec": sec, "present": present, "total": total, "pct": round(100 * sec / present) if present else 0}

def changes(t2t, i):
    out = []
    for row in t2t["rows"]:
        a = row["cells"][i - 1]["text"] if i > 0 else ""; b = row["cells"][i]["text"]
        if b and b != a: out.append((row, b))
    return out

def uid(prefix):
    return prefix + "_" + "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

def to_rehearsal(t2t):
    phases = []; cur = None
    for i in range(t2t["slots"]):
        ms = clean(t2t["milestones"][i] if i < len(t2t["milestones"]) else "")
        if ms or cur is None:
            cur = {"id": uid("ph"), "name": ((t2t["cols"][i]["clock"] + " ") if t2t["cols"][i]["clock"] else "") + ms if ms else "Troop to task from " + (t2t["cols"][0]["clock"] or "X"), "events": [], "t2tFrom": i}
            phases.append(cur)
        ch = changes(t2t, i)
        if not ch and i > 0: continue
        sec = security(t2t, i)
        ev = {"id": uid("ev"), "name": (t2t["cols"][i]["clock"] or t2t["cols"][i]["x"]) + (": " + ms if ms else ""), "step": "initiate", "trigger": t2t["cols"][i]["clock"] or t2t["cols"][i]["x"], "minutes": 2, "critical": False, "main": False, "moves": [], "show": [], "hide": [], "camera": None, "t2tSlot": i,
              "narration": "\n".join(r["short"] + ": " + t for r, t in ch) + (("\nSecurity on the line: %d of %d (%d%%)" % (sec["sec"], sec["present"], sec["pct"])) if sec["total"] else "")}
        cur["events"].append(ev)
    return phases

def read_xlsx(path, sheet):
    try:
        import openpyxl
    except ImportError:
        sys.exit("openpyxl is not installed: pip install openpyxl, or save the sheet as CSV")
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    return [["" if c is None else str(c) for c in r] for r in ws.iter_rows(values_only=True)], ws.title

def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096); f.seek(0)
        dialect = csv.excel_tab if "\t" in sample else csv.excel
        return [list(r) for r in csv.reader(f, dialect)]

def report(t2t, sheet_name):
    L = ["# Troop to task read for the sand table", "", "Sheet: %s. %d slots from %s, %d rows." % (sheet_name, t2t["slots"], t2t["x"] or "X", len(t2t["rows"])), "",
         "## Rows and the map units the page will look for", "", "| row | kind | strength | standing | page looks for |", "|---|---|---|---|---|"]
    for r in t2t["rows"]:
        looks = {"ft": ("%s %s, else %s" % (r["group"], r["short"], r["group"])) if r["group"] else r["short"], "sl": (r["group"] or r["short"]) + " (the leader detaches from it)", "gun": "a gun labeled Left or Right", "gate": "target: an object named MACO or gate", "lpop": "target: the OP", "pc": "PC or the CP", "psgt": "PSgt", "note": "(text only)", "other": r["short"]}.get(r["kind"], r["short"])
        L.append("| %s | %s | %s | %s | %s |" % (r["unit"], r["kind"], r["strength"] if r["strength"] is not None else "", "; ".join("%d on %s%s" % (s["n"], s["to"], (" %s to %s" % (s["from"], s["until"])) if s["from"] is not None else "") for s in r["standing"]), looks))
    L += ["", "## Security on the line by slot (page count beside the sheet's own row)", "", "| slot | clock | page: sec / present | your sheet |", "|---|---|---|---|"]
    for i in range(t2t["slots"]):
        s = security(t2t, i); L.append("| %s | %s | %d / %d (%d%%) | %s |" % (t2t["cols"][i]["x"], t2t["cols"][i]["clock"] or "", s["sec"], s["present"], s["pct"], t2t["security"][i] if i < len(t2t["security"]) else ""))
    L += ["", "Read with the page's rules: a blank cell continues the last entry; the gate guards count as security; the LP/OP pair and patrols are away; nothing else is inferred (t2t.js on the page is the reference)."]
    return "\n".join(L) + "\n"

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("matrix"); ap.add_argument("--sheet"); ap.add_argument("--plan"); ap.add_argument("--out"); ap.add_argument("--rehearsal", action="store_true"); ap.add_argument("--report")
    a = ap.parse_args()
    if a.matrix.lower().endswith((".xlsx", ".xlsm")): grid, sheet_name = read_xlsx(a.matrix, a.sheet)
    else: grid, sheet_name = read_csv(a.matrix), os.path.basename(a.matrix)
    t2t = parse_grid(grid)
    if "error" in t2t: sys.exit("troop to task: " + t2t["error"])
    if a.plan:
        plan = json.load(open(a.plan, encoding="utf-8"))
    else:
        plan = {"schema": 1, "id": uid("plan"), "name": os.path.splitext(os.path.basename(a.matrix))[0], "owner": "", "created": None, "updated": None, "aoi": None, "notes": "", "sheet": None, "objects": [], "routes": [], "custom": [], "phases": []}
    t2t["links"] = (plan.get("t2t") or {}).get("links", {})
    plan["t2t"] = t2t
    if a.rehearsal:
        keep = [p for p in plan.get("phases", []) if p.get("t2tFrom") is None]
        plan["phases"] = keep + to_rehearsal(t2t)
    out = a.out or (a.plan if a.plan else os.path.splitext(a.matrix)[0] + ".sandtable.json")
    json.dump(plan, open(out, "w", encoding="utf-8"), indent=1)
    rep = a.report or re.sub(r"\.sandtable\.json$", "", out) + ".t2t.md"
    open(rep, "w", encoding="utf-8").write(report(t2t, sheet_name))
    print("troop to task: %d rows, %d slots from %s (sheet %s) -> %s%s; report %s" % (len(t2t["rows"]), t2t["slots"], t2t["x"] or "X", sheet_name, out, (" with %d phases" % len([p for p in plan["phases"] if p.get("t2tFrom") is not None])) if a.rehearsal else "", rep))

if __name__ == "__main__":
    main()
