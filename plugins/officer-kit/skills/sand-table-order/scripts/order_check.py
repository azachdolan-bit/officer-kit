#!/usr/bin/env python3
"""Check a drafted order against the facts read from a sand table export. Exit 0 = the order carries the plan and invents nothing.

Usage: python3 order_check.py <order.md> <facts.json> [--full]

The order is lean (the density of the user's own official orders); full coverage of the plan lives in facts.md.
Coverage (checks 2 and 3) is therefore reported as advisory "NOT CARRIED" lines and does not fail the order,
unless --full is given, which restores them as failures for a user who wants every fact in the order.

Fails when:
  1. an 8 digit grid in the order is not a grid in the plan (a typo, or an invented position);
  2. (--full only) a placed object, a route, or a part from the plan is missing from the order (by label or name);
  3. (--full only) a field value from the plan does not appear in the order and is not listed under NOT IN THE PLAN;
  4. a warn check from the sand table's brief is not carried into the order's "Warnings carried" list;
  5. the five paragraph headings are not all present (Situation, Mission, Execution, Administration and Logistics, Command and Signal);
  6. the order has no "NOT IN THE PLAN" list (even an empty one must say so);
  7. an em dash or en dash appears (kit standard 9);
  8. a sector limit, FPL or PDF azimuth from the direct fire plan is not in the order, in grid or in magnetic, and not under NOT IN THE PLAN;
  9. the EMLCOA is missing, or its first sentence is not a tasking statement (no IOT purpose);
 10. a task statement under Tasks lacks a condition (Upon, On order, O/O, NLT, When) or a purpose (IOT);
 11. a planned target or the FPF has no communication element (C: or Communication:) in the fire support plan;
 12. paragraph 1.b (Friendly, up to the Mission paragraph) carries higher's intent: an intent heading, or PURPOSE:, METHOD: or END STATE text.
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
    full = "--full" in argv
    argv = [a for a in argv if a != "--full"]
    if len(argv) != 3:
        print(__doc__)
        return 2
    order = open(argv[1], encoding="utf-8").read()
    facts = json.load(open(argv[2], encoding="utf-8"))
    adv = []
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
            (fails if full else adv).append("object '%s' from the map is not in the order" % lab)
    for r in facts.get("routes", []):
        if norm(r.get("name", "")) not in low:
            (fails if full else adv).append("route '%s' is not in the order" % r.get("name"))
    for p in facts.get("parts", []):
        if norm(p.get("name", "")) not in low:
            (fails if full else adv).append("part '%s' is not in the order" % p.get("name"))
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
                        (fails if full else adv).append("%s/%s: grid %s from the plan is not in the order" % (f["step"], f["key"], d))
                continue
            pieces = [x.strip() for x in re.split(r"[\n;]+", it) if x.strip()] if ("\n" in it or len(it) > 60) else [it]
            for piece in pieces:
                key = words(piece) if len(piece) <= 60 else first_words(piece)
                if key and key not in lowords and key not in words(nip):
                    (fails if full else adv).append("%s/%s: '%s' from the plan is not in the order" % (f["step"], f["key"], piece[:60]))
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
        mags = {"LLL": r.get("lll_mag"), "RLL": r.get("rll_mag")}
        for k in ("fpl", "pdf"):
            if r.get(k):
                wanted.append((k.upper(), r[k]["az_grid"]))
                mags[k.upper()] = r[k].get("az_mag")
        for what, az in wanted:
            a3 = "%03d" % az
            m3 = "%03d" % mags[what] if mags.get(what) is not None else None
            found = re.search(r"(?<!\d)" + a3 + r"(?!\d)", order) or (m3 and re.search(r"(?<!\d)" + m3 + r"(?!\d)", order))
            if not found and a3 not in nip:
                fails.append("%s: %s azimuth %s grid from the direct fire plan is not in the order" % (r["label"], what, a3))
    # 9. EMLCOA as a tasking statement
    em = re.search(r"EMLCOA\W*\s*([^\n]*)", order)
    if not em:
        fails.append("no EMLCOA in the order")
    else:
        first = re.split(r"(?<=[.;])\s", em.group(1).strip())[0]
        if not re.search(r"\bIOT\b|\bin order to\b", first, re.I):
            fails.append("EMLCOA is not a tasking statement: its first sentence has no IOT purpose (%s)" % first[:80])
    # 10. task statements: condition and purpose
    tm = re.search(r"(?im)^[^\n]*\bTasks\b[^\n]*$([\s\S]*?)^[^\n]*Coordinating instructions", order)
    if tm:
        for line in tm.group(1).splitlines():
            t = line.strip(" -*#\t")
            if len(t) < 40 or re.match(r"^(\(?\w{1,3}[.)]\s*)?Part \d", t, re.I) and len(t) < 70:
                continue
            if not re.search(r"\b(upon|on order|o/o|nlt|when)\b", t, re.I):
                fails.append("task statement has no condition (Upon, On order, NLT): %s" % t[:80])
            if not re.search(r"\bIOT\b|\bin order to\b", t, re.I):
                fails.append("task statement has no purpose (IOT): %s" % t[:80])
    else:
        fails.append("no Tasks paragraph before the coordinating instructions")
    # 11. every planned target and the FPF carries its communication element
    ntg = sum(1 for f in facts.get("fields", []) if f.get("step") == "fsp" and re.fullmatch(r"tg\d", f.get("key", "")) and f.get("value"))
    ntg += 1 if any(f.get("step") == "fsp" and f.get("key") == "fpfc" and f.get("value") for f in facts.get("fields", [])) else 0
    ncom = len(re.findall(r"(?m)(^\s*C\s*[:\-]\s*\S)|(\bCommunication\s*:\s*\S)", order))
    if ntg and ncom < ntg:
        fails.append("%d planned targets (FPF included) but %d communication elements: give each its net (for example 60s COF net)" % (ntg, ncom))
    # 12. 1.b carries higher's mission, adjacent and supporting only; never higher's intent
    fm = re.search(r"(?im)^[^\n]*\bFriendly\b[^\n]*$([\s\S]*?)^\s*(#+\s*)?(\d\.\s*)?Mission\b", order)
    if fm:
        hit = re.search(r"(?i)\bintent\b|\bpurpose\s*:|\bmethod\s*:|\bend ?state\b", fm.group(1))
        if hit:
            fails.append("higher's intent in 1.b (%s): 1.b is higher's mission, adjacent and supporting only" % hit.group(0))
    print("ORDER CHECK: %d objects, %d routes, %d parts, %d fields, %d warns" % (len(facts.get("objects", [])), len(facts.get("routes", [])), len(facts.get("parts", [])), len(facts.get("fields", [])), len(warns)))
    for x in fails:
        print("  FAIL ", x)
    for x in adv:
        print("  NOT CARRIED (advisory, lives in facts.md) ", x)
    if not fails:
        print("  clean: nothing in the order is outside the plan" + (", and every fact in the plan is in it" if full else "; coverage advisories above are carried in facts.md"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
