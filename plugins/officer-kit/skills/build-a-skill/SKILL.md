---
name: build-a-skill
description: >
  This skill should be used when the user says "build a skill", "make me a skill", "I do this
  every week", "turn this into a skill", "automate this prompt", "create a custom skill",
  or describes a repeat task they want Claude to do the same way every time.
metadata:
  version: "0.1.0"
---

# Build a Skill

Interview the user about one repeat task and write a working skill file for it. No coding. The output is a folder with a `SKILL.md` they can drop into their own plugin or keep in their working folder. Load `references/skill-template.md` for the format.

## Two kinds of skill

A **personal skill** is a prompt with the rules decided: the five question interview below produces it in minutes. A **kit tool** is a product with a standard behind it (an order, a manual, a board's rubric) and needs the seven part shape the rest of the kit uses: the standard verbatim, fictional exemplars, an intake, the quantification ladder, a voice file, a mechanical checker, and a learning hook. For a kit tool, run `scripts/new_tool.py <tool-name> "<what it produces>"` to scaffold all seven with TODO markers, then fill them from the governing publication and the user's own exemplars (`add-exemplar`). `BUILD STRATEGY.md` in the repository is the long form of the shape; `references/tool-shape.md` here is the short form.

## Say this once

A skill is a prompt you never have to paste again, with the rules and format already decided. If you have done the same task three times, it should be a skill.

## Interview

One question at a time, short answers welcome. Five questions:

1. **What is the task?** One sentence. Push for a verb and an output: "draft the weekly platoon update," "turn range notes into an after action," "build a PT plan for the week."
2. **What goes in?** Where the input comes from: a file in the folder, an email, notes they paste, a calendar. Which folder or connector.
3. **What comes out?** The exact shape. Length, sections, format, filename, where it gets saved. Ask for an example of a good one if they have it.
4. **What are the rules?** Things it must always do and never do. Seed with the security line: no names, no markings, draft only.
5. **What would you say to trigger it?** Three or four phrases in their words. These go in the description so the skill fires when they talk normally.

## Write the skill

Produce `skills/<skill-name>/SKILL.md` using the template. Rules:

- Name is kebab case, two or three words, matches the folder.
- Description is third person and quotes the trigger phrases.
- Body is instructions to Claude, imperative, under 400 words. Sequence, output shape, rules. No explanation of why.
- Security block is included by default. Do not remove it unless the task is purely personal and the user says so.
- If the user gave an example output, put it in `references/example.md` and tell the skill to match it.

## Kit tool checklist (after new_tool.py)

- [ ] standard.md carries the order's own words with paragraph numbers, nothing paraphrased
- [ ] intake.md asks in the order a good reviewer asks, and every question that expects a number says so
- [ ] exemplar.md has one strong and one weak, fictional, annotated
- [ ] the checker enforces at least three things the standard imposes, plus the strike list and blocked content scan
- [ ] evals/<tool>/inputs has a good and a bad case and the checker passes one and fails the other
- [ ] SKILL.md description says what and when in third person with the phrases a user would say
- [ ] a person who did not build it runs it on their own material and it holds

## Test it

Run the new skill once on real input in the same session. Fix what missed. Then tell the user where the file is and how to install it: put the `skills/` folder inside a plugin, or keep it in the working folder and reference it by name.

## Common first skills for this audience

Offer these if the user is stuck: weekly update to the platoon commander, counseling draft from bullet notes (scrubbed), training schedule from a list of events, after action from range notes, PT plan for the week, lesson packet to quiz (already exists as `study-guide`), personal weekly review.
