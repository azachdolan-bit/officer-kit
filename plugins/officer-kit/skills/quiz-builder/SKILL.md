---
name: quiz-builder
description: >
  Builds Kahoot decks and other multiple choice quizzes from a captured source by filling the user's
  copy of Kahoot's official import template: sourced questions with close distractors, a balanced
  and unpatterned answer order, every file read back to prove the marked slot holds the right answer,
  and a host answer and page key for group sessions. Use when the user says "make a Kahoot",
  "Kahoot for", "quiz deck", "build a quiz from", "question bank", "host key", or wants multiple
  choice practice for a group.
metadata:
  version: "0.1.0"
---

# Quiz builder

A Kahoot fails in one of three ways: it breaks on import, it marks the wrong answer, or it can be passed without knowing the material. The first comes from files built without Kahoot's own template, the second from shuffling answers when Kahoot stores the answer as a slot number, and the third from patterns a player learns to read (the answer always in one slot, always the longest, the odd one out). This tool is built against all three, and against the fourth failure every study product shares: a fact the source does not carry.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Your own material (read first, every time)

1. `Overrides/quiz-builder.md` in the working folder, if it exists: the user's way wins. Say in one line what it changed.
2. The user's copy of Kahoot's official quiz import template. Find it in the working folder (a file named like `KahootQuizTemplate*.xlsx`). If there is none, stop and ask the user to download it from Kahoot's help article on importing from a spreadsheet; never build the layout yourself.
3. The source, captured to a file (`capture-source`). A study-guide spec for the same lesson is a good starting point; its questions carry over.

## Before you draft

1. **Assume it already failed** and write three reasons first; the usual ones are a question the source does not answer, a distractor that is also right, and a deck a player passes by pattern.
2. **Ask only what changes the product:** one deck or several (split on the source's own boundaries), and whether it will be hosted for a group (then build the host key).
3. **Say what you assumed.** If the source is thin for the number of questions asked, say so and offer fewer or a combined deck.

## Workflow

```
Quiz:
- [ ] 1. Template found; source captured
- [ ] 2. Spec written (references/spec.md) under the rules in references/rules.md
- [ ] 3. python3 scripts/build_kahoot.py <spec> --template <template> --out <folder> --source <source files> --report "<folder>/<set> gates.md" exits 0; read every warning
- [ ] 4. Hosted: python3 scripts/build_host_key.py <spec> "<folder>/<set> - Host Answer and Page Key.docx"
- [ ] 5. evidence-reviewer agent, blind, with the spec and the source: every correct answer right, every distractor wrong, no two defensible answers
- [ ] 6. Save the decks, the spec, the gate report, and the key together; name the gate report in the reply
```

## Importing into Kahoot

Create, blank canvas, Add question, Import spreadsheet, choose the file, Add questions. Delete the blank first slide the creator adds, or Kahoot will not save. Spot check the first three questions against the host key before hosting. If the tool is driving the browser, attach the file through the page's file input rather than the Select file button, which opens a picker it cannot see.

## Scripts

- `scripts/build_kahoot.py`: places answers, checks the rules, fills the template, reads every file back.
- `scripts/build_host_key.py`: the landscape host answer and page key.
- `scripts/quiz_lib.py`: the placement and the checks; shares text matching with `study-guide`.

Dependencies: openpyxl, python-docx.
