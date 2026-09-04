#!/usr/bin/env python3
"""Check a board briefing sheet (brief.md from references/template.md).

Usage:  python3 brief_check.py brief.md --minutes N [--package letter.json]
Exit 0 = passes (warnings allowed); 1 = missing field, missing so what line, blocked content,
or a number on the sheet that is not in the package.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, strike_hits, dashes, words  # noqa: E402

FIELDS = ["Board", "Clock", "Billet", "Additional duties", "Derogatory material", "TIS / TIG", "PME",
          "MCI / MarineNet", "Reading list", "Off duty education", "PFT", "CFT", "Rifle", "Pistol", "Swim",
          "MCMAP", "Height / weight", "Annual training", "Awards", "Deployments", "Community service"]
WPM = 140
WORD_NUMBERS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"}


def nums(text):
    out = set()
    for m in re.findall(r"\$?\d[\d,]*(?:\.\d+)?", text):
        out.add(m.replace("$", "").replace(",", ""))
    for w in re.findall(r"[a-z]+", text.lower()):
        if w in WORD_NUMBERS:
            out.add(WORD_NUMBERS[w])
    return out


def flat(p):
    t = p.get("text", "")
    for s in p.get("subs", []):
        t += " " + flat(s)
    return t


def main():
    if len(sys.argv) < 4 or "--minutes" not in sys.argv:
        sys.exit(__doc__)
    path = sys.argv[1]
    minutes = float(sys.argv[sys.argv.index("--minutes") + 1])
    pkg = sys.argv[sys.argv.index("--package") + 1] if "--package" in sys.argv else None
    text = open(path, encoding="utf-8").read()
    fails, warns = [], []

    for f in FIELDS:
        if not re.search(r"^\s*" + re.escape(f) + r"\s*:", text, re.M) and not re.search(r"\b" + re.escape(f) + r"\s*:", text):
            fails.append(f"field missing: {f}")
    blanks = len(re.findall(r"\[\s*\]", text))
    if blanks:
        warns.append(f"{blanks} blank field(s) the briefer must fill before the board")

    m = re.search(r"^## So what\s*$(.*?)(?:^##|\Z)", text, re.M | re.S)
    if not m:
        fails.append("no '## So what' section")
    else:
        lines = [l for l in m.group(1).splitlines() if re.match(r"^\s*\d\.\s+\S", l)]
        if len(lines) < 3:
            fails.append(f"{len(lines)} so what lines; three required, each a fact with a number and what it did for the unit")
        for l in lines:
            if not nums(re.sub(r"^\s*\d\.\s+", "", l)):
                fails.append(f"so what line without a number: {l.strip()[:60]}")
            if len(l.split()) > 35:
                warns.append(f"so what line over 35 words; a board member should be able to repeat it: {l.strip()[:50]}...")
        for w in strike_hits(m.group(1)):
            warns.append(f"strike list in the so what lines: '{w}'")

    spoken = re.sub(r"Questions the board may ask:.*", "", text, flags=re.S)
    wc = words(spoken)
    est = wc / WPM
    if est > minutes:
        warns.append(f"about {wc} words, {est:.1f} minutes at {WPM} a minute; the clock is {minutes:g}")

    for b in blocked_hits(text):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")

    if pkg:
        spec = json.load(open(pkg, encoding="utf-8"))
        ptext = " ".join(flat(p) for p in spec.get("paragraphs", [])) + " " + spec.get("subj", "") + " " + spec.get("poc", "")
        sheet_nums = nums(re.sub(r"(?m)^(?:Board|Clock|TIS / TIG|PME|Annual training|Awards)\s*:.*$", "", text))
        missing = sorted(sheet_nums - nums(ptext), key=lambda s: (len(s), s))
        if missing:
            fails.append(f"numbers on the sheet not in the package: {', '.join(missing)} (same numbers, exactly)")
        else:
            print(f"  package agreement: every number on the sheet appears in {pkg}")

    print(f"BOARD BRIEF CHECK: {path}  {wc} spoken words, about {est:.1f} minutes")
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
