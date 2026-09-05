#!/usr/bin/env python3
"""Check an officer's board preparation (board_prep.md) against MARADMIN 622/25 (FY28 officer promotion
selection boards), MCO 1553.4B enclosure (1) (PME complete criteria by grade), and ALMAR 024/25 (the FY26
Commandant's Professional Reading List).

Usage:  python3 board_prep_check.py board_prep.md
Exit 0 = passes (warnings allowed); 1 = a deadline line disagrees with the dates the message prints for the board
named in the header, an audit item is marked verified with no date, the letter to the board breaks a rule the
message states, a title is claimed on the FY26 list that the ALMAR does not print, the PME section does not name
the course the order requires for the grade, a prediction of the result, a name, a dash, a lifted phrase, or
blocked content.

Nothing here is computed that the message does not print or state: the convening and Bd.Corr.Due dates are the
paragraph 1 table as printed; the OMPF document deadline is "two weeks prior to the convening date" (paragraph 7.a).
"""
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes, words  # noqa: E402

# MARADMIN 622/25 paragraph 1 table, as printed: (Selection To, Component) -> (Bd.Corr.Due, Convening Date).
BOARDS = {
    "majgen active": ("27 Jun 26", "8 Jul 26"),
    "majgen reserve": ("26 Jun 26", "7 Jul 26"),
    "bgen active": ("3 Jul 26", "14 Jul 26"),
    "bgen reserve": ("10 Jul 26", "21 Jul 26"),
    "col active": ("24 Apr 26", "5 May 26"),
    "col reserve": ("23 Jul 26", "3 Aug 26"),
    "ltcol active": ("1 May 26", "12 May 26"),
    "ltcol reserve": ("10 Jan 27", "20 Jan 27"),
    "maj active": ("22 May 26", "2 Jun 26"),
    "maj reserve": ("26 Dec 26", "5 Jan 27"),
    "col, ltcol, and maj ar": ("23 Jul 26", "3 Aug 26"),
    "ltcol and maj ldo active": ("14 Aug 26", "25 Aug 26"),
    "capt active": ("22 Jan 27", "2 Feb 27"),
    "capt reserve/ar": ("6 Feb 27", "17 Feb 27"),
    "cwo reserve/ar": ("6 Feb 27", "17 Feb 27"),
    "cwo active": ("31 Jul 26", "11 Aug 26"),
}
FY = "28"
# MARADMIN 622/25 paragraph 4.a table: the grade and the grade it is considered for.
NEXT = {
    "brigadier general": "majgen", "colonel": "bgen", "lieutenant colonel": "col", "major": "ltcol",
    "captain": "maj", "first lieutenant": "capt", "cwo2": "cwo", "cwo3": "cwo", "cwo4": "cwo",
}
# MCO 1553.4B enclosure (1), PME complete criteria by grade. None = no formal PME requirement aside from
# professional self-study per the Marine Corps Professional Reading Program.
PME = {
    "second lieutenant": None, "first lieutenant": None, "cwo2": None, "cwo5": None, "colonel": None,
    "captain": (r"\bEWS\b|EWSDEP|\bACCC\b|Captains? Career Course|Expeditionary Warfare School", "career level paragraph 4.b: EWS, or the EWSDEP, or an ACCC"),
    "cwo3": (r"EWSDEP", "career level paragraph 4.a: the EWSDEP"),
    "ldo captain": (r"EWSDEP", "career level paragraph 4.a: the EWSDEP"),
    "major": (r"\bCSC\b|CSCDEP|Command and Staff|Command and General Staff|College of Naval Command|Command and Staff College", "intermediate level paragraph 5.c: CSC, or the CSCDEP, or the named sister service resident programs, or an approved foreign command and staff college"),
    "cwo4": (r"CSCDEP", "intermediate level paragraph 5.a: the CSCDEP"),
    "ldo major": (r"CSCDEP", "intermediate level paragraph 5.a: the CSCDEP"),
    "lieutenant colonel": (r"MCWAR|Marine Corps War College|War College|College of Naval Warfare|\bNWC\b|\bICAF\b|\bJAWS\b|National War College|Industrial College|Joint Advanced Warfighting", "senior level paragraph 4.b: MCWAR, or a named war college resident program, or NWC, ICAF, or JAWS, or an approved foreign school, or the Army or Air Force War College distance education program"),
    "ldo lieutenant colonel": (r"War College", "senior level paragraph 4.a: the Army or Air Force War College DEP"),
}
# ALMAR 024/25 paragraphs 3 and 4, titles as printed (main title before the colon, lowercased).
FY26 = {
    "once an eagle", "how the few became the proud", "lejeune", "first to fight", "always faithful", "semper fidelis",
    "with the old breed", "delivering destruction", "this kind of war", "the marines of montford point", "code talker",
    "corps competency?", "targeted", "echo in ramadi", "the american war in afghanistan", "on contested shores",
    "learning war", "a game of birds and wolves", "playing war", "neptune's inferno", "a new conception of war",
    "where good ideas come from", "the origins of victory", "evolution on demand", "7 seconds to die", "next war",
    "the fourth industrial revolution", "soft-wired", "co-intelligence", "generative ai for leaders", "the arms of the future",
    "make your bed", "you are worth it", "the white donkey", "on killing", "wisdom of the bullfrog", "matterhorn",
    "the yompers", "generals and admirals, criminals and crooks", "leadership strategy and tactics",
    "the greatest u.s. marine corps stories ever told", "call sign chaos", "risk", "nimitz at war", "five generations at work",
    "essentialism", "the closing of the american mind", "the defence of duffer's drift", "ender's game", "legacy",
    "the infinite game", "turn the ship around!", "on grand strategy", "speed kills", "the new makers of modern strategy",
    "ground combat", "the generals' war", "command", "the russian way of deterrence", "the long game",
    "fleet tactics and naval operations, 3rd ed.", "chinese amphibious warfare",
    "constitution of the united states of america", "warfighting (mcdp 1)", "competing (mcdp 1-4)", "intelligence (mcdp 2)",
    "expeditionary operations (mcdp 3)", "logistics (mcdp 4)", "learning (mcdp 7)", "leading marines (mcwp 6-11)",
    "sustaining the transformation (mcrp 6-11d)",
}
SECTIONS6 = ("commandant's choice", "heritage", "innovation", "leadership", "strategy", "foundational", "foundation")

MON3 = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
DATE = r"\b(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec) (\d{4}|\d{2})\b"
GRADES = r"\b(?:Second Lieutenant|First Lieutenant|Lieutenant Colonel|Brigadier General|Major General|Captain|Major|Colonel|2ndLt|1stLt|Capt|Maj|LtCol|Col|BGen|MajGen|CWO[2-5]|Sergeant Major|Master Sergeant|Gunnery Sergeant|Staff Sergeant|Sergeant|Corporal)"
NOT_NAMES = {"General", "Colonel", "Major", "Sergeant", "Active", "Reserve", "Board", "Promotion", "Selection", "Career", "Course",
             "Corps", "Unrestricted", "Restricted", "Assignments", "Commandant", "Marine", "Marines", "Officer", "Officers", "Command",
             "Staff", "College", "Selects", "Select", "Zone", "Lineal", "Boards"}
PREDICT = r"\b(?:will (?:be )?(?:selected|promoted|pick(?:ed)? up|make (?:major|lieutenant colonel|colonel|captain|brigadier general|general|it))|should (?:pick up|be selected|be promoted|make (?:major|lieutenant colonel|colonel|captain|it))|(?:is|am) (?:a lock|a shoo[- ]in|going to (?:be )?(?:selected|promoted|pick up))|guaranteed (?:selection|promotion)|confident (?:that )?(?:I|the officer|<MARINE>) will|the board will (?:select|promote))\b"
EXTRA_STRIKE = ["is competitive for", "a strong record", "deserves promotion", "the board will see", "i am confident the board",
                "best qualified", "fully qualified", "complete record"]
# Phrases from references/exemplar.md and voice.md. A draft that carries one took its content from the example.
LIFTED = [
    "17 April 2026. 74 documents", "Gap: 13 June 2024 to 28 July 2024, 46 days",
    "courses 8801 through 8804", "Count from the FY26 list in the last 12 months: 4",
    "access confirmed 16 March 2026", "61 documents; the two awards from 2025 are present",
    "Gap of 47 days between the report ending 12 June 2024", "seminars 1 through 6 dated 8 March 2026",
    "Career counselor said on 9 April 2026",
]


def parse_date(s):
    m = re.search(DATE, s)
    if not m:
        return None
    d, y = int(m.group(1)), int(m.group(3))
    mo = MON3[m.group(2).lower()[:3]]
    if y < 100:
        y += 2000
    try:
        return dt.date(y, mo, d)
    except ValueError:
        return None


def all_dates(s):
    return [parse_date(m.group(0)) for m in re.finditer(DATE, s) if parse_date(m.group(0))]


def fmt(d):
    return f"{d.day} {d.strftime('%B')} {d.year}"


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8").read()
    text = re.sub(r"[ \t]+", " ", raw)
    fails, warns = [], []
    head = text.split("\n## ", 1)[0]

    if not re.search(r"^# Board preparation", text, re.M):
        fails.append("title line '# Board preparation' missing")
    if "<MARINE>" not in head:
        fails.append("the Officer line does not carry <MARINE>; the label stays until substitution on the user's computer")

    # The board and its two dates, from the paragraph 1 table.
    bm = re.search(r"Board:\s*(.+?)\s*\(FY(\d{2})\)", head)
    key, fy, corr, conv = None, None, None, None
    if not bm:
        fails.append("no 'Board: <Selection To> <Component> (FY28)' in the header, in the words of the paragraph 1 table")
    else:
        key, fy = re.sub(r"\s+", " ", bm.group(1).strip().lower()), bm.group(2)
        if fy != FY:
            warns.append(f"FY{fy} is not the message this checker carries (MARADMIN 622/25 is FY{FY}); the dates cannot be checked against a table that is not in the library")
        elif key not in BOARDS:
            fails.append(f"board '{bm.group(1).strip()}' is not a row of the MARADMIN 622/25 paragraph 1 table; use the table's own words (for example 'Maj Active', 'Capt Reserve/AR', 'LtCol and Maj LDO Active')")
        else:
            corr, conv = parse_date(BOARDS[key][0]), parse_date(BOARDS[key][1])
    hc = re.search(r"Convening:\s*(" + DATE + r")", head)
    hd = re.search(r"Board correspondence due:\s*(" + DATE + r")", head)
    if not hc or not hd:
        fails.append("header must carry 'Convening: <date>' and 'Board correspondence due: <date>' read from the paragraph 1 table")
    elif conv:
        if parse_date(hc.group(1)) != conv:
            fails.append(f"header convening date {hc.group(1)} disagrees with the table: {key} convenes {BOARDS[key][1]} (MARADMIN 622/25 paragraph 1)")
        if parse_date(hd.group(1)) != corr:
            fails.append(f"header correspondence due {hd.group(1)} disagrees with the table: Bd.Corr.Due for {key} is {BOARDS[key][0]} (MARADMIN 622/25 paragraph 1)")

    # The grade, and whether it pairs with the board.
    gm = re.search(r"Officer:\s*<MARINE>,\s*(LDO )?(Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|Colonel|Brigadier General|CWO[2-5])", head, re.I)
    grade, ldo = None, False
    if not gm:
        fails.append("no grade after <MARINE> on the Officer line (Second Lieutenant .. Brigadier General, CWO2 .. CWO5, with 'LDO' in front where it applies)")
    else:
        grade = gm.group(2).lower()
        ldo = bool(gm.group(1))
        nxt = NEXT.get(grade)
        if key and key in BOARDS and nxt and nxt not in key.split(" ldo")[0].replace(",", "").split():
            fails.append(f"grade '{gm.group(0).split(', ')[1]}' is considered for selection to {nxt} (paragraph 4.a table); the header names the {key} board")
        if key and "ldo" in key and not ldo:
            warns.append("the LDO board is named but the Officer line does not say LDO")

    # Board and dates: every deadline line agrees with the header dates.
    bd = section(text, "Board and dates")
    if bd is None:
        fails.append("no '## Board and dates' section")
    else:
        lines = bd.splitlines()
        if not any(re.search(r"correspondence|President of the Board", ln, re.I) and all_dates(ln) for ln in lines):
            fails.append("no dated correspondence cutoff line; paragraph 1: correspondence must reach MMPB-10 NLT 2359 EST on the Bd.Corr.Due date, statutory, cannot be waived")
        if not any(re.search(r"OMPF documents|MMPB-22", ln, re.I) for ln in lines):
            warns.append("no OMPF document deadline line; paragraph 7.a: two weeks prior to the convening date, to MMPB-22")
        for ln in lines:
            ds = all_dates(ln)
            if not ds or not conv:
                continue
            if re.search(r"correspondence|President of the Board|RQS", ln, re.I) and not re.search(r"Portal access|opt-?out", ln, re.I):
                for d in ds:
                    if d != corr:
                        fails.append(f"deadline line '{ln.strip()[:70]}' carries {fmt(d)}; the table prints Bd.Corr.Due {BOARDS[key][0]} for {key} (paragraph 1)")
            elif re.search(r"OMPF documents|MMPB-22", ln, re.I):
                want = conv - dt.timedelta(days=14)
                for d in ds:
                    if d != want:
                        fails.append(f"OMPF document deadline {fmt(d)} is not two weeks prior to the convening date {fmt(conv)} (paragraph 7.a: 'received by CMC (MMPB-22) two weeks prior to the convening date'); expected {fmt(want)}")
            elif re.search(r"conven", ln, re.I) and not re.search(r"Portal access|TIG|date of rank|zone|opt", ln, re.I):
                for d in ds:
                    if d != conv:
                        fails.append(f"convening date {fmt(d)} on '{ln.strip()[:60]}' disagrees with the table: {BOARDS[key][1]} (paragraph 1)")
        if re.search(r"the week before|a few days before|shortly before|around the", bd, re.I):
            fails.append("a deadline stated as an approximation; the message sets dates (paragraph 1 table, paragraph 7.a)")

    # OMPF and MBS audit: verified means dated.
    au = section(text, "OMPF and MBS audit")
    if au is None:
        fails.append("no '## OMPF and MBS audit' section; paragraph 7 makes the officer personally responsible for the accuracy and completeness of the OMPF and MBS")
    else:
        for ln in au.splitlines():
            for m in re.finditer(r"Verified:\s*Yes\b[ ,]*(.{0,30})", ln, re.I):
                if not re.search(DATE, m.group(1)):
                    fails.append(f"audit item marked verified with no date: '{ln.strip()[:70]}'; the date it was seen in O-RMA, MCTFS, or MOL follows 'Verified: Yes'")
            if re.search(r"Verified:\s*(No|Open)\b", ln, re.I) and not re.search(r"\bsee\b|sent|submitted|request|MMPB|to fix|correct|action", ln, re.I):
                warns.append(f"audit item not verified and no fix named: '{ln.strip()[:70]}'")
        for item, pat, ref in (
            ("OMPF viewed", r"\bOMPF\b", "paragraph 7"), ("MBS viewed", r"\bMBS\b", "paragraph 7"),
            ("additions or deletions in the last 12 months", r"12.month|additions|deletions", "paragraph 7"),
            ("fitness report listing", r"fitness report", "paragraph 7.c"), ("PME completion on the MBS and certificates in the OMPF", r"\bPME\b", "paragraph 7.d"),
            ("civilian education in MCTFS", r"civilian education|MCTFS", "paragraph 7.e"), ("contact data in MOL and MCTFS", r"contact data|\bMOL\b", "paragraph 11"),
            ("classified reports", r"classified", "paragraph 9"),
        ):
            if not re.search(pat, au, re.I):
                warns.append(f"audit does not address {item} ({ref})")
        if key and re.search(r"reserve|\bar\b", key) and not re.search(r"CRCR", au):
            warns.append("reserve component board and the audit does not address the CRCR (paragraph 10.a)")
        if key and re.search(r"reserve|\bar\b", key) and not re.search(r"RQS", text):
            warns.append("reserve component board and no RQS line (paragraph 10.b: highly encouraged, under a signed cover letter, by the correspondence cutoff)")
        if re.search(r"looks good|all good|everything is (?:there|in order)|complete record", au, re.I):
            warns.append("a characterization in the audit ('looks good', 'complete'); say what was seen and when")

    fr = section(text, "Fitness reports")
    if fr is None:
        fails.append("no '## Fitness reports' section (paragraph 7.c)")
    elif re.search(r"\bgap\b", fr, re.I) and not re.search(r"\bno gap|gaps?: none|without a gap|no date gap", fr, re.I) and len(all_dates(fr)) < 2:
        fails.append("a fitness report gap without its dates; paragraph 7.c.1: date gaps must be corrected, and the fix (reconstructed original under one year, certified true copies over) depends on how old the missing report is")

    ph = section(text, "Photo")
    if ph is None:
        fails.append("no '## Photo' section")
    elif not re.search(r"not in the library", ph, re.I):
        warns.append("Photo: MARADMIN 622/25 states no photograph requirement and the publication that governs one is not in the library; say so and record who said what, with a date")

    # PME: required for the grade, then held.
    pm = section(text, "PME")
    if pm is None:
        fails.append("no '## PME' section (MCO 1553.4B enclosure (1); MARADMIN 622/25 paragraph 7.d)")
    elif grade:
        req = PME.get(("ldo " if ldo else "") + grade, PME.get(grade))
        if req is None:
            if not re.search(r"no formal PME|self.study|Reading Program", pm, re.I):
                warns.append(f"MCO 1553.4B enclosure (1): a {grade} has no formal PME responsibilities aside from professional self-study per the Marine Corps Professional Reading Program; say so")
        else:
            pat, where = req
            if not re.search(pat, pm, re.I):
                fails.append(f"PME section does not name the course MCO 1553.4B enclosure (1) requires for a {grade} ({where})")
        if re.search(r"(?<!not )(?<!Not )\bPME complete\b", pm) and not all_dates(pm):
            fails.append("PME complete claimed with no completion date; paragraph 7.d: completion is noted on the MBS and the certificate is in the OMPF, so the date exists")
        if re.search(r"required for promotion|must (?:be|have) .{0,20}(?:PME complete|completed PME) (?:to|for|before) (?:be )?promot", pm, re.I):
            fails.append("the PME section ties PME to promotion; MCO 1553.4B enclosure (1) paragraph 1.d: 'Completion of PME for officers [...] cannot be tied directly to promotion'")
        if not re.search(r"^Status:", pm, re.M):
            warns.append("no 'Status:' line in PME (complete on a date, or not complete with the sub courses done)")

    # Reading: titles claimed on the FY26 list are on it.
    rd = section(text, "Reading")
    if rd is None:
        fails.append("no '## Reading' section (ALMAR 024/25; MCO 1553.4B paragraph 4.b(1)(c))")
    else:
        n = 0
        for m in re.finditer(r'^- [“"](.+?)[”"] \(FY26 CPRL,\s*([^)]+)\)', rd, re.M):
            n += 1
            norm = m.group(1).replace("\u2019", "'").strip().lower()
            title = re.split(r":| \(", norm)[0].strip()
            full = norm
            if title not in FY26 and full not in FY26:
                fails.append(f"'{m.group(1)}' is marked FY26 CPRL and is not a title ALMAR 024/25 prints; list it under Archive or drop the mark")
            if m.group(2).strip().lower() not in SECTIONS6:
                warns.append(f"'{m.group(2)}' is not one of the six sections the ALMAR names (paragraph 2)")
        if n == 0 and not re.search(r"none read|no titles", rd, re.I):
            warns.append("no FY26 title lines in the form '- \"Title\" (FY26 CPRL, Section): read <when>'")
        elif 0 < n < 5:
            warns.append(f"{n} FY26 titles logged; ALMAR 024/25 paragraph 1.a: 'should aim to complete at least five titles annually'")
        if re.search(r"\d+ books? from the Commandant's list", rd, re.I) and n == 0:
            warns.append("a count without titles is not a log")

    # Letter to the board: the message's rules.
    lt = section(text, "Letter to the board")
    if lt is None:
        fails.append("no '## Letter to the board' section; if the officer does not write, the section says so (paragraph 8: encouraged, not required)")
    elif re.search(r"^To:", lt, re.M) or re.search(r"^Subj:", lt, re.M) or re.search(r"^Signed:", lt, re.M):
        if not re.search(r"President, FY\d{2} USMC(?:R|/USMCR)?\b.{0,80}promotion selection board", lt, re.I | re.S):
            fails.append("letter not addressed as the message requires; paragraph 8.a: 'The letter or cover letter must be addressed to: President, FY28 USMC/USMCR (appropriate grade and competitive category) promotion selection board'")
        elif fy and not re.search(r"President, FY" + fy, lt):
            fails.append(f"letter addressed to a different fiscal year than the header's FY{fy} board")
        if not re.search(r"signed.{0,40}\b(ink|CAC)\b", lt, re.I):
            fails.append("no signature line naming ink or CAC; paragraph 8.b: 'All letters to the board must be signed by the eligible officer [...] either with ink or with a CAC digital signature'")
        if re.search(r"\b(?:top secret|secret|confidential|classified)\b", lt, re.I):
            fails.append("classified marking or content in the letter; paragraph 8.c: 'All correspondence must be unclassified. Classified correspondence will not be accepted'")
        third = re.search(r"letter of recommendation|letter from (?:my|the|a) |recommendation from|endorsement from|on my behalf", lt, re.I)
        if third and not re.search(r"^Encl", lt, re.M):
            fails.append(f"third party material ('{third.group(0)}') without an enclosure list; paragraph 8.d: 'Documents or letters of recommendation from other parties [...] will not be provided to the board unless forwarded as a listed enclosure under a signed cover letter'")
        if re.search(r"(?:emailed|sent|mailed|forwarded|submitted) (?:it |the letter |their letter |his letter |her letter )?directly", lt, re.I):
            fails.append("material sent to the board directly by another party; paragraph 8.d: it reaches the board only as a listed enclosure under the officer's signed cover letter")
        if re.search(r"\b(?:place|add|include|insert|file|update|enter)\w*\s+(?:\w+\s+){0,12}(?:in|to|into) my (?:OMPF|official military personnel file|record)", lt, re.I):
            fails.append("the letter asks the board to add material to the record; paragraph 8: 'OMPF materials sent directly to the President of the Board will not become part of an officer's OMPF'")
        if re.search(r"^Encl.*fitness report", lt, re.I | re.M):
            warns.append("a fitness report as an enclosure; paragraph 7.c: 'Reports mailed directly to the President of the Board will not be added to a Marine's OMPF'; the report also goes to MMPB-23")
        if re.search(r"enclos|attached|enclosure \(\d\)", lt, re.I) and not re.search(r"^Encl", lt, re.M):
            fails.append("an enclosure is mentioned and none is listed; paragraph 8.d: 'All enclosures submitted with a letter [...] must be listed as enclosures within the letter'")
        sub = [ln for ln in lt.splitlines() if re.match(r"Submission:", ln)]
        if not sub:
            fails.append("no 'Submission:' line; paragraph 8.e: via the Boards and Surveys Correspondence Portal or via email to the officer promotions organizational mailbox, and the date against the Bd.Corr.Due date")
        else:
            s = sub[0]
            if not re.search(r"Portal|officerpromotions@usmc\.mil|organizational mailbox|email", s, re.I):
                fails.append("submission method is not one the message allows; paragraph 8.e: the Board Correspondence Portal or email to the officer promotions organizational mailbox")
            if re.search(r"email|mailbox", s, re.I) and not re.search(r"Portal", s) and not re.search(r"subject line", lt, re.I):
                warns.append("email submission without the subject line paragraph 8.g requires: 'correspondence to the FY28 USMC/USMCR (appropriate grade) promotion selection board'")
            if corr:
                for d in all_dates(s):
                    if d > corr:
                        fails.append(f"submission line carries {fmt(d)}, after the Bd.Corr.Due date {BOARDS[key][0]}; paragraph 1: 'Late correspondence will not be accepted under any circumstances'")
                if corr not in all_dates(s):
                    warns.append(f"submission line does not carry the Bd.Corr.Due date {BOARDS[key][0]} (paragraph 1 table)")
        if re.search(r"not be selected|non[- ]selection|not (?:wish|want) to be (?:selected|promoted)|request(?:ing)? (?:that I )?not be (?:selected|promoted)", lt, re.I):
            warns.append("a request for non selection; paragraph 8.h: the officer 'will still be considered for promotion and will incur a failure of selection if not recommended', and under 10 U.S.C. 1174 'is not entitled to separation pay if involuntarily discharged from active duty'")
        if words(lt) > 400:
            warns.append(f"letter section runs {words(lt)} words; the board reads hundreds, and the letter tells it what the record does not show")
        for w in strike_hits(lt) + [w for w in EXTRA_STRIKE if w in lt.lower()]:
            warns.append(f"strike list in the letter: '{w}'")
    elif not re.search(r"\bnone\b|does not (?:submit|write)|no letter|not required", lt, re.I):
        warns.append("Letter to the board neither drafts a letter nor says the officer does not write one")

    # Whole product.
    pm_hit = re.search(PREDICT, text, re.I)
    if pm_hit:
        fails.append(f"a prediction of the result ('{pm_hit.group(0)}'); the product prepares the record, the board decides")
    for w in strike_hits(text.replace(lt or "", "")) + [w for w in EXTRA_STRIKE if w in text.replace(lt or "", "").lower()]:
        warns.append(f"strike list: '{w}'")
    scrub = re.sub(r"<MARINE>", "", text)
    for mm in re.finditer(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}([A-Z][a-z]{2,})\b", scrub):
        if mm.group(1) not in NOT_NAMES:
            fails.append(f"a name appears ('{mm.group(0)}'); <MARINE> until substitution on the user's computer")
            break
    for p in LIFTED:
        if p.lower() in text.lower():
            fails.append(f"lifted from the exemplar or voice file: '{p}'; the example teaches shape, the intake supplies facts")
    for b in blocked_hits(re.sub(r"Classified reports? \(paragraph 9\)|classified reports?", "", text, flags=re.I)):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")

    print(f"BOARD PREP CHECK: {sys.argv[1]}  {key or 'no board'}  {grade or 'no grade'}")
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
