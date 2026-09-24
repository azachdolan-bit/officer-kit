---
name: board-prep
description: >
  Prepares an officer's own record for a promotion selection board to MARADMIN 622/25 (FY28 officer
  boards), MCO 1553.4B, and ALMAR 024/25: the board's convening and correspondence due dates read
  from the message's table, the OMPF document cutoff two weeks before convening, the OMPF and Master
  Brief Sheet audit item by item with the date each was verified, fitness report gaps and the fix
  the message names, the photo line, PME required for the grade against PME held, the reading log
  against the FY26 Commandant's list, and, if the officer wants one, the letter to the President of
  the Board under the message's rules (addressee, signature, unclassified, enclosures listed, third
  party letters only under a signed cover letter, Portal or mailbox, the cutoff). It never predicts
  the result. Use when the user says "board prep", "I am in zone", "letter to the board", "letter to
  the president of the board", "audit my OMPF", "check my MBS", "am I PME complete", "reading list
  for the board", or "when is my board".
metadata:
  version: "0.1.0"
  status: incomplete
---

# Board preparation

The message makes the officer, not the unit, responsible: "Each officer is personally responsible for ensuring the accuracy and completeness of their Official Military Personnel File (OMPF) and Master Brief Sheet (MBS) before the date the board convenes," and correspondence to the President of the Board that reaches MMPB-10 after 2359 EST on the Bd.Corr.Due date "will not be accepted under any circumstances." The tool reads the board's two dates from the paragraph 1 table, sets the OMPF document cutoff two weeks before convening as paragraph 7.a says, records what the officer verified and on what date, lays PME held against what MCO 1553.4B requires for the grade, logs reading against the titles ALMAR 024/25 prints, and drafts the letter only if the officer wants one and only inside the message's rules. It prepares the record; the board decides, and nothing in the product speaks to that. Two parts are unverified because their publications are not in the library: the Photo section (MARADMIN 622/25 says nothing about a photograph; MCO P1400.31D and the board's convening MARADMIN would settle it) and the Zone line (the zone MARADMIN for the officer's board, published 30 to 60 days before it). Both are written as "not in the library" or "not yet announced" until the officer supplies the source.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Read first

1. `references/standard.md`: MARADMIN 622/25 paragraph 1 (the table and its notes), paragraphs 2 to 6 (zones, eligibility, TIG, opt out), paragraph 7 (the audit, fitness reports, PME, civilian education), paragraph 8 (correspondence), paragraphs 9 to 11; MCO 1553.4B enclosure (1) by grade level; ALMAR 024/25 paragraphs 1 to 4; the Not in the library list.
2. `references/intake.md`: the questions, one at a time.
3. `references/voice.md`: the message's words, the audit line, the strike list.
4. `references/exemplar.md`: read only after the fact list is confirmed (step 6). It teaches shape and its content is not to be taken; the checker fails a lifted phrase.

## Your own material (read first, every time)

1. `Overrides/board-prep.md`: how this officer's monitor or career counselor wants the correspondence laid out, the MMPB-10 template as it stands on the officer promotion homepage, anything the convening MARADMIN for this board changed. The command's way wins; say in one line what it changed.
2. `Reference/Exemplars/board-prep/`: preparations and letters this officer or this command used, sanitized. They beat the plugin's fictional exemplar.
3. `<MARINE>` throughout; the name goes on the letter on the user's computer with `security-check/scripts/substitute.py`. The audit records that a document is present or absent by date; the content of an adverse document, a medical entry, or a family circumstance stays out of the product.
4. When the board's result is known or the letter came back, `aar` captures what changed.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question. The date each item was verified and the board's two dates from the table are the questions this product turns on; ask them plainly.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

## Workflow

```
Board preparation:
- [ ] 1. Frame: the board in the table's words (Selection To, Component), its convening date and Bd.Corr.Due date read from the paragraph 1 table; the officer's grade, DOR, component, PMOS; TIG against paragraph 4.a; zone if the zone MARADMIN is out, else "not yet announced"
- [ ] 2. Dates: convening; correspondence NLT 2359 EST on the Bd.Corr.Due date; OMPF documents to MMPB-22 two weeks before convening; fitness reports to MMPB-23 on the PES timelines; Portal access 60 days out; reserve RQS by the correspondence cutoff
- [ ] 3. Audit, one item at a time: OMPF, MBS, additions and deletions in the last 12 months, fitness report listing, PME on the MBS and certificates in the OMPF, civilian education in MCTFS, contact data in MOL and MCTFS, classified reports, CRCR for reserve; each verified with the date it was seen or marked No with the fix, its recipient, and its deadline
- [ ] 4. Fitness reports: periods end to end; each gap as dates and a day count; under or over one year old and the fix paragraph 7.c.1 names; what was sent to MMPB-23 and when
- [ ] 5. PME: what enclosure (1) requires for the grade, what is held with completion dates, whether the MBS and OMPF show it; sub courses with evidence if not complete. Reading: FY26 titles read, by section, with dates; Archive titles apart
- [ ] 6. Read back the fact list; the user confirms; nothing else goes in. Now read exemplar.md for shape
- [ ] 7. Letter: only if the officer wants one; what the record does not show, one point per paragraph, each tied to an enclosure; addressed per 8.a, signed per 8.b, unclassified, enclosures listed, third party letters only as listed enclosures, Portal or mailbox, submission date against the cutoff
- [ ] 8. Draft board_prep.md in the shape below
- [ ] 9. python3 scripts/board_prep_check.py board_prep.md exits 0
- [ ] 10. Strike pass with voice.md; the letter stays short
- [ ] 11. Saved to Career/Boards/<board> <FY> board prep <date>.md; the officer uploads the letter to the Portal or sends it to the mailbox and keeps the confirmation
- [ ] 12. Learning: what the board or MMPB-10 did differently, via aar
```

## The product (board_prep.md)

```
# Board preparation
Officer: <MARINE>, <grade>, <Active | Reserve (SMCR, IMA, IRR) | AR>, <PMOS>   Board: <Selection To> <Component> (FY28)   Convening: <date from the table>   Board correspondence due: <Bd.Corr.Due from the table>
Zone: <in zone | above zone | below zone, with the zone MARADMIN date | not yet announced>   Prepared: <date>
References: MARADMIN 622/25 paragraphs 1, 7, 8; MCO 1553.4B enclosure (1); ALMAR 024/25

## Board and dates
Board: <Selection To> <Component>, convenes <date> (MARADMIN 622/25 paragraph 1 table).
Correspondence to the President of the Board: received by CMC (MMPB-10) NLT 2359 EST <Bd.Corr.Due> (paragraph 1 table; statutory, cannot be waived; late correspondence not accepted).
OMPF documents other than fitness reports: received by CMC (MMPB-22) by <convening minus two weeks>, two weeks prior to the convening date (paragraph 7.a).
Fitness reports: to CMC (MMPB-23) by the timelines in MCO 1610.7B (paragraph 7.c); administrative changes may take up to 30 days (paragraph 7.c.2).
<Portal access; TIG; one year rule; RQS line for reserve; opt out or deferment if either applies>

## OMPF and MBS audit
- <item>: Verified: Yes <date seen>. <what was seen>          (or)  Verified: No; <fix, to whom, sent on date; see section>
<one line each: OMPF, MBS, additions and deletions in the last 12 months, fitness report listing, PME on MBS and certificates in OMPF, civilian education in MCTFS, contact data in MOL and MCTFS, classified reports, CRCR for reserve, corrections submitted>

## Fitness reports
Periods on the MBS: <start to end; ...>.
Gaps: none.   (or)   Gap: <start> to <end>, <n> days, <occasion>. <under or over one year old; the paragraph 7.c.1 fix; sent to MMPB-23 on date; follow up date>
In processing: <report or none>.

## Photo
MARADMIN 622/25 states no photograph requirement. What governs a photograph for this board is not in the library (MCO P1400.31D; the convening MARADMIN). <who said what, on what date, recorded as their statement>

## PME
Grade: <grade>. Required for the grade (MCO 1553.4B enclosure (1), <level> paragraph <n>): <the order's options>.
Held: <course, completion date, on the MBS yes or no, certificate in the OMPF yes or no>.
Status: <PME complete for the grade on date | not complete; sub courses done with evidence; letter to the board yes or no>. The order: completion of PME "cannot be tied directly to promotion" (enclosure (1) paragraph 1.d).

## Reading
FY26 CPRL (ALMAR 024/25): six sections, Commandant's Choice, Heritage, Innovation, Leadership, Strategy, and Foundational. The ALMAR: "should aim to complete at least five titles annually."
Read from the FY26 list:
- "<title as the ALMAR prints it>" (FY26 CPRL, <section>): read <month year>
Archive: <earlier list titles, or none logged>.
Titles read from the FY26 list in the last 12 months: <n>.

## Letter to the board
None: the officer does not submit correspondence (paragraph 8: encouraged, not required).
   (or)
The officer wants one. Purpose: <what the record does not show>.
From: <grade> <MARINE>, U.S. Marine Corps <Reserve>
To: President, FY28 USMC/USMCR <grade> (<competitive category>) Promotion Selection Board
Subj: CORRESPONDENCE TO THE FY28 USMC/USMCR <GRADE> PROMOTION SELECTION BOARD
Ref: (a) MARADMIN 622/25
Encl: (1) <each document, dated>
1. <one point, tied to an enclosure or a record fact>
Signed: <MARINE>, <ink | CAC digital signature>, <date>
Submission: <Board Correspondence Portal, uploaded date, confirmed in the Portal | email to officerpromotions@usmc.mil, date, subject line per 8.g, automatic reply kept>; due NLT 2359 EST <Bd.Corr.Due>.
```

## Rules

- The board in the table's words and its two dates as the table prints them. The checker carries the paragraph 1 table and fails a header or deadline line that disagrees with it. The table's Bd.Corr.Due date is used as printed; the footnote's "10 calendar days" is never used to compute a later one.
- The OMPF document cutoff is two weeks before the convening date (paragraph 7.a), to MMPB-22, not to the board. Fitness reports go to MMPB-23 on the PES timelines (paragraph 7.c); a report sent to the President of the Board does not enter the OMPF.
- An audit item is verified on a date or it is not verified. "Yes" with no date fails. "No" names the fix, the recipient, and when it went.
- A fitness report gap is stated as dates. Under one year old: a reconstructed original. Over one year old: certified true copies by the RS or RO (paragraph 7.c.1). Administrative changes may take up to 30 days (paragraph 7.c.2); the follow up date is in the product.
- Photo: the message says nothing about it, and the publication that would is not in the library. The section says so and records who said what, with a date, as their statement.
- PME: required for the grade from MCO 1553.4B enclosure (1) first, then held with dates, then status. "PME complete" carries a completion date. The order says PME "cannot be tied directly to promotion"; the product never says it is required for promotion.
- Reading: titles as the ALMAR prints them, by section, with the month read; the checker fails a title marked FY26 CPRL that the ALMAR does not print. The ALMAR's aim is five a year; the log counts what was read and does not round up.
- The letter is optional (paragraph 8). If written: addressed as 8.a says; signed in ink or by CAC (8.b); unclassified (8.c); every enclosure listed, and a letter from anyone else only as a listed enclosure under the officer's signed cover letter (8.d); by the Portal or the organizational mailbox (8.e to 8.g); received by 2359 EST on the Bd.Corr.Due date (paragraph 1). It never asks the board to add anything to the OMPF (paragraph 8). A request for non selection is written with the 8.h consequences beside it.
- Nothing about the result. No "will be selected", "should pick up", "will be promoted", or any sentence about the officer's chances. The checker fails them.
- Nothing medical, family, financial, or from an investigation; an adverse document is present or absent by date, not described.
- `<MARINE>` until substitution on the user's computer. No em or en dashes.

## Utility scripts

- `scripts/board_prep_check.py board_prep.md`: title and label; the board named in the paragraph 1 table's words and the header dates equal to the table's (fail); grade paired with the board per paragraph 4.a (fail); every dated deadline line in Board and dates equal to the table's date, and the OMPF document line two weeks before convening (fail); an approximate deadline (fail); audit items marked Verified: Yes with no date (fail), unverified items with no fix (warn), the paragraph 7, 7.c, 7.d, 7.e, 9, 10, 11 items present (warn); a fitness report gap with no dates (fail); Photo without the not in the library line (warn); the PME section naming the course enclosure (1) requires for the grade (fail), PME complete with no date (fail), PME tied to promotion (fail); a title marked FY26 CPRL that the ALMAR does not print (fail), fewer than five titles (warn); the letter, if drafted: addressee per 8.a, signature per 8.b, unclassified per 8.c, enclosures listed and third party material under a cover letter per 8.d, method per 8.e, submission date on or before the cutoff, OMPF request (each a fail, the rule quoted), non selection request (warn); a prediction of the result, a name, a lifted exemplar phrase, blocked content, and dashes (fail). Exit 1 on any failure.
