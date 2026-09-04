#!/usr/bin/env python3
"""Mechanical check of a fitness report narrative draft against MCO 1610.7B style and content rules.

Usage:  python3 fitrep_check.py draft.md
Exit 0 = no prohibited item (warnings allowed), 1 = a prohibited item found.

Expects headings "## Section B", "## Section C", "## Section I". Checks:
  B and C: bullets preceded by a dash or circle; no superlatives; no uppercase shouting,
           quotation marks, bold or italic markers, or exclamation; C carries no award or
           personal quality language
  I:       mandatory comments first; each directed comment begins "Directed Comment. Sect A, Item"
           and uses the manual's required statement where one exists; no unacceptable topics
           (chapter 4 paragraph 13d); limited gender pronouns; no superlatives or shouting
  all:     character counts per section, so the user can compare with the form's space
"""
import re
import sys

SUPERLATIVES = r"\b(best|greatest|finest|most outstanding|unparalleled|unmatched|phenomenal|incredible|superb|flawless|perfect|unbelievable|top \d+%|number one|#1)\b"
UNACCEPTABLE = [
    (r"\b(NJP|non-?judicial punishment|court-?martial|civil action|criminal action|fact-?finding|investigation)\b", "13d(1) pending NJP, courts martial, civil or criminal action, boards, investigations"),
    (r"\b(suspected|suspicion of)\b.*\b(drug|criminal)\b", "13d(2) suspected criminal activity"),
    (r"\b(administrative reduction|administrative separation|adsep|withholding of promotion)\b", "13d(3) administrative reduction or separation proceedings"),
    (r"\b(letter of (admonition|caution|reprimand)|non-?punitive letter|NPLOC)\b", "13d(4) non punitive letters"),
    (r"\b(alcohol treatment|rehab(ilitation)?|SARP)\b", "13d(5) alcohol treatment"),
    (r"\b(speeding|traffic (ticket|citation|violation))\b", "13d(6) minor traffic violations"),
    (r"\b(non-?selected|not selected|passed over)\b", "13d(7) prior non selection"),
    (r"\b(spouse|wife|husband)\b", "13d(8) the spouse"),
    (r"\b(attractive|handsome|charming|best (woman|female|man|male)|female officer|male officer)\b", "13d(9) gender based comments"),
    (r"\b(pregnan\w+|postpartum|medical condition|injur(y|ed)|surgery|diagnos\w+)\b", "13d(10) medical matters (allowed only if performance was affected; confirm)"),
    (r"\b(family problems|marital|divorce|personal problems)\b", "13d(11) personal or family problems"),
    (r"\b(single parent|single mother|single father)\b", "13d(12) single parent status"),
    (r"\b(civilian (employment|career|job)|private sector)\b", "13d(13) civilian employment potential"),
    (r"\b(merit reorder)\b", "13d(15) merit reorder"),
    (r"\bbriefed as a\b", "13d(16) briefed as a number"),
]
C_FORBIDDEN = r"\b(awarded|award|NAM|Navy Achievement|Commendation Medal|letter of appreciation|certificate of commendation|dedicated|loyal|enthusiastic|motivated|potential|leader of|future)\b"
PROMO_STATEMENTS = [
    "I recommend that the MRO be considered for promotion ahead of contemporaries.",
    "I recommend that the MRO not be considered for promotion with contemporaries.",
    "I recommend that the MRO not be considered for promotion at any time.",
]
BODY_STATEMENTS = [
    "The MRO is not within body composition standards.",
    "MRO has an approved BCP waiver effective",
    "MRO is exempt from body fat limits due to his/her PFT and CFT scores",
    "MRO is within body fat limits due to the one percent allowance given for his/her PFT and CFT scores.",
    "The MRO has been assigned to the Body Composition Program.",
    "The MRO has been assigned to the Military Appearance Program.",
]

FAIL, WARN = [], []


def sections(text):
    out = {}
    cur = None
    for ln in text.splitlines():
        m = re.match(r"^##\s+Section\s+([BCI])\b", ln, re.I)
        if m:
            cur = m.group(1).upper()
            out[cur] = []
        elif cur:
            out[cur].append(ln)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def style(name, body):
    for w in re.findall(r"\b[A-Z]{4,}\b", body):
        if w not in ("MRO", "USMC", "PFT", "CFT", "MOS", "MCO", "NCO", "SNCO", "MAGTF", "MEU", "PME", "MCMAP", "TAD", "FMF", "OIC", "SNCOIC", "BCP", "HQMC"):
            WARN.append(f"{name}: uppercase word {w!r} (no UPPERCASE for emphasis)")
    if re.search(r"[\"“”]", body):
        FAIL.append(f"{name}: quotation marks are not permitted")
    if re.search(r"\*\*|__|(?<!\w)\*(?!\w)", body):
        FAIL.append(f"{name}: bold or italic markers are not permitted")
    if "!" in body:
        FAIL.append(f"{name}: exclamation is not permitted")
    for m in re.finditer(SUPERLATIVES, body, re.I):
        FAIL.append(f"{name}: superlative {m.group(0)!r}")


def bullets(name, body):
    lines = [l for l in body.splitlines() if l.strip()]
    bad = [l for l in lines if not re.match(r"^\s*[-•o*]\s", l)]
    if bad:
        FAIL.append(f"{name}: {len(bad)} line(s) not in bulleted form with a leading mark: {bad[0][:50]!r}")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    S = sections(text)
    if not S:
        sys.exit("no '## Section B/C/I' headings found")

    if "B" in S:
        style("Section B", S["B"]); bullets("Section B", S["B"])
    if "C" in S:
        style("Section C", S["C"]); bullets("Section C", S["C"])
        for m in re.finditer(C_FORBIDDEN, S["C"], re.I):
            WARN.append(f"Section C: {m.group(0)!r} looks like an award, personal quality, or potential; C carries results only")
    if "I" in S:
        I = S["I"]
        style("Section I", I)
        for pat, why in UNACCEPTABLE:
            for m in re.finditer(pat, I, re.I):
                FAIL.append(f"Section I: {m.group(0)!r} falls under unacceptable comments {why}")
        pron = len(re.findall(r"\b(he|she|him|his|her|hers|himself|herself)\b", I, re.I))
        words = max(1, len(I.split()))
        if pron / words > 0.05:
            WARN.append(f"Section I: {pron} gender pronouns in {words} words; the manual says to limit them (use MRO)")
        dcs = [l for l in I.splitlines() if l.strip().lower().startswith("directed comment")]
        for l in dcs:
            if not re.match(r"^Directed Comment\. Sect [A-K], Item \d+[a-z]?:", l.strip()):
                FAIL.append(f"Section I: directed comment must begin 'Directed Comment. Sect A, Item Nx:' -> {l.strip()[:60]!r}")
            if "Item 7" in l and not any(s in l for s in PROMO_STATEMENTS):
                FAIL.append("Section I: Item 7 directed comment must use one of the manual's three promotion statements verbatim")
            if re.search(r"Item 8", l) and re.search(r"body|weight|BCP", l, re.I) and not any(s in l for s in BODY_STATEMENTS):
                WARN.append("Section I: body composition directed comment should use one of the manual's six statements verbatim")
        first = next((l for l in I.splitlines() if l.strip()), "")
        if first.lower().startswith("directed comment") and "simultaneous report" not in I.lower():
            FAIL.append("Section I: mandatory comments (the word picture) must come before directed comments")

    print(f"FITREP CHECK: {sys.argv[1]}")
    for k in ("B", "C", "I"):
        if k in S:
            print(f"  Section {k}: {len(S[k])} characters, {len(S[k].split())} words")
    for w in WARN:
        print(f"  WARN  {w}")
    for f in FAIL:
        print(f"  FAIL  {f}")
    if not WARN and not FAIL:
        print("  clean")
    print(f"  -> {len(FAIL)} failures, {len(WARN)} warnings")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
