# A/B test: study-guide 0.1.0 against 0.2.0 (23 Sep 26)

**Question.** Does the rebuilt `study-guide` produce a better product than the tool it replaces, judged blind?

**Setup.** Two drafters (same model, separate folders, neither aware of the other) got the same request, "I have a test on this chapter next week. Make me a study guide," and the same source: MCDP 7 Learning, chapter 3 (`source-mcdp7-ch3.txt`, public). Drafter A had the 0.1.0 skill (`old-SKILL.md`); drafter B had 0.2.0. Both had the 0.12.0 kit standards. A coin flip (seed 20260923, 0.345) made A product X and B product Y. Lines that named the tool's own instructions were removed from X before judging. Three blind judges: `source-fidelity-reviewer` on each product, and `red-team` comparing both against the chapter.

**Result.** The blind comparison chose **Y, the 0.2.0 product**: "X's failures are gaps in content: things a test can ask that X never teaches, plus one paraphrase that teaches a wrong link. A student cannot recover from those without the chapter." Both passed the fidelity review with zero unsourced facts and zero untraceable answers; Y carried the whole chapter, X dropped testable phrases (for example, assessments measure "the learner's progress and the instructor's effectiveness").

**What the old tool got right, and 0.2.0 took from it.** The judge named X's strongest trait: free recall questions and a "where it is" pointer for every answer. 0.2.0 now requires at least a quarter free recall in a guide's quiz, and its answer key prints where each answer is taught.

**Other findings fixed before release.** Multiple choice solvable by elimination (odd one out rule added), a table cell filled by inference (rule: write "not stated"), and eight layout defects found by the visual reviewer over four passes on the rendered guide and four on the walkthrough, all fixed in the builders.

**Side finding.** Drafter A, using the old skill, applied kit standard 7 from 0.12.0 on its own and added a complete section by section part to what the old skill calls a one page guide. The kit standards shipped that day already lifted the old tool.

Files: `old-SKILL.md`, `STANDARDS.md` (as given to both), `source-mcdp7-ch3.txt`, `productX-old-tool.txt`, `productY-new-tool.txt` (the .docx as text; tables appear at the end because of the text conversion, not in the document).
