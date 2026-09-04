#!/usr/bin/env python3
"""Check a counseling record (counseling.md in the default worksheet blocks).

Usage:  python3 counseling_check.py counseling.md
Exit 0 = passes (warnings allowed); 1 = missing block, undated incident, blocked content,
or a promise the leader cannot keep.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, dashes  # noqa: E402

DATE = r"\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b"
TRAITS = ["attitude", "lazy", "unreliable", "unmotivated", "disrespectful", "constantly", "always", "never", "bad", "poor", "sloppy", "careless", "unprofessional", "motivated", "outstanding"]
PROMISES = r"\b(?:will be (?:separated|discharged|promoted|reduced|NJP'?d|charged)|separation|administrative separation|page 11|NJP|non-?judicial punishment|court[- ]martial)\b"
CADENCE = r"\b(?:daily|weekly|biweekly|every (?:day|week|Monday|Tuesday|Wednesday|Thursday|Friday)|each (?:morning|day|week))\b"
MENTOR = r"\bmentor\b.*?\b(?:Private|PFC|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Chief Warrant Officer|Warrant Officer)\b"


def block(text, letter):
    m = re.search(r"^##\s*" + letter + r"\.\s*[^\n]*\n(.*?)(?=^##\s*[A-Z]\.|\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails, warns = [], []
    A, B, C, D, E, F, G = (block(text, x) for x in "ABCDEFG")

    if A is None:
        fails.append("block A (administrative) missing")
    else:
        for f in ("Marine", "Counselor", "Date", "Type"):
            if not re.search(r"^\s*" + f + r"\s*:", A, re.M):
                fails.append(f"block A: {f} line missing")
    initial = A is not None and re.search(r"Type\s*:\s*initial", A, re.I)
    if initial:
        if B is None:
            fails.append("initial counseling needs block B (billet and standards)")
        else:
            if not re.search(r"Goals", B, re.I) or len(re.findall(DATE, B)) < 2:
                fails.append("block B: goals for the period with dates, and the next counseling date")
    else:
        if C is None:
            fails.append("block C (observations and incidents) missing")
        else:
            lines = [l for l in C.splitlines() if l.strip().startswith(("-", "*")) or re.match(r"^\s*\d+\.", l)]
            if not lines:
                fails.append("block C: no incident lines (one per line, dated)")
            for l in lines:
                if not re.search(DATE, l):
                    fails.append(f"block C: undated incident: {l.strip()[:60]}")
                if not re.search(r"\bobserved by\b|\breported by\b", l, re.I):
                    warns.append(f"block C: who observed it? {l.strip()[:50]}...")
                traits = [t for t in TRAITS if re.search(r"\b" + t + r"\b", l, re.I)]
                if traits:
                    warns.append(f"block C: trait words in an incident line ({', '.join(traits)}); record the incident, not the characterization")
        if D is None:
            fails.append("block D (evaluation) missing")
        else:
            sents = len(re.findall(r"[.!?](?:\s|$)", D))
            if sents > 5:
                warns.append(f"block D: {sents} sentences; three is the standard (the pattern, the cost, one honest strength)")
            if not re.search(r"\b(?:cost|meant|missed|delayed|spent|not (?:moved|transported|delivered|submitted)|effect|mission|section|platoon)\b", D, re.I):
                warns.append("block D: name what it cost the unit or the mission")
    if E is None:
        fails.append("block E (plan) missing")
    else:
        if not re.search(MENTOR, E, re.I | re.S):
            fails.append("block E: no mentor by grade and name")
        if not re.search(CADENCE, E, re.I):
            fails.append("block E: no feedback cadence (weekly on a named day)")
        if not re.search(r"return condition", E, re.I) or not re.search(DATE, E):
            fails.append("block E: no return condition with a date (what, done by when, ends the plan)")
        if not re.search(r"end state", E, re.I):
            fails.append("block E: no end state sentence")
    if F is None:
        warns.append("block F (Marine's comments) missing; leave it for the Marine")
    if G is None:
        fails.append("block G (signatures) missing")

    for b in blocked_hits(text, allow=()):
        fails.append(f"blocked content: {b}")
    m = re.search(PROMISES, text, re.I)
    if m:
        fails.append(f"promise or punitive language the counselor cannot make in a counseling record: '{m.group(0)}'")
    if dashes(text):
        fails.append("em or en dash present")

    print(f"COUNSELING CHECK: {sys.argv[1]}  type: {'initial' if initial else 'event or follow on'}")
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
