# Changelog

## 0.8.1 (2026-09-05) It would not install

The first real install attempt failed with eight errors while all five eval harnesses were green. The kit had no check for whether the package would install.

- All six agents had invalid YAML frontmatter. An `<example>` block starting at column 1 parses as a new YAML key, so the whole block failed. A previous session concluded this was by design and changed the eval to a regex, which hid it for two versions. Every agent description is now a literal block scalar under 1024 characters, with surplus examples moved into the body where nothing is lost.
- The plugin description was 683 characters against a 500 limit. Rewritten to 478.
- The `inspect` skill description contained `<tool>`, which is not allowed in a skill description. Reworded.
- `evals/install_check.py` (new): runs the installer's checks in the repository. Both manifests parse and fit their limits, plugin.json and marketplace.json agree on the version, every skill and agent frontmatter parses with a name and a description that fits, no XML tags in skill descriptions, and every advertised script parses. 94 of 94.

## 0.8.0 (2026-09-05) Four rules, after the test

0.7.1 fixed the two defects the A/B test found and left the rest of the thinking layer standing. This release removes the rest of it. What the test actually rewarded was small, and what it punished was the apparatus: a template gets filled in instead of thought about.

Four rules survive, in `skills/think/SKILL.md`, and they are the whole skill:

1. Assume it already failed and write three reasons before drafting anything.
2. Ask only the questions whose answers change the product, and never put a candidate answer inside the question.
3. Say what you assumed and mark it in the product. Never write that the rest is covered.
4. Hand anything that gets signed to the blind `red-team` agent.

Removed:

- `think/references/estimate.md`, `check.md`, `tripwires.md`, `by-modality.md`, and `think/scripts/estimate_check.py`. The estimate produced the false coverage claim and anchored on its own example; its purpose was to surface unknowns and the drafter without it surfaced more of them. The premortem survives as rule 1, reconciliation is what the product checkers already do, and the rest was ceremony.
- The announced consequence tier. A tool telling the user which tier it is running at is output that changes nothing.
- The tier block on the four routine tools, entirely.

Changed:

- The 20 tools that produce something someone signs carry the four rules in a `## Before you draft` block, with each tool's own tailoring kept: the premortem before the hazard list on a risk worksheet, competing hypotheses on an investigation, MCWP 5-10 Appendix G on an order.
- `precision_check.py` absorbs the coverage claim patterns and is now the skill's only script.
- `CRITICAL THINKING.md` Part 4 is now what was built, what was tested, and what survived, and it says the kit got smaller after being tested. Parts 1 through 3 are unchanged, because the evidence in them is what predicted this result.
- `start/references/conventions.md` convention 5, MODULES.md, `evals/think_check.py` (13 of 13).

## 0.7.1 (2026-09-05) The thinking layer, tested against itself

0.7.0 shipped an estimate and a check onto 24 tools without ever running one end to end. This release is that test and what it found. The test is in `evals/ab-test-2026-09-05/` with every artifact, because the result went against the feature.

Two blind drafters built a risk assessment worksheet from the same tasking, one with the thinking layer and one with it deleted. A blind reviewer, given both with provenance stripped and told nothing about how either was made, chose the worksheet built **without** it. Both passed `raw_check.py` clean, both reached the same residual level and the same approval authority, and both left ten blanks open. The difference was that the thinking layer's product asserted 25 facts the tasking never supplied while telling the approving officer in writing that every gap was marked.

- `think/references/estimate.md`: the worked example was a live fire range worksheet, the same product as the tool most often run at this tier, and it supplied three of the five questions the test's drafter asked while displacing the one question the tasking actually raised. It is now a 6105 entry, and it opens by saying its content is not to be taken. `estimate_check.py` fails an estimate that lifts its phrases.
- `think/references/check.md`: pass 6 now forbids the coverage claim and carries the test as its evidence. "What was not checked" says what was not checked; it never says that everything else was.
- `think/scripts/precision_check.py`: a coverage claim in a delivered product fails at every tier. Also, risk levels (IE, IID, IIB) no longer read as undefined acronyms, which had been adding about twenty junk warnings to every worksheet.
- evals: `think_check.py` 14 of 14, with an assertion for each of the three defects.

Not changed, pending a decision: the deliberate tier still runs on all 12 tools. One test cannot separate the mechanism from run to run variance, and the thinking layer's product did find four hazards the other missed, including operator fatigue on the return movement, which the other sheet left as a named phase with no hazard in it.

## 0.7.0 (2026-09-05) Thinking as a mechanism

The kit produced documents faster than it thought about them. This release adds the thinking, built from the published evidence on how assistants fail rather than from intuition about what careful looks like, because three of the obvious fixes are measurably harmful.

- `CRITICAL THINKING.md` (new): how an assistant produces confident, plausible, wrong work; which fixes make it worse (self review with no external signal, rigid schemas around reasoning, mandated checklists, "are you sure", asking the model to explain itself as verification); what works; and the honest claim, which is legibility rather than accuracy. Sources throughout.
- `think` (new skill): the estimate before drafting (task and outcome with the XY check, standard, facts separated from assumptions tested against MCWP 5-10's four questions, the questions whose answers change the product, what this will not do, how it gets checked), the check before delivery (premortem with the failure asserted, expected but absent, adversarial read, reconciliation, single rapid reading, what was not checked), ten named tripwires, and per modality tailoring for risk, planning, writing, investigation, and evaluation.
- Consequence tiers on all 24 product tools: deliberate when someone can be hurt or it enters a record or has legal effect or a board decides irreversibly; rapid when it goes to a decision maker and is reversible; running for routine work. The tool names its tier and trigger in one line and anyone can raise it.
- `red-team` (new agent): blind adversarial pass on deliberate products. Premortem, expected but absent, adversarial read of every directive sentence, comparison against the standard and an exemplar. Findings with evidence, never a score.
- `think/scripts/estimate_check.py`: fails an estimate with no tier, an assumption sitting in the facts, an assumption with no falsifier or no collapse consequence, a question that does not say what it changes, or a question that carries its own answer.
- `think/scripts/precision_check.py`: center embedding, sentence length against AR 25-50's 15 word target, paragraphs past 10 lines, soft quantifiers, actorless passive directives, hidden verbs, mixed modals, loose sentence initial pronouns, unexpanded acronyms, "and/or", vague deadlines. Advises on style and fails on ambiguity that changes what the reader must do, with `--directive`. Skips text the order prescribes.
- `start/references/conventions.md`: a fifth convention, thinking is proportional and it is written down.
- evals: `think_check.py` 9 of 9, including that every product tool carries its tier and that the red team agent refuses to score.

## 0.6.2 (2026-09-05) Library first, mechanically

- `library/scripts/find_order.py <number>`: finds a publication in the Library path and Reference folder named in the rules file, extracts its text (`--text`, `--grep`), or renders a page as an image (`--page N --png`); exit 1 naming the roots searched when it is not on disk. Every tool reads an order through it before anything else; the web is for publications it reports as not on disk, and the standard file says which those were.
- `rules-file`: a Library section (Library path, Reference folder, the rule) in the template, the example, and the interview.
- `build-a-skill/references/tool-shape.md` and `BUILD STRATEGY.md`: the standard is read from the library and cites the file it came from.

## 0.6.1 (2026-09-05) Read from the user's own library

- `risk-assessment`: Figures 3-4 and 4-2 read from the user's copy of MCO 5100.29C and confirmed cell by cell; the caution is gone. Paragraphs 030302, 040203, 040302, 040303, and 040304 verbatim, including the EAP's minimum content, which the checker now warns on.
- `page-11`: MCO 1900.16 paragraph 6105 read from the user's copy. The order prescribes the entry's wording and requires the commanding officer's signature on adverse Page 11 entries, with a copy to CMC (MMRP-20) within 30 days. The tool, exemplar, and checker now use the order's format word for word; the checker fails an altered fixed sentence or a counselor's signature.
- `training-schedule`: MCO 1553.3C verbatim on the MCTIMS calendar's required fields, unit documents, and the commander's responsibilities.
- `dd200`: Volume 17 (FLIPL) and Volume 1 identified as the governing volumes; neither is in the library yet.
- LEARNINGS: read the order from the user's library first, render figure pages as images.

## 0.6.0 (2026-09-05) Infrastructure: yours, not the author's; the Training pack; the Legal and property pack

Built from the orders with fictional exemplars, because no real exemplars were available, and built so that every tool reads the user's own material first when it exists.

- Names removed by default (Path A): every product tool works on `<MARINE>` (grade and billet stay); `security-check/scripts/substitute.py` puts the name into the finished file on the user's computer and stores nothing; `build_letter.py` writes "Drafted with AI assistance (Officer Kit). The signer owns the words." into the file properties; `rules-file` records a working label.
- Make it your own: `Overrides/<tool>.md` (the command's way, read first by every tool), `Reference/Exemplars/<tool>/` (the command's approved products as patterns, read before the plugin's), the user's own `LEARNINGS.md` and `Proposals/`. `start/references/conventions.md` states the four conventions; `MAKE IT YOUR OWN.md` in the repo is the guide.
- `add-exemplar` (new): sanitizes an approved product into a pattern with an annotation; `scrub_check.py` fails on any residual name, identifier, or blocked content.
- `aar` (new): one lesson at a time into the user's queue, evidence first, fixed format; `lesson_check.py` fails malformed entries and forces any lesson that softens a check to low confidence.
- `inspect` (new): applies approved lessons one at a time to overrides or exemplars, or writes a proposal for the plugin; never edits the plugin; rejects softening lessons on sight.
- `build-a-skill`: `new_tool.py` scaffolds a kit tool in the seven part shape with TODO markers and evals; `references/tool-shape.md`; the finish checklist.
- Training pack (new): `risk-assessment` (MCO 5100.29C Vol 2; `raw_check.py` computes levels from the matrix, flags high risk training at IA, IB, IIA, IIB, names the approver, requires the four elements, fails a residual improvement without a control), `after-action`, `training-schedule` (MCO 1553.3C; conflicts, RAW status, prep list), `safety-brief` (three things with a number or an event by type), `range-package` (the pocket guide's OIC and RSO duties, cease fire language, MEDEVAC route and time).
- Legal and property pack (new): `investigation` (JAGMAN Chapter II and the NJS handbook; `investigation_check.py` enforces the findings to enclosures to opinions to recommendations chain, enclosure (1) the convening order, the 30 day clock, no signed statements in injury cases), `page-11` (the four 6105 elements, the rebuttal advisory, the not recommended deadline), `dd200` (the same chain engine plus the property table and the negligence opinion), `inspection-prep` (IGMC checklist self assessment with corrective action plan and binder).
- `common_checks.py` blocked content patterns narrowed so military words ("assault" in an attack, "custody" of property, "SAPR" as a training topic) pass and the personal senses still fail.
- evals: `packs_check.py` 25 of 25 (nine tools, both directions, plus substitute, scrub, lesson, and scaffold); `admin_check.py` 8 of 8; `enlisted_check.py` 14 of 14; naval letter 3 of 3. 35 skills.

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
