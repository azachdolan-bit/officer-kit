# Standard: the endorsement as SECNAV M-5216.5 Chapter 9 lays it out, with the endorsements the library's own orders reproduce

Status: built on the governing manual. SECNAV M-5216.5 (June 2015), the Department of the Navy Correspondence Manual, is in the library (`find_order.py "SECNAV M-5216.5"` reported FOUND on 18 September 2026: `library/5216.5  CH-1.pdf`). Chapter 9, Endorsements, pages 9-1 through 9-5, governs and is quoted below with its paragraph numbers: paragraph 9-1 General, paragraph 9-2 Format with subparagraphs 1 through 7, and Figures 9-1 (same page endorsement), 9-2 (new page endorsement), and 9-3 (assembly of an endorsement). The four endorsements that Marine Corps orders in the library reproduce as figures are kept under it, because they show how a Marine Corps unit fills the form the manual sets. The grid, margins, and signature placement come from the school correspondence standard the kit's `naval-letter` carries. What Chapter 9 does not settle is named at the end and is left as a gap, never filled from memory.

## What SECNAV M-5216.5 Chapter 9 settles (verbatim, with paragraph numbers; read from the manual on 18 September 2026)

### 1. The ordinal, and what the number counts (9-2.1.b)
"Number each endorsement in the sequence in which it is added to the basic letter. Indicate the numbers of the endorsement by using ordinal numbers such as FIRST, SECOND, THIRD, etc. Following the number, type "ENDORSEMENT on" and identify the basic letter using the same style as a reference line. When the heading exceeds one line, start the succeeding line with the word "on"."

So the ordinal counts the endorsements added to the basic letter, in the order they were added. It does not count echelons: an activity that adds no endorsement takes no number, and the next activity that does endorse takes the next ordinal. The manual's example, page 9-1, wraps the heading:

```
FIRST ENDORSEMENT on USS SCRANTON ltr 3000 Ser SSN 756/001 of
                    5 May 96
```

The rule says the succeeding line starts with the word "on"; the manual's own example wraps with the date indented instead. Figure 9-2 prints the line whole: "SECOND ENDORSEMENT on NAS Meridian ltr 5216 Ser 11/273 of 22 Apr 15" (SSIC, then Ser, then "of" and the date).

Where the line goes (9-2.1.a): "Start the endorsement line at the left margin on the second line below the date line. If the correspondence is classified, start the endorsement line on the second line below the classification line."

### 2. Same page or new page, and how each is laid out (9-1, 9-2.1.a, Figures 9-1 and 9-2)
9-1: "The length of the endorsement and the amount of space that is available on the basic letter or on the preceding endorsement determines if you should use a same-page or new page endorsement. If it will completely fit on the signature page of the basic letter or the preceding endorsement, you may add it to that page. If not, use a new-page endorsement."

Figure 9-1, the basic letter's paragraph 1: "An endorsement may be added to the bottom of a basic letter, like this one, or to a previous endorsement if: (a) All of the endorsement will fit on the page, and (b) it is sure to be signed without revision."

9-2.1.a: "When preparing a same-page endorsement, as long as the entire page will be photocopied, you may omit the SSIC, subject and the basic letter's identification symbols."

Figure 9-1, the first endorsement's paragraph 1: "A same-page endorsement may omit the SSIC, subject, and the basic letter's identification if the entire page will be photocopied. However, these elements are required on all new-page endorsements, such as the one on the next page."

Figure 9-2, paragraphs 1 and 2: "Start an endorsement on a new page. Number each page of your endorsement and continue the sequence of numbers from the previous endorsement or from the basic letter if you are the first endorser." "Every "new page" endorsement must repeat the basic letter's SSIC, identify the basic letter in the endorsement line, and use the basic letter's subject as its own."

What the two figures print, in order down the page:
- Same page (Figure 9-1): the basic letter, signed, on the originator's letterhead; a rule across the page under its signature; at the right, the endorser's Ser and date, with no SSIC; at the left margin "FIRST ENDORSEMENT" with nothing after it, the identification being omitted; From, To, Via; the numbered paragraph; the signature; then "Copy to:". No letterhead of the endorser's own, and no Subj.
- New page (Figure 9-2): the endorsing activity's letterhead; SSIC, Ser, date; the full endorsement line naming the basic letter; From and To; the basic letter's Subj; an Encl block for what this endorsement adds; numbered paragraphs; the signature, with "By direction" under the name where that applies; "Copy to:"; and the page number, continuing the basic letter's sequence.

### 3. References and enclosures the endorsement adds (9-2.3, 9-2.4)
9-2.3: "Do not repeat a reference in the reference line of your endorsement that has already been identified in the reference line of the basic letter or a previous endorsement. Identify only the references that you add. Assign a letter to all references you add by continuing the sequence of letters from the basic letter and previous endorsements. For example, if the basic letter and previous endorsements had references identified up to letter "f," the first reference of your endorsement would be letter "g.""

9-2.4: "Do not repeat an enclosure in your enclosure line that has already been identified in the enclosure line of the basic letter or prior endorsements. Identify only the enclosures that you add. Assign a number to all enclosures that you add by continuing the sequence of numbers from the basic letter and previous endorsements. For example, if the basic letter and previous endorsements had enclosures identified up to number "5," the first enclosure of your endorsement would be number "6.""

Figure 9-2 is the worked case: the basic letter carries "Encl: (1) Example of New-Page Endorsement" and the second endorsement's own block reads "Encl: (2) SECNAV M-5216.5".

### 4. The "Copy To:" block and who receives copies (9-2.5, 9-2.6)
9-2.5: "If your endorsement is significant and not routine, each activity that endorsed the basic letter before you and the originator of the basic letter shall be included as a copy to addressee on your endorsement. Additionally, all copy to addressees from the basic letter and previous endorsements shall be included as a copy to addressee. Significant endorsements include "forwarded, recommending disapproval," "readdressed and forwarded," and those with substantive comments. Routine endorsements include "forwarded," "forwarded for consideration," and "forwarded, recommending approval.""

This is the test the tool runs before it decides anything about a copy to block, because the manual's own examples name the actions on both sides:

| Significant (9-2.5) | Routine (9-2.5) |
|---|---|
| "forwarded, recommending disapproval" | "forwarded" |
| "readdressed and forwarded" | "forwarded for consideration" |
| "those with substantive comments" | "forwarded, recommending approval" |

Significant, so the block carries: the originator of the basic letter; each activity that endorsed it before you; and every copy to addressee from the basic letter and previous endorsements. Routine, so the manual does not require the block. Note that "forwarded, recommending approval" is routine in the manual's own list, however much reasoning the endorser puts under it; it is disapproval, readdressing, and substantive comment that turn an endorsement significant.

9-2.6, forwarding your endorsement and copies: "When forwarding your endorsement to the next via addressee or to the action addressee, you must also do the following: a. Attach any enclosure you identified in your endorsement to the original for forwarding to the action addressee. b. Forward one copy of your endorsement to each remaining addressee. c. Forward one copy of your endorsement to each copy to addressee. Include a copy of any enclosure you added. If a copy to addressee will be receiving the basic letter and previous endorsements for the first time from you, to the right of each of these addressees, type the word "complete" in parentheses to show that your endorsement includes the basic letter, enclosures, and prior endorsements."

Both figures print the block at the left margin below the signature, in the form "Copy to:" and then the activity with its code on the next line ("NAS Meridian (Code 11)"), and both carry the footnote "*Prior endorser included because second endorsement is significant."

### 5. What an endorsement may and may not change (9-1, 9-2.2, 9-2.3, 9-2.4, Figure 9-2)
May: "When a letter is transmitted via your activity, use an endorsement to forward comments, recommendations, or information. While an endorsement is mostly used to transmit correspondence through the chain of command, you may also use it to redirect a letter." And on routing, 9-1: "Additionally, a "Via" addressee may alter the order of any remaining "Via" addressees or add others." 9-2.2: "When preparing your endorsement, include in the "Via:" line any remaining "Via" addressees, if any. If there is only one via addressee remaining, do not number it. If there is more than one remaining, number the remaining addresses starting with the number (1) in parenthesis and consecutively number the rest." It may add references and enclosures (9-2.3, 9-2.4).

May not: reply to a routine letter with an endorsement (9-1: "Do not use an endorsement to reply to a routine letter."); repeat a reference or an enclosure the basic letter or a previous endorsement already identified (9-2.3, 9-2.4); or take its own subject, since every new page endorsement "must repeat the basic letter's SSIC, identify the basic letter in the endorsement line, and use the basic letter's subject as its own" (Figure 9-2).

### 6. Letterhead (Figures 9-1 and 9-2, 9-2.1.a)
Chapter 9's prose sets no letterhead rule in words. What the figures print: Figure 9-2, the new page endorsement, is on the endorsing activity's own letterhead ("DEPARTMENT OF THE NAVY", "NAVAL AIR FORCE ATLANTIC", "NORFOLK VA 23511-2494"), with the SSIC, Ser, and date under it. Figure 9-1, the same page endorsement, has no letterhead of its own: it sits under the basic letter's letterhead below a rule, carrying only the endorser's Ser and date, and 9-2.1.a permits it to omit "the SSIC, subject and the basic letter's identification symbols" as long as the entire page will be photocopied. The kit's letter standard builds the student letter with no letterhead. Which a unit uses is the command's practice, recorded in `Overrides/endorsement.md`.

### 7. Assembly for signature and mailing (9-2.7, Figure 9-3)
9-2.7: "Figure 9-2 shows a suggested way to assemble an endorsement for signature and mailing." (The chapter's own cross reference; the assembly drawing is Figure 9-3.) Figure 9-3's stack, before signature: "1. Briefing sheet as prescribed locally, usually omitted if letter is short or self explanatory. 2. Your endorsement. 3. Earlier endorsements, most recent on top. 4. Basic letter. 5. Earlier enclosures, plus any you added on top. 6. Copies of your endorsement for remaining Via addressees. 7. Envelope or mailing label, if required. 8. Copies of your endorsement for copy to addressees. 9. Envelope or mailing label, if required. 10. Official file copy of letter with enclosures. Left margin exposed so reviewers can initial and date there. 11. Background material, such as incoming letter, referenced documents." After signature, items 2 through 7 go to the next via addressee or the action addressee, 8 and 9 are mailed, and 10 and 11 are filed.

## What the library's own figures show (verbatim, page images and pdftotext, 5 September 2026)

### MCO 1900.16 (26 Nov 2013), enclosure (1), Figure 6-5 (PDF page 410): a unit's endorsement on a Marine's request
```
                                            (Letterhead)

FIRST ENDORSEMENT ON (SNM'S LETTER/AA FORM) OF (DATE)

From:       (Unit)
To:         General Court-Martial Convening Authority
Via:        (Chain of Command)

Subj:        EARLY RELEASE TO FURTHER EDUCATION OF (SNM)

Ref:        (a) MCO 1900.16, par. 6405

1.     Per the reference, the following is submitted:
[...]
3.     I (do) (do not) recommend SNM for early release on (See note).
[...]
                                                     (Signature)
```

### MCO 1900.16 CH 2 (15 FEB 2019), Appendix L, Figure L-10 (PDF page 662): Command Letter of Endorsement for Administrative Discharge
```
                                                                           SSIC
                                                                           Code
                                                                           Date

FIRST ENDORSEMENT on ADMINISTRATIVE DISCHARGE BOARD REPORT of ____________

From:   Commanding officer (Convening Authority)
To:     Separation Authority
Via:    (Chain of Command)

Subj:   RECOMMENDATION FOR ADMINISTRATIVE DISCHARGE OF (GRADE, FULL
        NAME, EDIPI/MOS, COMPONENT)

Encl:   (1) Defense counsel comment on board (if any)
        (2) Recorder's response to Counsel for the
            Respondent's comment
        (3) (Other enclosures included by convening authority)

1. As indicated by enclosure (1), an administrative discharge board convened
to hear this case. [...]
2. I (agree)(disagree) with the board's findings and recommendations.
[...]
                                        SIGNATURE
```

### NAVMC 4000.5D, enclosure (12), page 119: Supply Officer (SupO) Appointment Endorsement
```
                                   [Insert UnitLetterhead]
                                                                                            4400
                                                                                           (Code)
                                                                                           (Date)
      FIRST ENDORSEMENT on CO ltr 4400 (Code) dated (Date)

      From:     (Rank, First Name MI. Last Name)
      To:       Commanding Officer

      Subj:     APPOINTMENT AS SUPPLY OFFICER/ACCOUNTABLE
                PROPERTY OFFICER

      Ref:      (a) DOD 7000.14R
                (b) MCO 4400.201, Volume 3

      Encl:     (1) Relieved Supply Officer's Certificate of Relief
                (2) Endorsement to Relieved Supply Officer's Certificate of Relief

      1. I have read and familiarized myself with the duties and responsibilities as outlined in
      the references and the appointment order. I have reviewed this account along with
      Enclosure (1) and documented the results of this review in Enclosure (2). I accept these
      duties and responsibilities as the Supply Officer for this account.

                                             (Signature)
                                             (FI. MI. Last Name of SUPO)
```

### NAVMC 4000.5D, enclosure (12), page 129: Commander's Annual Physical Inventory Certification
```
                                 [Insert Unit Letterhead]
                                                                      4400
                                                                      (code)
                                                                      (Date)

      FIRST ENDORSEMENT on Supply Officer ltr 4400 (insert code) of (insert date)

      From: Commanding Officer
      To:   Supply Officer

      Subj: (insert inventory type) WALL TO WALL INVENTORY RESULTS FOR (insert
             DoDAAC)

      1.  I certify that I have reviewed your wall to wall inventory results
      which was completed on (date) and concur with your recommendations.
[...]
      3. I direct you to process the transactions required to properly adjust
      the property records.
[...]
                                              (Signature)
                                              (FI. MI. LAST Name of CO)
```

## What the four figures settle (how a Marine Corps unit fills the form the manual sets)
1. Heading block: SSIC, code, date at the right, as on a letter (Figure L-10, both NAVMC pages).
2. The identification line, at the left margin, on the second line below the date: the ordinal in capitals, the word ENDORSEMENT, "on", then the basic correspondence named by originator, "ltr", SSIC, code, and "of" or "dated" plus its date (both NAVMC pages: "FIRST ENDORSEMENT on CO ltr 4400 (Code) dated (Date)"; "FIRST ENDORSEMENT on Supply Officer ltr 4400 (insert code) of (insert date)"). Where the basic correspondence is not a letter, the figure names the document (Figure L-10: "on ADMINISTRATIVE DISCHARGE BOARD REPORT of ____"; Figure 6-5: "ON (SNM'S LETTER/AA FORM) OF (DATE)").
3. From, To, and Via where there is routing, on the second line below the identification line, in the letter's labelled form (all four figures).
4. Subj: the subject of the basic correspondence, in capitals (all four).
5. Ref and Encl blocks only when the endorsement itself adds a reference or an enclosure (Figure 6-5 adds a Ref; Figure L-10 and page 119 add Encl; page 129 adds neither).
6. Numbered paragraphs that do one of the things the figures do: forward with a recommendation ("I (do) (do not) recommend"), state the endorser's position ("I (agree)(disagree)"), certify ("I certify that I have reviewed"), accept or direct ("I accept these duties", "I direct you to"). First person is the figures' voice.
7. Signature block as on a letter: the fourth line below the last line of text, from page centre (the kit's correspondence standard; the figures show the signature at the right centre).

## From the kit's correspondence standard (naval-letter/references/standard.md, the school handout B020069XQ over SECNAV M-5216.5)
Times New Roman 12, 1 inch margins, 13.8 pt line pitch, every named gap a whole number of lines, Subj in capitals as a phrase, Ref lettered (a) (b), Encl numbered (1) (2), every reference cited and every citation resolving, signature on the fourth line, no dashes, continuation page furniture, and the date as day, abbreviated month, two digit year. `build_letter.py` lays all of it out; `qc_letter.py --kind endorsement` and `measure_pdf.py` check it.

## What Chapter 9 does not settle
Named, not filled. Chapter 9 is the whole of the manual's endorsement chapter; these are questions it does not reach, and on each the command's practice in `Overrides/endorsement.md` and the endorsements in `Reference/Exemplars/endorsement/` govern until a source that does reach them is on disk.
- The wording for returning correspondence without action. Chapter 9 names forwarding, redirecting, and the significant and routine actions in 9-2.5; it gives no form of words for a return and no rule for when one is used. "Returned" in `voice.md` comes from practice, not from this chapter.
- What counts as "substantive comments" in 9-2.5. The manual makes such an endorsement significant and gives no test for it, so the endorser decides and the checker warns rather than fails when the action is not one of the six the paragraph names.
- Whether an echelon in the chain may be passed over. 9-2.1.b settles the numbering (the sequence in which endorsements are added), and 9-1 lets a via addressee "alter the order of any remaining "Via" addressees or add others", but the chapter does not say whether an endorser may be skipped.
- Whether a unit's endorsement carries letterhead, as a rule in words. The figures show what item 6 above records; the chapter states no rule.
- Who may sign an endorsement, and when "By direction" is used. Figure 9-2 prints it under the signature; the chapter's text does not set the authority.
- What an endorsement does about an error in the basic letter, and whether correspondence may be withdrawn once endorsed. The chapter is silent on both.

## What the tool cannot yet render
The manual settles these; the kit's builder does not yet produce them, so they are corrected on the page before signature and the checker says so in its output.
- `naval-letter/scripts/build_letter.py` prints no "Copy to:" block. A significant endorsement's block (9-2.5) is typed onto the page after the build; `endorsement_check.py` still checks the spec's `copy_to` list against 9-2.5.
- `build_letter.py` letters a Ref block from (a) and numbers an Encl block from (1). Where the basic letter and previous endorsements already carry some, 9-2.3 and 9-2.4 require the sequence to continue, and `endorsement_check.py` prints the letters and numbers the added items must show.
- `build_letter.py` builds a new page endorsement. A same page endorsement (9-1, 9-2.1.a) is typed onto the signed page of the basic letter or the preceding endorsement.
