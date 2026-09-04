---
name: start
description: >
  First run walkthrough for the Officer Kit: confirms the plugin is installed, sets up a working
  folder on the user's computer with a structure matched to their job, connects it, writes the
  rules file at the depth they choose, and runs one real task. Use when the user says "start the
  officer kit", "officer kit start", "set up the kit", "where do I begin", "walk me through
  setup", "what can this do", "which tools do I need", or has just installed the plugin.
metadata:
  version: "0.2.0"
---

# Start

Get a new user from install to their first real product in ten minutes, one step at a time. Do not present the whole menu; do the next step, confirm it worked, move on.

## Say this once

Personal account, personal data, personal device. Nothing CUI, PII, FOUO, or from a .mil system. The `security-check` skill has the full green, yellow, red card. Everything the kit produces is a draft; you read it before it goes anywhere.

## Step 1. Confirm the install

This skill running is the proof. Say so in one line and move on. If the user reached you without the kit installed (a shared transcript, a copied prompt), tell them where the plugin file is and stop.

## Step 2. What do you do most?

Ask one question: "Which of these is most of your week?" Offer the modules in the user's terms and accept more than one:

| Answer | Module | First task candidates |
|---|---|---|
| Letters, requests, endorsements | Correspondence | draft a naval letter from something they need to send this week |
| Awards, fitreps, counselings, updates | Admin | an award write up from bullet notes, or a fitrep section I draft |
| Orders, planning, exercises | Planning | critique or analyze an order they have on hand |
| Teaching, classes, studying | Training and teaching | a study guide or quiz from a handout they have |
| Not sure yet | Share and improve | the rules file, which forces the question |

Record the answer; it shapes the folder and the first task.

## Step 3. Make the working folder

Propose a folder at a location the user names (Documents is a fine default). Structure, trimmed to the modules they picked:

```
<Name> Kit/
  CLAUDE.md            the rules file, written in step 5
  Correspondence/      letters, memos, endorsements (docx and pdf)
  Admin/               awards, fitreps, counselings, updates, AARs
    Awards/
    Fitreps/
  Planning/            orders received, analyses, worksheets, overlays
  Training/            handouts captured, study guides, quizzes, walkthroughs
  Reference/           the manuals and school handouts the tools cite
  Print/               cards and laminates
  _build/              scripts and intermediate files the tools create
```

Rules: every module gets its folder only if they picked it, plus Reference, Print, and _build always. Nothing from a .mil system goes in. If they already have a folder they work from, adapt it instead of making a new one; `folder-triage` can inventory and restructure it.

Create the folders if a folder is already connected; otherwise give the structure and ask them to create it.

## Step 4. Connect the folder

In Cowork, the folder has to be linked before Claude can read or save there. Say: "Add the folder in the Cowork sidebar, then tell me when it is connected." Confirm by listing it. Every product from now on is saved there in the same session it is made.

## Step 5. Write the rules file

Run `rules-file`. Say once: every question is optional; Light, Standard, or Full; the file lives on their computer and is never sent anywhere; Full is only needed if they will draft correspondence with the kit. Save as `CLAUDE.md` at the top of the folder.

## Step 6. Run one real task

Pick from the first task candidates for their module. Use their own material, not a sample. Save the product to the right subfolder. Then point out, in two lines, where the rules file changed the output and which reviewer ran.

## Step 7. What to do this week

Present only when asked or at the end of the first session. Keep it to the list.

- Day 1: rules file written, one real task done.
- Day 2: put the manuals your work cites into Reference (awards manual, PES manual, correspondence manual, the school handouts you were issued). Tools cite what is there.
- Day 3: one product from each module you use.
- Day 4: build one skill of your own with `build-a-skill` for something you do every week.
- Day 5: run `qc-gates` on something you are about to sign.
- Later: `fleet-transition` when you change units. `MODULES.md` in the repo lists every tool and what is coming.

## Tone

Match the user's register. Officers want direct, brief, specific. Show the result, then say what to do next.
