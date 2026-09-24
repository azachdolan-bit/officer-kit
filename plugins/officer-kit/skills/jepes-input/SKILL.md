---
name: jepes-input
description: >
  Prepares the command input a First Line Supervisor, Evaluator, or Reviewer submits under the
  Junior Enlisted Performance Evaluation System for a Marine in the grades Private through
  Corporal, to MCO 1616.1: a mark in each of the order's three categories (Individual Character,
  MOS and/or Mission Accomplishment, Leadership) on the 0.0 to 5.0 scale with the band named and
  the dated facts from the reporting period under it, the commendatory material an Exceptional
  mark requires and the counseling a Below Expectations mark requires, the promotion
  recommendation or NOT REC with its justification, the occasion and its dates against the
  order's table (SA 1 February to 31 July and 1 August to 31 January), the 45 day submission
  window, and the initial written counseling the FLS owes within 30 days. Use when the user says
  "JEPES marks for", "command input for", "semiannual JEPES", "pro/con for", "what do I mark this
  lance corporal", "NOT REC this Marine", "JEPES counseling", or "initial counseling for my new
  Marine".
metadata:
  version: "0.1.0"
  status: incomplete
---

# JEPES input

The Approver, the O-5 level commander or OIC equivalent, sets the final marks and is charged by the order to "protect against inflation"; everyone below submits recommendations. The order fixes the scale and defines each band: a Marine "should begin at 2.5 in all three categories," a mark of 4.1 or above requires "formal commendatory material visible in JEPES" and a directed comment, a mark of 0.9 or below rests on "counseling, documented or informal, that occurred during the reporting period," and command input "must be based on the Marine's accomplishments [...] during the reporting period." A mark with no dated fact under it is a number in a record that the Approver cannot defend. The tool asks for the facts before it lets a mark move from 2.5, names the band the number falls in, checks the occasion and dates against the order's table, and writes the initial counseling the FLS owes within 30 days. It prepares; the preparer submits in JEPES and the Approver approves. One part is unverified: Figure 1-2, the JEPES Command Input Evaluation Metrics that define what each category measures at each band, is an image in the order and its text is not in the library; the tool uses the band names and ranges of chapter 2 paragraph 3.a and the user must read the figure in JEPES before choosing a mark. The JEPES drop-down list of directed comments is likewise not in the library; the product names the justification in the user's words and the user selects the matching comment in JEPES.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Read first

1. `references/standard.md`: chapter 1 paragraph 1 (the grades and the fourth pillar), paragraph 3.b and 3.c (inflation, the 45 day window), paragraph 4.c (what the chain may not use, the Marine's recourse), paragraph 5 (the roles), paragraph 6 (the cycle, the initial counseling, the debrief); chapter 2 paragraph 1 (what each role shall do), paragraph 2 (the occasions and TO dates, the 30 day minimum, omitted occasions, due dates), paragraph 3 (the bands, NOT REC, adverse material), paragraph 4 (corrections); appendix E (billet accomplishments); the "## Not in the library" section.
2. `references/intake.md`: the questions, one at a time.
3. `references/voice.md`: the order's words, the band names, the strike list.
4. `references/exemplar.md`: read only after the fact list is confirmed (step 6). It teaches shape and its content is not to be taken; the checker fails a lifted phrase.

## Your own material (read first, every time)

1. `Overrides/jepes-input.md`: how this Approver wants justifications written, which directed comments the command pairs with which facts, the unit's reporting chain structure where it departs from squad, platoon, company, and the appointment letter if approval is delegated. The command's way wins; say in one line what it changed.
2. `Reference/Exemplars/jepes-input/`: command inputs this Approver approved, sanitized. They beat the plugin's fictional exemplar.
3. `<MARINE>` throughout; the name goes into JEPES on the user's computer with `security-check/scripts/substitute.py`. An adverse fact is the order's category and a date (chapter 2 paragraph 3.c); the story behind it stays out. Medical, family, and financial circumstances never appear; an exemption is a waiver code in MCTFS, not a sentence in a justification.
4. When the Approver changed a mark or returned the worksheet, `aar` captures why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

## Workflow

```
JEPES input:
- [ ] 1. Frame: the preparer's role (FLS, Evaluator, Reviewer; an SER or Command Reviewer comments and does not mark), the Approver by billet, the Marine (label, grade Private through Corporal, PMOS, billet), the date supervision began
- [ ] 2. Occasion: the code from the order's table and its FROM and TO dates; python3 scripts/jepes_dates.py --occasion <code> --to <date> [--supervision <date>] for the period, the day marks may first be submitted, the Approver's due date, and the initial counseling due date
- [ ] 3. Initial counseling, when the relationship is new: the four elements in the FLS's words (billet description, role in the unit, responsibilities, performance expectations), the objective scores validated and the corrective action started; conducted inside the 30 days
- [ ] 4. Facts under the three categories in the order's order, one question at a time, each with a date inside FROM to TO; the Marine's submitted billet accomplishments count; climb the ladder on each note and stop where the preparer can defend it to the Approver
- [ ] 5. The mark, from the facts: start at 2.5; what moves it and which way; for 4.1 and above the commendatory material by type and date and the directed comment; for 0.9 and below the counseling by date and the directed comment; the band named with the number
- [ ] 6. Read back the fact list and the marks; the user confirms; nothing else goes in. Now read exemplar.md for shape
- [ ] 7. Promotion recommendation: recommended (the default) or NOT REC with a directed justified comment, the adverse material by the order's category and date, and the note that it stands until the next occasion or lifted
- [ ] 8. Draft jepes_input.md in the shape below
- [ ] 9. python3 scripts/jepes_input_check.py jepes_input.md exits 0
- [ ] 10. Strike pass with voice.md; each justification stays the length of a comment field in JEPES
- [ ] 11. Saved to Admin/JEPES/<label> <code> <TO date>.md; the preparer enters the marks and justifications in JEPES and selects the directed comments; the debrief date goes on the calendar
- [ ] 12. Learning: what the Approver changed, via aar
```

## The product (jepes_input.md)

```
# JEPES command input
Marine: <MARINE>, <grade>, <PMOS>, <billet>   Prepared by: <First Line Supervisor | Evaluator | Reviewer> (<billet>)   Approver: <billet>
Occasion: <code> (<name>)   From: <day month year>   To: <day month year>   Submitted: <day month year>   Supervision began: <day month year>   Initial counseling: <day month year>
References: MCO 1616.1 enclosure (1) chapter 1 paragraphs 3.b and 6, chapter 2 paragraphs 2 and 3

## Individual Character
Mark: <0.0 to 5.0, one decimal> (<band>)
Facts: <dated facts inside the period; what moves the mark from 2.5 and where it stops; for 4.1 and above the commendatory material by type and date and the directed comment selected; for 0.9 and below the counseling by date and the directed comment selected>

## MOS and/or Mission Accomplishment
Mark: <mark> (<band>)
Facts: <as above>

## Leadership
Mark: <mark> (<band>)
Facts: <as above>

## Promotion recommendation
<Recommended for promotion. | NOT REC recommended: <the order's adverse material category or the commander's reason> <date>; directed comment selected; in effect until the next occasion or lifted by the commander.>

## Debrief
Planned <date> by <FLS and/or the reporting chain>. Focus for next period: <facts from this one>.
```

When the occasion is the initial counseling the order requires within 30 days of the relationship being established:

```
# JEPES initial counseling
Marine: <MARINE>, <grade>, <PMOS>, <billet>   Prepared by: First Line Supervisor (<billet>)   Approver: <billet>
Occasion: Initial counseling   Supervision began: <day month year>   Due: <30 days later>   Conducted: <day month year>
References: MCO 1616.1 enclosure (1) chapter 1 paragraph 6.b, chapter 2 paragraph 1.b(1)

## Billet description
## Role in the unit
## Responsibilities
## Performance expectations
## Objective scores validated
```

## Rules

- The grades are the order's: Private through Corporal. A Sergeant is not evaluated here; the checker fails the header.
- Only the FLS, Evaluator, and Reviewer submit recommended marks; the SER and Command Reviewer comment and "do not make recommended command input marks." The Approver sets the final marks and may delegate to one leader by appointment letter.
- The occasion is one of the order's twelve codes with the TO date the order fixes; the checker carries the table and fails an SA that does not end 31 July or 31 January, an AN that does not end 31 December, a FROM date outside the period, and a PR for a promotion to PFC or LCpl. Minimum observation 30 days. Recommended marks may not be submitted earlier than 45 days before the TO date.
- Three categories in the order's order, each with a mark on the 0.0 to 5.0 scale and the band named: Exceptional 4.1 to 5.0, Exceeds Expectations 3.1 to 4.0, Meets Expectations 2.0 to 3.0, Working Towards Expectations 1.0 to 1.9, Below Expectations 0.1 to 0.9. Start at 2.5; every mark, including 2.5, has a dated fact from inside the period under it.
- 4.1 and above: formal commendatory material of the period by type and date, and a directed comment. Without the material the order places the Marine at 4.0 or below. The order calls this band "a rarity."
- 0.9 and below: counseling of the period by date and a directed comment. This band "is not adverse" and does not by itself NOT REC the Marine.
- The Marine is recommended for promotion unless the commander approves a NOT REC. A 0.0 in any category is a NOT REC by default. A NOT REC carries a directed justified comment and, for adverse material, the order's category and a date; it stands until the next occasion or lifted.
- No personal or unit set of precepts in place of Figure 1-2; the Marine may take a suspected bias to the Approver by request mast (chapter 1 paragraph 4.c). Nothing about the promotion outcome; the cutting score decides.
- The initial written counseling within 30 days has the four elements the order names and is paired with validating the objective scores. The JEPES worksheet itself "is not a communication tool, nor a counseling document."
- Nothing medical, family, financial, or from an investigation. `<MARINE>` until substitution on the user's computer. No em or en dashes.

## Utility scripts

- `scripts/jepes_dates.py --occasion <code> --to <date> [--from <date>] [--date <date>] [--supervision <date>]`: the occasion's FROM and TO dates from the order's table, the first day recommended marks may be submitted (45 days before TO), the Approver's due date, the observation length against 30 days, and the initial counseling due date 30 days after the relationship was established.
- `scripts/jepes_input_check.py jepes_input.md`: title and label; a covered grade (fail otherwise); a preparer who marks (fail for SER or Command Reviewer); the occasion code in the order's table with FROM and TO dates that match it (fail on a wrong end date, a FROM outside the period, or a PR to PFC or LCpl); submission more than 45 days early (fail); observation under 30 days (warn); the three categories each with a mark on the scale and the band that matches the number (fail), a dated fact under it and one inside the period (fail), commendatory material for 4.1 and above (fail), counseling for 0.9 and below (fail), the directed comment named (warn); the promotion recommendation present, a 0.0 carried as NOT REC, a NOT REC with a dated justification (fail); the debrief (warn); an FLS whose supervision began in the period with no initial counseling date (fail); for the counseling product the four elements and a conducted date inside the 30 days (fail); promises about promotion, blocked content, names, lifted exemplar phrases, and dashes (fail). Exit 1 on any failure.
