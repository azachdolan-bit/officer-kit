#!/usr/bin/env python3
"""Check a Meritorious Mast (mer_mast.md) or a Certificate of Commendation (certcom.md) against MCO 1650.19J
w/Ch 1 enclosure (2) paragraphs 1, 8.f, 8.g, and 8.h and enclosure (1) paragraphs 1.l(5) and 9.a.

Usage:  python3 meritorious_mast_check.py mer_mast.md
Exit 0 = passes (warnings allowed); 1 = the level check names a different recognition than the product is
(a Mast for service the order says is a Certificate of Commendation, a Letter of Appreciation, or a personal
decoration, 8.g(1)), the routing the order sets is missing or backwards (copy to CMC (MMSB), nothing to
CMC (MMMA)), the awarding officer is not one the order lets sign, a Mast for an officer, a number in the text
the Facts section does not carry (the award tool's citation versus SOA logic), a promise, a name, a unit by
name, a lifted exemplar phrase, blocked content, or a dash.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes, words  # noqa: E402

PRODUCTS = {"Meritorious Mast": "MM", "Certificate of Commendation": "CC"}
RECOGNITIONS = [
    ("Meritorious Mast", "MM"),
    ("Certificate of Commendation", "CC"),
    ("Letter of Appreciation", "LOA"),
    ("personal decoration", "DEC"),
    ("Navy and Marine Corps Achievement Medal", "DEC"),
    ("Navy and Marine Corps Commendation Medal", "DEC"),
    ("Meritorious Service Medal", "DEC"),
    ("fitness report", "NONE"),
    ("proficiency and conduct", "NONE"),
    ("none", "NONE"),
]
OFFICER_GRADES = r"\b(?:Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|Colonel|Brigadier General|Major General|Warrant Officer|Chief Warrant Officer|2ndLt|1stLt|Capt|Maj|LtCol|Col|BGen|MajGen|WO|CWO\d?)\b"
GRADES = r"(?:Private First Class|Private|Lance Corporal|Corporal|Staff Sergeant|Gunnery Sergeant|Master Gunnery Sergeant|Master Sergeant|First Sergeant|Sergeant Major|Sergeant|Second Lieutenant|First Lieutenant|Captain|Lieutenant Colonel|Major|Colonel|Pvt|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|MGySgt|SgtMaj|2ndLt|1stLt|Capt|Maj|LtCol|Col)"
DATE = r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b"
MONTH_YEAR = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b"
UNIT_NAME = r"\b\d{1,3}(?:st|d|nd|rd|th)\s+(?:Bn|Battalion|Marines|Marine Regiment|Regiment|MarDiv|Marine Division|MAW|Marine Aircraft Wing|MLG|Marine Logistics Group|MEU|Marine Expeditionary (?:Unit|Brigade|Force)|MEF|MEB|Marine Corps District|Recruit Training Battalion)\b|\b(?:MCAS|MCB|MCRD|MCLB|MCAGCC|Camp)\s+[A-Z][a-z]+\b"
PROMISE = r"\b(?:will (?:be (?:promoted|meritoriously promoted|selected)|make an? (?:outstanding|excellent|fine|superb)|receive|earn)|guarantee\w*|deserves? (?:promotion|a medal|an award|to be promoted)|recommended for (?:meritorious )?promotion|is a lock for)\b"
EXTRA_STRIKE = ["asset to the marine corps", "great marine", "hard charger", "goes above and beyond", "second to none",
                "countless", "numerous", "always", "never fails", "selfless", "consummate professional", "sets the example"]
ABBR = r"\b(?:NCOIC|SNCOIC|OIC|MOS|TAD|BN|PLT|SQD|MEU|MAGTF|FMF|SOP|OPORD|CFT|PFT|CMC|MMSB|MMMA|OMPF|APS)\b"
# Phrases from references/exemplar.md and voice.md. A draft that carries one took its content from the example.
LIFTED = [
    "found 37 line items posted to the wrong account",
    "closed the inventory with 0 discrepancies, against 9",
    "spared the section a third cycle of the same error",
    "rewrote the battery's radio maintenance checklist",
    "radio readiness rose from 71 percent to 94 percent",
    "trained 22 radio operators from 4 batteries",
    "now maintain their radios to one standard written by this Marine",
    "Rebuilt 212 serialized item records in 14 working days",
    "regained a green armory rating for the first time in three quarters",
]
# The award tool's citation versus SOA logic: every number in the text must appear in the facts.
# "one" is left out of the spelled numbers because in prose it is usually a pronoun.
WORD_NUMBERS = {
    "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "fifteen": 15, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100,
}


def numbers_in(text):
    found = set()
    for m in re.findall(r"\$?\d[\d,]*(?:\.\d+)?", text):
        found.add(m.replace("$", "").replace(",", ""))
    for w in re.findall(r"[A-Za-z]+", text.lower()):
        if w in WORD_NUMBERS:
            found.add(str(WORD_NUMBERS[w]))
    return found


def section(text, name):
    m = re.search(r"## " + name + r"\s*\n(.*?)(?=\n## |\Z)", text, re.S)
    return m.group(1).strip() if m else None


def negated(text, token):
    """True if every sentence or bullet that mentions token also carries a negation."""
    hits = [s for s in re.split(r"(?<=[.;])\s+|\n", text) if re.search(token, s)]
    return bool(hits) and all(re.search(r"\b(?:not|no|never|nothing)\b", s, re.I) for s in hits)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8").read()
    text = re.sub(r"[ \t]+", " ", raw)
    fails, warns = [], []
    head = text.split("\n## ", 1)[0]

    tm = re.match(r"# (Meritorious Mast|Certificate of Commendation)\s*$", text.split("\n", 1)[0].strip())
    product = PRODUCTS[tm.group(1)] if tm else None
    if not tm:
        fails.append("title line must be '# Meritorious Mast' or '# Certificate of Commendation'")
    if "<MARINE>" not in head:
        fails.append("the Marine line does not carry <MARINE>; the label stays until substitution on the user's computer")
    if not re.search(r"Unit:", head):
        fails.append("no 'Unit:' in the header; the unit by echelon, not by name")
    am = re.search(r"Awarding officer:\s*(.+?)(?=\s+Date:|\n|$)", head, re.I)
    officer = am.group(1).strip().lower() if am else ""
    if not am:
        fails.append("no 'Awarding officer:' line in the header, by billet")
    if not re.search(r"Date:\s*" + DATE, head):
        warns.append("no 'Date: <day month year>' in the header")

    if product == "MM":
        gm = re.search(r"<MARINE>,\s*([^,]+?),", head)
        if gm and re.search(OFFICER_GRADES, gm.group(1)):
            fails.append(f"a Meritorious Mast is for an enlisted Marine (8.g); the header grade is '{gm.group(1).strip()}'")
        if officer:
            if re.search(r"by direction|on behalf|acting for", officer):
                fails.append("a Meritorious Mast is held by the Marine's Commander (8.g); 'by direction' is not that officer")
            elif re.search(r"platoon commander|platoon sergeant|section leader|first sergeant|sergeant major|executive officer|company commander|battery commander|detachment commander|officer in charge", officer) and not re.search(r"commanding officer|commanding general|\bcommander, ", officer):
                fails.append(f"awarding officer '{am.group(1).strip()}' is below the echelon the order sets: the Marine's Commander (battalion or equivalent echelon), 8.g. That officer reports; the commander holds the Mast")
            elif not re.search(r"commanding officer|commanding general|commander", officer):
                fails.append(f"awarding officer '{am.group(1).strip()}' is not a commander; the Mast is the Marine's Commander's (battalion or equivalent echelon), 8.g")
        if not re.search(r"Reported by:|reported (?:it|this|the performance)", text, re.I):
            warns.append("who observed the performance and reported it to the commander is not named by billet (8.g: the senior person who has observed the Marine's performance shall make a report)")
    if product == "CC" and officer:
        if re.search(r"by direction|on behalf|acting for", officer):
            fails.append("a Certificate of Commendation is issued by a general officer or a commander with NA authority (8.f(1)); 'by direction' is not that officer")
        elif not re.search(r"commanding general|general|commanding officer|commander", officer):
            fails.append(f"awarding officer '{am.group(1).strip()}' is not a general officer or a commander; any other officer recommends to one who has NA authority (8.f(2))")
        elif not re.search(r"general|special courts|spcmca|na authority|achievement medal authority", officer) and not re.search(r"special courts|spcmca|NA authority|1\.l\(5\)", text, re.I):
            warns.append("say what gives the awarding officer the authority: a general officer, or a commander with delegated NA authority as a Special Courts Martial Convening Authority (8.f(1); enclosure (1) 1.l(5))")

    lvl = section(text, "Level check")
    named = None
    if lvl is None:
        fails.append("no '## Level check' section; the recognition follows the facts (enclosure (2) paragraph 1)")
    else:
        rm = re.search(r"Recognition:\s*(.+)", lvl)
        if not rm:
            fails.append("## Level check has no 'Recognition: <Meritorious Mast | Certificate of Commendation | Letter of Appreciation | personal decoration>' line")
        else:
            line = rm.group(1).strip()
            found = [(n, code) for n, code in RECOGNITIONS if re.search(r"\b" + re.escape(n) + r"\b", line, re.I)]
            if not found:
                fails.append(f"'Recognition: {line}' names none of the order's recognitions")
            else:
                named = found[0][1]
                if len({c for _, c in found}) > 1:
                    fails.append(f"'Recognition: {line}' names more than one recognition; the level check picks one")
                elif named != product:
                    if named == "NONE":
                        fails.append(f"the level check says the facts stay in the marks and the fitness report; no {tm.group(1)} is drafted for them (enclosure (2) paragraph 1)")
                    elif product == "MM":
                        fails.append(f"the product is a Meritorious Mast and the level check says the facts are a {found[0][0]}. 8.g(1): 'A Meritorious Mast shall not be conducted when the service or performance of the Marine is recognized through the awarding of a Letter of Appreciation, Certificate of Commendation, or a personal decoration.' Draft that recognition instead")
                    else:
                        fails.append(f"the product is a Certificate of Commendation and the level check says the facts are a {found[0][0]}; the product type must follow the level check")
        if named == product and not re.search(r"8\.g\(1\)|shall not be conducted", lvl):
            warns.append("the level check does not cite 8.g(1); say that no other recognition covers this service (a Mast), or that no Mast is held because this certificate recognizes it")
        if named == product and not re.search(r"magnitude|level of responsibility|beyond the usual requirements|industry|judgment|initiative", lvl, re.I):
            warns.append("the level check does not use the order's factors: magnitude of the achievement and level of responsibility (enclosure (2) paragraph 1), or the 8.g threshold words")

    facts = section(text, "Facts")
    if facts is None or words(facts) < 10:
        fails.append("## Facts missing or under 10 words; the text proves nothing the facts do not")
    else:
        if not re.search(DATE, facts) and not re.search(MONTH_YEAR, facts):
            fails.append("no date in ## Facts; facts are dated")
        if not re.search(r"\d", re.sub(DATE + "|" + MONTH_YEAR, "", facts)):
            fails.append("no count in ## Facts beyond the dates; facts are countable")

    body = section(text, "Text")
    if body is None or words(body) < 20:
        fails.append("## Text missing or under 20 words")
    else:
        if "<MARINE>" not in body:
            warns.append("the text does not name the Marine by label; grade and <MARINE> at first mention")
        if facts:
            missing = sorted(numbers_in(body) - numbers_in(facts), key=lambda s: (len(s), s))
            if missing:
                fails.append(f"numbers in the text not found in ## Facts: {', '.join(missing)} (the text carries nothing the facts do not prove)")
        if not re.search(r"\d", body):
            warns.append("no number in the text; a recognition without a count is a characterization")
        if not re.search(DATE + "|" + MONTH_YEAR, body):
            warns.append("no date or period in the text")
        for w in strike_hits(body) + [w for w in EXTRA_STRIKE if re.search(r"\b" + re.escape(w) + r"\b", body.lower())]:
            warns.append(f"strike list: '{w}'")
        pm = re.search(PROMISE, body, re.I)
        if pm:
            fails.append(f"a promise ('{pm.group(0)}'); a recognition records what happened, not what a board or a commander will decide")
        for b in blocked_hits(body):
            fails.append(f"blocked content in the text: {b}")
        if ";" in body:
            warns.append("semicolon in the text; one claim per sentence")
        abbr = set(re.findall(ABBR, body))
        if abbr:
            warns.append(f"abbreviations the formation or the family may not know: {', '.join(sorted(abbr))}")
        if words(body) > 200:
            warns.append(f"the text runs {words(body)} words; the form's block is not in the library, so confirm it fits NAVMC {'10935' if product == 'MM' else '10631'}")

    rt = section(text, "Routing")
    if rt is None:
        fails.append("no '## Routing' section")
    else:
        if not re.search(r"MMSB", rt):
            fails.append("routing does not send a copy to CMC (MMSB) for the OMPF (8.g(2) for a Mast; 8.f(2) and enclosure (1) 9.a for a certificate)")
        if not re.search(r"MMMA", rt):
            fails.append("routing does not say that no copy goes to CMC (MMMA) (8.g(2); 8.f(2); enclosure (1) 9.a)")
        elif not negated(rt, r"MMMA"):
            fails.append("routing sends something to CMC (MMMA); the order: do not forward copies of approved Meritorious Masts or command level Certificates of Commendation to CMC (MMMA)")
        if not re.search(r"OMPF", rt):
            warns.append("say that the MMSB copy is for the OMPF; that is the reason the copy goes (8.g(2), 8.f(2))")
        if product == "MM":
            if not re.search(r"NAVMC 10935", rt):
                fails.append("routing does not name the form: NAVMC 10935, the Meritorious Mast form (8.g(2))")
            if re.search(r"HQMC APS|1650 ?\(EF\)|iAPS", rt) and not negated(rt, r"HQMC APS|1650 ?\(EF\)|iAPS"):
                warns.append("the order routes the Mast by form copy, not through the awards processing system; if the command now uses iAPS, cite Overrides/meritorious-mast.md")
        if product == "CC":
            if not re.search(r"NAVMC 10631\b", rt):
                fails.append("routing does not name the form: NAVMC 10631 original to the Marine (enclosure (1) 9.a)")
            if not re.search(r"10631A|green copy|record (?:file )?copy", rt):
                fails.append("routing does not name the record copy: NAVMC 10631A green copy to CMC (MMSB) for the OMPF (enclosure (1) 9.a)")
            if not re.search(r"HQMC APS|1650 ?\(EF\)", rt):
                warns.append("say that the certificate is not submitted via the HQMC APS and needs no 1650 (EF) (8.f(2))")
            elif not negated(rt, r"HQMC APS|1650 ?\(EF\)"):
                fails.append("routing submits the certificate through the HQMC APS or on a 1650 (EF); 8.f(2): these awards will not be submitted via the HQMC APS and do not require a 1650 (EF)")
            if re.search(r"\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b", rt):
                fails.append("a social security number in the routing; it is added to the green copy on the user's computer, never in the draft")
        if not re.search(r"presence of Marines|formation|ceremony", rt, re.I):
            warns.append("no presentation line; enclosure (1) 5.a: as soon as practical, with ceremony, in the presence of Marines")

    if re.search(UNIT_NAME, text):
        fails.append(f"a unit is named ('{re.search(UNIT_NAME, text).group(0)}'); the unit by echelon until substitution on the user's computer")
    scrub = re.sub(r"<MARINE>", "", text)
    mm = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]{2,}\b", scrub)
    if mm and not re.search(r"^(?:Sergeant Major|First Sergeant|Master Gunnery Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|Lance Corporal|Private First Class|Lieutenant Colonel|Brigadier General|Major General|Corporal|Sergeant|Colonel|Major|Captain) (?:Major|Sergeant|General|Corporal|Colonel|Class|Commander|Officer)$", mm.group(0)):
        fails.append(f"a name appears ('{mm.group(0)}'); <MARINE> until substitution on the user's computer")
    for p in LIFTED:
        if p.lower() in text.lower():
            fails.append(f"lifted from the exemplar or voice file: '{p}'; the example teaches shape, the intake supplies facts")
    for b in blocked_hits(head + "\n" + (lvl or "") + "\n" + (facts or "") + "\n" + (rt or "")):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")

    print(f"MERITORIOUS MAST CHECK: {sys.argv[1]}  {tm.group(1) if tm else 'no product'}  level check: {named or 'none'}")
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
