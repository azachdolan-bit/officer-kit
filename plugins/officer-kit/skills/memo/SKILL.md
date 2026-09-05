---
name: memo
description: >
  Writes the five staff papers MCTP 3-30A prints, each in its appendix's own parts and words: the
  memorandum for the record (what happened, who was there by billet, what was decided, what action
  is underway and why), the point paper (background, discussion, recommendation), the position or
  decision paper (purpose, major points, discussion, recommendation), the talking paper, and the
  information paper. The memorandum for the record builds on the naval letter grid and is measured
  on the page. The plain memorandum with From and To lines and the business letter are governed by
  SECNAV M-5216.5, which is not in the library, so the tool is marked incomplete and says so rather
  than guessing their form. Use when the user says "memo for the record", "write an MFR", "record
  what was decided", "point paper", "decision paper", "information paper", "talking paper", "the
  colonel wants a paper on this", or "put that in writing for the file".
metadata:
  version: "0.1.0"
  status: incomplete
---

# Memo

A staff paper exists so a senior can decide or act without going back to the person who wrote it. MCTP 3-30A names five and says what each is for: the memorandum for the record "to record the impressions, information, conclusions, or decisions that arise out of formal or informal discussions, conferences, meetings, or telephone conversations"; the point paper "to present key points, facts, positions, or questions in a brief and orderly fashion"; the position or decision paper "to develop, recommend, and obtain an official position"; the talking paper "to advance a point of view or summarize an action" for use while speaking; the information paper "to provide factual information in concise terms to prepare the recipient for discussions". One purpose, one paper, its appendix's parts in its order. The tool asks which and why, takes the facts, writes the paper, and checks the parts, the length, and whether the recommendation is one the reader can sign. **Incomplete:** the plain memorandum with From and To lines and the business letter belong to SECNAV M-5216.5, which is not in the library; the tool does not build them and offers the MFR or `naval-letter` instead. See `references/standard.md`, "Not in the library".

## Read first

1. `references/standard.md`: MCTP 3-30A chapter 3 on each paper, appendices A to E with the parts and headings verbatim, MCO 5216.20B chapter 13 on the memorandum's signature placement, and what only SECNAV M-5216.5 settles.
2. `references/intake.md`: the questions, one at a time.
3. `references/voice.md`: the publication's own style rules and the captions exactly as the appendices print them.
4. `references/exemplar.md`: read only after the fact list is confirmed (step 4). It teaches shape and its content is not to be taken; the checker fails a lifted phrase.

## Your own material (read first, every time)

1. `Overrides/memo.md`: this staff's format (paragraphs or ticks, who approves, whether the commander wants the recommendation first). MCTP 3-30A itself says "Minor differences exist between commands"; the command's way wins. Say in one line what it changed.
2. `Reference/Exemplars/memo/`: papers this staff signed, sanitized. They beat the plugin's fictional exemplar.
3. `<MARINE>` or the billet throughout; participants in an MFR are billets. The name goes on with `security-check/scripts/substitute.py` on the user's computer.
4. When a paper comes back changed, `aar` captures why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question. Which paper, and what the reader decides from it, are the questions this product turns on.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

## Workflow

```
Memo:
- [ ] 1. Which paper, from the purpose (chapter 3); if the user wants a From and To memorandum, say the manual is not in the library and offer the MFR or naval-letter
- [ ] 2. Who reads it and what they do with it; for a decision paper, the decision as a yes or no
- [ ] 3. Facts, one question at a time: for an MFR who met by billet, when, what was decided, what is underway and why; for the others the background, the points with numbers, the recommendation
- [ ] 4. Read back the fact list; the user confirms; nothing else goes in. Now read exemplar.md for shape
- [ ] 5. Draft memo.md in the appendix's parts, in its order and heading words
- [ ] 6. python3 scripts/memo_check.py memo.md exits 0
- [ ] 7. For an MFR to be rendered: spec.json with "kind": "mfr", then ../naval-letter/scripts/build_letter.py and qc_letter.py --kind mfr, then measure_pdf.py; the page read as a picture
- [ ] 8. Strike pass with voice.md; the paper inside its length
- [ ] 9. Saved to Correspondence/<subject> <kind> <date>.md (and .docx for a rendered MFR)
- [ ] 10. Learning: what came back, via aar
```

## The product (memo.md)

```
# Memo
Kind: <MFR | point paper | position/decision paper | talking paper | information paper>   Code: <originator code>   Date: <day month year>
Signer: <MARINE>, <billet>, <grade> USMC          (MFR only, as Appendix D shows)

## Subj
<THE SUBJECT IN CAPITALS, IN ENOUGH DETAIL TO FACILITATE FILING AND FUTURE REFERENCE>

<then the parts that paper's appendix prints, in its order:>
MFR:                    ## Paragraphs
point paper:            ## To  ## BACKGROUND  ## DISCUSSION  ## RECOMMENDATION  ## Prepared by  ## Approved by
position/decision:      ## Purpose  ## Major Points  ## Discussion  ## Recommendation  ## Prepared by  ## Approved by
talking paper:          ## FOR USE BY  ## SUBJECT  ## BACKGROUND  ## DISCUSSION  ## RECOMMENDATION  ## APPROVAL  ## ACTION OFFICER
information paper:      ## Subject  ## Purpose  ## Key Points  ## Prepared by
```

For a rendered MFR, the same content goes into a spec for `build_letter.py` with `"kind": "mfr"`, `"letterhead"` if the command uses one, and `"signature_lines"` for the billet and grade under the name.

## Rules

- One purpose, one paper, and its appendix's parts in its order and heading words. A paper that mixes an MFR's record with a decision paper's argument is neither.
- An MFR records: who by billet, when, what was decided, what is underway and why. It does not argue or speculate; the checker fails "I think" and its relatives there.
- Every recommendation is one the reader can approve or disapprove with a signature, as the publication requires.
- References are cited in the discussion where they were used; a reference listed and unused fails.
- Lengths the publication sets: a point paper "usually does not exceed one page"; an information or decision paper one page preferred, two at most. Cut or move detail to a tab; the checker fails an overrun.
- An information paper carries no address and no signature block, and refers to no enclosures except tabs.
- The MFR's signature name sits on the fourth line below the text from page centre, with the billet and grade lines under it as Appendix D shows.
- Unclassified papers carry no classification markings. `<MARINE>` or the billet, never a name. No em or en dashes.

## Utility scripts

- `scripts/memo_check.py memo.md`: the kind is one of the five (a From and To memorandum fails with the manual named); Code and Date present; every part its appendix prints present; subject in capitals; MFR signer line with name, billet, and grade; length against the publication's limit; recommendation approvable; MFR dated, by billet, not arguing, with the action underway (warn); decision paper's other agencies line (warn); information paper with no address or signature; references cited where listed; strike words; names, lifted phrases, blocked content, dashes (fail).
- `../naval-letter/scripts/build_letter.py spec.json out.docx` with `"kind": "mfr"` renders the memorandum for the record on the grid; `qc_letter.py out.docx --kind mfr` checks the caption and that no From or To line is present; `measure_pdf.py out.pdf` measures the page.
