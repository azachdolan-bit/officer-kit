#!/usr/bin/env python3
"""Check a staff paper (memo.md) against MCTP 3-30A chapter 3 and appendices A to E: memorandum for the record,
point paper, position/decision paper, talking paper, information paper. Each kind has the parts its appendix
prints, in its words; the checker fails a missing part, a recommendation the reader cannot sign, a paper over
the length the publication sets, a reference listed and not used, names, dashes, blocked content, and lifted
exemplar phrases.

Usage:  python3 memo_check.py memo.md
Exit 0 = passes (warnings allowed); 1 = a failure.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes, words  # noqa: E402

KINDS = {
    "mfr": {"caption": "MEMORANDUM FOR THE RECORD", "parts": ["Subj", "Paragraphs"], "max_words": None, "signer": True},
    "point paper": {"caption": "POINT PAPER", "parts": ["To", "Subj", "BACKGROUND", "DISCUSSION", "RECOMMENDATION", "Prepared by", "Approved by"], "max_words": 450, "signer": False},
    "position/decision paper": {"caption": "POSITION/DECISION PAPER", "parts": ["Subj", "Purpose", "Major Points", "Discussion", "Recommendation", "Prepared by", "Approved by"], "max_words": 900, "signer": False},
    "talking paper": {"caption": "TALKING PAPER", "parts": ["FOR USE BY", "SUBJECT", "BACKGROUND", "DISCUSSION", "RECOMMENDATION", "APPROVAL", "ACTION OFFICER"], "max_words": None, "signer": False},
    "information paper": {"caption": "INFORMATION PAPER", "parts": ["Subject", "Purpose", "Key Points", "Prepared by"], "max_words": 900, "signer": False},
}
ALIASES = {"memorandum for the record": "mfr", "decision paper": "position/decision paper", "position paper": "position/decision paper", "info paper": "information paper"}
GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|Colonel|Gunny|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj|LtCol|Col)"
DATE = r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b"
BILLET = r"\b(?:officer|sergeant|commander|chief|gunner|S-[1-6]|G-[1-6]|XO|CO|OIC|NCOIC|SNCOIC|representative|adjutant|corpsman|leader)\b"
SPECULATE = r"\b(?:I think|I feel|probably|it seems|seems like|in my opinion|we should probably)\b"
EXTRA_STRIKE = ["it should be noted that", "as you are aware", "in order to", "it is recommended that consideration be given", "various", "numerous", "leverage", "synergy", "robust", "going forward", "touch base"]
LIFTED = [
    "fix the firing order for the rifle range of 8 to 10 December 2026",
    "Company A fires 8 December, Companies B and C fire 9 December",
    "confirmed 26,400 rounds are on hand against a requirement of 24,200",
    "range control's request cutoff is 28 November 2026",
    "each company reports its unqualified count to the S-3 by 24 November 2026",
    "turn in schedule for the field exercise",
    "118 of 121 Marines available; 3 on light duty",
    "whether the company holds the quarterly inventory before or after the field exercise",
]


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*\n(.*?)(?=\n## |\Z)", text, re.S | re.M | re.I)
    return m.group(1).strip() if m else None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8").read()
    text = re.sub(r"[ \t]+", " ", raw)
    fails, warns = [], []
    head = text.split("\n## ", 1)[0]

    km = re.search(r"Kind:\s*([^\n]+?)(?=\s{2,}|\s+Code:|\s+Date:|\n|$)", head, re.I)
    kind = None
    if km:
        k = km.group(1).strip().lower()
        kind = ALIASES.get(k, k)
    if kind in ("memorandum", "memo", "from to memo"):
        fails.append("a memorandum with From and To lines is governed by SECNAV M-5216.5, which is not in the library; this tool builds the five staff papers MCTP 3-30A prints (MFR, point paper, position/decision paper, talking paper, information paper). Use the MFR to record what happened, or naval-letter to write to another office")
        spec = None
    elif kind not in KINDS:
        fails.append("Kind must be one of the publication's five papers: MFR, point paper, position/decision paper, talking paper, information paper (MCTP 3-30A chapter 3)")
        spec = None
    else:
        spec = KINDS[kind]
    if not re.search(r"Code:\s*\S", head):
        fails.append("no originator Code in the header; every appendix puts the code and date at the upper right")
    if not re.search(r"Date:\s*(" + DATE + r"|\d{4}-\d{2}-\d{2})", head):
        fails.append("no Date in the header (day month year)")

    if spec:
        for part in spec["parts"]:
            if section(text, part) is None:
                fails.append(f"missing part '## {part}' (MCTP 3-30A appendix for the {kind}: {spec['caption']})")
        subj = section(text, "Subj") or section(text, "SUBJECT") or section(text, "Subject")
        if subj is not None and subj.splitlines() and subj.splitlines()[0].strip() != subj.splitlines()[0].strip().upper():
            fails.append("the subject is not in capitals (every appendix prints it so)")
        if spec["signer"]:
            sg = re.search(r"Signer:\s*([^\n]+)", head)
            if not sg:
                fails.append("MFR without a Signer line (name, billet, grade and service, as Appendix D shows); the paper must be dated, signed, and show the organizational code")
            elif sg.group(1).count(",") < 2:
                fails.append("Signer line needs name, billet, and grade and service, separated by commas (Appendix D: I. M. RESPONSIBLE / OPS, AC/S G-2 / LtCol USMC)")
        else:
            if kind == "information paper" and (re.search(r"^## To\b", text, re.M) or re.search(r"Signer:", head)):
                fails.append("an information paper carries no address or signature block (chapter 3: 'They do not require an address or signature block')")
        body = "\n".join(s for s in (section(text, p) for p in spec["parts"]) if s)
        if spec["max_words"] and words(body) > spec["max_words"]:
            fails.append(f"{words(body)} words in the body; the publication holds a {kind} to {'one page' if kind == 'point paper' else 'two pages at most'}; move detail to a tab")
        rec = section(text, "RECOMMENDATION") or section(text, "Recommendation")
        if rec is not None and not re.search(r"\b(?:approve|disapprove|approval|disapproval|decision|sign|concur)\b", rec, re.I):
            fails.append("the recommendation is not one the reader can approve or disapprove ('Reduce recommendations to clear, concise statements that permit straightforward approval or disapproval')")
        if kind == "mfr":
            paras = section(text, "Paragraphs") or ""
            if not re.search(DATE, paras):
                fails.append("an MFR records when: no date in the paragraphs")
            if not re.search(BILLET, paras, re.I):
                warns.append("no participant by billet in the MFR; the record says who met or spoke")
            if re.search(SPECULATE, paras, re.I):
                fails.append(f"an MFR records, it does not argue: '{re.search(SPECULATE, paras, re.I).group(0)}'")
            if not re.search(r"action underway|action:|will |by \d{1,2} \w+ \d{4}", paras, re.I):
                warns.append("no action underway or due date recorded; the publication describes the MFR as 'a record of action underway and reasons for the action'")
        if kind == "position/decision paper":
            disc = section(text, "Discussion") or ""
            if not re.search(r"other (?:agencies|staff|service)|not applicable", disc, re.I):
                warns.append("positions of other agencies not addressed and 'Not Applicable' not stated (chapter 3)")
        if kind == "information paper" and re.search(r"\benclosure", body, re.I):
            warns.append("an information paper 'will not refer to enclosures except for additional tabs'")
        refs = section(text, "References")
        if refs:
            listed = re.findall(r"^\s*\(([a-z])\)", refs, re.M)
            for r in listed:
                if not re.search(r"reference \(" + r + r"\)", body, re.I):
                    fails.append(f"reference ({r}) is listed and not used in the discussion ('References that are used as a source are cited in the discussion')")
        for w in strike_hits(body) + [w for w in EXTRA_STRIKE if w in body.lower()]:
            warns.append(f"strike list: '{w}'")
        for b in blocked_hits(body):
            fails.append(f"blocked content: {b}")
        if re.search(r"\((?:U|C|S|TS)\)", body) and not re.search(r"Classification:\s*\S", head):
            warns.append("portion marks present with no Classification line in the header; an unclassified paper carries no markings")

    mm = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]{2,}\b", re.sub(r"<MARINE>", "", text))
    if mm and not re.search(r"^(?:Sergeant Major|First Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|Lance Corporal|Lieutenant Colonel) (?:Major|Sergeant|Corporal|Colonel)$", mm.group(0)):
        fails.append(f"a name appears ('{mm.group(0)}'); <MARINE> or the billet until substitution on the user's computer")
    for p in LIFTED:
        if p.lower() in text.lower():
            fails.append(f"lifted from the exemplar or voice file: '{p}'; the example teaches shape, the intake supplies facts")
    if dashes(text):
        fails.append("em or en dash present")

    print(f"MEMO CHECK: {sys.argv[1]}  {kind or 'no kind'}  {words(text)} words")
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
