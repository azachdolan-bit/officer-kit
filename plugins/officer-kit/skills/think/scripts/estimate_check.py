#!/usr/bin/env python3
"""Check an estimate before the drafting starts.

Usage:  python3 estimate_check.py estimate.md [--tier deliberate|rapid|running]

Exit 0 = passes (warnings allowed); 1 = a missing item, an untested assumption, or a question that
carries its own answer.

What it enforces, and why:
  the tier line          the tool has to say which tier it is running and what triggered it
  facts and assumptions  separate sections; an assumption sitting in the facts list is the failure
                         this whole thing exists to catch
  four questions         MCWP 5-10: logical, realistic, essential to continue, and does it assume
                         away the thing most likely to defeat this
  falsifier              what would turn this assumption into a fact
  consequence            what breaks if it is false; if the product changes, it is a question
  questions that change  every question states what its answer changes; a question that changes
                         nothing is not asked
  clean questions        a question that contains a candidate answer produces that answer
  scope                  what this will not do
  checked by             which check runs, and what nothing can check
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, dashes  # noqa: E402

SECTIONS = {
    "task": r"^##\s*(?:1\.\s*)?Task",
    "standard": r"^##\s*(?:2\.\s*)?Standard",
    "facts": r"^##\s*(?:3\.\s*)?Facts",
    "assumptions": r"^##\s*(?:3\.\s*)?Assumptions",
    "questions": r"^##\s*(?:4\.\s*)?Questions",
    "scope": r"^##\s*(?:5\.\s*)?(?:Will not|Out of scope|Scope)",
    "checked": r"^##\s*(?:6\.\s*)?Checked",
}
FALSIFIER = r"\b(?:becomes a fact|confirmed by|verified by|resolved by|turns into a fact|would make it a fact|fact when|from the (?:roster|record|order|log|training record))\b"
CONSEQUENCE = r"\b(?:if false|if it is false|if that is wrong|if this fails|breaks|collapses|nothing changes|the (?:sheet|product|package|draft) cannot|changes the)\b"
LEADING = [
    (r"\b(?:right|correct|yes)\?\s*$", "ends by inviting agreement"),
    (r"\b(?:don't you|doesn't it|isn't it|wouldn't it|shouldn't it|didn't you)\b", "tag question"),
    (r"\b(?:around|about|roughly|approximately)\s+\d+.*\?", "supplies the number it is asking for"),
    (r"\bI assume\b.*\?", "states the answer before asking"),
    (r"\b(?:was it|is it|were they)\s+(?:good|bad|successful|effective|significant|serious)\b", "supplies the evaluation"),
]


def section(text, key):
    pat = SECTIONS[key]
    m = re.search(pat + r"[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def bullets(block):
    return [l.strip().lstrip("-*").strip() for l in (block or "").splitlines()
            if l.strip().startswith(("-", "*")) or re.match(r"^\s*\d+[.)]\s", l)]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read()
    tier = None
    m = re.search(r"\bTier:\s*(deliberate|rapid|running)", text, re.I)
    if m:
        tier = m.group(1).lower()
    if "--tier" in sys.argv:
        tier = sys.argv[sys.argv.index("--tier") + 1].lower()
    fails, warns = [], []

    if not m:
        fails.append("no 'Tier:' line; the tool says which tier it is running and what triggered it")
    elif not re.search(r"Tier:\s*\w+[^\n]{8,}", text, re.I):
        warns.append("the tier line names a tier but not the trigger that set it")
    tier = tier or "deliberate"

    required = ["task", "standard", "assumptions", "questions"]
    if tier == "deliberate":
        required += ["facts", "scope", "checked"]
    for key in required:
        if section(text, key) is None:
            fails.append(f"missing section: {key}")

    facts = section(text, "facts")
    if facts and re.search(r"\bassum\w+", facts, re.I):
        fails.append("an assumption is sitting in the facts section; facts carry sources, assumptions carry a falsifier")
    if facts and not re.search(r"\bfrom (?:the )?\w|\(.*\)|per \w", facts):
        warns.append("facts with no sources named")

    assumptions = bullets(section(text, "assumptions"))
    if not assumptions and section(text, "assumptions") and len(section(text, "assumptions").split()) > 12:
        assumptions = [s.strip() for s in re.split(r"(?<=[.])\s+", section(text, "assumptions")) if len(s.split()) > 6]
    if not assumptions:
        warns.append("no assumptions listed; a product with none is rare, and saying so explicitly is the honest version")
    for a in assumptions:
        short = a[:56] + ("..." if len(a) > 56 else "")
        if not re.search(FALSIFIER, a, re.I):
            fails.append(f"assumption with no falsifier (what would make it a fact): {short}")
        if not re.search(CONSEQUENCE, a, re.I):
            fails.append(f"assumption with no consequence (what breaks if it is false): {short}")
    if tier == "deliberate" and len(assumptions) > 6:
        warns.append(f"{len(assumptions)} assumptions; the key assumptions check ends by deleting everything that is not load bearing, and a list this long is an inventory rather than a warning")

    questions = bullets(section(text, "questions"))
    if not questions and section(text, "questions"):
        questions = [q.strip() for q in re.findall(r"[^.?!]*\?", section(text, "questions")) if len(q.split()) > 3]
    for q in questions:
        short = q[:56] + ("..." if len(q) > 56 else "")
        if not re.search(r"\bchanges\b|\bdecides\b|\bdetermines\b|\bsets\b", q, re.I):
            fails.append(f"question with no statement of what its answer changes: {short}")
        for pat, why in LEADING:
            if re.search(pat, q, re.I):
                fails.append(f"leading question ({why}): {short}")
                break
        if re.match(r"^\s*(?:is|are|was|were|do|does|did|can|will|should|would|have|has)\b", q, re.I) and not re.search(r"\bconfirmed\b|\bon disk\b|\bpublish\w*\b", q, re.I):
            warns.append(f"yes or no question where a number, a name, or a date is probably wanted: {short}")
    if tier == "deliberate" and not questions:
        warns.append("no questions; either the task was fully specified, which is rare, or the underspecification pass did not run")

    checked = section(text, "checked")
    if checked and not re.search(r"\bcannot\b|\bnothing\b|\bnot check\w*\b|\bno (?:check|way)\b", checked, re.I):
        warns.append("the checked by section does not say what cannot be checked mechanically, which is the half the signer needs")

    for b in blocked_hits(text, allow=("medical", "SAPR or investigation", "substance", "financial")):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")

    print(f"ESTIMATE CHECK: {path}  tier {tier}, {len(assumptions)} assumptions, {len(questions)} questions")
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
