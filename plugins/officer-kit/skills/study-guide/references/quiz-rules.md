# Quiz rules

These apply to every quiz the tool writes. `scripts/gates.py` checks the ones a machine can check.

1. **Sourced.** The premise and the correct answer come from the source. Difficulty comes from precision, discrimination between similar items, and application of what was taught, never from facts the source does not carry. If the source is too thin for a hard question, say so; do not pad.
2. **Difficulty mix.** About 20 percent easy, 60 percent medium, 20 percent hard, spread through the quiz. Tag each question `d`.
3. **Distractors.** Plausible and close: an adjacent real value from the same source, a sibling term, the right idea in the wrong context, a partly correct answer missing its qualifier. Never two defensible answers. Throwaway options only on the easiest questions. No odd one out: if three options share a pattern the answer lacks (three items from one list, three visibly broken versions of a phrase), a student can pick the answer without knowing it; rewrite.
4. **Free recall.** At least a quarter of a guide's quiz is free recall (`"type": "recall"` with `answer` and no options): list it, state it, define it. Multiple choice alone lets a student pass by elimination and feel ready when they are not. A walkthrough's recall practice is its map modes.
5. **Positions.** The builders place correct answers in a seeded, balanced, unpatterned order (each position within one of a quarter of the questions, no two adjacent questions sharing a position, no stepping run, no two tile swing, no repeating cycle) and shuffle the distractors. Author the answer anywhere.
6. **Verified.** After the shuffle, each marked answer resolves to exactly the intended text, all four options are filled and distinct. The gate fails otherwise.
7. **Traceable.** Every answer is learnable from its own section's text; a final check may draw on all sections. When the answer is worded differently from the body, give `src`, the body phrase that proves it.
8. **No duplicates** within a product. In chat, never repeat a question.
9. **Explained.** Each question carries `e`: why the answer is right, in the source's terms. The guide's key also prints where each answer is taught, so a miss sends the student back to the right section.
