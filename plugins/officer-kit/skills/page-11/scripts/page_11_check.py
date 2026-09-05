#!/usr/bin/env python3
"""Check a Page 11 entry (entry.md) against MCO 1900.16 paragraph 6105's own entry format, or the not
recommended for promotion deadline.

Usage:  python3 page_11_check.py entry.md
Exit 0 = passes (warnings allowed); 1 = a required element missing, a fixed sentence altered, a name,
a promise, or blocked content.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, dashes  # noqa: E402

GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"
DATE = r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b|\b\d{1,2}, \d{1,2}, and \d{1,2} \w+ \d{4}\b"
TRAITS = r"\b(?:attitude|motivation|lazy|unprofessional|constantly|always)\b"
FIXED = [
    ("opening", r"Counseled this date concerning the following deficiencies:"),
    ("corrective action lead in", r"Specific recommendations for corrective action are"),
    ("assistance lead in", r"to seek assistance, which is available through the chain of command and"),
    ("VA benefits sentence", r"I understand that failure to complete my enlistment contract with an honorable characterization of service may preclude my eligibility for benefits from the Department of Veterans Affairs or other organizations and have an adverse effect on future civilian employment\."),
    ("rebuttal sentence", r"I was advised that within 5 working days after acknowledging this entry I may submit a written rebuttal which will be filed in the electronic service record\."),
    ("choose to line", r"I choose to ____ ?/not to ____ make such a statement\."),
]
CONSEQ = r"Failure to take corrective action and any further violations of the UCMJ, disciplinary action, or incidents requiring formal counseling may result in judicial or adverse administrative action, including but not limited to administrative separation\."
PROCESSED = r"I understand that I am being processed for the following judicial or adverse administrative action:"


def norm(s):
    return re.sub(r"\s+", " ", s)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = norm(open(sys.argv[1], encoding="utf-8").read())
    fails, warns = [], []
    head = text.split("## ", 1)[0]
    is6105 = "6105" in head
    notrec = re.search(r"not recommended", head, re.I)
    m = re.search(r"## Entry (.*?)(?=## |\Z)", text)
    body = m.group(1) if m else ""
    if not m:
        fails.append("no '## Entry' section")
    if is6105:
        for name, pat in FIXED:
            if not re.search(pat, body):
                fails.append(f"the order's {name} is missing or altered (MCO 1900.16 para 6105.3.e)")
        if not re.search(CONSEQ, body) and not re.search(PROCESSED, body):
            fails.append("neither the warning entry's consequences sentence nor the being processed sentence is present verbatim (entry (1) or entry (2))")
        if not re.search(DATE, body):
            fails.append("element a: the deficiency is not stated as dated facts")
        if not re.search(r"in violation of|contrary to|required by|standing operating procedure|order", body, re.I):
            warns.append("the standard violated is not named (an order, SOP, or lawful instruction)")
        ca = re.search(r"Specific recommendations for corrective action are (.*?) and to seek assistance", body)
        if ca:
            if not re.search(r"\b(?:report|submit|complete|attend|pass|maintain|arrive|be present|achieve|meet)\b", ca.group(1), re.I):
                fails.append("element b: corrective action has no observable verb")
            if not re.search(r"re ?evaluat", ca.group(1), re.I) or not re.search(DATE, ca.group(1)):
                fails.append("element d: the reasonable opportunity needs a period and the date the commanding officer will re evaluate")
        sa = re.search(r"through the chain of command and (.*?)\. Failure|through the chain of command and (.*?)\. I understand", body)
        if sa and len((sa.group(1) or sa.group(2) or "").strip()) < 8:
            fails.append("element b: no named source of assistance after 'the chain of command and'")
        if not re.search(r"Signature of Commanding Officer", text):
            fails.append("no commanding officer signature line; the order requires the CO to sign adverse Page 11 entries")
        if re.search(r"Counselor \(signature", text) or re.search(r"Signed by:\s*(?!Commanding officer)", head, re.I) and not re.search(r"Signed by:\s*Commanding officer", head, re.I):
            warns.append("signer is not the commanding officer; the order requires the CO's signature")
        if not re.search(r"MMRP-20", text):
            warns.append("the copy to CMC (MMRP-20) within 30 days is not noted")
        if re.search(r"will be separated|will be discharged", body, re.I):
            fails.append("'will be separated' is a promise; the order's consequences sentence says may result in")
        if re.search(TRAITS, body, re.I):
            warns.append(f"trait word in the entry ('{re.search(TRAITS, body, re.I).group(0)}'); deficiencies are dated facts")
    if notrec:
        if not re.search(r"by the 15th|15th of the month|unit diary", text, re.I):
            fails.append("not recommended for promotion entry without the unit diary deadline (by the 15th of the month before the promotion month)")
    if not is6105 and not notrec:
        warns.append("neither a 6105 entry nor a not recommended for promotion entry was recognized in the title")
    mm = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]+", text)
    if mm:
        fails.append(f"a name appears in the entry ('{mm.group(0)}'); <MARINE> until substitution on the user's computer")
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
