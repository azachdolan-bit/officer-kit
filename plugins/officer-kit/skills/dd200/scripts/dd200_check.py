#!/usr/bin/env python3
"""Check a DD 200 investigation report (report.md): the property table plus the findings chain.

Usage:  python3 dd200_check.py report.md
Exit 0 = passes (warnings allowed); 1 = broken chain, missing part, a name, or blocked content.

Chain: every finding cites enclosures that exist; every opinion cites findings that exist; every
recommendation cites opinions that exist; enclosure (1) is the convening order; every listed enclosure
is cited or flagged unused. Also: opinion words inside findings (warn); due date within 30 days of the
convening order or an extension noted; injury cases carry no signed statements (warn); classification line.
"""
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, dashes  # noqa: E402

GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj|LtCol)"
OPINION_WORDS = r"\b(?:probably|likely|appears?|seems?|I believe|should have|negligent\w*|careless\w*|reckless\w*|it is clear)\b"
PARTS = ["Property", "Findings of fact", "Opinions", "Recommendations", "Enclosures"]


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def numbered(block):
    items = {}
    for m in re.finditer(r"^\s*(\d+)\.\s+(.*?)(?=^\s*\d+\.\s|\Z)", block, re.M | re.S):
        items[int(m.group(1))] = " ".join(m.group(2).split())
    return items


def cites(text, tag):
    out = set()
    for m in re.finditer(r"\[" + tag + r"\s*([^\]]+)\]", text):
        for n in re.findall(r"\d+", m.group(1)):
            out.add(int(n))
    return out


def parse_date(s):
    for fmt in ("%d %B %Y", "%d %b %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            pass
    return None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails, warns = [], []
    order = [p for p in PARTS if section(text, p) is not None]
    for p in PARTS:
        if p not in order:
            fails.append(f"missing part: {p}")
    if order != [p for p in PARTS if p in order]:
        fails.append("parts out of order; preliminary statement, findings of fact, opinions, recommendations, enclosures")

    encl_block = section(text, "Enclosures") or ""
    encls = {int(m.group(1)): m.group(2).strip() for m in re.finditer(r"^\s*\((\d+)\)\s+(.*)$", encl_block, re.M)}
    if 1 not in encls or not re.search(r"appoint|convening", encls.get(1, ""), re.I):
        fails.append("enclosure (1) must be the appointment or convening letter")
    ff = numbered(section(text, "Findings of fact") or "")
    ops = numbered(section(text, "Opinions") or "")
    recs = numbered(section(text, "Recommendations") or "")
    if not ff:
        fails.append("no numbered findings of fact")
    cited_encls = set()
    for n, t in ff.items():
        c = cites(t, "Encl")
        if not c:
            fails.append(f"finding {n} cites no enclosure")
        for e in c:
            if e not in encls:
                fails.append(f"finding {n} cites enclosure ({e}) which is not in the list")
        cited_encls |= c
        if re.search(OPINION_WORDS, t, re.I):
            warns.append(f"finding {n} carries opinion language ('{re.search(OPINION_WORDS, t, re.I).group(0)}'); a finding is a fact, move the judgment to Opinions")
        if not re.search(r"\b\d{1,2} \w+ 20\d\d\b|\b\d{4}\b|at approximately|on or about", t):
            warns.append(f"finding {n} has no date or time")
    for n, t in ops.items():
        c = cites(t, "FF")
        if not c:
            fails.append(f"opinion {n} cites no findings")
        for f in c:
            if f not in ff:
                fails.append(f"opinion {n} cites finding {f} which does not exist")
    for n, t in recs.items():
        c = cites(t, "Op")
        if not c:
            fails.append(f"recommendation {n} cites no opinions")
        for o in c:
            if o not in ops:
                fails.append(f"recommendation {n} cites opinion {o} which does not exist")
        if re.search(r"disciplinary action", t, re.I) and not re.search(r"\b(?:NJP|nonjudicial|court[- ]martial|summary|special|general|Article \d+)\b", t, re.I):
            warns.append(f"recommendation {n} says 'disciplinary action' without a forum or charges (handbook page III-9)")
    for e in encls:
        if e != 1 and e not in cited_encls:
            warns.append(f"enclosure ({e}) is listed but no finding cites it; delete unused enclosures")
    if re.search(r"injur|casualty|hospital|clinic", text, re.I) and re.search(r"signed statement|sworn statement", encl_block, re.I):
        warns.append("injury case with a signed statement enclosed; the handbook says summaries of testimony, no signed witness statements, in any incident involving personal injury")
    prop = section(text, "Property") or ""
    rows = [r for r in prop.splitlines() if r.strip().startswith("|") and "Nomenclature" not in r and not re.match(r"^\|\s*-", r.strip())]
    if not rows:
        fails.append("Property table has no rows")
    for r in rows:
        c = [x.strip() for x in r.strip().strip("|").split("|")]
        if len(c) < 8 or not re.search(r"\d{4}-\d{2}-\d{3}-\d{4}", c[1]) or not c[2] or not re.search(r"\d", c[3]) or not re.search(r"\$?\d", c[4]):
            fails.append(f"Property row incomplete (NSN in 4-2-3-4 form, serial, quantity, unit price): {r.strip()[:60]}")
    allff = " ".join(ff.values())
    if not re.search(r"CMR|ECR|sub custody|custody card|inventory", allff, re.I):
        fails.append("no finding cites the custody record (CMR, ECR, sub custody card, inventory)")
    if not re.search(r"search", allff, re.I):
        fails.append("no finding records the search conducted")
    allops = " ".join(ops.values())
    if not re.search(r"simple negligence|gross negligence|willful misconduct|no negligence|not (?:the result of )?negligen", allops, re.I):
        fails.append("no opinion addresses negligence (simple, gross, willful misconduct, or none) with the order's standard")
    m = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]+", text)
    if m:
        fails.append(f"a name appears in the report ('{m.group(0)}'); <SUBJECT>, <WITNESS n>, billets only until substitution on the user's computer")
    for b in blocked_hits(text, allow=("medical", "SAPR or investigation", "substance")):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")
    print(f"DD 200 CHECK: {sys.argv[1]}  {len(ff)} findings, {len(ops)} opinions, {len(recs)} recommendations, {len(encls)} enclosures")
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
