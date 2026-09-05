---
name: safety-brief
description: >
  Writes a liberty, holiday, long weekend, or event safety brief from the season's actual
  hazards, the unit's own recent mishaps (by type, never by name), and the command's format:
  short, specific, with the numbers that make Marines listen, the resources with phone numbers
  the user supplies, and the leader's expectations stated once. Use when the user says "safety
  brief for the 96", "liberty brief", "holiday safety brief", "brief before the weekend", or
  "pre event safety brief".
metadata:
  version: "0.1.0"
---

# Safety brief

Marines have heard a thousand safety briefs and remember none of them. The one they remember named a real thing that happened to a unit like theirs, gave a number, and told them what to do about it in one sentence. MCO 5100.29C (Volume 3 traffic and motorcycle, Volume 5 recreation and off duty) is the program behind the brief; the brief itself is the leader's voice for five minutes.

## Read first

1. `references/standard.md`: what the safety program expects a brief to cover, by season and event type.
2. `references/intake.md`: the questions that produce a specific brief.
3. `references/exemplar.md`: a fictional 96 hour liberty brief done right, and a weak one.

## Your own material (read first, every time)

1. `Overrides/safety-brief.md`: the command's required topics, its format (some require a signed roster and a specific slide), local resources and numbers. The command's list wins.
2. `Reference/Exemplars/safety-brief/`: the unit's own briefs beat the fictional one.
3. Mishaps are described by type and unit level ("a lance corporal in the battalion"), never by name.
4. If the brief lands (or does not), `aar` captures what worked.

## Workflow

```
Safety brief:
- [ ] 1. Frame: the occasion (96, holiday, event), the audience (platoon, company), the length (five minutes), the command's required topics
- [ ] 2. The season's hazards: the three that matter now (heat, water, motorcycles, holiday driving, alcohol, fireworks, cold), with a number the user can source
- [ ] 3. The unit's own recent mishaps and near misses by type, without names
- [ ] 4. Resources: the duty numbers, the ride program, the chaplain, the base numbers, as the user supplies them
- [ ] 5. The leader's expectations in one sentence each: the plan before leaving, the check in, the call for a ride
- [ ] 6. Draft to the shape; five minutes at 140 words a minute is about 700 words, most briefs should be half that
- [ ] 7. python3 scripts/safety_brief_check.py brief.md exits 0
- [ ] 8. Saved to Training/Safety briefs/<occasion> <date>.md; roster and signature per the command's format
```

## The shape (brief.md)

```
# Safety brief: <occasion>, <dates>
Audience: <unit>   Briefer: <billet>   Length: <minutes>

## The three things
1. <hazard>: <the number or the real event, by type>. <what to do, one sentence>.
2. ...
3. ...

## Resources
- <resource>: <number supplied by the user>

## Expectations
- <one sentence each>

## Required by the command
- <topics the override file lists, each covered above or here>
```

## Rules

- Three things, not twelve. The command's required topics are covered in a line each under the last heading.
- Every hazard has a number or a real event by type. "Be safe on the roads" is not a brief; "two Marines in the division died on motorcycles in May, both on a first ride after a deployment" is.
- No names, no cases involving a person in the room, nothing from an investigation.
- Numbers the user supplies or can source; the tool never invents a statistic. If none is at hand, the line uses the event, not a number.
- Resources with real phone numbers from the user; the tool never guesses a number.

## Utility script

- `scripts/safety_brief_check.py brief.md`: three things present, each with a number or an event; resources with numbers; expectations present; length against the minutes; names and blocked content (fail). Exit 1 on a missing section, a name, or blocked content.
