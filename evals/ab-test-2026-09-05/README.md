# Did the thinking layer make the product better? One test, 5 September 2026

Version 0.7.0 added a consequence tier to 24 tools. Twelve run at the deliberate tier, which writes
an estimate before drafting and runs a six pass check before delivery. Nobody had ever run one end
to end. This is that test, kept in the repo because the result went against the feature and the
artifacts are the only reason anyone should believe it.

## Design

One tasking (`tasking.md`), written the way a lieutenant actually asks: a company live fire range,
Table 2, Range 7, two days, one heat casualty last year, "battalion wants it by Friday." Nothing was
planted in it. It is thin in the ordinary way.

Two independent agents drafted the worksheet from the same `risk-assessment` skill:

- **A** got the skill with the `## Thinking (tier: deliberate)` block deleted.
- **B** got the skill intact, plus the `think` skill it points to.

Neither knew the other existed. Neither was told a comparison was running. Both ran
`raw_check.py` and fixed what it caught.

Then both worksheets were stripped of provenance, shuffled by a coin flip whose key was written to
a file the reviewer never saw, and handed to the `red-team` agent with the standard, the matrix, and
the exemplar. It reported on each, then answered four comparison questions, the third of which was
the one that mattered: which facts does each worksheet assert that the tasking never supplied and
that are not marked as gaps.

## Result

Both passed `raw_check.py` clean. Both found the same top line: highest residual ID, not high risk
training under the 040302 pair test, battalion CO as the first O-5. Two independent sheets agreeing
on the approval authority is the strongest evidence in the package that the routing is right.

Both left exactly ten blanks open, in different notation.

The blind reviewer, asked which one it would route to the O-5 on Friday, chose **A: the worksheet
built with the thinking layer removed.**

Its reason: A asserted sixteen facts the tasking did not supply. B asserted twenty five, and B's
notes to the approver stated that "each missing item is a gap rather than an omission, and each one
is bracketed above," and that the corpsman was "the one assumption this sheet cannot carry." Both
sentences are claims about the whole product. Neither was true. Among what B asserted without
marking: a 0330 start, an unimproved access road, a movement in darkness, a manned range tower, an
overnight on the range, and the entire content of the table being fired.

A made no coverage claim, so its sixteen were things the approving officer had not been told. B's
twenty five were things he had been told in writing were not there.

## Why it happened, which is the part worth keeping

Two mechanisms, both visible in the artifacts.

**The worked example supplied the answers.** `references/estimate.md` carried a worked deliberate
estimate for a live fire range. Three of B's five questions came from it: the corpsman's
certification, what went wrong last time, whether the battalion publishes its own matrix. B
reproduced the example's load bearing assumption nearly verbatim. Meanwhile A, with no example in
front of it, asked the question the tasking actually raised: **Table 2 of what?** B never asked. It
assumed an answer and built five of its fourteen hazards on the assumption.

An example in the same domain as the task is not a help. It is a source of answers, and it displaced
the question that mattered.

**The check invited a claim it could not support.** Pass 6 asks what was not checked. B inverted it
into an assurance that everything else was. That inversion is available from the template's wording,
and it is worse than saying nothing, because the signer stops looking.

Neither of these is bad luck. Both are properties of the documents, and both are now fixed.

## What B did better, recorded so the fix does not overcorrect

B found four hazards A missed, and one of them is the kind that kills Marines: **operator fatigue on
the return movement after two days.** A listed a return phase and put no hazard in it, which is a
hole an investigating officer finds by counting. B also caught hot brass driving an uncontrolled
weapon movement, injury while clearing a hot chamber malfunction, and a dud handled on police call.
A found range fire and line safety degradation on day two, both of which B missed entirely.

Neither sheet is complete. Between them they hold a better hazard list than either holds alone.

## Fixes made because of this test

1. `precision_check.py` read every risk level (IE, IID, IIB) as an undefined acronym, producing
   about twenty junk warnings on the one document type it was wired into. Fixed; A's warning count
   fell from 31 to 19.
2. The worked example in `references/estimate.md` is now a 6105 entry, deliberately a different
   product from the one most often run at this tier, and it opens by saying its content is not to be
   taken. `estimate_check.py` fails an estimate that lifts its phrases.
3. A coverage claim in a delivered product now fails `precision_check.py` at every tier, with the
   patterns in `estimate_check.COVERAGE_CLAIM`. `check.md` pass 6 carries the prohibition and this
   test as its evidence.

All three are asserted in `evals/think_check.py`.

## What this test cannot tell you

It is one scenario and one run per arm. Run to run variance between two capable drafters could
produce a hazard count difference of 13 against 14 on its own, and probably did. Nothing here
separates the tier mechanism from luck on the hazard lists.

What it does establish is narrower and does not need a second run, because it is a property of the
documents rather than a difference in scores: the worked example supplies answers in its own domain,
and the check's sixth pass can be inverted into a false assurance. Those were true before the test
and would have been true on every run.

The reviewer is also a language model, from the same family as both drafters. It is blind to
provenance, which is the property that matters here, but it is not the O-5.
