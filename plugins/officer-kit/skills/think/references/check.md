# The check

Runs after the draft, before delivery. Six passes at the deliberate tier, three at rapid, the mechanical checker alone at running.

Every pass here either produces something a person reads or compares the product to something outside the session. None of them is "look at it again," because looking at it again with nothing to check against measurably makes it worse.

## 1. Premortem

Klein's method, and the sequencing carries the effect.

**Assert the failure.** Not "what could go wrong." The thing has already failed, in the specific terms of this product:

- Risk assessment: a Marine was injured on this event and this sheet is now an enclosure to the investigation.
- Award: the board downgraded it, or approved it and the Marine's peers can see it was inflated.
- Page 11: the separation board threw out the package because the entry did not support it.
- Investigation: the staff judge advocate returned it.
- Training schedule: the week collapsed on Tuesday morning.
- Letter of recommendation: the selection board read it and learned nothing.

**Write the reasons before rereading the draft.** Generating first and comparing second is what stops the draft from anchoring the list. Three reasons minimum.

**Then check each against the draft.** Some will already be handled; say so briefly. The ones that are not are the finding.

The evidence for the framing is one 1989 study: imagining an event has already happened increased the ability to identify reasons for outcomes by 30 percent. That measures reasons generated, not failures avoided, and it should not be sold as more.

## 2. Expected but absent

One question, from step 7 of Analysis of Competing Hypotheses, and the most commonly skipped step in ordinary analysis:

> What would I expect to see in a good version of this, that is not here?

It is different from "what is missing," because it runs against a model of the product rather than against the draft's own outline. A summary of action with no comparison to a peer group. An investigation with no finding about what the standard required. A schedule with no prep list for the one event that needs one. A counseling with no prior counseling cited, on a Marine who has clearly been counseled before.

## 3. Adversarial read

Every directive sentence, read for the most inconvenient meaning that still complies. If that reading is acceptable, the sentence is fine. If it is not, the sentence is underspecified and gets rewritten.

- "Report to the duty NCO daily" permits 2359. Rewrite: "not later than 0740 on every duty day."
- "Submit the inspection sheet weekly" permits Sunday at 2300. Rewrite: "by 1500 each Thursday."
- "Ensure vehicles are maintained" permits believing they are. Rewrite: name who inspects what, when.
- "Marines will be briefed on the hazards" permits a briefing nobody understood. Rewrite: who briefs, from what, and what the Marine has to be able to state afterward.

The technique's effect has not been measured in any study found, and it is offered as the mechanical form of what a reviewing authority does rather than as an evidenced intervention. Its value is that it is cheap and it is specific.

## 4. Reconciliation

Every number and every claim against its source. Mechanically wherever a checker exists: the citation's numbers against the summary of action, the sheet's residual levels against the matrix, the brief's numbers against the package, the findings against the enclosures.

Where no checker exists, name the artifact and the comparison in one line: "the 550 figure is from the training record the user pasted; the 94 percent is from the readiness report they cited; the 'first in the battalion' claim has no source and is marked as the recommender's assertion."

Never "I verified the numbers." Which numbers, against what.

## 5. Single rapid reading

Army Regulation 25-50's standard is a test, not a preference:

> Effective Army writing is understood by the reader in a single rapid reading and is free of errors in substance, organization, style, and correctness.

So: read it once, at speed, as the reader who has twenty of these. What does it require of them? If the answer takes a second pass to find, the main point is not first, or a sentence is carrying two claims, or a clause is buried inside another clause.

`scripts/precision_check.py` does the mechanical half: center embedding, sentence length against the 15 word target, paragraphs past 10 lines, unquantified quantifiers, passive directives with no actor, mixed modals, ambiguous sentence initial pronouns, undefined acronyms. The comprehension research is specific that structure rather than concept is what makes professional prose hard, and that the people who write that way do not prefer reading it: tested on lawyers, recall from plain versions beat legalese versions and the same lawyers rated the plain versions higher quality and equally enforceable.

## 6. What was not checked

Stated in the delivery, in one or two sentences. Not a disclaimer, a map of where the signer's own attention is required.

"The arithmetic and the required elements are checked mechanically. Nothing here can tell you the hazard list is complete or that the corpsman will be there, which are the two things that would actually hurt someone."

## At each tier

**Deliberate.** All six.

**Rapid.** Premortem, reconciliation, what was not checked.

**Running.** The product's mechanical checker.

## What does not belong here

- Asking whether the draft is good. It supplies no signal.
- Asking the model to explain how it reached the answer, as verification. The explanation is generated after the fact and does not reliably describe what produced the answer.
- A confidence score on the product. Verbalized confidence is weakly calibrated and moves with the prompt.
- Rewriting for polish. The check finds defects; the drafter fixes them; polish is not a defect.
