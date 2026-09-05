---
name: nomination
description: >
  Builds a quarterly or annual recognition nomination (Marine, NCO, or SNCO of the Quarter or
  of the Year, and the higher echelon nominations that follow a win) to the command's
  recognition order: the nomination letter in the board's lettered scoring categories with the
  numbers each expects, the data sheet content, and the enclosure list, from a category by
  category intake. Use when the user says "NCO of the quarter package", "Marine of the year
  nomination", "nominate for", "quarterly recognition", or "the MEF board package".
metadata:
  version: "0.1.0"
---

# Nomination

Recognition boards score the same categories a meritorious promotion board does, and the nomination letters that win are built on the same skeleton: a naval letter to the local recognition order, the Marine eligible and nominated in one sentence, the enclosures, then billets and lettered accomplishments a through g with a number under each. A quarter's nomination is scoped to the quarter; the annual to the year; the next echelon (Group to Wing to MEF) reuses the winning package with the dates and the addressee changed and, usually, a longer enclosure list.

## Read first

1. The command's recognition order, from the user's Reference or from the user: eligibility, the period covered, categories if the order lists them (the order's categories win over the default seven), the data sheet, the enclosures in order, routing, and the due date.
2. `references/categories.md`: the default seven categories and the numbers boards expect.
3. The `meritorious-promotion` skill's `references/exemplar.md` for the letter's shape; a nomination reads the same with "nominated as <Group> Noncommissioned Officer of the Quarter for <period>" in paragraph 1.
4. Format: the `naval-letter` skill; render with its `scripts/build_letter.py`.
5. `board-brief` builds the briefing sheet from the same facts.

## Your own material (read first, every time)

1. `Overrides/nomination.md` in the working folder, if it exists: the command's way wins over the defaults below. Say in one line what it changed.
2. `Reference/Exemplars/nomination/` in the working folder, if it has files: the user's own command's approved patterns beat the plugin's fictional exemplars.
3. The label. Another Marine's name never enters the session. Work on `<MARINE>` (grade and billet stay); the user runs `security-check/scripts/substitute.py` on the finished file on their own computer. If the rules file records a working label, use that instead.
4. When something comes back with edits, or a board answers differently than expected, tell the user `aar` will capture it.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

Quarantine the outcome: fill each category from the record before considering whether the package looks competitive.

## Workflow

```
Nomination package:
- [ ] 1. The order: recognition order identified; period covered; eligibility; categories; enclosure list in order; routing; due date
- [ ] 2. Frame: Marine, grade, unit; the award (Marine, NCO, or SNCO; quarter or year; echelon); nominating CO; the board
- [ ] 3. Billets in the period, dated; above grade marked
- [ ] 4. Intake by category, one at a time, scoped to the period; numbers with sources; "none" is none
- [ ] 5. Fact list read back and confirmed
- [ ] 6. Letter drafted as letter.json (paragraph 1 eligible and nominated per reference (a); paragraph 2 enclosures; paragraph 3 billets and a to g; POC)
- [ ] 7. python3 scripts/board_package_check.py letter.json --kind nomination exits 0
- [ ] 8. Rendered; saved to Admin/Nominations/<Marine label> <award> <period>/
- [ ] 9. If the Marine wins and the next echelon requires a package: same facts, new addressee and dates, the higher order's enclosure list
- [ ] 10. Learning: result and feedback to LEARNINGS.md
```

## Rules

- Scope to the period. A quarter's nomination that reaches back a year is padded, and boards notice.
- The order's categories replace the default seven when the order lists them; map the facts, do not force the letter into a shape the board does not score.
- Everything in the `meritorious-promotion` rules applies: numbers from the record, thin categories stay thin, nothing blocked, the CO owns the words.

## Utility script

- `scripts/board_package_check.py letter.json --kind nomination`: same checks as the meritorious promotion checker with the nomination wording in paragraph 1. Exit 1 on structure or blocked content.
