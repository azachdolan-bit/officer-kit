#!/usr/bin/env python3
"""sand-table-order harness: the reader lays out every fact from a fictional sand table export (fields, typed text, objects
with 8 digit grids from UTM, routes with computed legs, parts, the brief's checks); the checker passes an order written
from it and fails each planted defect in a bad one (an invented grid, a dropped object, a dropped field, a warn not
carried, a dash, a task without a condition or purpose, an EMLCOA that is not a tasking statement, a target
without its net; coverage of the plan is advisory unless --full). Usage: python3 evals/sand_table_order_check.py"""
import json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(ROOT, "plugins", "officer-kit", "skills", "sand-table-order", "scripts")
EV = os.path.join(ROOT, "evals", "sand-table-order")
fails, n = [], 0
def ok(c, m):
    global n
    n += 1
    if not c: fails.append(m)
def run(*a):
    r = subprocess.run([sys.executable] + list(a), capture_output=True, text=True, cwd=EV)
    return r.returncode, r.stdout + r.stderr
tmp = tempfile.mkdtemp()
fj, fm = os.path.join(tmp, "facts.json"), os.path.join(tmp, "facts.md")
code, out = run(os.path.join(SC, "plan_reader.py"), "fixture.sandtable.json", "fixture.sandtable-brief.md", "--json", fj, "--md", fm)
ok(code == 0, "reader should run:\n" + out)
facts = json.load(open(fj))
ok(facts["operation"] == "platoon defense" and facts["square"] == "TH", "operation and square read from the plan")
ok(len(facts["fields"]) >= 100, "every filled field is read (%d)" % len(facts["fields"]))
ok(len(facts["objects"]) == 37 and len(facts["routes"]) == 3 and len(facts["parts"]) == 2, "objects, routes and parts counted")
en = [o for o in facts["objects"] if o["id"] == "g_enlkl"][0]
ok(en["grids"] == ["TH 8680 7750"], "an object's UTM becomes its 8 digit grid (%s)" % en["grids"])
bp = [o for o in facts["objects"] if o["id"] == "g_sq2"][0]
ok(bp.get("sector") and bp["sector"]["kind"] == "primary" and "left" in bp["sector"], "a squad's sector of fire is read")
mg = [o for o in facts["objects"] if o["id"] == "g_mgL"][0]
ok(mg.get("fpl") and "az" in mg["fpl"], "a gun's FPL azimuth is read")
df = facts.get("direct_fire") or {}
mg1 = [r for r in df.get("positions", []) if r["label"] == "MG 1"]
ok(df.get("declination") == 11 and len(df.get("positions", [])) == 6 and mg1 and mg1[0]["fpl"]["az_grid"] == 317 and mg1[0]["fpl"]["az_mag"] == 328 and mg1[0]["fpl"]["mils"] == 5831 and mg1[0]["lll_grid"] == 205 and mg1[0]["rll_mag"] == 317, "the direct fire plan lists every position with a sector: limits and FPL in grid and magnetic with mils (%s)" % (mg1[0] if mg1 else None))
sq1 = [r for r in df.get("positions", []) if r["label"] == "1st Sqd (SE1)"][0]
ok(any(t["label"] == "TRP 1" and t["range_m"] == 286 and t["az_grid"] == 245 for t in sq1["trps"]) and all(((t["az_grid"] - 197) % 360) <= 101 for t in sq1["trps"]), "TRPs inside a sector are listed with range and azimuth from that position; none outside it")
ok("## Direct fire plan" in open(fm).read() and "FPL 317 grid (328 mag, 5831 mils)" in open(fm).read() and "range card PNG" in open(fm).read(), "facts.md carries the direct fire plan and points to the range card for dead space")
cas = [r for r in facts["routes"] if r["id"] == "g_r_cas"][0]
ok(len(cas["legs"]) == 2 and cas["legs"][0]["dist_m"] > 0 and 0 <= cas["legs"][0]["az_grid"] < 360, "route legs get a computed distance and grid azimuth")
ok(any(c["level"] == "warn" for c in facts["checks"]), "the brief's warn checks are read")
ok(facts["aoi"] == {"sw": "TH 8600 7700", "ne": "TH 8800 7800"}, "the AO corners are read (%s)" % facts["aoi"])
md = open(fm).read()
ok("## Everything on the map" in md and "1st Sqd (SE1)" in md and "leg 1:" in md, "facts.md carries the map and the legs")
# typed but unapplied text is read and marked
p = json.load(open(os.path.join(EV, "fixture.sandtable.json")))
p.setdefault("guide", {})["typed"] = {"coord": {"other": "TYPED_ONLY_MARKER"}}
tp = os.path.join(tmp, "typed.sandtable.json"); json.dump(p, open(tp, "w"))
code, out = run(os.path.join(SC, "plan_reader.py"), tp, "--json", os.path.join(tmp, "t.json"), "--md", os.path.join(tmp, "t.md"))
ok(code == 0 and "TYPED_ONLY_MARKER" in open(os.path.join(tmp, "t.md")).read() and "not applied" in open(os.path.join(tmp, "t.md")).read(), "typed but unapplied text is read and marked")
code, out = run(os.path.join(SC, "order_check.py"), "good-order.md", fj)
ok(code == 0, "good order should pass:\n" + out)
code, out = run(os.path.join(SC, "order_check.py"), "bad-order.md", fj)
ok(code == 1, "bad order should fail")
for needle, what in (("8680 7705 is not in the plan", "invented grid"), ("warn check not carried", "warn not carried"), ("em or en dash", "dash"),
                     ("FPL azimuth 317 grid from the direct fire plan is not in the order", "dropped FPL azimuth"),
                     ("task statement has no purpose (IOT)", "task without a purpose"), ("communication elements", "target without a net")):
    ok(("FAIL  " in out) and needle in out, "bad order: %s not caught" % what)
# coverage is advisory by default (the order is lean); --full restores it as a failure
ok("NOT CARRIED (advisory, lives in facts.md)  object '1st Sqd SUPP' from the map is not in the order" in out and "admin/resupply" in out, "bad order: dropped object and field reported as advisory")
code, outf = run(os.path.join(SC, "order_check.py"), "bad-order.md", fj, "--full")
ok(code == 1 and "FAIL  object '1st Sqd SUPP' from the map is not in the order" in outf, "--full makes a dropped object a failure")
# planted defects on the lean good order: EMLCOA without a purpose, a task without a condition, a target without its net
good = open(os.path.join(EV, "good-order.md"), encoding="utf-8").read()
for change, needle, what in (
        (("The enemy platoon seizes the crossroads along EN AA 1 IOT open the road east.", "The enemy platoon is reconnoitering the approaches."), "EMLCOA is not a tasking statement", "EMLCOA without a tactical task and purpose"),
        (("1st Sqd. SE1. Upon the enemy crossing TL AMBER, block", "1st Sqd. SE1. Block"), "task statement has no condition", "task without a condition"),
        (("C: 81s COF net.\n", ""), "communication elements", "target without a net"),
        (("(2) Adjacent. Units at", "(2) Higher's intent. PURPOSE: protect the trains. END STATE: the enemy is blocked.\n(3) Adjacent. Units at"), "higher's intent in 1.b", "higher's intent pasted into 1.b")):
    assert change[0] in good, change[0]
    tp = os.path.join(tmp, "variant.md"); open(tp, "w", encoding="utf-8").write(good.replace(change[0], change[1]))
    code, outv = run(os.path.join(SC, "order_check.py"), tp, fj)
    ok(code == 1 and needle in outv, "good order variant: %s not caught:\n%s" % (what, outv[-400:]))
print("SAND TABLE ORDER CHECK: %d items" % n)
for f in fails: print("  FAIL ", f)
print("-> %d of %d pass" % (n - len(fails), n))
sys.exit(1 if fails else 0)
