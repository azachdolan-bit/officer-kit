#!/usr/bin/env python3
"""study-guide harness: the fictional example passes all three gates and builds both products; a
seeded bad spec fails each gate for the reason planted; the engine carries no course content.
Usage: python3 evals/study_guide_check.py"""
import os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, "plugins", "officer-kit", "skills", "study-guide")
SC = os.path.join(SK, "scripts")
sys.path.insert(0, SC)
import study_lib as L
fails, n = [], 0
def ok(c, m):
    global n
    n += 1
    if not c: fails.append(m)
def run(*a):
    r = subprocess.run([sys.executable] + list(a), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
good = os.path.join(SK, "references", "example-spec.json")
src = os.path.join(SK, "references", "example-source.txt")
bad = os.path.join(ROOT, "evals", "study-guide", "bad-spec.json")
code, out = run(os.path.join(SC, "gates.py"), good, src)
ok(code == 0, "example spec should pass all gates:\n" + out)
code, out = run(os.path.join(SC, "gates.py"), bad, src)
ok(code == 1, "bad spec should fail")
ok("GATE 1 coverage" in out and "FAIL" in out.split("GATE 2")[0], "bad spec: coverage should fail on the dropped sentence")
ok(re.search(r"GATE 2 traceability: [1-9]", out) is not None, "bad spec: traceability should flag the invented answer")
ok("difficulty must be" in out, "bad spec: missing difficulty should fail")
ok("an option is empty" in out, "bad spec: empty option should fail")
ok("dash" in out, "bad spec: dash should fail")
tmp = tempfile.mkdtemp()
h, d = os.path.join(tmp, "w.html"), os.path.join(tmp, "g.docx")
code, out = run(os.path.join(SC, "build_walkthrough.py"), good, h)
ok(code == 0 and os.path.exists(h), "walkthrough should build: " + out)
if os.path.exists(h):
    t = open(h, encoding="utf-8").read()
    ok("{{" not in t, "walkthrough has an unfilled placeholder")
    ok("const SECTIONS" in t and "renderMap" in t, "walkthrough missing engine parts")
    ok(not re.search("[–—]", t), "walkthrough carries a dash")
code, out = run(os.path.join(SC, "build_guide.py"), good, d)
ok(code == 0 and os.path.exists(d), "guide should build: " + out)
import json, copy
gs = json.load(open(good, encoding="utf-8")); gs["mode"] = "guide"
gs["quiz"] = [copy.deepcopy(q) for sec in gs["sections"][1:4] for q in sec["quiz"]]
mc_only = copy.deepcopy(gs)
for sec in mc_only["sections"]: sec["quiz"] = []
mp = os.path.join(tmp, "mc_only.json"); json.dump(mc_only, open(mp, "w", encoding="utf-8"))
code, out = run(os.path.join(SC, "gates.py"), mp, src)
ok(code == 1 and "free recall" in out, "a guide quiz with no free recall should fail")
for q in gs["quiz"][:3]:
    ans = q["o"][q["a"]]
    for k in ("o", "a"): q.pop(k)
    q.update({"type": "recall", "answer": ans})
for sec in gs["sections"]: sec["quiz"] = []
gs["scenarios"] = [{"title": "The two day wait", "situation": "You will bake in two days and the kitchen is warm. Which feed, and what water?", "key": "A stiff feed of 1:2:1, with water below 30 degrees Celsius."}]
gp = os.path.join(tmp, "guide.json"); json.dump(gs, open(gp, "w", encoding="utf-8"))
code, out = run(os.path.join(SC, "gates.py"), gp, src)
ok(code == 0, "guide mode spec should pass the gates:\n" + out)
gd = os.path.join(tmp, "guide.docx")
code, out = run(os.path.join(SC, "build_guide.py"), gp, gd)
ok(code == 0 and "quiz 10 scenarios 1" in out, "guide mode should build quiz and scenario: " + out)
if os.path.exists(gd):
    from docx import Document
    txt = [p.text for p in Document(gd).paragraphs]
    ok("Quiz answer key" in txt and "Scenario answer key" in txt and "Skeleton" in txt, "guide missing a required part")
    ok(sum(1 for t in txt if t.startswith("____")) >= 9, "recall questions should print answer lines")
    ok(any("Where it is:" in t for t in txt), "answer key should say where each answer is taught")
    ok(txt.index("Practice quiz") < txt.index("Quiz answer key"), "answer key must follow the quiz")
code, out = run(os.path.join(SC, "build_walkthrough.py"), bad, h)
ok(code == 1, "walkthrough must refuse a spec that fails the quiz rules")
s = L.balance(L.load(good))
seq = [q["a"] for _, q in L.all_questions(s)]
ok(all(seq[i] != seq[i-1] for i in range(1, len(seq))), "balance left adjacent repeats")
ok(all(q["o"][q["a"]] == q["_intended"] for _, q in L.all_questions(s)), "balance moved an answer")
eng = open(os.path.join(SC, "engine_head.html"), encoding="utf-8").read() + open(os.path.join(SC, "engine_tail.html"), encoding="utf-8").read()
for term in ("Basic School", "Marine", "Moodle", "H5P", "Platoon", "B3", "Phase III", "suppress"):
    ok(term.lower() not in eng.lower(), "engine carries course content: " + term)
print("STUDY GUIDE CHECK: %d items" % n)
for f in fails: print("  FAIL ", f)
print("-> %d of %d pass" % (n - len(fails), n))
sys.exit(1 if fails else 0)
