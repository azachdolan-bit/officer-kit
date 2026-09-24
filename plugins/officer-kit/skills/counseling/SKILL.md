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

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Read first

1. `references/intake.md`: the questions, by block, and the standard for an incident line.
2. `references/exemplar.md`: one fictional event counseling and one fictional initial counseling, annotated.
3. The user's copy of MCO 1500.61 in Reference, if present, for the program's own language on the purpose of counseling and the leader's responsibilities. Reference `Admin/MCO 1500.61 Marine Leader Development.pdf` when the library has it.

## Your own material (read first, every time)

1. `Overrides/counseling.md` in the working folder, if it exists: the command's way wins over the defaults below. Say in one line what it changed.
2. `Reference/Exemplars/counseling/` in the working folder, if it has files: the user's own command's approved patterns beat the plugin's fictional exemplars.
3. The label. Another Marine's name never enters the session. Work on `<MARINE>` (grade and billet stay); the user runs `security-check/scripts/substitute.py` on the finished file on their own computer. If the rules file records a working label, use that instead.
4. When something comes back with edits, or a board answers differently than expected, tell the user `aar` will capture it.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

The adversarial read on every task in the plan: what does this permit that you did not mean? `think/scripts/precision_check.py counseling.md --directive`.

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
