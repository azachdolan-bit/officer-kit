#!/usr/bin/env python3
"""The structure pass: find the sentences that do not say what the writer meant.

Usage:  python3 precision_check.py <draft.md|draft.txt> [--directive] [--target-words N]

  --directive     the document tells someone to do something (an order, a Page 11 entry, a range
                  order, a counseling plan, an SOP). Ambiguity that changes what the reader must do
                  becomes a failure instead of a warning.
  --target-words  average sentence length target, default 15 (AR 25-50 para 1-37b).

Exit 0 = passes (warnings allowed); 1 = ambiguity that changes what the reader must do, in a
directive document.

What it finds, and why each one is here:
  center embedding      the measured cause of difficulty in professional prose: a long clause
                        wedged between a subject and its verb
  sentence length       AR 25-50: "understood by the reader in a single rapid reading"; average
                        sentence about 15 words
  long paragraphs       AR 25-50 para 1-37b: no more than 10 lines
  soft quantifiers      "several", "significant", "as required": the reader cannot comply with them
  actorless directives  "will be conducted" by whom
  hidden verbs          "conduct an inspection of" for "inspect"
  mixed modals          must / will / should used interchangeably for requirements
  loose pronouns        a sentence opening with This/These/It/They and no noun
  undefined acronyms    first use with no expansion
  and/or                permits three readings
  vague deadlines       "as soon as possible" is not a time

Prescribed text (an order's own entry wording, a citation's standard opening and closing) is not
the writer's to fix. Put it between lines reading  <!-- prescribed -->  and  <!-- /prescribed -->
and this script skips it.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SOFT = [
    "several", "many", "numerous", "various", "a number of", "significant", "significantly",
    "substantial", "some", "most", "frequently", "regularly", "periodically", "as required",
    "as necessary", "as appropriate", "in a timely manner", "adequate", "adequately", "sufficient",
    "minimal", "the majority of", "a variety of", "multiple", "routinely", "on a regular basis",
]
VAGUE_DEADLINE = r"\b(?:as soon as possible|asap|at the earliest|expeditiously|in the near future|shortly|in due course)\b"
MODALS = ("must", "shall", "will", "should", "may")
HIDDEN_VERB = r"\b(?:conduct|performance|perform|provide|provision|make|give|take|carry out|effect|undertake)\s+(?:of\s+)?(?:an?\s+|the\s+)?(\w+(?:tion|ment|ance|ence|sion|ing))\b"
ACRONYM = r"\b([A-Z]{2,6}(?:-[A-Z0-9]{1,4})?)\b"
KNOWN = {
    "USMC", "MOS", "NCO", "SNCO", "OIC", "RSO", "PFT", "CFT", "UCMJ", "CO", "XO", "SOP", "MCO",
    "NAVMC", "SECNAV", "OPORD", "FRAGO", "AAR", "RAW", "RAC", "EAP", "ECP", "TCCC", "MEDEVAC",
    "CBRN", "MCTIMS", "DRRS", "PII", "CUI", "SJA", "JAGMAN", "IG", "IGMC", "MARADMIN", "ALMAR",
    "TBS", "EWS", "PME", "MCMAP", "TIS", "TIG", "EAS", "ECC", "POC", "HHQ", "METL", "MCPP", "MEF",
    "AM", "PM", "US", "DOD", "DON", "I", "A", "II", "III", "IV", "V", "VI", "AND", "OR", "THE",
    "NLT", "NMT", "SP", "LD", "TBD", "ID", "DODIC", "NSN", "SSN", "EDIPI", "MCTFS", "MOL", "DTS",
}
FINITE = r"(?:is|are|was|were|has|have|had|will|shall|must|should|may|can|does|do|did|remains?|becomes?|provides?|requires?|ensures?|reflects?|serves?|carries|carry|\w+(?:s|ed))\b"


def sentences(text):
    out = []
    for para_i, para in enumerate(text.split("\n\n")):
        body = " ".join(l for l in para.splitlines() if not l.strip().startswith(("#", "|", "-", "*", ">")) or len(l.split()) > 6)
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z(])", body):
            s = s.strip()
            if len(s.split()) >= 3 and not s.startswith(("|", "#")):
                out.append((para_i, s))
    return out


def strip_prescribed(text):
    return re.sub(r"<!--\s*prescribed\s*-->.*?<!--\s*/prescribed\s*-->", "", text, flags=re.S | re.I)


def center_embedded(s):
    """A long clause between two commas, followed by a finite verb: the subject and its verb are split."""
    m = re.match(r"^([A-Z][^,]{2,60}),\s+([^,]{35,}),\s+(" + FINITE + r")", s)
    if m and len(m.group(2).split()) >= 8:
        return m.group(2)
    return None


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    directive = "--directive" in sys.argv
    target = int(sys.argv[sys.argv.index("--target-words") + 1]) if "--target-words" in sys.argv else 15
    raw = open(path, encoding="utf-8").read()
    text = strip_prescribed(raw)
    fails, warns = [], []
    sents = sentences(text)
    if not sents:
        print(f"PRECISION CHECK: {path}\n  no prose sentences found")
        return 0

    lengths = [len(s.split()) for _, s in sents]
    avg = sum(lengths) / len(lengths)

    for _, s in sents:
        short = s[:64] + ("..." if len(s) > 64 else "")
        n = len(s.split())
        if n > 40:
            warns.append(f"{n} words, two or three sentences wearing one coat: {short}")
        elif n > 25:
            warns.append(f"{n} words against a {target} word target: {short}")
        ce = center_embedded(s)
        if ce:
            warns.append(f"center embedded clause ({len(ce.split())} words) splits the subject from its verb: {short}")
        low = s.lower()
        soft = [w for w in SOFT if re.search(r"\b" + re.escape(w) + r"\b", low)]
        if soft:
            has_number = bool(re.search(r"\d", s))
            msg = f"soft quantifier {', '.join(repr(w) for w in soft)}{' beside a number, so say which' if has_number else ''}: {short}"
            (fails if directive and not has_number else warns).append(msg)
        if re.search(r"\b(?:will|shall|is to|are to)\s+be\s+\w+(?:ed|en)\b", s) and not re.search(r"\bby\s+(?:the\s+)?[A-Za-z]", s):
            (fails if directive else warns).append(f"directive in the passive with no actor: {short}")
        m = re.search(HIDDEN_VERB, s, re.I)
        if m:
            warns.append(f"hidden verb '{m.group(0)}': {short}")
        if re.search(VAGUE_DEADLINE, s, re.I):
            (fails if directive else warns).append(f"vague deadline: {short}")
        if re.search(r"\band/or\b", s, re.I):
            (fails if directive else warns).append(f"'and/or' permits three readings; say which: {short}")
        if re.match(r"^(This|These|Those|That|It|They)\s+(" + FINITE + r")", s):
            warns.append(f"opens with a pronoun and no noun; the reader has to guess the antecedent: {short}")

    if directive:
        used = {m for m in MODALS if re.search(r"\b" + m + r"\b", text, re.I)}
        req = used & {"must", "shall", "will"}
        if len(req) > 1 and "should" in used:
            warns.append(f"mixed modals for requirements ({', '.join(sorted(used))}); pick one for what is required and use 'may' only for what is optional")

    seen = set()
    for m in re.finditer(ACRONYM, text):
        a = m.group(1)
        if a in KNOWN or a in seen or a.isdigit():
            continue
        seen.add(a)
        expanded = re.search(r"\(\s*" + re.escape(a) + r"\s*\)", text) or re.search(re.escape(a) + r"\s*\([A-Za-z][^)]{6,}\)", text)
        if not expanded:
            warns.append(f"acronym '{a}' never expanded")

    for i, para in enumerate(text.split("\n\n")):
        lines = [l for l in para.splitlines() if l.strip()]
        if len(lines) > 10 and not any(l.strip().startswith(("|", "-", "*", "#")) for l in lines):
            warns.append(f"paragraph {i + 1} runs {len(lines)} lines against a 10 line limit")

    print(f"PRECISION CHECK: {path}  {len(sents)} sentences, average {avg:.1f} words (target {target}){', directive' if directive else ''}")
    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    if not warns and not fails:
        print("  clean")
    print(f"  -> {len(fails)} failures, {len(warns)} warnings")
    if avg > target + 8:
        print(f"  NOTE  the average sentence is {avg:.1f} words; AR 25-50 asks for about {target}, and the standard it serves is one rapid reading")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
