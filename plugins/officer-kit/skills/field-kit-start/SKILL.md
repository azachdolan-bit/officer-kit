---
name: field-kit-start
description: >
  This skill should be used when the user says "start the field kit", "field kit start",
  "where do I begin", "first week", "walk me through the kit", "what can this plugin do",
  or has just installed the Claude Field Kit and wants orientation.
metadata:
  version: "0.1.0"
---

# Field Kit Start

Orient a new user to the Claude Field Kit and get them through their first seven days.

## First run

1. State the ground rule once, plainly: personal account, personal data, personal device. Nothing CUI, PII, FOUO, or from a .mil system. Point to the `security-check` skill for the full card.
2. Ask what they want to use Claude for most this week. Offer four lanes: study prep, platoon or unit admin, personal life admin, or "not sure yet."
3. Based on the answer, run the matching first task from the table below. Do not present the whole menu; pick one and do it.

| Lane | First task | Skill to run |
|------|-----------|--------------|
| Study prep | Turn a lesson packet or notes into a study guide and quiz | `study-guide` |
| Unit admin | Inventory and organize a linked folder | `folder-triage` |
| Personal admin | Triage the inbox and draft replies | `inbox-triage` |
| Not sure | Build the rules file, which forces the question | `rules-file` |

4. After the first task, run `rules-file` if they have not built one yet. The rules file is the single highest leverage thing in the kit; do not let a first session end without it.

## The seven day plan

Present this only when asked, or at the end of the first session. Keep it to the list.

- Day 1: Rules file written. One real task done.
- Day 2: Link a folder in Cowork. Run `folder-triage` on it.
- Day 3: Connect Gmail and Calendar. Run `inbox-triage` and ask for a week view.
- Day 4: Build one custom skill with `build-a-skill` for something you do every week.
- Day 5: Set one scheduled task with `week-ahead`.
- Day 6: Use the Chrome extension for one browser task and voice input for one long brief.
- Day 7: Read `fleet-transition`. Update the fleet section of your rules file.

## Tone

Match the user's register. Officers in training want direct, brief, and specific. Skip preamble. Show the result, then say what to do next.

## Available skills in this kit

Reference these by name when the user asks what the kit can do:

- `security-check`: what is safe to give Claude, and a scan of a folder before linking it
- `rules-file`: build a personal rules file (CLAUDE.md) with TBS and fleet sections
- `folder-triage`: inventory, structure, and clean up a linked folder
- `study-guide`: lesson packet or notes into a study guide and practice quiz
- `order-critique`: review a five paragraph order for completeness and clarity
- `inbox-triage`: find what needs a reply and draft responses
- `week-ahead`: a week ahead brief, and how to schedule it
- `build-a-skill`: interview the user and write a custom skill for their repeat task
- `fleet-transition`: day one checklist for the first unit
