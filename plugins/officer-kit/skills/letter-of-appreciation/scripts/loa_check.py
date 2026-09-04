#!/usr/bin/env python3
"""Check a letter of appreciation spec (naval-letter JSON) for the event, count, role, thanks shape.

Usage:  python3 loa_check.py letter.json
Exit 0 = passes (warnings allowed); 1 = structural failure or blocked content.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, numbers, dashes, words  # noqa: E402

DATE = r"\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b"
ROLE_VERBS = r"\b(?:served|planned|briefed|taught|instructed|led|coordinated|built|sourced|secured|organized|ran|drove|rode|escorted|hosted|provided|delivered|repaired|recovered|trained|supervised|volunteered)\b"


def flat(p):
    t = p.get("text", "")
    for s in p.get("subs", []):
        t += " " + flat(s)
    return t


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    paras = [flat(p) for p in spec.get("paragraphs", [])]
    body = " ".join(paras) + " " + spec.get("poc", "")
    fails, warns = [], []

    if not 2 <= len(paras) <= 4:
        fails.append(f"{len(paras)} paragraphs; the shape is three (event and thanks, what it did and for whom, the role and close), a fourth for a POC")
    if not re.search(DATE, body):
        fails.append("no date; a letter of appreciation names the event's dates")
    if not numbers(body):
        fails.append("no count; how many people, hours, or items")
    if not re.search(r"\b(?:thank|thanks|appreciat|grateful)\w*", body, re.I):
        fails.append("no thanks sentence")
    if not re.search(ROLE_VERBS, body, re.I):
        fails.append("no sentence naming what the person did (a plain verb: served as, planned, taught, sourced)")
    if re.search(r"\b(?:throughout the year|over the past year|during your tour|your time (?:at|with|in)|entire tenure)\b", body, re.I):
        warns.append("reads as a period of service rather than an event; that is a fitness report or an award, not a letter of appreciation")

    for w in strike_hits(body):
        warns.append(f"strike list: '{w}'")
    for b in blocked_hits(body):
        fails.append(f"blocked content: {b}")
    if dashes(body):
        fails.append("em or en dash present")
    wc = words(body)
    if wc > 300:
        warns.append(f"{wc} words; a letter of appreciation is one page and usually under 250")

    print(f"LOA CHECK: {sys.argv[1]}  {len(paras)} paragraphs, {wc} words")
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
