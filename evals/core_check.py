#!/usr/bin/env python3
"""Deterministic evals for the Path D core tools (reenlistment, and the rest as they are built). Exit 0 = all pass."""
import os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, "..", "plugins", "officer-kit", "skills")
def run(*a, **kw): return subprocess.run([sys.executable, *a], capture_output=True, text=True, **kw)
res = []
def case(name, script, inp, exit_code, *needles, extra=()):
    r = run(f"{S}/{script}", *( [f"{H}/{inp}"] if inp else [] ), *extra)
    ok = r.returncode == exit_code and all(n in r.stdout for n in needles)
    if not ok:
        print(f"--- {name}: exit {r.returncode}\n{r.stdout}{r.stderr}")
    res.append((name, ok))
# reenlistment
case("reenlistment good", "reenlistment/scripts/reenlistment_check.py", "reenlistment/inputs/good.md", 0, "clean")
case("reenlistment bad", "reenlistment/scripts/reenlistment_check.py", "reenlistment/inputs/bad.md", 1, "population claim", "promise about the decision", "family or personal", "certification line", "windows do not match", "Corporal Brandt")
case("reenlistment notrec delegated", "reenlistment/scripts/reenlistment_check.py", "reenlistment/inputs/notrec_bad.md", 1, "may not be delegated", "commanding officer's interview", "dated facts")
case("reenlistment over tier", "reenlistment/scripts/reenlistment_check.py", "reenlistment/inputs/over_tier.md", 1, "top 60%", "requires the top 50 percent")
case("reenlistment windows", "reenlistment/scripts/reenlistment_windows.py", None, 0, "19 June 2025 to 19 August 2025", "19 June 2026 to 19 August 2026", "19 December 2026 to 19 February 2027", "standard:", extra=("--ecc", "19 August 2027", "--today", "2026-09-05"))
case("reenlistment windows immediate", "reenlistment/scripts/reenlistment_windows.py", None, 0, "immediate: 75 days", extra=("--ecc", "2027-03-31", "--today", "2027-01-15"))
bad = 0
for n, ok in res:
    print(f"{'PASS' if ok else 'FAIL'}  {n}"); bad += 0 if ok else 1
print(f"-> {len(res) - bad} of {len(res)} pass"); sys.exit(1 if bad else 0)
