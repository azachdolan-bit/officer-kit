#!/usr/bin/env python3
"""Completeness report for a captured source (markdown).

Reports chapter inventory and words per chapter, flags empty or thin chapters,
consecutive duplicate blocks (a paste that ran twice), and headings that follow a
list (platforms that print a block's title after its body).

Usage:  python3 capture_check.py capture.md [--min-words 40]
Exit 0 = nothing blocking, 1 = an empty chapter or a duplicate block.
"""
import re
import sys

THIN_DEFAULT = 40


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    thin = THIN_DEFAULT
    if "--min-words" in sys.argv:
        thin = int(sys.argv[sys.argv.index("--min-words") + 1])
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()

    # chapters: level 2 headings
    chapters = []
    cur = None
    for i, ln in enumerate(lines):
        m = re.match(r"^##\s+(.+)", ln)
        if m and not ln.startswith("###"):
            cur = {"title": m.group(1).strip(), "start": i, "body": []}
            chapters.append(cur)
        elif cur is not None:
            cur["body"].append(ln)

    blocking = 0
    print(f"CAPTURE CHECK: {path}")
    print(f"  chapters: {len(chapters)}   total words: {len(text.split())}")
    for c in chapters:
        words = len(" ".join(c["body"]).split())
        flag = ""
        if words == 0:
            flag = "  EMPTY"
            blocking += 1
        elif words < thin:
            flag = f"  thin (<{thin})"
        print(f"  {words:6d}  {c['title'][:70]}{flag}")

    # consecutive duplicate blocks (paragraph level, ignoring blanks)
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    dups = [(i, b) for i, b in enumerate(blocks[1:], start=1) if b == blocks[i - 1] and len(b) > 40]
    for i, b in dups:
        print(f"  DUPLICATE block {i}: {b[:60]!r}")
    blocking += len(dups)

    # headings that follow a list: possible title after content
    tac = 0
    for i in range(1, len(lines)):
        if re.match(r"^#{2,4}\s", lines[i]):
            j = i - 1
            while j >= 0 and not lines[j].strip():
                j -= 1
            if j >= 0 and re.match(r"^\s*([-*]|\d+[.)])\s", lines[j]):
                tac += 1
    if tac:
        print(f"  note: {tac} heading(s) directly follow a list; check whether the platform prints titles after content")

    if not chapters:
        print("  note: no '## ' chapter headings found; add one per chapter so coverage can be checked later")
    print(f"  -> {'blocking issues: ' + str(blocking) if blocking else 'nothing blocking'}")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
