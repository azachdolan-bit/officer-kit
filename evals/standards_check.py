#!/usr/bin/env python3
"""Kit standards wiring: STANDARDS.md exists with nine numbered standards and a version line,
every skill reads it, the rules file template carries the same version and nine lines,
start and week-ahead run the version check, and no file in the chain carries a dash.
Usage: python3 evals/standards_check.py"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "plugins", "officer-kit")
fails, n = [], 0
def ok(cond, msg):
    global n
    n += 1
    if not cond: fails.append(msg)
std = open(os.path.join(P, "STANDARDS.md"), encoding="utf-8").read()
m = re.search(r"^Kit standards: (\d+\.\d+\.\d+)$", std, re.M)
ok(m, "STANDARDS.md: no 'Kit standards: x.y.z' line")
ver = m.group(1) if m else "?"
ok(len(re.findall(r"^\d\. \*\*", std, re.M)) == 9, "STANDARDS.md: expected nine numbered standards")
for f in sorted(glob.glob(os.path.join(P, "skills", "*", "SKILL.md"))):
    ok("../../STANDARDS.md" in open(f, encoding="utf-8").read(), f"{os.path.relpath(f, P)}: does not read STANDARDS.md")
tpl = open(os.path.join(P, "skills", "rules-file", "references", "template.md"), encoding="utf-8").read()
ok(re.search(rf"^- Kit standards: {re.escape(ver)}$", tpl, re.M), f"template.md: Kit standards line does not match STANDARDS.md {ver}")
ok(len(re.findall(r"^- \d ", tpl, re.M)) == 9, "template.md: expected nine kit standard lines")
for s in ("start", "week-ahead"):
    ok("## Kit standards check" in open(os.path.join(P, "skills", s, "SKILL.md"), encoding="utf-8").read(), f"{s}: no Kit standards check")
pj = open(os.path.join(P, ".claude-plugin", "plugin.json"), encoding="utf-8").read()
pv = re.search(r'"version":\s*"([^"]+)"', pj).group(1)
ok(tuple(map(int, ver.split("."))) <= tuple(map(int, pv.split("."))), f"STANDARDS.md {ver} is newer than plugin.json {pv}")
for f in [os.path.join(P, "STANDARDS.md"), os.path.join(P, "skills", "rules-file", "references", "template.md")]:
    ok(not re.search("[–—]", open(f, encoding="utf-8").read()), f"{os.path.relpath(f, P)}: carries an em or en dash")
# standard 9, American spelling: no British form anywhere in the kit's own text (skills, references, agents, standards, evals fixtures)
BRITISH = ["manoeuvre", "manoeuver", "organisation", "organise", "centre", "colour", "labelled", "metre", "kilometre", "analysed", "analysing", "defence", "recognise", "catalogue", "favour", "behaviour", "programme", "licence", "practise", "honour", "armour", "modelled", "travelled"]
ALLOW = ["defence of duffer's drift", '"colour", "organisation"']   # titles quoted from a source stay as the source spells them
hits = []
for f in sorted(glob.glob(os.path.join(P, "**", "*.md"), recursive=True) + glob.glob(os.path.join(ROOT, "evals", "**", "*.md"), recursive=True) + glob.glob(os.path.join(P, "**", "*.py"), recursive=True)):
    for ln in open(f, encoding="utf-8", errors="replace").read().lower().splitlines():
        if ln.lstrip().startswith(">"):
            continue   # a block quote reproduces its source verbatim
        for w in BRITISH:
            for m in re.finditer(r"(?<![a-z])" + w + r"[a-z]*", ln):
                ctx = ln[max(0, m.start() - 30):m.end() + 30]
                if any(a in ln for a in ALLOW):
                    continue
                hits.append(f"{os.path.relpath(f, ROOT)}: {m.group(0)} ({ctx.strip()})")
ok(not hits, "British spelling in the kit's own text (standard 9):\n    " + "\n    ".join(hits[:40]) + ("\n    ... %d more" % (len(hits) - 40) if len(hits) > 40 else ""))
print(f"STANDARDS CHECK: {n} items")
for f in fails: print("  FAIL ", f)
print(f"-> {n - len(fails)} of {n} pass")
sys.exit(1 if fails else 0)
