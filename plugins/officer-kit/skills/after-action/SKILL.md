---
name: after-action
description: >
  Turns notes from a range, exercise, event, or product into an after action report the unit
  can act on: what was planned, what happened, what worked and why, what to fix with an owner
  and a date, in the unit's format, with every fix tied to an observation. Use when the user
  says "AAR for", "turn these range notes into an after action", "lessons from the exercise",
  "write up what happened", or "capture what we learned". When the AAR is about a kit product,
  it also feeds the user's LEARNINGS.md through aar.
metadata:
  version: "0.1.0"
---

# After action report

No order prescribes the AAR's format; the unit's SOP does, and most follow the same shape: what was supposed to happen, what happened, why the difference, and what to do about it with a name and a date. The AAR that gets read next year is the one where every fix traces to an observation and every observation has a fact in it.

## Read first

1. `references/standard.md`: the shape as the doctrine and common unit SOPs carry it, and what a sustain or improve item must contain.
2. `references/intake.md`: the questions by phase, and the difference between an observation and a complaint.
3. `references/exemplar.md`: a fictional range AAR done right, and a weak one annotated.

## Your own material (read first, every time)

1. `Overrides/after-action.md`: the unit's AAR format and where AARs go (the S-3, MCTIMS, a shared drive). The command's format wins.
2. `Reference/Exemplars/after-action/`: the unit's own accepted AARs beat the fictional one.
3. No names of other Marines; billets only. An AAR is read widely.
4. When the AAR concerns a kit product (a package that came back, a tool that failed), run `aar` afterward so the lesson reaches LEARNINGS.md.

## Before you draft

Assume this already failed and write three reasons before you build anything, then check each against the draft.

Also ask what a good AAR of this event would contain that this one does not. That question, rather than "what is missing from the outline," is what finds the lesson worth writing down.

Say what you had to assume. Never write that the rest is covered.

## Workflow

```
After action:
- [ ] 1. Frame: the event, dates, unit, who reads this AAR and what they will do with it
- [ ] 2. What was planned: the mission or purpose, the timeline, the numbers (personnel, rounds, vehicles, hours)
- [ ] 3. What happened, by phase, as dated facts with numbers; the difference from the plan stated as a fact
- [ ] 4. For each difference: why (the cause the unit can act on, not the weather), and whether the result was better or worse
- [ ] 5. Sustain items: what worked, why, and what would keep it working next time
- [ ] 6. Improve items: what to fix, the specific change, who owns it (billet), by when
- [ ] 7. python3 scripts/after_action_check.py aar.md exits 0
- [ ] 8. Saved to Training/<event> <date>/AAR.md in the unit's format; routed per the override file
```

## The shape (aar.md)

```
# After action report: <event>
Unit: <unit>   Dates: <dates>   Location: <location>   Prepared by: <billet>   Date: <date>

## Planned
<mission or purpose; the timeline; the numbers>

## What happened
### <phase>
- <date or time>: <fact with a number>; <difference from plan, if any>

## Sustain
| Observation | Why it worked | Keep it by |
|---|---|---|

## Improve
| Observation | Fix | Owner (billet) | By |
|---|---|---|---|

## Numbers
<the event's counts: personnel, rounds, hours, casualties (none), equipment down, cost if known>
```

## Rules

- Observations are facts with a time and a number. "Comm was bad" is a complaint; "the company net dropped for 40 minutes at 1410 when the relay vehicle moved" is an observation.
- Every improve item has a fix, an owner by billet, and a date. An improve item without those is a wish, and the checker warns.
- Every fix traces to an observation in What happened. The checker warns on a fix with no matching observation.
- Nothing about a named Marine's performance; that is a counseling or a fitrep. Billets only.
- Weather, terrain, and higher headquarters are causes the unit cannot act on; the AAR names the thing the unit can change.

## Utility script

- `scripts/after_action_check.py aar.md`: the four sections present; observations dated with a number; improve rows complete (fix, owner, date); sustain rows complete; blocked content and names (fail). Exit 1 on a missing section or blocked content.
