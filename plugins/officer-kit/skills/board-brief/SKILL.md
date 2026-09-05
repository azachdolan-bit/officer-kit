---
name: board-brief
description: >
  Builds the one page board briefing sheet a leader reads aloud when presenting a Marine to a
  meritorious promotion or recognition board: billet and duties, time in service and grade,
  PME, fitness and marksmanship scores, MCMAP, swim, reading list, education, community
  service, awards, annual training, and the "so what" lines, timed to the board's clock, from
  the same facts as the package. Use when the user says "brief this Marine to the board",
  "board briefing sheet", "I have four minutes to brief", or has just finished a mer pro or
  nomination package.
metadata:
  version: "0.1.0"
---

# Board brief

The person who briefs a Marine to a board gets a few minutes and a sheet. The sheet that works has every number the board scores in a fixed order, so the briefer never hunts, and ends with the three lines that answer the board's only real question: so what. The tool generates the sheet from the package's fact list and forces the so what lines to be written.

## Read first

1. `references/template.md`: the sheet, field by field, and the reading order.
2. The package's facts: `facts.json` saved by `meritorious-promotion` or `nomination` beside the letter, or the letter itself if no facts file exists. Never re-ask for a number that is already in the package; ask only for what the sheet has and the letter does not (TIS, TIG, annual training status, award list, PME dates).
3. The board's instructions from the user: minutes allowed, whether the Marine is present, whether the briefer answers questions.

## Your own material (read first, every time)

1. `Overrides/board-brief.md` in the working folder, if it exists: the command's way wins over the defaults below. Say in one line what it changed.
2. `Reference/Exemplars/board-brief/` in the working folder, if it has files: the user's own command's approved patterns beat the plugin's fictional exemplars.
3. The label. Another Marine's name never enters the session. Work on `<MARINE>` (grade and billet stay); the user runs `security-check/scripts/substitute.py` on the finished file on their own computer. If the rules file records a working label, use that instead.
4. When something comes back with edits, or a board answers differently than expected, tell the user `aar` will capture it.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

The premortem is the board's: they heard this and remembered nothing. Why?

## Workflow

```
Board brief:
- [ ] 1. Facts loaded from the package; gaps listed
- [ ] 2. Gaps asked one at a time (TIS, TIG, PME dates, annual training, awards); "unknown" recorded as a blank the briefer must fill, never invented
- [ ] 3. The so what: three lines, each a fact and its consequence for the unit, drawn from the package's strongest paragraphs; the user confirms or rewrites them
- [ ] 4. Sheet drafted as brief.md from the template
- [ ] 5. python3 scripts/brief_check.py brief.md --minutes 4 exits 0
- [ ] 6. Saved beside the package as Board brief.md; rehearsed once aloud against the clock
```

## The so what lines

Each line is a fact with a number and what it did for the unit, in one sentence a board member can repeat: "Licensed 25 Marines on the decon system and closed the shortfall the inspection found." Not "hard charger," not "future SNCO." Three lines, the strongest first. If the package cannot produce three, the package is thin and the briefer should know that before the board does.

## Rules

- Same numbers as the package, exactly. The checker compares every number on the sheet to the package when given `--package letter.json`.
- Blanks are visible. A field the user could not fill prints as `[ ]`, never as a plausible value.
- Nothing blocked: no medical, family, financial, or disciplinary content, and "derogatory material: none" is stated only when the user says so.
- Timing is an estimate at 140 words a minute. The briefer rehearses; the tool does not promise the clock.

## Utility script

- `scripts/brief_check.py brief.md --minutes N [--package letter.json]`: every template field present; three so what lines, each with a number; no `[ ]` blank left unflagged (warn per blank); word count against the clock; blocked content (fail); with `--package`, every number on the sheet appears in the package (fail on mismatch). Exit 1 on a missing field, missing so what, blocked content, or number mismatch.
