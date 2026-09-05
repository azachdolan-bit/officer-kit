# Meritorious Mast and Certificate of Commendation voice

The reader of a Meritorious Mast is the Marine, and the Marines in the formation who watched the thing happen and will hear it read. The reader of a Certificate of Commendation is the same formation and, years later, a board member turning the page in the OMPF. Both readers decide the same thing from the text: whether what it describes happened, and whether it was worth the paper. Facts with counts and dates answer that. Adjectives do not.

## The order's own words for the threshold (use as the test, not as the text)
"noteworthy or commendable beyond the usual requirements of duty" and "exceptional industry, judgment, or initiative" (enclosure (2) paragraph 8.g). The text names the industry, the judgment, or the initiative and the fact that shows it. It does not repeat the adjective; "exceptional" is on the strike list because it is the criterion, not the evidence.

## Shape
- Opening: what the Marine is recognized for, in one sentence, with the billet and the period or date.
- Body: two to four sentences, each carrying one fact from the Facts section: a count, a date, a comparison, a consequence.
- Close: one sentence on what the unit got. No line about the Marine's future, a board, or a promotion.
- A Certificate of Commendation text also names the awarding officer by billet and echelon in the signature block; the order's signature line rule (8.e(5)) is name, grade, official title, unit identification, and the name is `<MARINE>`'s commander's, added on the user's computer.

## Sentences that carry the shape
These sentences show shape only. No number, date, or fact in them is to be taken into a product; the intake supplies those, and `meritorious_mast_check.py` fails a draft that lifts a phrase from here.

"Corporal <MARINE> is commended for the recovery of the company's armory accountability between 3 and 21 March 2026." (What, billet, dates.)
"Rebuilt 212 serialized item records in 14 working days and closed the inspection with zero discrepancies against six the quarter before." (Count, duration, comparison.)
"Trained the four other Marines of the section on the new procedure so the section passed the follow on inspection without the Marine present." (Consequence the unit kept.)
"The battalion regained a green armory rating for the first time in three quarters." (What the unit got, as a fact.)

## Verbs that carry facts
recovered, rebuilt, trained, qualified, accounted for, corrected, reduced, raised, completed, passed, repaired, returned, identified, closed

## Strike on sight
See scripts/common_checks.py STRIKE. Add for these products: "asset to the Marine Corps", "great Marine", "hard charger", "goes above and beyond", "second to none", "countless", "numerous", "always", "never fails", "selfless", "consummate professional", "sets the example" (say what the example was).

## Never
- A number, date, or count in the text that the Facts section does not carry. The text proves nothing on its own; the facts prove the text.
- A Meritorious Mast for service already recognized, or about to be recognized, by a Letter of Appreciation, a Certificate of Commendation, or a personal decoration (8.g(1)).
- A Meritorious Mast text that describes what the level check says is a Certificate of Commendation or a personal decoration. The recognition follows the facts, not the other way round.
- A promise: promotion, a board, a future award, "will make an outstanding".
- A grade doing the work of the facts. The order: level of responsibility, not the grade of the individual (paragraph 6).
- Medical, family, financial, disciplinary, or investigation content about anyone.
- A unit by name or number in the draft; echelon only until substitution on the user's computer. Another Marine's name; `<MARINE>` throughout.
- Em or en dashes.

## Professionalism rules
- Grade and label at the first mention ("Lance Corporal <MARINE>"), then "the Marine" or "Lance Corporal <MARINE>".
- Numerals for counts; dates as day month year.
- One claim per sentence. No semicolons in the text.
- Abbreviations the formation would not know are spelled out; the Marine's family reads the copy.
