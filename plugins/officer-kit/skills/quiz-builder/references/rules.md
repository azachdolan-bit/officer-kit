# Quiz rules

`scripts/build_kahoot.py` checks every rule marked (checked) and refuses to write a file that fails one. The rest are the author's job and the blind reviewer's.

## Sourcing

1. **From the source only** (checked when sources are passed). The premise and the correct answer come from the user's notes, the captured lesson, or a reference actually read. When the answer is worded differently from the source, give `src`, the exact source phrase that proves it. Never invent a fact to make a question harder. If the source is too thin for a full deck, say so and combine it with a related topic.
2. **A place to send the player.** Every question carries `ref`: the section heading and page where the source teaches it. It prints in the host key.

## Writing the question

These follow the item writing guidelines of Haladyna, Downing, and Rodriguez (2002), adjusted where the author's own rules are stricter.

3. **Positive stems** (checked). A "which is not" or "except" question is allowed only when the point being tested is the exception, and then the word is written in capitals.
4. **No "all of the above", "none of the above", or "both of the above"** (checked). Write a real distractor.
5. **Two to four options** (checked). Three good options beat four with a throwaway; do not pad.
6. **Plausible, close distractors:** an adjacent real value from the same source, a sibling term, the right idea in the wrong context, a partly correct answer missing its qualifier. Never two defensible answers. Keep options alike in grammar and length.
7. **No length cue** (checked). In a deck of ten or more, the correct answer may be the single longest option in no more than 40 percent of questions.
8. **No odd one out, and no other cue.** If three options share a pattern the answer lacks, a player can pick it without knowing it. The same holds for grammar (only the answer agrees with the stem's tense or pronoun), for the one intangible option among concrete ones, for a stem that gives away its answer ("In a learner-centric model, what is the main focus?"), and for words only the correct option shares with the stem (checked, as a warning). Draw distractors from inside the source's own frame; a distractor that contradicts the lesson's thesis is eliminated by anyone who knows what kind of lesson it is.
8a. **No false premise and no giveaway across questions.** A stem may not assume what the source denies ("what is the single correct design" when the source says there is none). When a source revises a known saying, ask for the source's version by name, or the familiar version becomes a defensible answer. An answer that already appeared on screen in an earlier question's options is flagged (checked, as a warning).
9. **Difficulty** (checked, as a warning). About 20 percent easy, 60 percent medium, 20 percent hard, spread through the deck. Hard comes from precision, discrimination, and application, never from trivia the lesson did not stress.
10. **No duplicates** (checked) within a deck or across a set. Defining a term in one deck and applying it in a scenario in another is fine; asking the same fact the same way twice is not. Keep coverage in proportion to the source's weight.

## Kahoot mechanics

11. **The user's copy of Kahoot's official template, every time** (checked). Kahoot's importer expects the template's instruction rows, merged cells, and time dropdown; a file built from scratch looks right and breaks on import. The builder copies the template, overwrites the example row, and extends the dropdown.
12. **Field limits** (checked): question 120 characters, each answer 75. Tighten the wording; never cut the rule.
13. **Times the template allows** (checked). The builder reads the allowed list from the template's own dropdown, because Kahoot's published list has changed. Default: easy and medium 20 seconds, hard 30, and at least 30 for any question whose stem and options run past 200 characters, so reading time does not become the difficulty.
14. **Positions** (checked). Correct answers are placed by a seeded shuffle: balanced across the slots in each deck, no two adjacent questions on the same slot, no run of the answer stepping to the next tile, no swing between two tiles, and no repeating cycle (checked), distractors shuffled too. A set of numeric options is put in ascending order instead, and its position is left where the numbers fall.
15. **Read back** (checked). After writing, the builder opens each file and confirms that the correct slot holds the intended answer text, every answer cell used is filled, and every time is allowed. Kahoot stores the answer as a slot number, so this is where a shuffle silently breaks a quiz.
16. **Deck size** (warning over 40). Split a long deck on a natural boundary in the source.

## Integrity

17. A quiz built from course material stays with the people who built it (kit standard 6). Never compile or reuse actual assessment questions.
