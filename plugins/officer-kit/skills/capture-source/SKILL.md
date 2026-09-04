---
name: capture-source
description: >
  Turns an issued source into clean, complete text saved on disk before anything is built from
  it: an online interactive lesson, a handout PDF or Word file, a slide deck, or photos of a card,
  sheet, or page. Use when the user says "capture this", "pull the text out of", "transcribe
  this", "save this lesson", "get this handout into the folder", "here are photos of", or
  attaches source material a study product, letter, or brief will be built from. Every capture
  is saved in the same session and checked for completeness.
metadata:
  version: "0.2.0"
---

# Capture source

Everything downstream (study guides, quizzes, walkthroughs, letters, briefs) is only as good as the capture. Capture completely, save immediately, verify mechanically, and mark what is uncertain rather than smoothing it over.

## Rules that never bend

- **Save it the same session.** A capture that lives only in the chat is lost when the chat ends. Write it to the user's working folder before doing anything else with it.
- **Never gap fill.** If the source is thin, say so and offer to get the real document. Do not pad from general knowledge.
- **Expand everything before you copy.** Tabs, accordions, click to reveal panels, hotspots, and lazy loaded chapters hide text, and the hidden text is usually the objectives and the definitions.
- **Verbatim over tidy.** Keep the source's numbering, labels, units, and marginalia. Note where the source is wrong; do not fix it in the capture.
- **Mark uncertainty.** `[illegible]`, `[cut off]`, `[handwritten: ...]`. Never guess at a number.

## Choose the path

| Source | Path |
|---|---|
| Online interactive lesson (chaptered, panels, quizzes inside) | Section A |
| PDF, Word, or slide file | Section B |
| Photos of a card, sheet, form, or page | Section C |

## A. Online interactive lesson

1. Ask for the lesson name and the folder it belongs in. Create `<folder>/<lesson name> - Capture.md`.
2. For each chapter, in order: open the chapter, expand every panel and tab, then copy all visible text. Chapters render only once visited; an unvisited chapter is empty, not absent.
3. Paste each chapter under its own heading (`## Chapter N: <title>`). Keep list numbering and table structure.
4. Embedded knowledge checks and games are captured too, under a `### Knowledge check` heading, because they show what the course tests.
5. Run `python3 scripts/capture_check.py "<capture>.md"` and read the report: chapter count, words per chapter, empty or thin chapters, repeated blocks, and the title after content pattern (some platforms print a block's title below its body; the report flags headings that follow a list so a "missing heading" is not misread later).
6. Record source facts at the top of the file: lesson title, where it lives, date captured, chapter count, anything the lesson says about its own objectives.

If the user has a browser connector and directs its use, the same steps apply; the completeness check is the same.

## B. PDF, Word, or slides

1. Copy the file into the working folder if it is not already there.
2. Extract text (`pdftotext -layout` for PDFs; the docx or pptx skill for Office files). For scanned PDFs, OCR and say so in the source facts.
3. Tables: transcribe every table in full, in order. Do not summarise a table.
4. Figures and flow charts: describe the structure in text (boxes and arrows as steps) and note the figure number.
5. Run `capture_check.py` on the result. Save as `<title> - Capture.md` beside the original.

## C. Photos of a card, sheet, or page

Photo captures carry the most risk, so they carry a read back gate.

1. Establish scope and order: which photos, in what sequence, front and back.
2. Transcribe verbatim: labels, numbering, units, marginalia, printed and handwritten alike. Separate printed fields from handwritten annotations and ask which is authoritative.
3. Where printed numbering is inconsistent (a typo in the source), keep the source's numbering in the transcription and note the anomaly; renumber only in a derived product and only after the user confirms.
4. Mark anything illegible and ask for a better photo. Never infer a value from a neighbour.
5. **Read back gate.** Present the full transcription and ask the user to confirm before anything is built from it. Call out specifically: every number, every similar looking abbreviation, the line order, and whether each option set is complete.
6. Warn once: do not normalise toward the widely known textbook version of a standard report or card. School and unit versions differ, and a memory built version looks perfectly correct while being wrong.
7. Save as `<name> - Transcription.md` with the source facts and the confirmation date.

## Output

- The capture file, saved.
- The `capture_check.py` report, in the chat.
- A one line source facts summary: what, where, when, how many chapters or pages, what was uncertain.

## Utility script

- `scripts/capture_check.py <capture.md>`: chapter inventory, words per chapter, thin and empty chapters, consecutive duplicate blocks, headings that follow lists. Exit 1 when a chapter is empty or a duplicate block is found.
