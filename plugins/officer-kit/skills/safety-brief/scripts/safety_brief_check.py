#!/usr/bin/env python3
"""Check a safety brief (brief.md).

Usage:  python3 safety_brief_check.py brief.md
Exit 0 = passes (warnings allowed); 1 = missing section, a name, or blocked content.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, strike_hits, dashes, words, numbers  # noqa: E402

GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"
EVENT = r"\b(?:died|death|drown\w*|crash\w*|rollover|hurt|injur\w*|hospital\w*|mishap|fatalit\w*|last (?:month|quarter|summer|year)|in (?:May|June|July|August|September|October|November|December|January|February|March|April))\b"
STRIKE_BRIEF = ["be safe", "use good judgment", "cannot stress enough", "as always", "remember that you represent"]


def section(text, name):
    m = re.search(r"^## " + name + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails, warns = [], []
    for s in ("The three things", "Resources", "Expectations"):
        if section(text, s) is None:
            fails.append(f"missing section: {s}")
    three = section(text, "The three things") or ""
    items = [l for l in three.splitlines() if re.match(r"^\s*\d\.\s+\S", l)]
    if len(items) != 3:
        warns.append(f"{len(items)} things; three is the number Marines remember")
    for l in items:
        body = re.sub(r"^\s*\d\.\s+", "", l)
        if not numbers(body) and not re.search(EVENT, body, re.I):
            fails.append(f"a thing without a number or a real event by type: {body[:50]}")
    res = section(text, "Resources") or ""
    if not re.search(r"\d{3}\)?[-. ]\d{3}[-. ]\d{4}", res):
        warns.append("no phone numbers in Resources; the user supplies them, the tool never guesses")
    m = re.search(r"Length:\s*(\d+)", text)
    wc = words(text)
    if m and wc > int(m.group(1)) * 140:
        warns.append(f"{wc} words for {m.group(1)} minutes; about {int(m.group(1)) * 140} fits")
    mm = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]+", text)
    if mm:
        fails.append(f"a name appears in the brief ('{mm.group(0)}'); mishaps by type and unit level only")
    low = text.lower()
    for w in STRIKE_BRIEF + strike_hits(text):
        if w in low:
            warns.append(f"strike: '{w}'")
    for b in blocked_hits(text, allow=("medical", "substance")):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")
    print(f"SAFETY BRIEF CHECK: {sys.argv[1]}  {wc} words")
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
