---
name: fleet-transition
description: >
  This skill should be used when the user says "fleet transition", "I'm at my first unit",
  "day one checklist", "I just checked in", "set up Claude for my new unit", "update my
  rules for the fleet", or mentions reporting to a new command.
metadata:
  version: "0.1.0"
---

# Fleet Transition

Get the kit working at the first unit in the first week. Walk the checklist with the user, one item at a time, and update their rules file as they go.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Day one

1. **Re read the security card.** Run `security-check` and say the card out loud. The line does not move because the work got real. If anything, it gets stricter: a unit has real names, real locations, and real readiness data. All of that stays off the personal account.
2. **Ask the command what is allowed.** Before connecting anything, the user finds out from their S6 or IT what AI tools the command permits and on what accounts. If the command has a sanctioned tool, use that for work and keep the personal Claude account for personal and study use. Do not guess. Do not assume the school's tolerance carries over.
3. **Update the rules file.** Fill the Fleet section: unit, billet, what changed about weekly work, what connectors are allowed, date. Rewrite "What I handle weekly" for the new billet. Keep the security block untouched.

## Week one

4. **Rebuild the folder.** New linked folder for the new unit, structure from `folder-triage`, scrubbed from the start. Nothing moves from a government system into it.
5. **Retire the school skills, build the billet skills.** Study skills go to archive. Run `build-a-skill` for the two things the new billet does every week. Most common for a new platoon commander: the weekly update to the company commander, and the training schedule from the company's list.
6. **One scheduled task.** `week-ahead`, Sunday evening, personal calendar only.
7. **Find your buddy.** Someone else at the unit using Claude. Share the plugin. Compare rules files. The kit gets better when two people are running it.

## Microsoft note

At a unit the daily tools are likely Outlook, Teams, Word, and Excel. Claude has add ins for these. Whether the user can use them depends on the command's licensing and policy, and they will almost certainly be on a work account rather than the personal one. Explain the concept, point to the command's IT for the answer, and do not attempt to connect a .mil account to a personal Claude subscription under any circumstances.

## Output

When the user finishes, produce a short "Fleet setup complete" note: rules file updated (date), folder linked, skills built (names), scheduled task set, connectors confirmed with IT (yes / no / pending). Save it in `01_Admin`.
