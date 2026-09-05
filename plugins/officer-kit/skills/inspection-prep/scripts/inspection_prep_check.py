#!/usr/bin/env python3
"""Check an inspection self assessment (assessment.md).

Usage:  python3 inspection_prep_check.py assessment.md
Exit 0 = passes (warnings allowed); 1 = a yes without evidence, a no without a plan, or a name.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, dashes  # noqa: E402

GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def rows(block, header_word):
    out = []
    for r in (block or "").splitlines():
        if r.strip().startswith("|") and header_word not in r and not re.match(r"^\|\s*-", r.strip()):
            out.append([c.strip() for c in r.strip().strip("|").split("|")])
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails, warns = [], []
    items = rows(section(text, "Items"), "Checklist item")
    if not items:
        fails.append("no checklist items")
    disc = rows(section(text, "Discrepancies and corrective action"), "Fix")
    disc_items = {d[0] for d in disc if d}
    binder = section(text, "Binder contents") or ""
    nos = []
    for it in items:
        if len(it) < 5:
            fails.append(f"item row incomplete: {' | '.join(it)[:60]}")
            continue
        n, q, ref, ans, ev = it[:5]
        if ans.lower().startswith("yes"):
            if len(ev) < 8 or not re.search(r"tab|folder|binder|MCTIMS|MOL|iAPS|file|log|letter|roster|tracker", ev, re.I):
                fails.append(f"item {n}: yes without evidence and a location")
        elif ans.lower().startswith("no"):
            nos.append(n)
            if n not in disc_items:
                fails.append(f"item {n}: no, but not in the discrepancies and corrective action table")
        elif ans.lower().startswith("n/a"):
            if not ev or len(ev) < 8:
                warns.append(f"item {n}: N/A without a reason")
        else:
            fails.append(f"item {n}: answer must be Yes, No, or N/A with a reason")
        if not ref:
            warns.append(f"item {n}: no reference cited")
    for d in disc:
        if len(d) < 4 or any(not c for c in d[:4]) or not re.search(r"\d", d[3]):
            fails.append(f"discrepancy row incomplete or undated: {' | '.join(d)[:60]}")
    if not binder.strip():
        warns.append("no Binder contents section")
    m = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]+", text)
    if m:
        fails.append(f"a name appears in the assessment ('{m.group(0)}'); billets and tabs only")
    for b in blocked_hits(text, allow=("SAPR or investigation", "medical", "substance", "financial")):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")
    print(f"INSPECTION PREP CHECK: {sys.argv[1]}  {len(items)} items, {len(nos)} discrepancies")
    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    if not warns and not fails:
        print("  clean")
    print(f"  -> {len(fails)} failures, {len(warns)} warnings")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
