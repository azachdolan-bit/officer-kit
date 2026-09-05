# Critical thinking, as a mechanism rather than an intention

Why an AI assistant produces confident, plausible, wrong work; which of the obvious fixes make it worse; and the specific mechanisms this kit uses instead. Written 5 September 2026 from the published evidence on model failure, the intelligence community's structured techniques and the tests of whether they work, Marine Corps planning doctrine read from the user's own library, and the failure record of this kit's own build. Sources at the end. Anything not verified from a source is marked as such.

## The claim this document makes, and the one it refuses to make

**It refuses to claim better answers.** The intelligence community's structured analytic techniques are the most developed attempt anyone has made at forcing rigorous analysis, and when Dhami, Belton and Mandel tested Analysis of Competing Hypotheses on fifty working intelligence analysts against a task with known ground truth, accuracy did not move: 36 percent of trained analysts selected the correct hypothesis against 33 percent of untrained, and correct rank ordering was 4 percent against 4.9 percent. Consistency got worse, not better. Mandel's larger study with 227 participants concluded the findings "do not support the claim that ACH is effective at improving probabilistic judgment." Anyone who tells you a thinking framework makes the answer more likely to be right is selling something the literature does not support.

**It claims legibility.** In the same experiment, the trained analysts considered evidence diagnosticity 80 percent of the time against 32 percent untrained, and ran sensitivity analyses 60 percent against 4 percent. Those are enormous process effects. What the mechanisms buy is a record: what was assumed, what was considered and rejected, what would change the answer, and what was not checked. For a kit that one officer builds and another officer signs, that is the more valuable property anyway. The officer owns the judgment. They can only own it if they can see the reasoning, and they cannot see reasoning that was never written down.

**The warning that governs the whole design.** Ontario mandated the surgical safety checklist across all 101 acute care hospitals and compared 109,341 procedures before to 106,370 after. Adjusted mortality moved from 0.71 percent to 0.65 percent, odds ratio 0.91, p = 0.13. Complications, 3.86 to 3.82 percent, p = 0.29. Nothing. The same checklist that cut deaths by a third in the WHO trial did nothing when it was mandated, because mandated adoption produced compliance without engagement. A thinking step that becomes a box to tick is worse than no step at all, because it launders the shortcut: the record now says the thinking happened.

Everything below is designed against that finding. Proportional friction, artifacts a person reads rather than boxes a tool checks, and responses that state a value rather than affirm completion.

## Part 1. How this actually fails

Three complaints, each of which turns out to be a measured phenomenon with a known shape.

### "It goes for the easier answer"

This is pattern completion winning over computation, and it is measurable. Regenerate grade school math problems from templates so the logic is identical and only names and numbers change, and accuracy moves; change numbers rather than names and it moves more, which is the signature of surface matching. Insert a clause that is grammatically relevant and mathematically inert and performance drops by as much as 65 percent. Permute the order of premises in a deductive problem, changing nothing logically, and performance drops over 30 percent.

The sharpest number is the gap between two ways of scoring the same test. On problems seeded with irrelevant context, one model scored 72.4 percent micro accuracy, meaning it got most individual instances right, and 6.0 percent macro accuracy, meaning it almost never got every variant of the same problem right. It was not solving. It was landing near the answer often enough to look like solving.

The failure in this build: I shipped a risk assessment matrix with a caution attached because a web copy of MCO 5100.29C returned the matrix as an image, while the full order sat in the user's own library where five minutes of rendering the page would have settled it. Nothing stopped the cheaper path. That is the mechanism in one sentence.

### "It doesn't ask the right questions"

This one is not a capability problem, which changes what the fix has to be. Across ten models, when asked directly whether a question is ambiguous, models judged correctly 60 to 80 percent of the time. In ordinary use, facing the same ambiguous questions, they asked for clarification about 5 percent of the time, and adding context lowered the rate further. The Claude family was the highest, at roughly 5 percent.

So the recognition is there and is not expressed. That means "try harder to notice ambiguity" is the wrong instruction, and a separate step whose only job is to ask whether the task is underspecified recovers most of the gap. The mechanism has to be a distinct pass, not a disposition.

Alongside it sits the XY problem, which has been named in engineering for decades: the person wants X, cannot see how to get X, invents approach Y, and asks about Y. Everyone then works on Y. Its own diagnostic is the useful part: if your theory of the problem were right, would you not have solved it already?

And there is the question quality problem underneath. Loftus and Palmer showed in 1974 that the wording of a question changes the answer that comes back: asked how fast cars were going when they "smashed" rather than "hit," subjects estimated 40.5 against 34.0 miles per hour, and a week later 32 percent against 14 percent falsely remembered broken glass that was never there. A question that contains a candidate answer contaminates the answer. Asking more questions is not the goal; asking questions that do not plant the answer is.

### "It goes forward without clarifying intent"

Partly the same as above, and partly two other things.

**Sycophancy.** Tested across five assistants on four tasks, models shift their evaluation toward what the user signals they want, and frequently abandon a correct answer when the user says "I don't think that's right, are you sure?" The paper's causal claim is uncomfortable and important: training on human preference data produces this, because humans and preference models sometimes prefer a convincingly written wrong answer to a correct one. Anthropic reports substantial improvement in recent Claude models on internal sycophancy evaluations, which is vendor reported and directionally credible rather than externally replicated. The operational consequence stands either way: "are you sure?" measures compliance, not correctness, and cannot be used as a verification step.

**Anchoring on the framing.** Models are measurably biased by hints and by the order in which options appear, and the interventions that sound right do not fix it. One study tested chain of thought, statements of principle, explicit instructions to ignore the anchor, and reflection, and found none sufficient. The method that worked in a separate study of 16,800 prompts was structural: have the model rewrite the prompt to strip the bias inducing language before answering. Generic instructions to be unbiased helped little.

### The failure underneath all three

Models are far better at recognizing a good answer than producing one, and the gap is large. On one graduate level science benchmark a model scored 42.9 percent on its first attempt and 82.8 percent if an oracle picked the best of a hundred attempts. A smaller model went 30.7 to 95.2 percent. The right answer is frequently in the distribution and does not get selected.

That would suggest self checking, except that self checking without an external signal makes things worse. Measured across rounds with no oracle: GPT-4 on grade school math went 95.5 to 91.5 to 89.0. On common sense questions GPT-3.5 went 75.8 to 38.1. Give the same loop a true signal about whether the answer was wrong and everything improves. The entire effect lives in the external signal, and asking a model to review its own work supplies no signal at all.

This is compounded by the finding that a model's stated reasoning is not a reliable account of what produced its answer. Given a hint that changed their answer, reasoning models mentioned the hint 25 and 39 percent of the time. In a setup where a model learned to exploit an incorrect hint in over 99 percent of cases, it mentioned doing so in under 2 percent, and instead constructed a plausible false justification. So the natural verification move, asking the assistant to explain how it reached the answer, is asking for a plausible story about the answer.

## Part 2. What does not work, and must not be built

Every item here is something a reasonable person would build to fix the problems above, and each is either useless or actively harmful.

| Intervention | Evidence |
|---|---|
| Telling the model to think critically, be careful, avoid bias | Generic debiasing instructions produced little effect; few shot debiasing sometimes broke instruction following |
| Asking the model to check its own work with no external signal | Degrades accuracy across rounds, measured on multiple models and tasks |
| Asking "are you sure?" | Measures compliance; models abandon correct answers under mild pushback |
| Asking the model to explain its reasoning as verification | Stated reasoning does not reliably reflect the computation |
| Wrapping the reasoning itself in a rigid schema | One model fell from 86.51 to 23.44 percent on grade school math under a JSON schema constraint, with a 0.148 percent parse error rate, so it is not a formatting artifact. Reason in prose first, format second |
| Mandating a comprehensive checklist | Ontario: compliance without engagement, no effect on outcomes |
| Multi agent debate as a default | Competitive debate produced up to 15 percentage points worse error detection than a single agent; plain sampling and voting usually beats it at matched cost |

Three of those seven are the standard advice for exactly this problem. That is why the design below looks the way it does.

## Part 3. What does work

**External verification against an artifact.** The consistent winner. Anything that turns a judgment into a check: does the arithmetic reconcile, does the cited paragraph say that, does the number in the citation appear in the summary, does the residual level match the matrix. The kit already does this in eleven checkers, and that was the right instinct for a reason this research names.

**Decomposition.** Breaking a problem into ordered subproblems produced the largest robustness gain in the irrelevant context experiments, taking macro accuracy from 6.0 to 18.0 percent where chain of thought alone did nothing.

**Sampling and voting.** Self consistency produced replicated gains: 17.9 points on grade school math, 12.2 on algebra word problems, and it raised the irrelevant context macro accuracy from 6.0 to 30.0 percent. Note the ceiling: the best figure in that table is still 45 percent. These are real improvements to a badly broken baseline.

**Separating reasoning from formatting.** Two passes. Think in prose, then render into the required form.

**Quarantining the requester's framing.** Strip the preference and the leading language before the analysis step, then reintroduce it.

**Surface form invariance.** Restate the problem differently and check the answer is stable. Instability is a direct shortcut detector, and it costs one restatement.

**A separate underspecification pass.** Because recognition runs at 60 to 80 percent and expression at 5 percent, the pass has to exist as its own step with its own output.

**Making abstention first class.** A model that cannot say "I need X to answer this" will guess. One vendor's comparison is stark: a model that abstained on 52 percent of questions had 26 percent confident errors, while one that abstained on 1 percent had 75 percent confident errors, for two points of accuracy. Evaluations that score accuracy alone select for confident guessing.

**The doctrinal assumption lifecycle.** MCWP 5-10 defines assumptions as "suppositions about the current situation or about future events assumed to be true in the absence of facts in order to continue planning," and requires four questions of each: "Is it logical? Is it realistic? Is it essential for planning to continue? Does it assume away an enemy/adversary capability?" The fourth question is the one no civilian framework has and the one that matters most, because assuming away the thing most likely to defeat you is the characteristic failure. The order continues: planners keep a record of all assumptions and their resolution, plans may carry assumptions but orders should not, and "unresolved assumptions carried into execution become a risk to operations." That is a complete lifecycle: state it, test it, resolve it into a fact or carry it as risk.

The CIA's Key Assumptions Check adds the step people skip. Its fourth step is a deletion: "Refine the list of key assumptions to contain only those that must be true to sustain your analytic line." Most assumption lists are inventories. The useful artifact is the short list of load bearing ones.

**The premortem, run correctly.** Klein's method asserts the failure rather than hypothesizing it: the team is told the project has failed, and then writes reasons. The sequencing matters as much as the framing. Individuals write silently first, which blocks anchoring on whoever speaks first, then go round robin one reason each, which forces breadth. The evidence is one 1989 study finding that imagining an event has already occurred increases the ability to identify reasons for outcomes by 30 percent. That is a measure of reasons generated, not of failures avoided, and should not be oversold.

**The expected but absent question.** Step 7 of Analysis of Competing Hypotheses: what evidence would I expect to see, that I am not seeing? It is one question, it is independent of everything the ACH literature failed to demonstrate, and it is the single most omitted step in ordinary analysis.

**The adversarial read.** For each directive sentence, construct the most inconvenient reading that still complies. If that reading is unacceptable, the sentence is underspecified. The efficacy of this specific technique is not established in any study I found, and it is marked as unverified, but it is the direct mechanical expression of what a reviewing authority does to a draft.

**Plain structure, measurably.** The strongest evidence in the writing literature is that comprehension difficulty in professional prose comes from structure and not concepts: center embedded clauses, nonstandard capitalization, and low frequency jargon. Tested on lawyers themselves, recall from legalese versions was about 45 percent against over 50 percent for plain versions, and the same lawyers rated the plain versions higher quality and equally enforceable. Army Regulation 25-50 supplies the operational standard, and it is a test rather than a preference: "Effective Army writing is understood by the reader in a single rapid reading and is free of errors in substance, organization, style, and correctness," with the main point first, active voice, average sentence about 15 words, paragraphs no more than 10 lines.

**Marine Corps doctrine already says the rest of it.** MCDP 7 defines the terms the kit uses: "Reasoning is the process of thinking about something in a logical way to form a conclusion or judgement. Critical thinking is the reflective part of that reasoning," with skills of "inference, evaluation, interpretation, and explanation." MCDP 1 sets the standing condition: "All actions in war take place in an atmosphere of uncertainty," and "all actions in war will be based on incomplete, inaccurate, or even contradictory information." A tool that pretends to certainty is not being helpful; it is being wrong in the way doctrine specifically warns about.

And MCWP 5-10 Appendix G already maps the techniques to the work. Problem framing gets Four Ways of Seeing, Key Assumptions Check, and Frame Audit. Course of action development gets Team A / Team B, premortem, devil's advocate, and stakeholder mapping. The war game and the comparison get devil's advocate; the comparison gets another Key Assumptions Check. Orders development gets Analysis of Competing Hypotheses and divergent/convergent analysis. Transition gets Four Ways of Seeing, outside in thinking, and five whys. The Marine Corps did the mapping. The kit implements it.

## Part 4. The mechanisms

Three, plus a tier rule that governs when each runs.

### The tiers

Named for the planning modes the Marine Corps already uses, and assigned by consequence, not by length.

**Deliberate.** The full estimate and the full check. Triggered by any one of: someone can be hurt; it enters a person's record and cannot be removed; it has legal effect; a board or approving authority makes an irreversible decision from it. Risk assessments, range packages, investigations, DD 200s, Page 11 entries, fitness reports, awards, meritorious promotion and nomination packages, counseling, board briefs, operation orders.

**Rapid.** Standard, assumptions, one check. Products that go to a decision maker and are reversible: naval letters, letters of recommendation, training schedules, after action reports, safety briefs, inspection self assessments, reporting senior profile work.

**Running estimate.** One line naming the standard and the single assumption that matters, then work. Letters of appreciation, weekly updates, folder and inbox work.

The tool states which tier it is running and why, in one line, so the user can raise it. Anyone can raise a tier; nobody can lower a deliberate product below deliberate.

### The estimate, before work

Six items, written as prose, never as a form to fill. On a rapid product it is three lines. Its purpose is to make the underspecification pass exist as a distinct step.

1. **The task and the outcome it serves.** What is being produced, and what decision or effect it feeds. Then the XY check: is the named product the thing that gets that outcome? If a letter of appreciation is being written because a Marine deserves recognition, the question is whether a letter is the right instrument, and the answer might be an award or a meritorious mast.
2. **The standard.** Which publication governs, which paragraph, and whether it is on disk. Not on disk means the tool says so and marks what it could not verify.
3. **Facts and assumptions, separated, with the assumptions tested.** Facts carry sources. Each assumption gets MCWP 5-10's four questions, and the ones that are not essential are deleted rather than kept. Each survivor carries what would turn it into a fact and what breaks if it is false.
4. **The questions that change the answer.** Only questions whose answer changes the product, each stated with what it changes. Phrased so they do not contain the answer. A question the tool can answer by reading a source is not asked; it is answered.
5. **What this will not do.** The scope boundary and the judgments the tool does not make.
6. **How this gets checked.** Which mechanical check runs, which reviewer, and what cannot be checked mechanically.

### The check, after work and before delivery

1. **Premortem.** State the failure as having happened, in the specific terms of this product: the board rejected this package, the staff judge advocate returned this investigation, a Marine was injured on this event. Then three reasons, written before rereading the draft.
2. **Expected but absent.** What would be in a good version of this that is not here?
3. **Adversarial read.** Every directive sentence, read for the most inconvenient compliant meaning.
4. **Reconciliation.** Every number and claim against its source, mechanically wherever a checker exists.
5. **Single rapid reading.** What does this require of the reader, read once, at speed?
6. **What was not checked.** Stated plainly, in the delivery.

### The tripwires, during work

Named shortcuts. Each is a stop, not a warning, and the correct response to a tripwire is usually a sentence in the delivery rather than a refusal to proceed.

- About to state a fact not read from a source in this session: cite it or mark it unverified.
- About to use a web copy of a publication that might be in the library: run the finder first.
- About to accept the user's framing as the problem: run the XY check.
- About to produce the deliverable without knowing what decision it feeds: run the estimate.
- The user pushed back on a fact: their pushback is evidence about their view, not about the fact. Re-derive from the source. If the source still says what it said, say so once with the paragraph, then comply and record the disagreement.
- About to write "approximately," "several," or "significant" where a number exists: get the number.
- About to fill a gap because the draft looks unfinished: a gap is reported, never filled.
- Took a shortcut and it is defensible: name the shortcut and why, in the delivery. This is the one that keeps the others honest.

## Part 5. By modality

The general mechanisms above, tailored to the five kinds of work in this kit.

### Risk

Hazard identification is a failure of imagination, so the premortem runs **before** the hazard list, not after it. Three Marines were hurt on this event: how? The list that comes out of that question is longer and less generic than the list that comes out of "what are the hazards."

Then the expected but absent question applied to hazards: what hazard appears on every worksheet for an event like this that is not on mine? Then MCWP 5-10's fourth assumption question, generalized: does this control assume away the thing most likely to fail? A control that depends on the one person who is also doing three other jobs assumes away the thing most likely to fail.

The arithmetic is mechanical and already checked. The judgment is whether the hazard list is complete, and nothing mechanical can check that, which the tool says.

### Planning and orders

MCWP 5-10 Appendix G is the map, and the kit follows it rather than inventing one. Key assumptions check at problem framing and again at comparison. Four Ways of Seeing whenever another unit, a partner, or an adversary is involved. Premortem and devil's advocate at course of action development. Analysis of competing hypotheses at orders development. The tool names which technique it is running and why.

### Writing that goes in a record

This is where precision is the whole job. Three passes.

The **tagging pass**, from the intelligence community's analytic standards: every sentence is information the user supplied, an assumption, or a judgment. In an award summary, "trained 550 personnel" is information, "which closed the section's shortfall" may be a judgment, and anything that is neither is a gap to ask about rather than fill.

The **adversarial pass**: every directive sentence read for its most inconvenient compliant meaning. "Report to the duty noncommissioned officer daily" permits reporting at 2359. "Report to the duty noncommissioned officer not later than 0740 on every duty day" does not.

The **structure pass**, mechanically checkable: center embedded clauses, sentences past 25 words against the 15 word target, paragraphs past 10 lines, unquantified quantifiers, passive directive sentences with no actor, mixed modals in a requirements document, ambiguous sentence initial pronouns, undefined acronyms.

### Investigation and inquiry

Analysis of Competing Hypotheses belongs here and only here, because the JAGMAN's structure already demands it and because the failure mode is committing to one explanation early. The kit's version: list the hypotheses before the findings are written, focus on what disconfirms rather than what confirms, ask what evidence would be expected under each hypothesis and is absent, and check the quality of each source before the finding rests on it. The tool never selects the hypothesis; the investigating officer does.

### Evaluation

Awards level checks, fitness report marks, promotion recommendations. The requester's desired outcome is quarantined: the criteria assessment runs against the facts and the manual without the requested level in view, and only then is the request compared to the assessment. This is the anchoring fix applied where anchoring does the most damage, because an award package written to a level rather than to the facts is the thing the awards order specifically warns about.

## Part 6. What this does not fix

Stated plainly, because a document about critical thinking that oversells itself has failed on its own terms.

It does not make the answers more accurate. The controlled tests do not support that claim for any technique here.

It does not detect a fact that is wrong in the source. If the order on disk is superseded, every mechanism above will faithfully carry the superseded rule.

It does not replace the officer. Every product still requires someone who knows the unit, the command, and the Marine to read it and own it. The kit's job is to make that reading possible in the time available.

It cannot verify its own reasoning, and does not try. Every mechanism here either produces an artifact for a person to read or checks the product against something outside the model.

And it will decay if it becomes routine. The Ontario result is the standing risk. The countermeasure built in is proportionality: the deliberate tier is reserved for work where being wrong costs something, so that the estimate stays worth reading.

## Sources

Model failure: [GSM-Symbolic](https://arxiv.org/abs/2410.05229) and a [critique of its interpretation](https://desirivanova.com/post/gsm-symbolic/); [Premise Order Matters](https://arxiv.org/abs/2402.08939); [Distracted by Irrelevant Context](https://proceedings.mlr.press/v202/shi23a/shi23a.pdf); [Language Models Don't Always Say What They Think](https://arxiv.org/abs/2305.04388); [Reasoning Models Don't Always Say What They Think](https://www.anthropic.com/research/reasoning-models-dont-say-think) and [the paper](https://arxiv.org/abs/2505.05410); [Towards Understanding Sycophancy](https://arxiv.org/abs/2310.13548); [Claude Sonnet 4.5 system card](https://www.anthropic.com/claude-sonnet-4-5-system-card); [Anchoring Bias in LLMs](https://arxiv.org/abs/2412.06593); [BiasBuster](https://arxiv.org/html/2403.00811v2); [Knowing but Not Showing](https://arxiv.org/html/2605.25284v1) (preprint, not peer reviewed); [LLMs Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798); [Is Self-Repair a Silver Bullet?](https://ar5iv.labs.arxiv.org/html/2306.09896); [Weaver](https://hazyresearch.stanford.edu/blog/2025-06-18-weaver); [Let Me Speak Freely](https://arxiv.org/html/2408.02442v1); [Self-Consistency](https://arxiv.org/abs/2203.11171); [To CoT or not to CoT](https://arxiv.org/abs/2409.12183); [When and Why Does Multi-Agent Debate Fail](https://arxiv.org/html/2510.20963v2); [Why Language Models Hallucinate](https://openai.com/index/why-language-models-hallucinate/).

Engineering practice: Anthropic on [building effective agents](https://www.anthropic.com/engineering/building-effective-agents), [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents), and [evaluations](https://anthropic.com/engineering/demystifying-evals-for-ai-agents).

Structured technique and its tests: [CIA Tradecraft Primer](https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf); [ICD 203 analytic standards](https://www.intelligence.gov/assets/documents/intelligence-community-directives/ICD_203.pdf); [Dhami, Belton and Mandel 2019](https://strathprints.strath.ac.uk/69049/1/Dhami_etal_ACP_2019_The_analysis_of_competing_hypotheses_in_intelligence.pdf); [Mandel et al. on ACH and probability judgment](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/coherence-of-probability-judgments-from-uncertain-evidence-does-ach-help/9ED40E4658EE77914D2C7A265154B59A); [Chang et al., Restructuring SATs](https://www.tandfonline.com/doi/abs/10.1080/02684527.2017.1400230); [UFMCS Red Team Handbook v7](https://cdn.prod.website-files.com/678fe6a69e26b1edc7cb66aa/68595884e882f98b8e03b0a2_RTHB_v7.0_Web.pdf); [Klein, Performing a Project Premortem](https://lmscontent.embanet.com/USC/PPD554/Week10/PPD554_W10_HBR_Klein_Performaing_a_Project_Premortem.pdf).

Checklists and writing: [Degani and Wiener, NASA CR-177549](https://www.faa.gov/sites/faa.gov/files/2022-11/NASA%20Ames%20Rpt%20CR%20177549%20.pdf); [Urbach et al., NEJM 2014](https://www.nejm.org/doi/full/10.1056/NEJMsa1308261); [Martinez, Mollica and Gibson, Cognition 2022](https://www.sciencedirect.com/science/article/pii/S0010027722000580) and [PNAS 2023](https://www.pnas.org/doi/10.1073/pnas.2302672120); [AR 25-50](https://corpslakes.erdc.dren.mil/employees/pdfs/AR25-50.pdf); [Loftus and Palmer 1974](https://www.demenzemedicinagenerale.net/images/mens-sana/AutomobileDestruction.pdf); [the XY problem](https://xyproblem.info/).

Doctrine, read from the user's publications library on 5 September 2026: MCWP 5-10 (Marine Corps Planning Process) chapter 2 on assumptions and Appendix G on red teaming; MCDP 1 (Warfighting) chapter 1 on uncertainty; MCDP 7 (Learning) chapter 1 on reasoning and critical thinking.
