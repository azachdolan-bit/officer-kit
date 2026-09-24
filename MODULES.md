# Modules

Every tool in the kit, grouped by the kind of work it serves. **Available** means it is in the installed plugin now. **Building** means it is specified and next in line. **Planned** means specified, not yet started.

Standing rules for every tool: build from the user's sources only, never from general knowledge; verify before delivering; save every product to the working folder in the same session; nothing personal and no unit content inside the plugin itself.

Each tool lists the governing publication it is built to. School handouts outrank the parent manual where they differ; the newer school document wins.

## Correspondence

| Tool | Say | Does | Governed by | Status |
|---|---|---|---|---|
| `naval-letter` | "draft a naval letter to..." | Builds the letter from your rules file identity on the exact line grid, checks references both ways, measures the rendered page, refuses to ship a placeholder | SECNAV M-5216.5; the school correspondence handout where issued | Available |
| `directive` | "write the company SOP", "battalion order for" | Picks Order or Bulletin from the purpose, writes the order's own paragraph structure with every required statement, and checks them; a bulletin without its self canceling provision fails | MCO 5215.1K w/Admin Ch 3 | Available (no directive type is defined for an SOP, and the SSIC manual is not in the library) |
| `endorsement` | "endorse this request", "first endorsement on" | The identification line, From, To, Via, the basic letter's own Subj, and the action in the first sentence with a reason the addressee can check; the 9-2.5 significant or routine test that decides the copy to block, and the continued lettering of what the endorsement adds; renders and measures on the letter grid | SECNAV M-5216.5 ch 9; the endorsements MCO 1900.16 and NAVMC 4000.5D reproduce | Available (chapter 9 sets no wording for a return without action, no test for substantive comments, and no letterhead rule; the builder prints no copy to block and starts a Ref block at (a)) |
| `memo` | "memo for the record", "point paper", "decision paper", "from to memo", "MOA", "business letter" | The five staff papers the publication prints, each in its appendix's parts and words, and the MFR renders on the letter grid; the chapter 10 memorandums (From-To on the OPNAV printed form, plain paper, letterhead, the approval and disapproval decision block, and the MOA or MOU with the senior signing on the right and signing last) and the chapter 11 business letter, each written and checked in the manual's own parts | MCTP 3-30A ch 3 and App A to E; SECNAV M-5216.5 ch 10 and 11; MCO 5216.20B ch 13 | Available (the chapter 10 and 11 formats are written and checked but not rendered or measured; the manual gives the From-To form two different OPNAV numbers, puts the business letter's identification symbols on the left in its text and on the right in every figure, and never mentions a copy to block on a memorandum) |

## Admin

| Tool | Say | Does | Governed by | Status |
|---|---|---|---|---|
| `award` | "write up an award for...", "NAM citation", "summary of action" | Intake that quantifies what the Marine did, a level check against the manual's criteria (reaches, reaches a lower level, does not reach), then the summary of action and citation with no word the facts do not carry; the checker fails a citation that carries a number the SOA does not | MCO 1650.19J (processing, SOA and citation format) and SECNAV M-1650.1 (criteria, standard sentences, read from the user's Reference copy) | Available |
| `fitrep` | "draft a fitrep for...", "section I from these notes", "billet description" | Section I directed comments, billet description, and duties assigned from your notes; checks every attribute mark has a justifying comment and every prohibited item is absent | MCO 1610.7B (Performance Evaluation System); the school fitness report handout where issued | Available |
| `rs-profile` | "how does this mark affect my profile", "manage my profile", "relative value" | Keeps a private ledger of reports written, computes each report average, the RS average, high, and low per grade, and relative value on the 80 to 100 scale; shows where a proposed set of marks lands; flags a compressing profile; never proposes marks | MCO 1610.7B chapter 8 | Available |
| `counseling` | "counseling from these notes", "initial counseling", "event counseling" | Initial, follow on, or event counseling in the worksheet's blocks: incidents as dated facts with the observer named, an evaluation that names the cost to the unit, a plan with a mentor, a cadence, a return condition, and an end state; scrubbed of medical, family, and disciplinary content; never punitive | MCO 1500.61 (Marine Leader Development) where applicable | Available |
| `mrow-input` | "my fitrep input", "MROW for my report" | The Marine's own billet description and summary of accomplishments in the order's section B and C form, with what the order keeps out of section C kept out and awards and PME sent where the order sends them | MCO 1610.7B ch 1, 2, 4 | Available |
| `jepes-input` | "JEPES marks for my Marines" | Command input marks with the dated facts under each, the band the number falls in, the occasion and dates against the order's table, and the initial counseling the FLS owes within 30 days | MCO 1616.1 | Available (Figure 1-2, the evaluation metrics, is an image and not in the library) |
| `reenlistment` | "reenlistment recommendation for", "RELM comments" | The tier in the form's words with the population count that makes it true, comments under the order's three heads, the 21 prerequisite screen, the interview windows, and the CO's own interview when a Marine is not recommended | MCO 1040.31 | Available |
| `meritorious-mast` | "mer mast for", "certificate of commendation for" | The level check on the order's recognition ladder, the text from the facts and nothing else, and the routing the order sets | MCO 1650.19J | Available (iAPS per MARADMIN 024/22 not in the library) |
| `board-prep` | "major board is coming", "audit my OMPF" | The board's dates from the message, the OMPF and MBS audit with what was verified and when, PME held against the requirement, reading against the list, and the letter to the president inside the message's rules | MARADMIN 622/25; MCO 1553.4B; ALMAR 024/25 | Available (the zone MARADMIN and the photograph requirement not in the library) |
| `deocs-plan` | "DEOCS action plan" | Each finding as the report states it with one action carrying an owner by billet, a date, and a measure; no respondent identified | MARADMIN 306/25; MCO 5354.1G | Available (the deadlines and plan format live in DoDI 6400.11, not in the library) |
| `weekly-update` | "weekly update to my OIC" | BLUF first update in your boss's format from the rules file | none | Planned |
| `after-action` | "turn these range notes into an AAR" | What happened, what worked, what to fix, in the unit's format | none | Available |
| `training-schedule` | "build the training schedule from this list" | Week view from events with prep items | none | Available |
| `letter-of-appreciation` | "letter of appreciation for", "LOA" | Letter of appreciation for a Marine or a supporting unit, in correspondence format, from the facts of what they did | SECNAV M-5216.5 | Available |
| `letter-of-recommendation` | "letter of recommendation for", "recommend this Marine for" | Recommendation for a program, school, commissioning source, or civilian purpose; intake for what the reader is deciding and what the Marine did that bears on it | SECNAV M-5216.5; the program's own instruction where one exists | Available |
| `meritorious-promotion` | "mer pro package", "meritorious promotion for" | The meritorious promotion recommendation as the boards read it: letter to the local order, lettered paragraphs in the board's scoring categories with the numbers each expects, the data sheet and enclosure list, and the board briefing sheet | MCO P1400.32D w/Ch 2 (Enlisted Promotion Manual, 2012); the command's local order (MEF, Wing, or Group) | Available |
| `enlisted-program-package` | "package for", "recommend for MECEP", "recruiting duty screening" | Command endorsement and justification for an enlisted Marine's application to a program or special duty, to that program's MARADMIN or order | the program's governing order; SECNAV M-5216.5 | Planned |
| `nomination` | "NCO of the quarter package", "Marine of the year nomination" | The quarterly and annual recognition nomination: letter to the local order with the lettered categories the board scores (appearance and fitness, MOS competence, deployments, maturity, leadership, growth, influence on the command), the data sheet, and the enclosure list the order requires | the command's recognition order (a Wing or MEF order); SECNAV M-5216.5 | Available |
| `board-brief` | "brief this Marine to the board", "briefing sheet" | The one page board briefing sheet generated from the same facts as the package: billet, duties, TIS and TIG, PME, PFT, CFT, rifle, pistol, swim, MCMAP, reading, education, community service, awards, and the "so what" lines, timed to the board's clock | the command's board instructions | Available |
| `brief` | "build a brief", "slides for", "decision brief" | A PowerPoint brief from an intake for audience and the decision sought; one message per slide; every slide read by the visual reviewer | none | Planned |

## Training management

The platoon commander's week. Specified by `OFFICER ANALYSIS.md` Path B.

| Tool | Say | Does | Governed by | Status |
|---|---|---|---|---|
| `risk-assessment` | "RAW for this range", "risk assessment for" | The Risk Assessment Worksheet: hazards, initial RAC, controls, residual RAC, the approval level that follows from the RAC, the supervision plan; checker computes the RAC and names the approver | MCO 5100.29C Vol 2 (Risk Management) | Available |
| `safety-brief` | "safety brief for the 96", "liberty brief" | Liberty, holiday, and event safety briefs from the unit's format and the season's hazards | MCO 5100.29C Vols 3 and 5 | Available |
| `range-package` | "range package", "range order for" | Range request, range order or LOI, OIC and RSO duty checklist, the safety brief, tied to the RAW | MCO 3570.1 series and AR 385-63; the Range Safety Pocket Guide; the base range control SOP | Available |
| `training-schedule` | "build the training schedule from this list" | Week view from the T&R events the user names, with prep items, the RAW status, and the submission to higher | MCO 1553.3C (Unit Training Management); NAVMC 3500 series T&R manuals | Available |
| `after-action` | "turn these range notes into an AAR" | What happened, what worked, what to fix, in the unit's format; when the AAR is about a kit product, feeds LEARNINGS.md | none (unit SOP) | Available |

## Legal and property

The task with no training and a clock. Specified by `OFFICER ANALYSIS.md` Path C. These tools prepare documents to the format; they never advise on guilt, liability, or punishment, and every product goes to the SJA or the legal officer before it goes anywhere else.

| Tool | Say | Does | Governed by | Status |
|---|---|---|---|---|
| `investigation` | "I was appointed investigating officer", "preliminary inquiry into" | Appointment letter, the preliminary inquiry, and the command investigation report: preliminary statement, findings of fact each tied to an enclosure, opinions each tied to findings, recommendations each tied to opinions; the checker enforces the chain and the 30 day clock | JAGINST 5800.7G Chapter II; NJS JAGMAN Investigations Handbook (Oct 2024) | Available |
| `page-11` | "6105 for", "not recommended for promotion letter" | 6105 counseling entries and the not recommended letter with the unit diary deadline math | MCO 1900.16 w/Ch 3; MCO P1070.12K (IRAM); MCO P1400.32D w/Ch 2 | Available |
| `njp-package` | "prep the NJP package" | NAVMC 10132 fields, the rights the Marine must be read, the company grade limits; prepares, never advises | MCO 5800.16 Vol 14; MARADMIN 427/23 | Planned (the legal officer's domain; built only with an SJA reviewed exemplar) |
| `dd200` | "we lost gear", "DD 200 for" | The financial liability investigation of property loss on the same findings of fact engine as `investigation`; NAVMC 6 where it applies | MCO 4400.201 w/Ch 3; the TECOM DD 200 guide | Available |
| `inspection-prep` | "CGIP is coming", "self assess against the checklist" | Self assessment against the IGMC functional area checklist for a program, the corrective action plan, the program binder list | MCO 5040.6K; IGMC functional area checklists | Available |

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
| `study-guide` | "make a study guide", "walkthrough", "quiz me", "condense this handout", "whiteboard session" | Five formats from one spec (guide, interactive walkthrough, condensed handout, whiteboard session, quiz me); gates for coverage, answer traceability, and quiz rules before anything is built | the user's captured source | Available (0.2.0) |
| `walkthrough` | "build an interactive walkthrough" | Now a format of `study-guide` (0.13.0) | | Merged |
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
| `think` | "think this through", "what am I missing", "red team this", "check my thinking" | Four rules that survived being tested (evals/ab-test-2026-09-05): assume the product already failed and write the reasons before drafting, ask only what changes the product, say what you assumed and never claim the rest is covered, hand anything signed to the blind `red-team` agent. `precision_check.py` | Available |
| `red-team` (agent) | on any deliberate tier product | Blind adversarial pass: premortem with the failure asserted, expected but absent, adversarial read of every directive sentence, comparison against the standard and an exemplar; findings with evidence, never a score | Available |
| `build-a-skill` | "build a skill", "I do this every week", "new tool for" | Interview to a personal skill; or `new_tool.py` scaffolds a kit tool in the seven part shape with TODO markers and the checklist to finish it | Available |
| `share-method` | "make this shareable" | A method file with zero content a peer can run on their own material | Planned |
| `fleet-transition` | "I'm at my first unit" | Day one and week one at a new command; updates the rules file | Available |
| `folder-triage`, `inbox-triage`, `week-ahead` | "organize this folder", "triage my inbox", "week ahead" | Folder inventory and structure; inbox buckets with drafted replies; weekly brief | Available |
| `aar` | "capture that", "lesson learned", "it got downgraded" | Writes one lesson at a time to the user's own LEARNINGS.md in the fixed format; never edits a tool | Available |
| `debrief` | "debrief", "hotwash", "wrap up this chat" | End of chat sweep: every correction, rejection, and repeated instruction in the chat becomes a lesson with the user's words as evidence, sorted to the kit, this command's overrides, or the rules file; writes only what the user approves; lists every file the chat produced | Available |
| `inspect` | "apply what we learned", "review the lessons" | Applies approved lessons one at a time to Overrides/<tool>.md or Reference/Exemplars, or writes a proposal for the plugin; never edits the plugin | Available |
| `add-exemplar` | "this one got approved", "learn from this package" | Turns a product the user's command approved into a sanitized pattern in Reference/Exemplars/<tool>/ that the tool reads before its fictional exemplars; scrub checker | Available |

## Build order

1. Done: `start`, `library`, README, GETTING STARTED, this file; the Admin module core (`award`, `fitrep`, `rs-profile`) built from the governing manuals with mechanical checks and tests; the enlisted support tools (`letter-of-recommendation`, `letter-of-appreciation`, `meritorious-promotion`, `nomination`, `board-brief`, `counseling`) built to the seven part shape from annotated real packages, with fictional exemplars, intake, checkers, and evals; billet self reporting in `rules-file`.
2. Done (0.6.0): Path A, names removed by default (the label, `substitute.py`, the AI assistance line); the make it your own infrastructure (`Overrides/`, `Reference/Exemplars/`, `add-exemplar`, `aar`, `inspect`, the `new_tool.py` scaffold); the Training pack (`risk-assessment`, `after-action`, `training-schedule`, `safety-brief`, `range-package`); the Legal and property pack less NJP (`investigation`, `page-11`, `dd200`, `inspection-prep`). All built from the orders with fictional exemplars, because no real exemplars were available; every tool reads the user's own exemplars first when they exist.
3. Done (0.9.0), Path D, the rest of the core: `reenlistment`, `mrow-input`, `jepes-input`, `directive`, `board-prep`, `meritorious-mast`, `deocs-plan`, `endorsement`, `memo`. Each was built from its governing publication in the user's own library, quoted verbatim with paragraph numbers; where a publication is not on disk the tool says so in its opening paragraph, lists what that publication would settle, and leaves it unverified rather than filling it. Six of the nine carry such a gap. `evals/core_check.py` is the harness (36 cases). Build order inside the path was by how often a tool is actually run, not by how easy it was to source.
4. **Then (Path E):** pack selection from the rules file; the blind test in a fresh session; `share-method` and the marketplace question; `njp-package` once an SJA reviewed exemplar exists. **Blocking hooks are off the list.** A Cowork session's project root is the cloud container, not the user's connected folder, so a hook configured in their working folder is never read. The checkers stay steps the skills run, and they can be hooks only for Claude Code run locally against the working folder.
5. **After:** `order-analysis`, `tactical-planning`, `call-for-fire`; `quiz-builder` (the walkthrough is now a `study-guide` format); a workshop cut verified content free by script.
