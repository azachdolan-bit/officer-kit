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

A 6105 entry is the document that decides, months later, whether a Marine can be separated for the pattern it describes. MCO 1900.16 paragraph 6105 requires four things in it, prescribes the entry's wording, and requires the commanding officer's signature on every adverse Page 11 entry; a copy goes to CMC (MMRP-20) within 30 days. The tool fills the order's own entry format with dated facts, observable corrective action, and named sources of assistance, keeps the order's consequences and rebuttal sentences unchanged, and prepares the not recommended for promotion entry with the deadline the promotion manual sets. It prepares; the commanding officer signs, and the legal officer or SJA reviews before it goes in the record.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Read first

1. `references/standard.md`: the four required elements, the rebuttal language, the IRAM's form, the promotion manual's not recommended rule and deadline.
2. `references/intake.md`: the questions that produce a defensible entry.
3. `references/exemplar.md`: a fictional 6105 done right and a weak one.

## Your own material (read first, every time)

1. `Overrides/page-11.md`: the command's entry format, the legal officer's standing wording, who signs at what level. The command's way wins.
2. `Reference/Exemplars/page-11/`: entries the legal officer accepted from this command, sanitized.
3. `<MARINE>` throughout; the name and EDIPI go on the form on the user's computer. The entry describes deficiencies as dated facts; nothing medical, family, or from an investigation beyond what the commander directs.
4. When the legal officer returns an entry, `aar` captures why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

The adversarial read is the pass that matters: every directive sentence read for its most inconvenient compliant meaning. `think/scripts/precision_check.py entry.md --directive` on the parts the writer supplies, never on the order's prescribed wording.

## Workflow

```
Page 11:
- [ ] 1. Which entry: 6105 counseling, or not recommended for promotion (or both, which is common)
- [ ] 2. Frame: the Marine (label, grade, billet), the commanding officer who signs (the order requires the CO's signature), the date the CO counsels (that is the entry's date), the prior counselings on the same deficiency (dates, from counseling records); entry (1) if the Marine is not being processed, entry (2) if already being processed
- [ ] 3. The deficiency: what, when, how often, as dated facts; the standard it violates (an order, a regulation, a lawful instruction) by number where one exists
- [ ] 4. Corrective action: specific, observable, with a period; the sources of assistance (by program, with how to reach them)
- [ ] 5. Consequences: the comprehensive statement that failure may result in administrative separation and the other actions the command may take
- [ ] 6. The reasonable opportunity: the period the Marine is given, with the date the commander will re evaluate
- [ ] 7. The order's sentences unchanged: the consequences sentence, the VA benefits sentence, the five working day rebuttal sentence, the choose to or not to line; signature lines for the Marine and the commanding officer; the MMRP-20 copy within 30 days noted
- [ ] 8. Not recommended for promotion, when applicable: the entry, the unit diary action, and the deadline (by the 15th of the month before the promotion month)
- [ ] 9. python3 scripts/page_11_check.py entry.md exits 0
- [ ] 10. Saved to Admin/Page 11/<label> <type> <date>.md; to the legal officer for review; entered on the form by admin
```

## The 6105 entry (entry.md), in the order's format

```
# Page 11 entry: 6105 counseling
Marine: <MARINE>, <grade>, <billet>   Date: <date the CO counsels>   Signed by: Commanding officer
References: MCO 1900.16 paragraph 6105; MCO P1070.12K paragraph 4006.3r

## Entry
<date>: Counseled this date concerning the following deficiencies: <dated facts and the standard violated; prior counselings with dates>. Specific recommendations for corrective action are <observable action, period, re evaluation date> and to seek assistance, which is available through the chain of command and <named sources>. Failure to take corrective action and any further violations of the UCMJ, disciplinary action, or incidents requiring formal counseling may result in judicial or adverse administrative action, including but not limited to administrative separation. I understand that failure to complete my enlistment contract with an honorable characterization of service may preclude my eligibility for benefits from the Department of Veterans Affairs or other organizations and have an adverse effect on future civilian employment. I was advised that within 5 working days after acknowledging this entry I may submit a written rebuttal which will be filed in the electronic service record. I choose to ____ /not to ____ make such a statement.

## Acknowledgment
Signature of Marine: ____   Signature of Commanding Officer: ____

## After signature
Photocopy of the entry and any rebuttal to CMC (MMRP-20) within 30 days.
```

## Rules

- The order's format, word for word for the fixed sentences; the blanks are where the facts go. All four elements, every time. The checker fails an entry missing any of them or altering the fixed sentences.
- The commanding officer signs. A counselor's signature on an adverse Page 11 entry is not what the order requires.
- Deficiencies are dated facts and the standard they violate. "Bad attitude" is not a deficiency; "failed to report at the time posted on the duty roster on 12, 19, and 26 July 2026" is.
- Corrective action is observable: what the Marine will do, by when, that the counselor can see.
- Sources of assistance are named programs the command actually has, with how to reach them; the tool asks, never invents.
- The consequences sentence is the order's: "may result in judicial or adverse administrative action, including but not limited to administrative separation." Not reworded, not softened, not turned into a promise.
- Nothing medical, family, financial, or from an investigation, unless the commander directs it and the SJA has reviewed; and then only the fact, never the detail.
- Not recommended for promotion: the promotion manual makes the commander's recommendation the first requirement; the entry and the unit diary action are due by the 15th of the month before the month the Marine would otherwise be promoted. The tool computes the date from the promotion month the user gives.

## Utility script

- `scripts/page_11_check.py entry.md`: the order's fixed sentences present verbatim (counseled this date concerning the following deficiencies; specific recommendations for corrective action are; to seek assistance, which is available through the chain of command and; the consequences sentence; the VA benefits sentence; the 5 working day rebuttal sentence; the choose to line); the deficiency dated; corrective action with an observable verb and a re evaluation date; a named source of assistance; the commanding officer's signature line; the MMRP-20 copy noted; for not recommended, the deadline line; names, promises, and blocked content (fail). Exit 1 on a missing element, an altered fixed sentence, or a name.
