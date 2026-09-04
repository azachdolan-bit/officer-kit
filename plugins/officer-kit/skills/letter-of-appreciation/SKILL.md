---
name: letter-of-appreciation
description: >
  Writes a letter of appreciation for a Marine, Sailor, civilian, or supporting unit from the
  facts of what they did: the event and its dates, what it accomplished and for how many, the
  specific role that made it possible, and the thanks, in naval letter format on one page, then
  checks it. Use when the user says "letter of appreciation for", "LOA for", "thank you letter
  to the unit that", "recognize the Marines who", or wants to put a good deed into someone's
  record short of an award.
metadata:
  version: "0.1.0"
---

# Letter of appreciation

A letter of appreciation is the lightest recognition that goes into a record, and it is often the right one: the awards order says routine service is not an award, and a letter from someone senior enough says thank you in a way the Marine keeps. It is three paragraphs and one page, and the whole craft is naming the event, the number, and the role.

## Read first

1. `references/exemplar.md`: one fictional letter, annotated, and the intake beneath it.
2. Format: the `naval-letter` skill's `references/standard.md`; render with its `scripts/build_letter.py`. A letter to a civilian or an outside organization can use business letter format instead; ask.

## Workflow

```
Letter of appreciation:
- [ ] 1. Who is thanked (grade, name, unit; or the unit itself), who signs, and whether it goes in a record (then it is addressed to the individual via their CO)
- [ ] 2. The event: what, where, when (dates)
- [ ] 3. What it did and for how many: the count, the outcome, who benefited
- [ ] 4. The role: the specific thing this person did that made it possible
- [ ] 5. Draft as letter.json, three paragraphs plus POC if the signer wants one
- [ ] 6. python3 scripts/loa_check.py letter.json exits 0
- [ ] 7. Rendered; one page; saved to Admin/Letters/<label> LOA <date>/
```

## The three paragraphs

1. The event and the thanks: "On <dates>, you <did what> in support of <what>." Thanks stated once, plainly.
2. What it accomplished and for whom: the number of Marines, the outcome, the effect on the unit or program.
3. The specific role, and the close: the one thing this person did (range safety officer for two days; sourced the classroom; taught the block), and a line about what it means for the command. Signed by the senior.

## Rules

- One event per letter. A period of service is a fitness report or an award, not a letter of appreciation.
- Every letter carries at least one date and one count. "Your hard work" without either is not a letter of appreciation; it is a note.
- No word on the strike list. "Sincere" and "sincerest" are allowed once; they are what the letter is for.
- Nothing about the person beyond the event. No personal, medical, or family detail.
- If the user describes something that reaches a Certificate of Commendation or an Achievement Medal, say so once and offer the `award` tool; then write the letter if that is what they want.

## Utility script

- `scripts/loa_check.py letter.json`: three paragraphs (a fourth allowed for POC); a date and a count present; a thanks sentence; the role sentence names an act (a verb from the fact list); strike list words (warn); blocked content (fail); under one page. Exit 1 on structural or blocked content failure.
