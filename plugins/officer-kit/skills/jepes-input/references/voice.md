# JEPES input voice

The reader is the next member of the reporting chain and, at the end, the Approver, who sets the final marks and is charged by the order to "protect against inflation." The justification exists to make the mark true against the order's bands. It is not a counseling document and not a message to the Marine (chapter 1 paragraph 1.c(3)).

## The order's own words (use them exactly, never a paraphrase)
The three categories, in the order's order: Individual Character; MOS and/or Mission Accomplishment; Leadership. The bands: Exceptional (4.1 to 5.0); Exceeds Expectations (3.1 to 4.0); Meets Expectations (2.0 to 3.0); Working Towards Expectations (1.0 to 1.9); Below Expectations (0.1 to 0.9). The promotion line: recommended for promotion, or NOT REC. The occasion codes: PR, TR, CD, TD, TC, AN, SA, AT, DC, RD, DD, RT.

## Sentences that carry a mark
These sentences show shape only. No number, date, or fact in them is to be taken into a product; the intake supplies those, and `jepes_input_check.py` fails a draft that lifts a phrase from here.

"Mark: 2.5 (Meets Expectations). Performed the duties of an ammunition technician from 1 February 2026 to 31 July 2026 with no discrepancy on the 14 May 2026 inventory; nothing in the period moves the mark from 2.5." (A mark that stays at the starting point still has a dated fact under it.)

"Mark: 3.6 (Exceeds Expectations). Rebuilt 9 of the platoon's 11 radio batteries between 3 March and 22 April 2026, against a platoon average of 4 per Marine; no formal commendatory material in the period, so the mark stays below 4.1." (The fact, the comparison, and the reason the mark stops where it does.)

"Mark: 4.3 (Exceptional). Certificate of Commendation dated 18 June 2026 for the 2 to 6 June 2026 recovery of a disabled vehicle under blackout conditions; directed comment selected in JEPES." (The commendatory material by type and date, as the order requires for this band.)

"Mark: 0.8 (Below Expectations). Counseled 12 March 2026 and 29 April 2026 for missing the 0600 formation; directed comment selected in JEPES; this band is not adverse." (Counseling by date, in the period, as the order requires for this band.)

"NOT REC recommended: notification of separation proceedings received 9 July 2026; in effect until the next occasion or lifted by the commander." (The adverse material by the order's category and date, no story.)

## Verbs that carry facts
performed, completed, qualified, maintained, accounted for, rebuilt, repaired, led, trained, instructed, corrected, counseled, submitted, passed, ranked

## Strike on sight
See scripts/common_checks.py STRIKE. Add for this product: "hard charger", "asset to the unit", "great Marine", "motivated", "always", "never fails", "future sergeant major", "should be promoted", "deserves promotion", "will be promoted", "top Marine in the platoon" (a ranking is a count of a count, not an adjective).

## Never
- A mark of 4.1 or above without formal commendatory material of this period named by type and date.
- A mark of 0.9 or below without counseling of this period named by date.
- A band name that disagrees with the number.
- A fact from outside the FROM and TO dates.
- A unit or personal standard in place of Figure 1-2 (chapter 1 paragraph 4.c).
- Anything about the promotion outcome: the cutting score decides, and the Approver sets the final marks.
- Medical, family, or financial detail; an adverse fact is the order's category and a date.
- Another Marine's name. `<MARINE>` until substitution on the user's computer.
- Em or en dashes.

## Professionalism rules
- Grade and label after the first full mention ("Lance Corporal <MARINE>", then "the Marine").
- Numbers as numerals when they are counts; marks with one decimal; dates as day month year.
- One claim per sentence. The justification is a comment field in JEPES, not a page.
