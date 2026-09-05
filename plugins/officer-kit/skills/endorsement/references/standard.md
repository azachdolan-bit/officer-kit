# Standard: the endorsement as the orders in the user's library lay it out; SECNAV M-5216.5 (the governing manual) is NOT in the library

Status: INCOMPLETE. The Department of the Navy Correspondence Manual, SECNAV M-5216.5, governs endorsements and is not on disk (`find_order.py "SECNAV M-5216.5"` reported NOT IN THE LIBRARY on 5 September 2026; the user's rules file lists it among the manuals to download into Reference). Until it is, this tool draws its layout from four endorsements that Marine Corps orders in the library reproduce as figures, and from the school correspondence standard the kit's `naval-letter` already carries (grid, margins, signature, references and enclosures). What those sources settle is below. What only the manual settles is listed at the end and is left unverified in the product, never filled from memory.

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

## What the four figures settle (the layout the tool builds)
1. Heading block: SSIC, code, date at the right, as on a letter (Figure L-10, both NAVMC pages).
2. The identification line, at the left margin, on the second line below the date: the ordinal in capitals, the word ENDORSEMENT, "on", then the basic correspondence named by originator, "ltr", SSIC, code, and "of" or "dated" plus its date (both NAVMC pages: "FIRST ENDORSEMENT on CO ltr 4400 (Code) dated (Date)"; "FIRST ENDORSEMENT on Supply Officer ltr 4400 (insert code) of (insert date)"). Where the basic correspondence is not a letter, the figure names the document (Figure L-10: "on ADMINISTRATIVE DISCHARGE BOARD REPORT of ____"; Figure 6-5: "ON (SNM'S LETTER/AA FORM) OF (DATE)").
3. From, To, and Via where there is routing, on the second line below the identification line, in the letter's labelled form (all four figures).
4. Subj: the subject of the basic correspondence, in capitals (all four).
5. Ref and Encl blocks only when the endorsement itself adds a reference or an enclosure (Figure 6-5 adds a Ref; Figure L-10 and page 119 add Encl; page 129 adds neither).
6. Numbered paragraphs that do one of the things the figures do: forward with a recommendation ("I (do) (do not) recommend"), state the endorser's position ("I (agree)(disagree)"), certify ("I certify that I have reviewed"), accept or direct ("I accept these duties", "I direct you to"). First person is the figures' voice.
7. Signature block as on a letter: the fourth line below the last line of text, from page centre (the kit's correspondence standard; the figures show the signature at the right centre).

## From the kit's correspondence standard (naval-letter/references/standard.md, the school handout B020069XQ over SECNAV M-5216.5)
Times New Roman 12, 1 inch margins, 13.8 pt line pitch, every named gap a whole number of lines, Subj in capitals as a phrase, Ref lettered (a) (b), Encl numbered (1) (2), every reference cited and every citation resolving, signature on the fourth line, no dashes, continuation page furniture, and the date as day, abbreviated month, two digit year. `build_letter.py` lays all of it out; `qc_letter.py --kind endorsement` and `measure_pdf.py` check it.

## Not in the library: what only SECNAV M-5216.5 settles
Left unverified; the product marks each as a gap where it arises, and `Overrides/endorsement.md` records the command's practice until the manual is in Reference.
- The ordinal sequence for later endorsements (SECOND, THIRD, and so on) and whether an endorser skips a level.
- Whether a short endorsement may be typed on the basic letter's last page (a same page endorsement) and how it is laid out there, as against a new page endorsement.
- How references and enclosures added by an endorsement are lettered and numbered when the basic letter already has some (continuing the sequence or restarting).
- The "Copy to:" block and who receives copies of an endorsement.
- What an endorsement may and may not change about the basic correspondence, and the wording for returning a request without action.
- Whether letterhead is required at the unit (the figures show it; the school handout's student letter carries none).
