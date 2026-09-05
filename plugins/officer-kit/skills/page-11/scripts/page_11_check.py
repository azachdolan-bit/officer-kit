#!/usr/bin/env python3
"""Check a Page 11 entry (entry.md) for the 6105 elements or the not recommended deadline.

Usage:  python3 page_11_check.py entry.md
Exit 0 = passes (warnings allowed); 1 = a required element missing, a name, or blocked content.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, dashes  # noqa: E402

GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"
DATE = r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b|\b\d{1,2}, \d{1,2}, and \d{1,2} \w+ \d{4}\b"
TRAITS = r"\b(?:attitude|motivation|lazy|unprofessional|constantly|always)\b"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails, warns = [], []
    entry = re.search(r"^## Entry\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    body = entry.group(1) if entry else ""
    head = text.split("\n", 1)[0]
    is6105 = "6105" in head
    notrec = re.search(r"not recommended", head, re.I)
    if not entry:
        fails.append("no '## Entry' section")
    if is6105:
        if not re.search(r"deficienc", body, re.I) or not re.search(DATE, body):
            fails.append("element 1 missing: the deficiency as dated facts")
        if not re.search(r"in violation of|contrary to|required by", body, re.I):
            warns.append("the standard violated is not named (an order, SOP, or lawful instruction, by number or date)")
        if not re.search(r"corrective action", body, re.I) or not re.search(r"\b(?:report|submit|complete|attend|pass|maintain|arrive|be present|achieve)\b", body, re.I):
            fails.append("element 2 missing: specific, observable corrective action")
        if not re.search(r"assistance is available from|sources? of (?:further )?assistance", body, re.I):
            fails.append("element 2 missing: sources of further assistance")
        if not re.search(r"administrative separation", body, re.I) or not re.search(r"MCO 1900\.16", body):
            fails.append("element 3 missing: consequences naming administrative separation under MCO 1900.16")
        if not re.search(r"will be given .*? to demonstrate|re ?evaluated on " + DATE, body, re.I | re.S) or not re.search(r"re ?evaluated on", body, re.I):
            fails.append("element 4 missing: the reasonable opportunity with a period and a re evaluation date")
        if not re.search(r"5 working days|five working days", body, re.I) or not re.search(r"rebuttal", body, re.I):
            fails.append("rebuttal advisory missing (within 5 working days after acknowledging this entry, a written rebuttal may be submitted)")
        if not re.search(r"^## Acknowledgment", text, re.M):
            fails.append("no Acknowledgment block with signature lines")
        if re.search(r"will be separated|will be discharged", body, re.I):
            fails.append("'will be separated' is a promise the counselor cannot make; the entry says may result in administrative separation")
        if re.search(TRAITS, body, re.I):
            warns.append(f"trait word in the entry ('{re.search(TRAITS, body, re.I).group(0)}'); deficiencies are dated facts")
    if notrec:
        if not re.search(r"by the 15th|15th of the month|unit diary", text, re.I):
            fails.append("not recommended for promotion entry without the unit diary deadline (by the 15th of the month before the promotion month)")
    if not is6105 and not notrec:
        warns.append("neither a 6105 entry nor a not recommended for promotion entry was recognized")
    m = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]+", text)
    if m:
        fails.append(f"a name appears in the entry ('{m.group(0)}'); <MARINE> until substitution on the user's computer")
    for b in blocked_hits(text, allow=("SAPR or investigation",)):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")
    print(f"PAGE 11 CHECK: {sys.argv[1]}  {'6105' if is6105 else ''} {'not recommended' if notrec else ''}".rstrip())
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
