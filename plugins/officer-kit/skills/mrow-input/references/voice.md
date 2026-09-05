# MROW input voice

The reader is the RS, who will "assess the information provided by the MRO on the MROW and report that information on the MRO's fitness report as deemed appropriate" (chapter 2 paragraph 3.c(3)). Every line exists so the RS can lift it into section B or C with the fewest edits, or verify it and leave it out. The MRO does not evaluate the MRO.

## The order's words for each section (use them to test every line)
Section B: "the nature of the billet and the MRO's significant responsibilities as they relate to the accomplishment of his or her unit's or organization's mission during the reporting period" (5.a); "acceptable standards vice goals" (5.b(3)); "significant primary, additional, and special duties assigned by the RS" (5.c(2)).
Section C: "exactly what the Marine accomplished in the billet" (6.a(2)); "objective rather than qualitative" (6.a(3)); "only the results and achievements themselves" (6.a(4)); "short and direct, using words and phrases commonly understood by most Marines" (6.c(4)).

## Shape of a billet description bullet
Duty, then scope, then the standard the RS set. Present tense, because it describes the billet, not the period.

## Shape of an accomplishment bullet
Verb in past tense, then what, then the count, then the result against a baseline. One accomplishment per bullet. No adjective about the MRO.

## Sentences that carry the shape
These sentences show shape only. No number, date, or fact in them is to be taken into a product; the intake supplies those, and `mrow_input_check.py` fails a draft that lifts a phrase from here.

"- Platoon commander for 43 Marines and 9 vehicles; responsible for training to T&R standard and for readiness of assigned equipment." (Billet description: duty, scope, standard. No adjective.)
"- Collateral: unit voting assistance officer from 12 January 2026." (An additional duty with the date it was assigned.)
"- Qualified 41 of 43 Marines on the annual rifle range, against 36 of 43 the prior year." (Action, scope, result, comparison to a measured baseline.)
"- Planned and executed 4 live fire ranges for 210 Marines with no mishap and no range control violation." (Result stated in the unit's terms; the consequence is the number.)
"- Wrote the battalion's cold weather packing list, adopted by 3 companies for the February 2026 field exercise." (An accomplishment beyond the billet that still relates to an assigned duty.)

## Verbs that carry facts
led, trained, qualified, planned, executed, maintained, accounted for, inspected, corrected, wrote, briefed, deployed, completed, reduced, raised, closed

## Strike on sight
See scripts/common_checks.py STRIKE. The order's own strike (5.c(3)(a), 6.c(3)(a)): superlative adjectives, needless statistics, imprecise phrasing. Add for this product, as personal quality or potential words that paragraph 6.a(4) excludes from section C: "dedicated", "loyal", "enthusiastic", "motivated", "hard working", "selfless", "potential", "future", "attitude", "work ethic", "demeanor", "leader of Marines", "consistently", "always", "never fails", "excels".

## Never
- An award, Certificate of Commendation, Letter of Appreciation, Meritorious Mast, coin, or any other commendatory item in the accomplishments (6.c(1)(c)). They go in the list for the RS.
- Adverse material, disciplinary action, a pending investigation or NJP, about the MRO or anyone else (6.c(1)(c), 13.d).
- Participation as a member of a selection board or court-martial (6.b Note).
- A sentence about the marks, the ranking, the profile, or promotion. The RS marks; the MROW informs.
- UPPERCASE for emphasis, underlining, quotation marks, boldface, italics, or exclamation (5.c(3)(c), 6.c(3)(c)).
- An acronym the RS's reader outside the community would not know (5.c(4), 6.c(4)).
- Another Marine's name; `<MARINE>` or "the MRO" until substitution on the user's computer. Compare against a baseline, never against a named Marine.
- Em or en dashes. The bullet mark is a hyphen or a circle, which the order allows (5.c(1)(b)).

## Professionalism rules
- First person is not used; the input reads as the RS's section would ("Led", not "I led").
- Numbers as numerals when they are counts; dates as day month year.
- One claim per bullet. Short: the form's space, which the order does not measure in characters; the checker prints the count and the A-PES screen decides.
