# Skill template

Copy this into `skills/<skill-name>/SKILL.md`. Replace every bracket.

```markdown
---
name: [skill-name]
description: >
  This skill should be used when the user says "[trigger 1]", "[trigger 2]",
  "[trigger 3]", or [describes the situation in one line].
metadata:
  version: "0.1.0"
---

# [Skill Title]

[One line: what this produces and for whom.]

## Security
- No real names, SSNs, DoD IDs, EDIPIs, phone numbers, or addresses in the output. Use "the Marine" or placeholders.
- Stop if the input carries a CUI, FOUO, or classification marking, or came from a .mil system.
- Draft only. Never send or post.

## Input
- [Where it comes from: file in `02_Training`, pasted notes, Gmail, calendar]
- [What to do if it is missing: ask for it, or use the most recent file]

## Sequence
1. [First step]
2. [Second step]
3. [Third step]

## Output
- Format: [bullets / one paragraph / table / five sections named ...]
- Length: [one page / under 200 words / etc.]
- Tone: [match the rules file / direct and brief / formal correspondence]
- Save as: `[YYYY-MM-DD_topic.md]` in `[folder]`

## Never
- [Rule 1]
- [Rule 2]
```

## Example: weekly platoon update

```markdown
---
name: weekly-update
description: >
  This skill should be used when the user says "weekly update", "draft my update to the
  platoon commander", "write the Friday rollup", or "what do I tell the boss this week".
metadata:
  version: "0.1.0"
---

# Weekly Update

Draft the Friday update to the platoon commander from the week's notes.

## Security
- No real names in the output. Use billets: "the platoon sergeant," "Marine 1."
- Stop if any input carries a marking or came from a .mil system.
- Draft only.

## Input
- Notes the user pastes, plus anything dated this week in `01_Admin` and `02_Training`.
- If no notes, ask for three bullets on what happened.

## Sequence
1. Sort the notes into: done, in progress, blocked, next week.
2. Pull out anything that needs a decision from the platoon commander.
3. Write the update.

## Output
- Format: BLUF line, then four headers: Done, In Progress, Blocked, Next Week. Decisions Needed at the bottom if any.
- Length: under 200 words.
- Tone: direct, no adjectives.
- Save as: `YYYY-MM-DD_weekly-update.md` in `01_Admin`.

## Never
- Never generalize one event into a trend.
- Never include a number I did not give you.
```
