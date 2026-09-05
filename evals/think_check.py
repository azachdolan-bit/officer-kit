#!/usr/bin/env python3
"""Deterministic evals for the thinking mechanisms: the estimate checker, the precision checker,
and the wiring that puts a tier on every product tool. Exit 0 = all pass."""
import os, re, subprocess, sys, glob
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, "..", "plugins", "officer-kit", "skills")
def run(*a): return subprocess.run([sys.executable, *a], capture_output=True, text=True)
res = []
def case(name, script, inp, code, *needles, extra=()):
    r = run(f"{S}/{script}", f"{H}/{inp}", *extra)
    res.append((name, r.returncode == code and all(n in r.stdout for n in needles)))

case("estimate good", "think/scripts/estimate_check.py", "think/inputs/estimate_good.md", 0, "clean", "tier deliberate")
case("estimate bad", "think/scripts/estimate_check.py", "think/inputs/estimate_bad.md", 1,
     "no 'Tier:' line", "missing section: scope", "assumption is sitting in the facts section",
     "no falsifier", "no consequence", "leading question", "no statement of what its answer changes")
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
TIERS = {"deliberate": ["risk-assessment","range-package","investigation","dd200","page-11","fitrep","award","meritorious-promotion","nomination","counseling","board-brief","order-critique"],
         "rapid": ["naval-letter","letter-of-recommendation","training-schedule","after-action","safety-brief","inspection-prep","rs-profile","study-guide"],
         "running": ["letter-of-appreciation","week-ahead","folder-triage","inbox-triage"]}
missing = []
for tier, tools in TIERS.items():
    for t in tools:
        p = os.path.join(S, t, "SKILL.md")
        txt = open(p).read() if os.path.exists(p) else ""
        if f"## Thinking (tier: {tier})" not in txt:
            missing.append(f"{t} ({tier})")
res.append(("every product tool carries its tier", not missing))
if missing: print("  missing tiers:", ", ".join(missing))
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
bad = 0
for n, k in res:
    print(f"{'PASS' if k else 'FAIL'}  {n}"); bad += 0 if k else 1
print(f"-> {len(res) - bad} of {len(res)} pass"); sys.exit(1 if bad else 0)
