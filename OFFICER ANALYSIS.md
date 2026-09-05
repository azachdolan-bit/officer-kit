# What a Marine officer does, and what the kit must become

An analysis of the work a company grade Marine officer is responsible for, function by function and MOS by MOS, measured against what the Officer Kit does today, with ranked paths forward. Written 4 September 2026 from the governing publications, the TBS MOS Assignment Handbook, HQMC messages, board member accounts, and published research on checklists and AI assisted writing. Every order number below was checked against marines.mil or an official copy, and the highest stakes numbers (risk decision levels, NJP limits, retention windows and tiers, citation format) were re read from the orders themselves on 5 September 2026; anything not confirmed is marked UNVERIFIED. Sources are listed at the end.

## Bottom line

1. The officer's job is about fifteen recurring functions, and the kit covers three of them well (correspondence, performance evaluation, awards and recognition) and one partly (counseling). The biggest uncovered functions by frequency and pain are training management (schedules, risk assessment worksheets, range packages, after action reports), investigations and discipline (preliminary inquiries, command investigations, 6105 entries, NJP packages), property accountability (CMR review, DD 200 investigations), and readiness input. Those four are also the most checkable, because each has a fixed format in an order.
2. Writing load is not evenly distributed by MOS. Manpower officers (0102, the billet formerly coded 0180), judge advocates, financial management and supply officers, and communication strategy officers write for a living. Ground combat lieutenants write fitreps on NCOs, counselings, training schedules, and risk assessments. Pilots inherit adjutant work as a ground job. The kit should ship one core and MOS packs, not one MOS's kit.
3. The policy environment sets a hard design constraint the kit does not yet meet. DoDI 5200.48 forbids conducting official business involving CUI on non DoD systems; NAVMC 5239.1 (December 2024) puts responsibility for what goes into a public AI system on the user and says distrust and verify every output; even GenAI.mil, the government's own platform, prohibits PII. A fitrep or award on a named Marine is PII, and once it is a record it is CUI. The kit must work on inputs with names removed by default and put the name back locally at render time. That is a change to every Admin tool.
4. The research on how boards read products and on how professionals use AI validates the seven part tool shape and sharpens it: structured intake beats freeform prompting by a wide margin, mechanical checkers catch what judgment misses, AI reviewers scoring holistically are biased and inconsistent, and people over rely on AI output unless the tool forces them to affirm each claim. The kit's checkers should become hooks that block, its reviewers should score named dimensions pairwise against an exemplar, and every export should carry an AI assistance label.
5. Three things in the shipped kit are wrong or stale and get fixed with this analysis: the citation format (the 2019 awards manual and every current subordinate instruction say 8 lines, 1,250 characters, Times New Roman 10; the kit enforced the 2001 order's 9 lines and 1,200), the enlisted promotion manual citation (MCO P1400.32D w/Ch 2 is current, there is no 1400.32E), and the adjutant MOS (0180 became 0102 in 2014).

## Method, and what the research changed

Three parallel research passes: the officer MOS landscape and first tour billets; the functions every officer performs regardless of MOS with the current governing publication for each; and existing tools, board reading habits, the AI policy environment, and design research. Findings were cross checked against the three orders on disk (MCO 1610.7B, MCO 1650.19J, MCO 1500.61) and the private exemplar set.

What changed because of it: the citation checker limits (above); the decision to build the kit around names removed inputs; the decision to add an AI assistance label to every rendered product; the plan to convert checkers into blocking hooks; the reviewer design (pairwise against an exemplar, not a score); the addition of training management and investigations to the front of the build order, ahead of the teaching tools; and the MOS pack structure. Without the research the next build would have been quiz builder and study guide.

## Part 1. The functions, and what a tool for each needs

Each function below lists the governing publication, what the officer specifically owns, the products, and what the kit has. Frequency is the author's estimate for a platoon commander or company XO in a ground unit and is labeled as such; no official workload survey exists.

### 1. Correspondence and directives

Governed by SECNAV M-5216.5 (June 2015, Ch 1 May 2018), MCO 5216.20B w/Admin Ch 4 (September 2025, the Marine Corps supplement), and MCO 5215.1K w/Admin Ch 3 (September 2025, directives). The officer drafts, routes, and signs or chops standard letters, endorsements, memoranda, and memoranda for the record, and writes unit orders and SOPs in the directive format (situation, mission, execution, administration and logistics, command and signal). Weekly for anyone on a staff.

Kit today: `naval-letter` with a measured renderer and QC. Missing: endorsements (first through nth), memorandum and MFR formats, the directive format for a unit order or SOP, point and information papers (MCTP 3-30A). All four are format bound and checkable by the same measuring approach.

### 2. Performance evaluation

MCO 1610.7B (5 June 2023). The RS establishes Section B within 30 days, counsels, ensures the MRO starts an MROW in A-PES, writes Sections A through I and J-1, and manages a profile; the RO writes Section K on potential. Normal reports due to HQMC within 30 days of the period end, 60 for adverse. Lieutenants receive semiannual reports. JEPES (MCO 1616.1, November 2020) covers Pvt through Cpl on semiannual periods ending 31 January and 31 July, with the officer as Evaluator or Reviewer validating command input marks.

How boards read them, from board members' own accounts: about twenty minutes per record, a one minute brief, and most of the time spent on fitreps; members look at RS and RO relative values first and weigh marks over Section I; comments must match the marks, and forgettable performance gets forgettable comments, never negative ones; promotion language runs a continuum from "an absolute must" to "promote with peers," and the bottom of that continuum signals the Marine is not competitive. CNA's 2024 analysis found relative values in small profiles are statistically indistinguishable from noise, which is a caution the `rs-profile` tool should state to a new RS.

Kit today: `fitrep` and `rs-profile`, built from the manual's verbatim text. Missing: the MROW input tool for the officer's own report (every lieutenant twice a year); JEPES command input; the promotion language tier as an explicit intake field with the comment checked against it; a fitrep tracker for due dates; the RS profile caution above. The fitrep exemplar is on hold at Zach's direction.

### 3. Awards and recognition

SECNAV M-1650.1 (16 August 2019) for criteria and the combination citation and certificate format; MCO 1650.19J (2001, Ch 1 2012) for Marine Corps processing, the Summary of Action, and the Certificate of Commendation, Meritorious Mast (NAVMC 10935), and Letter of Appreciation, which since 2022 also route through iAPS. The order demands "definitive terms rather than broad generalized statements." The current citation format per the 2019 manual as carried in three subordinate instructions (HQBN TECOM personal awards guide; USNAINST 1650.5D, May 2020; CNLSCINST 1650.2B, October 2024): all capitals, landscape, Times New Roman 10, fully justified, one inch margins, 8 lines, 1,250 characters, no acronyms.

Kit today: `award` at the full seven part shape, `letter-of-appreciation`. Fixed with this analysis: the checker now enforces 8 lines and 1,250 characters. Missing: Meritorious Mast and Certificate of Commendation as the lightest recognition, the unit award input, and the end of tour award decision (the order says routine end of tour recommendations have no place; the tool already flags it).

### 4. Enlisted promotion, retention, and recognition

MCO P1400.32D w/Ch 2 (2012) is the current enlisted promotion manual; the commander's recommendation is the first requirement, and a "not recommended" entry goes in the unit diary by the 15th of the month prior with a Page 11 entry. MARADMIN 667/22 sets meritorious promotion quota rules. MCO 1040.31 (2010) governs retention: the CO may delegate career planning interviews in writing but "must conduct an interview when the Marine is not recommended for reenlistment"; windows are 26 to 24 months before ECC for the initial interview, 14 to 12 months for the first term and for careerists, 8 to 6 months before EAS; the four recommendation tiers are defined by population, recommended with enthusiasm for the top 25 percent of Marines in the grade, with confidence for the top 50 percent, with reservation (reason required), and not recommended (reason required). That definition is a fact the reenlistment tool must put in front of the CO, because a "with enthusiasm" on a Marine outside the top quarter is a false statement in a record (verified against the order, 5 September 2026). Marine of the Quarter and similar boards run on local orders.

Kit today: `meritorious-promotion`, `nomination`, `board-brief`, `letter-of-recommendation`. Missing: the "not recommended for promotion" letter with its Page 11 and the deadline math; the reenlistment recommendation and endorsement with the category language; the career planning interview record; the enlisted program package (MECEP, recruiting, drill instructor screening) to the program's MARADMIN.

### 5. Leader development and counseling

MCO 1500.61 (2017): six functional areas (fidelity, fighter, fitness, family, finances, future); the initial RS to MRO counseling is required by the PES order; proficiency and conduct counseling at regular intervals is prescribed by NAVMC 2795, whose MCPEL status is UNVERIFIED though the PDF is still hosted.

Kit today: `counseling`. Missing: the leader development plan across the six areas as a running document, and the counseling calendar tied to JEPES and fitrep dates.

### 6. Legal, discipline, and investigations

JAGINST 5800.7G, the Manual of the Judge Advocate General (effective January 2021), Chapter II for administrative investigations; the Naval Justice School JAGMAN Investigations Handbook (October 2024) gives the working format: a preliminary inquiry has no fixed format and takes about three working days; a command investigation is appointed in writing, normally due in 30 days, and reports as a preliminary statement, findings of fact, opinions, recommendations, and enclosures with the convening order first. MCO 5800.16, the Legal Support and Administration Manual (2021, 17 volumes): Volume 14 (18 May 2021) for enlisted NJP (paragraph 010303: a company grade commander may impose not more than 7 consecutive days correctional custody, 7 days' pay forfeiture, 14 consecutive days extra duties, 14 consecutive days restriction; field grade 30, half a month's pay for two months, 45, and 60; verified 5 September 2026), Volume 15 for officer misconduct. MARADMIN 427/23 moved the Unit Punishment Book instructions onto NAVMC 10132 itself. MCO 1900.16 w/Ch 3 (May 2025) for 6105 counseling entries and separations. MCO P1070.12K for Page 11 entries.

This is the function where a lieutenant is most likely to be handed a task with no training and a fixed format, and where a badly written product has legal consequences. Every officer will be an investigating officer.

Kit today: nothing. This is the largest gap.

### 7. Training management

MCO 1553.3C, Unit Training Management (August 2023): the METL is validated annually, within 45 days of assuming command, or 15 days after a new mission, and published in MCTIMS; required products are the commander's training guidance, the training plan, and training schedules submitted to higher; MCTIMS records T&R events, rosters, and risk assessments. MCO 1500.63A (April 2026) lists annual common military training. MCO 5100.29C Volume 2 (2020) is risk management: five steps (identify hazards, assess hazards, make risk decisions, implement controls, supervise); high risk training events "should use a risk assessment worksheet" carrying an emergency action plan, cease training procedures, a communications plan, and a pre execution checklist; the order's example decision matrix puts RAC 4 with company grade officers and RAC 5 with SNCOs and first line supervisors, with RAC 1 to 3 at the O-5 and O-6 level; all high risk training "should be approved in writing by the first O-5 Commander" in the training unit's chain (verified against the order's text, 5 September 2026). MCO 3570.1 series and AR 385-63 govern range safety, with the Range Safety Pocket Guide (February 2024) summarizing OIC and RSO duties. MCO 6100.13A and MCO 6110.3A (both May 2025) for PFT, CFT, and body composition administration.

Products: training schedule, RAW, range request and range order or LOI, safety brief, high risk training approval letter, after action report, T&R completion rosters, PFT and CFT and BCP rosters and assignment letters.

Kit today: nothing shipped (`training-schedule`, `after-action` planned). For a platoon commander this is the weekly load. The RAW is the single most checkable product in the Marine Corps: five steps, a fixed matrix, an approval level that follows from the RAC.

### 8. Readiness reporting

MCO 3000.13B (July 2020) and the DRRS-MC Commander's Readiness Handbook (September 2020). DRRS-MC runs on SIPR. Company grade officers feed personnel, equipment, supply, and training data into the battalion's monthly report. Nothing readiness related touches the kit. The kit's security card should say so explicitly.

### 9. Planning and operations

MCWP 5-10 w/Ch 1 (August 2020), the Marine Corps Planning Process, with orders formats in the appendices; MCTP 3-30A (July 2020) for staff action; MCRP 3-10A.2 (July 2024) for infantry company operations. The five paragraph order is carried in MCWP 5-10 and TBS handouts; "MCRP 5-10.1" as an orders pub was not found. Tactical decision games have no order behind them.

Kit today: `order-critique`. Planned: `order-analysis`, `tactical-planning`, `call-for-fire`. These are judgment tools with fewer mechanical checks, which is why they were specified second.

### 10. Supply, property, and maintenance

MCO 4400.150 (2014) consumer level supply; MCO 4400.201 w/Ch 3 (May 2025, 17 volumes) for property, including responsible officer and CMR duties and financial liability investigations (the specific volume is UNVERIFIED); DD 200 and NAVMC 6 are the forms, with a TECOM how to guide; MCO 4790.2 (2016) for maintenance management. The officer signs for the CMR, runs inventories, and initiates or investigates a DD 200 when gear is lost.

Products: RO acceptance, CMR review and inventory certification, sub custody records, DD 200 initiation and the investigating officer's findings, NAVMC 6, missing gear statements.

Kit today: nothing. The DD 200 investigation shares the JAGMAN findings of fact shape and can share a tool.

### 11. Safety and mishap reporting

MCO 5100.29C, Volumes 1 through 9 (2020 to 2021): Volume 3 traffic and motorcycle programs, Volume 9 mishap investigation and reporting. Safety Division's flowchart: OPREP-3 within one hour, an 8 Day Brief to the ACMC for Class A and B mishaps and non combat fatalities, SIREP within 30 days.

Products: ORM worksheet for every event (the RAW again), liberty and holiday safety briefs, motorcycle rider roster and mentorship input, mishap notifications, 8 Day Brief slides.

Kit today: nothing. The safety brief and the RAW belong with training management.

### 12. Personnel administration

MCO 1050.3J (leave and liberty, 2009), MCO 1754.9B (unit, personal, and family readiness, 2019), MCO 1752.5C (SAPR, 2019), MCO 5354.1G (prohibited activities and conduct, May 2024, replacing 5354.1F), MARADMIN 306/25 (annual DEOCS 1 August to 30 November for O-5 and O-6 commands over 50 personnel). Unit diary and MCTFS governed by the PRIM (UNVERIFIED). Products: leave approvals, special liberty requests, unit diary source documents, the commander's family readiness statement, incident reports, DEOCS action plans, check in and check out sheets.

Kit today: `inbox-triage`, `week-ahead`. Missing: the DEOCS action plan writer (annual, every O-5 command, every company feeds it) and the incident report shapes. SAPR and PAC reporting carry content the kit's privacy rules exclude; the tool for those is a checklist of what must be reported to whom by when, never the narrative.

### 13. Inspections

MCO 5040.6K (May 2026), the IGMC inspections program, with published functional area checklists (military awards, career planning, leave and liberty, safety management, SAPR, consumer level supply, and more). Products: self assessment against the checklist, corrective action plan, program binder, appointment letters.

Kit today: nothing. A functional area checklist is a checklist; the tool is the self assessment with the corrective action plan. Cheap to build, high value before a CGIP.

### 14. Financial

MCO 4600.40C (January 2026) for the government travel card; MCO 4650.39 (2011) for DTS, with approving officials appointed by DD 577. Products: DTS authorizations and vouchers, AO approvals, GTCC delinquency counseling, purchase requests, training budget input.

Kit today: nothing. DTS is a government system; the kit's value is the delinquency counseling (a `counseling` variant) and the budget input.

### 15. The officer's own career

MCO 1553.4B (2008) for PME; ALMAR 024/25 for the FY26 reading list (five titles a year encouraged); MCO 1200.18 and NAVMC 1200.1L (March 2025; 1200.1M replaces it 1 October 2026) for MOS requirements. Career designation panels (FY26 CDP-1 was MARADMIN 620/25; eligibility requires 540 days designated in the PMOS). Captain is by the All Fully Qualified Officers List, not a board. The major board reviews the OMPF and Master Brief Sheet; letters to the board are due 10 days prior; officers are responsible for auditing their own OMPF and MBS through O-RMA. Talent Management 2030 allows a one time promotion opt out without penalty and opt outs from PME and recruiting station commander boards.

Products: own MROW input, OMPF and MBS audit, PME plan, reading log, MOS roadmap self assessment, letter to the board.

Kit today: `fleet-transition`, `rules-file`. Missing: the MROW input tool (twice a year for every lieutenant), the board preparation checklist with the OMPF audit and the letter to the board, the reading log.

## Part 2. The MOS lens

The TBS Marine Officer MOS Assignment Handbook (2019 edition; a 2024 edition exists but could not be retrieved) is the official description of first tour billets. The pattern that matters for the kit:

| Family | First tour billet | What they write most | Kit pack |
|---|---|---|---|
| 0302, 0802, 1302, 0203 | Platoon commander, FO or FDO, company XO; platoons of roughly 45 | Fitreps on NCOs, counselings, training schedules, RAWs, range packages, AARs, awards | Core plus Training pack |
| 0102 Manpower (adjutant; 0180 was renumbered 0102 by MARADMIN 497/14) | Adjutant at an O-5 command, 400 to 1,200 personnel, plus legal officer, casualty assistance, postal, voting, historian | Correspondence, directives, strength reports, awards processing, DTS, legal packages | Core plus Admin pack in full, plus Legal |
| 0402, 3002, 3404 | S-4, MMO, MTO, supply OIC and fiscal officer, budget officer | Property records, CMR, inventories, budget estimates, execution reviews, maintenance reports | Core plus Property and Fiscal pack |
| 0602, 1702 | S-6, network operations | Comm plans, SOPs, readiness input | Core plus Planning pack |
| 5803 | PMO watch commander (LE battalions divested) | Incident reports, investigations | Core plus Legal pack |
| 4402 | Trial and defense counsel, SJA staff | Legal opinions, reviews of investigations | Their own tools; out of scope |
| 4502 | Media relations, plans, community relations | Press products | Out of scope for now |
| 6002, 6602 | MALS division OIC, MMCO | Maintenance flow, requisitions, financial management | Core plus Property pack |
| 72xx, 7315, 7318 | Section leader, platoon commander, control quals | Same as ground | Core plus Training pack |
| 75xx pilots | Aircraft commander syllabus plus a ground job (schedule writer, S-1, S-4A), SDO and ODO | Whatever the ground job is; often adjutant work without a 0102 | Core plus whichever pack the ground job needs |

Three implications. First, the core is the same for everyone: rules file, correspondence, fitrep, awards, counseling, the officer's own career. Second, packs are chosen by billet, not MOS, because a pilot in the S-1 needs the Admin pack and a 0402 platoon commander needs the Training pack; the rules file's billet description and module yes list already capture this and should drive pack selection. Third, force design has moved billets: tank battalions are gone (the 1802 platoon billet in the 2019 handbook no longer exists), cannon batteries went from 21 to 5, law enforcement battalions and bridge companies were eliminated, infantry battalions were resized to 811, and Marine Littoral Regiments (3d MLR at IOC December 2023, 12th MLR projected 2026) created new billets. The kit should never hard code a unit type.

## Part 3. The policy constraint

The stack, in order of authority:

1. DoDI 5200.48 paragraph 3.10.b: DoD personnel will not use non DoD information systems to conduct official business involving CUI.
2. DON CIO memo (September 2023): commercial large language models not recommended for operational use until security controls are investigated; outputs must be complemented by human expertise.
3. NAVMC 5239.1 (4 December 2024, announced by MARADMIN 056/25): users are responsible for what they input into publicly accessible generative AI systems and must adhere to existing legal, cybersecurity, OPSEC, and classification policy; users should distrust and verify all outputs; commands are discouraged from banning generative AI.
4. GenAI.mil (launched December 2025; DON transition mandated by April 2026): certified for CUI at IL5, and PII and PHI are prohibited on it. MARADMIN 214/26 makes a basic AI course mandatory by 31 December 2026 and notes GenAI.mil requires a CAC computer while permitting commercial tools for practice on personal devices.
5. Army CIO guidance (June 2024), not binding on Marines but the clearest practice statement: label any document created in whole or part with generative AI output.

What this means for a kit that runs on commercial Claude on a personal device: doctrine, formats, standards, and the user's own writing are fine; a draft that carries another Marine's name, EDIPI, marks, disciplinary facts, or a unit's readiness figures is not. The kit already keeps identifiers out of saved files and scans for blocked content. It does not yet keep the Marine's name out of the prompt, and every Admin tool asks for it.

The design that satisfies the constraint without making the tools useless: a label in place of the name throughout the session (`<MARINE>`, or a working label the user picks, like "the Sgt"), with grade and billet kept because they are needed for the criteria; a local substitution step at render time (a script that replaces the label in the finished docx or text with the name typed at that moment and never stored); a reminder printed by every Admin tool's first step; an AI assistance line on every rendered product, small and in the file properties, so the signer knows and the practice matches the Army's guidance. The reader should understand that this is a mitigation, not a permission; the officer decides what to put into a personal tool, and the kit's job is to make the safe way the easy way.

## Part 4. What the research says about how to build the tools

The seven part shape (standard, exemplars, intake, quantification ladder, voice, checks, learning hook) held up. Five findings sharpen it.

Structured intake beats freeform prompting. A 2026 comparison across three frontier models scored checklist structured prompts 7.5 of 8 against 5.67 for raw prompts, in one turn and with fewer tokens; clarifying question prompts scored between them and took two turns. The kit's intakes are already ordered questions; they should become schemas with required numeric fields so a draft cannot start on an empty fact list.

Mechanical checks catch what judgment misses. The WHO surgical checklist cut complications from 11 to 7 percent and deaths from 1.5 to 0.8 percent across 7,688 patients; Boorman's design rules are five to nine items, defined pause points, the items experts forget, one page, tested in real conditions. Anthropic's skill guidance says the same operationally: run the validator, fix, repeat; scripts solve rather than defer. The kit's checkers exist; the next step is wiring them as hooks that block a save until they pass, so the model cannot skip them. That is a Cowork hooks question (the plugin ships none yet) and one of the five untested unknowns.

AI reviewers scoring holistically are biased. The 2024 survey of LLM as judge documents position, verbosity, self preference, and authority biases and inconsistent inter rater reliability; position consistency ranges from 0.23 to 0.89 across models, and swapping order detects but does not fix it. Mitigations: dimension specific rubrics, pairwise comparison over absolute scores, decomposition, reference answers, human oversight. The kit's four blind reviewers should compare the draft to a stored exemplar on named dimensions (does every sentence carry a number; does the citation carry a fact the SOA does not) and never emit a score.

People over rely on AI output. A review of 74 studies found automation bias produces errors of omission and commission, worse under workload and time pressure, and mitigated by accountability, displayed confidence, and presenting information rather than recommendations. Cognitive forcing (making the person do something before accepting) reduces over reliance more than explanations do, and people rate those designs lowest. The kit's read back fact list is the right instinct; the export step should require the user to affirm or edit each flagged claim, and the tools should say when they are unsure rather than smooth over it.

Workflows with gates beat autonomous agents. Anthropic's own guidance prefers programmatic gates, uses evaluator loops only where criteria are clear, and puts human feedback at checkpoints; multi agent runs cost about fifteen times the tokens and each subagent needs an objective, an output format, sources, and boundaries. The kit's reviewers are already single purpose and blind; they should stay that way, and the kit should not grow an orchestrating agent.

## Part 5. Corrections to the kit from this analysis

1. Citation format: 8 lines, 1,250 characters, Times New Roman 10, fully justified, one inch margins, no acronyms, per SECNAV M-1650.1 (2019) as carried by HQBN TECOM's guide, USNAINST 1650.5D (2020), and CNLSCINST 1650.2B (2024). The kit enforced MCO 1650.19J's 2001 numbers (9 lines, 1,200). Fixed in `citation_check.py` and the award references with this commit. Read the table from the user's copy of the manual when it is on disk; the kit's numbers are the observed current practice.
2. MCO 1400.32: the current enlisted promotion manual is MCO P1400.32D w/Ch 2 (2012). MODULES.md updated.
3. Adjutant: MOS 0180 was renumbered 0102 (Manpower Officer) by MARADMIN 497/14. Any billet map uses 0102.
4. MCO 1553.3 is now 1553.3C, Unit Training Management, not Systems Approach to Training. MODULES.md updated.
5. MCO 5354.1F is superseded by 5354.1G (May 2024).
6. `rs-profile` should tell a new RS that relative values from a small profile are noise (CNA 2024) and that boards look at the RV first (board member accounts); the tool's arithmetic is right, the framing needs the caution.
7. The kit's security card should name DRRS-MC and anything on SIPR as out of scope, and should quote NAVMC 5239.1's "distrust and verify" line, because that is the Marine Corps' own instruction and it matches the kit's design.

## Part 6. The gaps, ranked

Ranked by frequency for a company grade officer, the pain of getting it wrong, and how mechanically checkable the product is (the author's judgment, stated as such). High on all three is where the kit earns its keep.

| Rank | Gap | Frequency | Pain if wrong | Checkable | Note |
|---|---|---|---|---|---|
| 1 | Risk Assessment Worksheet and safety brief | weekly | high (people get hurt; the approval level is in the order) | very | five steps, fixed matrix, RAC drives approval; MCO 5100.29C Vol 2 |
| 2 | Command investigation and preliminary inquiry | a few a year, no warning | very high (legal) | high | fixed report shape from the NJS handbook; 30 day clock |
| 3 | Training schedule and range package | weekly | medium | high | MCO 1553.3C products; range order or LOI; OIC and RSO duties |
| 4 | After action report | after every event | medium | medium | no order; unit format; the learning hook feeds it |
| 5 | Endorsement, memorandum, MFR, directive format | weekly for staff | medium | very | same measuring approach as naval-letter |
| 6 | Own MROW input | twice a year for lieutenants | high (own record) | medium | reads the rules file billet; Section C style |
| 7 | 6105 entry, not recommended letter, NJP package | monthly at company level | very high | high | LSAM Vol 14, MCO 1900.16, NAVMC 10132; fixed language |
| 8 | DD 200 and CMR inventory | quarterly, on turnover | high (financial liability) | high | shares the findings of fact shape with investigations |
| 9 | Reenlistment recommendation and career planning interview | monthly | medium | high | MCO 1040.31 categories and windows |
| 10 | JEPES command input and counseling calendar | semiannual | medium | high | MCO 1616.1 dates |
| 11 | Inspection self assessment and corrective action plan | annual | medium | very | IGMC checklists are public |
| 12 | DEOCS action plan | annual | medium | medium | MARADMIN 306/25 |
| 13 | Board preparation: OMPF audit, letter to the board, PME plan | per board | high (own career) | high | MARADMIN 622/25 mechanics |
| 14 | Enlisted program package (MECEP, DI, recruiting) | a few a year | medium | medium | program MARADMIN sets content |
| 15 | Meritorious Mast and Certificate of Commendation | monthly | low | very | NAVMC 10935; lighter than award |
| 16 | Order analysis, tactical planning, call for fire | per exercise | medium | low | judgment tools; specified, not built |
| 17 | Quiz builder, study guide, walkthrough | school and PME | low in the fleet | medium | valuable at TBS and EWS, less after |

## Part 7. Paths forward

Five paths, not mutually exclusive. Each is sized in sessions (one session is a working evening of the build and sync pattern that produced 0.5.0). The recommended sequence is at the end.

### Path A. Make the kit safe to use as built (names removed by default)

Add the label substitution to every Admin tool: a `<MARINE>` label through the session, a `substitute.py` that puts the name into the rendered product locally and never writes it to disk, the reminder line in every tool's first step, the AI assistance line in every rendered product's properties, and the security card update naming DRRS-MC and quoting NAVMC 5239.1. One session. This comes first because everything else adds tools that handle other Marines' records, and the constraint applies to all of them.

### Path B. The Training pack (the platoon commander's week)

`risk-assessment` (the RAW to MCO 5100.29C Vol 2 with the RAC computed and the approval level stated), `safety-brief`, `training-schedule` (MCO 1553.3C products, tied to the T&R events the user names), `range-package` (range request, range order or LOI, OIC and RSO duties from the pocket guide), `after-action` (with the learning hook writing to LEARNINGS.md when the AAR is about a kit product). Governing pubs to add to the library: MCO 5100.29C Vol 2, MCO 1553.3C, MCO 3570.1 series, the Range Safety Pocket Guide. Three sessions. Highest weekly value for the largest population of lieutenants.

### Path C. The Legal and Property pack (the task with no training and a clock)

`investigation` (preliminary inquiry and command investigation to the NJS handbook: appointment letter, preliminary statement, findings of fact each tied to an enclosure, opinions each tied to findings, recommendations each tied to opinions, the 30 day clock; the checker enforces the chain), `page-11` (6105 entries and the not recommended letter with the deadline math, to MCO 1900.16 and P1400.32D), `njp-package` (NAVMC 10132 fields and the company grade limits from LSAM Vol 14; the tool prepares, never advises on guilt), `dd200` (the financial liability investigation sharing the findings of fact engine). Pubs: JAGMAN Chapter II, the NJS handbook, LSAM Vols 14 and 15, MCO 1900.16, MCO 4400.201 (the volume for accountability, to be identified), the TECOM DD 200 guide. Three sessions. Highest pain reduction; every officer gets handed one of these.

### Path D. Finish the core (the officer's own record and the rest of correspondence)

`mrow-input` (the officer's own fitrep input, reading the rules file billet, Section C style, checked with `fitrep_check.py`), `board-prep` (OMPF audit checklist, letter to the board, PME plan, reading log, from MARADMIN 622/25 and MCO 1553.4B), `endorsement`, `memo` and MFR, `directive` (unit order and SOP format from MCO 5215.1K), `reenlistment` (MCO 1040.31 categories with their population definitions, windows, and the CO's personal interview rule), `jepes-input`, `meritorious-mast` and `certificate-of-commendation`. Three sessions. Makes the core complete for every MOS.

### Path E. The self improving loop and distribution

`aar` and `inspect` (the lessons queue into approved skill changes with evals), hooks that block on checker failure (tests unknown 2), the MOS and billet pack selection driven by the rules file, the blind test in a fresh session, the marketplace question (unknown 5), and a way for a peer to contribute a command's local order and exemplar patterns without contributing content. Two sessions. This is what makes the kit "self improving" in fact rather than in name, and what makes it something other officers can install.

### Recommended sequence

A first, because it changes every tool and is a session. Then B and C in parallel across sessions, because they are independent and together cover the two things a new lieutenant is handed most often (a range and an investigation). Then D. Then E, with the blind test before any distribution. The teaching tools (quiz builder, study guide v0.2, walkthrough) move after E; they are valuable at TBS and EWS and less in the fleet, and the kit is for the fleet.

Estimated total: twelve sessions to a kit that covers all fifteen functions for the core and the two heaviest packs, with the safety constraint met.

## Part 8. What to collect before the next build

The research reached the orders. The exemplars are what make a tool good, and those come from officers. Before Paths B and C:

1. Two or three real Risk Assessment Worksheets, approved, from any unit, with the names removed. The pattern of what a battalion actually accepts as a control is not in the order.
2. One command investigation and one preliminary inquiry, sanitized, from someone who wrote one. The NJS handbook gives the shape; the exemplar gives the voice of findings of fact that survived review.
3. A battalion's range order or LOI and the range control checklist for one base.
4. A DD 200 package that closed.
5. The local meritorious promotion and recognition orders for one Wing and one Division, so the category mapping is tested against two real rubrics.
6. Three officers in different MOSs (a 0102, a 0402 or 3002, and a pilot with a ground job) walked through the rules file, so the billet description and module yes list are tested on people who are not the author.
7. SECNAV M-1650.1 on disk. Every awards tool cites it and reads it partially from the web.

## Sources

Official publications and messages: NAVMC 1200.1L and 1200.1M, MOS Manual (marines.mil MCPEL); MARADMIN 167/25, 122/26 (MOS manual implementation); MARADMIN 497/14 (0180 to 0102); MCO 1610.7B (on disk); MCO 1616.1 JEPES; SECNAV M-1650.1 (2019) and MCO 1650.19J (on disk); MARADMIN 042/08 and 024/22 (iAPS); MCO P1400.32D w/Ch 2; MARADMIN 667/22; MCO 1040.31; MCO 1500.61 (on disk); JAGINST 5800.7G and MARADMIN 152/21; NJS JAGMAN Investigations Handbook (October 2024); MCO 5800.16 Vols 14 and 15; MARADMIN 427/23; MCO 1900.16 w/Ch 3; MCO P1070.12K; MCO 1553.3C; MCO 1500.63A; MCO 3570.1 series and the Range Safety Pocket Guide (February 2024); MCO 5100.29C Vols 1 through 9; MCO 6100.13A; MCO 6110.3A; MCO 3000.13B and the DRRS-MC Commander's Readiness Handbook (2020); MCWP 5-10 w/Ch 1; MCTP 3-30A; MCRP 3-10A.2; MCO 4400.150; MCO 4400.201 w/Ch 3; MCO 4790.2; TECOM DD 200 guide; MCO 1050.3J; MCO 1754.9B; MCO 1752.5C; MCO 5354.1G and MARADMIN 261/24; MARADMIN 306/25; MCO 5040.6K and the IGMC checklists; MCO 4600.40C; MCO 4650.39; MCO 1553.4B; ALMAR 024/25; MCO 1200.18; MARADMIN 620/25 (career designation); MARADMIN 108/25 and 622/25 (officer boards); MARADMIN 158/26 (blended seminar); Talent Management 2030 (November 2021) and updates (March 2023, December 2024); Force Design 2030 Annual Update (June 2023); CRS R47614 (November 2025); MARADMIN 599/20 (UAS MOSs); SECNAV M-5216.5; MCO 5216.20B; MCO 5215.1K; the TBS Marine Officer MOS Assignment Handbook (2019).

AI policy: DoDI 5200.48; DON CIO memo (September 2023, via Federal News Network); NAVMC 5239.1 (December 2024) and MARADMIN 056/25; MARADMIN 496/24 (NIPRGPT and CamoGPT); MARADMIN 214/26 (basic AI course); GenAI.mil launch coverage (DefenseScoop, Lawfare, December 2025) and the DON designation (ExecutiveGov, January 2026); Army CIO generative AI guidance (June 2024).

Citation format: HQBN TECOM Personal Awards guide; USNAINST 1650.5D (May 2020); CNLSCINST 1650.2B (October 2024).

Board reading: Heuer, "The Marine Corps Promotion Board Process," Marine Corps Gazette (December 2020); Miner, "Improving Selection Boards," Gazette (July 2021); TBS W3G0001XQ and B3K3738 fitness report handouts; CNA, "Stop Using Relative Values" (January 2024); Holmes, Proceedings (August 2025); Kreckman, Task and Purpose (2021) on award inflation; NavyWriter (community).

Design research: arXiv 2605.20149 (structured prompts, 2026); Haynes et al., WHO surgical checklist (2009, via Harvard Gazette); Gawande, The Checklist Manifesto, chapter 6 (Boorman's rules); arXiv 2411.15594 (LLM as judge survey, 2024) and 2406.07791 (position bias); Goddard et al., JAMIA (automation bias review); Buçinca et al., arXiv 2102.09692 (cognitive forcing); Anthropic, Building Effective Agents, Multi Agent Research System, Effective Context Engineering, Skill Authoring Best Practices, Claude Code Hooks guide.
