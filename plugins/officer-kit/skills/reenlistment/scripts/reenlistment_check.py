#!/usr/bin/env python3
"""Check a reenlistment recommendation (recommendation.md) against MCO 1040.31 enclosure (1) chapter 4
paragraph 4 and block 35 of NAVMC 11537.

Usage:  python3 reenlistment_check.py recommendation.md
Exit 0 = passes (warnings allowed); 1 = the tier is not supported by the population sentence, a mandatory
reason is missing, a non delegable tier is signed by a delegate, a not recommended Marine has no CO interview,
the windows do not match the dates, a name, a promise, a lifted exemplar phrase, or blocked content.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes, words  # noqa: E402
from reenlistment_windows import parse, windows  # noqa: E402

TIERS = [
    ("Recommended with Enthusiasm", 0.25),
    ("Recommended with Confidence", 0.50),
    ("Recommended with Reservation", None),
    ("Not Recommended", None),
]
BLOCKS = r"35([a-g])\s+(NCOIC ?/ ?SNCOIC|OIC|First Sergeant|Company Commander|Sergeant Major|Executive Officer|Commanding Officer)"
GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"
DATE = r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b"
PROMISE = r"\b(?:will (?:be approved|reenlist|make an? (?:outstanding|excellent|fine))|guarantee\w*|deserves to reenlist|is approved for reenlistment)\b"
EXTRA_STRIKE = ["asset to the marine corps", "great marine", "hard charger", "would follow anywhere", "no doubt", "definitely", "strongly recommend", "should be retained at all costs"]
# Phrases from references/exemplar.md and voice.md. A draft that carries one took its content from the example.
LIFTED = [
    "Standing: 8 of 22", "qualified 7 of 7 on the annual gun qualification", "the only one of the company's 9 squads",
    "since the section leader detached on 11 July 2026", "pro/con average 4.5/4.6 over 31 months",
    "Ranks 3 of the 14 sergeants known to me", "zero preventable equipment losses against a battalion average of three per section",
    "Has done the platoon sergeant's job for four months while the billet was gapped",
    "Two NJPs on this contract (12 March 2025, 4 August 2026)",
]


def section(text, name):
    m = re.search(r"## " + name + r"\s*\n(.*?)(?=\n## |\Z)", text, re.S)
    return m.group(1).strip() if m else None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8").read()
    text = re.sub(r"[ \t]+", " ", raw)
    fails, warns = [], []
    head = text.split("\n## ", 1)[0]

    if not re.search(r"^# Reenlistment recommendation", text, re.M):
        fails.append("title line '# Reenlistment recommendation' missing")
    if "<MARINE>" not in head:
        fails.append("the Marine line does not carry <MARINE>; the label stays until substitution on the user's computer")
    bm = re.search(BLOCKS, head, re.I)
    block = bm.group(1).lower() if bm else None
    if not bm:
        fails.append("no 'Block: 35a..35g <level>' line in the header (NAVMC 11537 block 35)")
    signed = re.search(r"Signed by:\s*(.+?)(?=\s+Date:|\s+References:|\n|$)", head, re.I)
    signer = signed.group(1).strip().lower() if signed else ""
    if not signed:
        warns.append("no 'Signed by:' line; the order lets the XO recommend for the CO except at two tiers, so say who signs")

    rec = section(text, "Recommendation")
    tier, share = None, None
    if rec is None:
        fails.append("no '## Recommendation' section")
    else:
        found = [(t, s) for t, s in TIERS if re.search(re.escape(t), rec, re.I)]
        if len(found) != 1:
            fails.append("exactly one of the form's four boxes must appear in ## Recommendation, in the form's words")
        else:
            tier, share = found[0]
            if share and not re.search(re.escape(tier) + r" \(Top " + str(int(share * 100)) + r" ?%\)", rec):
                warns.append(f"write the box as the form prints it: '{tier} (Top {int(share*100)} %)'")

    pop = section(text, "Population")
    if share:
        m = re.search(r"known to the certifying officer:\s*(\d+)\.?\s*Standing:\s*(\d+) of (\d+)", pop or "", re.I)
        if not pop or not m:
            fails.append(f"'{tier}' is a population claim (top {int(share*100)} percent of Marines in that grade known to the certifying officer, paragraph 4.d); ## Population must say how many are known and where this Marine stands, as numbers")
        else:
            n, k, n2 = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if n != n2:
                fails.append(f"population count {n} and standing denominator {n2} disagree")
            elif k < 1 or k > n:
                fails.append(f"standing {k} of {n} is not a place in that population")
            elif k / n > share:
                fails.append(f"standing {k} of {n} is the top {k/n:.0%}; '{tier}' requires the top {int(share*100)} percent (paragraph 4.d). The tier the numbers support is lower")
            if n < 4:
                warns.append(f"only {n} Marines of the grade known; the top quarter of {n} is a thin claim, say so in the comments")

    com = section(text, "Comments")
    if com is None or words(com) < 12:
        if tier in ("Recommended with Reservation", "Not Recommended"):
            fails.append(f"'{tier}': Comments Mandatory on the form, and paragraph 4.c requires amplifying information; the reason as dated facts")
        else:
            fails.append("## Comments missing or under 12 words; the form asks for brief comments justifying the recommendation")
    else:
        if tier in ("Recommended with Reservation", "Not Recommended") and not re.search(DATE, com):
            fails.append(f"'{tier}': the reason must be stated as dated facts (paragraph 4.c, 4.d); no date in the comments")
        if not re.search(r"\d", com):
            warns.append("no number in the comments; conduct, performance, and potential without a count is a characterization")
        for h in ("conduct", "performance", "potential"):
            if not re.search(h, com, re.I):
                warns.append(f"the order's head '{h}' (paragraph 4.b) is not addressed by name")
        if words(com) > 150:
            warns.append(f"comments run {words(com)} words; the form's field is small and the instruction says brief")
        for w in strike_hits(com) + [w for w in EXTRA_STRIKE if w in com.lower()]:
            warns.append(f"strike list: '{w}'")
        if re.search(PROMISE, com, re.I):
            fails.append(f"a promise about the decision ('{re.search(PROMISE, com, re.I).group(0)}'); CMC (MMEA-6) decides (paragraph 3.a)")
        scrubbed = re.sub(r"\bNJPs?\b|non-?judicial punishments?|court[- ]martial", "", com, flags=re.I)
        for b in blocked_hits(scrubbed):
            fails.append(f"blocked content in the comments: {b}; the prerequisites screen records yes or no, the comments carry no detail")

    if tier in ("Recommended with Reservation", "Not Recommended") and block == "g" and signer:
        delegated = re.search(r"by direction|executive officer|acting for|for the commanding officer|on behalf", signer)
        if delegated or not re.search(r"commanding officer|\bco\b|commander", signer):
            fails.append(f"'{tier}' at block 35g signed by '{signed.group(1).strip()}'; paragraph 4.c: this authority may not be delegated")
    if tier == "Not Recommended":
        iv = section(text, "Interview")
        if not iv or not re.search(DATE, iv) or not re.search(r"commanding officer", iv, re.I):
            fails.append("Not Recommended without a dated commanding officer's interview in ## Interview (chapter 3 paragraph 2.b: the CO must conduct it)")
        if not re.search(r"\bRE-\d[A-Z]\b", text):
            warns.append("no RE code recorded; paragraph 4.d: the CO indicates the reason ensuring assignment of the appropriate code, and the CO, not a delegate, assigns anything other than RE-1A")
        if not re.search(r"MMEA-6", text):
            warns.append("say that the request still goes to CMC (MMEA-6), which decides (paragraph 3.a)")

    if block == "g":
        cert = re.search(r"Does SNM meet all reenlistment prerequisites:\s*(Yes|No)\b", text)
        if not cert:
            fails.append("block 35g without the certification line 'Does SNM meet all reenlistment prerequisites: Yes/No' (paragraph 7; the form)")
        elif cert.group(1) == "No" and not re.search(r"waiv|prerequisite \(\d+\)", text, re.I):
            fails.append("certification is No but no prerequisite is named and no waiver stated; paragraph 7 requires the explanation in the CO's comments")
    pre = section(text, "Prerequisites")
    if pre and re.search(r"\bNo\b", pre) and re.search(r"waiver", pre, re.I) and not re.search(r"Commanding General|CG", pre):
        warns.append("a waiver needs the Commanding General's own endorsement, not by direction (paragraph 8); note it")

    ecc = re.search(r"ECC:\s*(" + DATE + r"|\d{4}-\d{2}-\d{2})", head)
    eas = re.search(r"EAS:\s*(" + DATE + r"|\d{4}-\d{2}-\d{2})", head)
    win = section(text, "Windows")
    if win and ecc:
        try:
            e = parse(ecc.group(1)); s = parse(eas.group(1)) if eas else e
            for name, w in windows(e, s):
                if w not in win:
                    fails.append(f"windows do not match the dates in the header: expected '{name}: {w}' (chapter 3 paragraph 2.b)")
        except SystemExit as ex:
            warns.append(str(ex))
    elif not win:
        warns.append("no ## Windows section; scripts/reenlistment_windows.py computes them from ECC and EAS")

    mm = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]{2,}\b", re.sub(r"<MARINE>", "", text))
    if mm and not re.search(r"^(?:Sergeant Major|First Sergeant|Company Commander|Executive Officer|Commanding Officer|Staff Sergeant|Gunnery Sergeant|Master Sergeant|Lance Corporal|Corporal|Sergeant) (?:Major|Sergeant|Commander|Officer|Corporal)$", mm.group(0)):
        fails.append(f"a name appears ('{mm.group(0)}'); <MARINE> until substitution on the user's computer")
    for p in LIFTED:
        if p.lower() in text.lower():
            fails.append(f"lifted from the exemplar or voice file: '{p}'; the example teaches shape, the intake supplies facts")
    for b in blocked_hits(head + "\n" + (win or "")):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")

    print(f"REENLISTMENT CHECK: {sys.argv[1]}  {tier or 'no tier'}  block 35{block or '?'}")
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
