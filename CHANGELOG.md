# Changelog

## 0.3.2 (2026-09-04) from zero

- GETTING STARTED.md: for someone who has never opened Cowork. What Cowork is, the one idea (Claude only knows what you give it), what is safe to give it, the five things you set up, the thirty minute path, the words you will see, what to do when something goes wrong.
- `library` (new): what the library is and why, three ways to build it (starter set by hand, full publications library via marine-regs, your own documents), the starter set per module with where to download each, MCPEL and DONI instructions, `library_check.py` coverage report.
- `start`: step 0 orientation for first time Cowork users; library step added before the first task.

## 0.3.1 (2026-09-04) reframed for officers in general

- README rewritten in plain language: what you are installing, first run in ten minutes, the modules.
- MODULES.md replaces ROADMAP.md: every tool by module (Correspondence, Admin, Planning, Training and teaching, Verify, Share and improve), what to say, what it does, the governing publication, and status. Admin module specified: award, fitrep, rs-profile, counseling, weekly-update, after-action, training-schedule.
- `start` replaces `field-kit-start`: install check, working folder structure matched to the user's job, connect the folder, rules file, first real task.
- No more "sprints" anywhere; build order is listed at the end of MODULES.md.

## 0.3.0 (2026-09-04) Sprint 0: the core

- `rules-file` v0.2: three depths (Light, Standard, Full), every question optional, skipped fields written as "not recorded (ask me at draft time)", correspondence identity block for letters, update in place.
- `naval-letter` (new): the standard as a reference, `build_letter.py` (JSON spec to docx on the 13.8 pt grid), `qc_letter.py` (Gate 2a, now also refuses placeholders), `measure_pdf.py` (Gate 2b, every gap on the page measured). Three evals passing.
- `qc-gates` (new): picks the gates by product type and runs the blind reviewers until clean; gate report format.
- `capture-source` (new): capture protocol for online lessons, files, and photos with the read back gate; `capture_check.py`.
- Evals for naval-letter (deterministic), capture-source, rules-file.

## 0.2.0 (2026-09-04) skeleton

- Repo created as a marketplace with one plugin, `officer-kit` (renamed from claude-field-kit the same day).
- Field Kit v0.1.0 skills carried over unchanged: field-kit-start, security-check, rules-file, folder-triage, study-guide, order-critique, inbox-triage, week-ahead, build-a-skill, fleet-transition.
- Five reviewer agents added, written from the correspondence standard and QC gates: significance-reviewer (Gate 0), evidence-reviewer (Gate 1), visual-reviewer (Gate 3), source-fidelity-reviewer (teaching products), researcher.
- ROADMAP.md: the six officer functions, every planned skill as a build spec, hooks, sprints.
- LEARNINGS.md queue seeded with eight lessons from the TBS build history.
- evals/ layout and grader rules.
- scripts/package.sh builds the installable .plugin file.

## 0.1.0 (2026-08) workshop release

- Ten skills for the Claude Field Kit workshop.
