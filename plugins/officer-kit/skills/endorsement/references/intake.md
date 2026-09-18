# Endorsement intake

One question at a time. "I do not know" is recorded as a gap, never filled. Ask what this endorsement raises, not what endorsements usually raise. Never put a candidate answer inside the question.

## 1. The basic correspondence
1. What is being endorsed: the originator by billet, the type (ltr, AA form, report, request), its SSIC, its originator code, and its date, exactly as they print on it? (These make the identification line; if any is missing the line carries a placeholder and the checker refuses it.)
2. Its Subj line, word for word. The endorsement repeats it.
3. Which endorsement is this in the chain (first, second, later)? Which activities have already endorsed it, by billet, and what did each say? (9-2.1.b numbers each endorsement "in the sequence in which it is added to the basic letter", so the ordinal counts endorsements, not echelons; and on a significant endorsement every prior endorser is a copy to addressee.)
4. What references and enclosures do the basic letter and the previous endorsements already identify, and through what letter and what number do they run? Who is already a copy to addressee on the basic letter or a previous endorsement? (9-2.3 and 9-2.4: this endorsement repeats none of them and continues the sequence for what it adds. 9-2.5: the earlier copy to addressees stay on a significant endorsement.)

## 2. What the endorser does
5. What is the endorser's action: forward, forward recommending approval or disapproval, concur or disagree with a finding, certify, accept, direct, or return? One of these, stated in the first sentence.
6. On what facts? What did the endorser see, check, or verify, with dates? An endorsement that recommends approval carries the reason the endorser has for it; an endorsement that disapproves carries the reason the requester will read.
7. Does the endorser add a reference or an enclosure that the basic correspondence did not have? Which, by exact title? (Only then does the endorsement carry a Ref or Encl block.)

## 3. Routing
8. To whom does it go, and via whom? Who signs it, personally or by direction? (Identity from the rules file's correspondence block; nothing guessed.)
9. Is there a deadline the basic correspondence sets that the endorsement must meet? By what date does it have to leave?
10. Same page or new page? Will the whole endorsement fit on the signature page of the basic letter or the preceding endorsement, and is it sure to be signed without revision (9-1, Figure 9-1)? A same page endorsement may omit the SSIC, subject, and the basic letter's identification symbols when the entire page will be photocopied (9-2.1.a); a new page endorsement repeats all three (Figure 9-2). `build_letter.py` renders a new page endorsement only.

## 4. Correlate to the standard
11. Hold the draft against standard.md: identification line complete; From, To, Via; the same Subj; Ref or Encl only if added; numbered paragraphs; first person; signature on the fourth line. Then run the 9-2.5 test: name the action and say whether this endorsement is significant ("forwarded, recommending disapproval", "readdressed and forwarded", substantive comments) or routine ("forwarded", "forwarded for consideration", "forwarded, recommending approval"). If it is significant, the copy to block carries the originator of the basic letter, every prior endorser, and all earlier copy to addressees, with "(complete)" beside anyone receiving the basic letter and the previous endorsements for the first time from this endorser (9-2.6.c). Say which of the things Chapter 9 does not settle this endorsement touches (a return without action, whether its comments are substantive, a level passed over) and mark each in the product as an assumption the signer closes.

## 5. The reader
12. How does this command write endorsements (one paragraph, "Forwarded, recommending approval." alone, or reasons; same page or new page; letterhead or none, which Chapter 9 does not settle in words)? Record in `Overrides/endorsement.md`.

## The quantification ladder
| Rung | Question |
|---|---|
| Action | What did the endorser do (review, verify, recommend)? |
| Scope | Against what: which records, which standard, which dates? |
| Result | What did the review find, in a number where there is one? |
| Comparison | Against the requirement the basic correspondence or the order sets |
| Consequence | What does the endorser want the addressee to do? |
Stop at the rung the endorser can defend.
