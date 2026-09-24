---
name: memo
description: >
  Writes the staff papers and memorandums an officer is asked for, each in its own source's parts and words: the five MCTP 3-30A prints (memorandum for the record, point paper, position or decision paper, talking paper, information paper), the memorandum formats of SECNAV M-5216.5 chapter 10 (From-To on the OPNAV form, plain-paper, letterhead, the decision block, and the memorandum of agreement or understanding), and the business letter of chapter 11, whose date, close, signature placement, and handling of references differ sharply from a naval letter's. The MFR is measured on the page; the chapter 10 and 11 formats are written and checked, not rendered. Use when the user says "memo for the record", "write an MFR", "record what was decided", "point paper", "decision paper", "information paper", "talking paper", "memorandum to the", "from to memo", "MOA", "MOU", "business letter", or "put that in writing for the file".
metadata:
  version: "0.2.0"
  status: incomplete
---

# Memo

A staff paper exists so a senior can decide or act without going back to the person who wrote it. MCTP 3-30A names five and says what each is for: the memorandum for the record "to record the impressions, information, conclusions, or decisions that arise out of formal or informal discussions, conferences, meetings, or telephone conversations"; the point paper "to present key points, facts, positions, or questions in a brief and orderly fashion"; the position or decision paper "to develop, recommend, and obtain an official position"; the talking paper "to advance a point of view or summarize an action" for use while speaking; the information paper "to provide factual information in concise terms to prepare the recipient for discussions". A memorandum is a different thing: SECNAV M-5216.5 10-1 says it "provides a less formal way to correspond within an activity/command", and chapter 10 prints several formats that are not interchangeable, each with its own condition. A business letter is a third thing again, for "agencies, businesses, or individuals outside DoD, who are unfamiliar with the standard letter" (11-1). One purpose, one product, its publication's parts in its order. The tool asks which and why, takes the facts, writes it, and checks the parts, the length, and whether the recommendation is one the reader can sign.

**What this tool does not do.** It does not render the chapter 10 memorandums or the business letter on the page: `build_letter.py` renders the memorandum for the record only, so the others are written to `memo.md` in the manual's parts, checked, and handed to a typist with the paragraph numbers. Four things chapters 10 and 11 leave unsettled are named in `references/standard.md`, "Still not settled", and are not filled in from anywhere else: the From-To form's OPNAV number, which the manual gives two ways; where a business letter's identification symbols go, which the text and every figure give differently; whether and how a "Copy to" block goes on a memorandum, which chapter 10 never mentions; and classification markings on any of these, which chapters 10 and 11 do not address.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Read first

1. `references/standard.md`: MCTP 3-30A chapter 3 on each paper and appendices A to E with the parts and headings verbatim; SECNAV M-5216.5 chapter 10 paragraph by paragraph with figures 10-1 to 10-7, chapter 11 in the manual's own order with figures 11-1 to 11-6, and chapter 2 paragraph 16 on the three date formats; MCO 5216.20B chapter 13 on the memorandum's signature placement; the comparison of the two sources on the memorandum for the record; and what is still not settled.
2. `references/intake.md`: the questions, one at a time.
3. `references/voice.md`: the publication's own style rules and the captions exactly as the appendices print them.
4. `references/exemplar.md`: read only after the fact list is confirmed (step 5). It teaches shape and its content is not to be taken; the checker fails a lifted phrase.

## Your own material (read first, every time)

1. `Overrides/memo.md`: this staff's format (paragraphs or ticks, who approves, whether the commander wants the recommendation first, which OPNAV memorandum form the activity stocks). MCTP 3-30A itself says "Minor differences exist between commands"; the command's way wins. Say in one line what it changed.
2. `Reference/Exemplars/memo/`: papers and memorandums this staff signed, sanitized. They beat the plugin's fictional exemplar.
3. `<MARINE>` or the billet throughout; participants in an MFR are billets. The name goes on with `security-check/scripts/substitute.py` on the user's computer.
4. When a paper comes back changed, `aar` captures why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question. Which product, and what the reader decides from it, are the questions this turns on.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

## Workflow

```
Memo:
- [ ] 1. Which product, from the purpose: one of the five staff papers (MCTP 3-30A chapter 3), a memorandum inside the activity (SECNAV M-5216.5 chapter 10), an agreement between commands (10-2.6), or a letter to someone outside DoD (chapter 11)
- [ ] 2. If a memorandum, which format, by the condition in its own paragraph: printed OPNAV form between individuals and offices of the same activity (10-2.2); plain paper for multiple addressees, via addressees, or both (10-2.3); letterhead for more formality, or outside the activity only where direct liaison is authorized and the matter "neither make[s] a commitment nor take[s] an official stand" (10-2.4); MFR to record what is not recorded elsewhere (10-2.1)
- [ ] 3. Who reads it and what they do with it; for a decision paper, the decision as a yes or no; for a memorandum asking approval of a single addressee, the decision block of 10-2.5
- [ ] 4. Facts, one question at a time, from intake.md section 2, including who signs and in what order for an MOA or MOU and what earlier letter a business letter must mention in its body
- [ ] 5. Read back the fact list; the user confirms; nothing else goes in. Now read exemplar.md for shape
- [ ] 6. Draft memo.md in that publication's parts, in its order and heading words
- [ ] 7. python3 scripts/memo_check.py memo.md exits 0
- [ ] 8. For an MFR to be rendered: spec.json with "kind": "mfr", then ../naval-letter/scripts/build_letter.py and qc_letter.py --kind mfr, then measure_pdf.py; the page read as a picture
- [ ] 9. For a chapter 10 or 11 format: no renderer exists, so hand over memo.md with the page mechanics named from standard.md (where the date sits, where the caption sits, where the signature starts) and say plainly that it was not measured on a page
- [ ] 10. Strike pass with voice.md; the product inside its length
- [ ] 11. Saved to Correspondence/<subject> <kind> <date>.md (and .docx for a rendered MFR)
- [ ] 12. Learning: what came back, via aar
```

## The product (memo.md)

```
# Memo
Kind: <one of the kinds below>   Code: <originator code>   Date: <day month year>
Signer: <MARINE>, <billet>, <grade> USMC          (MFR only, as Appendix D shows)

## Subj
<THE SUBJECT IN CAPITALS, IN ENOUGH DETAIL TO FACILITATE FILING AND FUTURE REFERENCE>

<then the parts that product's publication prints, in its order:>

MCTP 3-30A, the five staff papers
MFR:                    ## Paragraphs
point paper:            ## To  ## BACKGROUND  ## DISCUSSION  ## RECOMMENDATION  ## Prepared by  ## Approved by
position/decision:      ## Purpose  ## Major Points  ## Discussion  ## Recommendation  ## Prepared by  ## Approved by
talking paper:          ## FOR USE BY  ## SUBJECT  ## BACKGROUND  ## DISCUSSION  ## RECOMMENDATION  ## APPROVAL  ## ACTION OFFICER
information paper:      ## Subject  ## Purpose  ## Key Points  ## Prepared by

SECNAV M-5216.5 chapter 10, the memorandums
from-to memorandum:     Form: <OPNAV number>   ## From  ## To  ## Subj  ## Paragraphs  ## Signature
plain-paper memorandum: ## From  ## To  [## Via]  ## Subj  ## Paragraphs  ## Signature
letterhead memorandum:  ## From  ## To  ## Subj  ## Paragraphs        (header: Outside: yes/no, Direct liaison authorized: yes/no)
any of the three:       ## Decision      (only when a single addressee is asked to approve or disapprove, 10-2.5)
memorandum of agreement or of understanding:
                        ## Between  ## Subj  ## Purpose  ## Problem  ## Scope  ## Agreement  ## Effective Date  ## Signatures  ## Copies

SECNAV M-5216.5 chapter 11, the business letter
business letter:        SSIC: <ssic>  Code: <code>  Date: <Month D, YYYY>
                        ## Inside Address  [## Attention]  ## Salutation and/or ## Subject  ## Body  ## Close  ## Signature  [## Enclosures]  [## Separate Mailing]  [## Copy to]
```

For a rendered MFR, the same content goes into a spec for `build_letter.py` with `"kind": "mfr"`, `"letterhead"` if the command uses one, and `"signature_lines"` for the billet and grade under the name. Nothing else here has a renderer.

## Rules

- One purpose, one product, and its publication's parts in its order and heading words. A paper that mixes an MFR's record with a decision paper's argument is neither, and a memorandum is not a naval letter with the letterhead removed.
- An MFR records: who by billet, when, what was decided, what is underway and why. It does not argue or speculate; the checker fails "I think" and its relatives there. Both publications say the same thing about it and they do not conflict; see standard.md.
- Every recommendation is one the reader can approve or disapprove with a signature, as the publication requires.
- References are cited in the discussion where they were used; a reference listed and unused fails. **A business letter is the exception and the trap:** 11-2.7, "Refer to previous communications and enclosures in the body of the letter only, without calling them references or enclosures." No Ref line, no Encl line, and no "reference (a)" in the text.
- Lengths the publication sets: a point paper "usually does not exceed one page"; an information or decision paper one page preferred, two at most. Cut or move detail to a tab; the checker fails an overrun. Chapters 10 and 11 set no page limit.
- An information paper carries no address and no signature block, and refers to no enclosures except tabs.
- The signature is the part most often carried over from the wrong format, so it is read off the paragraph every time. MFR: the name on the fourth line below the text from page centre, with the billet and grade lines under it as Appendix D shows. From-To: the name alone, because "The writer signs his or her name without the organizational titles" (figure 10-2, paragraph 6). Letterhead: not required at all, because the From line identifies the signer (10-2.4). MOA or MOU: the senior official at the right, a third cosigner in the middle, overscoring above each line, and the senior activity signs after the junior (10-2.6.d). Business letter: "Sincerely," and then, on the fourth line below it at the centre of the page, the name in capitals and the grade spelled out (11-2.8 and 11-2.9).
- The date is read off the format, not off habit: the abbreviated format on a memorandum (17 Feb 15), the civilian format on a business letter (May 23, 2014, per 11-2.1.c), the standard format inside the text of either. Chapter 2 paragraph 16 sets all three.
- A letterhead memorandum leaves the activity only where direct liaison is authorized and the matter is routine and "neither make[s] a commitment nor take[s] an official stand". Anything that commits the command goes in a naval letter instead.
- Unclassified papers carry no classification markings. `<MARINE>` or the billet, never a name. No em or en dashes.

## Utility scripts

- `scripts/memo_check.py memo.md`: the kind is one the publications name, and a bare "memorandum" fails with chapter 10's list so the writer picks one; the identification symbols each kind actually requires; every part its publication prints; subject in capitals; MFR signer line with name, billet, and grade; length against the publication's limit; recommendation approvable; MFR dated, by billet, not arguing, with the action underway (warn); decision paper's other agencies line (warn); information paper with no address or signature; references cited where listed; From-To signed without organizational titles and its form number recorded (warn); plain paper used for the multiple or via addressees it is for (warn); letterhead outside the activity only with direct liaison authorized, and a commitment flagged (warn); a decision block carrying Approved, Disapproved, and Other and going to one addressee; an MOA or MOU with two or more parties, the manual's titled paragraphs (warn), the senior on the right, the senior signing last, overscoring and copies (warn); a business letter in the civilian date format, with no Ref or Encl block and no "reference (a)" in the body, a salutation ending in a colon or a subject line replacing it, "Sincerely," and nothing else as the close, an inside address ending in city, state, and ZIP with one space, unnumbered main paragraphs, and a signature name in capitals with the grade spelled out; strike words; names, lifted phrases, blocked content, dashes (fail).
- `../naval-letter/scripts/build_letter.py spec.json out.docx` with `"kind": "mfr"` renders the memorandum for the record on the grid; `qc_letter.py out.docx --kind mfr` checks the caption and that no From or To line is present; `measure_pdf.py out.pdf` measures the page. There is no renderer for the chapter 10 memorandums or the business letter.
