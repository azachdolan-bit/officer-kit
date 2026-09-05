---
name: deocs-plan
description: >
  Prepares the command climate action plan a commander signs after a Defense Organizational
  Climate Survey (DEOCS), to MARADMIN 306/25 and MCO 5354.1G w/Admin Ch 1: the survey window and
  latest start the MARADMIN sets (1 August to 30 November, commencing no later than 31 October),
  the order's 90 days for a change of command assessment, who administers the survey (EOA,
  Collateral Duty EOA, or EOC), each finding as the report states it with the report section
  named, one action per finding with an owner by billet, a date, and a measure that names what
  will be compared, the debrief to the unit, and the reporting line, then checks the dates
  against the sources and fails a plan that identifies a respondent, names a Marine, or promises
  the climate will improve. Use when the user says "DEOCS came back", "climate survey action
  plan", "command climate assessment", "CCA action plan", "out brief the DEOCS", "what do I do
  with these survey results", or "change of command climate survey".
metadata:
  version: "0.1.0"
  status: incomplete
---

# DEOCS plan

The order says the point of the assessment is that "understanding the sources of those concerns helps leaders craft an action plan to directly address them," and that "Survey results are the only hard facts collected during the command climate assessment"; everything else is perception. The report is evaluated at IGMCIP inspections, and a commander who does not conduct the assessment has that annotated on their fitness report. The tool takes the report as the commander received it and writes down what it says, where, then one action per finding that a billet can start on a date and the commander can check on a date. It never reads a cause into a number, never quotes a comment, and never points at a person. It prepares; the commander signs, and the EOA or EOC administers. Unverified: the out brief deadline, the action plan deadline, to whom the plan goes, whether the unit must be debriefed, and what a new commander receives are governed by DoDI 6400.11 (the order's reference (am)), which is not in the library; the tool checks those dates for presence and ordering only and marks the gap in the product.

## Read first

1. `references/standard.md`: MARADMIN 306/25 paragraphs 1 to 3 (who, when, who administers); MCO 5354.1G basic order 4.b(5) (the commander's duties) and 5.f (the EOA); enclosure (2) chapter 1 paragraph 8 (the EOC, which replaced the EOR), chapter 2 paragraph 2 (the command team brief), chapter 9 in full (the CCA), Appendix B definition 24; the dates table and "## Not in the library".
2. `references/intake.md`: the questions, one at a time.
3. `references/voice.md`: the sources' words, the four parts of an action, the strike list.
4. `references/exemplar.md`: read only after the fact list is confirmed (step 6). It teaches shape and its content is not to be taken; the checker fails a lifted phrase.

## Your own material (read first, every time)

1. `Overrides/deocs-plan.md`: the out brief and plan due dates this higher headquarters sets and where that is written (its SOP under the order's 4.b(5)(p)), to whom the plan goes, how this commander reads a plan, what the unit debrief looks like here. The command's way wins; say in one line what it changed.
2. `Reference/Exemplars/deocs-plan/`: plans this command signed, sanitized. They beat the plugin's fictional exemplar.
3. Billets throughout; `<MARINE>` if a Marine must be referred to at all, and `<UNIT>` for the unit until substitution on the user's computer with `security-check/scripts/substitute.py`. The report's breakouts and short answer comments stay on the user's computer; the plan carries counts.
4. When the plan comes back from the next echelon or the commander changed an action, `aar` captures why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

## Workflow

```
DEOCS plan:
- [ ] 1. Frame: unit by echelon; annual DEOCS or change of command CCA; the commander by billet; assumption of command date if change of command
- [ ] 2. Dates: opened, closed, out brief, plan due; who set the last two and where it is written (Overrides); the checker tests the window and the 90 days, and presence and ordering for the rest
- [ ] 3. Administrator: EOA, Collateral Duty EOA, or EOC, by billet; JKO Prev 004 complete before the survey opened
- [ ] 4. The report, section by section in the report's order: for each item the commander wants on the plan, what the report says in its words and numbers, under which section and label; strengths to sustain count; breakouts only as the report shows them and never small enough to point at someone; comments as a theme with a count
- [ ] 5. Read back the finding list; the user confirms; nothing else goes in
- [ ] 6. Now read exemplar.md for shape
- [ ] 7. One action per finding, one question at a time: the action a billet can start, the owner by billet, the date, the measure as what will be compared to what; climb the ladder and stop where the owner can start on Monday
- [ ] 8. Which program specialists the commander consulted or will consult (chapter 9 paragraph 4) and which other tools (interviews, focus groups, records reviews) add depth before an action is settled (paragraph 9)
- [ ] 9. Debrief: how and when the unit is told, and what stays with the commander and the EOA. Reporting: to whom, by when, where the report and plan are retained, with the source of each date or the gap marked
- [ ] 10. Draft deocs_plan.md in the shape below
- [ ] 11. python3 scripts/deocs_plan_check.py deocs_plan.md exits 0
- [ ] 12. Strike pass with voice.md
- [ ] 13. Saved to Command/Climate/<UNIT> DEOCS plan <close date>.md; the commander signs; the EOA or EOC files it with the report
- [ ] 14. Learning: what came back, via aar
```

## The product (deocs_plan.md)

```
# DEOCS command climate action plan
Unit: <UNIT> (<echelon>), under <next echelon>, under <the one above>   Survey: <annual DEOCS | change of command CCA>   [Assumed command: <day month year>]   Opened: <day month year>   Closed: <day month year>
Out brief: <day month year>   Plan due: <day month year>   Commander: <billet>   Survey administrator: <the servicing EOA | Collateral Duty EOA | EOC>, <JKO Prev 004 complete or not>
References: MARADMIN 306/25 paragraphs 1 to 3; MCO 5354.1G w/Admin Ch 1 enclosure (2) chapter 9 paragraphs <as used>

## Findings
1. Report section <name>, item <label>: <what the report states, its number as printed, its comparison figure if it prints one>.
2. ...

## Actions
1. Action: <one action a billet can start>. Owner: <billet>. Date: <day month year>. Measure: <what will be compared to what, or counted, on what document>.
2. ...            (numbered to the findings; 4a and 4b for two actions on one finding)

## Debrief
<How and when the unit is told, by whom, from what; what stays with the commander and the EOA.>

## Reporting
<To whom and by when, with the source of the date (Overrides, the higher headquarters SOP) or the gap marked; completion reported per reference (am); where the report and plan are retained (chapter 9 paragraph 11: IGMCIP inspections; chapter 2 paragraph 2.a: the incoming commander's brief).>

## Not in the library
<DoDI 6400.11 and whatever else the plan leaned on that the library does not hold.>
```

## Rules

- A finding is what the report says, where. The report section and label are named, the number is the one printed, and no percentage, average, or trend is computed that the report does not print. The order: "Survey results are the only hard facts collected during the command climate assessment."
- No cause in a finding. The survey is a perception data point; the order's tools for depth are "interviews, focus groups, records reviews, and analysis" with the servicing EOA (chapter 9 paragraph 9). A "because" belongs to those, not to the plan.
- One action per finding, with the four parts: action, owner by billet, date as day month year, measure. The checker fails an action missing any part and a finding with no action.
- The measure names what will be compared or counted and on what document. It never says which way the number will go. The checker fails "will improve", "is fixed", and their relatives anywhere in the plan.
- No person. No name, no rank plus name, no "the Sergeant who wrote", no "one respondent said", no breakout small enough to point at someone, no quotation from a comment. The sources in the library set no minimum respondent count; the portal guidance does and is not in the library, so the tool leaves any small breakout off the plan and says so.
- The dates the sources state are checked: the annual survey closes inside 1 August to 30 November and opens no later than 31 October (MARADMIN paragraph 1; chapter 9 paragraphs 6 and 8); a change of command CCA closes within 90 days after assumption of command (chapter 9 paragraph 5). The out brief and plan due dates are checked for presence and for following the close, and the checker prints that no source in the library sets a deadline for them.
- The administrator is the EOA, a Collateral Duty EOA, or the EOC (MARADMIN paragraph 3), with JKO Prev 004 complete. The order removed the EOR; the plan uses the order's billet.
- The report is not for general release (chapter 9 paragraph 10). The plan carries aggregate items; the report and its breakouts stay with the commander and the EOA.
- Nothing medical, family, financial, disciplinary, or from a complaint or an investigation. The DEOCS factor labels the order itself uses (EO, sexual assault response and prevention, harassment) may appear as the report prints them; a case may not.
- `<UNIT>` and billets until substitution on the user's computer. No em or en dashes.

## Utility scripts

- `scripts/deocs_plan_check.py deocs_plan.md`: title; Unit, Survey type, Commander as a billet, Survey administrator as EOA, Collateral Duty EOA, or EOC (fail otherwise; warn on EOR or no Prev 004); Closed, Out brief, and Plan due present as dates (fail); annual close inside 1 August to 30 November and open no later than 31 October (fail); change of command close within 90 days of Assumed command (fail); out brief or plan due before the close (fail); each finding names its report section (fail) and carries a number (warn) and no cause (warn); each finding has an action and each action has Action, Owner as a billet, Date as day month year, and Measure (fail); a promise about the outcome (fail); Debrief and Reporting present (fail) with dates and the source of the deadline (warn); an individual identified, a name, a lifted exemplar phrase, blocked content, or a dash (fail). Prints a NOTE that the out brief and plan deadlines are presence and ordering checks only. Exit 1 on any failure.
