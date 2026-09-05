---
name: aar
description: >
  Captures a lesson about a kit product into the user's own LEARNINGS.md queue: what came back
  with edits, what a board or approver did differently than the tool expected, what a reviewer
  caught, in the fixed lesson format, without changing any tool. Use when the user says "capture
  that", "lesson learned", "the CO changed", "it got downgraded", "that came back", "remember
  that for next time", or after any product's outcome is known.
metadata:
  version: "0.1.0"
---

# AAR (capture a lesson)

Nothing in the kit improves unless the outcome of a product gets written down where a later session will read it. This tool writes one lesson at a time, in a fixed shape, to `LEARNINGS.md` in the user's working folder. It never edits a tool, an override, or an exemplar; that is `inspect`, and it only happens with the user's approval.

## Workflow

```
Capture a lesson:
- [ ] 1. Which tool, and which product (label and date, never a name)
- [ ] 2. What happened, in one line of evidence: the edit the signer made, the board's answer, the reviewer's catch, the thing that was wrong at delivery
- [ ] 3. The lesson as an instruction: imperative, one or two lines, the way it should read in an override or a tool
- [ ] 4. Where it belongs: Overrides/<tool>.md (this command's way), Reference/Exemplars (a pattern), or the plugin itself (every user's way)
- [ ] 5. Confidence: high (a never or always from a direct correction), medium (a pattern that worked), low (an observation to watch)
- [ ] 6. python3 scripts/lesson_check.py LEARNINGS.md exits 0; appended with status pending
```

## The lesson format

```
## YYYY-MM-DD  <tool>  <high | medium | low>  -> <overrides | exemplar | plugin>
Evidence: <one line>
Lesson: <imperative, one or two lines>
Status: pending
```

## Rules

- Evidence first. A lesson without the thing that happened is an opinion, and `inspect` will reject it.
- No names, identifiers, or blocked content in the evidence line; refer to people by billet. The checker scans.
- One lesson per entry. Two things learned are two entries.
- A lesson that would soften a check, reduce sourcing, or suppress a reviewer is recorded with confidence low and a note that `inspect` rejects such lessons on sight; the user may still want the record.
- The tool never edits anything but LEARNINGS.md.

## Utility script

- `scripts/lesson_check.py LEARNINGS.md`: every entry has the four fields in order, a valid tool name, a confidence, a destination, and no blocked content. Exit 1 on a malformed entry.
