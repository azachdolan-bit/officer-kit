#!/usr/bin/env python3
"""Deterministic evals for the Admin module checkers (fitrep, rs-profile, award). Exit 0 = all pass."""
import os, subprocess, sys, tempfile
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, "..", "plugins", "officer-kit", "skills")
def run(*a): return subprocess.run([sys.executable, *a], capture_output=True, text=True)
res = []
r = run(f"{S}/fitrep/scripts/fitrep_check.py", f"{H}/fitrep/inputs/good_draft.md"); res.append(("fitrep clean-draft", r.returncode == 0 and "clean" in r.stdout))
r = run(f"{S}/fitrep/scripts/fitrep_check.py", f"{H}/fitrep/inputs/bad_draft.md"); res.append(("fitrep prohibited-content", r.returncode == 1 and all(k in r.stdout for k in ("13d(1)", "13d(8)", "13d(12)", "promotion statements", "word picture", "quotation"))))
r = run(f"{S}/rs-profile/scripts/rs_profile.py", f"{H}/rs-profile/inputs/ledger.csv", "--grade", "2ndLt"); res.append(("rs-profile averages-and-rv", "RS average: 3.58" in r.stdout and "high: 4.38" in r.stdout and "RV  100.0" in r.stdout and "82.75" in r.stdout and "MRO-05" not in r.stdout))
r = run(f"{S}/rs-profile/scripts/rs_profile.py", f"{H}/rs-profile/inputs/ledger.csv", "--grade", "2ndLt", "--propose", "D,D,D,D,D,D,D,D,D,D,D,D,D,H"); res.append(("rs-profile proposed-report", "average 4.0, relative value 95.25" in r.stdout and "3.58 -> 3.66" in r.stdout))
r = run(f"{S}/award/scripts/citation_check.py", f"{H}/award/inputs/na_citation.txt", "--level", "NA"); res.append(("award na-citation-clean", r.returncode == 0))
t = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False); t.write("For professional achievement " + "in the superior performance of duties " * 40 + "Marine Corps Naval Service."); t.close()
r = run(f"{S}/award/scripts/citation_check.py", t.name, "--level", "NA"); res.append(("award over-limit", r.returncode == 1 and "limit 1200" in r.stdout and "capital" in r.stdout)); os.unlink(t.name)
bad = 0
for n, ok in res:
    print(f"{'PASS' if ok else 'FAIL'}  {n}"); bad += 0 if ok else 1
print(f"-> {len(res) - bad} of {len(res)} pass"); sys.exit(1 if bad else 0)
