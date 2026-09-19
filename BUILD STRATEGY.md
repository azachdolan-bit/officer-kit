# Build strategy: how a tool earns its place in the kit

Written 4 Sep 2026 after the Admin module core shipped. This is the method for building every remaining tool, and for rebuilding the ones that exist, so that each one carries the critical thinking a good officer brings to the task rather than just a format.

## The first rule of every build

Read the order from the user's library before anything else: `library/scripts/find_order.py <number>` finds it, extracts it, or renders a figure page. The web is for publications the script reports as not on disk, and the standard file says which those were. This rule exists because two tools shipped with web copies and a caution while the full orders sat in the library.

## 1. Where the kit stands

Version 0.4.0, five commits, private repo `azachdolan-bit/officer-kit`, clone on Zach's machine, installable plugin file built. Not yet installed by anyone.

| Module | Available now | What each does | Built from |
|---|---|---|---|
| Correspondence | `naval-letter` | Letter from a JSON spec on the exact line grid; identity from the rules file; Gate 2 measures the rendered PDF; refuses placeholders | the school correspondence handout over SECNAV M-5216.5; 3 evals pass |
| Admin | `award`, `fitrep`, `rs-profile` | SOA and citation to the order's length and format rules; Sections B, C, I to the PES manual with the unacceptable list enforced; a private profile ledger with relative value | MCO 1650.19J, MCO 1610.7B, verbatim extracts; 6 evals pass |
| Planning | `order-critique` | Five paragraph order completeness review (the generic v0.1) | school handouts |
| Training and teaching | `capture-source`, `study-guide` (v0.1) | Complete capture with a read back gate for photos; guide, quiz, flashcards | none |
| Verify | `qc-gates` + 5 agents | Significance, evidence, visual, source fidelity reviewers, all blind; the gate stack by product type | the correspondence QC standard |
| Share and improve | `start`, `library`, `rules-file`, `security-check`, `build-a-skill`, `fleet-transition`, `folder-triage`, `inbox-triage`, `week-ahead` | First run from zero; three ways to build a library; the rules file at three depths, every question optional | the workshop kit plus new work |

Docs: README (what you are installing), GETTING STARTED (for someone who has never opened Cowork), MODULES (every tool, status, governing pub), CHANGELOG, LEARNINGS queue (eight seeded lessons).

What is honest about the current state: the tools enforce the standard well and think shallowly. `award` knows the format and the length limits and asks whether the facts justify the level; it does not yet know what a strong NAM summary looks like next to a weak one, how a particular approval authority likes them written, or how to turn "did a good job on the range" into a quantified achievement. That gap is what this strategy closes.

## 2. What a tool that thinks looks like

Every product an officer signs goes through the same unspoken process: know the standard, know what good looks like, ask the questions that surface the facts, quantify, write in the reader's voice, check it, and learn from what came back. A tool that only does the first of those is a template. The kit's tools will carry all seven, as parts of the skill folder:

| Part | What it is | Where it lives | Example for `award` |
|---|---|---|---|
| **Standard** | The governing publication, verbatim extract, cited by paragraph | `references/<pub>-extract.md` | MCO 1650.19J SOA and citation rules; SECNAV M-1650.1 criteria and standard sentences |
| **Exemplars** | Three to six finished products annotated line by line for why they work, plus one weak one annotated for why it fails | `references/exemplars.md` (fictional, scrubbed) and the user's own `Exemplars/` folder (real, private) | a NAM SOA that quantifies scope and result in every bullet; a NAVCOM citation that states the achievement in the first sentence; a weak one that lists duties instead of results |
| **Intake** | The questions the tool asks before it drafts, in the order a good mentor would ask them, with what each answer unlocks | `references/intake.md` | Who approves this? What was the single hardest thing this Marine did? What would have happened without them? What can you count? Who else saw it? |
| **Quantification** | The "so what" ladder: action, scope, result, impact, comparison; prompts that turn vague notes into numbers the recommender can defend | inside `intake.md` and the SKILL body | "raised platoon rifle qualification from 78 to 96 percent, the highest in the battalion for the cycle" |
| **Voice** | The verbs and phrasing the genre expects, the words it forbids, and the reader profile (how this boss, board, or approval authority reads) | `references/voice.md` plus the user's rules file "How my boss wants things" and a per reader style note | strong verbs for citations; no "assisted," no "helped with"; this CO wants the result before the action |
| **Checks** | A mechanical script for everything that can be counted, a blind reviewer for judgment | `scripts/*_check.py`, the `qc-gates` stack | length, caps, dashes, prohibited topics; then the evidence reviewer on the SOA's facts |
| **Learning** | What came back: the boss's edits, the reviewer's catches, the user's corrections, filed as lessons against this tool | `LEARNINGS.md` then, after review, the tool's own files | "Col X strikes any bullet without a number" becomes a reader profile line |

A tool is not marked Available until it has all seven. `award`, `fitrep`, and `naval-letter` have the standard and the checks; they are missing exemplars, intake, quantification, voice, and the learning hook, and will be rebuilt to this shape before the next new tool.

## 3. The tool factory: one recipe, run the same way every time

Building by hand, one tool at a time, is how the first nine tools were made. It does not scale to forty and it produces uneven depth. The recipe below is what a build looks like, and most of it can be run by agents in parallel while a person makes the calls that need judgment.

**Step 1. Research (agents, parallel).** For the tool's task: the governing publication and any school handout (verbatim extract); practitioner guidance (what experienced officers say makes this product good or bad; sources named and dated); public exemplars where they exist (published citations, released orders, doctrine examples); the failure modes (what gets a product returned). Output: a research packet with sources.

**Step 2. Standard and voice (agent, then person).** From the packet: the verbatim extract; the voice file (verbs, forbidden words, reader expectations); the checks that can be mechanical. A person reads the extract once and confirms nothing was paraphrased.

**Step 3. Exemplars (agent drafts, person judges).** Write three strong fictional exemplars and one weak one to the standard, annotate every line. A person decides whether they would sign them. If not, the annotations are wrong, and the tool is not ready.

**Step 4. Intake (person, with an agent).** Write the questions. This is the part that must come from officers, not from documents: what would a good XO ask a lieutenant who walked in with this? Draft with the agent, cut with the person, order them the way a conversation goes.

**Step 5. SKILL.md and scripts (agent).** Assemble from a fixed template so every tool reads the same way. Write the checker. Write three evals: one clean, one that must fail, one judgment case with a rubric.

**Step 6. Test blind (fresh session).** A second session, with the plugin installed and none of the build context, runs the evals and one real task from a user's own notes. Everything it gets wrong goes to the lessons queue. Fix, rerun, then mark Available.

**Step 7. Release.** Version bump, changelog line, package, push. Users click Update.

Steps 1, 2, 3, and 5 are agent work and can run for several tools at once. Steps 4 and 6 need a person and are where the quality comes from. The Workflow tool can run steps 1 to 3 and 5 as a scripted pipeline, one tool per lane, with the person's decisions collected at the end of each lane; that is the first thing to set up when the next batch starts.

## 4. Tailoring to the job, not the school

The kit must fit an S-1 clerk officer as well as a platoon commander. Two mechanisms:

**A billet map.** A table of the billets officers actually hold in their first years (platoon commander, company executive officer, company commander, S-1 assistant or adjutant, S-3 assistant, S-4 or supply officer, aide, series or instructor, staff secretary, watch officer) against the products each one signs or drafts every month. `start` asks the billet and turns on the modules and tools that match. The map is built from doctrine and billet descriptions first, then corrected by the officers who use the kit; every correction is a lesson.

**Reader profiles.** A boss, a board, and an approval authority read differently, and the same boss reads a fitrep differently from a training request. The rules file already holds "how my boss wants things"; the kit adds a short reader profile per recurring reader (name optional, role required): what they read first, what they strike, what they praise, length they tolerate. `award` and `fitrep` read the profile for the approver; `weekly-update` reads the profile for the OIC. Profiles are filled from the user's answers and from the lessons queue when a product comes back edited.

## 5. The feedback loop that makes it self improving

The kit gets better only if what comes back reaches the tool. Four sources, one queue:

1. **Corrections in session.** "Too in the weeds," "he never signs one without numbers." The `aar` tool captures these at the end of a task with the target tool named.
2. **Reviewer catches.** Every KILL, WRONG, or NO SHIP is a defect the drafting tool should have prevented; `qc-gates` writes it to the queue automatically.
3. **What the reader did.** The user pastes or describes the boss's edits; the tool diffs its draft against the signed version and files the pattern as a reader profile lesson.
4. **Blind test failures.** Step 6 above.

`inspect` turns the queue into proposed edits to the exact lines of the tool, a person approves, the tool's evals run, the change ships. Nothing softens a check or reduces sourcing without a person seeing it.

## 6. Order of work

1. **Rebuild the three Admin tools and `naval-letter` to the seven part shape** (exemplars, intake, quantification, voice, learning hook). They are the highest stakes products and the pattern for everything after.
2. **Build `aar` and `inspect`** so the loop exists before the next batch of tools creates more to learn from.
3. **Write the billet map and the reader profile format**, and wire them into `start` and `rules-file`.
4. **Set up the tool factory as a scripted pipeline** and run the next batch through it: `weekly-update`, `after-action`, `counseling`, `training-schedule`, `order-analysis`, `brief` (the PowerPoint brief tool: intake for audience and decision sought, the one slide rule, the reviewer on every slide).
5. **Blind test each batch in a fresh session** on real tasks from at least two officers in different billets, then release.

## 7. What I need from the user to start

- Two or three real products the user would sign today, in each of awards, fitreps, and letters, with the reader's edits if they exist. They stay in the user's folder as private exemplars; scrubbed fictional versions become the plugin's.
- The intake questions in the user's own words for one tool, spoken, not written: "if a lieutenant brought me a NAM, I would ask..." That recording is the seed for every intake file.
- The list of billets the first users hold, so the billet map starts from real people.

## 8. How a release reaches everyone (set up 19 Sep 26)

The repo is public and is a plugin marketplace. People install it in Claude desktop through Customize, Plugins, the plus button under Personal plugins, Add marketplace, Add from a repository, `https://github.com/azachdolan-bit/officer-kit`, then Install on Officer Kit. The Claude GitHub App is installed on the repo with Sync automatically turned on in Manage marketplaces, so a new version reaches every marketplace install without anyone doing anything.

The release drill, every time:

1. Bump the version in both `plugins/officer-kit/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (they must match).
2. Run `evals/install_check.py` and the harnesses. Build the file with `scripts/package.sh`.
3. Merge the change to `main` through a pull request. Automatic sync fires on a merged pull request that carries a version bump; a plain push may not.
4. On the GitHub releases page, publish a release tagged with the version and attach `dist/officer-kit.plugin` (for people who cannot use the marketplace) and, when it changed, `Officer-Kit-Starter-Library.zip`. `releases/latest` is the link on the slides and in GETTING STARTED, so it must always carry both files.
5. Anyone who installed from the file has to download the new file; anyone on the marketplace gets it automatically, or can force it with Check for updates in Manage marketplaces.

The starter library is fifteen public publications copied from the maintainer's marine-regs library, built by hand on 19 Sep 26 (list and source pages in the zip's README). Refresh it when a publication in it is superseded.
