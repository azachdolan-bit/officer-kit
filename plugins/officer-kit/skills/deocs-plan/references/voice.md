# DEOCS plan voice

The reader is the commander, who signs it and answers for it at the next inspection, and after that the next commander, who inherits it. The plan exists so that on each date on it someone can be asked whether the thing happened.

## The sources' own words (use them exactly, never a paraphrase)
"Command Climate Assessment (CCA)". "Defense Organizational Climate Survey (DEOCS)". "annual DEOCS" and "change of command CCA". "Equal Opportunity Advisor (EOA)", "Collateral Duty EOA", "Equal Opportunity Coordinator (EOC)". "survey administrator". "protective and risk factors". "action plan". "between 1 August and 30 November". "within 90 days after assumption of command". "Extensions are not permitted."

## The four parts of an action, in this order
Action, then owner by billet, then date, then measure. One line each. An action missing one of the four is a wish.

## Sentences that carry the plan
These sentences show shape only. No number, date, section name, or fact in them is to be taken into a product; the report and the intake supply those, and `deocs_plan_check.py` fails a draft that lifts a phrase from here.

"Finding 3. Report section Protective Factors, item Fairness: 61 percent favorable against a comparison group of 74." (The report's words, the report's numbers, the report's section.)
"Action: publish the awards board schedule and results by company on the first Friday of each month." (One action a person can start on a date.)
"Owner: the executive officer." (A billet. Never a name.)
"Date: 14 November 2026, reviewed at the monthly commander's review." (A date the commander can ask about.)
"Measure: the same item on the change of command DEOCS in 2027 compared to this report's 61 percent; awards board results posted for 6 of 6 months." (What will be compared, not how it will come out.)
"Debrief: company formations during the week of 17 November 2026, led by each company commander, from the one page summary the EOA prepares; the full report stays with the commander and the EOA." (How and when the unit is told.)

## Verbs that carry facts
publish, schedule, brief, train, review, count, compare, post, staff, appoint, consult, retain, report

## Strike on sight
See scripts/common_checks.py STRIKE. Add for this product: "toxic" (a characterization of the unit; the report's own item label is quoted as the report prints it), "morale problem", "culture problem", "the Marines feel", "clearly", "obviously", "root cause" (the survey is a perception data point; the order says the survey is the only hard fact and the rest is perception), "zero tolerance" (a slogan, not an action), "reinforce", "emphasize", "re-emphasize", "continue to" (none of these can be checked on a date).

## Never
- A number the report does not print. No computed percentage, no average of two items, no trend the report does not show.
- A reading of why a number is what it is. The finding is what the report says; the action is what the command will do; the "because" is left to the focus group or the interview the order names as the tools for depth.
- A person. No name, no "the Sergeant who wrote", no "one respondent said", no breakout small enough to point at someone. `<MARINE>` is the label if a Marine must be referred to at all, and in this product a Marine almost never is; billets do the work.
- A quotation from a short answer comment. The theme, as a count.
- "The climate is fixed." "The climate will improve." "This will raise trust." The plan states the action and what will be measured. The next survey says what happened.
- An owner who is a name, a rank alone, or "all hands".
- A date that is a quarter or a season. Day, month, year.
- Em or en dashes.

## Professionalism rules
- Findings in the report's order, numbered, each with its report section named.
- Actions numbered to the findings, one to one; two actions for one finding are 4a and 4b, never a merged action for two findings.
- Numbers as numerals; dates as day month year; billets in full on first use.
- One claim per sentence. A plan the commander can read in five minutes.
