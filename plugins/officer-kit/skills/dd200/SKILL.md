---
name: dd200
description: >
  Prepares the financial liability investigation of property loss (DD Form 200) the way the
  property order and the TECOM guide require it: the loss stated as dated facts, the chain of
  custody, the investigating officer's findings each tied to an enclosure, the finding on
  negligence or its absence, the recommendation on liability, and the NAVMC 6 where the Marine
  elects to pay, with the same chain checker the investigation tool uses. Use when the user
  says "we lost gear", "DD 200 for", "FLIPL", "missing gear statement", "financial liability
  investigation", "I'm the investigating officer for the lost", or "NAVMC 6".
metadata:
  version: "0.1.0"
---

# DD 200

Lost or damaged government property starts a clock and a form. MCO 4400.201 (Management of Property in the Possession of the Marine Corps, 17 volumes) governs accountability (Volume 1) and financial liability (Volume 17, Financial Liability Investigation of Property Loss); the TECOM headquarters battalion guide walks the DD 200 and the NAVMC 6 block by block. The investigation is a findings of fact investigation with a narrow question: what was lost, how, who had custody, and whether negligence or willful misconduct caused it. The tool builds it on the same chain the `investigation` tool enforces, prepares the blocks, and never decides liability; the appointing authority and the SJA do.

## Read first

1. `references/standard.md`: the order's volumes and the guide's block by block instructions, and the responsible officer's duties.
2. `references/intake.md`: the questions in the order the form asks them.
3. `references/exemplar.md`: a fictional DD 200 narrative and findings.
4. The `investigation` tool's `references/standard.md` for the findings chain rules; the checker here is the same engine.

## Your own material (read first, every time)

1. `Overrides/dd200.md`: the supply officer's format, the command's routing, the local deadline from discovery to initiation. The supply officer's way wins.
2. `Reference/Exemplars/dd200/`: investigations that closed in this command, sanitized.
3. `<MARINE>` and `<WITNESS n>` throughout; the custodian's name goes on the form on the user's computer. Serial numbers and NSNs are property data, not personal data, and belong in the report.
4. When the supply officer or SJA returns it, `aar` captures why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

List the competing explanations for the loss before writing findings. Ask what record would exist under each and is absent.

## Workflow

```
DD 200:
- [ ] 1. Frame: what was lost or damaged (nomenclature, NSN, serial, quantity, unit price, total), when discovered, by whom (billet), the responsible officer, the appointing authority, the deadline
- [ ] 2. Immediate actions: the search conducted (where, when, by whom, result), the missing gear statement, the supply officer notified on <date>
- [ ] 3. Custody: who had the item, on what record (CMR, ECR, sub custody card), from when, and the last time it was inventoried
- [ ] 4. Interviews and evidence: custody documents, inventory records, statements or summaries from the custodian and the last user (labels), the search log
- [ ] 5. Findings of fact: the item, the custody chain, the last sighting, the discovery, the search, each cited to an enclosure
- [ ] 6. Opinions: the proximate cause of the loss; whether simple negligence, gross negligence, or willful misconduct is present, or none, each cited to findings, with the standard from the order named
- [ ] 7. Recommendation: liability or relief, in the form's terms, cited to opinions; the amount if liability; NAVMC 6 if the Marine elects to pay
- [ ] 8. python3 scripts/dd200_check.py report.md exits 0
- [ ] 9. Saved to Admin/Property/<label> DD 200 <date>/; the blocks transferred to the form; to the supply officer and the SJA before the appointing authority
```

## The report (report.md)

Same shape as the `investigation` tool's report, with a Property block after the header:

```
## Property
| Nomenclature | NSN | Serial | Qty | Unit price | Total | Record | Custodian (label) |
```

Then Preliminary statement, Findings of fact, Opinions, Recommendations, Enclosures, with the chain cites.

## Rules

- The item is identified by NSN and serial from the record, never from memory. If the record and memory differ, the finding says so.
- The custody chain is documents: the CMR or ECR, the sub custody card, the inventory. A custody link with no document is a finding of its absence.
- Negligence is a standard from the order, cited; the opinion names simple or gross negligence or willful misconduct only with the standard quoted from the user's copy, or says none of the three is shown.
- The tool never states the liability amount as a decision; it states the value from the record and lets the appointing authority decide.
- Out of scope: losses involving weapons, ammunition, classified material, or controlled cryptographic items have their own reporting; say so and stop until the SJA and the supply officer direct.

## Utility script

- `scripts/dd200_check.py report.md`: the Property table with NSN, serial, quantity, price; the findings chain (the investigation engine); the custody record cited; a search finding present; an opinion on negligence naming a standard or its absence; the recommendation cites opinions; names (fail). Exit 1 on a broken chain, a missing property field, or a name.
