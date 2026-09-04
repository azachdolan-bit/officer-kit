#!/usr/bin/env python3
"""Check a letter of recommendation spec (the naval-letter JSON) for the six part shape.

Usage:  python3 lor_check.py letter.json
Exit 0 = passes (warnings allowed); 1 = structural failure or blocked content.

Checks: six numbered paragraphs (POC may be the "poc" field or paragraph 6); paragraph 1 states
a period (two month year mentions or "from ... to"); paragraph 2 recommends and ranks with a
denominator; paragraphs 3 and 4 carry at least three numbers between them; a POC exists;
strike list words (warn); blocked content (fail); rough length under one page (warn over 420 words).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, numbers, dashes, words  # noqa: E402

MONTH = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{4}"


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
    poc = spec.get("poc", "")
    body = " ".join(paras) + " " + poc
    fails, warns = [], []

    if len(paras) + (1 if poc else 0) < 6:
        fails.append(f"{len(paras)} paragraphs plus {'a' if poc else 'no'} POC; the shape is six: standing, recommendation and ranking, specifics, scene, close, POC")
    if paras:
        p1 = paras[0]
        if not (len(re.findall(MONTH, p1)) >= 2 or re.search(r"\bfrom\b.*\b(?:to|until|through)\b", p1, re.I)):
            fails.append("paragraph 1 does not state the period of observation (from <month year> to <month year>)")
        if not re.search(r"\b(?:served|commanded|supervised|led|observed)\b", p1, re.I):
            warns.append("paragraph 1 should say what the writer was to the Marine (served as, commanded, supervised)")
    if len(paras) > 1:
        p2 = paras[1]
        if not re.search(r"\brecommend", p2, re.I):
            fails.append("paragraph 2 does not recommend")
        rank = re.search(r"\b(?:best|top|finest|first)\b.*?\b(?:of|among)\b.*?\d", p2, re.I) or re.search(r"\b(?:number|no\.)\s*\d+\s+of\s+\d+", p2, re.I)
        if not rank:
            if re.search(r"\b(?:among the best|one of the best|one of the finest)\b", p2, re.I):
                fails.append("paragraph 2 ranks without a denominator ('among the best' of how many, over what period?)")
            else:
                warns.append("paragraph 2 has no ranking statement (best of how many, over what period); the letter is weaker without one, which is the writer's call")
    if len(paras) > 3:
        n = len(numbers(paras[2])) + len(numbers(paras[3]))
        if n < 3:
            fails.append(f"paragraphs 3 and 4 carry {n} numbers; at least three (people, dollars, rates, dates of the scene)")
        if not re.search(MONTH, paras[3]) and not re.search(r"\b(?:in|on|during)\b .*?\b(?:20\d\d|exercise|deployment|inspection)\b", paras[3], re.I):
            warns.append("paragraph 4 (the scene) is not dated")
    if not poc and not (len(paras) >= 6 and re.search(r"point of contact", paras[-1], re.I)):
        fails.append("no point of contact")

    for w in strike_hits(body):
        warns.append(f"strike list: '{w}' (delete; if the sentence loses no fact, it was fluff)")
    for b in blocked_hits(body):
        fails.append(f"blocked content: {b}")
    if dashes(body):
        fails.append("em or en dash present")
    wc = words(body)
    if wc > 420:
        warns.append(f"{wc} words; a one page letter with the heading block runs about 420")

    print(f"LOR CHECK: {sys.argv[1]}  {len(paras)} paragraphs, {wc} words")
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
