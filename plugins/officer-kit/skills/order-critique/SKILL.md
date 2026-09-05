---
name: order-critique
description: >
  This skill should be used when the user says "critique my order", "review this op order",
  "check my five paragraph order", "is my OSMEAC complete", "grade this order", "review my
  frag order", or pastes an operations order for feedback.
metadata:
  version: "0.1.0"
---

# Order Critique

Review a five paragraph order the way a good instructor would: completeness first, then clarity, then whether a squad leader could execute it from the text alone.

## Guardrail

Training orders written for a school exercise are green. Anything referencing a real operation, real unit locations, or carrying a marking is red; stop and point to `security-check`.

## Check in this order

**1. Structure.** Confirm all five paragraphs are present and in order: Orientation (if given separately), Situation, Mission, Execution, Administration and Logistics, Command and Signal. Under Situation: enemy, friendly, attachments and detachments. Under Execution: commander's intent, concept of operations, tasks, coordinating instructions. Under Command and Signal: signal then command. List anything missing before any other feedback.

**2. Mission statement.** Must contain who, what, when, where, and why, as one or two sentences, stated twice in the brief. Flag a missing element. Flag a "why" that is really a "what."

**3. Tasks.** Every subordinate unit gets a task. Every task is a tasking verb plus a purpose. Flag tasks with no purpose, purposes with no task, and units that were never tasked.

**4. Coordinating instructions.** Timeline, control measures, ROE if applicable, priority of fires, casualty and EPW plan pointers. Flag what is missing for this type of mission.

**5. Executability.** Read it as the most junior leader receiving it. Where would they have to guess? Name those spots.

## Output

- BLUF: one line. Complete or not, and the single biggest gap.
- Missing elements, as a checklist.
- Three fixes that would most improve it, each with the rewritten line.
- Do not rewrite the whole order unless asked. Never invent unit names, grids, or times; use the ones given or leave a placeholder.

If the user asks for a score, use a simple scale: Complete / Executable / Clear, each pass or fail, with one line each.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

MCWP 5-10 Appendix G maps the technique to the step: key assumptions check at problem framing, devil's advocate at the war game and the comparison, competing hypotheses at orders development.
