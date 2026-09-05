#!/usr/bin/env python3
"""Check an endorsement spec (spec.json for naval-letter/scripts/build_letter.py) against the layout the
library's own figures settle (MCO 1900.16 Figures 6-5 and L-10; NAVMC 4000.5D enclosure (12)) and the kit's
correspondence standard. SECNAV M-5216.5 is not in the library; what only it settles is reported as a note,
never checked as if known.

Usage:  python3 endorsement_check.py spec.json [--basic-subj "SUBJ OF THE BASIC LETTER"] [--basic-refs "title" ...]
Exit 0 = passes (warnings allowed); 1 = identification line incomplete, Subj changed, action missing from the
first sentence, a Ref the basic letter already lists, a name, a promise, a lifted phrase, blocked content, a dash.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes  # noqa: E402

ORDINALS = ["FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH", "EIGHTH", "NINTH", "TENTH"]
GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|Colonel|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj|LtCol|Col)"
ACTION = r"^(?:Forwarded|Readdressed|I (?:recommend|do not recommend|concur|do not concur|certify|direct|accept|return|agree|disagree)|Recommend(?:ing)? (?:approval|disapproval)|Returned|Concur|Approved|Disapproved)\b"
EXTRA_STRIKE = ["strongly recommend", "highly recommend", "wholeheartedly", "without reservation", "please", "kindly", "i feel", "i believe", "at your earliest convenience", "favorable consideration"]
PROMISE = r"\b(?:will be approved|guarantee\w*|is approved)\b"
LIFTED = [
    "I verified the leave balance of 31 days on 5 October 2026",
    "the section's two other licensed operators cover the period requested",
    "The Marine is the company's alternate armorer",
    "a start date 11 days before the battalion's field exercise",
    "a start date after 30 November 2026 would be supported",
    "meets the three conditions in reference (a) paragraph 4",
]
DATE_IN_LINE = r"\b(?:of|dated)\s+\d{1,2} [A-Z][a-z]{2} \d{2}\b|\b(?:of|dated)\s+\d{1,2} [A-Z][a-z]+ \d{4}\b"


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    spec = json.load(open(args[0], encoding="utf-8"))
    basic_subj = None
    basic_refs = []
    i = 1
    while i < len(args):
        if args[i] == "--basic-subj" and i + 1 < len(args):
            basic_subj = args[i + 1]; i += 2
        elif args[i] == "--basic-refs":
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                basic_refs.append(args[i]); i += 1
        else:
            i += 1
    fails, warns, notes = [], [], []

    e = spec.get("endorsement") or {}
    ordinal = str(e.get("ordinal", "")).upper()
    on = str(e.get("on", ""))
    if not e:
        fails.append("spec has no 'endorsement' block; build_letter.py needs {'ordinal': ..., 'on': ...} to print the identification line")
    else:
        if ordinal not in ORDINALS:
            fails.append(f"ordinal {ordinal!r} is not a written ordinal (FIRST, SECOND, ...)")
        elif ordinal != "FIRST":
            notes.append("a later endorsement: the ordinal sequence and whether a level may be skipped are settled by SECNAV M-5216.5, not in the library; confirm against the chain on the basic letter")
        if not re.search(r"\b(?:ltr|AA form|report|request|memo(?:randum)?)\b", on, re.I):
            fails.append(f"identification line does not name the basic correspondence by type ('ltr', 'AA form', 'report'): {on!r}")
        if not re.search(DATE_IN_LINE, on):
            fails.append(f"identification line does not carry the basic correspondence's date after 'of' or 'dated': {on!r}")
        if re.search(r"\bltr\b", on, re.I) and not re.search(r"\bltr \d{4,5}\b", on):
            fails.append(f"a letter is identified by 'ltr <SSIC> <code> of <date>'; no SSIC after 'ltr': {on!r}")
        if re.search(r"\[[A-Z ]+\]", on):
            fails.append("placeholder in the identification line; ask for the missing value, never guess it")

    subj = str(spec.get("subj", "")).strip()
    if not subj:
        fails.append("no Subj; the endorsement repeats the basic correspondence's Subj line")
    elif basic_subj and subj.upper() != basic_subj.strip().upper():
        fails.append(f"Subj changed: endorsement {subj.upper()!r}, basic {basic_subj.strip().upper()!r}; the endorsement carries the same subject")
    for k in ("from", "to"):
        if not spec.get(k):
            fails.append(f"no '{k}' line")
    if spec.get("via") == []:
        pass
    paras = spec.get("paragraphs") or []
    texts = []

    def walk(items):
        for it in items:
            if isinstance(it, str):
                it = {"text": it}
            texts.append(it.get("text", ""))
            walk(it.get("subs") or [])
    walk(paras)
    body = "\n".join(texts)
    if not texts:
        fails.append("no paragraphs")
    else:
        first = texts[0].strip()
        if not re.match(ACTION, first):
            fails.append(f"the first sentence does not state the endorser's action (Forwarded, recommending ...; I concur; I certify; I direct; Readdressed and forwarded): {first[:60]!r}")
        if re.match(r"^Forwarded, recommending (?:approval|disapproval)\.?\s*$", first) and len(texts) == 1:
            warns.append("a recommendation with no reason; the addressee has nothing to check (voice.md)")
        if re.search(r"disapprov|do not recommend|do not concur|disagree", first, re.I) and not re.search(r"\d", body):
            warns.append("a disapproval or disagreement with no date or count in it; the requester reads this")
        if len(texts) > 3:
            warns.append(f"{len(texts)} paragraphs; an endorsement is normally one or two")
    refs = spec.get("refs") or []
    if basic_refs:
        norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
        for r in refs:
            if norm(r) in {norm(b) for b in basic_refs}:
                fails.append(f"reference {r!r} is already on the basic letter; the endorsement's Ref block is for what it adds")
    if refs or spec.get("encls"):
        notes.append("added references or enclosures: how they are lettered and numbered against the basic letter's is settled by SECNAV M-5216.5, not in the library; the product marks the sequence as unverified")
    for w in strike_hits(body) + [w for w in EXTRA_STRIKE if w in body.lower()]:
        warns.append(f"strike list: '{w}'")
    if re.search(PROMISE, body, re.I):
        fails.append(f"a promise about the decision ('{re.search(PROMISE, body, re.I).group(0)}'); the addressee decides")
    allt = json.dumps(spec)
    mm = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]{2,}\b", re.sub(r"<MARINE>", "", allt))
    if mm and not re.search(r"^(?:Sergeant Major|First Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|Lance Corporal|Lieutenant Colonel) (?:Major|Sergeant|Corporal|Colonel)$", mm.group(0)):
        fails.append(f"a name appears ('{mm.group(0)}'); <MARINE> until substitution on the user's computer")
    for p in LIFTED:
        if p.lower() in allt.lower():
            fails.append(f"lifted from the exemplar or voice file: '{p}'; the example teaches shape, the intake supplies facts")
    for b in blocked_hits(body):
        fails.append(f"blocked content: {b}")
    if dashes(allt):
        fails.append("em or en dash present")

    print(f"ENDORSEMENT CHECK: {args[0]}  {ordinal or 'no ordinal'}  {len(texts)} paragraphs")
    for n in notes:
        print(f"  NOTE  {n}")
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
