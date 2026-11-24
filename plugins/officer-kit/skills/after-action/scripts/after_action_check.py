#!/usr/bin/env python3
"""Check an after action report (aar.md).

Usage:  python3 after_action_check.py aar.md [--sections "Planned,What happened,Sustain,Improve"]
  --sections   the exemplar's own headings, in that order, when the AAR follows an approved exemplar
               instead of the fallback shape; every test runs on the mapped sections, at any heading level
Exit 0 = passes (warnings allowed); 1 = missing section or blocked content.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, strike_hits, dashes, words, numbers  # noqa: E402

GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"
TOPIC_FIX = r"^(?:improve|better|more|increase|enhance)\b"


def section(text, name, any_level=False):
    h = r"#{1,6} " if any_level else r"## "
    m = re.search(r"^" + h + re.escape(name) + r"\s*$(.*?)(?=^" + h + r"|\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def main():
    args = sys.argv[1:]
    names, mapped = ["Planned", "What happened", "Sustain", "Improve"], False
    if "--sections" in args:
        i = args.index("--sections")
        if i + 1 >= len(args):
            sys.exit(__doc__)
        names = [n.strip() for n in args[i + 1].split(",")]
        del args[i:i + 2]
        mapped = True
        if len(names) != 4 or not all(names):
            sys.exit("--sections takes four headings: Planned, What happened, Sustain, Improve, in that order")
    if len(args) != 1:
        sys.exit(__doc__)
    sys.argv[1:] = args
    text = open(args[0], encoding="utf-8").read()
    sec = dict(zip(("Planned", "What happened", "Sustain", "Improve"), names))
    fails, warns = [], []
    for k, s in sec.items():
        if section(text, s, mapped) is None:
            fails.append(f"missing section: {s}" + (f" (mapped to {k})" if mapped else ""))
    wh = section(text, sec["What happened"], mapped) or ""
    obs = [l for l in wh.splitlines() if l.strip().startswith("-")]
    if not obs and mapped:
        obs = [l for l in wh.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not obs:
        fails.append(f"{sec['What happened']} has no observation lines (- <time>: <fact with a number>)")
    for l in obs:
        if not re.search(r"\b\d{3,4}\b|\b\d{1,2} \w+ \d{4}\b", l):
            warns.append(f"observation without a time: {l.strip()[:50]}")
        if len(numbers(l)) < 2:
            warns.append(f"observation without a number beyond the time: {l.strip()[:50]}")
    for name, cols in (("Sustain", 3), ("Improve", 4)):
        body = section(text, sec[name], mapped) or ""
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in body.splitlines() if r.strip().startswith("|") and not re.match(r"^\|\s*-", r.strip()) and "Observation" not in r]
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
