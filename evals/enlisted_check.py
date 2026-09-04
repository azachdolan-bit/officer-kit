#!/usr/bin/env python3
"""Deterministic evals for the enlisted support tools (letter-of-recommendation, letter-of-appreciation,
meritorious-promotion, nomination, board-brief, counseling). Exit 0 = all pass."""
import os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, "..", "plugins", "officer-kit", "skills")
def run(*a): return subprocess.run([sys.executable, *a], capture_output=True, text=True)
res = []
r = run(f"{S}/letter-of-recommendation/scripts/lor_check.py", f"{H}/letter-of-recommendation/inputs/strong.json"); res.append(("lor strong-clean", r.returncode == 0 and "clean" in r.stdout))
r = run(f"{S}/letter-of-recommendation/scripts/lor_check.py", f"{H}/letter-of-recommendation/inputs/weak.json"); res.append(("lor weak-fails", r.returncode == 1 and all(k in r.stdout for k in ("denominator", "period of observation", "point of contact", "medical", "family"))))
r = run(f"{S}/letter-of-appreciation/scripts/loa_check.py", f"{H}/letter-of-appreciation/inputs/good.json"); res.append(("loa good-clean", r.returncode == 0 and "clean" in r.stdout))
r = run(f"{S}/letter-of-appreciation/scripts/loa_check.py", f"{H}/letter-of-appreciation/inputs/bad.json"); res.append(("loa bad-fails", r.returncode == 1 and all(k in r.stdout for k in ("no date", "no count", "period of service"))))
r = run(f"{S}/meritorious-promotion/scripts/board_package_check.py", f"{H}/meritorious-promotion/inputs/good.json", "--kind", "merpro"); res.append(("merpro good-clean", r.returncode == 0 and "clean" in r.stdout))
r = run(f"{S}/meritorious-promotion/scripts/board_package_check.py", f"{H}/meritorious-promotion/inputs/bad.json", "--kind", "merpro"); res.append(("merpro bad-fails", r.returncode == 1 and all(k in r.stdout for k in ("6 enclosures", "4 lettered", "divorce", "(d) maturity"))))
r = run(f"{S}/nomination/scripts/board_package_check.py", f"{H}/nomination/inputs/good.json", "--kind", "nomination"); res.append(("nomination good-clean", r.returncode == 0 and "clean" in r.stdout))
r = run(f"{S}/board-brief/scripts/brief_check.py", f"{H}/board-brief/inputs/brief.md", "--minutes", "4", "--package", f"{H}/meritorious-promotion/inputs/good.json"); res.append(("board-brief agrees-with-package", r.returncode == 0 and "package agreement" in r.stdout and "1 blank" in r.stdout))
r = run(f"{S}/board-brief/scripts/brief_check.py", f"{H}/board-brief/inputs/brief_bad.md", "--minutes", "4", "--package", f"{H}/meritorious-promotion/inputs/good.json"); res.append(("board-brief mismatch-and-no-number", r.returncode == 1 and "28" in r.stdout and "without a number" in r.stdout))
r = run(f"{S}/counseling/scripts/counseling_check.py", f"{H}/counseling/inputs/event_good.md"); res.append(("counseling event-clean", r.returncode == 0 and "clean" in r.stdout))
r = run(f"{S}/counseling/scripts/counseling_check.py", f"{H}/counseling/inputs/event_bad.md"); res.append(("counseling event-fails", r.returncode == 1 and all(k in r.stdout for k in ("undated", "mentor", "personal issues", "will be separated", "trait words"))))
# the letter specs render and pass the correspondence QC
import tempfile
for name, spec in (("lor", "letter-of-recommendation/inputs/strong.json"), ("merpro", "meritorious-promotion/inputs/good.json"), ("loa", "letter-of-appreciation/inputs/good.json")):
    out = os.path.join(tempfile.gettempdir(), f"ok_{name}.docx")
    r1 = run(f"{S}/naval-letter/scripts/build_letter.py", f"{H}/{spec}", out); r2 = run(f"{S}/naval-letter/scripts/qc_letter.py", out)
    res.append((f"{name} renders-and-passes-correspondence-qc", r1.returncode == 0 and r2.returncode == 0))
bad = 0
for n, ok in res:
    print(f"{'PASS' if ok else 'FAIL'}  {n}"); bad += 0 if ok else 1
print(f"-> {len(res) - bad} of {len(res)} pass"); sys.exit(1 if bad else 0)
