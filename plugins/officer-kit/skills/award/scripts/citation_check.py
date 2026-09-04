#!/usr/bin/env python3
"""Mechanical check of an award citation against MCO 1650.19J enclosure (4) and (5) format rules.

Usage:  python3 citation_check.py citation.txt --level NA|NC|MM
Exit 0 = within limits (warnings allowed), 1 = a limit or capitalization failure.

NA and NC: all capital letters, Times New Roman 9 point, landscape, nine lines, 1200 characters
           (the order also states 1250 in enclosure (5); 1200 is used here).
MM:        regular capitalization, Times New Roman 12 point, portrait, 24 lines.
Also checks for an opening sentence ("For ...") and a closing sentence naming the Marine Corps
and the Naval Service, and warns on abbreviations.
"""
import re
import sys

LIMITS = {"NA": (1200, 9, True), "NC": (1200, 9, True), "MM": (None, 24, False)}
CHARS_PER_LINE_LANDSCAPE_9PT = 150   # rough estimate for Times New Roman 9 on a landscape line; the printed certificate is the authority


def main():
    if len(sys.argv) < 4 or "--level" not in sys.argv:
        sys.exit(__doc__)
    path = sys.argv[1]
    level = sys.argv[sys.argv.index("--level") + 1].upper()
    if level not in LIMITS:
        sys.exit("level must be NA, NC, or MM")
    text = open(path, encoding="utf-8").read().strip()
    max_chars, max_lines, caps = LIMITS[level]
    fails, warns = [], []

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
    if re.search(r"\b[A-Z]{2,}[0-9]*\b", text) and caps:
        pass  # everything is caps; abbreviation scan below uses the lowercase copy if given
    abbr = set(re.findall(r"\b(?:NCOIC|SNCOIC|OIC|MOS|TAD|BN|CO|PLT|SQD|MEU|MAGTF|FMF|SOP|OPORD|PT|CFT|PFT)\b", text))
    if abbr:
        warns.append(f"abbreviations a reader outside the unit may not know: {', '.join(sorted(abbr))}")
    if "—" in text or "–" in text:
        fails.append("em or en dash present")

    print(f"CITATION CHECK: {path}  level {level}")
    print(f"  {n} characters, {lines_given} line breaks, about {lines_est} printed lines" + (f" (limit {max_chars} characters, {max_lines} lines)" if max_chars else f" (limit {max_lines} lines)"))
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
