# Learnings queue

Candidate lessons for the plugin under `plugins/officer-kit/`, captured by the `aar` skill (or by hand) and waiting for review by `inspect`. Nothing here changes a skill until a person approves it and the skill's evals pass.

Format, one entry per lesson:

```
## YYYY-MM-DD  <target skill>  <confidence: high | medium | low>
Evidence: <what happened, one line: the correction, the gate failure, the defect>
Lesson: <the instruction as it should appear in the skill, imperative>
Status: pending | approved <version> | rejected <reason>
```

Confidence: high = a never or always statement from a direct correction; medium = a pattern that worked; low = an observation to watch.

A lesson that would soften a gate, reduce sourcing, or suppress a reviewer is rejected on sight.

---

## 2026-09-04  naval-letter  high
Evidence: The signed 1501c letter took nine revision passes; every rule in the correspondence standard exists because something looked finished and was wrong.
Lesson: Measure the rendered PDF with pdftotext bbox; never eyeball line pitch. Copy the heading block from the user's rules file, never reconstruct it.
Status: pending

## 2026-09-04  discrepancy-report  high
Evidence: Week 14 draft had 19 findings; Gate 1 left 10; Gate 0 then cut 9 to 7 and reversed one. Gate 2 found two defects in an already delivered memo.
Lesson: Run Gate 0 before Gate 1, and neither substitutes for the other. Boss's priority order for findings: contradictions and confusing material inside the lesson first, then objective list issues, then spelling last.
Status: pending

## 2026-09-04  walkthrough  high
Evidence: First offense walkthrough draft rejected: "you did not include enough material and are testing me on stuff that's not in this interactive module."
Lesson: Bodies carry the complete lesson, verbatim where the source is verbatim. Every section quiz answer must be present in that section's body. Run both completeness gates before delivery.
Status: pending

## 2026-09-04  study-guide  high
Evidence: CST1 guide rejected as "too in the weeds" when it led with graded step rubrics.
Lesson: Knowledge first, then a worked practice scenario with the answer key on its own page. Open with a skeleton outline of the whole lesson.
Status: pending

## 2026-09-04  quiz-builder  high
Evidence: A from scratch quiz workbook silently dropped importer features; a shuffle corrupted the marked answer because the importer stores a slot number, not text.
Lesson: Always populate the official template. After any shuffle, resolve every slot number to its text and assert it equals the intended verbatim answer; all four cells non empty; print pass or fail.
Status: pending

## 2026-09-04  topic-brief  high
Evidence: First Iwo backgrounder rejected as "almost unreadable... not focused."
Lesson: Lead with the topic, not the timeline. One orienting paragraph of context, then every section on the named topic, every number tied back in the same sentence.
Status: pending

## 2026-09-04  order-analysis  medium
Evidence: A false finding (FPFs "registered before the BPs exist") came from misreading parts based columns; a mils value was wrong by 200.
Lesson: Decode BW / EW / CE / CS before judging sequencing. Verify every direction and distance in code. Check the "not a defect" list before raising a finding.
Status: pending

## 2026-09-04  share-method  high
Evidence: The academic integrity policy forbids sharing a study guide with anyone who did not help build it; a method file with zero content is shareable.
Lesson: Share the method, never the product. Grep the shared file for subject terms and doctrinal values and expect zero real hits. Never mention browser automation in a shared document.
Status: pending
