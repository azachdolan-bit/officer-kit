#!/usr/bin/env python3
"""Write a sand table plan file from the facts read out of a base order, so the planner opens the sand table with higher's
paragraphs already in place and builds only what is theirs.

Usage:
  python3 plan_writer.py facts.json --out <name>.sandtable.json [--sourced sourced.md]

facts.json (Claude writes it after reading the order; every value carries where it came from):
  {
    "name": "1st Plt defense, MG STEX",           plan title
    "sheet": "stex",                               which map sheet: ta16 or stex (see references/field-map.md)
    "optype": "platoon defense",                   platoon defense, platoon offense or squad offense
    "order": "MG STEX Defense FRAGO, 31 Jul 26",   the base order, named for the notes
    "fields": [
      {"step": "mission", "key": "mission", "value": "NLT 1800 ...", "src": "para 3.c.(1)"},
      {"step": "enemy", "key": "size", "value": "squad", "src": "para 1.a.(1)"},
      ...
    ]
  }

What comes out: a plan file the sand table imports (Plan, Import file). It carries guide.values only; the page builds every
symbol, line and route from the values when it imports the file. Every field of every step on the operation's track is
present, "" where the order gave nothing, so the guide shows the planner exactly what is left. sourced.md lists every
filled field with its source and every blank, for the planner to correct before importing.

Rules the writer enforces:
  - a field key must exist on the page's guide (references/guide_fields.json); an unknown key is an error, not a guess;
  - a grid field (place, points, draw, area, unit) takes 4, 6 or 8 digit grids only; anything else is refused;
  - a select field takes one of its options or "";
  - objects, routes and phases are always empty: the page builds them;
  - no value is invented: the writer copies, it never fills.
"""
import json
import os
import random
import re
import string
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = json.load(open(os.path.join(HERE, "..", "references", "guide_fields.json"), encoding="utf-8"))
GRID_TYPES = {"place", "points", "draw", "area", "unit", "target"}
SHEETS = {"ta16": "TH", "stex": "MG"}
TRACK = {"platoon defense": "defense", "platoon offense": "offense", "squad offense": "offense"}


def steps_for(optype):
    mode = TRACK[optype]
    return [s for s in FIELDS if s["id"] != "review" and s["mode"] in ("both", mode)]


def field_def(step, key):
    for s in FIELDS:
        if s["id"] == step:
            for f in s["fields"]:
                if f["k"] == key:
                    return s, f
    return None, None


def grids_ok(text):
    """Every token of a grid list must be a 4, 6 or 8 digit grid (a unit or target carries its grid in a sub key)."""
    toks = [t for t in re.split(r"[\s,;]+", str(text).strip()) if t]
    return all(re.fullmatch(r"\d{4}|\d{6}|\d{8}", t) for t in toks)


def check_value(step, f, val, errs, where):
    t = f["t"]
    if t in ("unit",):
        if not isinstance(val, dict) or set(val) - {"role", "grid"}:
            errs.append("%s: a unit is {role, grid}" % where)
        elif val.get("grid") and not grids_ok(val["grid"]):
            errs.append("%s: unit grid must be 4, 6 or 8 digits" % where)
        return
    if t == "target":
        if not isinstance(val, dict) or set(val) - {"num", "grid", "wpn", "trigger", "obs", "task"}:
            errs.append("%s: a target is {num, grid, wpn, trigger, obs, task}" % where)
        elif val.get("grid") and not grids_ok(val["grid"]):
            errs.append("%s: target grid must be 4, 6 or 8 digits" % where)
        return
    if not isinstance(val, str):
        errs.append("%s: value must be text" % where)
        return
    if t in GRID_TYPES and val and not grids_ok(val):
        errs.append("%s: '%s' is not a grid list (4, 6 or 8 digits each)" % (where, val[:40]))
    if t == "squares" and val and not all(re.fullmatch(r"\d{4}", x) for x in re.split(r"[\s,;]+", val.strip()) if x):
        errs.append("%s: squares are 4 digit grid squares" % where)
    if t == "select" and val and f.get("opts") and val not in f["opts"]:
        errs.append("%s: '%s' is not one of %s" % (where, val, f["opts"]))
    if t == "number" and val and not re.fullmatch(r"-?\d+(\.\d+)?", val.strip()):
        errs.append("%s: '%s' is not a number" % (where, val))


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    facts = json.load(open(argv[1], encoding="utf-8"))
    out = None
    sourced = None
    i = 2
    while i < len(argv):
        if argv[i] == "--out":
            out = argv[i + 1]
            i += 2
        elif argv[i] == "--sourced":
            sourced = argv[i + 1]
            i += 2
        else:
            print("unknown argument", argv[i])
            return 2
    errs = []
    optype = facts.get("optype") or "platoon defense"
    if optype not in TRACK:
        errs.append("optype must be platoon defense, platoon offense or squad offense")
    sheet = facts.get("sheet") or "ta16"
    if sheet not in SHEETS:
        errs.append("sheet must be one of %s" % sorted(SHEETS))
    if errs:
        print("\n".join("FAIL " + e for e in errs))
        return 1
    steps = steps_for(optype)
    values = {}
    for s in steps:
        values[s["id"]] = {}
        for f in s["fields"]:
            if f["t"] == "unit":
                values[s["id"]][f["k"]] = {"role": "", "grid": ""}
            elif f["t"] == "target":
                values[s["id"]][f["k"]] = {"num": "", "grid": "", "wpn": "", "trigger": "", "obs": "", "task": ""}
            else:
                values[s["id"]][f["k"]] = ""
    values["name"]["optype"] = optype
    values["name"]["name"] = facts.get("name", "")
    notes = "Prefilled from the base order" + (": " + facts["order"] if facts.get("order") else "") + ". Every value carries its paragraph in the sourced list; blanks are the planner's to fill."
    values["name"]["notes"] = notes
    filled = []
    seen = set()
    for fct in facts.get("fields", []):
        step, key, val, src = fct.get("step"), fct.get("key"), fct.get("value"), fct.get("src", "")
        where = "%s/%s" % (step, key)
        s, f = field_def(step, key)
        if not s or not f:
            errs.append("%s: no such field on the guide (see references/guide_fields.json)" % where)
            continue
        if s["id"] not in values:
            errs.append("%s: that step is not on the %s track" % (where, TRACK[optype]))
            continue
        if not src:
            errs.append("%s: every value needs its src (the paragraph of the order it came from)" % where)
        if (step, key) in seen:
            errs.append("%s: given twice" % where)
        seen.add((step, key))
        check_value(step, f, val, errs, where)
        if val in ("", None) or (isinstance(val, dict) and all(v == "" for v in val.values())):
            continue
        values[step][key] = val
        filled.append((s, f, val, src))
    if errs:
        print("\n".join("FAIL " + e for e in errs))
        return 1
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    pid = "plan_" + "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    plan = {"schema": 1, "id": pid, "name": facts.get("name", "") or "Plan from the base order", "owner": None, "created": now, "updated": now,
            "saveId": None, "sheet": sheet, "aoi": None, "objects": [], "routes": [], "custom": [], "phases": [], "notes": notes,
            "guide": {"values": values, "source": {"kind": "officer-kit sand-table-intake", "order": facts.get("order", ""), "written": now}}}
    out = out or (re.sub(r"[^\w\- ]+", "", plan["name"]).strip().replace(" ", "_") or "plan") + ".sandtable.json"
    json.dump(plan, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # the sourced list: what was filled, from where; what is blank, by step
    L = ["# What the base order gave the sand table: " + plan["name"], "", "Operation: %s. Sheet %s (grid square %s). Base order: %s." % (optype, sheet, SHEETS[sheet], facts.get("order", "not named")), "",
         "Import `%s` on the sand table page (Plan, Import file). The page builds every symbol, line and route from these values and opens the Guide at Review. Check each filled value against its paragraph before you plan; the blanks below are yours." % os.path.basename(out), "",
         "## Filled from the order (%d)" % len(filled), ""]
    cur = None
    for s, f, val, src in filled:
        if s["id"] != cur:
            cur = s["id"]
            L.append("")
            L.append("### " + s["title"])
        v = val if isinstance(val, str) else ", ".join("%s %s" % (k, x) for k, x in val.items() if x)
        L.append("- %s (%s): %s  [%s]" % (f["label"] or f["k"], f["k"], v.replace("\n", "; "), src))
    L += ["", "## Left for the planner (blank in the file)", ""]
    for s in steps:
        blanks = [f["label"] or f["k"] for f in s["fields"] if (s["id"], f["k"]) not in {(x[0]["id"], x[1]["k"]) for x in filled} and f["k"] not in ("optype", "name", "notes")]
        if blanks:
            L.append("- %s: %s" % (s["title"], "; ".join(blanks)))
    L.append("")
    L.append("Nothing in this file was invented: a value is in it only with the paragraph it came from, and a field the order did not fill is empty.")
    sourced = sourced or re.sub(r"\.sandtable\.json$", "", out) + ".sourced.md"
    open(sourced, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote %s: %s, sheet %s, %d fields filled from the order, %d steps on the track" % (out, optype, sheet, len(filled), len(steps)))
    print("wrote", sourced)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
