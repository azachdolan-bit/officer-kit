---
name: award
description: >
  Drafts a personal award recommendation from the recommender's notes: the Summary of Action
  in the length and format the Marine Corps awards order requires for the award level, and the
  citation in the Navy and Marine Corps Awards Manual's standard form, then checks both
  mechanically (length, format, capitalization, opening and closing sentences) and asks whether
  the facts justify the level requested. Use when the user says "write up an award", "NAM for",
  "NAVCOM", "MSM", "summary of action", "citation for", "impact award", "end of tour award",
  "certificate of commendation", or pastes bullets about a Marine and asks for an award.
metadata:
  version: "0.1.0"
---

# Award

An award package is two documents that must agree: a Summary of Action that proves the case in the recommender's words, and a citation in the manual's form that a general officer will sign. The processing order says the SOA is what gets the award approved, and that quality and level of responsibility, not the Marine's grade, set the level of the award.

Two authorities, read in this order:

1. `references/mco-1650-19j-extract.md`: the Marine Corps processing order, verbatim. SOA length and format by award, citation format, the criteria guide, the level of award rule.
2. The user's copy of SECNAV M-1650.1 (Navy and Marine Corps Awards Manual) in Reference: chapter 2 criteria for the award requested, and Appendix 2E tables 20 and 21 for the combination citation and certificate format and the standard opening and closing sentences. The plugin does not carry the manual's text; read the tables from the user's copy at draft time. If it is not in Reference, say so, use the format rules in the extract, and mark the opening and closing sentences as "verify against SECNAV M-1650.1 Appendix 2E."

## Inputs

- **The Marine**: grade, name as it will print, billet, unit, period of the action, and whether this is a specific achievement, sustained superior performance, an impact award, or an end of tour recommendation. The order says routine end of tour awards "have no place in the awards system"; if that is what the notes describe, say so and ask what specifically distinguished the service.
- **The level requested**: NA (Achievement), NC (Commendation), MM (Meritorious Service), or a Certificate of Commendation. NA is limited to O-4 and below and cannot recognize valor or non combat heroism.
- **The notes**: what the Marine did, with results, scope, numbers, and dates the recommender can stand behind. Nothing is invented; a thin set of notes produces a thin SOA and a note saying so.
- **Approval chain**: who originates and who approves, if known, for the routing line.

## Workflow

```
Award package:
- [ ] 1. Level, type, period, and the Marine's line recorded; end of tour flagged if that is all the notes show
- [ ] 2. Notes sorted into achievements with results; each tied to a date or period
- [ ] 3. Level check: do the facts meet the criteria for the level requested (extract paragraph 5, manual chapter 2)? Say so either way; propose the level the facts support
- [ ] 4. SOA drafted in the required format and length (NA: bullets, one page; NC: bullets or paragraphs, two pages; MM: paragraphs, three pages)
- [ ] 5. Citation drafted: NA and NC all capitals, Times New Roman 9, landscape, nine lines, 1200 characters; MM regular capitalization, 12 point, portrait, 24 lines; opening and closing sentences from the manual's tables
- [ ] 6. python3 scripts/citation_check.py citation.txt --level NA exits 0; SOA page estimate within limit
- [ ] 7. Saved to Admin/Awards/<Marine label> <award> <date>/ as SOA.md and Citation.txt; the user reads both against their copy of the manual
```

**The SOA.** Lead with the single most significant achievement. Every bullet or paragraph states what the Marine did, the scope (how many, how large, over what period), and the result for the unit or the Marine Corps. Numbers the recommender can defend; none the recommender cannot. No adjectives doing the work of facts. For NA and NC, brevity is encouraged by the order itself.

**The citation.** The manual's standard opening sentence for the award and type ("For professional achievement in the superior performance of his duties while serving as..." is the common NA opening; take the exact wording from Table 21 in the user's copy), then two to four sentences of the strongest specific facts, then the standard closing ("...reflected great credit upon him and were in keeping with the highest traditions of the Marine Corps and the United States Naval Service" is the common form; take it from the table). No abbreviations a general officer's reader would not know. Every fact in the citation appears in the SOA.

## Rules

- Never inflate the level. If the notes support an NA and the user asks for an NC, say what the manual's criteria require and what is missing.
- Never invent a number, a date, or a result. Ask.
- The citation carries nothing the SOA does not prove.
- Other people's personal data stays out of the saved files beyond the Marine's name and grade as they will print. No SSN, EDIPI, or medical detail.
- The order's two character limits for the NA and NC citation (1200 and 1250) are both in the extract; the check uses 1200.
- Valor and combat awards are outside this tool; they carry different SOA requirements and routing. Say so and stop.

## Utility script

- `scripts/citation_check.py citation.txt --level NA|NC|MM`: character and line count against the limit for the level, capitalization rule, presence of an opening and a closing sentence, abbreviations, and the Marine's grade and name on the first line. Exit 1 on a limit or capitalization failure.
