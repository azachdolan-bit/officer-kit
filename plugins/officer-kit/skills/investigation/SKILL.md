---
name: investigation
description: >
  Prepares an administrative investigation the way the JAGMAN and the Naval Justice School
  handbook require it: the preliminary inquiry, and the command investigation report with a
  preliminary statement, findings of fact each tied to an enclosure, opinions each tied to
  findings, recommendations each tied to opinions, the enclosure list with the convening order
  first, the 30 day clock, and the rights warnings that must precede an interview, with the
  chain checked mechanically. Use when the user says "I was appointed investigating officer",
  "command investigation", "preliminary inquiry into", "JAGMAN", "findings of fact", "write the
  investigation report", or "how do I investigate".
metadata:
  version: "0.1.0"
---

# Investigation

Every officer is handed one of these with no notice and a 30 day clock. The Manual of the Judge Advocate General (JAGINST 5800.7G, Chapter II) governs; the Naval Justice School's JAGMAN Investigations Handbook (October 2024) says how a report that survives review is built. The report's power is its chain: every finding of fact cites an enclosure, every opinion cites findings, every recommendation cites opinions. Break the chain and the SJA sends it back. The tool builds the report so the chain cannot break, and it prepares; it never decides what happened, and every product goes to the staff judge advocate before the convening authority.

## Read first

1. `references/standard.md`: the handbook's own words on the report's parts, the rules for each, enclosures, the timeline, the appointment, and the warnings before interviews.
2. `references/intake.md`: the questions in the order an investigating officer works: the convening order, the evidence, the witnesses, the facts, the opinions, the recommendations.
3. `references/exemplar.md`: a fictional command investigation into a training injury, and a weak one annotated.

## Your own material (read first, every time)

1. `Overrides/investigation.md`: the command's SJA's format preferences, the convening authority's standing instructions, local forms. The SJA's way wins.
2. `Reference/Exemplars/investigation/`: reports the SJA accepted from this command, sanitized by `add-exemplar`.
3. The label rule is strict here: the subject and witnesses are `<WITNESS 1>`, `<SUBJECT>`, billets only; names go in at the last step on the user's computer. Nothing from the report body ever goes to a commercial model with a name attached.
4. When the SJA returns the report, `aar` captures why, without the facts of the case.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

List the competing hypotheses before writing findings, including the one where nobody did anything wrong. Work to disconfirm rather than confirm, and ask what evidence each hypothesis predicts that is absent.

## Workflow

```
Investigation:
- [ ] 1. Which: preliminary inquiry (quick, informal, about three working days, need not be written) or command investigation (appointed in writing, normally 30 days, the full report). The convening order says; if there is none, it is a PI
- [ ] 2. Read the convening order: what is to be investigated, what the CA directed the IO to address, the due date, any special instructions. The order is enclosure (1)
- [ ] 3. Consult the SJA before the first interview (the handbook requires it); ask what warnings apply
- [ ] 4. Evidence plan: documents to collect, scenes to see, witnesses to interview, in the handbook's order (everything else before a suspect)
- [ ] 5. Warnings: Article 31(b) for any military witness suspected of an offense, misconduct, or improper performance of duty; the injury or disease statement warning before any signed statement about an injury; the Privacy Act statement when personal information is taken. Forms from the JAGMAN appendices via the SJA
- [ ] 6. Interviews and statements, each its own enclosure; the tool drafts the question list per witness from the convening order, never the answers
- [ ] 7. Findings of fact: one fact per finding, specific as to person (by billet or label), time, place, event; chronological; each cites its enclosures
- [ ] 8. Opinions: each a reasonable inference from cited findings; addresses responsibility and what the CA directed
- [ ] 9. Recommendations: each from cited opinions; specific (a forum and charges if disciplinary; a draft if a punitive letter); corrective, disciplinary, or administrative
- [ ] 10. Preliminary statement: evidence collected or forthcoming, nature of the investigation, delays and extensions (noted here even if verbal), conflicting evidence and reliability, custody of original evidence
- [ ] 11. Enclosures: convening order first, then in the order the findings cite them; unused enclosures deleted; certified true copies where reproduced; nothing from the prohibited list (NCIS reports, mishap reports, IG reports, polygraphs, medical QA)
- [ ] 12. python3 scripts/investigation_check.py report.md exits 0 (the chain, the parts, the clock, the label rule)
- [ ] 13. Saved to Admin/Investigations/<label> <date>/report.md; to the SJA for review before the CA; names substituted on the user's computer
```

## The report (report.md)

```
# Command investigation: <subject of the convening order>
Convening authority: <billet>   Convening order: <date>   Due: <date>   Investigating officer: <billet>   Classification: <UNCLASSIFIED>

## Preliminary statement
<the handbook's required content>

## Findings of fact
1. <fact>. [Encl (2), (3)]
2. <fact>. [Encl (4)]

## Opinions
1. <inference>. [FF 1, 2, 5]

## Recommendations
1. <specific action>. [Op 1]

## Enclosures
(1) Convening order of <date>
(2) <statement of WITNESS 1, billet, date>
```

## Rules

- The tool prepares; the investigating officer finds. Findings are the IO's words about the evidence the IO collected; the tool arranges, cites, and checks them, and never supplies a fact the enclosures do not carry.
- Never interview a suspect before the rest of the evidence is in, and never without the warning. The tool refuses to draft a suspect's question list until the SJA consultation and the warning are recorded in the plan.
- No signed witness statements in any incident involving personal injury or a potential claim against the Navy (the handbook's rule); summaries of testimony instead. The checker warns when an enclosure list shows a signed statement in an injury case.
- Facts are facts. A finding with "probably," "it seems," "I believe" is an opinion and the checker moves it.
- Extensions are noted in the preliminary statement even when granted verbally.
- The label rule: `<SUBJECT>`, `<WITNESS n>`, billets. The checker fails a name.
- Out of scope, say so and stop: anything with NCIS or CID involvement beyond what the CA states; death cases (20 day rule, litigation report requirements, JA supervision); litigation report investigations; anything classified. Those go to the SJA before any drafting.

## Utility script

- `scripts/investigation_check.py report.md`: the five parts present in order; every finding cites at least one enclosure that exists in the list; every opinion cites findings that exist; every recommendation cites opinions that exist; enclosure (1) is the convening order; every listed enclosure is cited somewhere or flagged unused; opinion words inside findings (warn and list); the due date is within 30 days of the convening order or an extension is noted in the preliminary statement; names and blocked content (fail). Exit 1 on a broken chain, a missing part, or a name.
