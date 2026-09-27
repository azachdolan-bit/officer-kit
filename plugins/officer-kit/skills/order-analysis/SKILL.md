---
name: order-analysis
description: >
  Analyzes an order the user received: the resourcing that bounds the plan, a hasty METT-T worksheet
  where every fact carries its paragraph, the order's own column abbreviations decoded before any
  sequence is judged, every grid, distance, and bearing computed in code with its error budget,
  contradictions inside the order quoted from both ends, and the RFIs for higher. Use when the user
  says "analyze this order", "METT-T this order", "METT-TC", "find the contradictions", "check the
  grids", "what do I need to ask the PC", or attaches an operations order, warning order, or frag.
metadata:
  version: "0.1.0"
---

# Order analysis

The order is the higher commander's words; the analysis is what a subordinate leader needs to know about them before planning: what the order gives, what it asks, where it says two things at once, and what to ask. Its failure modes are specific. A finding built on a misread column, a bearing converted by hand, a distance inside the grid's own error, a weapon range from general knowledge, or a plan that spends assets the order never gave. Every one of those has happened in a real review, and each has a mechanism here. This tool analyzes a received order; `order-critique` reviews one the user wrote.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Your own material (read first, every time)

1. `Overrides/order-analysis.md`: the user's school or unit way wins (their factor set, their parts format, their priorities).
2. The user's school or unit order format and planning material in Reference, then `references/order-format.md`. Any weapon range, planning factor, or definition comes from the user's own captures and publications, library first (kit standard 5), never from general knowledge.
3. Training orders from a school exercise are green. An order about a real operation, real unit locations, or carrying a marking is red: stop and point to `security-check`.

## Before you draft

1. **Assume it already failed** and write three reasons first; the usual ones are a sequence finding from an undecoded column, a number computed by hand, and a finding that is really a doctrine preference.
2. **Ask only what changes the product:** the user's billet in the order (it decides whose tasks and RFIs matter), whether they want contradictions only or the full worksheet, and whether a map is in hand.
3. **Say what you assumed.** An order that does not say something is an RFI, never a fact.

## Workflow

```
Order analysis:
- [ ] 1. Capture the order to text (capture-source); keep its paragraph numbers
- [ ] 2. Resourcing first: paragraph 1.C and paragraph 4, quoted. It bounds the plan and the findings (references/not-a-defect.md, item 9)
- [ ] 3. Legend: decode every column abbreviation and school term the order uses, from the order or the user's material, before judging any sequence. If neither decodes it, it is an RFI and no sequence finding goes out
- [ ] 4. Facts: the METT-T (or the user's set) worksheet, each fact with its paragraph and a verbatim quote; gaps become RFIs
- [ ] 5. Grids: python3 scripts/grid_tool.py extract <order.txt>; the same point with two grids is a candidate; measure every distance and bearing that matters with grid_tool.py measure; a map is fitted with scripts/map_calibrate.py before anything is measured on it
- [ ] 6. Candidates, in passes: (a) the same thing said two ways (grids, names, attachments, titles, locations); (b) tasks against end states: can the tasks, done as written, produce each part's Ends With, Conditions Set, and the commander's end state; (c) contingency plans against the mission (a no comm, lost Marine, or CASEVAC plan that abandons the task); (d) geometry, from grid_tool; (e) sequence, only after the legend; (f) omissions, as RFIs. Map against order and doctrine comparisons only when the user asks, in their own section
- [ ] 7. Check each candidate against references/not-a-defect.md
- [ ] 8. Write analysis.json (references/analysis-spec.md); python3 scripts/analysis_check.py analysis.json order.txt exits 0
- [ ] 9. Gate 0 significance-reviewer, then Gate 1 evidence-reviewer, blind, with the findings and the order; record both verdicts in each finding; rerun the checker
- [ ] 10. Report: facts, findings (plain numbers, both ends quoted, consequence), RFIs; save the report, analysis.json, and the gate report together
```

## Rules

- **Both ends, in the order's words.** A contradiction names both passages by paragraph and quotes each; the consequence says what a subordinate would do wrong. If the finding cannot be quoted from both ends, it is not a contradiction.
- **Numbers from code.** Every distance, bearing, and conversion comes from `grid_tool.py`, with the error budget stated. The circle is 6400 mils; northwest is 5600.
- **The table governs the narrative** when a control measure table and an "approximately" paragraph disagree; plot from the table and ask.
- **Bound by the order's resourcing.** Do not plan with, or fault the order for lacking, assets it does not give.
- **A subordinate asks; they do not fix.** The output is RFIs to higher, not a rewritten order, unless the user asks for a draft.
- Plain numbering, 1 through N.

## Scripts

- `scripts/grid_tool.py`: extract grids, measure distance and bearing with the error budget, convert direction words and mils.
- `scripts/map_calibrate.py`: fit a map scan from control points and report whether it is square enough to measure.
- `scripts/analysis_check.py`: the analysis against the order: verbatim quotes, recomputed numbers, the legend, recorded gates.
