---
name: page-11
description: >
  Drafts the two adverse Page 11 entries a company grade officer prepares most: the paragraph
  6105 counseling entry (deficiency, specific corrective action with sources of assistance,
  the consequences including administrative separation, the reasonable opportunity, and the
  acknowledgment and five working day rebuttal language) and the not recommended for promotion
  entry with its unit diary deadline, to the Separation and Retirement Manual, the IRAM, and the
  enlisted promotion manual, and checks that every required element is present. Use when the
  user says "6105 for", "page 11 for", "counseling entry", "not recommended for promotion
  letter", "not rec", "document this for separation", or "administrative remarks entry".
metadata:
  version: "0.1.0"
---

# Page 11

A 6105 entry is the document that decides, months later, whether a Marine can be separated for the pattern it describes. MCO 1900.16 (the Separation and Retirement Manual) requires four things in it, and the TBS records handout says it plainly: if any is missing, "the administrative requirement for separation has not yet been satisfied." The tool builds the entry so the four are always present, in the IRAM's form, with the acknowledgment and rebuttal language, and it prepares the not recommended for promotion entry with the deadline the promotion manual sets. It prepares; the commander signs, and the legal officer or SJA reviews before it goes in the record.

## Read first

1. `references/standard.md`: the four required elements, the rebuttal language, the IRAM's form, the promotion manual's not recommended rule and deadline.
2. `references/intake.md`: the questions that produce a defensible entry.
3. `references/exemplar.md`: a fictional 6105 done right and a weak one.

## Your own material (read first, every time)

1. `Overrides/page-11.md`: the command's entry format, the legal officer's standing wording, who signs at what level. The command's way wins.
2. `Reference/Exemplars/page-11/`: entries the legal officer accepted from this command, sanitized.
3. `<MARINE>` throughout; the name and EDIPI go on the form on the user's computer. The entry describes deficiencies as dated facts; nothing medical, family, or from an investigation beyond what the commander directs.
4. When the legal officer returns an entry, `aar` captures why.

## Workflow

```
Page 11:
- [ ] 1. Which entry: 6105 counseling, or not recommended for promotion (or both, which is common)
- [ ] 2. Frame: the Marine (label, grade, billet), the counselor or commander who signs, the date, the prior counselings on the same deficiency (dates, from counseling records)
- [ ] 3. The deficiency: what, when, how often, as dated facts; the standard it violates (an order, a regulation, a lawful instruction) by number where one exists
- [ ] 4. Corrective action: specific, observable, with a period; the sources of assistance (by program, with how to reach them)
- [ ] 5. Consequences: the comprehensive statement that failure may result in administrative separation and the other actions the command may take
- [ ] 6. The reasonable opportunity: the period the Marine is given, with the date the commander will re evaluate
- [ ] 7. Acknowledgment and rebuttal: the Marine's acknowledgment line and the five working day rebuttal advisory
- [ ] 8. Not recommended for promotion, when applicable: the entry, the unit diary action, and the deadline (by the 15th of the month before the promotion month)
- [ ] 9. python3 scripts/page_11_check.py entry.md exits 0
- [ ] 10. Saved to Admin/Page 11/<label> <type> <date>.md; to the legal officer for review; entered on the form by admin
```

## The 6105 entry (entry.md)

```
# Page 11 entry: 6105 counseling
Marine: <MARINE>, <grade>, <billet>   Date: <date>   Signed by: <billet>
References: MCO 1900.16 paragraph 6105; MCO P1070.12K paragraph 4005

## Entry
<date>: Counseled this date concerning the following deficiencies: <dated facts, the standard violated>. Counseled on the same deficiency on <dates> (counseling records). <MARINE> is advised that <the specific corrective action>, and that assistance is available from <sources with how to reach them>. <MARINE> is further advised that failure to take the recommended corrective action and to overcome these deficiencies may result in administrative separation under MCO 1900.16, in addition to <other actions the command may take>. <MARINE> will be given <period> to demonstrate correction, and will be re evaluated on <date>. <MARINE> is advised that within 5 working days after acknowledging this entry, a written rebuttal may be submitted for inclusion in the service record.

## Acknowledgment
<MARINE> (signature line)   Date:
Counselor (signature line)   Date:
```

## Rules

- All four elements, every time. The checker fails an entry missing any of them.
- Deficiencies are dated facts and the standard they violate. "Bad attitude" is not a deficiency; "failed to report at the time posted on the duty roster on 12, 19, and 26 July 2026" is.
- Corrective action is observable: what the Marine will do, by when, that the counselor can see.
- Sources of assistance are named programs the command actually has, with how to reach them; the tool asks, never invents.
- The consequences statement names administrative separation under MCO 1900.16 explicitly. That is the sentence the separation depends on.
- Nothing medical, family, financial, or from an investigation, unless the commander directs it and the SJA has reviewed; and then only the fact, never the detail.
- Not recommended for promotion: the promotion manual makes the commander's recommendation the first requirement; the entry and the unit diary action are due by the 15th of the month before the month the Marine would otherwise be promoted. The tool computes the date from the promotion month the user gives.

## Utility script

- `scripts/page_11_check.py entry.md`: the four required elements present (deficiency with a date; corrective action with an observable verb and a period; sources of assistance; consequences naming administrative separation); the reasonable opportunity with a re evaluation date; the five working day rebuttal advisory; the acknowledgment block; for not recommended, the deadline line; names and blocked content (fail). Exit 1 on a missing element or a name.
