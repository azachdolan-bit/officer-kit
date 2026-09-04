---
name: rules-file
description: >
  This skill should be used when the user says "build my rules file", "write my CLAUDE.md",
  "set up my rules", "rules file", "tell you about me", "personalize Claude", "make a project
  rules file", or wants Claude to remember how they work across tasks.
metadata:
  version: "0.1.0"
---

# Rules File Builder

Interview the user and produce a personal rules file (CLAUDE.md) they save at the top of their working folder and carry to every future unit. Load `references/template.md` for the full template and `references/example.md` for a filled in example.

## Why this matters (say it once)

A rules file is ten minutes that pays back on every task after it. Claude reads it at the start of every session in that folder, so the user never re explains their billet, their tone, or their no go list.

## Interview

Ask one question at a time. Keep each to a line. Accept short answers and do not ask for more than they give. Six questions:

1. Who are you? Rank, billet, unit or school, MOS if assigned. (For a TBS student: "2ndLt, TBS student, Delta Company, MOS pending.")
2. What do you handle every week? Three to six items. Push for verbs: "draft counselings, build the training schedule, track EQFs, reply to platoon reps."
3. How do you want drafts written? Offer: direct and brief, formal Marine Corps correspondence style, conversational. Ask about length and any words to avoid.
4. Who do you report to and how do they like things? OIC or platoon commander name is optional; what matters is format: BLUF first, bullets, one page, etc.
5. What should Claude never do? Seed with: never send email without showing the draft, never invent a reference or an order number, never include names in anything that leaves the folder, never touch anything marked CUI.
6. What is your fleet plan? First unit if known, otherwise "unknown, update on arrival."

## Write the file

Fill the template with their answers. Rules for the output:

- Keep it under 300 words. Long rules files get ignored.
- Every line is a fact or an instruction, not a paragraph.
- The security block is mandatory and comes first. Never remove or soften it.
- Include a dated "Fleet" section that is mostly blank with instructions to fill it on arrival.
- Save as `CLAUDE.md` in the root of their linked folder if Cowork is active. Otherwise deliver the file and tell them to place it at the top of the folder they will work from.

## After writing

Run one real task with the file active so they see the difference. Suggest: "Draft a one paragraph weekly update to my OIC on [topic]." Point out where the rules file changed the output.

Remind them: update it when the billet changes, not before.
