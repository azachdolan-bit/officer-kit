---
name: think
description: >
  Four rules that survived being tested: assume the product already failed and write the reasons
  before drafting, ask the questions whose answers change the product, never claim to have covered
  what was not checked, and hand anything that gets signed to a blind reviewer. Use when the user
  says "think this through", "what am I missing", "red team this", "check my thinking", or before
  any product that can hurt someone, enter a permanent record, or decide something irreversible.
metadata:
  version: "0.2.0"
---

# Think

This skill used to be larger. It carried an estimate written before drafting, six formal passes
before delivery, ten named tripwires, and per modality tailoring. It was tested against itself on 5
September 2026 and most of it lost. `evals/ab-test-2026-09-05/` holds the artifacts.

What the test found, in one line: a template gets filled in instead of thought about. The drafter
working from a worked example reproduced the example's questions, never asked the obvious question
the tasking raised, invented twenty five details, and then told the approving officer that every gap
was marked. The drafter with no template asked better questions and claimed less. A blind reviewer
chose the second one.

So what is left is four rules and no template. Each one either produces something a person reads or
checks the product against something outside this session. Nothing here is a box to tick, and
nothing here asks the model to review its own work, which supplies no signal.

## 1. Assume it already failed, before you draft

Not "what could go wrong." The thing has failed, in this product's specific terms, and you are
writing the reasons.

- Risk assessment: a Marine was hurt on this event and this sheet is now an enclosure to the investigation.
- Award: the board downgraded it, or approved it and the Marine's peers could see it was inflated.
- Page 11: the separation board threw out the package because this entry did not support it.
- Investigation: the staff judge advocate returned it.
- Schedule: the week collapsed on Tuesday.
- Recommendation: the board read it and learned nothing about the Marine.

Three reasons minimum, written **before** you look at the draft or build the list. The ordering is
the whole mechanism. Reasons written after rereading a draft are a list of what the draft already
covers. In the test this was the one part that earned its keep: it is why one worksheet caught
operator fatigue on the drive home after a two day range, which the other left as a named phase with
no hazard in it.

## 2. Ask what you cannot answer, and only that

A question earns its place by changing the product. If the answer would not change what you write,
do not ask it.

Never supply the answer inside the question. "Roughly forty Marines?" gets forty. "How many Marines,
from the roster?" gets the number. A question that carries a candidate answer produces that answer,
and that is measured, not a style preference.

Ask the question the tasking actually raises, not the question a similar product usually raises.
The test's clearest failure was a drafter that asked three questions borrowed from an example and
never asked what "Table 2" meant, then built five of fourteen hazards on its own guess.

## 3. Say what you assumed. Never say you covered the rest.

State what you did not know and had to fill in, and mark it in the product itself so it cannot be
signed without being closed.

Then stop. Do not write that every gap is marked, that all assumptions are listed, that this is the
one assumption the product cannot carry, or that anything is otherwise complete. No pass anywhere
establishes that, and the claim is worse than silence, because the signer stops looking. This is the
finding that decided the test, and `scripts/precision_check.py` fails a product that makes the
claim, at every tier.

The honest form names its own basis. "Checked against the matrix and the required elements" rather
than "everything not listed is confirmed." "The assumptions I noticed" rather than "the assumptions."

## 4. Hand anything that gets signed to the red team

The `red-team` agent, blind: the draft, the standard, an exemplar if one exists, and nothing about
how the draft was made. It reports findings with evidence and never scores.

This is the only mechanism here that brings in a signal from outside the session, and it is the one
that caught everything the other mechanisms missed. Use it on any product that can hurt someone,
enter a permanent record, have legal effect, or decide something irreversible. It costs one agent.

## The scripts

- `scripts/precision_check.py <draft> [--directive]`: coverage claims (fails, every tier); center
  embedding, sentence length against a 15 word target, paragraphs past 10 lines, soft quantifiers,
  actorless passive directives, hidden verbs, mixed modals, loose pronouns, undefined acronyms,
  "and/or", vague deadlines. With `--directive`, ambiguity that changes what the reader must do
  fails instead of warning. Skips text an order prescribes, between `<!-- prescribed -->` markers.
- Each product tool's own checker does the arithmetic and the required elements. Those are fast,
  dumb, and reliable, and they run first.

## What this does not do

It does not make the answer more likely to be right. Structured technique tested on fifty
intelligence analysts moved accuracy from 33 to 36 percent, which is nothing. It does not supply a
fact, decide anything, or know what the commander wants. And an account of reasoning is a claim
about a product, checkable against the product, not a confession: where a shortcut was taken, name
it in the delivery rather than describing the reasoning that led to it.

`CRITICAL THINKING.md` in the repository carries the evidence, the sources, and the test.
