---
name: rules-file
description: >
  Interviews the user and writes a personal rules file (CLAUDE.md) they keep at the top of
  their working folder and carry to every future unit, with an optional correspondence identity
  block that the naval-letter skill copies from. Every question is optional; the user decides
  how much of themselves to record. Use when the user says "build my rules file", "write my
  CLAUDE.md", "set up my rules", "rules file", "tell you about me", "personalize Claude",
  "make a project rules file", "update my rules", or wants Claude to remember how they work.
metadata:
  version: "0.3.0"
---

# Rules file builder

Interview the user and produce a rules file they save at the top of their working folder. Load `references/template.md` for the file shape and `references/example.md` for a filled in example.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Say this once

A rules file is ten minutes that pays back on every task after it. Claude reads it at the start of every session in that folder, so you never re explain your billet, your tone, or your no go list. Every question below is optional: skip anything you would rather not record. The file lives on your computer and is never sent anywhere. The more you give, the less you re explain; a thin file still works, and anything you leave out is simply asked for when a task needs it.

## Pick a depth first

Offer three, and accept the answer without argument:

| Depth | Records | Good for |
|---|---|---|
| **Light** | how you want drafts written, what Claude must never do | anyone who wants the behaviour without the biography |
| **Standard** | Light, plus rank and billet, weekly work, how your boss likes things | most users |
| **Full** | Standard, plus the correspondence identity block (the exact lines that print on a letter you sign) | anyone who will draft naval letters with the kit |

A user can move up later by running this skill again; it updates the file in place.

## Interview

One question at a time. Keep each to a line. Accept short answers; do not ask for more than they give. If they say "skip," write the field as `not recorded` and move on. Never fill a skipped field from context, a signature in an email, or an earlier document; a value they did not give is a value they did not give.

Standard and Full ask 1 to 6, including 1a and 1b. Light asks 1b, 3, and 5 only (the billet description is skipped, the module list is kept so the kit knows what to offer). Full adds 7.

1. **Who are you?** Rank, billet, unit or school, MOS if assigned. Any part may be left out.
1a00. **Library path.** If they built the full publications library (option B in `library`), record its folder path; every tool and every session reads orders from there first and goes to the web only when a publication is not on disk. Record the Reference folder too.
1a0. **Working label.** Say once: other Marines never appear by name in this folder or in a session; the tools use a label, `<MARINE>` unless you prefer another, and the name goes in at the last step on your own computer. Record the label.
1a. **Your billet, in your words.** Two to four lines: what the billet is responsible for, who you answer to and who answers to you (by billet, not name), and what a normal week looks like. This is the line the tools use to pick what to offer and to write your own fitness report input later; it is written by you, never guessed from the rank. The user may paste the billet description from their last fitness report or counseling instead.
1b. **Which of these does your billet make you do?** Read the list and take every yes: awards; fitness reports on others; your own fitrep input and profile; counselings; letters of recommendation or appreciation; meritorious promotion or recognition packages; naval letters and endorsements; orders and planning; teaching, classes, or studying. Record the yes list as the modules line; `start` and `week-ahead` read it.
2. **What do you handle every week?** Three to six items, verbs first: "draft counselings, build the training schedule, track exam queries."
3. **How do you want drafts written?** Offer: direct and brief; formal correspondence style; conversational. Ask about length and words to avoid.
4. **Who do you report to and how do they like things?** A name is optional; the format is what matters: BLUF first, bullets, one page.
5. **What should Claude never do?** Seed with: never send anything without showing the draft; never invent a reference or an order number; never include other people's names or personal details in anything that leaves the folder; never touch anything marked CUI.
6. **What is your fleet plan?** First unit if known, otherwise "unknown, update on arrival."
7. **Correspondence identity** (Full only). Say once: "These are the lines that print on a letter you sign. Copy them from a letter you have already signed if you have one; the exact printed form matters. Skip any you would rather supply at draft time." Then ask, one at a time:
   - SSIC you usually use (1500 for training matters is common)
   - Originator code, as printed on a signed letter
   - From line, exactly as it prints: rank, full name, billet, unit, course or command
   - Usual To line
   - Signature form (initials and surname in caps, for example F. M. LAST)
   - Point of contact line (phone or email, or both, or neither)

## Write the file

Fill the template with their answers. Rules for the output:

- Keep it under 150 lines. Long rules files get ignored.
- Every line is a fact or an instruction, not a paragraph.
- The security block is mandatory and comes first. Never remove or soften it. It protects other people's data and controlled material; it does not forbid the user's own name on their own correspondence.
- The Kit standards block comes second, copied from the template with its `Kit standards:` version line, which must match `STANDARDS.md`. The user may strike any numbered line; write a struck line as `- struck: <number>` so a later update never adds it back.
- Skipped fields are written as `not recorded (ask me at draft time)` so a later session asks instead of guessing.
- Include the dated Fleet section, mostly blank, with instructions to fill it on arrival.
- Save as `CLAUDE.md` in the root of the linked folder when one is connected. Otherwise deliver the file and say where to put it: the top of the folder they will work from.
- If the folder already has a CLAUDE.md, update the sections the interview touched and leave the rest as it was. Show the diff.

## After writing

Run one real task with the file active so they see the difference. Suggest: "Draft a one paragraph weekly update to my OIC on [topic]." Point out where the rules file changed the output.

Remind them: update it when the billet changes, not before. The Full block can be added at any time by running this skill again and saying "add my correspondence identity."

## Privacy rules

- Depth is the user's call. Do not sell Full; say what it unlocks and stop.
- Never record a field the user skipped, even if the value is visible elsewhere in the session.
- The rules file is the only place personal identity lives. Skills copy from it; they never store it.
- Never write anything from a `.mil` system, or anything marked CUI, into the file.
