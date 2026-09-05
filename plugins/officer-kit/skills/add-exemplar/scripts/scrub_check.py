#!/usr/bin/env python3
"""Fail if a pattern file still carries a name, an identifier, or blocked content.

Usage:  python3 scrub_check.py pattern.md
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits  # noqa: E402

GRADES = r"(?:Private First Class|Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Master Gunnery Sergeant|Sergeant Major|Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|Colonel|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|MGySgt|SgtMaj|2ndLt|1stLt|Capt|Maj|LtCol|Col)"
ALLOWED_AFTER_GRADE = {"MARINE", "LAST", "Okafor", "Hale", "Vance", "Ashe", "Rios", "Penn", "Brandt", "Ives", "Roe", "Example"}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails = []
    for m in re.finditer(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}([A-Z][a-z]+)", text):
        if m.group(1) not in ALLOWED_AFTER_GRADE:
            fails.append(f"a name may remain after a grade: '{m.group(0)}'")
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
        fails.append("email address present")
    if re.search(r"\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b", text):
        fails.append("phone number present")
    for b in blocked_hits(text):
        fails.append(f"blocked content: {b}")
    print(f"SCRUB CHECK: {sys.argv[1]}")
    for f in fails:
        print(f"  FAIL  {f}")
    if not fails:
        print("  clean")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
