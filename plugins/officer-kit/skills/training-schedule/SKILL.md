---
name: training-schedule
description: >
  Builds the weekly training schedule from the events the unit must train and the plan above
  it, to MCO 1553.3C: each event with its T&R code, time, place, instructor by billet, uniform,
  gear, prerequisites, and the risk assessment and range package status, with a prep list per
  event and the conflicts and gaps called out. Use when the user says "build the training
  schedule", "next week's schedule", "training plan for the week", "put these events on the
  schedule", or "what do I need before Thursday's range".
metadata:
  version: "0.1.0"
---

# Training schedule

MCO 1553.3C (Unit Training Management) makes the training schedule the commander's published intent for the week, tied to the T&R events the plan requires, recorded in MCTIMS, and submitted to higher. The schedule that works is the one where every event has an instructor, a place, the gear, and a prep list with dates, so the week does not collapse on Monday.

## Read first

1. `references/standard.md`: the order's own words on the schedule, the plan it comes from, MCTIMS, and the annual requirements.
2. `references/intake.md`: the events, the constraints, and the prep list questions.
3. `references/exemplar.md`: a fictional week done right and a weak one.

## Your own material (read first, every time)

1. `Overrides/training-schedule.md`: the battalion's format (many use a fixed spreadsheet), submission day and time, the S-3's rules (no changes inside 72 hours, for example). The command's format wins.
2. `Reference/Exemplars/training-schedule/`: the unit's own accepted schedules beat the fictional one.
3. Instructors and leaders appear by billet, never by name.
4. When the S-3 returns a schedule, `aar` captures why.

## Before you draft

Assume this already failed and write three reasons before you build anything, then check each against the draft.

The premortem is the week's: it collapsed on Tuesday. Why?

Say what you had to assume. Never write that the rest is covered.

## Workflow

```
Training schedule:
- [ ] 1. Frame: the week, the unit, the commander's training guidance and the training plan's events for this week, the submission deadline
- [ ] 2. Fixed events first: higher's events, ranges already booked, annual requirements due (MCO 1500.63A), medical and admin days
- [ ] 3. Unit events: each with its T&R code (from the NAVMC 3500 manual for the MOS), prerequisites, and the standard
- [ ] 4. For each event: date, time, place, instructor by billet, uniform, gear, ammunition or equipment, transport
- [ ] 5. For each event that needs one: risk assessment status (risk-assessment), range package status (range-package), classroom or range booked
- [ ] 6. Conflicts and gaps: two events for the same people, an instructor double booked, a range without a RAW, a prerequisite not met
- [ ] 7. Prep list per event with dates and owners by billet
- [ ] 8. python3 scripts/training_schedule_check.py schedule.md exits 0
- [ ] 9. Saved to Training/Schedules/<week>.md; transferred to the command's format; submitted per the override file
```

## The shape (schedule.md)

```
# Training schedule: <unit>, week of <date>
Commander's guidance for the week: <one line>   Submitted: <date> to <S-3>

| Day | Time | Event | T&R code | Place | Instructor (billet) | Uniform and gear | Prereqs | RAW | Range pkg |
|---|---|---|---|---|---|---|---|---|---|
| Mon | 0800 to 1200 | ... | 0311-M16-2001 | ... | Squad leader, 1st squad | ... | ... | signed | n/a |

## Conflicts and gaps
- <the thing that does not fit, and the proposed fix>

## Prep list
| Event | Task | Owner (billet) | By |
|---|---|---|---|
```

## Rules

- Every event has a T&R code or a stated reason it has none (admin, medical, higher's event).
- Every event with weapons, vehicles, water, heights, or heat has a RAW status; "pending" is a status, "blank" is a gap the checker flags.
- Instructors by billet. Two events with the same instructor at the same time is a conflict the checker flags.
- The schedule does not invent times; the user gives them or the tool marks TBD and lists it as a gap.
- The command's format wins for the submitted product; the tool's shape is the working copy.

## Utility script

- `scripts/training_schedule_check.py schedule.md`: every row has day, time, event, place, instructor; T&R code or a reason; RAW status on hazardous events; time conflicts by instructor; prep list rows complete; names (fail). Exit 1 on a row missing its core fields or on a name.
