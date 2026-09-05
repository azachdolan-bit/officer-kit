#!/usr/bin/env python3
"""Check a range package (package.md).

Usage:  python3 range_package_check.py package.md
Exit 0 = passes (warnings allowed); 1 = missing part, a name, or blocked content.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, dashes  # noqa: E402

GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"
PARTS = ["Facts", "Base checklist", "Range request", "Risk assessment", "Range order", "OIC and RSO checklist", "Range safety brief", "Medical and communications"]


def section(text, name, level="## "):
    m = re.search(r"^" + re.escape(level + name) + r"\s*$(.*?)(?=^" + re.escape(level) + r"|\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails, warns = [], []
    for p in PARTS:
        if section(text, p) is None:
            fails.append(f"missing part: {p}")
    facts = section(text, "Facts") or ""
    if not re.search(r"\bOIC\b.*certified", facts, re.I | re.S) or not re.search(r"\bRSO\b.*certified", facts, re.I | re.S):
        fails.append("Facts: OIC and RSO certification not stated")
    if not re.search(r"\b[A-Z]\d{3}\b", facts):
        fails.append("Facts: ammunition without a DODIC")
    if not re.search(r"\d+\s+Marines|personnel\s*[:=]?\s*\d+", facts, re.I):
        warns.append("Facts: personnel count not stated")
    ra = section(text, "Risk assessment") or ""
    if not re.search(r"\b[IV]+[A-E]\b", ra) or not re.search(r"approved by", ra, re.I):
        fails.append("Risk assessment: residual level and approver not stated")
    order = section(text, "Range order") or ""
    for para in ("Situation", "Mission", "Execution", "Administration and logistics", "Command and signal"):
        if not re.search(r"^### " + para, order, re.M):
            fails.append(f"Range order: missing paragraph {para}")
    cl = section(text, "OIC and RSO checklist") or ""
    for ph in ("Before firing", "During firing", "After firing"):
        if not re.search(r"^### " + ph, cl, re.M):
            fails.append(f"OIC and RSO checklist: missing {ph}")
    if not re.search(r"cease fire", text, re.I) or not re.search(r"Condition 4", text):
        fails.append("cease fire language missing: verbally and by hand and arm signal, all weapons to Condition 4")
    med = section(text, "Medical and communications") or ""
    if not re.search(r"\d+\s*minutes", med) or not re.search(r"route|road|by air|by ground", med, re.I):
        fails.append("Medical and communications: evacuation route and time to care not stated")
    if not re.search(r"corpsman", med, re.I):
        warns.append("Medical and communications: corpsman and certification not stated")
    m = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]+", text)
    if m:
        fails.append(f"a name appears in the package ('{m.group(0)}'); billets only, names on the base's roster pages")
    for b in blocked_hits(text, allow=("medical",)):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")
    print(f"RANGE PACKAGE CHECK: {sys.argv[1]}")
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
