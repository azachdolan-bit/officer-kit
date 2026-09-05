# Board preparation voice

Two readers. The audit, fitness report, photo, PME, and reading sections are read by the officer and the career counselor or monitor, who decide from them what still has to reach MMPB-22, MMPB-23, or MMPB-10 and by when. The letter is read by the President of the Board and the members, who read hundreds and decide nothing from a letter that restates the record.

## The message's own words (use them exactly)
"President, FY28 USMC/USMCR (appropriate grade and competitive category) promotion selection board" (paragraph 8.a, with the grade and category filled in). "Encouraged, but are not required" (paragraph 8). "NLT 2359 Eastern Standard Time (EST)" (paragraph 1). "Two weeks prior to the convening date" (paragraph 7.a). "Reconstructed original" and "certified as true copies" (paragraph 7.c.1). "To be considered PME complete" (MCO 1553.4B enclosure (1)). "Aim to complete at least five titles annually" (ALMAR 024/25 paragraph 1.a).

## The audit line
Item, where it was checked, verified with a date or not, and the fix with its recipient and deadline. One line per item. "Yes" carries a date or it is not a yes.

## Sentences that carry the preparation
These sentences show shape only. No date, count, or fact in them is to be taken into a product; the intake supplies those, and `board_prep_check.py` fails a draft that lifts a phrase from here.

"OMPF viewed in O-RMA on 14 April 2026; 61 documents; the two awards from 2025 are present." (Verified with a date and a count.)
"MBS fitness report listing ends 31 January 2026; the report ending 19 March 2026 is in processing status at MMPB-23." (A record fact, not a worry.)
"Gap of 47 days between the report ending 12 June 2024 and the report beginning 29 July 2024; the missing report is over one year old; certified true copies sent to MMPB-23 on 3 April 2026." (The gap as dates, the rule that applies, the fix with a date.)
"Required for the grade: EWS, EWSDEP, or an ACCC. Held: EWSDEP, completed 22 September 2025, on the MBS, certificate in the OMPF." (Required, then held, then where it shows.)
"Read from the FY26 list: three titles; the ALMAR's aim is five a year." (The log against the expectation, not rounded.)
"Enclosure (1) is the CCE completion letter for EWSDEP seminars 1 through 6 dated 8 March 2026; seminars 7 and 8 are scheduled for May 2026." (The letter tells the board a fact the record does not show, with the evidence listed.)

## Verbs that carry facts
viewed, verified, listed, submitted, received, corrected, completed, enrolled, read, enclosed, signed, uploaded

## Strike on sight
See scripts/common_checks.py STRIKE. Add for this product: "will be selected", "should pick up", "will pick up", "will be promoted", "is competitive for", "a strong record", "deserves promotion", "the board will see", "I am confident the board", "best qualified" as a claim about the officer, "fully qualified" as a claim about the officer (the AFQOL screen decides that), "complete record" (say what was verified and when).

## Never
- Any statement about what the board will do, or what the officer's chances are. The product prepares a record; the board decides.
- A deadline that does not come from the message: the Bd.Corr.Due date and the convening date from the paragraph 1 table, two weeks before convening for OMPF documents. Nothing computed from memory of another year's message.
- "Verified" without a date.
- A letter that asks the board to add anything to the OMPF; the message says it will not (paragraph 8).
- A letter from another party except as a listed enclosure under the officer's signed cover letter (paragraph 8.d).
- Anything classified in the correspondence (paragraph 8.c).
- A title marked as on the FY26 list that the ALMAR does not print.
- Another Marine's name. `<MARINE>` until substitution on the user's computer.
- Em or en dashes.

## Professionalism rules
- Grade and label after the first full mention ("Captain <MARINE>", then "the officer").
- Dates as day month year; the table's dates may be written as the table prints them (8 Jul 26) or in full (8 July 2026).
- One item per line in the audit; one point per paragraph in the letter, each tied to an enclosure or a record fact.
- The letter is short. It tells the board what the record cannot, and stops.
