"""Shared checks for the enlisted support tools. Copied into each tool's scripts folder so every skill stays self contained."""
import re

STRIKE = [
    "enthusiastically", "exceptional", "exceptionally", "outstanding", "superb", "phenomenal",
    "epitome", "epitomizes", "go to", "go-to", "take charge", "above and beyond", "herculean",
    "unmatched", "unparalleled", "level headed", "level-headed", "tireless", "invaluable",
    "instrumental", "pivotal", "vital", "above reproach", "heart and soul", "face of the",
    "without a doubt", "truly", "utmost",
]

# Content that never belongs in a product that goes in another Marine's record or before a board.
BLOCKED = {
    "SSN pattern": r"\b\d{3}-\d{2}-\d{4}\b",
    "EDIPI or ten digit id": r"\b\d{10}\b",
    "medical": r"\b(?:medical|diagnos\w*|injur\w*|surgery|pregnan\w*|mental health|therap\w*|counsel(?:ing|or) center|medication|PTSD|TBI|LIMDU|limited duty)\b",
    "SAPR or investigation": r"\b(?:SAPR (?:report|case|incident|complaint|referral)|(?:un)?restricted report|sexual (?:assault|harassment|misconduct)|harass(?:ment|ed|ing)|NJP|court[- ]martial|under investigation|investigated for|EO complaint|CID|NCIS)\b",
    "family or personal": r"\b(?:divorce\w*|child custody|custody (?:battle|dispute|of (?:his|her|their) (?:child|kids|son|daughter))|spouse|wife|husband|girlfriend|boyfriend|marriage|marital|family (?:problem|situation|issue)\w*|personal (?:problem|situation|issue)s?|hardship|single parent)\b",
    "financial": r"\b(?:debt|bankrupt\w*|garnish\w*|credit score|financial (?:trouble|problem|hardship))\b",
    "substance": r"\b(?:alcohol|DUI|DWI|drug|substance)\b",
}

def strike_hits(text):
    low = text.lower()
    return [w for w in STRIKE if re.search(r"\b" + re.escape(w) + r"\b", low)]

def blocked_hits(text, allow=()):
    hits = []
    for name, pat in BLOCKED.items():
        if name in allow:
            continue
        m = re.search(pat, text, re.I)
        if m:
            hits.append(f"{name} ('{m.group(0)}')")
    return hits

def numbers(text):
    return re.findall(r"\$?\d[\d,]*(?:\.\d+)?%?", text)

def dashes(text):
    return "—" in text or "–" in text

def words(text):
    return len(re.findall(r"\S+", text))
