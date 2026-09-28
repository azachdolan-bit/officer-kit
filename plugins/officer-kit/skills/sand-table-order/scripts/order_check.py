#!/usr/bin/env python3
"""Check a drafted order against the facts read from a sand table export. Exit 0 = the order carries the plan and invents nothing.

Usage: python3 order_check.py <order.md> <facts.json>

Fails when:
  1. an 8 digit grid in the order is not a grid in the plan (a typo, or an invented position);
  2. a placed object, a route, or a part from the plan is missing from the order (by label or name);
  3. a short field value (a grid, a name, a time, a number, a select) from the plan does not appear in the order and is not
     listed under NOT IN THE PLAN; long text fields are checked by their first five words;
  4. a warn check from the sand table's brief is not carried into the order's "Warnings carried" list;
  5. the five paragraph headings are not all present (Situation, Mission, Execution, Administration and Logistics, Command and Signal);
  6. the order has no "NOT IN THE PLAN" list (even an empty one must say so);
  7. an em dash or en dash appears (kit standard 9);
  8. a sector limit, FPL or PDF azimuth from the direct fire plan (grid, three digits) is not in the order and not under NOT IN THE PLAN.
"""
import json
import re
import sys

HEADINGS = ["Situation", "Mission", "Execution", "Administration and Logistics", "Command and Signal"]
SKIP_KEYS = {"optype", "notes", "name", "ao", "squares", "pace", "gate", "third"}


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def words(s):
    return " ".join(re.findall(r"[a-z0-9']+", str(s).lower()))


def first_words(s, n=5):
    w = re.findall(r"[A-Za-z0-9']+", str(s))
    return " ".join(w[:n]).lower()


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    order = open(argv[1], encoding="utf-8").read()
    facts = json.load(open(argv[2], encoding="utf-8"))
    low = norm(order)
    lowords = words(order)
    fails = []
    # 1. grids in the order exist in the plan
    plan_grids = set(facts.get("grids", []))
    for g in set(re.findall(r"\b(\d{4}) ?(\d{4})\b", order)):
        d = g[0] + g[1]
        if d not in plan_grids and not re.fullmatch(r"(19|20)\d{6}", d):
            fails.append("grid %s %s is not in the plan (typo or invented)" % g)
    # 2. every object, route and part is in the order
    for o in facts.get("objects", []):
        lab = o.get("label") or ""
        if lab and norm(lab) not in low and norm(re.sub(r"\s*\(.*?\)", "", lab)) not in low:
            fails.append("object '%s' from the map is not in the order" % lab)
    for r in facts.get("routes", []):
        if norm(r.get("name", "")) not in low:
            fails.append("route '%s' is not in the order" % r.get("name"))
    for p in facts.get("parts", []):
        if norm(p.get("name", "")) not in low:
            fails.append("part '%s' is not in the order" % p.get("name"))
    # 3. field values
    nip = ""
    m = re.search(r"NOT IN THE PLAN[\s\S]*", order)
    if m:
        nip = norm(m.group(0))
    for f in facts.get("fields", []) + facts.get("typed", []):
        if f["key"] in SKIP_KEYS:
            continue
        val = f["value"]
        items = []
        if isinstance(val, dict):
            items = [str(x) for x in val.values() if x not in (None, "")]
        else:
            items = [str(val)]
        for it in items:
            it = it.strip()
            if not it:
                continue
            if re.fullmatch(r"[\d\s\n]+", it):
                digits = [d for d in re.findall(r"\d{8}", it)]
                for d in digits:
                    if not re.search(d[:4] + r" ?" + d[4:], order):
                        fails.append("%s/%s: grid %s from the plan is not in the order" % (f["step"], f["key"], d))
                continue
            pieces = [x.strip() for x in re.split(r"[\n;]+", it) if x.strip()] if ("\n" in it or len(it) > 60) else [it]
            for piece in pieces:
                key = words(piece) if len(piece) <= 60 else first_words(piece)
                if key and key not in lowords and key not in words(nip):
                    fails.append("%s/%s: '%s' from the plan is not in the order" % (f["step"], f["key"], piece[:60]))
    # 4. warn checks carried
    warns = [c for c in facts.get("checks", []) if c.get("level") == "warn"]
    if warns:
        wm = re.search(r"Warnings carried[\s\S]*", order)
        wtxt = norm(wm.group(0)) if wm else ""
        for c in warns:
            if first_words(c["text"], 4) not in wtxt:
                fails.append("warn check not carried: " + c["text"][:80])
    # 5. headings
    for h in HEADINGS:
        if not re.search(r"(?im)^\s*(#+\s*)?(\d+\.\s*)?" + re.escape(h) + r"\b", order):
            fails.append("heading missing: " + h)
    # 6. NOT IN THE PLAN list
    if not m:
        fails.append("no NOT IN THE PLAN list (write the heading even when nothing is missing)")
    # 7. dashes
    if re.search("[\\u2013\\u2014]", order):
        fails.append("em or en dash in the order (kit standard 9)")
    # 8. direct fire azimuths (three digit grid) are in the order
    for r in (facts.get("direct_fire") or {}).get("positions", []):
        wanted = []
        if "lll_grid" in r and "rll_grid" in r:
            wanted += [("LLL", r["lll_grid"]), ("RLL", r["rll_grid"])]
        for k in ("fpl", "pdf"):
            if r.get(k):
                wanted.append((k.upper(), r[k]["az_grid"]))
        for what, az in wanted:
            a3 = "%03d" % az
            if not re.search(r"(?<!\d)" + a3 + r"(?!\d)", order) and a3 not in nip:
                fails.append("%s: %s azimuth %s grid from the direct fire plan is not in the order" % (r["label"], what, a3))
    print("ORDER CHECK: %d objects, %d routes, %d parts, %d fields, %d warns" % (len(facts.get("objects", [])), len(facts.get("routes", [])), len(facts.get("parts", [])), len(facts.get("fields", [])), len(warns)))
    for x in fails:
        print("  FAIL ", x)
    if not fails:
        print("  clean: every fact in the plan is in the order, and nothing in the order is outside the plan")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
