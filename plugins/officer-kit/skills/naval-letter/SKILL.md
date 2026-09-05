---
name: naval-letter
description: >
  Drafts, builds, and quality checks a naval letter to the school handout standard (B020069XQ
  over SECNAV M-5216.5): no letterhead, 13.8 pt line grid, signature on the fourth line,
  reference integrity both ways, remedy ladders, no dashes. Use when the user says "naval
  letter", "draft a letter to", "write this up as correspondence", "request for review",
  "memo to the company", "letter format", or asks for anything that goes up a chain of
  command in writing. Identity comes from the user's rules file; anything withheld becomes a
  placeholder the QC gate refuses to pass.
metadata:
  version: "0.2.0"
---

# Naval letter

Produce a letter that is right on substance and right on form, then prove it with the gates. A letter that is right on substance and wrong on form reads as an author who did not check his work, and the substance goes down with it.

Read `references/standard.md` before the first draft of a session. It is the whole standard: format, identity, substance, reference integrity, gates, delivery, and the measured targets.

## Inputs

- **What the letter must do**, in the user's words: the ask, the audience, the remedy wanted.
- **The sources**: the actual files the letter will cite. List the folder; never build a reference list from memory.
- **The identity block** from the user's rules file (correspondence section): SSIC, originator code, From line, usual To line, signature form, POC line. If the rules file has no such section, or a field is missing, ask once for the missing values. Never invent a name, code, phone, or email. A user may decline to record any of these; the letter then carries a placeholder until they supply the value at draft time.

## Your own material (read first, every time)

1. `Overrides/naval-letter.md` in the working folder, if it exists: the command's way wins over the defaults below. Say in one line what it changed.
2. `Reference/Exemplars/naval-letter/` in the working folder, if it has files: the user's own command's approved patterns beat the plugin's fictional exemplars.
3. The label. Another Marine's name never enters the session. Work on `<MARINE>` (grade and billet stay); the user runs `security-check/scripts/substitute.py` on the finished file on their own computer. If the rules file records a working label, use that instead.
4. When something comes back with edits, or a board answers differently than expected, tell the user `aar` will capture it.

## Workflow

Copy this checklist and track it:

```
Letter progress:
- [ ] 1. Sources listed from the folder; each reference is one real document by its actual title
- [ ] 2. Identity block read from the rules file (missing fields asked for, not guessed)
- [ ] 3. Spec written to spec.json (structure below)
- [ ] 4. Built: python3 scripts/build_letter.py spec.json "<name>.docx"
- [ ] 5. Gate 2a: python3 scripts/qc_letter.py "<name>.docx" --encl-title "<exact title>" ... exits 0
- [ ] 6. Rendered to PDF; Gate 2b: python3 scripts/measure_pdf.py "<name>.pdf" exits 0
- [ ] 7. Gates 0 and 1 run (findings based letters only), cuts applied, rebuilt, Gate 2 rerun
- [ ] 8. Rendered PDF read as pages: page count, no orphaned lines, signature where it belongs
- [ ] 9. Delivered: docx plus pdf, enclosures as their own files, cover email drafted
```

**Step 1, sources.** `ls` the source folder. One document per reference letter, named as it exists on disk (a plain descriptor in parentheses is fine: "(interactive lesson)"). Enclosure titles verbatim. Every reference will be cited in the body and every citation will resolve; plan the body around the references, not the other way round.

**Step 2, identity.** Read the user's rules file. Copy the correspondence fields into the spec exactly. If a field is absent, ask: "Your rules file does not carry a From line. Give me the line as it should print, or say skip and I will leave a placeholder for you to fill." Do not proceed past Gate 2 with a placeholder.

**Step 3, spec.** Write `spec.json`:

```json
{
  "ssic": "1500", "originator_code": "...", "date": "2026-09-04",
  "from": "...", "to": "...", "via": [],
  "subj": "ALL CAPS PHRASE",
  "refs": ["one document per entry"], "encls": ["exact title"],
  "paragraphs": [
    {"text": "Purpose.  On behalf of ..., I request ..."},
    {"text": "...", "subs": [{"text": "...", "subs": [{"text": "..."}]}]}
  ],
  "poc": "My point of contact information is ... .",
  "signature": "F. M. LAST"
}
```

Substance rules while writing the paragraphs: standing in the first sentence; one claim per paragraph; ask, prove the negative, prove the positive, remedies, POC; remedy ladder with parallel "or"; no hedging clauses; no dashes; findings only documents carry no severity and no fixes; every claim names both ends and its consequence in the same breath; plain numbering.

**Steps 4 to 6, build and mechanical QC.** The build script pins the 13.8 pt pitch and lays out every gap. `qc_letter.py` must exit 0 (warnings are allowed but read them). Convert to PDF (`soffice --headless --convert-to pdf`) and run `measure_pdf.py`; it must exit 0. If it fails, fix the spec and rebuild; never hand edit spacing.

**Step 7, judgment gates.** For a letter that reports findings or makes claims against sources, run the blind reviewers before you trust the body: `significance-reviewer` (Gate 0) then `evidence-reviewer` (Gate 1), each given only the draft findings and the source files. Cut everything that does not survive. Rebuild and rerun Gate 2. The `qc-gates` skill runs this sequence if you would rather delegate it.

**Step 8, read the pages.** Render to images and look: page count, nothing orphaned onto a final page, signature block on the fourth line at page centre, continuation Subj on the sixth line. If a letter runs a few lines over, cut body text.

**Step 9, deliver.** `.docx` plus `.pdf` into the user's correspondence folder, enclosures as their own files marked "Enclosure (n)" lower right. Draft the cover email: two or three sentences, subject names the object and the action.

## Rules

- Never compress signature spacing, heading spacing, or margins to fit a page.
- Never reconstruct the identity block from memory or from an earlier letter in the conversation; read the rules file.
- Never ship a placeholder. Never guess a value to remove one.
- Any change to the reference list triggers a renumber sweep of every citation.
- Do not swap a dash for a colon; rewrite the sentence.
- Personal data stays in the user's folder. Nothing in this skill's files carries a real name, number, or address.

## Utility scripts

- `scripts/build_letter.py spec.json out.docx` renders the letter on the grid; reports placeholders left.
- `scripts/qc_letter.py out.docx [--encl-title "..."]...` is Gate 2a; exit 0 is clean.
- `scripts/measure_pdf.py out.pdf` is Gate 2b; every gap measured against the standard.

Dependencies: `pip install python-docx`; `pdftotext` (poppler) and LibreOffice (`soffice`) for rendering and measuring.
