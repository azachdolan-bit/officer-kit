#!/usr/bin/env python3
"""Structure check for a builder meant to be shared: does it carry every safeguard the method needs?

Usage: python3 builder_check.py <builder.md> [--app]

Checks, by the sections in references/builder-template.md:
  1. The opening says the file contains no course material, and tells the peer that what it builds
     is theirs and their own policy governs sharing it.
  2. Prerequisite: the peer's source is the only authority, no general knowledge, and with no
     source attached the builder stops and asks.
  3. Photographs (whenever the builder mentions photos): read the whole transcription back and wait
     for confirmation, mark anything unreadable and ask, keep handwriting separate from print.
  4. Extraction is exhaustive by category, in the source's own words.
  5. Verification re-derives every worked example and reports how many.
  6. Delivery names every gap rather than filling it.
  7. --app: the product carries an in page self test that drives the real input engine and reports 100 percent.
  8. No em or en dashes, and no mention of browser automation.
Exit 0 when every check passes, 1 otherwise."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leak_scan import MECHANISM

def sections(text):
    out, cur = {}, "_top"
    for line in text.splitlines():
        m = re.match(r"^#{1,3}\s+(.*)", line)
        if m:
            cur = m.group(1).strip().lower()
        out.setdefault(cur, []).append(line)
    return {k: "\n".join(v) for k, v in out.items()}

def find(secs, word):
    for k, v in secs.items():
        if word in k:
            return v
    return None

def check(text, app=False):
    res = []
    def ok(c, m):
        res.append((bool(c), m))
    head, sep, _ = text.partition("INSTRUCTIONS FOR CLAUDE")
    ok(sep, "has an INSTRUCTIONS FOR CLAUDE heading that separates the peer's part from Claude's")
    ok(re.search(r"contains no (?:course|unit|lesson|class)? ?(?:material|content)", head, re.I), "opening says the file contains no course material")
    ok(re.search(r"policy", head, re.I) and re.search(r"\byours\b|\byour own\b", head, re.I), "opening tells the peer the output is theirs and their own policy governs sharing it")
    s = sections(text)
    pre = find(s, "prerequisite")
    ok(pre, "has a Prerequisite section")
    pre = pre or ""
    ok(re.search(r"only authority", pre, re.I), "prerequisite: the peer's source is the only authority")
    ok(re.search(r"general knowledge", pre, re.I), "prerequisite: nothing from general knowledge")
    ok(re.search(r"no source[^.]*\.?[^.]*\b(stop|ask)", pre, re.I | re.S), "prerequisite: with no source attached, stop and ask")
    if re.search(r"photo", text, re.I):
        ph = find(s, "photo") or ""
        ok(ph, "mentions photos, so needs a Working from photographs section")
        ok(re.search(r"read[^.]*back", ph, re.I) and re.search(r"confirm", ph, re.I), "photographs: read the whole transcription back and wait for confirmation")
        ok(re.search(r"unreadable|illegible", ph, re.I), "photographs: mark anything unreadable and ask for a better photo")
        ok(re.search(r"handwrit", ph, re.I), "photographs: separate handwritten annotations from print")
    ex = find(s, "extract") or ""
    ok(ex, "has an Extract section")
    ok(re.search(r"\bevery\b|\ball\b", ex, re.I) and re.search(r"exactly as the source|verbatim|source's own words", ex, re.I), "extraction is exhaustive and in the source's own words")
    ve = find(s, "verif") or ""
    ok(ve, "has a Verify section")
    ok(re.search(r"worked example", ve, re.I) and re.search(r"how many|count", ve, re.I), "verification re-derives every worked example and reports how many")
    de = find(s, "deliver") or ""
    ok(de and re.search(r"\bgap", de, re.I), "delivery names every gap rather than filling it")
    if app:
        ok(re.search(r"self[- ]?test", text, re.I) and re.search(r"100", text), "app: an in page self test that drives the real input engine and reports 100 percent")
    ok(not re.search("[–—]", text), "no em or en dashes")
    ok(not any(re.search(p, text, re.I) for p in MECHANISM), "no mention of browser automation")
    return res

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    res = check(text, "--app" in sys.argv)
    for i, (c, m) in enumerate(res, 1):
        print("%2d. %s  %s" % (i, "PASS" if c else "FAIL", m))
    bad = sum(1 for c, _ in res if not c)
    print("-> %d of %d pass" % (len(res) - bad, len(res)))
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
