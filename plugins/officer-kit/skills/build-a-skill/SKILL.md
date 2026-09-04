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

## Test it

Run the new skill once on real input in the same session. Fix what missed. Then tell the user where the file is and how to install it: put the `skills/` folder inside a plugin, or keep it in the working folder and reference it by name.

## Common first skills for this audience

Offer these if the user is stuck: weekly update to the platoon commander, counseling draft from bullet notes (scrubbed), training schedule from a list of events, after action from range notes, PT plan for the week, lesson packet to quiz (already exists as `study-guide`), personal weekly review.
