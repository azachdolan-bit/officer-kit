---
name: meritorious-promotion
description: >
  Builds a meritorious promotion recommendation the way the boards read it: the letter to the
  command's local order with the recommendation in the board's lettered scoring categories and
  the numbers each expects, the enclosure list the order requires, and the data for the board
  briefing sheet, from an intake that asks for facts under each category and leaves a thin one
  thin. Use when the user says "mer pro", "meritorious promotion for", "recommend for
  meritorious promotion", "mer pro board package", or "write the mer pro letter".
metadata:
  version: "0.1.0"
---

# Meritorious promotion

A meritorious promotion board scores a fixed set of categories, and the recommendation letter that wins is the one that puts a verifiable number under each category in the order the board scores them. Commands five years and two units apart have used the same seven lettered paragraphs; that is the board's rubric surfacing in the letter, and the tool builds to it explicitly.

The Marine Corps standard is MCO P1400.32D w/Ch 2 (the Enlisted Promotion Manual, 2012; MARADMIN 667/22 for meritorious quota rules); the package itself is governed by the command's local order (a MEF, Wing, or Group order), which sets eligibility, the enclosure list, the data sheet, and the board date. The tool asks for that order first and does not invent one.

## Read first

1. The command's local order, from the user's Reference or from the user. Record: eligibility window, the enclosures required in order, the data sheet form, routing, and the due date.
2. `references/categories.md`: the seven board categories, what each contains, and the numbers boards expect under each.
3. `references/exemplar.md`: a fictional recommendation letter, annotated.
4. Format: the `naval-letter` skill's `references/standard.md`; render with its `scripts/build_letter.py`.
5. When the package is done, `board-brief` builds the briefing sheet from the same facts.

## Workflow

```
Meritorious promotion package:
- [ ] 1. The order: local order identified, eligibility confirmed against it (TIG, TIS, cutting score if applicable, no pending adverse action per the user), enclosure list copied in order, due date
- [ ] 2. Frame: Marine's grade, name, MOS, unit; recommending CO; approving authority; board date
- [ ] 3. Billets: every billet held in the current grade with dates; above grade billets marked
- [ ] 4. Intake by category, a through g, one at a time (categories.md); each fact with a number and a source; "none" recorded as none
- [ ] 5. Read back the fact list by category; user confirms; nothing else goes in
- [ ] 6. Letter drafted as letter.json: paragraph 1 eligible and recommended per the reference; paragraph 2 enclosures; paragraph 3 billets then "accomplishments are as follows:" and subparagraphs a to g; POC
- [ ] 7. python3 scripts/board_package_check.py letter.json --kind merpro exits 0
- [ ] 8. Rendered; enclosure list matches the order; saved to Admin/Promotions/<Marine label> mer pro <date>/
- [ ] 9. board-brief run from the same fact list; facts.json saved beside the letter
- [ ] 10. Learning: board result and any feedback recorded in LEARNINGS.md
```

## The letter

Paragraph 1: "Per reference (a), <Grade Name> is eligible and recommended for meritorious promotion to <grade>." One sentence.

Paragraph 2: "Enclosures (1) through (n) are submitted as required by the reference." The enclosures are listed in the heading block exactly as the order names them.

Paragraph 3: one sentence per billet held in grade, with dates and "a billet normally held by a <grade>" where true. Then "<Grade Name>'s meritorious accomplishments are as follows:" and the lettered subparagraphs in the order in `references/categories.md`. Each subparagraph is facts and numbers, two to five sentences, and a category with nothing in it says so in one sentence rather than padding ("has not yet had the opportunity to deploy").

POC paragraph, then the CO's signature.

## Rules

- Eligibility is the order's, not the tool's. If the user cannot confirm eligibility against the order, the package is drafted with that gap stated at the top of the fact list.
- Every number comes from the user or the record they hold (MCTFS screens, the training record, the data sheet). The tool never estimates a PFT score.
- A thin category stays thin. Padding a category is the fastest way to lose a board that reads twenty packages.
- Nothing medical, family, financial, or disciplinary, and no EDIPI or SSN in the letter text; those belong on the forms the order requires, filled by admin.
- The CO signs and owns the words. The user reports the CO's edits; the tool records them as a reader profile for that CO.

## Utility script

- `scripts/board_package_check.py letter.json --kind merpro`: three body paragraphs plus POC; paragraph 1 states eligible and recommended per the reference; paragraph 2 names the enclosures and their count matches the encl list; paragraph 3 has subparagraphs a through g in order; each category is checked for the numbers it expects (warn when absent, fail when the category is missing); strike list (warn); blocked content and identifiers (fail). Exit 1 on structure or blocked content.
