# Roadmap

The plugin is organized around six things an officer does every week. Each skill below is a build spec: what it does, what existing rules and scripts it absorbs, and how it is verified. Skills marked BUILT exist under `plugins/officer-kit/skills/`. Everything else is planned.

Standing rules for every skill: produce from sources only, never from general knowledge; verify before delivering; save every product to the working folder in the same session; no course content, personal data, or identity in the plugin itself (those live in the user's own rules file).

## 1. Produce from sources

| Skill | Status | Does | Absorbs | Scripts to port | Gate |
|---|---|---|---|---|---|
| `capture-source` | planned | Turn an issued source into clean text on disk: an online lesson, a handout PDF, photos of a card or sheet. Photo protocol: transcribe verbatim, mark illegible, separate printed from handwritten, read back and confirm before building. Save the same session. | capture workflow, save all captures rule, photo safeguards from the builder files | `capture_check.py` (structured text vs full text length compare) | completeness compare |
| `study-guide` | BUILT (v0.1, lite) | Lesson to guide, quiz, flashcards. v0.2 adds the house docx generator, the skeleton outline first, the condensed handout variant, and the depth rule (knowledge and scenarios, not rubric mechanics). | study guide workflow, depth rule, skeleton outlines, condensing rules, no gap filling | `generate_study_guide.js`, `validate_content.py` | source-fidelity-reviewer |
| `print-card` | planned | 3x5, 4x6, 5x8, and 8.5x11 duplex laminates from a spec: reference cards, ID cards, skeletons, copy cards. Sourced versus inferred marked on the card. | card projects, duplex and flip rules, sourced vs inferred rule | `render_card.py` (HTML to PDF at page size) | visual-reviewer |
| `topic-brief` | planned | A brief that stays on the named topic: one paragraph of context, every fact tied back, numbers hygiene, source list, a cue card. Program formats (a timed class, a doctrine element) as references. | topic scoped briefs rule, presentation program format | `render_card.py` (shared) | evidence-reviewer |

## 2. Verify before signing

| Skill | Status | Does | Absorbs | Scripts to port | Gate |
|---|---|---|---|---|---|
| `qc-gates` | planned | The gate stack on demand: "QC this before I sign." Picks the gates by product type (findings: 0, 1, 2, 3; teaching product: fidelity; visual: 3) and runs the reviewer agents blind, in order, until each returns clean. Explains what each gate cut. | the four gate definitions from the correspondence standard | `measure_pdf.py` (line pitch gaps from pdftotext bbox) | itself |

Agents (BUILT): `significance-reviewer` (Gate 0), `evidence-reviewer` (Gate 1), `visual-reviewer` (Gate 3), `source-fidelity-reviewer` (teaching products), `researcher` (wide read only research). Each keeps its own memory of what it has caught before.

## 3. Correspond to the standard

| Skill | Status | Does | Absorbs | Scripts to port | Gate |
|---|---|---|---|---|---|
| `naval-letter` | planned | A naval letter to the student handout standard over the SECNAV manual: no letterhead, 13.8 pt line pitch, signature on the fourth line, reference integrity both directions, remedy ladders, standing in the first sentence, no dashes. Heading block and POC line come from the user's rules file, never from the plugin. | correspondence standard, substance rules, reference and citation integrity | `qc_letter.py` (Gate 2, mechanical), `measure_pdf.py` | qc_letter.py then rendered PDF read |
| `discrepancy-report` | planned | The assess and report pipeline, end to end: audit a week's material, Gate 0, Gate 1, build the letter and the cumulative tracker, build the examples deck, Gate 2, Gate 3, deliver docx plus PDF plus enclosure plus deck. First instance: the weekly academic discrepancy report at TBS. | the report SOP, plain numbering, the specificity standard, findings only, held findings protocol | `build_memo.py`, `build_tracker.py`, `fields_equal.py` (abort when letter and tracker text drift) | all four gates |
| `evidence-deck` | planned | Comparison decks that show every finding against the artifact that proves it: two verbatim cards and a band, black grey white, crops cut by measured coordinates, text budgeted before the picture is sized, describe never direct. Also the order contradictions deck. | deck build note, deck lessons from the STEX contradictions deck, 474 character rule | `build.js`, `crop2.py`, `make_shots.py`, `render_slides.sh` | visual-reviewer until SHIP |

## 4. Plan and assess

| Skill | Status | Does | Absorbs | Scripts to port | Gate |
|---|---|---|---|---|---|
| `order-critique` | BUILT (v0.1, generic) | Five paragraph order completeness and clarity review. Stays as the fast generic check. | | | |
| `order-analysis` | planned | The deep version: hasty METT-TC worksheet from an order; internal contradiction audit (paragraph X says A, paragraph Y says not A); grid and map checks with a stated error budget; decode parts based columns before judging sequencing; check claims against the issued references before asserting a shortfall; the "looks like a defect but is not" list. | STEX QC lessons, PEX order review, day attack review | `map_georef.py`, `grid_check.py` | evidence-reviewer |
| `tactical-planning` | planned | Playbook driven planning from receipt of order to complete plan; task statement builder from the doctrinal task list; fire support planning fields; the planning checklist card; a TDG session mode that loads a reference set and runs closed book. | planning toolkit, defense planning framework, TDG session | none yet | none (advisory) |
| `call-for-fire` | planned | The school's call for fire standard applied: drills, scenario generation with geometry built backwards so it closes, mil relation and bracketing checks, conflicts between the two issued sources resolved in favour of the newer one. | CFF standard, CFF drills | `cff_check.py` (worked examples must reproduce) | mechanical reproduce check |
| `lo-audit` | planned | Two way audit: the objective list against the taught content and back. Findings JSON with document, item number, expected code, asserted programmatically. Feeds `discrepancy-report`. | phase audits, audit engine | `audit_engine.py`, claim table assert | significance then evidence |

## 5. Teach

| Skill | Status | Does | Absorbs | Scripts to port | Gate |
|---|---|---|---|---|---|
| `walkthrough` | planned | Interactive HTML class walkthrough from a capture: fixed engine, sectioned teaching bodies carrying the complete material, check yourself quizzes, comprehensive final, subject themed verdicts. Two completeness gates before delivery. | walkthrough template spec, walkthrough completeness rule | engine template as asset, `coverage_check.py`, `quiz_trace.py`, `balance_answers.py`, Playwright pass | both completeness gates, source-fidelity-reviewer |
| `quiz-builder` | planned | Decks from the official import template, never from scratch; balanced de patterned shuffle; bell curve difficulty; tight plausible distractors; verbatim correct answer check after every shuffle; cross deck dedupe; challenge decks (reverse lookup, discrimination, sequence and scenario); host answer and page key; in chat practice exam with a no repeat tracker. | the seven quiz rules, host key, challenge decks, practice exam rounds, no duplicate questions in chat | `fill_template.py`, `shuffle.py`, `verify_kahoot.py`, `dedupe_decks.py` | `verify_kahoot.py` (mechanical) |
| `drill-builder` | planned | Procedural drills (report formats, call for fire, radio programming) from a handout or card photos, and the shareable zero content BUILDER files that let a peer generate their own from their own issued source. Embedded self test for generated apps. | the four builder files merged, shareable study tools rule, radio simulator | `scenario_geometry.py`, `zero_content_check.py` | source-fidelity-reviewer mode 2 |

## 6. Share and learn

| Skill | Status | Does | Absorbs | Scripts to port | Gate |
|---|---|---|---|---|---|
| `field-kit-start` | BUILT | Orientation and the seven day plan. v0.2 updates the skill table to the six functions. | | | |
| `security-check` | BUILT | Green, yellow, red; folder scan before linking. | | | |
| `rules-file` | BUILT (v0.1) | Interview to a personal rules file. v0.2 adds the correspondence identity block (rank, name, billet, unit, course, originator code, signature form, POC line) so `naval-letter` can copy it, and path scoped rules for the working folder. | | | |
| `build-a-skill` | BUILT | Interview to a working skill. v0.2 adds the eval requirement (three golden cases) and the skill spec rules. | skill authoring rules | | |
| `fleet-transition` | BUILT | Day one and week one at the first unit. | | | |
| `folder-triage`, `inbox-triage`, `week-ahead` | BUILT | Admin. Unchanged. | | | |
| `share-method` | planned | Turn any product into a shareable method file: zero course content, exhaustive by category extraction, the recipient's source as the only authority, self verification required. Verified by the fidelity reviewer in mode 2. | shareable study tools rule, the privacy rule for shared docs | `zero_content_check.py` | source-fidelity-reviewer mode 2 |
| `peer-eval` | planned | Raw notes to rubric anchored scores in a tracker. | peer eval workflow | `score_sheet.py` | none |
| `aar` | planned | After action: mine the session for corrections, confirmations, gate failures, and build defects; write candidate lessons to `LEARNINGS.md` with target skill, confidence, evidence. Never edits a skill. | | `aar_capture.py` | none |
| `inspect` | planned | Weekly: present the LEARNINGS queue as diffs against the specific SKILL.md lines; approve, reject, reword; run the skill's evals; bump version; commit with the why. Refuses any lesson that would soften a gate, reduce sourcing, or suppress a reviewer. Monthly: usage review, merge or retire, keep the rules file short. | | `inspect_queue.py` | the skill's own evals |

## Hooks (planned, untested)

| Event | Matcher | Does |
|---|---|---|
| PreToolUse | write or commit of a `.docx` into a correspondence folder | block unless a fresh `qc_letter.py` pass stamp exists for that file |
| PostToolUse | write of a quiz `.xlsx` | run `verify_kahoot.py`, surface the fail count |
| SessionStart | all | print the LEARNINGS queue count and a ten line standing digest |
| Stop | all | run `aar` in capture mode against the transcript |

Test in Sprint 0 whether hook commands can reach the user's working folder from a cloud session; write every script to accept a container path as well as a mounted one.

## Sprints

| Sprint | Ship |
|---|---|
| 0 | Repo, marketplace, agents (done), `rules-file` v0.2 with the identity block, `capture-source`, `naval-letter`, `qc-gates`, the five unknowns tested |
| 1 | `quiz-builder`, `study-guide` v0.2, `walkthrough`, evals for all three |
| 2 | `order-analysis`, `evidence-deck`, `discrepancy-report`, `lo-audit`, `tactical-planning`, `call-for-fire`, `print-card`, `drill-builder`, `topic-brief` |
| 3 | `aar`, `inspect`, hooks, evals for every skill, memory migration, rules file slimmed |
| 4 | Workshop cut: README and `field-kit-start` rewritten around the six functions, zero content and zero identity verified by script, `.plugin` build |
