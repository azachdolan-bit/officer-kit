---
name: fitrep
description: >
  Drafts the narrative sections of a Marine Corps fitness report from the reporting senior's
  notes to MCO 1610.7B: Section B billet description, Section C billet accomplishments, and
  Section I mandatory, directed, and additional comments, then checks the draft against the
  manual's style rules, the unacceptable comments list, and the directed comment triggers. Use
  when the user says "draft a fitrep", "fitrep on", "section I for", "billet description for",
  "section C bullets", "write up this Marine's report", "MROW", or pastes counseling notes and
  asks for a fitness report. Works for reporting seniors writing on their Marines and for a
  Marine drafting input for their own report.
metadata:
  version: "0.1.0"
---

# Fitness report

Sections B, C, and I are the words a board reads. The manual is specific about what they may and may not say, and an RS who violates it either gets the report returned or, worse, harms the Marine without meaning to. Read `references/pes-manual-extract.md` before the first draft of a session; it carries the manual's own words for Sections B, C, I, and the directed comment list.

Attribute marks (Sections D through H) are the RS's judgment and are never proposed by this tool. If the user wants to see how marks land against their profile, that is `rs-profile`.

## Inputs

- **Who and what.** The MRO's grade and billet, the reporting occasion and period, and whether the user is the RS or the MRO preparing input. When the user is the MRO, the billet description comes from the "My billet, in my words" section of their rules file; read it and confirm it rather than asking again.
- **The notes.** Counseling notes, the MROW, unit input, the RS's bullets. Anything the RS actually observed. Nothing is invented; a thin set of notes produces a short section, and the draft says so.
- **Section A facts that trigger directed comments**: occasion code, period length, duty assignment count, special case marks, commendatory or derogatory material, promotion recommendation, PFT/CFT codes, body composition, reserve status, grade relationships between RS, RO, and MRO. Ask for these once as a checklist; each "yes" produces a directed comment.
- **The user's copy of the manual** in Reference, if present, for the current edition. The extract is from the 5 Jun 2023 edition.

## Your own material (read first, every time)

1. `Overrides/fitrep.md` in the working folder, if it exists: the command's way wins over the defaults below. Say in one line what it changed.
2. `Reference/Exemplars/fitrep/` in the working folder, if it has files: the user's own command's approved patterns beat the plugin's fictional exemplars.
3. The label. Another Marine's name never enters the session. Work on `<MARINE>` (grade and billet stay); the user runs `security-check/scripts/substitute.py` on the finished file on their own computer. If the rules file records a working label, use that instead.
4. When something comes back with edits, or a board answers differently than expected, tell the user `aar` will capture it.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

Quarantine the outcome: assemble the observed facts and read the manual's rules before any mark or comment is considered, then compare.

## Workflow

```
Fitrep draft:
- [ ] 1. Grade, billet, occasion, period, role of the user recorded
- [ ] 2. Notes read; each accomplishment tagged as B (duty), C (result), or I (character, potential)
- [ ] 3. Section A checklist asked; directed comments required listed
- [ ] 4. Section B drafted: bulleted duties, standards not goals, no superlatives
- [ ] 5. Section C drafted: bulleted results only, no personal qualities, no awards
- [ ] 6. Section I drafted: mandatory word picture first, then each directed comment in the required form, then additional comments
- [ ] 7. python3 scripts/fitrep_check.py draft.md exits 0
- [ ] 8. Draft saved to Admin/Fitreps/<MRO label> <occasion> <date>.md; user reads it against the manual's Section I style rules
```

**Section B.** Bullets, each preceded by a dash. The nature of the billet and the MRO's significant responsibilities as they relate to the unit's mission. Standards, not goals. Not a restatement of MOS prerequisites. No superlative adjectives, needless statistics, imprecise phrasing, uppercase, quotation marks, bold, italics, or exclamation. Space limited; no addendum.

**Section C.** Bullets, each preceded by a dash. What the MRO accomplished: results and achievements only. Objective, not qualitative. No personal qualities, no potential, no awards, no commendatory or adverse material, no board or court-martial membership. Short and direct, in words most Marines understand; avoid community specific acronyms. Space limited; no addendum.

**Section I.** In this order:

1. **Mandatory comments** (the word picture): performance, proficiency, potential, and other traits of the whole Marine that the marks do not show. Address any conflict inside the report or the profile that a board member would not see. Consistent with the marks; neither conflicting with nor obscuring them. Not gratuitous.
2. **Directed comments**, one per trigger, each beginning exactly `Directed Comment. Sect A, Item Na:` followed by the manual's required statement where it prescribes one (promotion recommendation statements, body composition statements, "Simultaneous report" as the opening when the MRO holds multiple duty assignments).
3. **Additional comments**: character outside the billet, community involvement, volunteer work. Within the space provided unless directed comments push the total over, in which case an addendum page is used.

Style for every section: objective, concise, clear in intent; normal capitalization; no superlatives; limited pronouns.

**Unacceptable in Section I** (the manual's list, checked mechanically): pending NJP, courts martial, civil or criminal action, boards, or investigations; suspected criminal activity; administrative reduction or separation proceedings; non punitive letters; voluntary alcohol treatment not affecting duty; minor traffic violations; prior non selection; the spouse; gender based comments; medical matters not affecting duty; personal or family problems not affecting duty; single parent status; civilian employment potential; minor shortcomings in an otherwise positive report; merit reorder; "briefed as a" recommendations.

## Rules

- Never propose attribute marks. Never write to a profile.
- Never include anything from the unacceptable list, even if the notes contain it. Say what was left out and why, citing the paragraph.
- Never invent an accomplishment, a number, or a date. Thin notes produce a short section and a note to the user.
- Never write a laudatory Section I over low marks or the reverse; if the notes and the intended marks disagree, say so before drafting.
- Adverse reports follow Chapter 5, which this tool does not carry. If any Section A item makes the report adverse (promotion "No", derogatory material, a failed PFT/CFT event, U or X qualification with negligence), stop and tell the user to work from Chapter 5 with their copy of the manual.
- Other people's personal data stays out of the saved draft beyond what the report itself requires.

## Utility script

- `scripts/fitrep_check.py draft.md`: checks the draft's B, C, and I sections for prohibited formatting, superlatives, the unacceptable comment list, gender pronoun density, directed comment form, bullet marks, and reports character counts per section. Exit 1 on a prohibited item.

Draft file format the checker expects:

```
## Section B
- bullet
## Section C
- bullet
## Section I
Mandatory comments paragraph...
Directed Comment. Sect A, Item 7: I recommend that the MRO be considered for promotion ahead of contemporaries.
Additional: ...
```
