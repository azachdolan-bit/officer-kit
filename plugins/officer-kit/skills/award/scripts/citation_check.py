#!/usr/bin/env python3
"""Mechanical check of an award citation against MCO 1650.19J enclosure (4) and (5) format rules,
and of the citation against the Summary of Action it must agree with.

Usage:  python3 citation_check.py citation.txt --level NA|NC|MM [--soa SOA.md]
Exit 0 = within limits (warnings allowed), 1 = a limit, capitalization, or SOA agreement failure.

NA and NC: all capital letters, Times New Roman 10, landscape, fully justified, one inch margins,
           8 lines, 1,250 characters, no acronyms. Source: SECNAV M-1650.1 (2019) Appendix 2E Table 20 as
           carried by HQBN TECOM's personal awards guide, USNAINST 1650.5D (2020), and CNLSCINST 1650.2B (2024).
           MCO 1650.19J (2001) said 9 lines and Times New Roman 9; the 2019 manual superseded that.
MM:        regular capitalization, Times New Roman 12 point, portrait, 24 lines.
Also checks for an opening sentence ("For ...") and a closing sentence naming the Marine Corps
and the Naval Service, warns on abbreviations and on words that do the work facts should do,
and with --soa fails if a number in the citation does not appear in the SOA
(the 2018 lesson: a citation said $2,820 where the SOA said $2,887.38, and it was signed that way).
"""
import re
import sys

LIMITS = {"NA": (1250, 8, True), "NC": (1250, 8, True), "MM": (None, 24, False)}
CHARS_PER_LINE_LANDSCAPE_9PT = 160   # rough estimate for Times New Roman 10 justified on a 9 inch landscape line; the printed certificate is the authority

FLUFF = [
    "enthusiastically", "exceptional", "exceptionally", "outstanding", "superb", "phenomenal",
    "epitome", "epitomizes", "go to", "go-to", "take charge", "above and beyond", "herculean",
    "unmatched", "unparalleled", "level headed", "level-headed", "tireless", "invaluable",
    "instrumental", "pivotal", "vital",
]
WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15, "twenty": 20, "thirty": 30,
    "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100,
}


def numbers_in(text):
    """Every number in the text, normalized: digits with commas and decimals, plus spelled out small numbers."""
    found = set()
    for m in re.findall(r"\$?\d[\d,]*(?:\.\d+)?", text):
        found.add(m.replace("$", "").replace(",", ""))
    for w in re.findall(r"[A-Za-z\-]+", text.lower()):
        if w in WORD_NUMBERS:
            found.add(str(WORD_NUMBERS[w]))
    return found


def main():
    if len(sys.argv) < 4 or "--level" not in sys.argv:
        sys.exit(__doc__)
    path = sys.argv[1]
    level = sys.argv[sys.argv.index("--level") + 1].upper()
    if level not in LIMITS:
        sys.exit("level must be NA, NC, or MM")
    soa_path = sys.argv[sys.argv.index("--soa") + 1] if "--soa" in sys.argv else None
    text = open(path, encoding="utf-8").read().strip()
    max_chars, max_lines, caps = LIMITS[level]
    fails, warns, notes = [], [], []

    n = len(text)
    lines_given = len([l for l in text.splitlines() if l.strip()])
    lines_est = max(lines_given, -(-n // CHARS_PER_LINE_LANDSCAPE_9PT)) if caps else lines_given
    if max_chars and n > max_chars:
        fails.append(f"{n} characters; limit {max_chars}")
    if lines_est > max_lines:
        fails.append(f"about {lines_est} lines; limit {max_lines}")
    if caps and text != text.upper():
        fails.append("NA and NC citations are typed in all capital letters")
    if not caps and text == text.upper():
        warns.append("MM citations use regular capitalization")
    if not re.match(r"^\s*FOR\b", text, re.I):
        warns.append("no opening sentence beginning 'For ...' (take the standard opening from SECNAV M-1650.1 Appendix 2E Table 21)")
    if not re.search(r"MARINE CORPS", text, re.I) or not re.search(r"NAVAL SERVICE", text, re.I):
        warns.append("closing sentence should name the Marine Corps and the United States Naval Service per the manual's standard closing")
    abbr = set(re.findall(r"\b(?:NCOIC|SNCOIC|OIC|MOS|TAD|BN|CO|PLT|SQD|MEU|MAGTF|FMF|SOP|OPORD|PT|CFT|PFT)\b", text))
    if abbr:
        warns.append(f"abbreviations a reader outside the unit may not know: {', '.join(sorted(abbr))}")
    if "—" in text or "–" in text:
        fails.append("em or en dash present")
    if ";" in text:
        warns.append("semicolon in a citation; one claim per sentence")
    low = text.lower()
    fluff = [w for w in FLUFF if re.search(r"\b" + re.escape(w) + r"\b", low)]
    if fluff:
        warns.append(f"words doing the work facts should do: {', '.join(fluff)} (delete each; if the sentence loses no fact, it was fluff)")

    body = re.sub(r"^\s*FOR\b.*?\.\s", "", text, count=1, flags=re.I | re.S)
    if not re.search(r"\d", body):
        warns.append("no number after the opening sentence; every strong sentence in an approved citation carries one")

    if soa_path:
        soa = open(soa_path, encoding="utf-8").read()
        cite_nums = numbers_in(text)
        soa_nums = numbers_in(soa)
        missing = sorted(cite_nums - soa_nums, key=lambda s: (len(s), s))
        # years in the opening line are dates, not claims; still required to agree, but reported separately
        if missing:
            fails.append(f"numbers in the citation not found in the SOA: {', '.join(missing)} (the citation carries nothing the SOA does not prove)")
        else:
            notes.append(f"SOA agreement: all {len(cite_nums)} numbers in the citation appear in {soa_path}")

    print(f"CITATION CHECK: {path}  level {level}")
    print(f"  {n} characters, {lines_given} line breaks, about {lines_est} printed lines" + (f" (limit {max_chars} characters, {max_lines} lines)" if max_chars else f" (limit {max_lines} lines)"))
    for m in notes:
        print(f"  {m}")
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
