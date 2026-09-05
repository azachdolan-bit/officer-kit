---
name: inspection-prep
description: >
  Prepares a program for a Commanding General's Inspection or a command inspection: the self
  assessment against the Inspector General of the Marine Corps functional area checklist for
  that program, item by item with the evidence that answers each, the discrepancies with a
  corrective action plan (fix, owner by billet, date), and the program binder's contents list.
  Use when the user says "CGIP is coming", "inspection prep for", "self assess the awards
  program", "functional area checklist", "IGMC checklist", "corrective action plan", or is the
  officer responsible for any inspected program.
metadata:
  version: "0.1.0"
---

# Inspection prep

MCO 5040.6K (May 2026) runs the Inspector General's inspection program, and the IGMC publishes the functional area checklists it inspects against (awards, career planning, leave and liberty, safety management, SAPR, consumer level supply, and many more). A program passes when the officer responsible can answer every checklist item with a document. The tool turns the checklist into a self assessment with evidence, lists what is missing as discrepancies with a plan, and builds the binder's contents so the inspector finds everything in order.

## Read first

1. `references/standard.md`: the order and where the checklists live; what an inspector expects of a program.
2. `references/intake.md`: the questions per checklist item.
3. `references/exemplar.md`: a fictional self assessment for a small program.

## Your own material (read first, every time)

1. `Overrides/inspection-prep.md`: the command's inspection schedule, the local checklist additions, the binder format the inspector expects. The command's list wins.
2. `Reference/Exemplars/inspection-prep/`: self assessments that passed in this command.
3. `Reference/Checklists/<program>.md`: the current IGMC checklist for the program, saved by the user from the IGMC site (the tool never invents a checklist item; it asks for the file).
4. Appointment letters and rosters carry names on the user's computer; the assessment refers to billets.

## Thinking (tier: rapid)

**Rapid**, because an inspector reads it and it is reversible. Run the estimate before drafting and the check before delivery: the `think` skill, `references/estimate.md` and `references/check.md`, `references/tripwires.md` for the named shortcuts. State the tier and its trigger in one line so the user can raise it.

The adversarial read applies to every yes: what does this evidence actually prove, read by an inspector who is not inclined to help?

## Workflow

```
Inspection prep:
- [ ] 1. Frame: the program, the inspection (CGIP, command inspection, higher's visit), the date, the officer responsible, the checklist file in Reference/Checklists
- [ ] 2. The checklist read item by item: for each, the question, the reference it cites, and the evidence that would answer it (a letter, a roster, a log, a training record)
- [ ] 3. Self assessment: for each item, yes with the evidence named and where it is, or no with what is missing
- [ ] 4. Discrepancies: every no, with the fix, the owner by billet, and the date, before the inspection date
- [ ] 5. The binder: contents in checklist order, tab by tab, with the evidence for each item
- [ ] 6. python3 scripts/inspection_prep_check.py assessment.md exits 0
- [ ] 7. Saved to Admin/Inspections/<program> <date>/; the corrective action plan tracked weekly until the inspection
```

## The shape (assessment.md)

```
# Self assessment: <program>, <inspection>, <date>
Officer responsible: <billet>   Checklist: <file, version or date>

## Items
| # | Checklist item | Reference | Answer | Evidence and location |
|---|---|---|---|---|
| 1 | Is an awards officer appointed in writing? | MCO 1650.19J | Yes | Appointment letter of <date>, tab 1 |
| 2 | ... | ... | No | missing: <what> |

## Discrepancies and corrective action
| Item | Fix | Owner (billet) | By |
|---|---|---|---|

## Binder contents
| Tab | Contents | Items answered |
|---|---|---|
```

## Rules

- The checklist is the IGMC's or the command's, from a file the user provides. The tool never invents an item; if the file is missing, it says where to get it and stops at the frame.
- Yes means evidence named and located. A yes with no evidence is a no, and the checker treats it that way.
- Every discrepancy has a fix, an owner, and a date before the inspection.
- Nothing about a named Marine in the assessment; appointment letters and rosters are referred to by tab.

## Utility script

- `scripts/inspection_prep_check.py assessment.md`: every item has an answer; every yes has evidence and a location; every no appears in the discrepancies with fix, owner, date; the binder lists every yes item's evidence; names (fail). Exit 1 on a yes without evidence, a no without a plan, or a name.
