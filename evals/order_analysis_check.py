#!/usr/bin/env python3
"""order-analysis harness: grid arithmetic against hand values, the direction table, grid extraction
and two-grid candidates on a fictional order, the checker passing a good analysis and failing each
planted defect in a bad one, and map calibration flagging a scan that is not square.
Usage: python3 evals/order_analysis_check.py"""
import json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(ROOT, "plugins", "officer-kit", "skills", "order-analysis", "scripts")
EV = os.path.join(ROOT, "evals", "order-analysis")
sys.path.insert(0, SC)
import grid_tool as G
fails, n = [], 0
def ok(c, m):
    global n
    n += 1
    if not c: fails.append(m)
def run(*a):
    r = subprocess.run([sys.executable] + list(a), capture_output=True, text=True, cwd=EV)
    return r.returncode, r.stdout + r.stderr
m = G.measure("QS 400 500", "QS 403 504")
ok(m["distance_m"] == 500, "3-4-5 distance should be 500 m, got %s" % m["distance_m"])
ok(m["azimuth_mils"] == round(36.87 * 6400 / 360), "azimuth of a 3-4-5 leg should be 36.9 degrees in mils")
ok(m["error_budget_m"] == 141, "two 6 digit grids carry a 141 m worst case budget, got %s" % m["error_budget_m"])
ok(G.measure("QS 4000 5000", "QS 4000 5100")["azimuth_mils"] == 0, "due north is 0 mils")
ok(G.measure("QS 4000 5000", "QS 3900 5000")["azimuth_mils"] == 4800, "due west is 4800 mils")
ok(G.dir_mils("NW") == 5600 and G.dir_mils("northwest") == 5600, "northwest is 5600 mils")
ok(G.dir_mils("SE") == 2400 and G.word_of(1000) == "ENE", "direction table")
try:
    G.measure("QS 400 500", "QT 400 500"); ok(False, "different squares must refuse")
except ValueError:
    ok(True, "")
rows = G.extract(open(os.path.join(EV, "order.txt")).read())
ok(any(r["grid"] == "AB 2001" and r["other_square"] for r in rows), "a target number must be marked as another square")
c = G.candidates(rows)
ok(any(x["name"] == "assault position" and not x["inside_budget"] for x in c), "the assault position given two grids should be a candidate")
ok(not any(x["name"] == "obj a" for x in c), "Obj A given the same grid three times is not a candidate")
code, out = run(os.path.join(SC, "analysis_check.py"), "good-analysis.json", "order.txt")
ok(code == 0, "good analysis should pass:\n" + out)
code, out = run(os.path.join(SC, "analysis_check.py"), "bad-analysis.json", "order.txt")
ok(code == 1, "bad analysis should fail")
for needle, why in (("decode it in 'legend'", "undecoded columns"), ("quote not in the order", "invented quote"), ("is 423 m, not 250", "wrong distance"),
                    ("no gate1 verdict", "missing gate record"), ("sequence finding before", "sequence without legend"), ("5600 mils, not 5400", "northwest by hand"),
                    ("no locator", "fact without paragraph")):
    ok(needle in out, "bad analysis should fail on " + why)
bad2 = json.load(open(os.path.join(EV, "good-analysis.json"))); bad2["legend"][0]["source"] = "references/not-a-defect.md item 2"
tmp = tempfile.mkdtemp(); bp = os.path.join(tmp, "b2.json"); json.dump(bad2, open(bp, "w"))
code, out = run(os.path.join(SC, "analysis_check.py"), bp, "order.txt")
ok(code == 1 and "kit's own reference" in out, "a legend decoded from the kit's reference must fail")
pts = os.path.join(tmp, "p.json")
json.dump([{"px": [0, 0], "grid": "QS 40000 50000"}, {"px": [1000, 0], "grid": "QS 41000 50000"}, {"px": [0, -900], "grid": "QS 40000 51000"}, {"px": [1000, -900], "grid": "QS 41000 51000"}], open(pts, "w"))
code, out = run(os.path.join(SC, "map_calibrate.py"), pts)
ok(code == 0 and "NOT SQUARE" in out, "a 1000 by 900 pixel per km scan should be flagged not square:\n" + out)
print("ORDER ANALYSIS CHECK: %d items" % n)
for f in fails: print("  FAIL ", f)
print("-> %d of %d pass" % (n - len(fails), n))
sys.exit(1 if fails else 0)
