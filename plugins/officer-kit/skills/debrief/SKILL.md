---
name: debrief
description: >
  Runs the end of chat debrief: sweeps the whole conversation for every correction, rejected or
  redone product, and instruction the user had to repeat, turns each into a lesson with the
  user's own words as evidence, sorts it to where it belongs (the kit, this command's overrides,
  or the user's rules file), writes only what the user approves, and lists every file the chat
  produced with its saved path. Use when the user says "debrief", "hotwash", "wrap up this chat",
  "what did we learn", or is closing a chat in which they corrected Claude.
metadata:
  version: "0.1.0"
---

# Debrief (end of chat)

A correction made in a chat dies in that chat unless it is written where the next session reads it. `aar` writes one lesson when the user asks for it; `debrief` sweeps the whole chat once, at the end, while the evidence is still on the screen. It follows the four questions of an after action review: what was supposed to happen, what happened, why, and what to sustain or change. It never edits a tool.

## Workflow

```
Debrief:
- [ ] 1. Read the rules file (CLAUDE.md). Take the lessons queue path from its "Lessons queue" line; default is LEARNINGS.md at the top of the working folder. If the file does not exist, create it with the header below.
- [ ] 2. Sweep the chat from the first message to the last for the signals listed below. Quote the user's words; do not paraphrase them.
- [ ] 3. For each signal, one line each: what was supposed to happen, what happened, why.
- [ ] 4. Check whether it is already recorded: the rules file, the queue, Overrides/<tool>.md, and the tool's own SKILL.md. Recorded and broken again is an enforcement gap (see Repeats).
- [ ] 5. Sort each lesson to a bin and a destination (table below).
- [ ] 6. Show the debrief table. The user approves, edits, or strikes each row in one reply. Nothing is written before that reply.
- [ ] 7. Write the approved rows: queue entries in the fixed format, rules file changes shown as a diff first.
- [ ] 8. Run python3 ../aar/scripts/lesson_check.py <queue path>; it must exit 0.
- [ ] 9. Files: list every file this chat created or changed with its path on disk. Flag anything that exists only in the chat.
- [ ] 10. Queue status in one line: pending count and the oldest pending date. If five or more are pending or the oldest is more than seven days old, say: run inspect.
```

## Signals

Count as a signal:

- A direct correction: "no," "that is wrong," "not what I asked," a fact the user fixed.
- A product or section the user rejected, struck, or asked to redo.
- An instruction the user had to give a second time. This is the most important signal: the rule existed and did not fire.
- An edit the user made to a draft; compare what they changed.
- A reviewer or gate catch that would otherwise have shipped.
- A question that exposed a gap ("where did that number come from?").
- A stated preference about format or process that applies beyond this task.

Not a signal: a requirement that belongs to this task only, or the user choosing between options they were offered.

Sustains: at most three things the user said worked, one line each. They are shown in the table and written only if the user wants them kept.

## Bins and destinations

| Bin | Test | Destination |
|---|---|---|
| Kit | True for any officer using this tool | Queue entry `-> plugin` |
| Unit | True for this command, billet, or unit SOP | Queue entry `-> overrides`, which `inspect` applies to Overrides/<tool>.md |
| Pattern | An approved product to copy | Queue entry `-> exemplar` |
| Personal | How this user wants Claude to work on any task | The rules file, under "How I want drafts written" or "Never", shown as a diff |
| This task only | Will not recur | Nothing written; say so in the table |

The tool name in a queue heading is the kit tool the lesson would change. A rule for every tool uses `kit-standards`. A lesson for a tool the kit does not have names the tool that should exist.

## Repeats

A lesson that is already recorded and fired again is not a new lesson. Write it as enforcement: the Lesson line names the mechanism that would make it fire (a checker line, a gate, a reviewer question, a line in the tool's Before you draft block, or a rules file line), at confidence high.

## The debrief table

| # | Your words | Lesson | Bin and destination | Already recorded? | Confidence |
|---|---|---|---|---|---|

Confidence: high for a never or always from a direct correction; medium for a pattern that worked; low for an observation to watch.

## Queue entry format

```
## YYYY-MM-DD  <tool>  <high | medium | low>  -> <plugin | overrides | exemplar>
Evidence: <the user's words, short, and what they corrected>
Lesson: <imperative, one or two lines>
Status: pending
```

Header for a new queue file:

```
# Learnings queue

Lessons captured by aar and debrief, waiting for inspect. Nothing here changes a tool until a person approves it.
```

## Rules

- Only the user's corrections and confirmations become lessons. Claude's own improvement ideas are not lessons unless the user adopts them in the chat.
- Evidence quotes the user. No other person's name or identifier; refer to people by billet. The checker scans.
- One lesson per row and per entry.
- A lesson that would soften a gate, reduce sourcing, or suppress a reviewer is recorded at confidence low; `inspect` rejects it on sight.
- Never edit a plugin file. Kit lessons wait in the queue. `inspect` turns approved ones into a proposal in Proposals/ that the user can send to the kit author on the repository's issues page. If the rules file names a kit maintainer queue, kit lessons go there instead.
- Claude's automatic memory is not a destination. It does not reach the kit, the rules file, or anyone else.
- A chat with no signals: say so in one line, list the files, give the queue status, done.
