# Changelog

## 0.5.1 (2026-09-05) The analysis, and corrections from it

- `OFFICER ANALYSIS.md` (new): what a company grade officer does across fifteen functions, the MOS lens, the AI policy constraint, what the research on boards and on AI assisted writing changes in the tool design, the gaps ranked, five paths forward with a recommended sequence, and what to collect before the next build. Sources listed.
- `award` and `citation_check.py`: NA and NC citation limits corrected to the 2019 awards manual as carried by current subordinate instructions (8 lines, 1,250 characters, Times New Roman 10, fully justified, one inch margins, no acronyms); the 2001 order's 9 lines and 9 point were stale. Extract carries a note.
- `security-check`: the Marine Corps' own generative AI guidance (NAVMC 5239.1, MARADMIN 056/25) and DoDI 5200.48 stated on the card; DRRS-MC and anything from SIPR named out of scope; the AI assistance line in rendered products.
- `rs-profile`: the caution to a new RS that boards read relative values first and that a small profile's relative values are close to noise.
- `meritorious-promotion` and MODULES: MCO P1400.32D w/Ch 2 is the current enlisted promotion manual.
- MODULES: Training management and Legal and property packs specified; nine more core tools specified; build order rewritten to the analysis's Paths A through E.

## 0.5.0 (2026-09-04) Enlisted support tools and the award rebuild

- `award` 0.2.0: rebuilt to the seven part tool shape. `references/intake.md` (fourteen questions in five sections: frame, what actually happened, correlate to the manual, correlate to reality, the reader; the quantification ladder), `references/voice.md` (standard sentences as approved citations use them, fact verbs, the strike list, professionalism rules), `references/exemplars.md` (four fictional exemplars, one weak and annotated line by line). Level check gives one of three verdicts and never predicts a board. SOA offered in bullets or paragraphs. `citation_check.py --soa SOA.md` fails a citation carrying a number the SOA does not; warns on strike list words, semicolons, and a body with no number.
- `letter-of-recommendation` (new): six paragraph shape (standing, recommendation and ranking with a denominator, specifics, one dated scene, close, POC); `lor_check.py`.
- `letter-of-appreciation` (new): event, count, role, thanks on one page; `loa_check.py`; offers `award` when the facts reach a decoration.
- `meritorious-promotion` (new): the letter to the command's local order in the board's seven lettered categories with the numbers each expects (`references/categories.md`); `board_package_check.py`.
- `nomination` (new): quarterly and annual recognition packages on the same skeleton, scoped to the period; the order's categories win when listed.
- `board-brief` (new): the one page briefing sheet from the package's facts, three so what lines with numbers forced, timed to the clock; `brief_check.py --package` fails on any number that differs from the package.
- `counseling` (new): initial, follow on, and event counseling in worksheet blocks; incidents dated with the observer named; plan with mentor, cadence, return condition, end state; `counseling_check.py` fails on undated incidents, blocked content, and punitive promises.
- Every new tool carries `scripts/common_checks.py`: the strike list and the blocked content scan (identifiers, medical, SAPR and investigations, family, financial, substance).
- `rules-file` 0.3.0: the user writes their own billet description (responsible for, answers to and has answering, a normal week) and a module yes list; `start` 0.3.0 reads them instead of asking; `fitrep` reads the billet when the user is the MRO. Admin subfolders for Counseling, Letters, Promotions, Nominations.
- evals: `admin_check.py` 8 of 8; `enlisted_check.py` 14 of 14 including render and correspondence QC of the letter specs; judgment cases for every new tool.

## 0.4.0 (2026-09-04) Admin module core

- `fitrep` (new): Sections B, C, and I from the RS's notes to MCO 1610.7B; verbatim manual extract for Sections B, C, I and the directed comment list; `fitrep_check.py` enforces style rules, the unacceptable comments list, directed comment form, and the manual's verbatim promotion and body composition statements. Never proposes attribute marks; stops on adverse reports.
- `rs-profile` (new): private ledger of reports written; report average, RS average, high, low, relative value on the 80 to 100 scale with the manual's anchors (RS average 90, RS high 100), thirds, compression note, what if for a proposed set of marks. Chapter 8 extract verbatim.
- `award` (new): Summary of Action and citation to MCO 1650.19J format and length rules (extract verbatim), criteria and standard sentences read from the user's copy of SECNAV M-1650.1; `citation_check.py` for length, lines, capitalization, opening and closing.
- evals/admin_check.py: six deterministic cases, all passing.

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
