# quiz-builder test (24 Sep 26)

**Setup.** A drafter with only the skill, the kit standards, Kahoot's template, and MCDP 7 chapter 3 (public) was asked for "about 20 questions" to host for a platoon. It built one 20 question deck, a host key, a spec, a gate report, and notes. `test-deck-mcdp7-ch3.txt` is the deck as the reviewers saw it (placement from the first build).

**Blind evidence review.** 19 of 20 SUBSTANTIVE, 1 THIN, none WRONG. The THIN one asked for "the adage" when the chapter revises a familiar saying, so the familiar version was defensible. A second stem assumed something the chapter denies. Both are now rules (8a).

**Blind red team, failure asserted: a player who never read the chapter scores well.** It held. Nine of twenty were answerable from cues alone: distractors that contradict the lesson's thesis, a stem that gives away its answer, grammar only the answer fits, one question printing the next one's answer, and an answer order that stepped through the tiles (Q4 to Q9 ran 2, 3, 4, 1, 2, 3) while passing the old checks.

**Changed because of it.**
- Placement now samples an order that passes every pattern check (no repeats, no stepping run, no A B A B swing, no repeating cycle); 200 seeds on the real deck and 200 on a synthetic one all pass. The same check now guards `study-guide`.
- Warnings for a stem word only the correct option repeats, and for an answer that already appeared on screen.
- A question longer than 200 characters with its options gets at least 30 seconds.
- Rules 8 and 8a: cues from grammar, the lone intangible option, stems that answer themselves, distractors outside the source's frame, false premises, and revised sayings.

Author judgment still carries what a checker cannot: whether a distractor is close. The red team remains the step that catches it.
