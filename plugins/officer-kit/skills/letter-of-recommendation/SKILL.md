---
name: letter-of-recommendation
description: >
  Writes a letter of recommendation for a Marine to a program, school, commissioning source,
  board, or civilian purpose, from the writer's own observation: standing, the one line ranking
  statement the reader is deciding on, specifics with numbers, one concrete scene, and the
  close, in naval letter format, then checks it mechanically. Use when the user says "letter of
  recommendation for", "recommend this Marine for", "LOR for MECEP", "endorsement for", "write a
  rec for", or "reference letter", or pastes a Marine's record and asks for a recommendation.
metadata:
  version: "0.1.0"
---

# Letter of recommendation

A selection board reads a hundred of these. What survives is a ranking statement from someone with standing, backed by two or three numbers and one scene the writer saw. Adjectives do not survive. The tool exists to get the writer's standing, the ranking, the numbers, and the scene onto one page and to strip everything else.

The writer must have observed the Marine. If the user is drafting for a senior to sign, the intake asks what that senior actually saw; a letter written from a data sheet reads like one.

## Read first

1. `references/intake.md`: the questions in order, and the ranking statement rule.
2. `references/exemplar.md`: one fictional strong letter and one fictional weak letter, annotated.
3. The program's own instruction, if it is in the user's Reference (a MARADMIN or order names what the board weighs and sometimes what the letter must contain). If it is not, ask the user for what the board scores and record it.
4. Format: the `naval-letter` skill's `references/standard.md`. Render with its `scripts/build_letter.py`.

## Your own material (read first, every time)

1. `Overrides/letter-of-recommendation.md` in the working folder, if it exists: the command's way wins over the defaults below. Say in one line what it changed.
2. `Reference/Exemplars/letter-of-recommendation/` in the working folder, if it has files: the user's own command's approved patterns beat the plugin's fictional exemplars.
3. The label. Another Marine's name never enters the session. Work on `<MARINE>` (grade and billet stay); the user runs `security-check/scripts/substitute.py` on the finished file on their own computer. If the rules file records a working label, use that instead.
4. When something comes back with edits, or a board answers differently than expected, tell the user `aar` will capture it.

## Thinking (tier: rapid)

**Rapid**, because a board reads it and it is reversible. Run the estimate before drafting and the check before delivery: the `think` skill, `references/estimate.md` and `references/check.md`, `references/tripwires.md` for the named shortcuts. State the tier and its trigger in one line so the user can raise it.

The premortem is the board's: they read this and learned nothing about the Marine. Why?

## Workflow

```
Letter of recommendation:
- [ ] 1. The reader: what program or purpose, who decides, what they score, the deadline and any required content from the program's instruction
- [ ] 2. Standing: who the writer is to the Marine, in what billets, over what period, direct or indirect observation
- [ ] 3. The ranking statement: best of how many, over what period, in what respect (intake.md rule); declined if the writer cannot make one honestly
- [ ] 4. Specifics: two to four facts with numbers that bear on what the reader is deciding
- [ ] 5. One scene: a thing the writer saw the Marine do, dated, one paragraph
- [ ] 6. Read back the fact list; user confirms; nothing else goes in
- [ ] 7. Draft as letter.json (naval-letter spec); paragraphs in the six part shape
- [ ] 8. python3 scripts/lor_check.py letter.json exits 0
- [ ] 9. Rendered with the naval-letter build script; one page; saved to Admin/Letters/<Marine label> LOR <program> <date>/
- [ ] 10. Learning: if the board's outcome or the signer's edits teach something, record it in LEARNINGS.md
```

## The six paragraphs

1. Standing. "I served as <Marine>'s <relationship> from <month year> to <month year> as <billet>, <unit>." Direct observation stated as such.
2. The recommendation and the ranking statement. One sentence names the program and recommends, in the strength the writer means (recommended, strongly recommended, recommended without reservation). One sentence ranks: best of how many, over what period. The unit's scale in one clause (a squadron of 600 Marines and Sailors).
3. Specifics. Billets held, above grade if so; two to four numbers (personnel trained, equipment accounted for, a readiness change, a selection).
4. The scene. One thing the writer watched happen, with the date or period and what it showed. This is the paragraph a board remembers.
5. The close. What the writer expects if the Marine is selected, and one line of what the Marine will do next if not. No new claims.
6. Point of contact.

One page. Numbers as numerals. Grade and last name after the first full mention. No word on the strike list in `scripts/common_checks.py`.

## Rules

- Never rank when the writer will not. "Among the best I have served with" is a ranking; the tool asks for the denominator and takes "I cannot say" as the answer.
- Never write from the data sheet alone. PFT scores and course completions belong in the package's data sheet; the letter carries what the writer saw.
- Nothing medical, family, financial, disciplinary, or from an investigation, even favorable ("overcame a difficult family situation" stays out). The checker scans for it.
- A letter for a civilian purpose (a job, a school) keeps the same shape, drops the naval letter format if the reader is civilian, and never carries the Marine's identifiers beyond name and grade.
- The signer's voice wins. If the user reports the signer's edits, apply them and record the pattern in the reader profile for that signer.

## Utility script

- `scripts/lor_check.py letter.json`: six paragraphs present in order; standing paragraph has a period; a ranking statement with a denominator; at least three numbers in paragraphs 3 and 4; a POC; strike list words (warn); blocked content (fail); estimated length under one page. Exit 1 on a structural or blocked content failure.
