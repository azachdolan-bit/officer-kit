---
name: week-ahead
description: >
  This skill should be used when the user says "week ahead", "what's my week look like",
  "brief me on the week", "Sunday brief", "schedule a weekly brief", "set up a recurring brief",
  "morning brief", or wants a standing summary of calendar and email.
metadata:
  version: "0.1.0"
---

# Week Ahead

Produce a one screen brief of the coming week, then offer to make it a scheduled task so it shows up without being asked.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Requires

Connected calendar, and optionally email. Personal accounts only. If neither is connected, produce the brief from whatever the user pastes or from the linked folder's schedules.

## The brief

Keep it to one screen. Sections, in order, in the user's rules file tone:

- **BLUF.** The one thing this week that matters most, and the first conflict if there is one.
- **By day.** Monday through Sunday, each a line: fixed events with times, and the one prep item that day needs.
- **Conflicts and gaps.** Overlaps, back to backs with no travel time, days with nothing scheduled that probably should have something.
- **Owed.** Emails that need a reply this week (pull from `inbox-triage` logic if email is connected), and anything the user said they'd deliver.
- **Suggested three.** Three tasks to do first thing Monday.

## Kit standards check (once per brief)

If the connected folder has a rules file, read its `Kit standards:` line and compare it to the version at the top of `STANDARDS.md`. If the line is missing or older, add one line to the brief naming the new standards, and on request show the block the template now carries as a diff against what the rules file has, skipping any line recorded as `- struck: <number>`, and add it only on the user's yes. Say what changed in one line per standard. Never touch any other section of the rules file.

## Make it recurring

After delivering once, ask: "Want this every Sunday at 1900?" On a yes, create a scheduled task using the app's scheduled task feature with a standalone prompt that reproduces this brief. Write the prompt so it works with no memory of this conversation: state the connectors to use, the sections, the tone, and the one screen limit.

Suggested defaults: Sunday 1900 local for the week ahead, and optionally weekday 0600 for a shorter daily version (today only, BLUF plus by hour plus owed).

Tell the user how to edit or stop it. Advise one scheduled task to start, not several.

## Rules

- Do not include content from any .mil calendar or mailbox. Personal accounts only.
- If a day is packed, compress: "0800 to 1700 field, no gaps." Do not list every block.
- Never move or create calendar events without a go.
