---
name: counseling
description: >
  Writes a counseling record (initial, follow on, or event counseling) from a leader's notes to
  the Marine Corps counseling program: observations and incidents as dated facts in the
  leader's words, an evaluation that names the effect on the mission, and a plan with a named
  mentor, a feedback cadence, a measurable return condition, and an end state, then scrubs it
  of content that does not belong in a counseling record. Use when the user says "counseling
  from these notes", "initial counseling for", "write up this Marine for", "event counseling",
  "follow on counseling", "counsel this Marine on", or "document this".
metadata:
  version: "0.1.0"
---

# Counseling

A counseling record is read later, by people who were not there: the next leader, a board, sometimes a lawyer. What holds up is a dated fact in the leader's words, an honest evaluation of what it cost the unit, and a plan that names a person, a cadence, and a condition the Marine can meet. Characterizations ("bad attitude") do not hold up, and neither does a plan with no date.

The governing publication is MCO 1500.61 (Marine Leader Development) and the counseling worksheet the user's command uses (a NAVMC form or a local sheet). The tool asks which sheet and writes to its blocks; the default blocks below match the common worksheet.

## Read first

1. `references/intake.md`: the questions, by block, and the standard for an incident line.
2. `references/exemplar.md`: one fictional event counseling and one fictional initial counseling, annotated.
3. The user's copy of MCO 1500.61 in Reference, if present, for the program's own language on the purpose of counseling and the leader's responsibilities. Reference `Admin/MCO 1500.61 Marine Leader Development.pdf` when the library has it.

## Workflow

```
Counseling record:
- [ ] 1. Type (initial, follow on, event), the Marine (grade, name, billet), the counselor, the date, the worksheet the command uses
- [ ] 2. Initial: billet description, standards expected, goals for the period, the next counseling date. Event or follow on: each incident as a dated fact (what, when, who observed it, what instruction preceded it)
- [ ] 3. Evaluation: what the pattern is and what it cost the unit, in three sentences
- [ ] 4. Plan: tasks for the next period with dates; a named mentor; the feedback cadence; the return condition (what done by when ends the plan); the end state in one sentence
- [ ] 5. Read back the incident list; the user confirms each is their own observation or names who observed it
- [ ] 6. Draft as counseling.md in the worksheet's blocks
- [ ] 7. python3 scripts/counseling_check.py counseling.md exits 0
- [ ] 8. Saved to Admin/Counseling/<Marine label> <type> <date>.md; printed to the command's form by the user; signatures on paper
```

## The blocks (default worksheet)

- **A. Administrative**: Marine, counselor, date, type, period covered, references (MCO 1500.61 and the command's sheet).
- **B. Billet and standards** (initial counseling): the billet in the leader's words, the standards expected, and the goals for the period with dates.
- **C. Observations and incidents**: one line each, dated, in the observer's words. What was expected, what happened, who saw it. No adjectives.
- **D. Evaluation**: what the incidents add up to and the effect on the section's mission. Three sentences.
- **E. Plan for the next period**: numbered tasks with dates; the mentor by grade and name; the cadence (weekly on a named day); the return condition; the end state.
- **F. Marine's comments**: left blank for the Marine.
- **G. Signatures**: names and date lines; signed on paper, never by the tool.

## Rules

- Facts, not traits. "Late to duty changeover on 12 July after receiving the time in writing on 11 July" is an incident. "Unreliable" is not.
- The counselor's own observation, or the observer named. The tool asks for both and records "reported by <grade name>" where the counselor did not see it.
- Nothing medical, family, financial, or from an investigation goes in the record, even when the notes contain it and even when it is the reason. A leader who needs to record that a Marine was referred somewhere writes "referred to the appropriate resource on <date>" and nothing more. The checker fails on the content.
- No promise the leader cannot keep: no "will be separated," no "will be promoted." The plan states what the leader will do (meet weekly, assign the mentor, re evaluate on a date).
- Never draft a punitive document. NJP, adverse fitness reports, page 11 entries, and separation are outside this tool; say so and stop. Counseling is developmental even when the event was bad.

## Utility script

- `scripts/counseling_check.py counseling.md`: blocks A, C or B, D, E, F, G present; every incident line in C carries a date; E has a mentor by grade and name, a cadence word, a return condition with a date, and an end state; D is present and short; trait words in C (warn); blocked content anywhere (fail); promises the leader cannot keep (fail). Exit 1 on a missing block, an undated incident, or blocked content.
