# Naval letter standard and QC gates

Contents: 1 Format · 2 Identity block · 3 Substance · 4 References and enclosures · 5 The gates · 6 Delivery · 7 Measured targets

Authority for format is the school's student handout on military correspondence (at The Basic School, B020069XQ) over SECNAV M-5216.5, under the standing rule that the school handout outranks the parent publication where they differ. Where the handout is silent, the parent manual governs.

Every rule below exists because a draft that looked finished was wrong.

## 1. Format

| Element | Rule |
|---|---|
| Letterhead | None on a student letter. Start with the SSIC block. |
| SSIC block | Left aligned on a common tab, not three right aligned lines. SECNAV M-5216.5 ch. 7: the SSIC starts "2 inches or more from the right edge of the paper" and "the longest line of the sender's symbol should end close to the right margin." Tab at 6.5 inches from the left edge of the paper (5.5 inches of indent inside a 1 inch margin). SSIC, then originator code, then date, on consecutive lines. |
| Font and margins | Times New Roman 12, 1 inch top, bottom, and sides. |
| From, To, Via | Labels at the left margin, text at a 0.5 inch tab, runover aligned under the text. Omit Via entirely when there is no routing requirement; never leave an empty one. |
| Subj | All caps. A phrase, not a sentence. Second line below the last heading line. |
| Ref | Lower case letter in parentheses: (a), (b). Second line below Subj. |
| Encl | Number in parentheses: (1), (2). Second line below Ref. |
| Paragraphs | 1. then a. then (1) then (a). Single spaced within, double spaced between. First line indented by level, runover returning to the left margin. |
| Signature block | Fourth line below the last line of text (three blank lines), starting at the centre of the page. A signature page carries at least two lines of text. |
| Continuation pages | Subj line repeats starting on the sixth line; page number centred 0.5 inch from the bottom, no punctuation. |
| Enclosure marking | On the enclosure itself, "Enclosure (1)" lower right on every page. The letter carries no such marking. |
| Date | Day, abbreviated month, two digit year: 4 Sep 26. |

**Spacing is counted in lines, and the line pitch must be pinned.** Word renders Times New Roman 12 single spaced at a 13.8 pt pitch; LibreOffice defaults to 15.85, which silently breaks every "second line below" and "fourth line below" measurement. So: line spacing exactly 13.8 pt on the Normal style, zero space before and after everywhere, and every blank line a real empty paragraph. `scripts/build_letter.py` does all of this.

**The spacing is not negotiable to fit a page.** When a letter runs a few lines onto a second page, cut body text. Never compress the signature spacing, the heading spacing, or the margins.

## 2. Identity block

The From line, originator code, signature form, and point of contact line come from the user's rules file, never from this plugin and never reconstructed from memory. Read them from the rules file's correspondence section and copy them into the spec. Any field the user has chosen not to record renders as a bracketed placeholder, and Gate 2 refuses to pass a letter with a placeholder in it; ask the user for the value at draft time, and do not guess it.

Typical shape of the block in a rules file:

```
## Correspondence identity
SSIC default: 1500
Originator code: <as printed on a signed letter>
From: <Rank Full Name, Billet, Unit, Course or Command>
To (usual): <Billet, Unit>
Signature: <F. M. LAST>
POC line: My point of contact information is <phone> or <email>.
```

Reference entries carry a title and, where it helps, a plain descriptor in parentheses: `(a) Introduction to Fire Support Planning (interactive lesson)`. Activity, resource, and folder numbers stay out of the Ref block; they belong in the body when they are part of a route to a specific chapter.

**Do not state what is implied.** A findings report that recommends nothing is already saying so by recommending nothing. Cut sentences like "Findings are stated as observed; no corrective action is recommended."

## 3. Substance

- **Establish standing in the first sentence** when writing in a billet: "On behalf of the Alpha Company student population, I request..." A letter from a representative is not a personal complaint; say whose interest it represents.
- **One claim per paragraph.** A request typically runs: paragraph 1 asks; 2 proves the negative; 3 proves the positive; 4 requests remedies; 5 is the point of contact.
- **Cut hedging clauses.** "This request concerns the sourcing of the learning objective" beats "...rather than the keying of any single question."
- **Alternatives get explicit parallel "or" and identical grammatical shape:** "that X be removed from scoring, or that partial credit be awarded, or that the objective be resourced."
- **Offer a remedy ladder, not an ultimatum:** full relief, partial relief, prospective fix.
- **No em dashes or en dashes.** Gate 2 fails on them. Rewrite the sentence; do not swap in a colon.
- **Findings only documents** carry no severity ranking and no recommended fixes unless asked.
- **Specificity.** Every claim names both ends: where the thing is, where it is not, and the consequence, in the same breath. Fold the location into the last sentences of the subparagraph; do not add a separate "where to find it" line.
- **Plain numbering.** Findings are 1 through N. No composite identifiers.

## 4. References and enclosures

Every defect in this class survived multiple read throughs. Assume you cannot catch them by eye.

1. **Build the reference list by listing the source folder, never from memory.** Name each file as it actually exists.
2. **One document per reference letter.** A reference containing "and" is a defect until proven otherwise.
3. **No two references may name the same artifact.**
4. **Every reference is cited at least once in the body; every citation resolves to a listed reference.** Both directions.
5. **Any change to the reference list triggers a full renumber sweep** of every in body citation. Do it mechanically.
6. **The enclosure title in the Encl line matches the actual document's title verbatim**, with no descriptive parenthetical.
7. **A locator must belong to the document it is attached to.** A chapter number does not describe a study guide organised by topic. When two sources teach the same material, cite each in its own scheme.
8. **Any fact that lives in two places gets a mechanical equality check, or one of the places goes.** A letter and its enclosure once shipped "44 and 45" against "45 and 46" because the same finding was typed twice.

## 5. The gates

Nothing is delivered until every applicable gate has run. They catch different things and none substitutes for another.

| Gate | Kind | Who | What it answers |
|---|---|---|---|
| 0 Significance | judgment, blind | `significance-reviewer` agent | Is a true observation actually a defect worth reporting? Baseline, consequence, alternative explanation, authority. |
| 1 Evidence | judgment, blind | `evidence-reviewer` agent | Is every claim proven verbatim against the source, located, and counted? What did the draft miss? |
| 2 Document | mechanical | `scripts/qc_letter.py` then `scripts/measure_pdf.py` | Heading elements, reference integrity both ways, enclosure title, signature spacing, dashes, control characters, sequence, placeholders; then the rendered PDF measured on the 13.8 pt grid. |
| 3 Visual | judgment, blind | `visual-reviewer` agent | Anything rendered that goes with the letter (a deck, an enclosure with layout). Repeat until SHIP. |

Gates 0 and 1 apply to findings based letters (reports, audits, review requests). Gate 2 applies to every letter. Gate 3 applies whenever a visual product ships with it.

On the first weekly report that used them, Gate 1 cut nineteen findings to ten (two were factually wrong) and Gate 0 then cut ten to seven and reversed one. Gate 2 later found two defects in a memo that had already been delivered: a signature block two lines below the text and an em dash. Both had passed a careful human read.

## 6. Delivery

- Deliverable is `.docx` plus `.pdf`. The enclosure is attached as its own file, marked "Enclosure (1)" lower right on each page.
- Cover email: two or three sentences. What it is, the one fact that matters, where the detail sits. Subject line names the object and the action.
- If the letter promises a separate submission, that thing exists before the letter goes out.

## 7. Measured targets on a correct letter (points, from `pdftotext -bbox`)

| Where | Gap |
|---|---|
| SSIC to code to date | 13.8 each |
| Date to From | 27.6 |
| From to To | 13.8 (27.6 if From runs over) |
| To (or last Via) to Subj | 27.6 |
| Subj to Ref | 27.6 (41.4 if Subj runs over) |
| Ref entries | 13.8 each |
| Last Ref to Encl | 27.6 |
| Encl to paragraph 1 | 27.6 |
| Between paragraphs | 27.6 |
| Last text line to signature | 55.2, at x = 306 (page centre) |
| Continuation page, top of page to Subj | 82.8 (the sixth line); body resumes on the second line below |

`scripts/measure_pdf.py` checks every one of these and also that every gap on every page is a whole number of pitches.
