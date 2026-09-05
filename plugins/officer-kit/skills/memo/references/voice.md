# Memo voice

The publication's own words on how these papers read: "Write in short, clear, direct conversational style"; "Use the active voice and avoid jargon; brevity is expected; identify all acronyms"; "brief, 'telegraphic' style that can stand alone"; "Reduce recommendations to clear, concise statements that permit straightforward approval or disapproval"; "Only essential facts". A reader who has to look something up has been failed by the paper.

## The captions and headings, exactly as the appendices print them
MEMORANDUM FOR THE RECORD. POINT PAPER with 1. BACKGROUND, 2. DISCUSSION, 3. RECOMMENDATION, Prepared by, Approved by. POSITION/DECISION PAPER with 1. Purpose, 2. Major Points, 3. Discussion, 4. Recommendation, Prepared by, Approved by. TALKING PAPER with FOR USE BY, SUBJECT, BACKGROUND, DISCUSSION, RECOMMENDATION, APPROVAL, ACTION OFFICER. INFORMATION PAPER with Subject, 1. Purpose, 2. Key Points, Prepared by.

## Shape (these sentences show shape only; no fact in them is to be taken, and the checker fails a lifted one)
MFR: "On 3 November 2026 the S-4 and the company gunnery sergeants met to settle the turn in schedule for the field exercise. The S-4 directed that all serialized gear be turned in by 1600 on 14 November 2026; the company representatives concurred. Action underway: the company is publishing the turn in schedule by platoon on 5 November 2026."
Point paper: "1. BACKGROUND. Rifle range scheduled 8 to 10 December 2026; the company last fired in June 2026 with 4 unqualified. 2. DISCUSSION. a. 118 of 121 Marines available; 3 on light duty. b. Range control requires the RSO letter 10 days prior. 3. RECOMMENDATION. Approve the range order for signature by 26 November 2026."
Decision paper purpose: "Obtain the commanding officer's decision on whether the company holds the quarterly inventory before or after the field exercise."

## Verbs that carry facts
met, directed, decided, concurred, recorded, confirmed, scheduled, completed, requires, recommends, approve, disapprove

## Strike on sight
See scripts/common_checks.py STRIKE. Add for this product: "it should be noted that", "as you are aware", "in order to", "it is recommended that consideration be given" (write "Recommend approve"), "various", "numerous" (count them), "leverage", "synergy", "robust", "going forward", "touch base".

## Never
- An MFR that argues. It records who, when, what was said or decided, and what is now underway.
- A recommendation the reader cannot approve or disapprove with a signature.
- A reference listed and not used in the discussion.
- A paper over its length with nothing moved to a tab.
- Another Marine's name; `<MARINE>` or the billet. Participants in an MFR are billets.
- Em or en dashes.

## Professionalism rules
- Dates as day month year. Times as four digits. Counts as numerals.
- One idea per paragraph or tick. Acronyms spelled out once.
- Unclassified papers carry no classification markings.
