#!/usr/bin/env python3
"""Check MROW input (mrow.md) against MCO 1610.7B enclosure (2): chapter 1 paragraphs 6 and 7, chapter 2
paragraph 3.c, chapter 4 paragraphs 5 (section B), 6 (section C), 13.d (unacceptable comments), and the kit's
blocked content, names, dashes, and lifted phrases.

Usage:  python3 mrow_input_check.py mrow.md
Exit 0 = passes (warnings allowed); 1 = a structural failure (title, MRO label, period dates, RS billet, a
missing or unbulleted section), a section C exclusion (award or commendatory material, adverse or disciplinary
material, personal quality or potential language, selection board or court-martial membership), a style
violation the order forbids (superlative, quotation marks, bold or italic, exclamation), a claim about the marks
or promotion, blocked content, a name, a lifted phrase, or an em or en dash.

The order fixes no character or line limit for the MROW or for sections B and C ("the space provided",
5.c(1) and 6.c(1)); the checker prints counts and imposes no cap.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes, words  # noqa: E402

DATE = r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b"
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|Colonel|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj|LtCol|Col)"

# Copied from fitrep/scripts/fitrep_check.py (SUPERLATIVES, UNACCEPTABLE, C_FORBIDDEN, and the style() rules),
# then split so that what chapter 4 paragraph 6 forbids in section C fails rather than warns.
SUPERLATIVES = r"\b(best|greatest|finest|most outstanding|unparalleled|unmatched|phenomenal|incredible|superb|flawless|perfect|unbelievable|top \d+%|number one|#1)\b"
UNACCEPTABLE = [
    (r"\b(NJP|non-?judicial punishment|court-?martial|civil action|criminal action|fact-?finding|investigation)\b", "13.d(1) pending NJP, courts martial, civil or criminal action, boards, investigations"),
    (r"\b(suspected|suspicion of)\b.*\b(drug|criminal)\b", "13.d(2) suspected criminal activity"),
    (r"\b(administrative reduction|administrative separation|adsep|withholding of promotion)\b", "13.d(3) administrative reduction or separation proceedings"),
    (r"\b(letter of (admonition|caution|reprimand)|non-?punitive letter|NPLOC)\b", "13.d(4) non punitive letters"),
    (r"\b(alcohol treatment|rehab(ilitation)?|SARP)\b", "13.d(5) alcohol treatment"),
    (r"\b(speeding|traffic (ticket|citation|violation))\b", "13.d(6) minor traffic violations"),
    (r"\b(non-?selected|not selected|passed over)\b", "13.d(7) prior non selection"),
    (r"\b(spouse|wife|husband)\b", "13.d(8) the spouse"),
    (r"\b(pregnan\w+|postpartum|medical condition|injur(y|ed)|surgery|diagnos\w+)\b", "13.d(10) medical matters"),
    (r"\b(family problems|family situation|marital|divorce|personal problems)\b", "13.d(11) personal or family problems"),
    (r"\b(single parent|single mother|single father)\b", "13.d(12) single parent status"),
    (r"\b(civilian (employment|career|job)|private sector)\b", "13.d(13) civilian employment potential"),
]
# 6.c(1)(c): awards, other commendatory material, adverse material, disciplinary action
AWARDS = r"\b(?:awarded|award(?:s|ed)?|medal|NAM|Navy (?:and Marine Corps )?Achievement|Commendation Medal|Meritorious Service Medal|MSM|NAVCOM|letter of appreciation|certificate of commendation|meritorious mast|command coin|decoration|commend(?:ed|ation|atory)|impact award|end of tour award)\b"
DISCIPLINE = r"\b(?:page 11|6105|counseling entry|disciplin\w*|adverse (?:material|action|report|fitness report)|reduced in (?:rank|grade)|relieved (?:of|for)|misconduct|charged with|reprimand\w*)\b"
# 6.a(4): personal qualities or potential impact
QUALITIES = r"\b(?:potential|future(?! op)|dedicated|dedication|loyal(?:ty)?|enthusiastic|enthusiasm|motivated|motivation|hard[ -]?working|selfless|attitude|work ethic|demeanor|leader of marines|consistently|always|never fails|excels?|tireless|passionate|passion|charisma\w*|maturity|intangibles?)\b"
# 6.b Note: participation as a member of a selection board or court-martial
BOARD = r"\b(?:(?:member|membership|sat|served|participat\w+)\W+(?:\w+\W+){0,6}?(?:selection board|promotion board|court-?martial)|(?:selection board|promotion board|court-?martial) (?:member|duty|panel))\b"
# The RS marks sections D through H and writes section I (chapter 2 paragraph 3.c(3)); the MROW carries facts.
MARKS = r"\b(?:should be marked|mark(?:ed)? (?:me|the MRO|this report)|deserves? (?:a|an|to be|promotion)|(?:top|upper) (?:third|half|quarter|\d+ ?(?:%|percent))|relative value|(?:RS|reporting senior)'?s? profile|(?:my|his|her|their) peers|ahead of (?:contemporaries|peers)|recommend(?:ed)? for (?:accelerated |early )?promotion|promot(?:e|ed|ion) (?:early|now|ahead)|section [D-I] mark\w*|a[n]? ?[A-H] in (?:section|mission|leadership|character|intellect))\b"
FIRST_PERSON = r"\b(?:I|my|me|myself)\b"
# Phrases from references/exemplar.md and voice.md. A draft that carries one took its content from the example.
LIFTED = [
    "Trained the platoon through 12 of 12 scheduled collective T&R events",
    "Ran 4 company live fire ranges for 190 Marines",
    "from 6 in December 2025 to 0 in June 2026 and 0 in September 2026",
    "Wrote 44 weekly training schedules for the company",
    "the platoon completed 3 of 3 assigned attacks within the exercise controller's time standard",
    "Accountable for 52 serialized weapons and 14 items of communications equipment",
    "Qualified 41 of 43 Marines on the annual rifle range, against 36 of 43 the prior year",
    "Planned and executed 4 live fire ranges for 210 Marines",
    "adopted by 3 companies for the February 2026 field exercise",
]
ACRONYM_OK = {"MRO", "USMC", "PFT", "CFT", "MOS", "MCO", "NCO", "SNCO", "MAGTF", "MEU", "PME", "MCMAP", "TAD", "FMF", "OIC",
              "SNCOIC", "BCP", "HQMC", "MROW", "APES", "SOP", "NCOIC", "USN", "MEF", "MARDIV", "ATFP", "ORM", "T&R", "TEEP",
              "CBRN", "CMC", "MMRP", "NMCI", "PCS", "PCA", "FROM", "TO"}


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"[^\n]*\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else None


def parse_date(s):
    m = re.match(r"(\d{1,2}) (\w+) (\d{4})", s)
    return (int(m.group(3)), MONTHS.index(m.group(2).lower()) + 1, int(m.group(1)))


def style(name, body, fails, warns):
    for w in set(re.findall(r"\b[A-Z][A-Z&]{3,}\b", body)):
        if w not in ACRONYM_OK:
            warns.append(f"{name}: uppercase word '{w}'; no UPPERCASE for emphasis, and acronyms only where widely understood (5.c(3)(c), 5.c(4), 6.c(3)(c), 6.c(4))")
    if re.search(r"[\"“”]", body):
        fails.append(f"{name}: quotation marks are not permitted (5.c(3)(c), 6.c(3)(c))")
    if re.search(r"\*\*|__|(?<!\w)\*(?!\w)|(?<!\w)_\w[^_\n]*\w_(?!\w)", body):
        fails.append(f"{name}: bold, italic, or underline markers are not permitted (5.c(3)(c), 6.c(3)(c))")
    if "!" in body:
        fails.append(f"{name}: exclamation is not permitted (5.c(3)(c), 6.c(3)(c))")
    for m in re.finditer(SUPERLATIVES, body, re.I):
        fails.append(f"{name}: superlative '{m.group(0)}' (omit superlative adjectives, 5.c(3)(a), 6.c(3)(a))")
    for w in strike_hits(body):
        warns.append(f"{name}: strike list '{w}' (imprecise phrasing, 5.c(3)(a), 6.c(3)(a))")
    if re.search(FIRST_PERSON, body):
        warns.append(f"{name}: first person; the input reads as the RS's section would")


def bullets(name, body, fails):
    lines = [l for l in body.splitlines() if l.strip()]
    bad = [l for l in lines if not re.match(r"^\s*[-•o*]\s", l)]
    if bad:
        fails.append(f"{name}: {len(bad)} line(s) not in bulleted text format with a distinctive mark (5.c(1), 6.c(1)): '{bad[0][:50]}'")
    elif not lines:
        fails.append(f"{name}: empty")
    return [l for l in lines if l not in bad]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8").read()
    text = re.sub(r"[ \t]+", " ", raw)
    fails, warns = [], []
    head = text.split("\n## ", 1)[0]

    if not re.search(r"^# MROW input", text, re.M):
        fails.append("title line '# MROW input' missing")
    if "<MARINE>" not in head and not re.search(r"\bthe MRO\b", head):
        fails.append("the MRO line carries neither <MARINE> nor 'the MRO'; the label stays until substitution on the user's computer")
    if not re.search(r"\bMRO:", head):
        fails.append("no 'MRO:' line in the header (label, grade, billet)")
    elif not re.search(r"MRO:[^\n]*" + GRADES, head):
        warns.append("no grade on the MRO line")
    fr = re.search(r"From (" + DATE + r")", head)
    to = re.search(r"To (" + DATE + r")", head)
    if not fr or not to:
        fails.append("the period must read 'From <day month year> To <day month year>' in the header (the report's section A item 3; chapter 1 paragraph 7.a ties the MROW to the end of the period)")
    elif parse_date(fr.group(1)) >= parse_date(to.group(1)):
        fails.append(f"period From {fr.group(1)} is not before To {to.group(1)}")
    if not re.search(r"\bRS:\s*\S", head):
        fails.append("no 'RS:' billet in the header; the RS is the reader (chapter 2 paragraph 3.c(3))")
    if not re.search(r"\bRO:\s*\S", head):
        warns.append("no 'RO:' billet in the header")
    if not re.search(r"Occasion:\s*[A-Z]{2}\b", head):
        warns.append("no 'Occasion: <code>' in the header (AN, CH, TD, and so on)")

    b = section(text, "Billet description")
    c = section(text, "Billet accomplishments")
    rs = section(text, "For the RS")
    counts = {}
    if b is None:
        fails.append("no '## Billet description' section (chapter 1 paragraph 6.b: the MROW carries the billet description)")
    else:
        counts["Billet description"] = (len(b), words(b))
        style("Billet description", b, fails, warns)
        bl = bullets("Billet description", b, fails)
        if re.search(r"\bgoals?\b", b, re.I):
            warns.append("Billet description: 'goal'; the order says acceptable standards vice goals (5.b(3))")
        if re.search(r"\b(?:MOS|primary MOS|qualified as an?)\b", b):
            warns.append("Billet description: mentions the MOS; the description should not restate the prerequisites of the Marine's MOS (5.a)")
        if re.search(AWARDS, b, re.I):
            fails.append(f"Billet description: award or commendatory material ('{re.search(AWARDS, b, re.I).group(0)}'); duties only")

    if c is None:
        fails.append("no '## Billet accomplishments' section (chapter 1 paragraph 6.b, chapter 4 paragraph 6.b: the MROW carries the summary of accomplishments)")
    else:
        counts["Billet accomplishments"] = (len(c), words(c))
        style("Billet accomplishments", c, fails, warns)
        cl = bullets("Billet accomplishments", c, fails)
        for l in cl:
            m = re.search(AWARDS, l, re.I)
            if m:
                fails.append(f"Billet accomplishments: '{m.group(0)}' is an award or commendatory material; 6.c(1)(c) keeps awards out of section C. List it under ## For the RS")
            m = re.search(DISCIPLINE, l, re.I)
            if m:
                fails.append(f"Billet accomplishments: '{m.group(0)}' is adverse material or disciplinary action (6.c(1)(c))")
            m = re.search(QUALITIES, l, re.I)
            if m:
                fails.append(f"Billet accomplishments: '{m.group(0)}' is a personal quality, potential, or imprecise phrasing; 6.a(4) and 6.c(3)(a): list only the results and achievements themselves")
        if re.search(BOARD, c, re.I):
            fails.append("Billet accomplishments: participation as a member of a selection board or court-martial (6.b Note: do not reference it)")
        for pat, why in UNACCEPTABLE:
            m = re.search(pat, c, re.I)
            if m:
                fails.append(f"Billet accomplishments: '{m.group(0)}' falls under unacceptable comments {why}")
        no_num = [l for l in cl if not re.search(r"\d", l)]
        for l in no_num:
            warns.append(f"Billet accomplishments: no number in '{l.strip()[:50]}'; a result without a count is a description")

    body = "\n".join(x for x in (b, c) if x)
    m = re.search(MARKS, body, re.I)
    if m:
        fails.append(f"a claim about the marks, the profile, or promotion ('{m.group(0)}'); the RS assesses the MROW and marks the report (chapter 2 paragraph 3.c(3)); the MROW carries facts")
    for bh in blocked_hits(body):
        fails.append(f"blocked content in the input: {bh}; adverse, medical, family, and financial matters are told to the RS in person, never written into the MROW")
    if rs is not None:
        if re.search(r"\b(?:pending|submitted|recommended for) (?:an? )?(?:award|NAM|medal|MSM|NAVCOM)\b|award recommendation", rs, re.I):
            fails.append("For the RS: a pending award recommendation is listed; the RS cannot discuss pending award recommendations (4.f(1)(a) Note)")
        for bh in blocked_hits(rs):
            fails.append(f"blocked content under For the RS: {bh}")
    if c and re.search(r"\bPME\b|\b(?:career|advanced|expeditionary warfare|command and staff|resident) course\b|distance education|\bschool\b", c, re.I):
        warns.append("PME or schooling appears in the accomplishments; chapter 1 paragraph 6.b puts PME in the summary for the RS (## For the RS), and 6.b(2) keeps section C to items that relate to assigned duties. A student billet is the exception")
    if rs is None:
        warns.append("no '## For the RS' list; chapter 1 paragraph 6.b: the summary is the MRO's chance to tell the RS about awards and PME, and a 'none' line is a fact the RS needs for item 6a")

    stripped = re.sub(r"<MARINE>", "", text)
    for mm in re.finditer(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}([A-Z][a-z]{2,})\b", stripped):
        if mm.group(1) not in ("Major", "Sergeant", "Commander", "Officer", "Corporal", "Colonel", "General", "Marines", "Marine"):
            fails.append(f"a name appears ('{mm.group(0)}'); <MARINE> or a billet until substitution on the user's computer")
            break
    for p in LIFTED:
        if p.lower() in text.lower():
            fails.append(f"lifted from the exemplar or voice file: '{p}'; the example teaches shape, the intake supplies facts")
    if dashes(text):
        fails.append("em or en dash present")

    print(f"MROW INPUT CHECK: {sys.argv[1]}")
    for k, (ch, wd) in counts.items():
        print(f"  {k}: {ch} characters, {wd} words (the order fixes no limit; the A-PES field and the form's space decide)")
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
