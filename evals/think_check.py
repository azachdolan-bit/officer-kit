#!/usr/bin/env python3
"""Deterministic evals for the four rules that survived the 5 Sep 2026 A/B test: the precision
checker, the coverage claim ban, and the wiring that puts the rules on every tool that gets signed.
Exit 0 = all pass."""
import os, re, subprocess, sys, glob
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, "..", "plugins", "officer-kit", "skills")
def run(*a): return subprocess.run([sys.executable, *a], capture_output=True, text=True)
res = []
def case(name, script, inp, code, *needles, extra=()):
    r = run(f"{S}/{script}", f"{H}/{inp}", *extra)
    res.append((name, r.returncode == code and all(n in r.stdout for n in needles)))

case("precision loose", "think/scripts/precision_check.py", "think/inputs/loose.md", 1,
     "center embedded", "soft quantifier", "passive with no actor", "vague deadline", "and/or",
     "hidden verb", "mixed modals", "pronoun and no noun", "never expanded", extra=("--directive",))
case("precision tight", "think/scripts/precision_check.py", "think/inputs/tight.md", 0, "clean", extra=("--directive",))
# advisory mode: the same loose document passes when it is not directive
r = run(f"{S}/think/scripts/precision_check.py", f"{H}/think/inputs/loose.md")
res.append(("precision advisory when not directive", r.returncode == 0 and "WARN" in r.stdout and "FAIL" not in r.stdout))
# prescribed text is skipped
import tempfile
t = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
t.write("# X\n\n<!-- prescribed -->\nThe vehicles will be inspected as required and reported as soon as possible.\n<!-- /prescribed -->\n\nThe motor transport chief inspects the four vehicles each Thursday.\n"); t.close()
r = run(f"{S}/think/scripts/precision_check.py", t.name, "--directive")
res.append(("prescribed text skipped", r.returncode == 0 and "as required" not in r.stdout)); os.unlink(t.name)
# every product tool carries a tier, and the tiers are the ones the think skill lists
SIGNED = ["risk-assessment","range-package","investigation","dd200","page-11","fitrep","award",
          "meritorious-promotion","nomination","counseling","board-brief","order-critique",
          "naval-letter","letter-of-recommendation","training-schedule","after-action",
          "safety-brief","inspection-prep","rs-profile","study-guide"]
ROUTINE = ["letter-of-appreciation","week-ahead","folder-triage","inbox-triage"]
missing = []
for t in SIGNED:
    p = os.path.join(S, t, "SKILL.md")
    txt = open(p).read() if os.path.exists(p) else ""
    if "## Before you draft" not in txt or "Assume it already failed" not in txt.replace("Assume this already failed","Assume it already failed"):
        missing.append(t)
res.append(("every signed product runs the four rules", not missing))
if missing: print("  missing:", ", ".join(missing))
extra = [t for t in ROUTINE if "## Before you draft" in (open(os.path.join(S,t,"SKILL.md")).read() if os.path.exists(os.path.join(S,t,"SKILL.md")) else "")]
res.append(("routine tools carry no ceremony", not extra))
if extra: print("  unexpected:", ", ".join(extra))
th = open(f"{S}/think/SKILL.md").read()
res.append(("think skill states all four rules",
            all(x in th for x in ["Assume it already failed, before you draft",
                                  "Ask what you cannot answer",
                                  "Never say you covered the rest",
                                  "Hand anything that gets signed to the red team"])))
import glob as _g
res.append(("the deleted templates are gone", not _g.glob(f"{S}/think/references/*") and not os.path.exists(f"{S}/think/scripts/estimate_check.py")))
# the think skill and the red team agent exist and are well formed
import yaml
ok = os.path.exists(f"{S}/think/SKILL.md")
if ok:
    fm = yaml.safe_load(open(f"{S}/think/SKILL.md").read().split("---")[1])
    ok = fm.get("name") == "think" and len(fm.get("description", "")) < 1024
rtp = os.path.join(S, "..", "agents", "red-team.md")
if os.path.exists(rtp):
    head = open(rtp).read().split("---")[1]
    ok = ok and re.search(r"^name: red-team$", head, re.M) and re.search(r"^description: \S", head, re.M) and re.search(r"^model:", head, re.M) and re.search(r"^tools:", head, re.M)
else:
    ok = False
res.append(("think skill and red-team agent well formed", bool(ok)))
# the red team agent never scores
rt = open(os.path.join(S, "..", "agents", "red-team.md")).read()
res.append(("red team refuses to score", "You do not score" in rt and "never scores" in rt))
# the three defects the 5 Sep A/B test found, each with the artifact that exposed it
sys.path.insert(0, f"{S}/think/scripts")
import subprocess, tempfile  # noqa: E402
def run(script, body, *args):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(body); p = f.name
    return subprocess.run([sys.executable, f"{S}/think/scripts/{script}", p, *args],
                          capture_output=True, text=True)

# 1. a risk level is not an undefined acronym
r = run("precision_check.py", "# Sheet\n\nThe residual is IID and the initial was IIB. Hazard two sits at IE.\n", "--directive")
res.append(("risk levels do not read as undefined acronyms", "acronym" not in r.stdout))

# 2. a coverage claim in a delivered product fails, at every tier
r = run("precision_check.py", "# Sheet\n\nThe head count is not filled in. Each missing item is a gap rather than an omission.\n")
res.append(("coverage claim in a product fails", r.returncode == 1 and "coverage claim" in r.stdout))
r = run("precision_check.py", "# Sheet\n\nChecked against the matrix and the required elements. Nothing here confirms the hazard list is complete.\n")
res.append(("naming what was not checked still passes", r.returncode == 0))

bad = 0
for n, k in res:
    print(f"{'PASS' if k else 'FAIL'}  {n}"); bad += 0 if k else 1
print(f"-> {len(res) - bad} of {len(res)} pass"); sys.exit(1 if bad else 0)
