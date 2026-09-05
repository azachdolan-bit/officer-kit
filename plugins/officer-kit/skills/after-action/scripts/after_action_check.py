#!/usr/bin/env python3
"""Check an after action report (aar.md).

Usage:  python3 after_action_check.py aar.md
Exit 0 = passes (warnings allowed); 1 = missing section or blocked content.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, strike_hits, dashes, words, numbers  # noqa: E402

GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"
TOPIC_FIX = r"^(?:improve|better|more|increase|enhance)\b"


def section(text, name):
    m = re.search(r"^## " + name + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails, warns = [], []
    for s in ("Planned", "What happened", "Sustain", "Improve"):
        if section(text, s) is None:
            fails.append(f"missing section: {s}")
    wh = section(text, "What happened") or ""
    obs = [l for l in wh.splitlines() if l.strip().startswith("-")]
    if not obs:
        fails.append("What happened has no observation lines (- <time>: <fact with a number>)")
    for l in obs:
        if not re.search(r"\b\d{3,4}\b|\b\d{1,2} \w+ \d{4}\b", l):
            warns.append(f"observation without a time: {l.strip()[:50]}")
        if len(numbers(l)) < 2:
            warns.append(f"observation without a number beyond the time: {l.strip()[:50]}")
    for name, cols in (("Sustain", 3), ("Improve", 4)):
        sec = section(text, name) or ""
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in sec.splitlines() if r.strip().startswith("|") and not re.match(r"^\|\s*-", r.strip()) and "Observation" not in r]
        if not rows:
            warns.append(f"{name} has no rows")
        for r in rows:
            if len(r) < cols or any(not c for c in r[:cols]):
                warns.append(f"{name} row incomplete: {' | '.join(r)[:60]}")
            if name == "Improve" and len(r) >= 2 and re.match(TOPIC_FIX, r[1].strip(), re.I):
                warns.append(f"Improve fix is a topic, not a change: '{r[1][:40]}'")
            if name == "Improve" and len(r) >= 4 and not re.search(r"\d", r[3]):
                warns.append(f"Improve row has no date: '{r[3]}'")
    m = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]+", text)
    if m:
        fails.append(f"a name appears in the AAR ('{m.group(0)}'); billets only")
    for w in strike_hits(text):
        warns.append(f"strike list: '{w}'")
    for b in blocked_hits(text, allow=("medical",)):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")
    print(f"AAR CHECK: {sys.argv[1]}  {len(obs)} observations, {words(text)} words")
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
