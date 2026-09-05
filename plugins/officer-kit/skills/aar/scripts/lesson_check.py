#!/usr/bin/env python3
"""Check a LEARNINGS.md queue for well formed entries.

Usage:  python3 lesson_check.py LEARNINGS.md
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits  # noqa: E402

HEAD = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s+([a-z0-9-]+)\s+(high|medium|low)\s+->\s+(overrides|exemplar|plugin)\s*$", re.M)
SOFTEN = re.compile(r"\b(?:skip the check|disable|turn off|remove the (?:check|gate|reviewer)|don't run|do not run|no need to verify|trust the)\b", re.I)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    fails, n = [], 0
    parts = HEAD.split(text)
    # parts: [pre, date, tool, conf, dest, body, date, tool, ...]
    for i in range(1, len(parts), 5):
        n += 1
        date, tool, conf, dest, body = parts[i:i + 5]
        for f in ("Evidence:", "Lesson:", "Status:"):
            if f not in body:
                fails.append(f"entry {date} {tool}: missing {f}")
        if not re.search(r"Status:\s*(?:pending|approved[^\n]*|rejected[^\n]*)", body):
            fails.append(f"entry {date} {tool}: status must be pending, approved <version>, or rejected <reason>")
        ev = re.search(r"Evidence:\s*(.*)", body)
        if ev and len(ev.group(1).strip()) < 15:
            fails.append(f"entry {date} {tool}: evidence line too thin")
        for b in blocked_hits(body):
            fails.append(f"entry {date} {tool}: blocked content: {b}")
        if SOFTEN.search(body) and conf != "low":
            fails.append(f"entry {date} {tool}: a lesson that softens a check must be recorded at confidence low")
    if n == 0:
        fails.append("no entries found; the heading form is '## YYYY-MM-DD  <tool>  <high|medium|low>  -> <overrides|exemplar|plugin>'")
    print(f"LESSON CHECK: {sys.argv[1]}  {n} entries")
    for f in fails:
        print(f"  FAIL  {f}")
    if not fails:
        print("  clean")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
