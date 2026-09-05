# Endorsement voice

An endorsement is read by the next addressee up the chain, who has the basic correspondence in hand and wants to know one thing in the first sentence: what did this endorser do with it, and why.

## The forms the library's figures use (verbatim from them)
Identification line: "FIRST ENDORSEMENT on CO ltr 4400 (Code) dated (Date)"; "FIRST ENDORSEMENT on Supply Officer ltr 4400 (insert code) of (insert date)"; "FIRST ENDORSEMENT on ADMINISTRATIVE DISCHARGE BOARD REPORT of ____________".
First sentences: "I (do) (do not) recommend SNM for early release on (See note)." "I (agree)(disagree) with the board's findings and recommendations." "I certify that I have reviewed your wall to wall inventory results which was completed on (date) and concur with your recommendations." "I direct you to process the transactions required to properly adjust the property records."

## Shape (these sentences show shape only; no fact in them is to be taken, and the checker fails a lifted one)
"Forwarded, recommending approval. The Marine's request meets the three conditions in reference (a) paragraph 4; I verified the leave balance on 2 October 2026 and the platoon can absorb the absence."
"Forwarded, recommending disapproval. The request asks for a start date 11 days before the battalion's field exercise, in which the Marine is the section's only licensed operator; a start date after 30 November 2026 would be supported."
"Readdressed and forwarded." (When the endorser adds nothing and the chain requires the endorsement.)

## Verbs that carry the endorser's action
forwarded, recommend, concur, do not concur, certify, verified, reviewed, direct, return, readdressed

## Strike on sight
See scripts/common_checks.py STRIKE. Add for this product: "strongly recommend", "highly recommend", "wholeheartedly", "without reservation" (the reasons are the strength), "please", "kindly", "I feel", "I believe" (state what was verified), "at your earliest convenience".

## Never
- An endorsement that adds nothing and says a great deal.
- A recommendation with no reason the addressee can check.
- A Ref or Encl block for something the basic correspondence already lists (the endorsement adds; it does not repeat).
- A different Subj from the basic correspondence.
- Another Marine's name in the body; `<MARINE>` until substitution. The identification line names the originator by billet.
- Em or en dashes.

## Professionalism rules
- First person, as the figures use it. One action per endorsement, in the first sentence.
- Dates as day month year in the body; the heading date as the letter standard prints it.
- One paragraph is normal; two when there is a condition; three is a letter.
