---
name: think
description: >
  The kit's thinking discipline: the estimate that runs before a product is drafted (the task and
  the outcome it serves, the standard, facts separated from tested assumptions, the questions whose
  answers change the product, what this will not do, how it gets checked), the check that runs
  before delivery (premortem, expected but absent, adversarial read, reconciliation, single rapid
  reading), and the named shortcuts that stop work. Every product tool runs this at its consequence
  tier. Use when the user says "think this through", "what am I missing", "red team this", "is this
  the right approach", "check my thinking", or before any product that can hurt someone, enter a
  record, or decide something irreversible.
metadata:
  version: "0.1.0"
---

# Think

The kit's tools produce documents that people sign. A document that reads well and was never thought through is the failure this skill exists to prevent, and it is a specific, measured failure rather than a vague one: assistants recognize that a task is underspecified 60 to 80 percent of the time and ask about it around 5 percent of the time; they are far better at recognizing a good answer than producing one; and their own account of their reasoning is not a reliable account of it. `CRITICAL THINKING.md` in the repository carries the evidence and the sources.

Two conclusions from that evidence govern the design, and both are counterintuitive enough to state up front. **Self review supplies no signal.** Asking for a second look at one's own work, with nothing external to check against, measurably degrades accuracy; so every mechanism here either produces an artifact a person reads or checks the product against something outside the session. **A step that always runs becomes a step that is ticked.** When Ontario mandated the surgical checklist across 101 hospitals and 200,000 procedures, mortality did not move. So the estimate is proportional to consequence, and its output is prose a person reads rather than boxes a tool checks.

The honest promise: this does not make the answer more likely to be right. Tested on fifty intelligence analysts, structured technique moved accuracy from 33 to 36 percent, which is nothing, while moving whether analysts considered evidence diagnosticity from 32 to 80 percent, which is everything for a product someone else has to sign. What this buys is a legible record of what was assumed, what was considered, what would change the answer, and what was not checked.

## Read first

1. `references/estimate.md`: the six items, the tier rule, and what a good one looks like at each tier.
2. `references/check.md`: the six passes before delivery.
3. `references/tripwires.md`: the named shortcuts, and what to do at each.
4. `references/by-modality.md`: how this changes for risk, planning, writing, investigation, and evaluation.

## The tiers

The tool states which tier it is running and why, in one line. Anyone can raise a tier. Nothing lowers a deliberate product below deliberate.

| Tier | Triggered by | Estimate | Check |
|---|---|---|---|
| **Deliberate** | someone can be hurt; it enters a record and cannot be removed; it has legal effect; a board or approver decides something irreversible from it | all six items | all six passes |
| **Rapid** | goes to a decision maker, reversible | standard, assumptions, the questions that change the answer | premortem, reconciliation, what was not checked |
| **Running** | routine, low consequence | one line: the standard and the assumption that matters | the mechanical checker for that product |

Deliberate: risk assessment, range package, investigation, DD 200, Page 11, fitness report, award, meritorious promotion, nomination, counseling, board brief, operation order, order analysis.

Rapid: naval letter, letter of recommendation, training schedule, after action report, safety brief, inspection self assessment, reporting senior profile, study guide, walkthrough.

Running: letter of appreciation, weekly update, folder and inbox work, week ahead.

## Workflow

```
Think:
- [ ] 1. Tier named, in one line, with the trigger that set it
- [ ] 2. Estimate written to the tier (references/estimate.md); shown to the user before drafting, not after
- [ ] 3. Questions asked: only those whose answer changes the product, each with what it changes; phrased so they carry no candidate answer; a question a source can answer is answered, not asked
- [ ] 4. Blocking questions separated from the rest: a missing fact that cannot be assumed stops work; everything else proceeds with the assumption recorded
- [ ] 5. Draft (the tool's own workflow)
- [ ] 6. Check to the tier (references/check.md)
- [ ] 7. python3 scripts/estimate_check.py estimate.md exits 0 on deliberate products
- [ ] 8. Delivery states: what was assumed, what was not checked, and any shortcut taken and why
```

## Rules

- **Never fill a gap.** A gap is reported. This is the rule the other rules protect.
- **A question that carries its answer is contaminated.** "The count was around forty, right?" produces forty. "How many attended, and from what roster?" produces a number and a source.
- **Do not ask what a source can answer.** Reading the order is the tool's job; asking the user to recall the order is the tool avoiding its job.
- **Pushback is evidence about a view, not about a fact.** When the user says a fact is wrong, re-derive it from the source. If the source still says it, say so once with the paragraph, then do what the user directs and record the disagreement in the fact list or the file's notes so the signer sees both.
- **Never verify by self explanation.** "I checked and it is correct" is not a check. Name the artifact that was compared to what.
- **State the shortcut.** Taking a shortcut is often right. Taking one silently is not. One sentence in the delivery: what was skipped and why it is acceptable.
- **Abstention is an output.** "I need X before this is worth drafting" is a complete and correct answer.
- **The tool does not decide.** It does not choose the award level, the mark, the hypothesis, the liability, or the risk the commander accepts. It puts the argument and the gaps on the page for the person who does.

## Utility scripts

- `scripts/estimate_check.py estimate.md`: facts and assumptions present and separate; every assumption tested and carrying a falsifier and a collapse consequence; every question carrying what it changes and free of embedded answers; the scope line and the checked by line present. Exit 1 on a missing element.
- `scripts/precision_check.py <draft> [--directive]`: the structure pass. Center embedded clauses, sentences over the length target, paragraphs over ten lines, unquantified quantifiers where a number belongs, directive sentences in the passive with no actor, mixed modals, ambiguous sentence initial pronouns, undefined acronyms, "and/or". Advises on style; fails on ambiguity that changes what the reader must do.
