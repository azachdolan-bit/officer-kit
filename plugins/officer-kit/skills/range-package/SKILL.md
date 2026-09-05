---
name: range-package
description: >
  Assembles the range package a range control accepts: the range request with the facts range
  control needs, the range order or letter of instruction in the unit's format, the OIC and RSO
  duty checklist from the Range Safety Pocket Guide, the range safety brief, the medical and
  communications plan, and the link to the risk assessment, with every item on the base's
  checklist accounted for. Use when the user says "range package", "range order for", "range
  request", "OIC checklist", "what does range control need", or is the OIC or RSO of any range.
metadata:
  version: "0.1.0"
---

# Range package

Range safety is governed by MCO 3570.1 (Range Safety, joint with AR 385-63) and by each base's range control SOP, and the package is what range control reads before it lets the unit on the range. The tool builds the package as a set of parts and tracks which the base requires; the base's checklist wins, and the tool's list is the common one.

## Read first

1. `references/standard.md`: the order and the Range Safety Pocket Guide (February 2024) on OIC and RSO duties, the briefs and checks before, during, and after firing, cease fire, and medical evacuation.
2. `references/intake.md`: the facts range control needs and the questions per part.
3. `references/exemplar.md`: a fictional range order and OIC checklist.
4. The `risk-assessment` tool: the RAW is part of every package.

## Your own material (read first, every time)

1. `Overrides/range-package.md`: the base's range control checklist and forms, the request lead time, the unit's range order format, the range control numbers. The base's list wins over the common one.
2. `Reference/Exemplars/range-package/`: packages range control accepted from this unit.
3. Billets, never names, in the package body; names on the signature and roster pages the base requires, added on the user's computer.
4. When range control returns a package, `aar` captures why.

## Thinking (tier: deliberate)

**Deliberate**, because someone can be hurt. Run the estimate before drafting and the check before delivery: the `think` skill, `references/estimate.md` and `references/check.md`, `references/tripwires.md` for the named shortcuts. State the tier and its trigger in one line so the user can raise it.

The premortem runs before the package is assembled, and the adversarial read applies to every control measure and every timing in the order.

## Workflow

```
Range package:
- [ ] 1. Frame: the range, the dates, the event, the weapons and ammunition by DODIC and count, the unit, personnel count, the OIC and RSO by billet and their certification status
- [ ] 2. The base's checklist from the override file, or the common list in standard.md; the request lead time
- [ ] 3. Range request: the facts range control asks for, in its form
- [ ] 4. Risk assessment: run or link risk-assessment; the RAW's residual level and approval are stated in the order
- [ ] 5. Range order or LOI: situation, mission, execution (course of fire by serial, the safety plan, the control measures, the limits), administration and logistics (ammunition, medical, transport, chow), command and signal (nets, cease fire, MEDEVAC)
- [ ] 6. OIC and RSO checklist: before, during, after, from the pocket guide, with the base's additions
- [ ] 7. Range safety brief: the brief the RSO gives on the line
- [ ] 8. Medical and communications plan: the corpsman and their certification, the evacuation route and time, the nets and checks
- [ ] 9. python3 scripts/range_package_check.py package.md exits 0
- [ ] 10. Saved to Training/<range> <date>/; the base's forms filled by hand from the package
```

## The parts (package.md, one heading per part)

```
# Range package: <range>, <dates>, <event>
## Facts
Unit, dates, range, event, weapons, ammunition by DODIC and count, personnel, OIC (billet, certified <date>), RSO (billet, certified <date>), corpsman (billet, certification)
## Base checklist
- [ ] <each item the base requires, with its status>
## Range request
## Risk assessment
Residual level <level>; high risk training <yes|no>; approved by <billet> on <date>
## Range order
### Situation
### Mission
### Execution
### Administration and logistics
### Command and signal
## OIC and RSO checklist
### Before firing
### During firing
### After firing
## Range safety brief
## Medical and communications
```

## Rules

- The base's checklist wins. If the user cannot produce it, the tool says so and uses the common list, marked as such.
- The OIC and RSO are certified for the range or the package says they are not and who will be.
- Ammunition by DODIC and count; the package never rounds.
- Cease fire is stated the way the pocket guide states it: verbally and by the hand and arm signal, all weapons to Condition 4.
- MEDEVAC names the corpsman's certification, the route, the time to care, and who calls range control.
- Nothing about a named Marine; billets only.

## Utility script

- `scripts/range_package_check.py package.md`: every part heading present; Facts carry OIC and RSO certification, ammunition by DODIC and count, personnel; Risk assessment line has a level and an approver; the order has the five paragraphs; the checklist has before, during, after; cease fire and Condition 4 stated; MEDEVAC has a route and time; names and blocked content (fail). Exit 1 on a missing part or a name.
