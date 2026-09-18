#!/usr/bin/env python3
"""Check an endorsement spec (spec.json for naval-letter/scripts/build_letter.py) against SECNAV M-5216.5
(June 2015) chapter 9, Endorsements, the layout the library's own figures show (MCO 1900.16 Figures 6-5 and
L-10; NAVMC 4000.5D enclosure (12)), and the kit's correspondence standard. Paragraph numbers in the messages
are the manual's.

Usage:  python3 endorsement_check.py spec.json [--basic-subj "SUBJ OF THE BASIC LETTER"]
            [--basic-refs "title" ...] [--basic-encls "title" ...] [--originator "the originator by billet"]
            [--prior-endorsers "activity" ...] [--basic-copy-to "activity" ...]

  --basic-refs, --basic-encls   every reference and enclosure already identified on the basic letter and in
        previous endorsements, in order. 9-2.3 and 9-2.4: the endorsement does not repeat them, and letters
        and numbers what it adds by continuing the sequence.
  --originator, --prior-endorsers, --basic-copy-to   9-2.5: on a significant endorsement each of these is a
        copy to addressee on this endorsement.

Test inputs in this repo: evals/endorsement/inputs/good.json (exit 0), later.json (exit 0), and bad.json with
--basic-subj "REQUEST FOR SPECIAL LIBERTY" --basic-refs "MCO 1050.3J" (exit 1).

Exit 0 = passes (warnings allowed); 1 = identification line incomplete, Subj changed, action missing from the
first sentence, a reference or enclosure the basic letter already lists, a significant endorsement with no copy
to block or with one that omits an addressee 9-2.5 requires, a declared continuation that does not match the
sequence, a name, a promise, a lifted phrase, blocked content, a dash.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes  # noqa: E402

ORDINALS = ["FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH", "EIGHTH", "NINTH", "TENTH"]
GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|Colonel|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj|LtCol|Col)"
LETTERS = "abcdefghijklmnopqrstuvwxyz"
# 9-2.5, in the manual's own words: 'Significant endorsements include "forwarded, recommending disapproval,"
# "readdressed and forwarded," and those with substantive comments. Routine endorsements include "forwarded,"
# "forwarded for consideration," and "forwarded, recommending approval."'  Significant is tested first, because
# "Forwarded, recommending disapproval" also opens with the routine word.
SIGNIFICANT = r"^(?:Forwarded,?\s+recommending\s+disapproval|Readdressed|Returned|Disapproved|I\s+do\s+not\s+recommend|I\s+do\s+not\s+concur|I\s+disagree)\b"
ROUTINE = r"^(?:Forwarded\s+for\s+consideration|Forwarded,?\s+recommending\s+approval|Forwarded)\b"
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
    "puts the battalion command post exercise on the two days requested",
    "the second operator is on leave until 22 October 2026",
    "A request for 24 through 26 October 2026 would be supported",
    "Battalion training schedule for the week of 12 October 2026",
]
DATE_IN_LINE = r"\b(?:of|dated)\s+\d{1,2} [A-Z][a-z]{2} \d{2}\b|\b(?:of|dated)\s+\d{1,2} [A-Z][a-z]+ \d{4}\b"


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    spec = json.load(open(args[0], encoding="utf-8"))
    basic_subj = None
    originator = None
    lists = {"--basic-refs": [], "--basic-encls": [], "--prior-endorsers": [], "--basic-copy-to": []}
    i = 1
    while i < len(args):
        if args[i] == "--basic-subj" and i + 1 < len(args):
            basic_subj = args[i + 1]; i += 2
        elif args[i] == "--originator" and i + 1 < len(args):
            originator = args[i + 1]; i += 2
        elif args[i] in lists:
            key = args[i]; i += 1
            while i < len(args) and not args[i].startswith("--"):
                lists[key].append(args[i]); i += 1
        else:
            i += 1
    basic_refs = lists["--basic-refs"]
    basic_encls = lists["--basic-encls"]
    prior_endorsers = lists["--prior-endorsers"]
    basic_copy_to = lists["--basic-copy-to"]
    norm = lambda t: re.sub(r"[^a-z0-9]", "", str(t).lower())
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
            notes.append(f"{ordinal} endorsement: 9-2.1.b numbers each endorsement 'in the sequence in which it is added to the basic letter', so the ordinal counts the endorsements already on it, not the echelons in the chain; check it against the endorsements the basic letter carries. Chapter 9 does not say whether an echelon may be passed over")
        if not re.search(r"\b(?:ltr|AA form|report|request|memo(?:randum)?)\b", on, re.I):
            fails.append(f"identification line does not name the basic correspondence by type ('ltr', 'AA form', 'report'): {on!r}")
        if not re.search(DATE_IN_LINE, on):
            fails.append(f"identification line does not carry the basic correspondence's date after 'of' or 'dated': {on!r}")
        if re.search(r"\bltr\b", on, re.I) and not re.search(r"\bltr \d{4,5}\b", on):
            fails.append(f"a letter is identified by 'ltr <SSIC> <code> of <date>'; no SSIC after 'ltr': {on!r}")
        if re.search(r"\[[A-Z ]+\]", on):
            fails.append("placeholder in the identification line; ask for the missing value, never guess it")

    if spec.get("same_page"):
        notes.append("same page endorsement: 9-1 allows it only 'If it will completely fit on the signature page of the basic letter or the preceding endorsement', Figure 9-1 adds 'it is sure to be signed without revision', and 9-2.1.a lets it omit 'the SSIC, subject and the basic letter's identification symbols' 'as long as the entire page will be photocopied'. build_letter.py renders a new page endorsement only; a same page endorsement is typed onto the signed page it rides on")

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
    # ---- 9-2.5: significant or routine, and the copy to block that follows from it ----
    first_line = texts[0].strip() if texts else ""
    if re.match(SIGNIFICANT, first_line, re.I):
        kind = "significant"
    elif re.match(ROUTINE, first_line, re.I):
        kind = "routine"
    else:
        kind = "unclassed"
    copy_to = spec.get("copy_to") or []
    if isinstance(copy_to, str):
        copy_to = [copy_to]
    copy_to = [c for c in copy_to if str(c).strip()]
    if kind == "significant":
        required = ([originator] if originator else []) + prior_endorsers + basic_copy_to
        if not copy_to:
            fails.append("a significant endorsement with no copy to block. 9-2.5: 'If your endorsement is significant and not routine, each activity that endorsed the basic letter before you and the originator of the basic letter shall be included as a copy to addressee on your endorsement. Additionally, all copy to addressees from the basic letter and previous endorsements shall be included as a copy to addressee.' 9-2.5 counts 'forwarded, recommending disapproval,' 'readdressed and forwarded,' and substantive comments as significant")
        else:
            have = {norm(c) for c in copy_to}
            for r in required:
                if norm(r) not in have:
                    fails.append(f"the copy to block does not carry {r!r}; 9-2.5 puts the originator of the basic letter, each activity that endorsed it before you, and every copy to addressee from the basic letter and previous endorsements on a significant endorsement")
            if not required:
                notes.append("significant endorsement: the copy to block was not checked against the chain, because --originator, --prior-endorsers and --basic-copy-to were not given. 9-2.5 puts the originator of the basic letter, each prior endorser, and all earlier copy to addressees in it")
            notes.append("9-2.6.c: 'If a copy to addressee will be receiving the basic letter and previous endorsements for the first time from you, to the right of each of these addressees, type the word \'complete\' in parentheses'")
        notes.append("build_letter.py prints no copy to block; type it at the left margin below the signature, as Figures 9-1 and 9-2 print it, before the endorsement is signed")
    elif kind == "routine" and copy_to:
        notes.append("9-2.5 requires the copy to block on an endorsement that is 'significant and not routine'; it lists this action as routine, and neither requires the block nor forbids it")
    elif kind == "unclassed" and texts:
        warns.append("the action in the first sentence is none of the six 9-2.5 names ('forwarded,' 'forwarded for consideration,' 'forwarded, recommending approval' routine; 'forwarded, recommending disapproval,' 'readdressed and forwarded' significant). 9-2.5 also makes an endorsement carrying substantive comments significant and does not define substantive, so the endorser decides: if these comments are substantive, the copy to block is required")

    # ---- 9-2.3 and 9-2.4: what the endorsement adds, and the letters and numbers it carries ----
    refs = spec.get("refs") or []
    encls = spec.get("encls") or []
    added_refs, added_encls = [], []
    for r in refs:
        if norm(r) in {norm(b) for b in basic_refs}:
            fails.append(f"reference {r!r} is already on the basic letter or a previous endorsement; 9-2.3: 'Do not repeat a reference in the reference line of your endorsement that has already been identified in the reference line of the basic letter or a previous endorsement. Identify only the references that you add.'")
        else:
            added_refs.append(r)
    for e_ in encls:
        if norm(e_) in {norm(b) for b in basic_encls}:
            fails.append(f"enclosure {e_!r} is already on the basic letter or a previous endorsement; 9-2.4: 'Do not repeat an enclosure in your enclosure line that has already been identified in the enclosure line of the basic letter or prior endorsements. Identify only the enclosures that you add.'")
        else:
            added_encls.append(e_)

    def continuation(items, already, declared, kindname, para, unit):
        """9-2.3 / 9-2.4: what this endorsement adds continues the sequence from the basic letter."""
        if not items:
            return
        if not already:
            notes.append(f"added {kindname}: {para} letters and numbers what an endorsement adds 'by continuing the sequence ... from the basic letter and previous endorsements'; pass --basic-{kindname} so the check can name the {unit} each added one carries")
            return
        start = len(already)
        if kindname == "refs":
            if start + len(items) > 26:
                return
            want = [f"({LETTERS[start + n]})" for n in range(len(items))]
            through = f"({LETTERS[start - 1]})"
            first_mark = LETTERS[start]
        else:
            want = [f"({start + n + 1})" for n in range(len(items))]
            through = f"({start})"
            first_mark = str(start + 1)
        if declared:
            if str(declared).strip("() ").lower() != first_mark:
                fails.append(f"the spec declares the first added {unit} as {declared!r}; the basic letter and previous endorsements run through {through}, so {para} makes it ({first_mark})")
                return
        warns.append(f"{para}: the basic letter and previous endorsements carry {kindname} through {through}, so what this endorsement adds is {' '.join(want)}; build_letter.py starts a block at ({'a' if kindname == 'refs' else '1'}), so correct the block on the page before signature")

    continuation(added_refs, basic_refs, spec.get("refs_start"), "refs", "9-2.3", "letter")
    continuation(added_encls, basic_encls, spec.get("encls_start"), "encls", "9-2.4", "number")
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
