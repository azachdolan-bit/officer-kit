#!/usr/bin/env python3
"""sand-table-intake harness: the writer turns the fictional fixture facts into a plan file the page imports (every step of the
track present, higher's fields filled with their sources, the planner's blank, nothing on the map); the checker passes it
and fails each planted defect (an unknown field, a bad grid, a planner decision filled, a value without its paragraph, a
dash, objects on the map); order_text reads a docx. Usage: python3 evals/sand_table_intake_check.py"""
import json, os, re, subprocess, sys, tempfile, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(ROOT, "plugins", "officer-kit", "skills", "sand-table-intake", "scripts")
EV = os.path.join(ROOT, "evals", "sand-table-intake")
fails, n = [], 0
def ok(c, m):
    global n
    n += 1
    if not c: fails.append(m)
def run(*a):
    r = subprocess.run([sys.executable] + list(a), capture_output=True, text=True, cwd=EV)
    return r.returncode, r.stdout + r.stderr
tmp = tempfile.mkdtemp()
out = os.path.join(tmp, "fixture.sandtable.json")
code, txt = run(os.path.join(SC, "plan_writer.py"), "fixture-facts.json", "--out", out)
ok(code == 0, "writer should run:\n" + txt)
plan = json.load(open(out))
facts = json.load(open(os.path.join(EV, "fixture-facts.json")))
ok(plan["schema"] == 1 and re.fullmatch(r"plan_[a-z0-9]{10}", plan["id"]) and plan["sheet"] == "stex", "page shape: schema, id, sheet")
ok(plan["routes"] == [] and plan["phases"] == [], "no routes or phases: the page builds them")
ok(len(plan["objects"]) == 6 and all(o["id"].startswith("src_") and "from the base order" in o["props"]["remarks"] for o in plan["objects"]), "higher's positions and control measures are on the map with their source (%d)" % len(plan["objects"]))
kilo = [o for o in plan["objects"] if o["label"].startswith("1st Platoon")][0]
ok(kilo["kind"] == "point" and kilo["symbol"] == "inf_platoon" and kilo["utm"] == [[284550.0, 4212850.0]], "a 6 digit grid lands at the center of its 100 m square in UTM (%s)" % kilo["utm"])
en = [o for o in plan["objects"] if o["side"] == "enemy"][0]
ok(en["layer"] == "enemy" and en["symbol"] == "inf_squad", "an enemy object sits on the enemy layer")
V = plan["guide"]["values"]
ok(set(V) >= {"name", "ao", "mission", "enemy", "terrain", "troops", "time", "emlcoa", "cgcv", "ea", "type", "dist", "orient", "occ", "tcm", "sec", "obst", "parts", "tasks", "fsp", "coord", "admin"} and "oform" not in V, "every defense step present, no offense step (%s)" % sorted(V))
ok(V["name"]["optype"] == "platoon defense" and V["mission"]["mission"].startswith("2nd Platoon (ME)") and V["troops"]["adjl"] == "845128", "higher's values copied verbatim")
ok(all(v == "" for v in V["ea"].values()) and V["dist"]["sq1"] == {"role": "", "grid": ""} and V["fsp"]["tg1"]["grid"] == "", "the planner's fields are present and blank")
for f in facts["fields"]:
    ok(V[f["step"]][f["key"]] == f["value"], "value carried: %s/%s" % (f["step"], f["key"]))
src = open(re.sub(r"\.sandtable\.json$", ".sourced.md", out)).read()
ok("para 3.c.(1)" in src and "Left for the planner" in src and "EA: where to kill him" in src, "sourced.md cites paragraphs and lists the blanks")
code, txt = run(os.path.join(SC, "plan_check.py"), out, "--intake")
ok(code == 0 and "clean" in txt, "checker passes the good file:\n" + txt)
# planted defects, one at a time
def variant(mutate, name):
    f = json.load(open(os.path.join(EV, "fixture-facts.json")))
    mutate(f)
    p = os.path.join(tmp, name + ".json")
    json.dump(f, open(p, "w"))
    return run(os.path.join(SC, "plan_writer.py"), p, "--out", os.path.join(tmp, name + ".sandtable.json"))
code, txt = variant(lambda f: f["fields"].append({"step": "mission", "key": "nosuch", "value": "x", "src": "p"}), "unknown")
ok(code == 1 and "no such field" in txt, "writer refuses an unknown field")
code, txt = variant(lambda f: f["fields"].append({"step": "troops", "key": "m81", "value": "85201 310", "src": "p"}), "badgrid")
ok(code == 1 and "not a grid list" in txt, "writer refuses a grid that is not 4, 6 or 8 digits")
code, txt = variant(lambda f: f["fields"].append({"step": "fsp", "key": "fpfwpn", "value": "120mm", "src": "p"}), "badsel")
ok(code == 1 and "not one of" in txt, "writer refuses a select value the page does not offer")
code, txt = variant(lambda f: f["fields"].append({"step": "admin", "key": "epw", "value": "none stated"}), "nosrc")
ok(code == 1 and "needs its src" in txt, "writer refuses a value with no paragraph")
code, txt = variant(lambda f: f["fields"].append({"step": "oform", "key": "atype", "value": "hasty attack", "src": "p"}), "wrongtrack")
ok(code == 1 and "not on the defense track" in txt, "writer refuses an offense field on a defense plan")
code, txt = variant(lambda f: f["objects"].append({"label": "PL BLUE", "symbol": "pl", "grids": "84001150", "src": "p"}), "shortline")
ok(code == 1 and "needs at least 2 grids" in txt, "writer refuses a line with one grid")
code, txt = variant(lambda f: f["objects"].append({"label": "Something", "symbol": "inf_squad", "grids": "845128"}), "objnosrc")
ok(code == 1 and "needs its src" in txt, "writer refuses an object with no source")
code, txt = variant(lambda f: f["objects"].append({"label": "X", "symbol": "tank", "grids": "845128", "src": "p"}), "badsym")
ok(code == 1 and "unknown symbol" in txt, "writer refuses a symbol the page does not have")
code, txt = variant(lambda f: f["fields"].append({"step": "oform", "key": "atype", "value": "hasty attack", "src": "p"}), "wrongtrack2")
ok(code == 1 and "not on the defense track" in txt, "writer refuses an offense field on a defense plan")
# checker defects on the plan file itself
def plan_variant(mutate, name, flag="--intake"):
    p = json.load(open(out))
    mutate(p)
    q = os.path.join(tmp, name + ".sandtable.json")
    json.dump(p, open(q, "w"))
    return run(os.path.join(SC, "plan_check.py"), q, flag)
code, txt = plan_variant(lambda p: p["guide"]["values"]["ea"].__setitem__("why", "open ground"), "plannerfilled")
ok(code == 1 and "planner decision" in txt, "checker fails a planner decision filled by the intake")
code, txt = plan_variant(lambda p: p["objects"].append({"id": "x9", "label": "Ghost", "kind": "point", "side": "friendly", "symbol": "point", "utm": [[284000.0, 4211000.0]], "props": {"task": "", "purpose": "", "remarks": ""}}), "objnosrc2")
ok(code == 1 and "carries no source" in txt, "checker fails an intake object with no source in its remarks")
code, txt = plan_variant(lambda p: p["objects"].append({"id": "g_enlkl", "label": "EN", "kind": "point", "side": "enemy", "symbol": "inf_squad", "utm": [[284000.0, 4211000.0]], "props": {"task": "", "purpose": "", "remarks": "from the base order, p"}}), "guideid")
ok(code == 1 and "guide id" in txt, "checker fails an intake object that takes a guide id")
code, txt = plan_variant(lambda p: p["guide"]["values"]["time"].__setitem__("log", "smoke – 4"), "dash")
ok(code == 1 and "dash" in txt, "checker fails an en dash in a value")
code, txt = plan_variant(lambda p: p.__setitem__("sheet", "other"), "sheet")
ok(code == 1 and "sheet must be" in txt, "checker fails an unknown sheet")
code, txt = plan_variant(lambda p: p["guide"]["values"]["ea"].__setitem__("why", "open ground"), "plannerok", "")
ok(code == 0, "without --intake a planner value is fine (a planner's own export)")
# order_text reads a docx (built here, no packages)
dx = os.path.join(tmp, "order.docx")
with zipfile.ZipFile(dx, "w") as z:
    z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
    z.writestr("word/document.xml", '<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>2. Mission. NLT 1900, Bravo Company blocks south.</w:t></w:r></w:p><w:p><w:r><w:t xml:space="preserve">3. Execution</w:t></w:r></w:p></w:body></w:document>')
code, txt = run(os.path.join(SC, "order_text.py"), dx, "--out", os.path.join(tmp, "order.txt"))
ok(code == 0 and open(os.path.join(tmp, "order.txt")).read().startswith("2. Mission. NLT 1900") and "3. Execution" in open(os.path.join(tmp, "order.txt")).read(), "order_text reads a docx paragraph by paragraph")
# the field list matches what the sand-table-order reader titles
gf = json.load(open(os.path.join(ROOT, "plugins", "officer-kit", "skills", "sand-table-intake", "references", "guide_fields.json")))
ok(len(gf) >= 27 and sum(len(s["fields"]) for s in gf) >= 170, "guide_fields.json carries the page's steps and fields (%d steps)" % len(gf))
# the fixture order is fictional and dash free
fx = open(os.path.join(EV, "fixture-base-order.md"), encoding="utf-8").read()
ok("fictional" in fx and not re.search("[–—]", fx), "fixture order is marked fictional and carries no dashes")
# the troop to task reader (0.3.0): the fictional matrix to a plan file the page walks by the clock
t2 = os.path.join(tmp, "t2t.sandtable.json")
code, txt = run(os.path.join(SC, "t2t_reader.py"), "fixture-troop-to-task.csv", "--out", t2, "--rehearsal")
ok(code == 0 and "10 rows, 6 slots from 1300" in txt, "t2t_reader reads the fixture matrix:\n" + txt)
tp = json.load(open(t2)); T = tp.get("t2t") or {}
ok(T.get("slots") == 6 and T.get("x") == "1300" and len(T.get("rows", [])) == 10 and T["cols"][2]["clock"] == "1400", "the matrix carries 6 slots from 1300 with the clock per column")
rows = {(r["group"], r["short"]): r for r in T["rows"]}
ft2 = rows.get(("1st Sqd", "2nd FT")); ft1 = rows.get(("2nd Sqd", "1st FT"))
ok(ft2 and ft2["strength"] == 4 and ft2["standing"] == [{"n": 2, "to": "lpop", "from": 840, "until": 930}], "a row name's standing pair on the LP/OP with its clock window is read (%s)" % (ft2 and ft2["standing"]))
ok(ft1 and ft1["cells"][2]["away"] == [{"n": 2, "to": "gate"}] and ft1["cells"][2]["dig"] == 2 and ft1["cells"][4]["patrol"], "a cell's (2 on MACO), its diggers and DAY PATROL are read")
sl = rows.get(("1st Sqd", "1st Squad, left")); ok(sl and sl["kind"] == "sl" and sl["cells"][1]["leaderAt"] == "tm" and sl["cells"][3]["leaderAt"] == "cp", "a leader row reads terrain model and brief")
sys.path.insert(0, SC); import t2t_reader as R
sec = [R.security(T, i) for i in range(6)]
ok(all("%d/%d" % (sec[i]["sec"], sec[i]["present"]) == T["security"][i].split(" / ")[0] for i in range(6)), "the security count matches the fixture's own row on every slot (%s)" % ["%d/%d" % (x["sec"], x["present"]) for x in sec])
st = R.row_state(T, ft2, 3); ok(st["present"] == 2 and st["away"] == [{"n": 2, "to": "lpop", "standing": True}], "a blank cell continues the entry: at 1430 the pair is still on the LP/OP and 2 remain")
ok(len(tp["phases"]) == 3 and [len(x["events"]) for x in tp["phases"]] == [2, 2, 2] and tp["phases"][0]["name"] == "1300 Stand to" and tp["phases"][1]["events"][0]["t2tSlot"] == 2 and "Security on the line" in tp["phases"][0]["events"][0]["narration"], "--rehearsal builds a phase per milestone and an event per changed slot carrying its slot and the security line")
rep = open(os.path.join(tmp, "t2t.t2t.md"), encoding="utf-8").read(); ok("## Security on the line by slot" in rep and "1st Sqd 2nd FT, else 1st Sqd" in rep, "the report lists what the page will look for and the security table")
# merging into an existing plan keeps its objects and non matrix phases
base = json.load(open(out)); base["phases"] = [{"id": "ph_keep", "name": "Kept", "events": []}]; bp = os.path.join(tmp, "base.sandtable.json"); json.dump(base, open(bp, "w"))
code, txt = run(os.path.join(SC, "t2t_reader.py"), "fixture-troop-to-task.csv", "--plan", bp, "--rehearsal")
mp = json.load(open(bp)); ok(code == 0 and len(mp["objects"]) == len(base["objects"]) and mp["phases"][0]["name"] == "Kept" and len(mp["phases"]) == 4 and mp.get("t2t", {}).get("slots") == 6, "--plan merges the matrix into an existing plan file, keeping its objects and its own phases")
code, txt = run(os.path.join(SC, "plan_check.py"), bp)
ok(code == 0, "the checker passes the base order's plan file once it carries the matrix and its rehearsal (a planner's file, not an intake file):\n" + txt)
fx2 = open(os.path.join(EV, "fixture-troop-to-task.csv"), encoding="utf-8").read(); ok("fictional" in fx2 and not re.search("[\u2013\u2014]", fx2), "the fixture matrix is marked fictional and carries no dashes")
print("sand-table-intake check: %d items, %d failed" % (n, len(fails)))
for f in fails:
    print("  FAIL", f)
sys.exit(1 if fails else 0)
