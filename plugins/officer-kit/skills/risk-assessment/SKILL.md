---
name: risk-assessment
description: >
  Builds a Risk Assessment Worksheet for a training event or operation to MCO 5100.29C Volume 2:
  hazards identified by phase, each assessed for severity and probability to a risk level,
  controls that actually change the number, the residual level, the approval authority that
  follows from it, the high risk training flag, and the supervision plan, then checks the
  arithmetic and the required elements mechanically. Use when the user says "RAW for", "risk
  assessment for the range", "ORM worksheet", "is this high risk training", "what level has to
  approve this", or is planning any event with a range, vehicles, water, heights, heat, or live
  fire.
metadata:
  version: "0.1.0"
---

# Risk assessment

A Risk Assessment Worksheet is the one document where a lieutenant's arithmetic decides who has to sign. The order gives five steps, a severity scale, a probability scale, a matrix, and the rule that high risk training is anything left at IA, IB, IIA, or IIB after controls, which the first O-5 in the chain approves in writing. The worksheet that works names real hazards by phase, applies controls that change the probability or the severity (not "be careful"), and shows the number moving. The tool builds it that way and computes the levels so the user never argues with a matrix at 0500.

## Read first

1. `references/standard.md`: the order's own words on the five steps, the severity and probability categories, the worksheet's required elements, the definition of high risk training, and the approval rule.
2. `references/matrix.md`: the matrix the checker uses, and how to replace it with the command's own if it differs.
3. `references/intake.md`: hazards by phase, the questions that produce controls that change the number.
4. `references/exemplar.md`: a fictional live fire RAW done right, and a weak one annotated.

## Your own material (read first, every time)

1. `Overrides/risk-assessment.md` in the working folder, if it exists: the command's worksheet form, its matrix if it differs from the joint one, its standing controls, who signs at each level. Say in one line what it changed.
2. `Reference/Exemplars/risk-assessment/` in the working folder: approved worksheets from this command beat the fictional one.
3. No names in the worksheet body; billets only (OIC, RSO, safety corpsman). Names go on the signature block on the user's computer.
4. When range control or the approver changes something, tell the user `aar` will capture it.

## Workflow

```
Risk assessment:
- [ ] 1. Frame: the event, dates, location, unit, personnel count, the OIC and RSO by billet, the command's worksheet form if it has one
- [ ] 2. Phases listed (movement, setup, execution by serial, recovery, night, weather) so hazards are found where they live
- [ ] 3. Hazards by phase, one line each, from intake.md and the event's own history (last time this was run, what went wrong)
- [ ] 4. Each hazard: severity I to IV, probability A to E, initial level from the matrix, with the one line reason for each rating
- [ ] 5. Controls per hazard that change the probability or the severity, each with who implements it and when; "brief safety" is not a control
- [ ] 6. Residual severity and probability, residual level; the user says out loud why the control moves the number
- [ ] 7. python3 scripts/raw_check.py raw.md exits 0: arithmetic, required elements, high risk flag, approval level
- [ ] 8. If any residual is IA, IB, IIA, or IIB: high risk training; the emergency action plan, cease training and training time out procedures, primary and secondary communications, and the pre execution checklist are written, and the first O-5 approves in writing
- [ ] 9. Supervision plan: who watches which control, and the trigger to stop
- [ ] 10. Saved to Training/<event> <date>/RAW.md; the user transfers it to the command's form and routes it
- [ ] 11. Learning: after the event, aar records any hazard that appeared that the sheet did not carry
```

## The worksheet (raw.md)

```
# Risk Assessment Worksheet: <event>
Unit: <unit>   Dates: <dates>   Location: <location>   Personnel: <count>
OIC: <billet>   RSO: <billet>   Prepared: <date>   Worksheet form: <command form or "this sheet">

## Hazards
| # | Phase | Hazard | Sev | Prob | Initial | Controls (who, when) | Sev | Prob | Residual |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Execution | Heat casualty during the 4 hour live fire iteration in August | II | C | IIC | Flag conditions checked hourly by the RSO; work rest cycle per the flag; two water buffalos at the line; corpsman with ice sheets at the ECP | II | E | IIE |

## Highest residual level: <level>
## High risk training: <yes | no>  (yes if any residual is IA, IB, IIA, IIB)
## Approval authority: <from the residual level and the command's matrix; first O-5 in writing if high risk>

## Emergency action plan
<who does what if the worst hazard happens: nearest medical, evacuation route and time, communications, who calls>

## Cease training and training time out
<how anyone stops training, the words and the signal, and what happens next>

## Communications
Primary: <net>   Secondary: <means>   Check: <when>

## Pre execution checklist
- [ ] <the things confirmed the morning of, including any change since the sheet was signed>

## Supervision
| Control | Who watches it | Stop trigger |
|---|---|---|
```

## Rules

- A control changes the number or it is not a control. The checker warns on controls with no verb of change (brief, remind, ensure, be aware) and fails when a residual level improves with no control listed.
- Severity rarely changes; probability is what controls move. A residual that drops severity from I to III needs a stated reason (a different weapon, a different distance), and the checker warns.
- High risk training is a fact of the residual level, not a judgment. If it is IA, IB, IIA, or IIB after controls, it is high risk, and the sheet says so and goes to the O-5.
- Nothing in the sheet names a Marine; billets only. The corpsman's certification is stated, not the corpsman's name.
- The tool never lowers a rating to avoid an approval level. If the user wants a lower level, the sheet shows a control that earns it.
- The command's form and matrix win when they exist; the checker's matrix is the joint matrix from the order's figure and is replaceable in `references/matrix.md` or the override file.

## Utility script

- `scripts/raw_check.py raw.md [--matrix references/matrix.md]`: every hazard row has a phase, severity I to IV, probability A to E, initial and residual levels that match the matrix; residual not worse than initial; no residual improvement without a control; controls with no verb of change (warn); the four required elements present when high risk; the high risk line and the approval line agree with the highest residual; blocked content and names (fail). Exit 1 on arithmetic, a missing required element, or a mismatch between the levels and the flags.
