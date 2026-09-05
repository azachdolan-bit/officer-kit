#!/usr/bin/env python3
"""Check a JEPES command input (jepes_input.md) against MCO 1616.1 enclosure (1) chapter 1 paragraphs 3, 5 and 6 and
chapter 2 paragraphs 1, 2 and 3.

Usage:  python3 jepes_input_check.py jepes_input.md
Exit 0 = passes (warnings allowed); 1 = a grade the order does not cover, a preparer the order does not let mark, an
occasion or date the order does not recognize, a mark outside 0.0 to 5.0 or with a band name that disagrees with it,
a mark with no dated fact under it or no fact inside the period, an Exceptional mark without commendatory material,
a Below Expectations mark without counseling, a 0.0 without a NOT REC, a NOT REC without a dated justification,
marks submitted more than 45 days early, an initial counseling missing an element or outside its 30 days, a promise
about promotion, blocked content, a name, a lifted exemplar phrase, or a dash.
"""
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes, words  # noqa: E402
from jepes_dates import OCCASIONS, parse, fmt, fixed_period_for, SUBMIT_DAYS, MIN_OBSERVATION, COUNSELING_DAYS  # noqa: E402

CATEGORIES = ["Individual Character", "MOS and/or Mission Accomplishment", "Leadership"]
# Chapter 2 paragraph 3.a: the bands and their ranges, low to high inclusive.
BANDS = [
    ("Below Expectations", 0.1, 0.9),
    ("Working Towards Expectations", 1.0, 1.9),
    ("Meets Expectations", 2.0, 3.0),
    ("Exceeds Expectations", 3.1, 4.0),
    ("Exceptional", 4.1, 5.0),
]
COVERED_GRADES = r"(?:Private First Class|Private|Lance Corporal|Corporal|Pvt|PFC|LCpl|Cpl)"
NOT_COVERED = r"(?:Sergeant Major|Master Gunnery Sergeant|First Sergeant|Master Sergeant|Gunnery Sergeant|Staff Sergeant|Sergeant|SgtMaj|MGySgt|1stSgt|MSgt|GySgt|SSgt|Sgt)"
MARKING_ROLES = r"(?:First Line Supervisor|FLS|Evaluator|Reviewer|Approver)"
NON_MARKING_ROLES = r"(?:Senior Enlisted Reviewer|SER|Command Reviewer)"
GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|Pvt|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"
DATE = r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b"
MARK = r"Mark:\s*(-?\d+(?:\.\d+)?)\s*(?:\(([^)]*)\))?"
COMMEND = r"\b(?:certificate of commendation|certificate of appreciation|letter of appreciation|meritorious mast|achievement medal|commendation medal|NAM|NAVCOM|medal|award(?:ed)?|commendatory material)\b"
ADVERSE = r"legal action|separation proceedings|Body Composition|\bBCP\b|Military Appearance|\bMAP\b|PFT/CFT failure|PFT failure|CFT failure|training failure|Competency Review Board|\bCRB\b"
PROMISE = r"\b(?:will (?:be promoted|pick up|make (?:corporal|sergeant)|get promoted)|guarantee\w*|deserves (?:to be )?promot\w+|should be promoted|is a lock for|next cycle for sure)\b"
EXTRA_STRIKE = ["hard charger", "asset to the unit", "great marine", "motivated", "always", "never fails", "future sergeant major", "top marine in the platoon"]
# Phrases from references/exemplar.md and voice.md. A draft that carries one took its content from the example.
LIFTED = [
    "Returned a wallet with 340 dollars found on the range road",
    "placed 3rd of the 41 lance corporals in the company",
    "no weapon stoppage across 6 live fire attacks",
    "Led the fire team for 11 days from 8 to 18 June 2026",
    "hold the fire team billet for a full training cycle",
    "Rebuilt 9 of the platoon's 11 radio batteries",
    "recovery of a disabled vehicle under blackout conditions",
    "for missing the 0600 formation",
    "keeps the section's 3 loadsets current",
]


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else None


def header_date(head, label):
    m = re.search(label + r":\s*(" + DATE + r"|\d{4}-\d{2}-\d{2})", head)
    return parse(m.group(1)) if m else None


def band_for(value):
    for name, lo, hi in BANDS:
        if lo <= value <= hi:
            return name
    return None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8").read()
    text = re.sub(r"[ \t]+", " ", raw)
    fails, warns = [], []
    head = text.split("\n## ", 1)[0]

    counseling = bool(re.search(r"^# JEPES initial counseling", text, re.M))
    if not counseling and not re.search(r"^# JEPES command input", text, re.M):
        fails.append("title line '# JEPES command input' (or '# JEPES initial counseling') missing")
    if "<MARINE>" not in head:
        fails.append("the Marine line does not carry <MARINE>; the label stays until substitution on the user's computer")

    # The grades the order covers: Private through Corporal (basic order paragraph 1; chapter 1 paragraph 1.a; chapter 2 paragraph 2.a).
    marine_line = re.search(r"Marine:\s*(.+?)(?=\s+Prepared by:|\n|$)", head)
    ml = marine_line.group(1) if marine_line else head
    if re.search(r"\b" + NOT_COVERED + r"\b", ml) and not re.search(r"\b" + COVERED_GRADES + r"\b", ml):
        fails.append(f"grade '{re.search(NOT_COVERED, ml).group(0)}' is not covered; JEPES evaluates Private through Corporal (chapter 1 paragraph 1.a), Sergeant and above fall under the PES and MCO 1610.7B")
    elif not re.search(r"\b" + COVERED_GRADES + r"\b", ml):
        fails.append("no covered grade on the Marine line (Private, Private First Class, Lance Corporal, Corporal)")
    gm = re.search(r"\b" + COVERED_GRADES + r"\b", ml)
    grade = gm.group(0) if gm else None

    # Who prepares: only the FLS, Evaluator, Reviewer (and the Approver) make marks (chapter 1 paragraph 5; chapter 2 paragraph 1.e).
    prep = re.search(r"Prepared by:\s*(.+?)(?=\s+Approver:|\n|$)", head)
    role = prep.group(1).strip() if prep else ""
    if not prep:
        fails.append("no 'Prepared by:' line naming the preparer's reporting chain role (chapter 1 paragraph 5)")
    elif re.search(r"\b" + NON_MARKING_ROLES + r"\b", role):
        fails.append(f"prepared by '{role}': the Senior Enlisted Reviewer and Command Reviewer do not make recommended command input marks (chapter 1 paragraph 5.d and 5.f; chapter 2 paragraph 1.e)")
    elif not re.search(r"\b" + MARKING_ROLES + r"\b", role):
        fails.append(f"prepared by '{role}' is not a reporting chain role that marks (First Line Supervisor, Evaluator, Reviewer; chapter 1 paragraph 5)")
    is_fls = bool(re.search(r"First Line Supervisor|\bFLS\b", role))
    if not re.search(r"Approver:\s*\S", head):
        warns.append("no 'Approver:' line; the O-5 level commander or OIC equivalent sets the final marks (chapter 1 paragraph 5.g), name the billet")

    occ = re.search(r"Occasion:\s*([A-Z]{2})\b|Occasion:\s*(Initial counseling)", head)
    code = None
    if not occ:
        fails.append("no 'Occasion:' line with one of the order's codes (PR, TR, CD, TD, TC, AN, SA, AT, DC, RD, DD, RT; chapter 2 paragraph 2.b) or 'Initial counseling'")
    elif occ.group(2):
        if not counseling:
            fails.append("Occasion: Initial counseling belongs under the title '# JEPES initial counseling'")
    else:
        code = occ.group(1)
        if code not in OCCASIONS:
            fails.append(f"occasion code '{code}' is not one the order recognizes (chapter 2 paragraph 2.b lists PR, TR, CD, TD, TC, AN, SA, AT, DC, RD, DD, RT)")
            code = None
        elif counseling:
            fails.append(f"occasion {code} is a reporting occasion; the product title is '# JEPES command input'")

    supervision = header_date(head, "Supervision began")
    ic_date = header_date(head, "Initial counseling")

    if counseling:
        conducted = header_date(head, "Conducted")
        due = header_date(head, "Due")
        if not supervision:
            fails.append("no 'Supervision began:' date; the 30 days run from the relationship being established (chapter 2 paragraph 1.b(1))")
        else:
            expected_due = supervision + dt.timedelta(days=COUNSELING_DAYS)
            if due and due != expected_due:
                fails.append(f"Due {fmt(due)} disagrees with the order's 30 days from {fmt(supervision)}: {fmt(expected_due)}")
            if not conducted:
                fails.append("no 'Conducted:' date for the initial written counseling")
            elif conducted > expected_due:
                fails.append(f"initial counseling conducted {fmt(conducted)}, after the 30 days the order allows (due {fmt(expected_due)}; chapter 2 paragraph 1.b(1))")
            elif conducted < supervision:
                fails.append(f"conducted {fmt(conducted)} is before supervision began {fmt(supervision)}")
        for name in ("Billet description", "Role in the unit", "Responsibilities", "Performance expectations"):
            s = section(text, name)
            if s is None or words(s) < 5:
                fails.append(f"'## {name}' missing or empty; chapter 2 paragraph 1.b(1) names it as an element of the initial written counseling")
        exp = section(text, "Performance expectations")
        if exp and not re.search(r"\d", exp):
            warns.append("no number in the performance expectations; an expectation without a count or a date cannot be checked at the debrief")
        if section(text, "Objective scores validated") is None:
            warns.append("no '## Objective scores validated'; chapter 1 paragraph 6.b pairs the initial counseling with validating objective scores and starting corrective action")
        for c in CATEGORIES:
            if section(text, c) is not None:
                warns.append(f"'## {c}' in an initial counseling; marks are drafted on a reporting occasion, the counseling sets expectations")
        body = "\n".join(s for s in (section(text, n) for n in ("Billet description", "Role in the unit", "Responsibilities", "Performance expectations", "Objective scores validated")) if s)
        for b in blocked_hits(body):
            fails.append(f"blocked content: {b}")
        for w in strike_hits(body):
            warns.append(f"strike list: '{w}'")

    start = end = None
    if code:
        start = header_date(head, "From")
        end = header_date(head, "To")
        submitted = header_date(head, "Submitted")
        rule = OCCASIONS[code]
        if not start or not end:
            fails.append(f"From: and To: dates as day month year are required; {code} ends {rule['to']} (chapter 2 paragraph 2.b)")
        else:
            if rule["fixed"]:
                fixed_start = fixed_period_for(code, end)
                if fixed_start is None:
                    fails.append(f"To {fmt(end)} is not a {code} end date; the order fixes {code} TO DATE: {rule['to']} (chapter 2 paragraph 2.b({'7' if code == 'SA' else '6'}))")
                elif not (fixed_start <= start <= end):
                    fails.append(f"From {fmt(start)} is outside the {code} period {fmt(fixed_start)} to {fmt(end)} (chapter 2 paragraph 2.b)")
                elif start != fixed_start:
                    warns.append(f"From {fmt(start)} is later than the period's {fmt(fixed_start)}; that is right only when a previous occasion ended {fmt(start - dt.timedelta(days=1))} (chapter 2 paragraph 2.b)")
            elif start > end:
                fails.append(f"From {fmt(start)} is after To {fmt(end)}")
            days = (end - start).days + 1
            if days < MIN_OBSERVATION:
                warns.append(f"observation {days} days, under the {MIN_OBSERVATION} day minimum (chapter 2 paragraph 2.c; service schools under 30 days excepted)")
            if submitted:
                if (end - submitted).days > SUBMIT_DAYS:
                    fails.append(f"submitted {fmt(submitted)}, more than {SUBMIT_DAYS} days before To {fmt(end)}; recommended marks may not be submitted earlier than {fmt(end - dt.timedelta(days=SUBMIT_DAYS))} (chapter 1 paragraphs 3.c and 6.c)")
                elif submitted > end:
                    warns.append(f"submitted {fmt(submitted)} after To {fmt(end)}; the occasion is delinquent once past its to date without approval (chapter 1 paragraph 3.c)")
            else:
                warns.append("no 'Submitted:' date; the 45 day window (chapter 1 paragraph 6.c) cannot be checked")
            if supervision and start <= supervision <= end and not ic_date:
                msg = f"supervision began {fmt(supervision)}, inside this period, and no 'Initial counseling:' date is recorded; the FLS owes an initial written counseling within 30 days (chapter 2 paragraph 1.b(1))"
                (fails if is_fls else warns).append(msg)
            if supervision and ic_date and (ic_date - supervision).days > COUNSELING_DAYS:
                warns.append(f"initial counseling {fmt(ic_date)} was later than 30 days after supervision began {fmt(supervision)}")
        if code == "PR" and grade in ("Private", "Pvt", "Private First Class", "PFC"):
            fails.append(f"PR with grade {grade}: promotion to private first class and lance corporal do not qualify as a reporting occasion (chapter 2 paragraph 2.b(1))")
        if code in ("AN", "AT") and not re.search(r"Reserve", head, re.I):
            warns.append(f"{code} is an occasion for Marines in the Reserve Component (chapter 2 paragraph 2.b); say so on the header or use SA")

    marks = {}
    if not counseling:
        for c in CATEGORIES:
            s = section(text, c)
            if s is None:
                fails.append(f"'## {c}' missing; the order names three lines of command input (chapter 1 paragraph 1.c(1)d)")
                continue
            mm = re.search(MARK, s)
            if not mm:
                fails.append(f"{c}: no 'Mark: X.X (Band)' line")
                continue
            value = float(mm.group(1))
            marks[c] = value
            if value < 0 or value > 5 or not re.fullmatch(r"\d\.\d", mm.group(1)):
                fails.append(f"{c}: mark {mm.group(1)} is outside the order's 0.0 to 5.0 scale with one decimal (chapter 2 paragraph 3.a; appendix B line 4)")
                continue
            band = band_for(value)
            label = (mm.group(2) or "").strip()
            if value == 0.0:
                if not label:
                    warns.append(f"{c}: 0.0 carries no band; it is a NOT REC by default (chapter 2 paragraph 3.b(2))")
            elif not label:
                warns.append(f"{c}: name the band with the number: '{band}' (chapter 2 paragraph 3.a)")
            elif label.lower() != band.lower():
                fails.append(f"{c}: mark {mm.group(1)} is '{band}' in the order's bands, not '{label}' (chapter 2 paragraph 3.a)")
            facts = s[mm.end():]
            dates = [parse(d) for d in re.findall(DATE, facts)]
            if not dates:
                fails.append(f"{c}: no dated fact under the mark; command input is based on the Marine's accomplishments during the reporting period (chapter 1 paragraph 3.b(2))")
            elif start and end:
                inside = [d for d in dates if start <= d <= end]
                if not inside:
                    fails.append(f"{c}: no fact dated inside the period {fmt(start)} to {fmt(end)} (chapter 1 paragraph 3.b(2))")
                for d in dates:
                    if not (start <= d <= end):
                        warns.append(f"{c}: fact dated {fmt(d)} is outside the period {fmt(start)} to {fmt(end)}")
            if value >= 4.1:
                if not re.search(COMMEND, facts, re.I):
                    fails.append(f"{c}: {mm.group(1)} is Exceptional; the order requires formal commendatory material visible in JEPES, named by type and date (chapter 2 paragraph 3.a(1))")
                if not re.search(r"directed comment", facts, re.I):
                    warns.append(f"{c}: Exceptional requires a justification comment from the drop-down list of directed comments; say which was selected (chapter 2 paragraph 3.a(1))")
            if 0.1 <= value <= 0.9:
                if not re.search(r"counsel", facts, re.I) or not dates:
                    fails.append(f"{c}: {mm.group(1)} is Below Expectations; the order places it on counseling, documented or informal, during the period, by date (chapter 2 paragraph 3.a(5))")
                if not re.search(r"directed comment", facts, re.I):
                    warns.append(f"{c}: Below Expectations requires a justification comment from the drop-down list of directed comments; say which was selected (chapter 2 paragraph 3.a(5))")
            if not re.search(r"\d", re.sub(DATE, "", facts)):
                warns.append(f"{c}: no count in the facts; a fact without a number is a characterization")
            for w in strike_hits(facts) + [w for w in EXTRA_STRIKE if re.search(r"\b" + re.escape(w) + r"\b", facts.lower())]:
                warns.append(f"{c}: strike list: '{w}'")
            pm = re.search(PROMISE, facts, re.I)
            if pm:
                fails.append(f"{c}: a promise about promotion ('{pm.group(0)}'); the cutting score and the Approver decide (appendix C; chapter 1 paragraph 5.g)")
            for b in blocked_hits(facts):
                fails.append(f"{c}: blocked content: {b}; an adverse fact is the order's category and a date")

        promo = section(text, "Promotion recommendation")
        if promo is None:
            fails.append("no '## Promotion recommendation'; the Marine is recommended by default and a NOT REC occurs with every occasion (chapter 2 paragraph 3.b)")
        else:
            notrec = bool(re.search(r"NOT REC", promo))
            if not notrec and not re.search(r"recommended for promotion", promo, re.I):
                fails.append("## Promotion recommendation must say 'Recommended for promotion' or 'NOT REC' (chapter 2 paragraph 3.b)")
            zeros = [c for c, v in marks.items() if v == 0.0]
            if zeros and not notrec:
                fails.append(f"a 0.0 in {', '.join(zeros)} is a NOT REC by default (chapter 2 paragraph 3.b(2)); the promotion recommendation must say so")
            if notrec:
                if not re.search(DATE, promo):
                    fails.append("NOT REC without a dated justification; the order requires a directed justified comment (chapter 2 paragraph 3.b(3))")
                if not re.search(ADVERSE, promo, re.I) and not re.search(r"directed", promo, re.I):
                    warns.append("NOT REC names none of the order's adverse material categories (chapter 2 paragraph 3.c) and no directed comment; say which applies")
                if not re.search(r"until the next occasion|lifted", promo, re.I):
                    warns.append("say that the NOT REC is in effect until the next occasion or lifted by the commander (chapter 2 paragraph 3.b(1))")
            pm = re.search(PROMISE, promo, re.I)
            if pm:
                fails.append(f"a promise about promotion in the recommendation ('{pm.group(0)}')")
            scrubbed = re.sub(r"\bNJPs?\b|non-?judicial punishments?|court[- ]martial", "", promo, flags=re.I)
            for b in blocked_hits(scrubbed):
                fails.append(f"blocked content in the promotion recommendation: {b}; use the order's category and a date")
        if section(text, "Debrief") is None:
            warns.append("no '## Debrief'; the cycle ends when the Marine is debriefed by the FLS and/or the reporting chain (chapter 1 paragraph 6.f)")

    mm = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]{2,}\b", re.sub(r"<MARINE>", "", text))
    if mm and not re.search(r"^(?:Private First|Lance Corporal|Sergeant Major|First Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|Corporal Course|Corporals Course|First Line|Captain Career)$", mm.group(0)):
        fails.append(f"a name appears ('{mm.group(0)}'); <MARINE> until substitution on the user's computer")
    for p in LIFTED:
        if p.lower() in text.lower():
            fails.append(f"lifted from the exemplar or voice file: '{p}'; the example teaches shape, the intake supplies facts")
    for b in blocked_hits(head):
        fails.append(f"blocked content in the header: {b}")
    if dashes(text):
        fails.append("em or en dash present")

    label = "initial counseling" if counseling else (code or "no occasion")
    summary = " ".join(f"{c.split()[0]} {v:.1f}" for c, v in marks.items())
    print(f"JEPES INPUT CHECK: {sys.argv[1]}  {label}  {summary}".rstrip())
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
