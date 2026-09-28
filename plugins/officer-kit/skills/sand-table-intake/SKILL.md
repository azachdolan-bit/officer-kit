---
name: sand-table-intake
description: >
  Turns a base order the user received (the company or battalion order a platoon plans from) into the plan file the
  virtual sand table imports, with every paragraph higher wrote already in place and every decision that is the
  planner's left blank: the page builds the map from it, the planner does the tactical work there, and sand-table-order
  turns the export back into their order. Every value carries its paragraph; nothing is invented. Use when the user
  says "load my base order into the sand table", "sand table file from this order", "prefill the sand table",
  "start the sand table from the company order", "intake this order for the sand table", or attaches a base order and
  names the sand table. Also carries a troop to task matrix (xlsx or csv) into the plan file so the page walks it by
  the clock: "put my troop to task on the sand table", "rock walk the troop to task", "load the priorities of work".
metadata:
  version: "0.3.0"
---

# Sand table intake

The base order is higher's half of the plan: situation, mission, intent, fires available, adjacent units, timeline, logistics. The sand table's guided build asks for all of that before it asks for the planner's half (EMLCOA, engagement area, positions, parts, tasks, targets). This tool carries higher's half into the sand table as a file, so the planner opens the page and starts where their own work starts. The loop closes with `sand-table-order`: the planner exports from the page and that tool writes the order. Its failure modes are specific: a planner decision filled in from the order's example or from doctrine, a grid retyped wrong, a paragraph paraphrased into a different meaning, a value with no paragraph behind it. Each has a mechanism here.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Your own material (read first, every time)

1. `Overrides/sand-table-intake.md`: the user's school or unit way wins (their factor set, which sheet their exercise is on).
2. The base order itself, captured to text with the paragraph numbers kept.
3. Training orders from a school exercise are green. An order about a real operation, real unit locations, or carrying a marking is red: stop and point to `security-check`.

## Before you draft

1. **Assume it already failed** and write three reasons first; the usual ones are a planner decision filled from the order's own EMLCOA or intent, a 6 digit grid retyped as 8, and a value copied from the wrong platoon's task.
2. **Ask only what changes the product:** which platoon the user is (their task paragraph is the mission; the others are adjacent), which sheet the exercise is on (`references/field-map.md` lists the sheets the page carries), and the operation type when the order does not settle it.
3. **Say what you assumed.** A paragraph the order does not have is a blank, never a guess.

## Workflow

```
Sand table intake:
- [ ] 1. Save the order beside the product (kit standard 1); python3 scripts/order_text.py <order.docx> writes order.txt with the paragraph numbers kept (a PDF or photos: capture-source first)
- [ ] 2. Read references/field-map.md: which paragraph feeds which guide field, and which fields stay blank because the planner decides them
- [ ] 3. Write facts.json: one entry per field the order fills, and one object per position or control measure higher gives with a grid that the guide has no field for (adjacent units, a known enemy position, the company AA, CCP and CP, checkpoints, phase lines and boundaries), each with the order's label and its paragraph; with the value in the order's words (verbatim for mission statements, intent and EMLCOA; condensed only for long orientation prose, keeping every number and name) and src naming the paragraph. Grids exactly as written (4, 6 or 8 digits). The user's own platoon task is the mission; the other platoons' tasks and positions go to adjacent
- [ ] 4. python3 scripts/plan_writer.py facts.json --out <name>.sandtable.json: refuses an unknown field, a bad grid, a select value the page does not offer, or a value with no src; writes <name>.sourced.md (every filled field with its paragraph; every blank by step)
- [ ] 5. python3 scripts/plan_check.py <name>.sandtable.json --intake exits 0 (the page's shape; no planner decision filled; nothing on the map)
- [ ] 6. red-team agent, blind, with sourced.md and order.txt: every filled value found in the cited paragraph, nothing filled that the order leaves to the platoon
- [ ] 7. Save the plan file, sourced.md and facts.json together; name the path; tell the user: import it on the sand table page (Plan, Import file); the page switches to the file's sheet if it is not on it, builds the map from the values and opens the Guide at Review
- [ ] 8. A troop to task matrix (xlsx or csv): python3 scripts/t2t_reader.py <matrix.xlsx> --sheet "<sheet name>" --plan <name>.sandtable.json --rehearsal (or --out <name>.sandtable.json with no base order); read the <name>.t2t.md report back to the user: which map unit each row will draw from, and the page's security count beside their own row; a slot where the two differ is a cell the reader did not understand, not a correction to their plan
```

## Troop to task (priorities of work on the clock)

B3M0830XQ-DM Annex C: priorities of work are married to a timeline that starts at X (the time stand to ends), and the troop to task matrix carries them by unit. The page walks that matrix: a clock slider steps the slots; each unit row draws from the map unit of the same name (1st Sqd 1st FT, or the squad when the fire team is not placed; Left gun, Right gun; PC or the CP); a party away appears at its target (a buddy pair at the object named MACO or gate, the OP triangle at the LP/OP, fire team frames out along the route named patrol, one dot for a leader at the terrain model or the CP) and the unit's badge counts down. `t2t_reader.py` is the page's own reader in Python (the page's `t2t.js` is the reference): it reads a Unit column, X columns with a Clock row, one row per unit with its strength in parentheses, Milestones and Security rows; in a cell only the planner's shorthand, "2 sec, 2 dig: task", "(2 on MACO)", a row name's "(2 on LP/OP 0030 to 0900)" as a standing pair between those times, DAY, NIGHT or FT PATROL and "Leads ... patrol" as the whole row out, STAND TO, and on a leader's row "terrain model", "brief", "debrief", "planning". A blank cell continues the last entry. Nothing else is inferred: a cell the reader does not understand is carried as text and drawn as nobody away. With `--rehearsal` it also writes one phase per milestone and one event per slot with a change, so Rehearse plays the matrix and the clock follows. The user can paste the same block from Excel straight into the page (Plan, Troop to task) without this tool; the tool is for the file that carries the base order and the matrix together, and for the report.

## Rules

- **The order is the only source.** Every value in facts.json names its paragraph. A value with no paragraph is refused by the writer.
- **Everything higher placed is on the map.** A grid in the order is a symbol on the table the moment the file opens, labeled with the order's own name for it and carrying its paragraph in the remarks. A described location with no grid is placed only when the sheet can fix it (a named hill, a distance from a named feature) and is labeled derived.
- **Higher's half only.** The planner's decisions (EMLCOA, CG/CV, engagement area and trigger lines, battle position, distribution, orientation, occupation, security, obstacles, the offense scheme, parts, squad tasks, targets, FPF, engagement criteria, CCP and CASEVAC route) stay blank even when the order carries higher's version of them; higher's EMLCOA goes to the enemy step's "Higher's EMLCOA" field, higher's intent to the mission step's "Higher" field, and the planner writes their own on the page. The checker fails an intake file that fills them.
- **Grids as written.** A 6 digit grid stays 6 digits; the page places it at the center of its 100 m square and the planner refines it. Never extend a grid.
- **Their words.** Mission, intent, tasks and EMLCOA verbatim. Orientation and logistics may be condensed, keeping every number, name and time. No doctrine, no example values.
- **Left and right are not decided by the order** unless it says so; when it does not, the src line says "confirm" and the planner settles it on the page.
- Plain numbering. No dashes in values (kit standard 9); an em or en dash in the order is written as a comma or a word.

## Scripts

- `scripts/order_text.py`: a .docx or .pptx order to text with its paragraph numbers.
- `scripts/plan_writer.py`: facts.json to the plan file and sourced.md, refusing anything the page's guide does not have a field for.
- `scripts/plan_check.py`: the plan file against the page's shape and the intake rules.
- `scripts/t2t_reader.py`: a troop to task matrix (xlsx with --sheet, or csv) into plan["t2t"] of a new or existing plan file, with --rehearsal the phases and events, and a .t2t.md report (rows, what the page looks for, the security count per slot beside the planner's own row).
- `references/guide_fields.json`: every step and field of the page's guided build, extracted from the page's own source; when the page changes, this file is regenerated with it.

## What it does not do

It does not plan, and it does not analyze the order (`order-analysis` does that: contradictions, RFIs, the resourcing bound). It carries higher's paragraphs to the sand table so the planner's time on the page is spent on the decisions that are theirs.
