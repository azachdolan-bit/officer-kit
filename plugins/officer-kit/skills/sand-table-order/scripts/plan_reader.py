#!/usr/bin/env python3
"""Read a sand table export and lay out every fact in it, so the order is written from the file and nothing else.

Usage:
  python3 plan_reader.py <plan.sandtable.json> [<plan.sandtable-brief.md>] [--json facts.json] [--md facts.md]

The plan file is the whole plan the sand table holds: the guide steps as the planner filled them (guide.values), text typed
on a step but never applied (guide.typed), every object on the map with its UTM position, every route, the parts and events,
the notes, the area of operations and the sheet. The brief (optional) is the plain text the sand table exports for a chat;
it adds the checks the sand table ran and the magnetic azimuths of every route leg, which need the sheet's declination.

What comes out: facts.json (for order_check.py) and facts.md (to read). Every grid is derived from UTM in code: the 8 digit
grid is the 10 meter easting and northing inside the 100 km square. Distances and grid azimuths are computed here; magnetic
azimuths are taken from the brief when it is given and marked absent otherwise, never guessed.
"""
import json
import math
import re
import sys

SHEETS = {"ta16": ("18S", "TH"), "stex": ("18S", "MG")}   # sheet id -> grid zone designator and 100 km square the sand table uses
DECL = {"ta16": 11, "stex": 0}   # magnetic = grid + this, per sheet, as the sand table's terrain_meta.json states it (TA16: the user's rule of 11 degrees; the STEX sketch has none)
MILS = 6400 / 360.0
TRP_SYMBOLS = ("trp", "target", "point")

GUIDE_TITLES = {
    "name": "Name and operation", "ao": "Area of operations", "mission": "Mission", "enemy": "Enemy", "terrain": "Terrain and weather",
    "troops": "Troops and fire support", "time": "Time, space, logistics, civil", "emlcoa": "EMLCOA", "cgcv": "CG, CV and exploitation",
    "ea": "Engagement area (EA step 3)", "type": "Type and method", "dist": "Distribution of forces", "orient": "Orientation",
    "occ": "Occupation", "tcm": "Control measures", "sec": "Security", "obst": "Obstacles", "oform": "Type of attack and form of maneuver",
    "oto": "Task organization", "otcm": "Control measures and routes", "oseq": "Sequence and signals", "parts": "Parts", "tasks": "Tasks",
    "fsp": "Fire support plan", "coord": "Coordinating instructions", "admin": "Admin, logistics, command and signal",
}
ORDER = list(GUIDE_TITLES.keys())


def grid8(utm, square):
    e, n = utm
    return "%s %04d %04d" % (square, int(math.floor(e / 10)) % 10000, int(math.floor(n / 10)) % 10000)


def grid_digits(utm):
    e, n = utm
    return "%04d%04d" % (int(math.floor(e / 10)) % 10000, int(math.floor(n / 10)) % 10000)


def az_grid(a, b):
    d = math.degrees(math.atan2(b[0] - a[0], b[1] - a[1]))
    return (d + 360) % 360


def dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def flat_value(v):
    if isinstance(v, dict):
        parts = ["%s %s" % (k, x) for k, x in v.items() if x not in (None, "")]
        return ", ".join(parts)
    return str(v).replace("\n", "; ")


def read_brief(path):
    """Checks and route legs from the brief, keyed loosely; the brief is plain text the sand table wrote."""
    out = {"checks": [], "legs": {}, "raw": ""}
    if not path:
        return out
    txt = open(path, encoding="utf-8").read()
    out["raw"] = txt
    step = None
    for line in txt.splitlines():
        m = re.match(r"^## (.+)$", line)
        if m:
            step = m.group(1).strip()
            continue
        m = re.match(r"^\s*- check \((ok|note|warn)\): (.*?)(?: \[(.*)\])?$", line)
        if m:
            out["checks"].append({"step": step, "level": m.group(1), "text": m.group(2).strip(), "src": (m.group(3) or "").strip()})
            continue
        m = re.match(r"^- Route (.+?): (.+?); (leg 1 .*)$", line)
        if m:
            out["legs"][m.group(1).strip()] = m.group(3).strip()
    return out


def read_plan(path):
    plan = json.load(open(path, encoding="utf-8"))
    gzd, square = SHEETS.get(plan.get("sheet") or "", ("?", "??"))
    V = (plan.get("guide") or {}).get("values") or {}
    T = (plan.get("guide") or {}).get("typed") or {}
    optype = (V.get("name") or {}).get("optype") or (V.get("mission") or {}).get("optype") or "platoon defense"
    facts = {"plan": plan.get("name", ""), "sheet": plan.get("sheet", ""), "gzd": gzd, "square": square, "operation": optype,
             "aoi": None, "fields": [], "typed": [], "objects": [], "routes": [], "parts": [], "notes": plan.get("notes", ""), "grids": []}
    if plan.get("aoi"):
        a = plan["aoi"]
        facts["aoi"] = {"sw": grid8([a["e0"], a["n0"]], square), "ne": grid8([a["e1"], a["n1"]], square)}
    for step in ORDER + [k for k in V if k not in ORDER]:
        v = V.get(step)
        if not v:
            continue
        for key, val in v.items():
            if val in (None, "") or (isinstance(val, dict) and all(x in (None, "") for x in val.values())):
                continue
            facts["fields"].append({"step": step, "title": GUIDE_TITLES.get(step, step), "key": key, "value": val, "text": flat_value(val)})
    for step, t in T.items():
        for key, val in (t or {}).items():
            applied = (V.get(step) or {}).get(key)
            if val in (None, "") or val == applied or (isinstance(val, dict) and all(x in (None, "") for x in val.values())):
                continue
            facts["typed"].append({"step": step, "title": GUIDE_TITLES.get(step, step), "key": key, "value": val, "text": flat_value(val)})
    grids = set()
    for o in plan.get("objects", []):
        pts = o.get("utm") or []
        g = [grid8(p, square) for p in pts]
        grids.update(grid_digits(p) for p in pts)
        props = o.get("props") or {}
        sec = props.get("sector")
        item = {"id": o.get("id"), "label": o.get("label") or o.get("symbol"), "symbol": o.get("symbol"), "side": o.get("side"), "kind": o.get("kind"),
                "grids": g, "task": props.get("task", ""), "purpose": props.get("purpose", ""), "remarks": props.get("remarks", "")}
        if sec:
            item["sector"] = {k: sec.get(k) for k in ("kind", "left", "right", "range") if sec.get(k) is not None}
            if sec.get("fpl"):
                item["fpl"] = sec["fpl"]
            if sec.get("pdf"):
                item["pdf"] = sec["pdf"]
        if o.get("kind") == "area" and len(pts) >= 3:
            cx = sum(p[0] for p in pts) / len(pts)
            cy = sum(p[1] for p in pts) / len(pts)
            item["center"] = grid8([cx, cy], square)
            grids.add(grid_digits([cx, cy]))
        facts["objects"].append(item)
    for r in plan.get("routes", []):
        pts = r.get("points") or []
        legs = []
        for i in range(1, len(pts)):
            legs.append({"leg": i, "from": grid8(pts[i - 1], square), "to": grid8(pts[i], square), "dist_m": round(dist(pts[i - 1], pts[i])), "az_grid": round(az_grid(pts[i - 1], pts[i]))})
        grids.update(grid_digits(p) for p in pts)
        facts["routes"].append({"id": r.get("id"), "name": r.get("name"), "pace_kmh": r.get("pace_kmh"), "notes": r.get("notes", ""), "grids": [grid8(p, square) for p in pts], "legs": legs, "total_m": sum(l["dist_m"] for l in legs)})
    for ph in plan.get("phases", []):
        facts["parts"].append({"name": ph.get("name"), "events": [{"name": e.get("name"), "trigger": e.get("trigger", ""), "narration": e.get("narration", "")} for e in ph.get("events", [])]})
    for f in facts["fields"] + facts["typed"]:
        for m in re.findall(r"\b(\d{4}) ?(\d{4})\b", f["text"]):
            grids.add(m[0] + m[1])
    if plan.get("aoi"):
        a = plan["aoi"]
        for pt in ([a["e0"], a["n0"]], [a["e1"], a["n1"]], [a["e0"], a["n1"]], [a["e1"], a["n0"]]):
            grids.add(grid_digits(pt))
    facts["grids"] = sorted(grids)
    facts["direct_fire"] = direct_fire(plan, facts, square)
    return facts


def direct_fire(plan, facts, square):
    """Every friendly position with a sector: limits, FPL and PDF in grid and magnetic azimuth with mils, and the TRPs inside the sector
    within its range, with azimuth and range from that position. Grazing fire, dead space and the orientation diagram live on the
    range card the page exports (bare earth terrain the file does not carry); this table says so."""
    decl = DECL.get(plan.get("sheet") or "", 0)
    mag = lambda az: (az + decl) % 360
    out = []
    objs = plan.get("objects", [])
    marks = [o for o in objs if o.get("kind") == "point" and o.get("symbol") in TRP_SYMBOLS and o.get("utm")]
    for o in objs:
        props = o.get("props") or {}
        sec = props.get("sector")
        if not sec or o.get("kind") != "point" or o.get("side") != "friendly" or not o.get("utm"):
            continue
        c = o["utm"][0]
        left, right = sec.get("left"), sec.get("right")
        rng = sec.get("range") or 300
        row = {"label": o.get("label") or o.get("symbol"), "symbol": o.get("symbol"), "grid": grid8(c, square), "kind": sec.get("kind") or "primary", "range_m": rng}
        for k, v in (("lll", left), ("rll", right)):
            if v is not None:
                row[k + "_grid"] = round(v)
                row[k + "_mag"] = round(mag(v))
                row[k + "_mils"] = round(mag(v) * MILS)
        for k in ("fpl", "pdf"):
            d = sec.get(k)
            if d and d.get("az") is not None:
                row[k] = {"az_grid": round(d["az"]), "az_mag": round(mag(d["az"])), "mils": round(mag(d["az"]) * MILS), "len_m": d.get("len") or (600 if k == "fpl" else 400)}
        trps = []
        span = ((right - left) % 360) if (left is not None and right is not None) else 360
        for m in marks:
            q = m["utm"][0]
            d = dist(c, q)
            az = az_grid(c, q)
            if d > rng * 2 and d > 1800:
                continue
            if left is not None and right is not None and ((az - left) % 360) > span:
                continue
            trps.append({"label": m.get("label") or m.get("symbol"), "grid": grid8(q, square), "range_m": round(d), "az_grid": round(az), "az_mag": round(mag(az))})
        trps.sort(key=lambda t: t["range_m"])
        row["trps"] = trps
        out.append(row)
    return {"declination": decl, "positions": out, "note": "grazing fire, dead space and the orientation diagram are on the range card PNG the page exports for each gun (bare earth terrain, not in this file); the fire plan sketch PNG from the Plan menu is the sketch annex"}


def to_md(facts, brief):
    L = ["# Facts from the sand table export: " + facts["plan"], ""]
    L.append("Operation: %s. Sheet %s, grids %s %s, 8 digit (10 m). Grid azimuths computed from UTM; magnetic azimuths only where the brief gives them." % (facts["operation"], facts["sheet"] or "?", facts["gzd"], facts["square"]))
    if facts["aoi"]:
        L.append("Area of operations: SW %s, NE %s." % (facts["aoi"]["sw"], facts["aoi"]["ne"]))
    L.append("")
    L.append("## Fields, in the order the planner filled them")
    cur = None
    for f in facts["fields"]:
        if f["title"] != cur:
            cur = f["title"]
            L.append("")
            L.append("### " + cur)
        L.append("- %s: %s" % (f["key"], f["text"]))
    if facts["typed"]:
        L.append("")
        L.append("### Typed but not applied (the planner wrote these and did not press Apply; use them, and say so)")
        for f in facts["typed"]:
            L.append("- %s / %s: %s" % (f["title"], f["key"], f["text"]))
    L.append("")
    L.append("## Everything on the map")
    for o in facts["objects"]:
        line = "- %s (%s, %s): %s" % (o["label"], o["side"], o["symbol"], " to ".join(o["grids"]))
        if o.get("center"):
            line += "; center " + o["center"]
        if o.get("sector"):
            s = o["sector"]
            line += "; sector %s left %s right %s range %s m" % (s.get("kind", ""), s.get("left"), s.get("right"), s.get("range"))
        if o.get("fpl"):
            line += "; FPL az %s" % o["fpl"].get("az")
        if o.get("pdf"):
            line += "; PDF az %s" % o["pdf"].get("az")
        for k in ("task", "purpose", "remarks"):
            if o.get(k):
                line += "; %s %s" % (k, o[k])
        L.append(line)
    df = facts.get("direct_fire") or {}
    if df.get("positions"):
        L.append("")
        L.append("## Direct fire plan (sectors, FPLs, PDFs and TRPs from the map; magnetic = grid + %d)" % df.get("declination", 0))
        for r in df["positions"]:
            line = "- %s (%s, %s position) at %s: " % (r["label"], r["symbol"], r["kind"], r["grid"])
            if "lll_grid" in r and "rll_grid" in r:
                line += "LLL %03d grid (%03d mag, %d mils), RLL %03d grid (%03d mag, %d mils), sector length %s m" % (r["lll_grid"], r["lll_mag"], r["lll_mils"], r["rll_grid"], r["rll_mag"], r["rll_mils"], r["range_m"])
            else:
                line += "no limits set"
            for k in ("fpl", "pdf"):
                if r.get(k):
                    line += "; %s %03d grid (%03d mag, %d mils), %s m" % (k.upper(), r[k]["az_grid"], r[k]["az_mag"], r[k]["mils"], r[k]["len_m"])
            L.append(line)
            for t in r["trps"]:
                L.append("  - %s at %s: %d m, %03d grid (%03d mag)" % (t["label"], t["grid"], t["range_m"], t["az_grid"], t["az_mag"]))
        L.append("- " + df["note"])
    L.append("")
    L.append("## Routes (distance and grid azimuth per leg, computed)")
    for r in facts["routes"]:
        L.append("- %s: %s; total %d m" % (r["name"], " to ".join(r["grids"]), r["total_m"]))
        for l in r["legs"]:
            L.append("  - leg %d: %s to %s, %d m at %03d grid" % (l["leg"], l["from"], l["to"], l["dist_m"], l["az_grid"]))
        if brief["legs"].get(r["name"]):
            L.append("  - from the brief (magnetic): " + brief["legs"][r["name"]])
    L.append("")
    L.append("## Parts and events")
    for p in facts["parts"]:
        L.append("- " + str(p["name"]))
        for e in p["events"]:
            L.append("  - %s%s" % (e["name"], (" (trigger: %s)" % e["trigger"]) if e.get("trigger") else ""))
    if facts["notes"]:
        L.append("")
        L.append("## Notes")
        L.append(facts["notes"])
    if brief["checks"]:
        L.append("")
        L.append("## Checks the sand table ran (carry every warn into the order)")
        for c in brief["checks"]:
            if c["level"] != "ok":
                L.append("- (%s) %s: %s" % (c["level"], c["step"], c["text"]))
    return "\n".join(L) + "\n"


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    plan_path = argv[1]
    brief_path = None
    out_json = "facts.json"
    out_md = "facts.md"
    i = 2
    while i < len(argv):
        if argv[i] == "--json":
            out_json = argv[i + 1]
            i += 2
        elif argv[i] == "--md":
            out_md = argv[i + 1]
            i += 2
        else:
            brief_path = argv[i]
            i += 1
    facts = read_plan(plan_path)
    brief = read_brief(brief_path)
    facts["checks"] = brief["checks"]
    facts["brief_legs"] = brief["legs"]
    json.dump(facts, open(out_json, "w", encoding="utf-8"), indent=1)
    open(out_md, "w", encoding="utf-8").write(to_md(facts, brief))
    print("read %s: %d fields, %d typed, %d objects, %d routes, %d parts, %d grids; %d checks from the brief" % (
        facts["plan"], len(facts["fields"]), len(facts["typed"]), len(facts["objects"]), len(facts["routes"]), len(facts["parts"]), len(facts["grids"]), len(brief["checks"])))
    print("wrote", out_json, "and", out_md)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
