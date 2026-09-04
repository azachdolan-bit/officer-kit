---
name: study-guide
description: >
  This skill should be used when the user says "make a study guide", "turn this into flashcards",
  "quiz me", "study this packet", "summarize this lesson", "practice test", "help me study for",
  or attaches a lesson packet, class notes, or a doctrinal publication for study.
metadata:
  version: "0.1.0"
---

# Study Guide

Turn a lesson packet, notes, or a published reference into something the user can study from in twenty minutes and be tested on.

## Inputs

Accept a file in the linked folder, an attachment, or pasted text. Published doctrine and the user's own notes are green. If the material carries a CUI or FOUO marking, stop and point to `security-check`.

## Output, in this order

**1. One page guide.** Headline: what this lesson is for. Then the core concepts as short definitions, the process or sequence if there is one, the numbers that get tested (distances, timelines, ratios, counts), and the acronyms. Keep it to one page. Cut anything that is context rather than content.

**2. Twenty question quiz.** Mix: ten recall (define, list, state), five application (given this situation, what do you do), five "which is wrong" (spot the error in a statement). Put the answer key at the bottom, separated, so the user can hide it.

**3. Flashcard set** if asked. Format as `Q | A`, one per line, so it pastes into any flashcard app.

## Quiz me mode

If the user says "quiz me," ask one question at a time. Wait for the answer. Grade it in one line, give the correct answer if they missed, then the next question. At the end, list what they missed and offer to drill those.

## Rules

- Test what the material says, not what Claude knows about the topic. If a number in the packet conflicts with general knowledge, use the packet and flag it.
- Never invent a reference or citation. If the packet cites an order, keep the citation as written.
- Five paragraph order, OSMEAC, BAMCIS, METT-TC, troop leading steps: when these appear, make sure the sequence and every element are in the guide. They get tested every time.
- Save outputs to `03_Academics` in the linked folder if it exists, named `YYYY-MM-DD_topic_studyguide.md`.
