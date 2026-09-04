# Evals

Every skill ships with at least three golden cases before its instructions grow past a page. A skill edit that fails its evals does not ship.

Layout:

```
evals/
  <skill-name>/
    cases.json          the cases: query, input files, expected behaviour
    inputs/             golden inputs (method only; no course content, no identity)
    expected/           golden outputs or the checker that grades them
    check.py            optional: deterministic grader (exit 0 pass, 1 fail)
    private/            gitignored: real inputs kept locally for a personal run
```

`cases.json` format, one object per case:

```json
{
  "skill": "naval-letter",
  "query": "Draft a letter requesting review of an unsourced objective on the phase exam",
  "files": ["inputs/sample_sources.md"],
  "expected_behavior": [
    "Heading block matches the rules file identity, not a reconstructed one",
    "qc_letter.py exits 0",
    "Signature block is 55.2 pt below the last text line in the rendered PDF"
  ]
}
```

Two kinds of grader:

- **Deterministic** (correspondence, quizzes, call for fire): a script on a golden file. `qc_letter.py` on a known good letter, `verify_kahoot.py` on a known good deck, `cff_check.py` reproducing the worked examples.
- **Judgment** (study guide, walkthrough, brief): a golden input plus a rubric the `source-fidelity-reviewer` or `evidence-reviewer` applies.

Run pattern: edit the skill in one session, run the evals in a fresh session, so the test does not inherit the editor's context. When `claude plugin eval` becomes available, these cases port to it unchanged.
