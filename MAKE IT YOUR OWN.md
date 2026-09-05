# Make it your own

The kit ships method, never content. Every tool works on day one from the governing order and a fictional example, and every tool gets better the moment you give it your command's way. This page is how, in the order you will actually do it. Nothing here edits the plugin; everything lives in your working folder, so a kit update never overwrites what you added.

## The four places you add things

**`Overrides/<tool>.md`** is how your command does it. One file per tool, plain text, short lines under headings. The approval authority's habits (result first, paragraphs, what they strike), the local order and its enclosure list, the format the S-1 actually accepts, the base's range checklist, the SJA's preferences. Every tool reads its override file before it does anything and tells you in one line what changed. You can write these files by hand any time; `inspect` writes to them when you approve a lesson.

**`Reference/Exemplars/<tool>/`** is your command's approved products as patterns. When a package of yours gets approved (or downgraded, which teaches just as much), say "this one got approved" and `add-exemplar` strips the identifiers, keeps the exact sentences and numbers, writes an annotation, and files it. From then on the tool reads your pattern before its fictional one.

**`LEARNINGS.md`** is your lessons queue. When something comes back with edits, a board answers differently than the tool expected, or a reviewer catches something, say "capture that" and `aar` writes one lesson in a fixed format with the evidence first. Nothing changes until you run `inspect` and approve each lesson, one at a time.

**`Reference/`** is your library: the orders the tools cite. `library` walks you through building it. A tool that cannot find its order on disk says so and marks what it could not verify; it never pretends.

## The label

Another Marine's name never goes into a session or a saved draft. The tools work on `<MARINE>` (with grade and billet, because the criteria need them). When a product is finished, run `security-check/scripts/substitute.py` on the file on your own computer; it asks for the name once, writes a named copy beside the labeled original, and stores nothing. The named copy goes out and gets deleted; the labeled original is your record. `rules-file` records a different working label if you prefer one.

Why: DoDI 5200.48 forbids official business involving CUI on non DoD systems, NAVMC 5239.1 puts responsibility for what goes into a public AI system on you, and even GenAI.mil prohibits PII. The label makes the safe way the easy way. It is a mitigation, not a permission; you decide what goes in.

## Building a tool of your own

Two kinds. A personal skill (a prompt with the rules decided, for something you do every week) takes five questions in `build-a-skill`. A kit tool, one with a standard behind it, needs the seven part shape the rest of the kit uses, and `build-a-skill/scripts/new_tool.py <name> "<what it produces>"` scaffolds all seven with TODO markers: the standard (verbatim from the order, with paragraph numbers), fictional exemplars (one strong, one weak, annotated), the intake (the questions a good reviewer asks, in order), the quantification ladder, the voice file, a checker that enforces what the standard imposes, and the learning hook. `BUILD STRATEGY.md` is the long form; `build-a-skill/references/tool-shape.md` is the short one. The checklist at the end of `build-a-skill` says when it is done: a person who did not build it runs it on their own material and it holds.

## Sending something back to the kit

When `inspect` decides a lesson belongs in the plugin itself (every user's way, not just your command's), it writes `Proposals/<date> <tool>.md`: the lesson, the evidence with no names, the exact wording change, and the eval case that would prove it. Send that file to the kit's repository as an issue or a pull request. The kit's own `LEARNINGS.md` is the author's queue; yours is yours.

## What every tool refuses, whoever owns it

To invent a number, a date, a result, or a comparison. To carry a name through the session. To write medical, family, financial, disciplinary, or investigation content about a person. To promise an outcome a board or an approver decides. To soften a check because a lesson asked it to; `aar` records such a lesson at low confidence and `inspect` rejects it on sight.
