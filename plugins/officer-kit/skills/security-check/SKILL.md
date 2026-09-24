---
name: security-check
description: >
  This skill should be used when the user asks "is this safe to share", "can I put this in Claude",
  "security check", "check this folder", "green yellow red", "what can I give Claude",
  is about to link a folder, or mentions CUI, PII, FOUO, OPSEC, or classification.
metadata:
  version: "0.1.0"
---

# Security Check

Keep the user on the right side of the line. This skill exists because the user is a service member using a personal Claude account. Apply it before any folder link, file upload, or connector task that looks like it touches unit material.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## The card

**Green: go.** Unclassified personal material, published doctrine and open source references, study notes in the user's own words, personal schedules, personal email, receipts, workout plans, anything already public.

**Yellow: strip and go.** Unit admin where names, SSNs, DoD ID numbers, EDIPIs, phone numbers, addresses, medical details, and unit specific operational details have been removed or replaced with placeholders. Rosters become "Marine 1, Marine 2." Training schedules keep the structure, drop the location specifics and unit identifiers. Counseling drafts use "the Marine."

**Red: stop.** Anything marked CUI, FOUO, or classified at any level. Anything pulled from a .mil system, government email, or a government device. PII of anyone other than the user. Operational details: locations, timelines, movements, capabilities, readiness. Medical, legal, or disciplinary records. Anything the user would not want to explain to their OIC or an IG.

When unsure, treat it as red and say so.

## What the Marine Corps itself says

NAVMC 5239.1 (4 December 2024, announced by MARADMIN 056/25) is the Marine Corps' own guidance on publicly available generative AI: users are responsible for what they put into a public AI system and must follow existing legal, cybersecurity, OPSEC, and classification policy; users should distrust and verify all outputs before use; commands are discouraged from banning generative AI. DoDI 5200.48 forbids conducting official business involving CUI on non DoD systems. The government's own platform, GenAI.mil, is certified for CUI and still prohibits PII on it. Read together: doctrine, formats, and the user's own writing are fine here; another Marine's name, EDIPI, marks, disciplinary facts, or a unit's readiness numbers are not. The Admin tools work on a label in place of the name and put the name back at render time on the user's own computer.

DRRS-MC, anything from SIPR, and readiness figures of any kind are out of scope for every tool in the kit. Say so if they come up.

## Folder scan

When the user is about to link a folder or asks to check one:

1. Inventory file names and types. Do not open files unless the user asks.
2. Flag by name any file that looks red: markings in the filename (CUI, FOUO, SECRET, NOFORN), rosters, SSN or EDIPI lists, medical, legal, NJP, counseling with names, anything with a .mil origin in its name.
3. Flag yellow candidates: rosters, schedules, counselings, evaluations, awards, anything with a Marine's name in the filename.
4. Report in three short lists: Red (remove before linking), Yellow (scrub before use), Green (fine). Keep it to filenames and a five word reason each.
5. If anything is red, tell the user to move it out of the folder before linking. Do not proceed with the link until they confirm.

## When the user pushes back

Do not lecture. State the line once, offer the scrubbed alternative, and move on. "I can draft the counseling if you swap the name for 'the Marine.' Want me to do that?"

## Reminders to surface

Say these when relevant, once, not every turn:

- Personal account only. Never sign in to Claude with a .mil address or on a government device.
- Drafts stay drafts. Nothing Claude produces goes onto a government system by copy and paste without the user reading it first.
- Claude has no clearance, no need to know, and no authority. It is a drafting tool.
- The disclaimer for the workshop and kit: personal initiative, not an official TBS or USMC product.
- Every rendered product carries an AI assistance line in its file properties. The signer owns the words; the line is there so nobody has to guess.

## Utility script

- `scripts/substitute.py <file.docx|.txt|.md> [--label "<MARINE>"] [--out file]`: asks for the name once on the user's own computer, writes a named copy beside the labeled original, stores nothing. Handles `<MARINE>`, `<MARINE_CAPS>`, `<LAST>`, `<LAST_CAPS>`. The labeled original stays the record; the named copy is submitted and deleted.
