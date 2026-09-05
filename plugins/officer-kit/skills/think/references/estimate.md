# The estimate

Written before drafting, shown to the user before drafting, in prose. Never a form. The point is that a person reads it and can redirect the work in one sentence while redirecting is still cheap.

## The six items

### 1. The task and the outcome it serves

What is being produced, and the decision or effect it feeds. Then the check that catches the most expensive kind of error: is the named product the thing that gets that outcome?

The pattern to catch is old and has a name. Someone wants an outcome, cannot see the route, invents a product, and asks for the product. Everyone then works on the product. Its own diagnostic: if the requester's theory of the problem were right, would the problem not already be solved?

In this kit it looks like: a letter of appreciation requested because a Marine deserves recognition, when the facts reach an Achievement Medal. A counseling requested when the leader needs the Marine to change and the last three counselings did nothing. A risk assessment requested to get a range approved, when the actual need is a range that is safe with the people available.

Ask once, in one line, and accept the answer. "You asked for X, which serves Y; a letter of appreciation is the lightest thing that reaches the record and the facts here may reach an award. Say which and I will draft it."

### 2. The standard

Which publication governs, which paragraph, and whether it is on disk. Run `library/scripts/find_order.py <number>` before saying anything about what a publication requires. Not on disk means the estimate says so and names what could not be verified. A tool that cites an order it did not read is the failure this whole kit is built against.

### 3. Facts and assumptions, separated, with the assumptions tested

Facts carry sources. Assumptions are stated as assumptions and tested with the four questions from MCWP 5-10:

> Is it logical? Is it realistic? Is it essential for planning to continue? Does it assume away an enemy/adversary capability?

The fourth question generalizes, and it is the one that earns its place: does this assume away the thing most likely to defeat the product? A range plan that assumes the corpsman will be there assumes away the most common reason ranges get cancelled. An award package that assumes the approver reads paragraphs assumes away the reader.

The third question is a deletion test, and the deletion is the point. The CIA's key assumptions check ends by refining "the list of key assumptions to contain only those that must be true." An assumption that is not load bearing is removed from the list, not kept for completeness. A list of fourteen assumptions is an inventory nobody reads; a list of three is a warning.

Each surviving assumption carries two things:

- **What would make it a fact.** The document, the roster, the phone call. Doctrine is explicit that assumptions should be turned into facts as soon as possible.
- **What breaks if it is false.** Nothing, a paragraph, or the whole product. An assumption whose collapse changes the product is a question, not an assumption, and moves to item 4.

MCWP 5-10 also supplies the disposition rule: plans may carry assumptions, orders should not, and "unresolved assumptions carried into execution become a risk to operations." Anything that survives into the delivered product is named in the delivery as risk the signer is accepting.

### 4. The questions that change the answer

Only questions whose answer changes the product. Each with what it changes. Two rules on the asking:

**No candidate answers.** Question wording changes the answer that comes back; this is one of the oldest measured findings in the field. Asked how fast cars were going when they "smashed" rather than "hit," people answered 40.5 against 34.0 miles per hour, and a week later 32 percent against 14 percent remembered broken glass that was never there. So: "How many Marines attended, and from what roster?" and not "It was around forty, right?" Open form where an open form exists. No embedded evaluation. No yes or no where a number or a name is wanted.

**Blocking versus recorded.** A question whose answer must exist before the draft is worth writing blocks work: the local order for a promotion package, the convening order for an investigation, the residual level's approval authority. Everything else proceeds with the assumption recorded, and the draft is delivered with the gap named. Waiting on a question that does not block is its own failure.

Three questions asked well beat eleven asked to appear thorough. The test for each: write down what the product looks like under each possible answer. If it looks the same, do not ask.

### 5. What this will not do

The scope boundary, and the judgments the tool does not make. This is short and it is not hedging: it tells the reader where their own work starts. "This does not decide the award level. It puts the facts against the criteria so you can."

### 6. How this gets checked

Which mechanical check runs, which reviewer, and what cannot be checked mechanically. The last clause is the important one. A checker that verifies the citation's character count does not verify that the Marine did what the citation says, and the estimate says so.

## At each tier

**Deliberate.** All six, roughly ten to twenty lines. Shown before drafting.

**Rapid.** Three: the standard, the assumptions that matter, and the questions that change the answer. Three to six lines.

**Running.** One line: the standard, and the single assumption that matters. "MCO 1650.19J; assuming the 38 count is from your roster; drafting."

## A deliberate estimate, worked

**Read this for its shape and take none of its content.** A worked example in the same domain as the task is not a help, it is a source of answers. Measured on this kit: an estimate written with a live fire range example in front of it reproduced that example's load bearing assumption and two of its three questions, and never asked the one question the actual tasking made obvious. So the example below is deliberately a different product from the one most often run at this tier. If a phrase from it turns up in a real estimate, that estimate was copied rather than written, and `estimate_check.py` fails it.

The user asks for a 6105 entry on a Marine who has missed formation three times.

> **Tier: deliberate.** It enters a record that cannot be removed and a separation board may rely on it.
>
> **Task and outcome.** A 6105 entry documenting unexcused absence, to give the Marine formal notice and a chance to correct, and to stand up if a package is built later. The entry is the right product only if counseling has already happened and failed; if it has not, the product is a counseling and the entry comes after.
>
> **Standard.** MCO 1900.16 paragraph 6105, read from the library. The entry text is prescribed and is not the drafter's to reword. The CO signs an adverse entry; a copy goes to CMC within 30 days; the Marine has 5 working days to rebut.
>
> **Facts.** Three absences, on the dates the user supplied from the duty log. Two prior informal counselings, dated, from the user.
>
> **Assumptions.** One is load bearing: the two prior counselings were documented rather than verbal. Becomes a fact from the Marine's record book. If false, the entry has no counseling history to rest on, and a board will read it as a first offense escalated straight to a permanent entry, so the entry is premature. That makes it a blocking question. Second: the CO intends this as adverse rather than administrative. Becomes a fact by asking the CO; if false, the signature block and the CMC routing both change.
>
> **Questions that change the answer.** (1) Are the prior counselings in the record book with dates? Changes whether this entry is supportable at all. Blocking. (2) What did the Marine say about the absences? Changes the entry's statement of facts, which the rebuttal will contest first. (3) Does the CO intend this as adverse? Changes the routing and the rebuttal clock.
>
> **Will not do.** This does not decide whether to separate, and it does not judge the Marine. It records the facts in the order's prescribed form and names what has to be true for the entry to stand.
>
> **Checked by.** `page11_check.py` for the prescribed wording, the four required elements, the signature block, and the 5 day rebuttal line; the red team agent against the standard. Nothing mechanical can tell you the facts are right or that the counseling actually happened, which is why question 1 blocks.
