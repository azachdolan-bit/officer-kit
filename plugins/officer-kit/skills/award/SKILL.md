---
name: award
description: >
  Builds a personal award recommendation the way a good XO does it: an intake that quantifies
  what the Marine actually did, a level check against the awards manual's criteria, a Summary of
  Action and citation that say exactly that and nothing more, and a mechanical check that the
  citation carries no number or claim the SOA does not prove. Use when the user says "write up
  an award", "NAM for", "NAVCOM", "MSM", "summary of action", "citation for", "impact award",
  "end of tour award", "certificate of commendation", or pastes bullets about a Marine and asks
  for an award.
metadata:
  version: "0.2.0"
---

# Award

An award package is two documents that must agree: a Summary of Action that proves the case in the recommender's words, and a citation in the manual's form that a general officer will sign. The processing order says the SOA is what gets the award approved, and that quality and level of responsibility, not the Marine's grade, set the level.

The tool's job is three correlations, in order: what the Marine did, quantified; whether that reaches the manual's criteria for the level requested; and whether the write up says exactly that. Fluff is a failure, not a style. An accurate, professional page that reaches a lower level is a success; an inflated page is not.

## Read first

1. `references/mco-1650-19j-extract.md`: the Marine Corps processing order, verbatim. SOA length and format by award, citation format, criteria guide, the level of award rule.
2. The user's copy of SECNAV M-1650.1 (Navy and Marine Corps Awards Manual) in Reference: chapter 2 criteria for the award requested; Appendix 2E tables 20 and 21 for the citation format and the standard opening and closing sentences. The plugin does not carry the manual's text. If it is not in Reference, say so, use the extract, and mark the standard sentences "verify against SECNAV M-1650.1 Appendix 2E."
3. `references/intake.md`: the questions, in order, and the quantification ladder.
4. `references/voice.md`: standard sentences as approved citations use them, fact verbs, the strike list, professionalism rules.
5. `references/exemplars.md`: four fictional exemplars, three strong and one weak annotated line by line. Read before drafting; never copy text from them.

## Your own material (read first, every time)

1. `Overrides/award.md` in the working folder, if it exists: the command's way wins over the defaults below. Say in one line what it changed.
2. `Reference/Exemplars/award/` in the working folder, if it has files: the user's own command's approved patterns beat the plugin's fictional exemplars.
3. The label. Another Marine's name never enters the session. Work on `<MARINE>` (grade and billet stay); the user runs `security-check/scripts/substitute.py` on the finished file on their own computer. If the rules file records a working label, use that instead.
4. When something comes back with edits, or a board answers differently than expected, tell the user `aar` will capture it.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

Quarantine the requested level: weigh the facts against the criteria before the requested level is in view, then compare the two and say where they differ.

## Workflow

```
Award package:
- [ ] 1. Frame: award, approver, type (specific achievement, sustained, impact, transfer, end of tour), billet, dates, above grade or not
- [ ] 2. Intake: questions 4 to 10 from intake.md, one at a time; "I do not know" is recorded as a gap, never filled
- [ ] 3. Climb the ladder on every vague note (action, scope, result, comparison, consequence); stop where the recommender can defend
- [ ] 4. Level check: hold the facts against the manual's criteria; say reaches, reaches a lower level (quote the criterion), or does not reach a decoration
- [ ] 5. Read back the fact list (item, number, period, source); user confirms; nothing outside the list goes in
- [ ] 6. Reader profile: ask once how the approval authority reads these; record in Admin/Awards/reader-profile.md
- [ ] 7. SOA drafted in the command's form (bullets or paragraphs) within the order's length for the level
- [ ] 8. Citation drafted: standard opening and closing, two to four fact sentences between, each with a number
- [ ] 9. python3 scripts/citation_check.py Citation.txt --level NA --soa SOA.md exits 0
- [ ] 10. Strike pass with voice.md: delete every word on the strike list; if the sentence lost no fact, it stays deleted
- [ ] 11. Saved to Admin/Awards/<Marine label> <award> <date>/ as SOA.md and Citation.txt; the user reads both against the manual
- [ ] 12. Learning: if the board's answer differs from the level check, or the approver struck something, record it in LEARNINGS.md
```

## The SOA

Lead with the single most consequential achievement (intake question 4). Every bullet or paragraph states what the Marine did, the scope (how many, how large, over what period), and the result for the unit, with a source a reader could ask for. Numbers the recommender can defend; none the recommender cannot. Billet above grade is stated once, in the first paragraph. Volunteer work is one paragraph, never the lead.

Format: the 2001 order says NA in bullets on one page, NC bullets or paragraphs on two, MM paragraphs on three. Commands routinely approve NA and NC summaries written in paragraphs. Ask which the command uses, draft that, and state the order's rule once. Say when a draft exceeds the order's length; do not fail it.

## The citation

Opening sentence from the manual's table for the award and type (observed forms in voice.md), two to four sentences of the strongest facts in order of significance with the SOA's numbers unchanged, then the standard closing. All capitals, Times New Roman 10, landscape, fully justified, one inch margins, 8 lines, 1,250 characters, no acronyms for NA and NC (SECNAV M-1650.1 Appendix 2E Table 20 as carried by current subordinate instructions; the 2001 processing order's 9 lines and 9 point are superseded); MM regular capitalization, 12 point, 24 lines. No abbreviations a reader outside the unit would not know. One claim per sentence, no semicolons.

## The level check (step 4)

Read the criteria for the level from the user's manual and the extract's criteria guide. Say one of three things: the facts reach the level as the manual describes it; the facts reach a lower level, naming it and quoting the criterion that separates them, with an offer to write to that level or keep the request with the gap stated; or the facts do not reach a personal decoration, with an offer of a Certificate of Commendation or a letter of appreciation. The tool never predicts a board. Boards downgrade well argued packages; the page's job is to make the scope unmistakable so the argument is there to weigh.

## Rules

- Never inflate. Never invent a number, a date, a result, or a comparison. A sentence that stops at scope is honest; one that invents a comparison is not.
- The citation carries nothing the SOA does not prove, and the checker enforces the numbers.
- Routine end of tour recommendations "have no place in the awards system" per the order. If that is all the notes show, say so and ask what specifically distinguished the service.
- NA is limited to O-4 and below and cannot recognize valor. Valor and combat awards are outside this tool; say so and stop.
- Other people's personal data stays out of the saved files beyond the Marine's grade and name as they will print. No SSN, EDIPI, medical, financial, or family detail.
- The recommender's judgment beats the tool's. When they choose to keep a request the facts argue against, draft it accurately and note the gap in the fact list, not in the SOA.

## Utility script

- `scripts/citation_check.py Citation.txt --level NA|NC|MM [--soa SOA.md]`: character and line count for the level, capitalization, opening and closing sentences, abbreviations, semicolons, strike list words, a number after the opening; with `--soa`, fails if any number in the citation is absent from the SOA. Exit 1 on a limit, capitalization, or agreement failure.
