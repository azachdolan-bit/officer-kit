---
name: qc-gates
description: >
  Runs the verification gate stack on a product before it is signed or delivered: significance
  and evidence review for findings, mechanical document QC for letters, visual review for anything
  rendered, source fidelity review for teaching products. Picks the gates by product type and runs
  the blind reviewer agents until each returns clean. Use when the user says "QC this", "run the
  gates", "check this before I sign", "red team this", "is this ready to send", "verify this
  against the sources", or hands over a finished draft and asks whether it holds up.
metadata:
  version: "0.2.0"
---

# QC gates

Verification is a separate job from drafting, done by someone who did not draft. Each reviewer agent is blind: it gets the product and the sources, never the reasoning that produced them. Accuracy is not significance, a clean document is not a true one, and a true finding can still be laid out wrong; the gates catch different things and none substitutes for another.

## Pick the gates

| Product | Gates, in order |
|---|---|
| Findings based letter or report (discrepancies, an audit, a review request, an order contradiction list) | 0 Significance then 1 Evidence then 2 Document then 3 Visual if anything rendered ships with it |
| Any other naval letter or memo | 1 Evidence if it makes claims against sources then 2 Document |
| Brief, backgrounder, presentation card | 1 Evidence (numbers hygiene) then 3 Visual for the card |
| Study guide, walkthrough, quiz, drill, condensed handout | Source fidelity (mode 1) then 3 Visual if printed |
| Shareable builder or method file | Source fidelity (mode 2, zero content) |
| Deck, laminate, anything rendered | 3 Visual, repeated until SHIP |

Full stack only on things the user signs or hands to someone senior. Study products get fidelity only. Scratch gets nothing; do not spend reviewer tokens on a draft the user has not asked to check.

## Run

Copy this checklist and track it:

```
Gate run:
- [ ] Product type named; gates chosen from the table
- [ ] Sources collected as file paths (the reviewer reads them itself)
- [ ] Gate 0 significance-reviewer: verdicts recorded, KILL and DEMOTE applied
- [ ] Gate 1 evidence-reviewer: grades recorded, THIN / REACHING / WRONG cut, "missed" list triaged
- [ ] Product rebuilt after cuts
- [ ] Gate 2 qc_letter.py exit 0, PDF rendered, measure_pdf.py exit 0 (letters)
- [ ] Source fidelity reviewer PASS (teaching products)
- [ ] Gate 3 visual-reviewer SHIP (rendered products), rerun after every fix
- [ ] Gate report written: what each gate cut and why
```

**Brief a reviewer like this.** Give the agent: the product (path or text), the source file paths, the output shape it must return (each agent's definition carries it), and nothing else. Do not include the draft's justification, the conversation, or your own opinion of which findings are strong. If a reviewer asks why something was written, the answer is "not your concern; grade it."

**Apply the verdicts mechanically.** Gate 0: KILL removes the finding; DEMOTE moves it to an appendix or drops it; SURVIVES IF REWORDED takes the reviewer's rewrite. Gate 1: anything below SUBSTANTIVE is cut, not softened. The "missed by the draft" list is triaged: verify each candidate against the source yourself before adding it, then send the additions back through Gate 0 and Gate 1.

**Rebuild, then rerun.** Any cut changes numbering, references, and counts. Rebuild from the corrected data and run Gate 2 again from the start. Never patch the rendered file.

**Gate 3 is a loop.** Render every page or slide to an image, send the set to `visual-reviewer`, fix everything on the list, render again, send again. Stop only at SHIP. One pass has never been enough on a dense deck.

## The gate report

End with a short report the user can read in a minute:

```
Gates run: 0, 1, 2, 3
Gate 0: N drafted, K survive. Killed: <finding, the one question that killed it>
Gate 1: N claims, K SUBSTANTIVE. Cut: <claim, grade, reason>. Added from the missed list: <n>
Gate 2: qc_letter clean; measure_pdf clean (signature 55.2, page 2 Subj 82.8)
Gate 3: SHIP after <n> passes; last pass fixed <defect>
```

## Rules

- Reviewers are blind. Never pass them the drafting reasoning.
- Never argue a reviewer out of a KILL or a WRONG in the same session. If the user disagrees, the user overrides, and the report says so.
- Never run a judgment gate on a product with a placeholder or a known mechanical defect; fix the mechanics first so the reviewer's tokens go to substance.
- Record what each gate caught. That record feeds `LEARNINGS.md`; a defect the drafting skill should have prevented is a lesson for that skill.

## Where the pieces live

- Agents: `significance-reviewer`, `evidence-reviewer`, `visual-reviewer`, `source-fidelity-reviewer` (plugin `agents/`).
- Mechanical scripts for letters: `skills/naval-letter/scripts/qc_letter.py` and `measure_pdf.py`.
- Rendering: `soffice --headless --convert-to pdf`, then `pdftoppm -png -r 110` for page images.
