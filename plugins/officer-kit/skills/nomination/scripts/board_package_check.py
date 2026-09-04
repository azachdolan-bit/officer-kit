#!/usr/bin/env python3
"""Check a board package recommendation letter (naval-letter JSON spec) against the board's skeleton.

Usage:  python3 board_package_check.py letter.json --kind merpro|nomination
Exit 0 = passes (warnings allowed); 1 = structural failure or blocked content.

Structure: paragraph 1 eligible and recommended per the reference; paragraph 2 enclosures, count
matching the encl list; paragraph 3 billets then subparagraphs a to g in the board's category order;
POC. Each category is scanned for the numbers the board expects (warn if absent). Identifiers
(EDIPI, SSN) are allowed in the subject line only. Blocked content fails.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, numbers, dashes, words  # noqa: E402

CATEGORIES = [
    ("a", "appearance and fitness", [r"\b(?:PFT|physical fitness test)\b", r"\b(?:CFT|combat fitness test)\b", r"\b(?:rifle|pistol)\b", r"\b(?:belt|MCMAP)\b", r"\b(?:swim|water survival)\b"]),
    ("b", "MOS competence", [r"\b(?:instruct|taught|train|licens|certif|inspect)\w*"]),
    ("c", "deployments", [r"\b(?:deploy\w*|not yet had the opportunity)\b"]),
    ("d", "maturity under stress", [r"\b(?:20\d\d|January|February|March|April|May|June|July|August|September|October|November|December)\b"]),
    ("e", "leadership", [r"\$\s?\d", r"\b(?:led|leads|leading|section|squad|team|platoon)\b"]),
    ("f", "professional growth", [r"\b(?:MarineNet|MCI|course|PME|reading list|credits?|degree)\b"]),
    ("g", "influence on the command", [r"\b(?:hours?)\b", r"\b(?:volunteer\w*|color guard|Single Marine Program|mentor\w*|community)\b"]),
]
LEAD_WORDS = {"merpro": r"eligible and recommended for meritorious promotion", "nomination": r"(?:eligible and )?(?:recommended|nominated) (?:for|as)"}


def flat(p):
    t = p.get("text", "")
    for s in p.get("subs", []):
        t += " " + flat(s)
    return t


def main():
    if len(sys.argv) < 4 or "--kind" not in sys.argv:
        sys.exit(__doc__)
    kind = sys.argv[sys.argv.index("--kind") + 1]
    if kind not in LEAD_WORDS:
        sys.exit("kind must be merpro or nomination")
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    paras = spec.get("paragraphs", [])
    encls = spec.get("encls", [])
    poc = spec.get("poc", "")
    fails, warns = [], []

    if len(paras) < 3:
        fails.append(f"{len(paras)} body paragraphs; the skeleton is three (recommendation, enclosures, billets and lettered accomplishments) plus POC")
    if paras and not re.search(LEAD_WORDS[kind], paras[0].get("text", ""), re.I):
        fails.append("paragraph 1 does not state the recommendation per the reference in the order's words")
    if paras and not re.search(r"\breference\b", paras[0].get("text", ""), re.I):
        warns.append("paragraph 1 should cite the reference (the local order)")
    if len(paras) > 1:
        p2 = paras[1].get("text", "")
        if not re.search(r"\benclosures?\b", p2, re.I):
            fails.append("paragraph 2 does not name the enclosures")
        m = re.search(r"\(1\) through \((\d+)\)", p2)
        if m and int(m.group(1)) != len(encls):
            fails.append(f"paragraph 2 says {m.group(1)} enclosures; the Encl list has {len(encls)}")
        if not encls:
            warns.append("no Encl list in the spec; copy the order's enclosure list in its order")
    if len(paras) > 2:
        p3 = paras[2]
        if not re.search(r"accomplishments are as follows", p3.get("text", ""), re.I):
            warns.append("paragraph 3 should end 'meritorious accomplishments are as follows:' before the lettered subparagraphs")
        if not re.search(r"\b(?:since|from) \w+ 20\d\d\b", p3.get("text", ""), re.I):
            warns.append("paragraph 3 should date each billet held")
        subs = p3.get("subs", [])
        if len(subs) < len(CATEGORIES):
            fails.append(f"paragraph 3 has {len(subs)} lettered subparagraphs; the board scores {len(CATEGORIES)} (a to g, see categories.md)")
        for i, (letter, name, pats) in enumerate(CATEGORIES):
            if i >= len(subs):
                break
            t = flat(subs[i])
            hits = [p for p in pats if re.search(p, t, re.I)]
            if len(hits) < max(1, len(pats) // 2):
                warns.append(f"({letter}) {name}: expected markers thin ({len(hits)} of {len(pats)}); if the category is empty, one honest sentence, not padding")
            if letter != "c" and not numbers(t):
                warns.append(f"({letter}) {name}: no number")
    if not poc:
        fails.append("no point of contact")

    body = " ".join(flat(p) for p in paras) + " " + poc
    for w in strike_hits(body):
        warns.append(f"strike list: '{w}'")
    for b in blocked_hits(body):
        fails.append(f"blocked content in the body: {b}")
    if dashes(body):
        fails.append("em or en dash present")
    print(f"BOARD PACKAGE CHECK ({kind}): {sys.argv[1]}  {len(paras)} paragraphs, {len(encls)} enclosures, {words(body)} words")
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
