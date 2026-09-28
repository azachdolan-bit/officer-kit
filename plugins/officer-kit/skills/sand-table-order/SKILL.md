---
name: sand-table-order
description: >
  Writes a five paragraph order from a virtual sand table export: the .sandtable.json plan file (every guided step
  the planner filled, everything placed and drawn on the map with grids, sectors of fire, routes, parts and events)
  and the .sandtable-brief.md (the same plan as text with the sand table's checks and magnetic azimuths). Every fact
  is read by script, every grid derived from the map, nothing invented; what the plan does not hold is listed as
  NOT IN THE PLAN, and every warning the sand table raised is carried. Use when the user attaches a .sandtable.json
  or .sandtable-brief.md, or says "write my order from the sand table", "build the order from this plan file",
  "sand table export", "order package", "turn my plan into an order".
metadata:
  version: "0.2.0"
---

# Sand table order

The planner did the tactical work on the sand table: METT-TC, EMLCOA, the engagement area or the objective, the positions, the routes, the fires, the parts. This tool turns that export into the order they will brief, in their own format, with nothing added. Its failure modes are specific: a grid retyped wrong, a placed position left out, a paragraph filled from doctrine instead of the plan, a warning the sand table raised written over. Each has a mechanism here. `order-critique` reviews an order the user wrote; `order-analysis` analyzes one they received; this one writes from a plan they built. `sand-table-intake` is the other half of the loop: it turns the base order into the file the sand table starts from, so the export this tool reads carries higher's paragraphs with their sources and the planner's decisions from the page.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Your own material (read first, every time)

1. `Overrides/sand-table-order.md`: the user's school or unit way wins.
2. The user's order format and drafting guidance from their Reference or planning folder (a skeleton, a drafting playbook, a parts based execution table, a fire support matrix). The order is written to that format. With none on disk, the platoon format in `references/order-map.md` (MCRP 3-10A.3 Appendix J) applies, and the reply says so.
3. Training plans from a school exercise are green. A plan about a real operation, real unit locations, or carrying a marking is red: stop and point to `security-check`.

## Before you draft

1. **Assume it already failed** and write three reasons first; the usual ones are a paragraph filled from doctrine because the plan was silent, a grid retyped by hand, and a position on the map that never reached the order.
2. **Ask only what changes the product:** the user's own format if none is on disk, and whether they want the whole order or one paragraph. Do not ask for anything the export already holds.
3. **Say what you assumed.** The plan is the only source. A paragraph element the plan does not hold is written as NOT IN THE PLAN, never filled.

## Workflow

```
Sand table order:
- [ ] 1. Save the attached files beside the product (kit standard 1); read references/plan-format.md once. An order package zip from the page (Plan, Export order package) holds everything at once: README.txt, the plan file, the brief, the fire plan sketch PNG, the view PNG and one range card PNG per gun; unzip it beside the product and use the plan file and brief below, the PNGs as the annexes
- [ ] 2. python3 scripts/plan_reader.py <plan.sandtable.json> [<plan.sandtable-brief.md>] --json facts.json --md facts.md; read facts.md end to end. It carries every field, every typed but unapplied line, every object with its grid and sector, the direct fire plan (every position's limits, FPL and PDF in grid and magnetic azimuth with mils, and the TRPs inside each sector with range and azimuth), every route with computed legs, the parts, and the brief's checks
- [ ] 3. Operation type from facts (platoon defense, platoon offense, squad offense) decides the scheme of maneuver shape: defense in the user's defense format (TDOOTS where their school uses it) with the engagement area first; offense as type of attack, form of maneuver, task organization, control measures, sequence and signals; then the parts as the planner wrote them
- [ ] 4. Write the order to the user's format, paragraph by paragraph from references/order-map.md, copying grids from facts.md (never retyped from memory), every route with its legs, the direct fire plan in the scheme of maneuver (each position's limits, each gun's FPL or PDF, the azimuths as facts.md gives them), every task in its four elements, every warn check verbatim under "Warnings carried", every missing element under "NOT IN THE PLAN". The annexes come from the order package zip, or one at a time from the page (Plan, Fire plan sketch; Objects, Range card); ask for them when the user attached the plan file alone; save them beside the order and name them in the scheme of maneuver. Grazing fire and dead space are on those cards, not in the file: never state them from the file
- [ ] 5. python3 scripts/order_check.py order.md facts.json exits 0 (every grid in the order is in the plan; every object, route, part and field in the plan is in the order or listed as not in the plan; every sector limit, FPL and PDF azimuth in the order; warnings carried; the five headings; no dashes). Fix and rerun until clean
- [ ] 6. red-team agent, blind, with the order, the user's format, and facts.md as the source
- [ ] 7. Save the order, facts.md and the checker's output together; name the path
```

## Rules

- **The plan is the only source.** No unit name, grid, time, frequency, number, task, or phrase comes from anywhere else. Where the plan is silent the paragraph heading stands with "NOT IN THE PLAN: <what is missing>".
- **Grids from the reader.** Every grid in the order is copied from facts.md, which derives it from the map in code. Distances and azimuths likewise: grid azimuths from the reader, magnetic only when the brief gives them.
- **Everything on the map appears.** Every placed position, control measure, sector of fire, FPL or PDF, obstacle and route is in the scheme of maneuver with its grid, and every route leg with its distance and azimuth. The direct fire plan reads from the reader's table: grid azimuths in the order, magnetic beside them where the user's format wants magnetic (the reader converts with the sheet's declination and gives mils).
- **The sketch and the cards are annexes, not paragraphs.** The fire plan sketch and each gun's range card come from the page as PNG files (B3M0830XQ-DM Annex D; MCTP 3-01C pp. 4-23 to 4-28) and ride beside the order; the order names them and copies no grazing or dead space figure from anywhere but those cards.
- **Typed but not applied is still theirs.** Lines the planner typed and never applied are used and marked "(typed, not applied)" so they can confirm them.
- **Warnings carried, never buried.** Every warn check the sand table raised is quoted under "Warnings carried" at the end, so the planner fixes the plan rather than briefs around it.
- Plain, direct order language: short sentences, the planner's own task verbs, no filler. Plain numbering in the two closing lists.

## Scripts

- `scripts/plan_reader.py`: the export to facts.json and facts.md: fields, typed lines, objects with 8 digit grids from UTM, sectors, the direct fire plan (limits, FPL and PDF in grid and magnetic with mils; TRPs per sector), routes with computed legs, parts, the brief's checks.
- `scripts/order_check.py`: the drafted order against facts.json: grids, coverage, direct fire azimuths, warnings, headings, the NOT IN THE PLAN list, dashes.

## What it does not do

It does not plan. A position the planner never placed, a target never planned, a task never written stays out of the order and goes on the NOT IN THE PLAN list. The sand table's own checks (frontage, ranges, line of sight, sector geometry) are the planner's to act on; the order carries the warnings and changes nothing.
