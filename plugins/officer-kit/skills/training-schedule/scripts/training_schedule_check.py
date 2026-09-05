#!/usr/bin/env python3
"""Check a weekly training schedule (schedule.md).

Usage:  python3 training_schedule_check.py schedule.md
Exit 0 = passes (warnings allowed); 1 = a row missing its core fields, a name, or blocked content.
"""
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, dashes  # noqa: E402

GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"
HAZ = r"\b(?:range|live fire|fire|weapons?|rounds?|vehicle|convoy|motor|swim|water|rappel|heights?|obstacle|hike|march|PFT|CFT|MCMAP|grenade|demolition|breach)\b"
TR = r"\b\d{4}-[A-Z0-9]{2,6}-\d{4}\b"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails, warns = [], []
    rows = []
    for line in text.splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 10 and c[0] in ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun") or (len(c) >= 10 and re.match(r"^\d{1,2} \w{3}", c[0])):
            rows.append(c)
    if not rows:
        fails.append("no schedule rows found (Day | Time | Event | T&R code | Place | Instructor | Uniform and gear | Prereqs | RAW | Range pkg)")
    by_slot = defaultdict(list)
    for c in rows:
        day, time, event, code, place, instr, gear, prereq, raw, pkg = c[:10]
        tag = f"{day} {time} {event[:30]}"
        for name, val in (("time", time), ("event", event), ("place", place), ("instructor", instr)):
            if not val or val.upper() == "TBD":
                fails.append(f"{tag}: no {name}")
        if not re.search(TR, code) and not re.search(r"none|annual|admin|medical|higher", code, re.I):
            warns.append(f"{tag}: no T&R code and no stated reason")
        if re.search(HAZ, event, re.I) and (not raw or raw.lower() in ("", "n/a", "none")):
            fails.append(f"{tag}: hazardous event with no risk assessment status (drafted, signed, pending)")
        if re.search(r"\brange\b|live fire", event, re.I) and (not pkg or pkg.lower() in ("", "n/a", "none")):
            warns.append(f"{tag}: range event with no range package status")
        if re.search(GRADES + r"\s+[A-Z][a-z]+", instr):
            fails.append(f"{tag}: instructor by name; billets only")
        if instr:
            by_slot[(day, time, instr.lower())].append(event)
        if re.search(r"\ball hands\b", event, re.I) and not re.search(r"\d", event):
            warns.append(f"{tag}: 'all hands' without a count")
    for (day, time, instr), evs in by_slot.items():
        if len(evs) > 1:
            fails.append(f"instructor '{instr}' double booked {day} {time}: {', '.join(evs)}")
    if not re.search(r"^## Prep list", text, re.M):
        warns.append("no Prep list section")
    else:
        prep = re.search(r"^## Prep list\s*$(.*?)(?=^## |\Z)", text, re.M | re.S).group(1)
        prows = [[x.strip() for x in r.strip().strip("|").split("|")] for r in prep.splitlines() if r.strip().startswith("|") and "Event" not in r and not re.match(r"^\|\s*-", r.strip())]
        for r in prows:
            if len(r) < 4 or any(not x for x in r[:4]) or not re.search(r"\d", r[3]):
                warns.append(f"prep row incomplete or undated: {' | '.join(r)[:60]}")
    if not re.search(r"^## Conflicts and gaps", text, re.M):
        warns.append("no Conflicts and gaps section; a week with none should say none")
    for b in blocked_hits(text, allow=("medical",)):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")
    print(f"SCHEDULE CHECK: {sys.argv[1]}  {len(rows)} events")
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
