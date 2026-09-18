#!/usr/bin/env python3
"""Check a staff paper or memorandum (memo.md) against its governing publication.

MCTP 3-30A chapter 3 and appendices A to E govern the five staff papers: memorandum for the record,
point paper, position/decision paper, talking paper, information paper. SECNAV M-5216.5 chapter 10
governs the memorandum formats: memorandum for the record, From-To (printed form), plain paper,
letterhead, the decision block, and the memorandum of agreement or understanding. SECNAV M-5216.5
chapter 11 governs the business letter. Each kind has the parts its publication prints, in its words;
the checker fails a missing part, a recommendation the reader cannot sign, a paper over the length the
publication sets, a reference listed and not used, a business letter that carries a naval letter's
habits, an agreement whose senior signs on the wrong side or first, names, dashes, blocked content,
and lifted exemplar phrases.

The memorandum for the record is the one kind both publications carry and they agree; see
references/standard.md, "The memorandum for the record: MCTP 3-30A Appendix D against SECNAV
M-5216.5 chapter 10".

Usage:  python3 memo_check.py memo.md
Exit 0 = passes (warnings allowed); 1 = a failure.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes, words  # noqa: E402

# need_code / need_date: the identification symbols that kind's publication requires in the header.
# SECNAV M-5216.5 10-2.2 and 10-2.3: "The only identification symbol you need is the date, unless
# local practice calls for more." 11-2.1: a business letter carries SSIC, originator's code, and date.
KINDS = {
    "mfr": {"source": "MCTP 3-30A appendix D and SECNAV M-5216.5 10-2.1", "caption": "MEMORANDUM FOR THE RECORD", "parts": ["Subj", "Paragraphs"], "max_words": None, "signer": True, "need_code": True, "need_date": True},
    "point paper": {"source": "MCTP 3-30A appendix B", "caption": "POINT PAPER", "parts": ["To", "Subj", "BACKGROUND", "DISCUSSION", "RECOMMENDATION", "Prepared by", "Approved by"], "max_words": 450, "signer": False, "need_code": True, "need_date": True},
    "position/decision paper": {"source": "MCTP 3-30A appendix A", "caption": "POSITION/DECISION PAPER", "parts": ["Subj", "Purpose", "Major Points", "Discussion", "Recommendation", "Prepared by", "Approved by"], "max_words": 900, "signer": False, "need_code": True, "need_date": True},
    "talking paper": {"source": "MCTP 3-30A appendix C", "caption": "TALKING PAPER", "parts": ["FOR USE BY", "SUBJECT", "BACKGROUND", "DISCUSSION", "RECOMMENDATION", "APPROVAL", "ACTION OFFICER"], "max_words": None, "signer": False, "need_code": True, "need_date": True},
    "information paper": {"source": "MCTP 3-30A appendix E", "caption": "INFORMATION PAPER", "parts": ["Subject", "Purpose", "Key Points", "Prepared by"], "max_words": 900, "signer": False, "need_code": True, "need_date": True},
    "from-to memorandum": {"source": "SECNAV M-5216.5 10-2.2 and figure 10-2", "caption": "Memorandum (OPNAV printed form)", "parts": ["From", "To", "Subj", "Paragraphs"], "max_words": None, "signer": False, "need_code": False, "need_date": True},
    "plain-paper memorandum": {"source": "SECNAV M-5216.5 10-2.3 and figure 10-3", "caption": "MEMORANDUM", "parts": ["From", "To", "Subj", "Paragraphs"], "max_words": None, "signer": False, "need_code": False, "need_date": True},
    "letterhead memorandum": {"source": "SECNAV M-5216.5 10-2.4 and figure 10-4", "caption": "MEMORANDUM", "parts": ["From", "To", "Subj", "Paragraphs"], "max_words": None, "signer": False, "need_code": False, "need_date": True},
    "memorandum of agreement": {"source": "SECNAV M-5216.5 10-2.6 and figure 10-5", "caption": "MEMORANDUM OF AGREEMENT", "parts": ["Between", "Subj", "Signatures"], "max_words": None, "signer": False, "need_code": False, "need_date": False},
    "memorandum of understanding": {"source": "SECNAV M-5216.5 10-2.6 and figures 10-6 and 10-7", "caption": "MEMORANDUM OF UNDERSTANDING", "parts": ["Between", "Subj", "Signatures"], "max_words": None, "signer": False, "need_code": False, "need_date": False},
    "business letter": {"source": "SECNAV M-5216.5 chapter 11", "caption": "(no caption; letterhead only)", "parts": ["Inside Address", "Body", "Close", "Signature"], "max_words": None, "signer": False, "need_code": True, "need_date": True},
}
ALIASES = {
    "memorandum for the record": "mfr",
    "decision paper": "position/decision paper", "position paper": "position/decision paper",
    "info paper": "information paper",
    "from to memorandum": "from-to memorandum", "from-to memo": "from-to memorandum",
    "from to memo": "from-to memorandum", "printed memorandum": "from-to memorandum",
    "memorandum form": "from-to memorandum", "opnav memorandum": "from-to memorandum",
    "plain paper memorandum": "plain-paper memorandum", "plain-paper memo": "plain-paper memorandum",
    "plain paper memo": "plain-paper memorandum",
    "letterhead memo": "letterhead memorandum",
    "moa": "memorandum of agreement", "memorandum of agreement or understanding": "memorandum of agreement",
    "mou": "memorandum of understanding",
    "business letter to a company": "business letter", "civilian business letter": "business letter",
}
MEMO_KINDS = ("from-to memorandum", "plain-paper memorandum", "letterhead memorandum")
MOA_KINDS = ("memorandum of agreement", "memorandum of understanding")
# SECNAV M-5216.5 10-2.6.b(1) to (5): "The basic text may contain, but is not limited to, the
# following titled paragraphs". A missing one is a question to the writer, not an error.
MOA_PARAS = ["Purpose", "Problem", "Scope", ("Agreement", "Understanding"), "Effective Date"]
GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|Colonel|Gunny|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj|LtCol|Col)"
ABBREV_GRADES = r"\b(?:PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|MGySgt|1stSgt|SgtMaj|2ndLt|1stLt|Capt|Maj|LtCol|Col|BGen|MajGen|LtGen|Gen|CWO[2-5]|WO)\b"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DATE = r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b"
ABBREV_DATE = r"\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2}\b"
CIVIL_DATE = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b"
ANY_DATE = "(?:" + DATE + "|" + ABBREV_DATE + "|" + CIVIL_DATE + r"|\d{4}-\d{2}-\d{2})"
BILLET = r"\b(?:officer|sergeant|commander|chief|gunner|S-[1-6]|G-[1-6]|XO|CO|OIC|NCOIC|SNCOIC|representative|adjutant|corpsman|leader)\b"
SPECULATE = r"\b(?:I think|I feel|probably|it seems|seems like|in my opinion|we should probably)\b"
# SECNAV M-5216.5 10-2.4: a letterhead memorandum goes outside the activity only on "routine matters
# that neither make a commitment nor take an official stand".
COMMITMENT = r"\b(?:commits?|commitment|committed|obligat\w+|agrees to|guarantee\w*|this command's position|the official position|binding)\b"
COLLECTIVE = r"(?:Ladies and Gentlemen|Gentlemen|Ladies|Mesdames|Dear Sirs|Dear Sir or Madam)"
NAVAL_CLOSE = r"(?:Very respectfully|Respectfully(?: yours)?|Sincerely yours|Best regards|Regards|V/r|Semper Fidelis)"
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
    "Leave requests reach the S-1 five working days before the first day of leave",
    "the consolidated leave roster to the executive officer every Thursday",
    "the loan of two 20 by 40 foot general purpose tents",
]


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*\n(.*?)(?=\n## |\Z)", text, re.S | re.M | re.I)
    return m.group(1).strip() if m else None


def any_section(text, names):
    for n in (names if isinstance(names, (tuple, list)) else [names]):
        s = section(text, n)
        if s is not None:
            return s
    return None


def part_label(names):
    return names if isinstance(names, str) else " or ".join(names)


def parse_date(s):
    """Return a sortable tuple for a date in any of the manual's three formats, or None."""
    m = re.search(DATE, s)
    if m:
        d, mo, y = m.group(0).split()
        return (int(y), MONTHS.index(mo) + 1, int(d))
    m = re.search(CIVIL_DATE, s)
    if m:
        mo, rest = m.group(0).split(" ", 1)
        d, y = rest.split(", ")
        return (int(y), MONTHS.index(mo) + 1, int(d))
    m = re.search(ABBREV_DATE, s)
    if m:
        d, mo, y = m.group(0).split()
        return (2000 + int(y), [x[:3] for x in MONTHS].index(mo) + 1, int(d))
    m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", s)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def addressee_count(to_text):
    if to_text is None:
        return 0
    lines = [l.strip(" -*") for l in to_text.splitlines() if l.strip()]
    n = 0
    for l in lines:
        n += len([x for x in l.split(";") if x.strip()]) if ";" in l else 1
    return n


def check_memorandum(kind, text, head, fails, warns):
    """SECNAV M-5216.5 chapter 10, paragraphs 2, 3, 4, and 5."""
    to = section(text, "To")
    if kind == "from-to memorandum":
        form = re.search(r"Form:\s*([^\n]+)", head, re.I)
        if not form:
            warns.append("no Form line; 10-2.2 names OPNAV 5215/144A and 5215/144B and figure 10-2 names OPNAV 5216/144A and 5216/144B for the same two sizes, so record the number the activity actually stocks")
        elif not re.search(r"\b521[56]/144[AB]\b", form.group(1)):
            warns.append(f"Form '{form.group(1).strip()}' is not one of the printed forms the manual names (10-2.2: OPNAV 5215/144A or 5215/144B; figure 10-2: OPNAV 5216/144A or 5216/144B)")
        sg = re.search(r"Signer:\s*([^\n]+)", head)
        if sg and (re.search(ABBREV_GRADES, sg.group(1)) or "," in sg.group(1)):
            fails.append("the Signer line carries organizational titles; figure 10-2, paragraph 6: 'The writer signs his or her name without the organizational titles.' Put the name alone")
    if kind == "plain-paper memorandum":
        if addressee_count(to) < 2 and section(text, "Via") is None:
            warns.append("one addressee and no Via; 10-2.3 makes the plain-paper memorandum the flexible choice 'when there are multiple addressees, via addressees, or both', and the printed form or the letterhead memorandum covers a single addressee")
    if kind == "letterhead memorandum":
        outside = re.search(r"Outside(?: the activity)?:\s*(yes|y|true)\b", head, re.I)
        if outside:
            if not re.search(r"Direct liaison authorized:\s*(yes|y|true)\b", head, re.I):
                fails.append("a letterhead memorandum outside the activity with no 'Direct liaison authorized: yes' in the header; 10-2.4: 'When direct liaison with individuals outside of your activity is authorized, the letterhead memorandum may be used to correspond on routine matters that neither make a commitment nor take an official stand.'")
            paras = section(text, "Paragraphs") or ""
            m = re.search(COMMITMENT, paras, re.I)
            if m:
                warns.append(f"'{m.group(0)}' reads as a commitment or an official stand in a letterhead memorandum going outside the activity (10-2.4); that matter goes in a naval letter")
    dec = any_section(text, ("Decision", "Decision block"))
    if dec is not None:
        for label in ("Approved", "Disapproved", "Other"):
            if not re.search(r"\b" + label + r"\b", dec, re.I):
                fails.append(f"the decision block has no '{label}' line; 10-2.5 prints three, in the order Approved, Disapproved, Other, each preceded by an overscored line")
        if not re.search(r"DECISION:", dec):
            warns.append("no heading line ending 'DECISION:' in the decision block; 10-2.5 shows 'COMMANDING OFFICER DECISION:' at the left margin, two lines below the signature line")
        if addressee_count(to) > 1:
            fails.append(f"a decision block with {addressee_count(to)} addressees; 10-2.5 puts one on a memorandum 'When only requesting an approval/disapproval decision from a single addressee'")


def check_moa(kind, text, fails, warns):
    """SECNAV M-5216.5 10-2.6."""
    between = section(text, "Between") or ""
    parties = [l.strip() for l in between.splitlines() if l.strip() and l.strip().upper() != "AND"]
    if len(parties) < 2:
        fails.append("the Between block names fewer than two activities; 10-2.6.b centres 'BETWEEN' and follows it with 'the names of the agreeing activities (centered)'")
    for names in MOA_PARAS:
        if any_section(text, names) is None:
            warns.append(f"no '## {part_label(names)}' paragraph; 10-2.6.b lists it among the titled paragraphs the basic text 'may contain, but is not limited to', so name it or say why it is not needed")
    eff = any_section(text, ("Effective Date",))
    if eff is not None and not re.search(ANY_DATE, eff):
        fails.append("the Effective Date paragraph carries no date; 10-2.6.b(5): 'Enter the date the agreement will take effect.'")
    sigs = section(text, "Signatures") or ""
    rows = {}
    for line in sigs.splitlines():
        m = re.match(r"\s*(Left|Right|Middle)\b([^:]*):\s*(.+)", line.strip(), re.I)
        if m:
            rows[m.group(1).lower()] = (m.group(2) + " " + m.group(3))
    if "right" not in rows:
        fails.append("no 'Right:' signature line; 10-2.6.d: 'Arrange signature lines so the senior official is at the right.' Label each signature line Left, Middle, or Right and mark which activity is the senior")
    for side in ("left", "middle"):
        if side in rows and re.search(r"\bsenior\b", rows[side], re.I):
            fails.append(f"the senior is marked on the {side}; 10-2.6.d: 'Arrange signature lines so the senior official is at the right.'")
    if "right" in rows and not re.search(r"\bsenior\b", rows["right"], re.I):
        warns.append("the Right signature line is not marked as the senior activity; 10-2.6.d puts the senior official at the right, so say which one it is")
    if len(parties) > 2 and "middle" not in rows:
        warns.append(f"{len(parties)} activities and no 'Middle:' signature line; 10-2.6.d: 'Place the signature line of a third cosigner in the middle of the page.'")
    senior_on_left = any(re.search(r"\bsenior\b", rows.get(s, ""), re.I) for s in ("left", "middle"))
    if "left" in rows and "right" in rows and not senior_on_left:
        dl, dr = parse_date(rows["left"]), parse_date(rows["right"])
        if dl and dr and dr < dl:
            fails.append("the senior activity on the right signed before the junior on the left; 10-2.6.d: 'The senior activity should sign the agreement after the junior activity(ies).'")
        elif not (dl and dr):
            warns.append("a signature line without a date; the order of signing is a rule here (10-2.6.d) and the dates are how it is checked")
    if sigs and "___" not in sigs:
        warns.append("no overscoring above the signature lines; 10-2.6.d: 'Precede all signature lines by over scoring as shown in figures 10-5 and 10-6.'")
    if not re.search(r"copies", (sigs + " " + (any_section(text, ("Copies",)) or "")), re.I):
        warns.append("nothing records who sends the copies; 10-2.6.e: 'The activity signing last should send copies of the agreement to all cosigners.'")


def check_business_letter(text, head, fails, warns):
    """SECNAV M-5216.5 chapter 11. The four habits of a naval letter that do not belong here."""
    dm = re.search(r"Date:\s*([^\n]+)", head)
    if dm and not re.search(CIVIL_DATE, dm.group(1)):
        fails.append(f"the date '{dm.group(1).strip()}' is not the civilian format; 11-2.1.c: 'Write the date in month-day-year order. The month is written out in full, followed by the day in Arabic numerals, a comma, and the full year also in Arabic numerals, e.g., May 23, 2014.'")
    if not re.search(r"SSIC:\s*\S", head):
        warns.append("no SSIC in the header; 11-2.1 puts three identification symbols together, the SSIC, the originator's code, and the date")
    body = section(text, "Body") or ""
    for name in ("Ref", "References", "Encl", "Enclosure block"):
        if section(text, name) is not None:
            fails.append(f"a '## {name}' block on a business letter; 11-2.7: 'Refer to previous communications and enclosures in the body of the letter only, without calling them references or enclosures.' Enclosures are listed after the signature under 11-2.10")
    m = re.search(r"\b(?:reference|enclosure)s?\s*\(", body, re.I)
    if m:
        fails.append(f"the body calls something a reference or an enclosure ('{m.group(0).strip()}'); 11-2.7 refers to them 'in the body of the letter only, without calling them references or enclosures'")
    sal = section(text, "Salutation")
    subj = section(text, "Subject")
    if sal is None and subj is None:
        fails.append("neither a Salutation nor a Subject line; 11-2.5: 'Use of a subject line is optional and may replace the salutation.' One of the two starts the letter")
    if sal is not None and not sal.strip().endswith(":"):
        fails.append("the salutation does not end in a colon; 11-2.4 sets the courtesy title and surname 'followed by a colon'")
    att = section(text, "Attention")
    if att is not None and sal is not None and not re.search(COLLECTIVE, sal, re.I):
        warns.append("an attention line with a salutation to an individual; figure 11-5: 'The salutation must agree with the first line of the address. If the first line is a business, division, or organization collectively, a collective salutation such as \"Ladies and Gentlemen\" is used even if the attention line directs the letter to an individual.'")
    close = (section(text, "Close") or "").strip()
    if close and close != "Sincerely,":
        fails.append(f"the complimentary close is '{close}'; 11-2.8 gives one and only one: 'Use \"Sincerely\" followed by a comma for the complimentary close of a business letter starting at the center of the page on the second line below the text.'")
    m = re.search(NAVAL_CLOSE, text)
    if m and m.group(0) not in ("Sincerely,",):
        fails.append(f"'{m.group(0)}' is not the close of a business letter; 11-2.8 sets 'Sincerely,' and the naval and personal letter closes do not carry over")
    addr = section(text, "Inside Address") or ""
    if not re.search(r"\b[A-Z]{2}\s\d{5}(?:-\d{4})?\b", addr):
        fails.append("the inside address has no 'city, state, and ZIP+4 code on the last line' (11-2.2)")
    if re.search(r"\b[A-Z]{2}\s{2,}\d{5}", addr):
        fails.append("two or more spaces between the state and the ZIP code; 11-2.2 notes the 'new requirement for only one space between state and ZIP code vice two to five spaces'")
    if re.search(r"^\s*\d+\.\s", body, re.M):
        fails.append("a numbered main paragraph in the body; 11-2.6: 'Do not number main paragraphs.' Subparagraphs are lettered and numbered in standard letter fashion")
    sig = section(text, "Signature") or ""
    siglines = [l.strip() for l in sig.splitlines() if l.strip()]
    if siglines:
        name = re.sub(r"<[^>]*>", "", siglines[0])
        if re.search(r"[a-z]", name) and not re.search(r"(?:Mc|Mac|De|Di|Du|La|Le|Van|O')[A-Z]", name):
            fails.append(f"the signer's name is not in all capitals ('{siglines[0]}'); 11-2.9.a(1): 'Signer's name in all capital letters, with the exception of a last name starting with a prefix'")
    m = re.search(ABBREV_GRADES, sig)
    if m:
        fails.append(f"the grade '{m.group(0)}' is abbreviated in the signature line; 11-2.9.a(2): 'Military grade (if any) spelled out'")
    if re.search(r"\bUSMC\b", sig):
        warns.append("'USMC' in the signature line; 11-2.9 does not rule on the service, and figures 11-4 and 11-5 spell it out ('Commander, U.S. Navy'), so spell it out unless the command says otherwise")
    encl = any_section(text, ("Enclosures", "Enclosure"))
    if encl is not None and not (re.search(r"^\s*\d+\.", encl, re.M) or re.search(r"Enclosures?\s*\(\d+\)", encl)):
        warns.append("the enclosure line neither numbers and describes the enclosures nor gives a count in parentheses; 11-2.10.a and 11-2.10.b set the two forms")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8").read()
    text = re.sub(r"[ \t]+", " ", raw)
    fails, warns = [], []
    head = text.split("\n## ", 1)[0]

    km = re.search(r"Kind:\s*([^\n]+?)(?=\s{2,}|\s+Code:|\s+Date:|\s+SSIC:|\s+Form:|\n|$)", head, re.I)
    kind = None
    if km:
        k = km.group(1).strip().lower()
        kind = ALIASES.get(k, k)
    if kind in ("memorandum", "memo", "memorandum (from and to)"):
        fails.append("Kind 'memorandum' does not say which. SECNAV M-5216.5 chapter 10 prints several and they are not interchangeable: 'from-to memorandum' on the OPNAV printed form (10-2.2), 'plain-paper memorandum' for multiple or via addressees (10-2.3), 'letterhead memorandum' for more formality or authorized direct liaison outside the activity (10-2.4), 'MFR' to record what is not recorded elsewhere (10-2.1), or 'memorandum of agreement' or 'memorandum of understanding' (10-2.6). Name one")
        spec = None
    elif kind not in KINDS:
        fails.append("Kind must be one of the five staff papers MCTP 3-30A prints (MFR, point paper, position/decision paper, talking paper, information paper) or one of the formats SECNAV M-5216.5 prints (from-to memorandum, plain-paper memorandum, letterhead memorandum, memorandum of agreement, memorandum of understanding, business letter)")
        spec = None
    else:
        spec = KINDS[kind]
    if spec and spec["need_code"] and not re.search(r"Code:\s*\S", head):
        fails.append("no originator Code in the header; every appendix puts the code and date at the upper right" if kind in ("mfr", "point paper", "position/decision paper", "talking paper", "information paper") else "no originator Code in the header; 11-2.1 blocks the SSIC, the originator's code, and the date together")
    if spec and spec["need_date"] and not re.search(r"Date:\s*(" + ANY_DATE + r")", head):
        fails.append("no Date in the header (day month year)" if kind != "business letter" else "no Date in the header; 11-2.1.c sets month-day-year, e.g. May 23, 2014")
    if spec and not spec["need_code"] and not re.search(r"Date:\s*(" + ANY_DATE + r")", head) and kind in MEMO_KINDS:
        fails.append("no Date in the header; for these memorandums the date is the one identification symbol the manual requires (10-2.2 and 10-2.3.a: 'The only identification symbol you need is the date, unless local practice calls for more.')")

    if spec:
        for names in spec["parts"]:
            if any_section(text, names) is None:
                fails.append(f"missing part '## {part_label(names)}' ({spec['source']} for the {kind}: {spec['caption']})")
        subj = section(text, "Subj") or section(text, "SUBJECT") or section(text, "Subject")
        if subj is not None and subj.splitlines() and subj.splitlines()[0].strip() != subj.splitlines()[0].strip().upper():
            fails.append("the subject is not in capitals (every appendix prints it so)" if kind != "business letter" else "the subject line is not in capitals; 11-2.5: 'Capitalize every letter in the subject line.'")
        if kind == "business letter" and subj is not None and len(subj.splitlines()[0].strip()) > 80:
            warns.append("the subject line runs past one line; 11-2.5: 'very brief, to the point, and not be more than one line in length, if possible'")
        if spec["signer"]:
            sg = re.search(r"Signer:\s*([^\n]+)", head)
            if not sg:
                fails.append("MFR without a Signer line (name, billet, grade and service, as Appendix D shows); the paper must be dated, signed, and show the organizational code")
            elif sg.group(1).count(",") < 2:
                fails.append("Signer line needs name, billet, and grade and service, separated by commas (Appendix D: I. M. RESPONSIBLE / OPS, AC/S G-2 / LtCol USMC)")
        else:
            if kind == "information paper" and (re.search(r"^## To\b", text, re.M) or re.search(r"Signer:", head)):
                fails.append("an information paper carries no address or signature block (chapter 3: 'They do not require an address or signature block')")
        body = "\n".join(s for s in (any_section(text, p) for p in spec["parts"]) if s)
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
        if kind in MEMO_KINDS:
            check_memorandum(kind, text, head, fails, warns)
        if kind in MOA_KINDS:
            check_moa(kind, text, fails, warns)
        if kind == "business letter":
            check_business_letter(text, head, fails, warns)
        refs = section(text, "References")
        if refs and kind != "business letter":
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
