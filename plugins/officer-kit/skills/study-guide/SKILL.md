---
name: study-guide
description: >
  Builds study products from a captured lesson, handout, or publication: a study guide (skeleton,
  complete knowledge sections, practice scenarios and a quiz with answer keys on their own pages),
  an interactive walkthrough that replaces reading the lesson, a condensed handout, a whiteboard
  session plan, or a one question at a time quiz in chat, with gates that prove the product carries
  the whole source and that every quiz answer is in the body. Use when the user says "make a study
  guide", "study guide for", "walkthrough", "quiz me", "flashcards", "condense this handout",
  "whiteboard session", or attaches lesson material to study.
metadata:
  version: "0.2.0"
---

# Study guide

The product is a way to learn the lesson and then test yourself on it, built only from the user's own source. The two ways a study product fails are the ones this tool is built against: it summarizes the lesson and then tests on material the summary left out, or it fills a gap from general knowledge. Practice testing and spaced practice are the study methods with the strongest evidence; highlighting, summarizing, and rereading are among the weakest (Dunlosky and others, 2013). So every format is built around recall, and a condensed version is a separate product the user asks for by name.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Your own material (read first, every time)

1. `Overrides/study-guide.md` in the working folder, if it exists: the user's way wins. Say in one line what it changed.
2. `Reference/Exemplars/study-guide/`, if it has files: the user's approved products beat the example here.
3. The source. Nothing is built before the source is captured to a file in the working folder (`capture-source`). A capture proves presence, never absence; if the lesson has figures, check the rendered lesson before saying something is not in it.

## Before you draft

1. **Assume it already failed** and write three reasons first: the usual ones are a section that summarizes instead of teaching, a quiz answer the body never gives, and a fact from general knowledge.
2. **Ask only what changes the product:** which format, if the request fits two; which parts get scenarios, if it is not obvious; the priority order, for a whiteboard session.
3. **Say what you assumed** and mark it. Never write that the guide covers everything; the gate report says what was measured.

## Workflow

```
Study product:
- [ ] 1. Source captured to a file; figure inventory noted
- [ ] 2. Format chosen (references/formats.md)
- [ ] 3. Spec written from the source (references/spec.md): skeleton, sections in source order, verbatim where testable, quiz per references/quiz-rules.md
- [ ] 4. python3 scripts/gates.py <spec> <source files> --report <spec name> gates.md exits 0; read every missing sentence and every flag, fix the spec, rerun
- [ ] 5. Build: scripts/build_guide.py (guide, handout, whiteboard) or scripts/build_walkthrough.py (walkthrough)
- [ ] 6. source-fidelity-reviewer agent, blind, with the product and the source
- [ ] 7. Walkthrough: open it, answer one question per section, confirm the map recall modes work
- [ ] 8. Save the product, the spec, and the gate report together in Training/<topic>/; name the gate report in the reply
```

## Rules

- The source is the only authority: the user's notes, the captured lesson, and references actually read. When two sources conflict, the school or unit document outranks the general publication, the newer outranks the older, and the conflict goes in the product as a SOURCE CONFLICT callout.
- Complete means complete. A section body carries its chapter's teaching text, verbatim where the source is verbatim; the walkthrough also carries the full chapter behind "Read it as issued". Gate 1 must pass.
- Inventing a scenario is expected; inventing a fact inside it is not. Verify every number in a scenario in code.
- Organizing labels you add (table headers, category names, mnemonic labels) are fine; what a cell or a skeleton line claims comes from the source. Never fill an empty cell by inference; write "not stated". A table sits directly under the sentence that introduces it, with a `Table:` caption.
- Open every guide and walkthrough with the skeleton: the whole lesson as a memorization outline.
- A product built from course or unit material stays with the people who built it (kit standard 6). To help a peer, share this tool, not the product.
- Quiz me mode never pastes the set and never repeats a question.

## Scripts

- `scripts/gates.py`: coverage, traceability, and quiz rules on the spec; writes the gate report.
- `scripts/build_walkthrough.py`, `scripts/build_guide.py`: balance the answers, check, and build.
- `scripts/study_lib.py`: shared code. `scripts/engine_head.html`, `engine_tail.html`: the walkthrough engine, content free.

Dependencies: python-docx for the guide.
