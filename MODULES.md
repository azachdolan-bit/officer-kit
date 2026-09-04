# Modules

Every tool in the kit, grouped by the kind of work it serves. **Available** means it is in the installed plugin now. **Building** means it is specified and next in line. **Planned** means specified, not yet started.

Standing rules for every tool: build from the user's sources only, never from general knowledge; verify before delivering; save every product to the working folder in the same session; nothing personal and no unit content inside the plugin itself.

Each tool lists the governing publication it is built to. School handouts outrank the parent manual where they differ; the newer school document wins.

## Correspondence

| Tool | Say | Does | Governed by | Status |
|---|---|---|---|---|
| `naval-letter` | "draft a naval letter to..." | Builds the letter from your rules file identity on the exact line grid, checks references both ways, measures the rendered page, refuses to ship a placeholder | SECNAV M-5216.5; the school correspondence handout where issued | Available |
| `endorsement` | "endorse this request" | First through nth endorsements in the same standard | SECNAV M-5216.5 | Planned |
| `memo` | "memo for the record", "write a MFR" | Memorandum and memorandum for the record formats | SECNAV M-5216.5 | Planned |

## Admin

| Tool | Say | Does | Governed by | Status |
|---|---|---|---|---|
| `award` | "write up an award for...", "NAM citation", "summary of action" | Intake that quantifies what the Marine did, a level check against the manual's criteria (reaches, reaches a lower level, does not reach), then the summary of action and citation with no word the facts do not carry; the checker fails a citation that carries a number the SOA does not | MCO 1650.19J (processing, SOA and citation format) and SECNAV M-1650.1 (criteria, standard sentences, read from the user's Reference copy) | Available |
| `fitrep` | "draft a fitrep for...", "section I from these notes", "billet description" | Section I directed comments, billet description, and duties assigned from your notes; checks every attribute mark has a justifying comment and every prohibited item is absent | MCO 1610.7B (Performance Evaluation System); the school fitness report handout where issued | Available |
| `rs-profile` | "how does this mark affect my profile", "manage my profile", "relative value" | Keeps a private ledger of reports written, computes each report average, the RS average, high, and low per grade, and relative value on the 80 to 100 scale; shows where a proposed set of marks lands; flags a compressing profile; never proposes marks | MCO 1610.7B chapter 8 | Available |
| `counseling` | "counseling from these notes", "initial counseling", "event counseling" | Initial, follow on, or event counseling in the worksheet's blocks: incidents as dated facts with the observer named, an evaluation that names the cost to the unit, a plan with a mentor, a cadence, a return condition, and an end state; scrubbed of medical, family, and disciplinary content; never punitive | MCO 1500.61 (Marine Leader Development) where applicable | Available |
| `weekly-update` | "weekly update to my OIC" | BLUF first update in your boss's format from the rules file | none | Planned |
| `after-action` | "turn these range notes into an AAR" | What happened, what worked, what to fix, in the unit's format | none | Planned |
| `training-schedule` | "build the training schedule from this list" | Week view from events with prep items | none | Planned |
| `letter-of-appreciation` | "letter of appreciation for", "LOA" | Letter of appreciation for a Marine or a supporting unit, in correspondence format, from the facts of what they did | SECNAV M-5216.5 | Available |
| `letter-of-recommendation` | "letter of recommendation for", "recommend this Marine for" | Recommendation for a program, school, commissioning source, or civilian purpose; intake for what the reader is deciding and what the Marine did that bears on it | SECNAV M-5216.5; the program's own instruction where one exists | Available |
| `meritorious-promotion` | "mer pro package", "meritorious promotion for" | The meritorious promotion recommendation as the boards read it: letter to the local order, lettered paragraphs in the board's scoring categories with the numbers each expects, the data sheet and enclosure list, and the board briefing sheet | MCO 1400.32 (Enlisted Promotion Manual); the command's local order (MEF, Wing, or Group) | Available |
| `enlisted-program-package` | "package for", "recommend for MECEP", "recruiting duty screening" | Command endorsement and justification for an enlisted Marine's application to a program or special duty, to that program's MARADMIN or order | the program's governing order; SECNAV M-5216.5 | Planned |
| `nomination` | "NCO of the quarter package", "Marine of the year nomination" | The quarterly and annual recognition nomination: letter to the local order with the lettered categories the board scores (appearance and fitness, MOS competence, deployments, maturity, leadership, growth, influence on the command), the data sheet, and the enclosure list the order requires | the command's recognition order (a Wing or MEF order); SECNAV M-5216.5 | Available |
| `board-brief` | "brief this Marine to the board", "briefing sheet" | The one page board briefing sheet generated from the same facts as the package: billet, duties, TIS and TIG, PME, PFT, CFT, rifle, pistol, swim, MCMAP, reading, education, community service, awards, and the "so what" lines, timed to the board's clock | the command's board instructions | Available |
| `brief` | "build a brief", "slides for", "decision brief" | A PowerPoint brief from an intake for audience and the decision sought; one message per slide; every slide read by the visual reviewer | none | Planned |

## Planning

| Tool | Say | Does | Governed by | Status |
|---|---|---|---|---|
| `order-critique` | "critique my order", "is my OSMEAC complete" | Completeness and clarity review of a five paragraph order | MCTP 3-10A; the school tactical planning handouts | Available |
| `order-analysis` | "analyze this order", "METT-TC", "find the contradictions" | Hasty METT-TC worksheet from an order; internal contradiction audit; map and grid checks with a stated error budget; the list of things that look like defects but are not | MCDP 1-0 App C; MCTP 3-10A; the school handouts | Planned |
| `tactical-planning` | "walk me through the planning process", "task statement" | Playbook driven planning from receipt of order to complete plan; task statement builder from the doctrinal task list; TDG session mode | MCDP 1-0; the school tactical planning handouts | Planned |
| `call-for-fire` | "CFF drill", "check this call for fire" | Drills, scenario generation with geometry that closes, mil relation and bracketing checks | MCRP 3-10F.2; the school handout where issued | Planned |

## Training and teaching

| Tool | Say | Does | Governed by | Status |
|---|---|---|---|---|
| `capture-source` | "capture this lesson", "transcribe these photos" | Complete text of an issued source saved on disk, completeness checked, read back gate for photos | none | Available |
| `study-guide` | "make a study guide", "quiz me" | Guide, quiz, flashcards from a source; knowledge first, then practice scenarios | none | Available (v0.1; house docx generator in the next version) |
| `walkthrough` | "build an interactive walkthrough" | Sectioned HTML class walkthrough carrying the complete source with check yourself quizzes; two completeness gates | none | Planned |
| `quiz-builder` | "build a Kahoot", "challenge deck", "host key" | Decks from the official import template, balanced shuffle, bell curve difficulty, verbatim answer check, host answer key | none | Planned |
| `drill-builder` | "make a drill for this report format" | Procedural drills and shareable zero content builders | none | Planned |
| `print-card` | "make a 5x8 card", "laminate" | Duplex cards at 3x5, 4x6, 5x8, letter | none | Planned |
| `topic-brief` | "brief on...", "presentation card" | Topic scoped brief with numbers hygiene and a cue card | none | Planned |

## Verify

| Tool | Say | Does | Status |
|---|---|---|---|
| `qc-gates` | "QC this before I sign", "run the gates" | Picks the gates by product type and runs the reviewers until clean; gate report | Available |
| `significance-reviewer` (agent) | runs inside qc-gates | Is a true observation actually a defect worth reporting? | Available |
| `evidence-reviewer` (agent) | runs inside qc-gates | Is every claim proven verbatim against the source? What did the draft miss? | Available |
| `visual-reviewer` (agent) | runs inside qc-gates | Does every rendered page read correctly? SHIP or NO SHIP | Available |
| `source-fidelity-reviewer` (agent) | runs inside qc-gates | Does a teaching product carry the source completely and add nothing? | Available |
| `researcher` (agent) | on demand | Wide read only research returning a fixed table | Available |

## Share and improve

| Tool | Say | Does | Status |
|---|---|---|---|
| `start` | "start the officer kit" | First run walkthrough: install check, working folder, connect it, rules file, first task | Available |
| `library` | "build my library", "which pubs do I need" | Explains what the library is, three ways to build it (starter set by hand, the full publications library with one command via the marine-regs plugin, your own unit documents), the starter set per module with where to get each, and a coverage check | Available |
| `security-check` | "is this safe to share" | Green, yellow, red; folder scan before linking | Available |
| `rules-file` | "build my rules file" | Interview at Light, Standard, or Full depth; every question optional | Available |
| `build-a-skill` | "build a skill", "I do this every week" | Interview to a working skill with tests | Available |
| `share-method` | "make this shareable" | A method file with zero content a peer can run on their own material | Planned |
| `fleet-transition` | "I'm at my first unit" | Day one and week one at a new command; updates the rules file | Available |
| `folder-triage`, `inbox-triage`, `week-ahead` | "organize this folder", "triage my inbox", "week ahead" | Folder inventory and structure; inbox buckets with drafted replies; weekly brief | Available |
| `aar` | "capture lessons" | Writes corrections and reviewer catches to the lessons queue; never edits a tool | Planned |
| `inspect` | "review the lessons queue" | Turns the queue into proposed changes, runs the tool's tests, ships approved changes | Planned |

## Build order

1. Done: `start`, `library`, README, GETTING STARTED, this file; the Admin module core (`award`, `fitrep`, `rs-profile`) built from the governing manuals with mechanical checks and tests; the enlisted support tools (`letter-of-recommendation`, `letter-of-appreciation`, `meritorious-promotion`, `nomination`, `board-brief`, `counseling`) built to the seven part shape from annotated real packages, with fictional exemplars, intake, checkers, and evals; billet self reporting in `rules-file`.
2. **Next:** `order-analysis`, `quiz-builder`, `study-guide` v0.2, `walkthrough`.
4. **Then:** `aar` and `inspect`, so the kit improves itself; `share-method`; the remaining Admin and Correspondence tools.
5. **Then:** a workshop cut with everything verified content free by script.
