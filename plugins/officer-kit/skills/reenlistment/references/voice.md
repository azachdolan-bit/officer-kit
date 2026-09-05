# Reenlistment voice

The form asks for brief comments that justify the box checked. The reader is the next signer up the block and, at the end, CMC (MMEA-6), which reads hundreds of these and decides. The comments exist to make the box true.

## The form's own words (use them exactly, never a paraphrase)
Recommended with Enthusiasm (Top 25 %). Recommended with Confidence (Top 50 %). Recommended with Reservation. Not Recommended. "Does SNM meet all reenlistment prerequisites: Yes / No."

## The order's three heads, in this order
Conduct, then performance, then future potential as it relates to rank, age, experience, and maturity (paragraph 4.b). One or two sentences each, facts with dates and counts.

## Sentences that carry the tier
These sentences show shape only. No number, date, or fact in them is to be taken into a product; the intake supplies those, and `reenlistment_check.py` fails a draft that lifts a phrase from here.

"Ranks 3 of the 14 sergeants known to me." (The population sentence. Without it the top two tiers are adjectives.)
"No adverse material on this contract; pro/con 4.6/4.7." (Conduct as a record fact.)
"Led a 12 Marine section through two deployments; zero preventable equipment losses against a battalion average of three per section." (Performance with a comparison.)
"Has done the platoon sergeant's job for four months while the billet was gapped; ready for staff sergeant's responsibilities now." (Potential tied to the next grade.)
"Recommended with Reservation. Two NJPs on this contract (12 March 2025, 4 August 2026), the second for the same offense after counseling; performance in the billet is otherwise at standard." (The reason, as facts, when the order requires one.)

## Verbs that carry facts
led, trained, qualified, maintained, accounted for, corrected, raised, reduced, deployed, completed, passed, ranked

## Strike on sight
See scripts/common_checks.py STRIKE. Add for this product: "asset to the Marine Corps", "great Marine", "hard charger", "would follow anywhere", "no doubt", "definitely", "strongly recommend" (the box is the recommendation; the comments are the reasons), "will make an outstanding", "should be retained at all costs".

## Never
- A tier above what the population sentence supports.
- "Recommended with Enthusiasm" with no number under it.
- Anything about the decision: MMEA-6 decides, and even a "not recommended" request goes forward.
- Medical, family, or financial detail; the prerequisites screen records yes, no, or waiver requested, not the circumstances. The order itself keeps the CO's certification "yes" on one item to protect the Marine's privacy.
- Another Marine's name. `<MARINE>` until substitution on the user's computer.
- Em or en dashes.

## Professionalism rules
- Grade and label after the first full mention ("Sergeant <MARINE>", then "the Marine" or "Sergeant <MARINE>").
- Numbers as numerals when they are counts; dates as day month year.
- One claim per sentence. Brief means the comments field on the form, not a page.
