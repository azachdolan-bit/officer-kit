#!/usr/bin/env python3
"""Check a sand table plan file before it goes to the planner: the same shape the page's own validator accepts, the guide
keys the page knows, grids that parse, and (for an intake file) nothing on the map that the order did not put there.

Usage: python3 plan_check.py <name>.sandtable.json [--intake]

Fails when:
  1. the top level keys are not the page's (schema 1, id, name, owner, created, updated, saveId, sheet, aoi, objects, routes,
     custom, phases, notes, guide);
  2. sheet is not one the page carries (ta16, stex);
  3. a guide step or field key is unknown to the page (references/guide_fields.json), or a value has the wrong shape;
  4. a grid field carries something that is not a 4, 6 or 8 digit grid;
  5. with --intake: objects, routes or phases are not empty (the page builds them from the values), or a planner decision
     step (EMLCOA, CG/CV, EA, BP, distribution, orientation, occupation, security, obstacles, parts, tasks, targets,
     engagement criteria, or the offense scheme) carries a value, since the base order does not make those decisions;
  6. an em dash or en dash is in a value (kit standard 9; the order's own dashes are copied as hyphens or words).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = {s["id"]: s for s in json.load(open(os.path.join(HERE, "..", "references", "guide_fields.json"), encoding="utf-8"))}
TOP = ["schema", "id", "name", "owner", "created", "updated", "saveId", "sheet", "aoi", "objects", "routes", "custom", "phases", "notes", "guide"]
SHEETS = ("ta16", "stex")
GRID_TYPES = {"place", "points", "draw", "area"}
PLANNER_STEPS = {"emlcoa", "cgcv", "ea", "type", "dist", "orient", "occ", "sec", "obst", "oform", "oto", "otcm", "oseq", "parts", "tasks"}
PLANNER_KEYS = {("fsp", "tg1"), ("fsp", "tg2"), ("fsp", "tg3"), ("fsp", "tg4"), ("fsp", "fpfc"), ("fsp", "fpfatt"), ("fsp", "fpflen"), ("fsp", "fpftrig"), ("coord", "engfar"), ("coord", "engnear"), ("tcm", "cps"), ("admin", "ccp"), ("admin", "casroute")}


def grids_ok(text):
    toks = [t for t in re.split(r"[\s,;]+", str(text).strip()) if t]
    return all(re.fullmatch(r"\d{4}|\d{6}|\d{8}", t) for t in toks)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    intake = "--intake" in argv
    p = json.load(open(argv[1], encoding="utf-8"))
    fails = []
    missing = [k for k in TOP if k not in p]
    if missing:
        fails.append("top level keys missing: " + ", ".join(missing))
    if p.get("schema") != 1:
        fails.append("schema must be 1")
    if not re.fullmatch(r"plan_[a-z0-9]{10}", str(p.get("id", ""))):
        fails.append("id must be plan_ and ten lowercase letters or digits")
    if p.get("sheet") not in SHEETS:
        fails.append("sheet must be one of %s" % (SHEETS,))
    for k in ("objects", "routes", "custom", "phases"):
        if not isinstance(p.get(k), list):
            fails.append(k + " must be a list")
    if p.get("aoi") is not None:
        a = p["aoi"]
        if not (isinstance(a, dict) and all(isinstance(a.get(x), (int, float)) for x in ("e0", "n0", "e1", "n1")) and a["e1"] > a["e0"] and a["n1"] > a["n0"]):
            fails.append("aoi must be null or {e0, n0, e1, n1} UTM with e1 > e0 and n1 > n0")
    V = (p.get("guide") or {}).get("values")
    if not isinstance(V, dict):
        fails.append("guide.values missing")
        V = {}
    filled = 0
    for step, vals in V.items():
        if step not in FIELDS:
            fails.append("unknown guide step '%s'" % step)
            continue
        if not isinstance(vals, dict):
            fails.append("%s: values must be an object" % step)
            continue
        defs = {f["k"]: f for f in FIELDS[step]["fields"]}
        for key, val in vals.items():
            where = "%s/%s" % (step, key)
            f = defs.get(key)
            if not f:
                fails.append("%s: unknown field" % where)
                continue
            empty = val in ("", None) or (isinstance(val, dict) and all(x in ("", None) for x in val.values()))
            if not empty:
                filled += 1
            if f["t"] in ("unit", "target"):
                if not isinstance(val, dict):
                    fails.append("%s: must be an object" % where)
                    continue
                if val.get("grid") and not grids_ok(val["grid"]):
                    fails.append("%s: grid must be 4, 6 or 8 digits" % where)
                texts = [str(x) for x in val.values()]
            else:
                if not isinstance(val, str):
                    fails.append("%s: must be text" % where)
                    continue
                if f["t"] in GRID_TYPES and val and not grids_ok(val):
                    fails.append("%s: '%s' is not a grid list" % (where, val[:40]))
                if f["t"] == "select" and val and f.get("opts") and val not in f["opts"]:
                    fails.append("%s: '%s' is not one of %s" % (where, val, f["opts"]))
                texts = [val]
            for t in texts:
                if re.search("[\\u2013\\u2014]", t):
                    fails.append("%s: em or en dash in the value (kit standard 9)" % where)
            if intake and not empty and key not in ("optype", "name", "notes") and (step in PLANNER_STEPS or (step, key) in PLANNER_KEYS):
                fails.append("%s: a planner decision was filled by the intake; the base order does not decide it" % where)
    if intake:
        for k in ("objects", "routes", "phases"):
            if p.get(k):
                fails.append("%s must be empty in an intake file: the page builds them from the values" % k)
    print("PLAN CHECK: %s, sheet %s, %d steps, %d fields filled%s" % (p.get("name"), p.get("sheet"), len(V), filled, ", intake rules on" if intake else ""))
    for x in fails:
        print("  FAIL ", x)
    if not fails:
        print("  clean: the page will import it")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
