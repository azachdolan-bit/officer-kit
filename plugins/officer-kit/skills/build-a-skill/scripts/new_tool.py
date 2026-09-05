#!/usr/bin/env python3
"""Scaffold a new Officer Kit tool in the seven part shape.

Usage:  python3 new_tool.py <tool-name> "<one line: what the product is>" [--out <skills dir>]

Writes skills/<tool-name>/ with SKILL.md, references/standard.md, references/intake.md,
references/voice.md, references/exemplar.md, scripts/<tool>_check.py (with common_checks.py),
and evals/<tool-name>/cases.json beside the skills dir. Every file carries TODO markers where
the builder must supply the governing publication's text, the questions, and a fictional exemplar.
The scaffold is the shape; the substance comes from the order and from the user's own exemplars.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SKILL = '''---
name: {name}
description: >
  {what} TODO: finish this description in third person: what the tool produces, what it checks,
  and the phrases a user would say ("...", "...", "...").
metadata:
  version: "0.1.0"
---

# {title}

TODO: two or three sentences on what the product is for, who reads it, and what makes a good one in the reader's terms.

## Read first

1. `references/standard.md`: the governing publication's own words on this product (TODO: extract verbatim; cite the order, edition, and paragraph).
2. `references/intake.md`: the questions in the order a good reviewer asks them.
3. `references/voice.md`: the sentences the product uses, the verbs that carry facts, the words to strike.
4. `references/exemplar.md`: one fictional strong exemplar and one weak one, annotated.

## Your own material (read first, every time)

1. `Overrides/{name}.md` in the working folder, if it exists: the command's way wins over the defaults below. Say in one line what it changed.
2. `Reference/Exemplars/{name}/` in the working folder, if it has files: the user's own command's approved patterns beat the plugin's fictional exemplars.
3. The label. Another Marine's name never enters the session. Work on `<MARINE>` (grade and billet stay); the user runs `security-check/scripts/substitute.py` on the finished file on their own computer.
4. When something comes back with edits, tell the user `aar` will capture it.

## Workflow

```
{title}:
- [ ] 1. Frame: who reads it, what they decide, the deadline, the format the command uses
- [ ] 2. Intake from intake.md, one question at a time; "I do not know" is a gap, never filled
- [ ] 3. Climb the ladder on every vague note: action, scope, result, comparison, consequence; stop where the user can defend
- [ ] 4. Read back the fact list; user confirms; nothing else goes in
- [ ] 5. Draft in the product's shape (standard.md)
- [ ] 6. python3 scripts/{snake}_check.py <draft> exits 0
- [ ] 7. Strike pass with voice.md
- [ ] 8. Saved to <folder>/<label> {name} <date>; the user reads it against the standard
- [ ] 9. Learning: outcome and edits to LEARNINGS.md via aar
```

## Rules

- Never invent a number, a date, or a result. Ask.
- Nothing medical, family, financial, disciplinary, or from an investigation about a person; no identifiers. The checker scans.
- TODO: the two or three rules specific to this product that the standard imposes.

## Utility script

- `scripts/{snake}_check.py <draft>`: TODO: the mechanical checks (structure, required lines, numbers present, limits), plus the strike list and blocked content scan from common_checks.py. Exit 1 on a structural or blocked content failure.
'''

STANDARD = '''# Standard: TODO <publication number, title, edition date>

Verbatim extracts only. Each with its paragraph number. Nothing paraphrased.

## TODO: the product's required content
> (quote)

## TODO: format and length
> (quote)

## TODO: who approves, and the timeline
> (quote)
'''

INTAKE = '''# {title} intake

One question at a time. "I do not know" is recorded, never filled.

## 1. Frame
1. Who reads this and what do they decide from it?
2. When is it due and in what form?

## 2. What actually happened (or what is required)
3. TODO
4. TODO

## 3. Correlate to the standard
5. Hold the answers against standard.md. Say what reaches it, what does not, and what is missing.

## 4. Correlate to reality
6. Read back the fact list (item, number, period, source). The user confirms.

## 5. The reader
7. How does the approver read these, if known? Record in Overrides/{name}.md.

## The quantification ladder
| Rung | Question |
|---|---|
| Action | What was done? |
| Scope | For how many, how often, how long? |
| Result | What changed, in a number? |
| Comparison | Against what? |
| Consequence | What did the unit get? |
Stop at the rung the user can defend.
'''

VOICE = '''# {title} voice

## Standard sentences (from the standard, verbatim; confirm against the user's copy)
TODO

## Verbs that carry facts
led, trained, identified, corrected, secured, raised, reduced, tracked, built, delivered, TODO

## Strike on sight
See scripts/common_checks.py STRIKE. Add product specific words here: TODO

## Professionalism rules
- Grade and last name after the first full mention; never a first name alone.
- Numbers as numerals when they are counts.
- One claim per sentence.
'''

EXEMPLAR = '''# {title} exemplars, fictional, annotated

Every name, unit, number, and date here is invented.

## Strong
TODO: the product as it should read, with an annotation after it explaining what each part does for the reader.

## Weak (annotated line by line)
TODO: the same product done badly, each line followed by [why it fails and what the intake would have produced instead].
'''

CHECK = '''#!/usr/bin/env python3
"""Check a {name} draft. TODO: describe the checks.

Usage:  python3 {snake}_check.py <draft.md>
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
            fails.append(f"missing: {{h}}")
    if not numbers(text):
        warns.append("no numbers anywhere; a product without a number is a characterization")
    for w in strike_hits(text):
        warns.append(f"strike list: '{{w}}'")
    for b in blocked_hits(text):
        fails.append(f"blocked content: {{b}}")
    if dashes(text):
        fails.append("em or en dash present")
    print(f"{upper} CHECK: {{sys.argv[1]}}  {{words(text)}} words")
    for w in warns:
        print(f"  WARN  {{w}}")
    for f in fails:
        print(f"  FAIL  {{f}}")
    if not warns and not fails:
        print("  clean")
    print(f"  -> {{len(fails)}} failures, {{len(warns)}} warnings")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
'''

CASES = '''[
  {{"skill": "{name}", "id": "clean", "query": "Run {snake}_check.py on inputs/good.md", "files": ["inputs/good.md"], "expected_behavior": ["exit 0"], "grader": "TODO"}},
  {{"skill": "{name}", "id": "fails", "query": "Run {snake}_check.py on inputs/bad.md", "files": ["inputs/bad.md"], "expected_behavior": ["exit 1", "TODO: which failures"], "grader": "TODO"}},
  {{"skill": "{name}", "id": "intake", "query": "TODO: a vague request a user would actually make", "files": [], "expected_behavior": ["asks the intake questions one at a time", "does not draft from adjectives", "reads back a fact list before drafting"]}}
]
'''


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    name = sys.argv[1]
    what = sys.argv[2]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.abspath(os.path.join(HERE, "..", ".."))
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        sys.exit("tool name must be kebab case: letters, digits, hyphens")
    snake = name.replace("-", "_")
    title = name.replace("-", " ").capitalize()
    upper = snake.upper()
    d = os.path.join(out, name)
    if os.path.exists(d):
        sys.exit(f"{d} already exists")
    os.makedirs(os.path.join(d, "references"))
    os.makedirs(os.path.join(d, "scripts"))
    ctx = dict(name=name, what=what, title=title, snake=snake, upper=upper)
    open(os.path.join(d, "SKILL.md"), "w").write(SKILL.format(**ctx))
    open(os.path.join(d, "references", "standard.md"), "w").write(STANDARD.format(**ctx))
    open(os.path.join(d, "references", "intake.md"), "w").write(INTAKE.format(**ctx))
    open(os.path.join(d, "references", "voice.md"), "w").write(VOICE.format(**ctx))
    open(os.path.join(d, "references", "exemplar.md"), "w").write(EXEMPLAR.format(**ctx))
    open(os.path.join(d, "scripts", f"{snake}_check.py"), "w").write(CHECK.format(**ctx))
    src = os.path.join(HERE, "common_checks.py")
    if os.path.exists(src):
        open(os.path.join(d, "scripts", "common_checks.py"), "w").write(open(src).read())
    ev = os.path.join(out, "..", "..", "..", "evals", name) if os.path.basename(out) == "skills" else os.path.join(out, "evals", name)
    ev = os.path.normpath(ev)
    os.makedirs(os.path.join(ev, "inputs"), exist_ok=True)
    open(os.path.join(ev, "cases.json"), "w").write(CASES.format(**ctx))
    print(f"scaffolded {d}")
    print(f"evals at {ev}")
    print("Next: fill standard.md from the order (verbatim, with paragraph numbers), write the intake and a fictional exemplar, "
          "make the checker enforce the standard, write inputs/good.md and inputs/bad.md, then run the checker on both.")


if __name__ == "__main__":
    main()
