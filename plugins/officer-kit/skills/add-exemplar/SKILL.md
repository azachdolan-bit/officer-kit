---
name: add-exemplar
description: >
  Turns a real product the user's command approved (an award, a fitrep section, a letter, a
  package, a counseling, a risk assessment, an investigation) into a pattern file in the user's
  own Reference/Exemplars folder: identifiers stripped, shape and numbers kept, an annotation of
  what made it work, so every tool reads the command's own way before the plugin's fictional
  examples. Use when the user says "add this as an exemplar", "this one got approved", "use this
  as the model", "learn from this package", or drops an approved product into the folder.
metadata:
  version: "0.1.0"
---

# Add exemplar

The plugin ships fictional exemplars so every tool works on day one. A product the user's own command approved is worth more than any of them, because it carries that command's rubric, voice, and format. This tool takes such a product, strips what must not be stored, keeps what teaches, and files it where the matching tool will read it first.

The source stays where the user keeps it. What this tool writes is a pattern: the structure, the numbers with their context, the sentences that carried the argument, and an annotation. Names, identifiers, and anything from the blocked list never enter the pattern file.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Workflow

```
Add exemplar:
- [ ] 1. Which tool does this feed? (award, fitrep, letter-of-recommendation, meritorious-promotion, nomination, counseling, risk-assessment, investigation, ...) One product, one tool
- [ ] 2. Outcome: approved as submitted, approved after edits (what edits), downgraded, returned, or unknown. The outcome is what makes it an exemplar
- [ ] 3. Read the product. Build the pattern: the shape (sections, paragraph order, length), every number with what it measured, the sentences that carried the argument, the standard sentences used
- [ ] 4. python3 scripts/scrub_check.py pattern.md exits 0 (no names, identifiers, or blocked content remain)
- [ ] 5. Annotate: what made it work in the reader's terms; what the user would change; the reader profile lines it implies (for Overrides/<tool>.md)
- [ ] 6. Saved to Reference/Exemplars/<tool>/<YYYY-MM-DD> <label>.md; offer the override lines to Overrides/<tool>.md
```

## The pattern file

```
# Exemplar: <tool>, <label>, <outcome>
Source: <where the user keeps the original; never copied here>
Approved by: <billet, not name>   Command type: <battalion, squadron, MEF staff>   Year: <YYYY>

## Shape
<sections in order, with lengths; bullets or paragraphs; anything the format required>

## Numbers and what they measured
- <number>: <what it measured, over what period, compared to what>

## Sentences that carried it
- "<sentence with the name replaced by <MARINE>>"  <why it worked>

## Standard sentences used
<openings, closings, required phrases exactly as they appeared>

## What the reader did
<approved as is; struck X; asked for Y; downgraded because Z (if known)>

## Override lines this implies
- <one line per habit worth recording in Overrides/<tool>.md>
```

## Rules

- Strip, do not summarize. The value is the exact sentence shape and the exact numbers; only the identifiers change.
- `<MARINE>` replaces the subject's name everywhere, including possessives. Other people become their billet ("the company commander"). No EDIPI, SSN, phone numbers, or email addresses.
- Blocked content (medical, family, financial, disciplinary, investigation details about a person) is dropped even if the original carried it; note "a paragraph on <topic> was dropped" in the annotation so the shape is still honest.
- A product that was returned or downgraded is as valuable as one approved; file it with the outcome and what the reader said.
- Never file a product the user did not write or receive in their own duties. If the provenance is unclear, ask, and file nothing until it is clear.

## Utility script

- `scripts/scrub_check.py pattern.md`: fails on any residual name pattern next to a grade (a grade followed by a capitalized word that is not a known placeholder), identifiers, email addresses, phone numbers, or blocked content. Exit 1 on any hit.
