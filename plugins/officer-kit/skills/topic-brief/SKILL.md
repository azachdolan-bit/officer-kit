---
name: topic-brief
description: >
  Researches and builds a short talk or backgrounder on an assigned, scoped topic (a history
  presentation, a professional military education brief, a period of instruction, a topic for the
  platoon): a brief that leads with the topic and gives general context one paragraph, incidents
  grouped by what they illustrate, every number tied to the topic and traced to a source, a lines
  not to say list where sources disagree, a timed script in the format the user's own program sets,
  and a keyword cue card. Use when the user says "history presentation on", "brief me on",
  "I have to give a five minute class on", "topic brief", "PME brief", "backgrounder on", or
  "make me a cue card".
metadata:
  version: "0.1.0"
---

# Topic brief

A topic brief fails the way the first draft of a real one did: it opened with the war's strategy, the bombers, and the casualty totals, wove the assigned topic through a general battle history, and left the reader asking how most of it related to the topic at all. The other failures are quieter. A number that is true for two days gets said about one night. A name the sources dispute gets said as fact. A doctrinal element gets named ("friction") instead of shown. A talk written for five minutes runs six.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Standard 2 governs every fact; standard 5 governs every doctrinal quote. Where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Your own material (read first, every time)

1. `Overrides/topic-brief.md` in the working folder, if it exists: the user's way wins. Say in one line what it changed.
2. The assignment, word for word: the topic as assigned, the time limit, and the program's format guide if there is one (search the working folder for "presentation guide", "format", or the course name). Quote the format rules from the guide with their locator; with no guide on disk, quote the assignment as the user gave it. Where the guide asks for a doctrinal element, read that publication from the library (`library/scripts/find_order.py`), never the web.
3. Research files the user already has on the topic. Build on them; do not redo them.

## Before you draft

1. **State the topic in one sentence** before any research, the way MCTP 3-30A tells a staff officer to open a briefing's preparation. Every later fact has to answer "how does this relate to that sentence?"
2. **Assume it already failed** and write three reasons first, in the reply. The usual ones: the context crowds out the topic, a number is true for a different scope than the sentence it is in, and the doctrinal element is named rather than shown.
3. **Fit the topic to the sources.** When the sources cover less than the assigned topic, scope the brief to what they support, say so in the opening paragraph, and name the rest as a gap with where it would be found. Never widen it from general knowledge.
4. **Ask only what changes the product:** the audience, the time limit if the guide does not set it, and whether the user wants the brief, the talk, the card, or all three (build only what is asked, standard 4).

## Workflow

```
Topic brief:
- [ ] 1. Topic sentence; format rules quoted from the user's guide; doctrine read from the library
- [ ] 2. Research from sources the user can check; every fact with its source; disputes recorded as they are found
- [ ] 3. Brief (references/brief-shape.md): topic first, context one paragraph, incidents grouped by what they illustrate, numbers tied to the topic, sources table, lines not to say
- [ ] 4. python3 scripts/brief_check.py <brief> --kind brief --sources <files> --numbers exits 0; read every number against its sentence for scope
- [ ] 5. Script (references/script-and-card.md), timed to the format; python3 scripts/brief_check.py <script> --kind script --sources <files> [--doctrine "<pub>"] [--format 1,3,1] --numbers exits 0
- [ ] 6. evidence-reviewer agent, blind, with the script and the sources: every number, quote, and scope
- [ ] 7. Card: python3 scripts/build_card.py <card.json> <out.html> --script <script> [--pdf <out.pdf>] exits 0; visual-reviewer on the rendered card until SHIP
- [ ] 8. Save the brief, script, card, and research beside each other; name every path
```

## Numbers hygiene

Every number carries its source and its scope in the same sentence: whose count, what period, what unit. When sources disagree, say the claim that is true under all of them ("at least 53", "nearly 800" with the source named) and put the others in lines not to say with the reason. Translate a number the audience cannot picture into one they can when the sources give something to compare it to; when they do not, leave it plain rather than invent a comparison. Cut any number that does not serve the topic sentence. The checker proves each number has a source, not that it is said at the right scope; `--numbers` lists every number beside its sentence and its row for that read. A person's later memory is said as memory ("he later told his biographer"), never as a transcript.

## Reply

The paths, the run time at the user's pace, the checker results, the evidence review verdict, and the lines not to say, so the user knows the traps before they stand up.

## Why it is built this way

- **MCTP 3-30A** (Effective Briefing Skills, 2-8; Military Briefings, 2-15): state the topic before the research, know every piece of content including acronyms, revise for succinctness, practice; an information briefing's outcome is comprehension, with "enough familiar material to establish a basis for understanding." That last phrase is the one paragraph context budget.
- **Speaking rate:** conversation runs about 150 words a minute and a comfortable presentation 100 to 150; the checker times the script at the user's pace (140 by default) and reports 130 and 150, so a nervous fast delivery and a deliberate slow one are both inside the limit.
- **Speaker notes** guidance from public speaking texts: key words and phrases, not sentences, in large print, one side, numbered; only an exact quotation goes on a card in full, with its citation. The card builder enforces that.
- **Communicating numbers** (Heath and Starr, Making Numbers Count): translate a number into something the listener can picture, or it is lost.
- **Historical thinking** (sourcing and corroboration): who counted, and do the sources agree. Lines not to say is where the disagreement is written down.

## Scripts

- `scripts/brief_check.py`: topic first, the context budget, every number traced to the sources table, quotes verbatim in the sources, lines not to say kept out of the script, time marks and run time against the limit and the format, the doctrinal element quoted rather than named, no dashes.
- `scripts/build_card.py`: a keyword cue card (5 by 3 inches by default) from a small JSON file, checked against the script, rendered to PDF when Chromium is available.
