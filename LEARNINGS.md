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

## 2026-09-22  significance-reviewer  high
Evidence: A weekly discrepancy report claimed that eight of sixteen enabling objectives in a Moodle lesson had no instruction behind them. Verification cut it to four. All eight really were unsupported inside that lesson, but only four were tagged "taught asynchronously" in the course's consolidated objective list, which is what made that lesson the vehicle that owed them; the other four carried no tag and may belong to a resident period the course site cannot show. The drafting step counted instead of classifying, and the gate answered once for a claim that was eight claims.
Lesson: Ask obligation before absence. For any finding that says instruction or content is missing, name the document that designates the delivery vehicle for each item and count only the items whose designated vehicle is the source that was searched; disclose the rest in the same exhibit and exclude them from the count. Expand any counted claim into one row and one verdict per item before grading, and report the count that survives.
Status: approved 0.10.1

## 2026-09-22  capture-source  high
Evidence: The same report said "Swinging Traverse does not appear" in a machine gun lesson. It appears, printed inside the classification figure in the chapter that teaches it. The claim had been checked against a text capture, which cannot see inside an image. A second claim in the same product, that an objective was "published only in the study guide," missed the consolidated objective list, which carries it on page 6.
Lesson: A capture proves presence, never absence. Stamp every capture header TEXT ONLY, record a figure inventory per chapter (image count and the text visible on each), and send any later absence claim back to the rendered source before it ships. Search the governing objective list before any "only in" claim.
Status: approved 0.10.1

## 2026-09-22  qc-gates  medium
Evidence: The week that produced the overstatement left no findings file and no gate report in the audit folder, while the two weeks before it left both. Whether the gates were skipped or run without being recorded could not be determined afterwards, which is the same thing as not running them.
Lesson: A gate that leaves no artifact did not run. Write the findings to a file before any gate, save the gate report beside it, and name that report in the delivered product.
Status: approved 0.10.1

## 2026-09-05  qc-gates  high
Evidence: Checked where a Cowork session's project root actually is. It is the cloud container (`/home/claude`), not the user's connected folder. The container's own `~/.claude/` holds the platform's hook scripts and no settings.json, and the connected folder has no `.claude` directory at all. A hook configured at `<working folder>\.claude\settings.json` is therefore never read by a Cowork session. The kit had been planning blocking hooks as the next infrastructure step, and OFFICER ANALYSIS.md recommended them in three places.
Lesson: Do not plan on blocking hooks in Cowork. A checker runs because a skill's workflow runs it and because a reviewer would catch a product that skipped it, not because a hook forces it. Blocking hooks are available only to Claude Code run locally with the working folder as its root, and any tool that depends on one must say so.
Status: approved 0.8.2

## 2026-09-05  build-a-skill  high
Evidence: The first real install attempt of the packaged plugin failed with eight errors at once: the plugin description was 683 characters against a 500 limit, the `inspect` skill description contained an XML tag, and all six agents had invalid YAML frontmatter because an `<example>` block at column 1 parses as a new YAML key. All five eval harnesses were passing at the time. An earlier session had recorded the opposite conclusion, that agent frontmatter is invalid YAML by design and should be checked with a regex; that was wrong and it hid this for two versions.
Lesson: Agent frontmatter must be valid YAML. Put the description and its `<example>` blocks in a literal block scalar (`description: |`, every line indented two spaces), keep the description under 1024 characters, and move surplus examples into the body. Never validate frontmatter with a regex to work around a parse failure; the parse failure is the finding.
Status: approved 0.8.1

## 2026-09-05  qc-gates  high
Evidence: Same install failure. The kit had five harnesses covering its content and none covering whether the package would install. Everything green, nothing installable.
Lesson: Run the installer's own checks in the repository. `evals/install_check.py` validates both manifests, every skill and agent frontmatter, description limits, XML tags in descriptions, version agreement between plugin.json and marketplace.json, and that every advertised script parses. It runs before any package is delivered.

## 2026-09-05  think  high
Evidence: The first end to end test of the deliberate tier (evals/ab-test-2026-09-05/). Two blind drafters, same tasking, one with the thinking layer and one without. A blind reviewer chose the worksheet built WITHOUT it, because the one built with it asserted 25 facts the tasking never supplied while telling the approver in writing that every gap was marked. Three of its five questions came from the worked example in estimate.md rather than from the tasking, and it never asked the question the tasking made obvious.
Lesson: A worked example in the same domain as the task supplies answers instead of teaching form. Keep every worked example in a different product from the tool it teaches, say in the example itself that its content is not to be taken, and fail an estimate that reuses its phrases.
Status: approved 0.7.1

## 2026-09-05  think  high
Evidence: Same test. The check's sixth pass, "what was not checked," was inverted into "each missing item is a gap rather than an omission, and each one is bracketed above." That sentence is a claim about the whole product that no pass in the check establishes, and it was false. The competing product made no such claim and was preferred for that reason alone.
Lesson: Never write that everything missing is marked, that every gap is bracketed, or that something is the one assumption a product cannot carry. Say what was checked and against what. A false assurance is worse than silence, because the signer stops looking.
Status: approved 0.7.1

## 2026-09-05  think  medium
Evidence: Same test. precision_check.py read every risk level (IE, IID, IIB) as an undefined acronym, adding about twenty junk warnings to a risk worksheet, which is the document type it had just been wired into. Second time in two days that a checker was shipped without being run on its own target document.
Lesson: Before wiring a checker into a tool, run it on that tool's own exemplar and read every line of the output. A check whose output nobody will read is worth less than no check, because the record then says it ran.

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

## 2026-09-05  build-a-skill  high  -> plugin
Evidence: The risk assessment matrix shipped with a caution because the web copy of MCO 5100.29C returned Figure 3-4 as an image; the full order was in the user's publications library the whole time, and rendering the page with pdftoppm and reading it settled the matrix in five minutes. The same library held MCO 1900.16, whose paragraph 6105 prescribes the Page 11 entry's exact wording and requires the CO's signature, which the first draft of `page-11` had not carried.
Lesson: Before writing any tool's standard.md, look in the user's publications library for the order and read it there, rendering figure pages as images when the text is a picture; only fall back to the web when the order is not on disk. Never ship a caution the library could have removed.
Status: pending

## 2026-09-05  think  high  -> plugin
Evidence: The precision checker, run on the kit's own CRITICAL THINKING.md, produced 116 warnings in a flat list. A checker that produces 116 undifferentiated warnings is the Ontario failure in miniature: the reader stops reading it, and the finding that mattered is buried with the ninety that did not. The same document also showed that acronym flagging is noise outside a directive product, where the reader has to act on the term.
Lesson: Group a checker's warnings by kind, show at most three of each with a count of the rest, and scope a check to the products where its finding changes what the reader must do. A check nobody reads is worth less than no check, because the record now says it ran.
Status: pending

## 2026-09-05  think  high  -> plugin
Evidence: Three of the fixes a reasonable person would build for "think harder" are measurably harmful: self review with no external signal degrades accuracy across rounds, a rigid schema wrapped around the reasoning took one model from 86 to 23 percent on grade school math, and a mandated checklist across 101 hospitals and 200,000 procedures moved mortality not at all.
Lesson: Never add a step that asks the model to review its own work with nothing external to check against. Verification is against an artifact: the source, the arithmetic, the checker, a blind agent with the standard in hand. Reason in prose, format second. Keep the structure around the thinking, not inside it.
Status: pending
