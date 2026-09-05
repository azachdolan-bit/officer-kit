---
name: reenlistment
description: >
  Prepares a reenlistment, extension, or lateral move recommendation for block 35 of the RELM
  (NAVMC 11537) and the commanding officer's certification, to MCO 1040.31: the tier in the
  form's words with the population count that makes it true (with enthusiasm is the top 25
  percent of the grade known to the certifying officer, with confidence the top 50), brief
  comments under the order's three heads (conduct, performance, future potential), the
  mandatory reason for with reservation or not recommended, the 21 prerequisite screen, the
  interview windows computed from ECC and EAS, and the commanding officer's own interview
  when the Marine is not recommended. Use when the user says "reenlistment recommendation
  for", "RELM comments", "recommend this Marine for reenlistment", "with enthusiasm or with
  confidence", "not recommended for reenlistment", "career planning interview", "EAS
  interview", or "is this Marine in his reenlistment window".
metadata:
  version: "0.1.0"
---

# Reenlistment

The RELM goes up seven signature blocks and ends at CMC (MMEA-6), which decides; the order says the recommendation's role is "to initiate dialogue between the command and CMC (MMEA-6)" and that even a not recommended request is still referred there. The order also defines the two top tiers by population: "Recommended w/enthusiasm" is the top 25 percent of Marines in that grade known to the certifying officer, "Recommended w/confidence" the top 50 percent. A with enthusiasm on a Marine outside the top quarter is a false statement in a record. The tool asks for the count before it lets the box be checked, writes the comments the form asks for ("brief comments justifying your recommendations") under the order's three heads, screens the prerequisites for the CO's certification, and computes the interview windows. It prepares; the officer at each block signs, and the Career Planner owns the form.

## Read first

1. `references/standard.md`: chapter 3 (interviews, who conducts them, the windows), chapter 4 paragraphs 3 to 9 (who decides, the recommendation table, the 21 prerequisites, the certification, waivers), chapter 6 (the contact record), Figure 6-7 block 35 as the form prints it, Appendix D codes.
2. `references/intake.md`: the questions, one at a time.
3. `references/voice.md`: the form's words, the three heads, the strike list.
4. `references/exemplar.md`: read only after the fact list is confirmed (step 5). It teaches shape and its content is not to be taken; the checker fails a lifted phrase.

## Your own material (read first, every time)

1. `Overrides/reenlistment.md`: how this CO and Career Planner want block 35 written, the current RELM revision in the electronic system where it differs from the 2010 order's figure, the unit's delegation letter for interviews. The command's way wins; say in one line what it changed.
2. `Reference/Exemplars/reenlistment/`: recommendations this command signed, sanitized. They beat the plugin's fictional exemplar.
3. `<MARINE>` throughout; the name goes on the form on the user's computer with `security-check/scripts/substitute.py`. Conduct is a record fact by date (an NJP on a date); the story behind it stays out. Medical, family, and financial circumstances are yes or no on the prerequisites screen, never detail in the comments.
4. When the RELM comes back from MMEA-6 or the CO changed the tier, `aar` captures why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question. The population count and the Marine's standing are the questions this product turns on; ask them plainly.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

## Workflow

```
Reenlistment:
- [ ] 1. Frame: which block (35a to 35g), request type (reenlistment, extension, lateral move), who signs and whether personally; the Marine (label, grade, PMOS, billet), ECC and EAS as dates, first term or career
- [ ] 2. Windows: python3 scripts/reenlistment_windows.py --ecc <date> --eas <date> [--today <date>]; which required interview this attaches to and whether it fell inside its window
- [ ] 3. Population: how many of this grade the certifying officer knows well enough to rank, and where this Marine stands as a number of that number; the tier follows, never the other way round
- [ ] 4. Facts under the three heads, one question at a time: conduct as record facts by date; performance as counts with a comparison; potential tied to the next grade; climb the ladder on each note and stop where the officer can defend it to MMEA-6
- [ ] 5. Read back the fact list; the user confirms; nothing else goes in. Now read exemplar.md for shape
- [ ] 6. For 35g: the prerequisites screen, 5.a (1) to (21) plus 5.b or 5.c, each yes, no, or unknown; for each no, waivable or not, and the CG's own endorsement and the Marine's letter if a waiver is requested
- [ ] 7. For with reservation or not recommended: the reason as dated facts; at 35g the CO's own signature (not delegable); for not recommended, the date the CO personally interviewed the Marine and the RE code the CO assigns
- [ ] 8. Draft recommendation.md in the shape below; the form's words for the box
- [ ] 9. python3 scripts/reenlistment_check.py recommendation.md exits 0
- [ ] 10. Strike pass with voice.md; comments stay brief enough for the form's field
- [ ] 11. Saved to Admin/Reenlistment/<label> RELM <block> <date>.md; the officer copies the comments onto the form; the Career Planner routes it
- [ ] 12. Learning: what came back, via aar
```

## The product (recommendation.md)

```
# Reenlistment recommendation
Marine: <MARINE>, <grade>, <PMOS>, <billet>   Request: <reenlistment | extension | lateral move>   <First term | Career>   ECC: <day month year>   EAS: <day month year>
Block: 35<a-g> <level>   Signed by: <who, and whether personally>   Date: <date>
References: MCO 1040.31 enclosure (1) chapter 4 paragraph 4; NAVMC 11537 block 35

## Recommendation
<one of: Recommended with Enthusiasm (Top 25 %) | Recommended with Confidence (Top 50 %) | Recommended with Reservation | Not Recommended>

## Population            (required for the two top tiers)
<Grade>s known to the certifying officer: <N>. Standing: <k> of <N>.

## Comments
Conduct: <record facts by date>. Performance: <counts with a comparison>. Potential: <tied to the next grade, with the limit stated>. <For with reservation or not recommended: the reason as dated facts.>

## Prerequisites         (block 35g, or whoever prepares the certification)
Does SNM meet all reenlistment prerequisites: <Yes | No>
<Screened against 5.a (1) to (21) and 5.b or 5.c on <date> with the Career Planner; any no by prerequisite number, waivable or not, waiver requested or not.>

## Interview             (not recommended only)
Commanding officer's interview conducted <date> by the commanding officer personally. RE code assigned by the CO: <code, from Appendix D>. The request is referred to CMC (MMEA-6), which decides.

## Windows
<the three lines from reenlistment_windows.py, then which interview this attaches to and whether it fell inside its window>
```

## Rules

- The box in the form's words, and only one. The two top tiers require the population sentence; the checker fails a with enthusiasm above the top quarter or a with confidence above the top half of the count given. If the officer cannot count, those tiers are not available and the record says why.
- Comments under the order's three heads, in the order's order: conduct, performance, future potential as it relates to rank, age, experience, and maturity. Facts with dates and counts. Brief: the form's field, not a page.
- With reservation and not recommended: comments mandatory, the reason as dated facts, and at block 35g the commanding officer's own signature. The order: "The authority to provide a recommendation of 'Recommended With Reservation' or 'Not Recommended' may not be delegated."
- Not recommended: the commanding officer must personally interview the Marine; the CO, not a delegate, assigns any RE code other than RE-1A; the request still goes to MMEA-6, and only MMEA-6 denies further service.
- The certification is the CO's statement to MMEA-6 that the Marine meets every prerequisite. Screen all 21 plus the first term or career items, record yes, no, or unknown, and never certify yes over an unknown. A waiver goes up with the Commanding General's own endorsement (by direction is not sufficient) and a letter from the Marine.
- The windows are the order's: initial 26 to 24 months before ECC, FTAP or careerist 14 to 12 before ECC, EAS interview 8 to 6 before EAS; the script computes them and the checker fails a Windows section that disagrees with the header dates.
- Nothing about the decision. No promise about promotion, a board, or MMEA-6.
- Nothing medical, family, financial, or from an investigation in the comments. The order itself keeps one certification "yes" to protect the Marine's privacy; the tool follows that logic everywhere.
- `<MARINE>` until substitution on the user's computer. No em or en dashes.

## Utility scripts

- `scripts/reenlistment_windows.py --ecc <date> [--eas <date>] [--today <date>] [--fmcr]`: the three interview windows (and the FMCR request window), and the reenlistment type by time remaining (immediate under 90 days, standard, early), from chapter 3 paragraph 2.b and chapter 4 paragraph 1.c.
- `scripts/reenlistment_check.py recommendation.md`: title and label; block 35a to 35g named; exactly one tier in the form's words; population sentence present for the two top tiers and the standing inside the tier's share; comments present (mandatory, with a date, for the two lower tiers), the three heads named, numbers present, strike words, promises about the decision (fail), blocked content in the comments (fail); the two lower tiers at 35g signed by the CO personally (fail otherwise); not recommended with a dated CO interview (fail) and an RE code and the MMEA-6 line (warn); 35g with the certification line (fail); the Windows section recomputed from the header dates (fail on mismatch); names, lifted exemplar phrases, and dashes (fail). Exit 1 on any failure.
