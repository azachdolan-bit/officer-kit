#!/usr/bin/env python3
"""Check a risk-assessment draft. TODO: describe the checks.

Usage:  python3 risk_assessment_check.py <draft.md>
Exit 0 = passes (warnings allowed); 1 = structural failure or blocked content.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, numbers, dashes, words  # noqa: E402

REQUIRED_HEADINGS = []  # TODO: e.g. ["## Situation", "## Mission"]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails, warns = [], []
    for h in REQUIRED_HEADINGS:
        if h not in text:
            fails.append(f"missing: {h}")
    if not numbers(text):
        warns.append("no numbers anywhere; a product without a number is a characterization")
    for w in strike_hits(text):
        warns.append(f"strike list: '{w}'")
    for b in blocked_hits(text):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")
    print(f"RISK_ASSESSMENT CHECK: {sys.argv[1]}  {words(text)} words")
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
