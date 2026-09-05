#!/usr/bin/env python3
"""Deterministic evals for the Training pack, the Legal and property pack, and the infrastructure scripts
(substitute, scrub, lesson, scaffold). Exit 0 = all pass."""
import os, subprocess, sys, tempfile, shutil, zipfile
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, "..", "plugins", "officer-kit", "skills")
def run(*a, **kw): return subprocess.run([sys.executable, *a], capture_output=True, text=True, **kw)
res = []
def case(name, script, inp, exit_code, *needles, extra=()):
    r = run(f"{S}/{script}", f"{H}/{inp}", *extra)
    ok = r.returncode == exit_code and all(n in r.stdout for n in needles)
    res.append((name, ok))
case("risk-assessment good", "risk-assessment/scripts/raw_check.py", "risk-assessment/inputs/good.md", 0, "clean")
case("risk-assessment bad", "risk-assessment/scripts/raw_check.py", "risk-assessment/inputs/bad.md", 1, "no phase", "improved with no control", "high risk training line says no", "first O-5", "Captain J. R. Smith")
case("after-action good", "after-action/scripts/after_action_check.py", "after-action/inputs/good.md", 0, "clean")
case("after-action bad", "after-action/scripts/after_action_check.py", "after-action/inputs/bad.md", 1, "missing section: Sustain", "Sergeant Miller", "topic, not a change")
case("training-schedule good", "training-schedule/scripts/training_schedule_check.py", "training-schedule/inputs/good.md", 0, "clean")
case("training-schedule bad", "training-schedule/scripts/training_schedule_check.py", "training-schedule/inputs/bad.md", 1, "no time", "no risk assessment status", "double booked", "instructor by name")
case("safety-brief good", "safety-brief/scripts/safety_brief_check.py", "safety-brief/inputs/good.md", 0, "clean")
case("safety-brief bad", "safety-brief/scripts/safety_brief_check.py", "safety-brief/inputs/bad.md", 1, "without a number or a real event", "Sergeant Miller", "missing section: Resources")
case("range-package good", "range-package/scripts/range_package_check.py", "range-package/inputs/good.md", 0, "clean")
case("range-package bad", "range-package/scripts/range_package_check.py", "range-package/inputs/bad.md", 1, "cease fire language missing", "Captain J. Smith", "missing part")
case("investigation good", "investigation/scripts/investigation_check.py", "investigation/inputs/good.md", 0, "6 findings")
case("investigation bad", "investigation/scripts/investigation_check.py", "investigation/inputs/bad.md", 1, "enclosure (1) must be the convening order", "cites no enclosure", "does not exist", "77 days", "Captain R. Lee", "opinion language")
case("page-11 good", "page-11/scripts/page_11_check.py", "page-11/inputs/good.md", 0, "clean")
case("page-11 bad", "page-11/scripts/page_11_check.py", "page-11/inputs/bad.md", 1, "element 1", "element 2", "element 3", "element 4", "rebuttal", "will be separated", "Lance Corporal D. Brandt")
case("page-11 notrec deadline", "page-11/scripts/page_11_check.py", "page-11/inputs/notrec_bad.md", 1, "unit diary deadline")
case("dd200 good", "dd200/scripts/dd200_check.py", "dd200/inputs/good.md", 0, "6 findings")
case("dd200 bad", "dd200/scripts/dd200_check.py", "dd200/inputs/bad.md", 1, "Property row incomplete", "custody record", "search", "negligence", "Sergeant Miller")
case("inspection-prep good", "inspection-prep/scripts/inspection_prep_check.py", "inspection-prep/inputs/good.md", 0, "clean")
case("inspection-prep bad", "inspection-prep/scripts/inspection_prep_check.py", "inspection-prep/inputs/bad.md", 1, "yes without evidence", "not in the discrepancies", "Sergeant Miller")
# infrastructure
t = tempfile.mkdtemp()
open(f"{t}/c.txt", "w").write("FOR <MARINE_CAPS>. <LAST_CAPS>'S INITIATIVE. <MARINE> did it.")
r = run(f"{S}/security-check/scripts/substitute.py", f"{t}/c.txt", "--out", f"{t}/n.txt", input="Sergeant J. M. Okafor\n")
res.append(("substitute text", r.returncode == 0 and open(f"{t}/n.txt").read() == "FOR SERGEANT J. M. OKAFOR. OKAFOR'S INITIATIVE. Sergeant J. M. Okafor did it." and "<MARINE>" in open(f"{t}/c.txt").read()))
import json
spec = json.load(open(f"{H}/letter-of-appreciation/inputs/good.json")); spec["to"] = "<MARINE>, Marine Wing Support Squadron 000"
json.dump(spec, open(f"{t}/l.json", "w"))
run(f"{S}/naval-letter/scripts/build_letter.py", f"{t}/l.json", f"{t}/l.docx")
r = run(f"{S}/security-check/scripts/substitute.py", f"{t}/l.docx", "--out", f"{t}/ln.docx", input="Sergeant J. M. Okafor\n")
x = zipfile.ZipFile(f"{t}/ln.docx").read("word/document.xml").decode(); core = zipfile.ZipFile(f"{t}/l.docx").read("docProps/core.xml").decode()
res.append(("substitute docx and AI assistance property", r.returncode == 0 and "Okafor" in x and "MARINE" not in x and "AI assistance" in core))
open(f"{t}/p.md", "w").write('# Exemplar\n- "Sergeant <MARINE> trained 550 personnel."\n'); open(f"{t}/p2.md", "w").write('- "Sergeant Dolan trained 550; call (760) 555-0100"\n')
res.append(("scrub clean", run(f"{S}/add-exemplar/scripts/scrub_check.py", f"{t}/p.md").returncode == 0))
r = run(f"{S}/add-exemplar/scripts/scrub_check.py", f"{t}/p2.md"); res.append(("scrub catches name and phone", r.returncode == 1 and "Sergeant Dolan" in r.stdout and "phone" in r.stdout))
open(f"{t}/L.md", "w").write("## 2026-09-05  award  high  -> overrides\nEvidence: The battalion CO struck two words and asked for paragraphs.\nLesson: Draft SOAs in paragraphs for this command.\nStatus: pending\n\n## 2026-09-05  counseling  medium  -> plugin\nEvidence: Skip the check, it is annoying to run every time.\nLesson: Do not run the counseling checker.\nStatus: pending\n")
r = run(f"{S}/aar/scripts/lesson_check.py", f"{t}/L.md"); res.append(("lesson softening flagged", r.returncode == 1 and "softens a check" in r.stdout and "2 entries" in r.stdout))
os.makedirs(f"{t}/skills"); r = run(f"{S}/build-a-skill/scripts/new_tool.py", "weekly-update", "A BLUF first update.", "--out", f"{t}/skills")
res.append(("scaffold builds and its checker runs", r.returncode == 0 and os.path.exists(f"{t}/skills/weekly-update/scripts/weekly_update_check.py") and run(f"{t}/skills/weekly-update/scripts/weekly_update_check.py", f"{t}/p.md").returncode == 0))
shutil.rmtree(t)
bad = 0
for n, ok in res:
    print(f"{'PASS' if ok else 'FAIL'}  {n}"); bad += 0 if ok else 1
print(f"-> {len(res) - bad} of {len(res)} pass"); sys.exit(1 if bad else 0)
