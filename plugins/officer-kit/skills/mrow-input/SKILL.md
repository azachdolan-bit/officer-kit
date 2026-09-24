---
name: mrow-input
description: >
  Prepares the Marine Reported On Worksheet (MROW) input an officer or SNCO submits for their own
  fitness report, to MCO 1610.7B: the billet description as the MRO drafts it for the reporting
  senior (duty, scope, the standard the RS set, in bullets) and the billet accomplishments in
  section C form (what was done, in numbers, against what baseline), with awards and PME listed
  separately for the RS because the order keeps them out of section C. Reads the billet from the
  user's rules file, climbs the ladder on each accomplishment, and refuses what the order forbids
  in section C: personal qualities, potential, awards, adverse or disciplinary material, selection
  board or court-martial membership, and any line about the marks. Use when the user says "MROW",
  "my MROW input", "worksheet for my fitrep", "billet accomplishments for my report", "summary of
  accomplishments", "what do I give my RS", "draft my billet description", or wants to prepare
  input for a report written on them.
metadata:
  version: "0.1.0"
---

# MROW input

The order puts the first move in the evaluation cycle on the Marine being reported on: "Prior to the end of the reporting period, the MRO shall provide a summary of accomplishments to the RS. The CMC directs the use of the MRO Worksheet (MROW) for billet description and summary of accomplishments documentation" (chapter 1 paragraph 6.b). The RS then decides what of it the report carries: the RS must "Assess the information provided by the MRO on the MROW and report that information on the MRO's fitness report as deemed appropriate" (chapter 2 paragraph 3.c(3)). So the MROW is input, not a report: it wins or loses on whether the RS can verify each line and lift it into section B or C with the fewest edits. This tool writes that input in the form the order gives those two sections (chapter 4 paragraphs 5 and 6), keeps out what the order keeps out of section C, and puts awards and PME where the order sends them, in a list for the RS. It prepares; the RS writes the report, marks it, and signs it. The A-PES screen's own field layout and any field length it enforces are not in the order and are unverified; the user reads them off the screen.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Read first

1. `references/standard.md`: chapter 1 paragraphs 6 and 7 (who starts the MROW, when, what it carries), chapter 2 paragraph 3 (what the RS does with it), chapter 4 paragraph 3 (unique billets), 4.f(1) (what counts as commendatory material), 5 (section B), 6 (section C, with the forbidden list gathered), 13.d (unacceptable comments), 17 (classified duties), and the note that the order fixes no length limit.
2. `references/intake.md`: the questions, one at a time.
3. `references/voice.md`: the order's words for each section, the bullet shapes, the strike list.
4. `references/exemplar.md`: read only after the fact list is confirmed (step 6). It teaches shape and its content is not to be taken; the checker fails a lifted phrase.

## Your own material (read first, every time)

1. The rules file (`CLAUDE.md` at the top of the working folder): the "My billet, in my words" section, or whatever the user's rules file calls the billet line. That is the billet as the RS and the MRO formalized it; read it and confirm it rather than asking again. If the rules file has no billet, ask for it and offer to record it there.
2. `Overrides/mrow-input.md`: how this RS wants the worksheet written, the A-PES field length read off the screen, the order of duties on the counseling sheet. The command's way wins; say in one line what it changed.
3. `Reference/Exemplars/mrow-input/`: worksheets this RS accepted, sanitized. They beat the plugin's fictional exemplar.
4. `<MARINE>` or "the MRO" throughout, and every other Marine by billet; the name goes on the A-PES screen from the user's own computer. Nothing adverse, medical, family, or financial about anyone enters the session; if it bears on the period, the MRO tells the RS in person.
5. When the report comes back and the RS kept, cut, or rewrote lines, `aar` captures which and why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

## Workflow

```
MROW input:
- [ ] 1. Frame: occasion code, period From and To as dates, grade, the billet from the rules file confirmed, RS and RO by billet, any unique billet duty (chapter 4 paragraph 3)
- [ ] 2. Billet description: primary duties as the RS assigned them, additional and special duties with the date assigned, scope as counts, the standard the RS set; nothing that restates the MOS
- [ ] 3. Changes during the period: what was added or dropped, when, and whether the RS discussed it (paragraph 5.d)
- [ ] 4. Accomplishments, one at a time: climb the ladder (action, scope, result, comparison, consequence) and stop where the RS could verify it; tie each to an assigned duty (paragraph 6.b(2))
- [ ] 5. Sort: awards, Certificates of Commendation, scholarship or honor graduate certificates, and PME completions leave the accomplishments and go on the list for the RS with dates (chapter 1 paragraph 6.b, chapter 4 paragraph 4.f(1)); a pending award recommendation is not listed at all; selection board or court-martial membership is struck (paragraph 6.b Note)
- [ ] 6. Read back the fact list; the user confirms; nothing else goes in. Now read exemplar.md for shape
- [ ] 7. Draft mrow.md in the shape below, bullets only, past tense results, no first person
- [ ] 8. python3 scripts/mrow_input_check.py mrow.md exits 0
- [ ] 9. Strike pass with voice.md; compare the character counts the checker prints with the A-PES field on the screen, since the order fixes no limit
- [ ] 10. Saved to Admin/Fitrep/<label> MROW <period To date>.md; the user types it into A-PES on their own computer and forwards the MROW to the RS before the end of the period
- [ ] 11. Learning: what the RS kept, cut, or rewrote, via aar
```

## The product (mrow.md)

```
# MROW input
MRO: <MARINE>, <grade>, <billet as the rules file states it>   Period: From <day month year> To <day month year>   Occasion: <code>
RS: <billet>   RO: <billet>   Prepared: <date>
References: MCO 1610.7B enclosure (2) chapter 1 paragraphs 6 and 7; chapter 2 paragraph 3.c; chapter 4 paragraphs 5 and 6

## Billet description
- <duty; scope as a count; the standard the RS set>
- <additional or special duty, with the date assigned>

## Billet accomplishments
- <past tense verb, what, count, result against a baseline>
- <one accomplishment per bullet, each tied to an assigned duty>

## For the RS (not section C)
- PME: <what, completion date> or none
- Commendatory material: <what was presented, date> or none presented during the period
- Promotion preference (item 8h): <first sergeant | master sergeant | not applicable to this grade>
```

## Rules

- Bullets, each with a distinctive mark, in both sections; the order requires "bulletized text format" (5.c(1)(a), 6.c(1)(a)). No paragraph prose.
- Section B lines describe the billet: "the nature of the billet and the MRO's significant responsibilities" (5.a), "acceptable standards vice goals" (5.b(3)), and not "the prerequisites of the Marine's MOS" (5.a). Counts that define the job stay; "needless statistics" go (5.c(3)(a)).
- Section C lines are results: "exactly what the Marine accomplished in the billet" (6.a(2)), "objective rather than qualitative" (6.a(3)), "only the results and achievements themselves" with no "reference to personal qualities or potential impact" (6.a(4)). Each relates to an assigned duty (6.b(2)). A line with no number is a description and the checker warns on it.
- Out of section C, on the order's word: awards, other commendatory material, adverse material, disciplinary action (6.c(1)(c)); participation as a member of a selection board or court-martial (6.b Note); superlative adjectives, needless statistics, imprecise phrasing (6.c(3)(a)); UPPERCASE, underlining, quotation marks, boldface, italics, punctuation in exclamation (6.c(3)(c)); acronyms specific to one community or MOS (6.c(4)). The checker fails the first four groups and warns on acronyms.
- Awards and PME go on the list for the RS with dates, because the order names them as what the summary of accomplishments should tell the RS (chapter 1 paragraph 6.b) and the RS handles them in item 6a and section I (4.f(1)(c)). A "none" line is a fact the RS needs. A pending award recommendation is never listed (4.f(1)(a) Note).
- Nothing about the marks, the ranking, the RS's profile, or promotion. The RS marks and writes; the MROW carries facts (chapter 2 paragraph 3.c(3)). The checker fails a line that claims a mark.
- Nothing from paragraph 13.d's unacceptable comments list, about the MRO or anyone else, and nothing adverse, medical, family, or financial. If it affected the period, the MRO tells the RS in person.
- Classified duties: the word "classified" replaces the entry (paragraph 17.b).
- Length: the order fixes no character, line, or word limit for the MROW or for sections B and C, only "the space provided" on the form (5.c(1), 6.c(1)). The checker prints counts; the A-PES field and the RS decide. Do not treat any other number as a limit.
- `<MARINE>` or "the MRO" until the user types it into A-PES; every other Marine by billet. No em or en dashes; the bullet mark is a hyphen or a circle.

## Utility scripts

- `scripts/mrow_input_check.py mrow.md`: title and MRO label; period From and To as dates in order (fail); RS billet (fail), RO billet and occasion code (warn); both sections present and bulleted (fail); in both: superlative, quotation marks, bold or italic or underline, exclamation (fail), uppercase words outside a short acronym list, strike words, first person (warn); in the billet description: an award (fail), "goal" or the MOS (warn); in the accomplishments: award or commendatory material, adverse or disciplinary material, personal quality or potential or imprecise phrasing words, selection board or court-martial membership, the paragraph 13.d topics (fail), a bullet with no number (warn), PME in the accomplishments (warn); anywhere in the two sections: a claim about the marks, profile, or promotion, the kit's blocked content (fail); a pending award recommendation under For the RS (fail), no For the RS list (warn); a name, a lifted exemplar or voice phrase, an em or en dash (fail). Prints character and word counts per section and imposes no cap. Exit 1 on any failure.
