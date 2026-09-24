---
name: inspect
description: >
  Reviews the user's LEARNINGS.md queue and turns approved lessons into changes where they
  belong: lines in the tool's Overrides file for this command's way, a pattern in Reference/Exemplars,
  or a written change proposal for the plugin itself, with the tool's checks run before anything
  ships. Use when the user says "review the lessons", "apply what we learned", "inspect the
  queue", "update my overrides", or at the end of a week with pending lessons.
metadata:
  version: "0.1.0"
---

# Inspect (apply lessons)

`aar` writes lessons; this tool applies them, one at a time, with the user's approval on each, to the place the lesson named. Nothing changes without a yes. Nothing in the plugin changes at all from here; plugin lessons become a proposal file the user can send to the kit's repository, because the installed plugin is replaced on update and any edit to it would be lost.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Workflow

```
Inspect the queue:
- [ ] 1. python3 ../aar/scripts/lesson_check.py LEARNINGS.md exits 0
- [ ] 2. Pending lessons listed, newest first, with evidence and destination
- [ ] 3. For each: reject on sight if it softens a check, reduces sourcing, or suppresses a reviewer (status: rejected <reason>); otherwise ask approve, defer, or reject
- [ ] 4. Approved overrides lesson: the line appended under the right heading in Overrides/<tool>.md; status: approved <date>
- [ ] 5. Approved exemplar lesson: run add-exemplar on the product it names; status: approved <date>
- [ ] 6. Approved plugin lesson: a proposal written to Proposals/<date> <tool>.md (the lesson, the evidence, the exact wording change, the eval case that would prove it); status: approved <date>, proposal filed
- [ ] 7. If a tool's override changed, run that tool's checker on the last product in its folder to confirm nothing now fails
- [ ] 8. Summary: what changed, what was deferred, what was rejected and why
```

## Rules

- One lesson, one decision, one change. No batch approvals.
- The user's overrides are theirs; the tool writes under the heading the lesson names (Reader, Command, Lessons) and never rewrites what is already there.
- A rejected lesson stays in the queue with its reason; the queue is a record, not a to do list.
- Never edit a file under the plugin. Proposals only.
- When a lesson contradicts an existing override line, show both and ask; do not pick.

## The proposal file

```
# Proposal: <tool>, <date>
Lesson: <the instruction>
Evidence: <one line, no names>
Change: <the file in the plugin and the exact wording to add or replace>
Eval: <the case in evals/<tool>/cases.json that would prove it>
From: <the user's working label, never a name unless they choose to sign it>
```
