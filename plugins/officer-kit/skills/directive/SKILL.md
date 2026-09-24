---
name: directive
description: >
  Drafts a unit order or bulletin for a commander to sign in the directives format of MCO 5215.1K
  w/Admin Ch 3: the type that fits the purpose (an order for a permanent reference, a bulletin for
  a one time requirement of 12 months or less with its cancellation line; the order knows no third
  type, so a company or battalion standing operating procedure issues as an order), the five
  paragraph structure the order prescribes (Situation, Cancellation second if needed, Mission,
  Execution with Commander's Intent and Concept of Operations, Subordinate Element Missions,
  Coordinating Instructions, Administration and Logistics, Command and Signal with the
  applicability and effective statements), the SSIC and point number, the signature block,
  reference integrity, the supplements a company may not issue, and the annual review, then checks
  the draft. Use when the user says "write a company order", "battalion order for", "SOP for the",
  "standing operating procedure", "bulletin for", or "put this out as a directive".
metadata:
  version: "0.1.0"
  status: incomplete
---

# Directive

A directive is read for years by Marines who were not there when it was written, and the Directives Control Point rejects it before the commander sees it if the format is wrong. The order is strict on both counts: "Marine Corps directives shall be issued as an 'Order' or 'Bulletin'", an order is "a directive of continuing authority or information, meant to be a permanent reference", a bulletin "must have a self-canceling provision" and "normally remains in effect up to 12 months, but no longer", Situation "must be the first paragraph", Cancellation "is always the second paragraph, if needed", and "All references must be used in the text." The tool asks what the reader must do and for how long, picks the type from the answer, writes the paragraphs in the order's structure and words, and checks them. It drafts; the commander signs, and the DCP verifies the SSIC and assigns the point number. Two parts are unverified against a source: the order defines no "standing operating procedure" type, so an SOP is issued here as an order on the order's own definition and the command's local practice may differ; and the SSIC itself comes from SECNAV M-5210.2, which is not in the library, so the tool records the number the user gives and who verifies it. See `references/standard.md`, "Not in the library".

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Read first

1. `references/standard.md`: chapter 1 paragraphs 3 (definitions), 5 (supplements and the five barred subjects below battalion), 6 and 7 (authority and signature), 21 to 27 (identification, references, enclosures), 32 and 33 (paragraphs), 37 (signature block); chapter 2 with figure 2-2 (the field command order); chapter 3 with figures 3-1 and 3-2 (bulletins); the basic order's review rules; and the section on what applies to a battalion or company as against HQMC.
2. `references/intake.md`: the questions, one at a time.
3. `references/voice.md`: the order's paragraph titles and statements, the tasking sentence, the strike list.
4. `references/exemplar.md`: read only after the fact list is confirmed (step 6). It teaches shape and its content is not to be taken; the checker fails a lifted phrase.

## Your own material (read first, every time)

1. `Overrides/directive.md`: the command's own directives order, its designation line abbreviation and sponsor codes, who the DCP is, whether the command runs an SOP series outside its directives system, any local review cycle. The command's way wins; say in one line what it changed.
2. `Reference/Exemplars/directive/`: directives this command signed, sanitized. They beat the plugin's fictional exemplar.
3. `<SIGNER_CAPS>` in the signature block; the commander's name goes on the document on the user's computer with `security-check/scripts/substitute.py --label "<SIGNER>"`. No Marine's name anywhere else: a directive states the rule, a record entry states the case.
4. When the DCP or the commander changed the draft, `aar` captures why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

## Workflow

```
Directive:
- [ ] 1. Type: what the reader must do and for how long; continuing and permanent is an order, one time or 12 months or less is a bulletin; nothing else exists (an SOP is an order, a letter of instruction is not a directive)
- [ ] 2. Standing: echelon, principal official by title, whether the subject is one a company may not supplement (leave and liberty, assumption of command, alcoholic beverage control, mail handling, command security), whether a higher directive already covers it completely
- [ ] 3. Identification: designation line, SSIC proposed and who at the DCP verifies it, point number (order) or cancellation month and year with Canc or Canc frp (bulletin), sponsor code, revision letter if any, Reserve designation if Reserve only
- [ ] 4. Cancellation, references, enclosures: what this cancels (only what the command sponsors, a bulletin with its date), every reference the text will use in order of first appearance, every enclosure by exact title, any report, form, or records requirement
- [ ] 5. Content under each paragraph, one question at a time: Situation, Mission, Commander's Intent, Concept of Operations, Subordinate Element Missions by billet with the main effort named, Coordinating Instructions, Administration and Logistics with the records disposition; or Purpose, Background, Action, Reserve Applicability, Cancellation Contingency for a bulletin; climb the ladder on each tasking
- [ ] 6. Read back the fact list; the user confirms; nothing else goes in. Now read exemplar.md for shape
- [ ] 7. Signature and distribution: who signs and under what delegation, the distribution statement, DISTRIBUTION and Copy to
- [ ] 8. Draft directive.md in the shape below; the order's titles and statements verbatim
- [ ] 9. python3 scripts/directive_check.py directive.md exits 0
- [ ] 10. Strike pass with voice.md; no "I" or "me"; acronyms spelled out once
- [ ] 11. Saved to Admin/Directives/<designation> <SSIC> <date>.md; the user lays it out in Courier 10 or 12 with one inch margins and underlined titles, substitutes the signer, and routes it to the DCP
- [ ] 12. Learning: what the DCP or the commander changed, via aar
```

## The product (directive.md)

```
# Directive
Type: <Order | Bulletin>   Echelon: <company | battalion | ...>   Purpose: <what the reader does and for how long>   Supplements: <higher directive | none>
Identification: <XXO SSIC.point[rev] | XXBul SSIC>   Sponsor code: <code>   Date signed: (Date Signed)
Signed by: <the principal official (title) | title, by title | title, by direction | title, acting>   DCP: <who verifies the SSIC and assigns the point number>
References: MCO 5215.1K w/Admin Ch 3 enclosure (1) chapter <2 | 3>; figure <2-2 | 3-1 | 3-2>

## Letterhead page
UNIT LETTERHEAD
                                        Canc: <Mon YYYY>          (bulletin only; Canc frp: when contingent)
                                        <XXO SSIC.point | XXBul SSIC>
                                        <sponsor code>
                                        (Date Signed)

<DESIGNATION LINE IN CAPITALS, e.g. BATTALION ORDER 1553.1>

From:  <principal official's title>
To:    Distribution List

Subj:  <SUBJECT IN CAPITALS>

Ref:   (a) <in order of first appearance; bulletins with (canc: Mon YY)>
Encl:  (1) <exact title>

Reports Required: <title (Report Control Symbol), paragraph>     (only if a report is imposed)

DISTRIBUTION STATEMENT <A>: <the statement from paragraph 19, unaltered>

## Body
1. Situation. <purpose>
2. Cancellation. <what this cancels, only if needed; then Mission is 3 and there are six paragraphs>
2. Mission. <task: who, what, where, when, why>
3. Execution
    a. Commander's Intent and Concept of Operations
        (1) Commander's Intent. <purpose and end state in the commander's words>
        (2) Concept of Operations. <how>
    b. Subordinate Element Missions
        (1) <main effort by billet>
        (2) <supporting efforts, reserve>
    c. Coordinating Instructions
        (1) <what applies to two or more elements>
        (2) <...>
4. Administration and Logistics
    a. <support, responsibilities>
    b. <records kept and disposed of per reference>
5. Command and Signal
    a. Command. This Order is applicable to <the Marine Corps Total Force | the Marine Corps Reserve | all Marines and Sailors assigned or attached to the command>.
    b. Signal. This Order is effective the date signed.

(Bulletin body instead: 1. Purpose. 2. Cancellation (if needed). 3. Background (if needed). 4. Action. 5. Reserve Applicability. This Bulletin is applicable to <...>. 6. Cancellation Contingency (last, only with Canc frp, never repeating the date).)

## Signature page
                                        <SIGNER_CAPS>
                                        <title only when signing by title; "By direction" when delegated further; "Acting" when acting>

DISTRIBUTION: <who must act>

Copy to: <who is informed>

## Review
Annual review <month>, recorded on NAVMC 10974 or the command's tracking system by <billet>; revise at 9 years or after the ninth change; command directives review within 1 year of a change of command. DCP: <billet>, designated in writing.
```

## Rules

- Two types. "Marine Corps directives shall be issued as an 'Order' or 'Bulletin'." An order is continuing authority and a permanent reference in the five paragraph format; a bulletin is one time or brief term, self canceling, 12 months at most, in the chapter 3 format. A standing operating procedure that is a permanent reference is an order. A letter of instruction is exempt from the program and is not this tool's product. The checker fails a third type.
- Order paragraphs in the order's order: Situation first; Cancellation second only when something is canceled, and then Mission is third and there are six paragraphs; Execution with a. Commander's Intent and Concept of Operations broken into (1) and (2), b. Subordinate Element Missions, c. Coordinating Instructions; Administration and Logistics; Command and Signal with a. Command carrying the applicability statement and b. Signal reading "This Order is effective the date signed." The checker fails a missing or misplaced paragraph or subparagraph and an altered statement.
- Bulletin: "Canc: Mon YYYY" or "Canc frp: Mon YYYY" above the SSIC on the first page, no point number, Purpose first, Cancellation second if needed, Reserve Applicability present, Cancellation Contingency last when the cancellation is contingent and never repeating the date. The checker fails a bulletin without its cancellation line or past 12 months.
- Field commands write to figure 2-2 in the command's own designation line, under the principal official's title. The identification block is the abbreviated type, SSIC, point number, and revision letter (never I, O, or Q); the DCP verifies the SSIC and assigns the point number.
- No supplement below battalion or squadron on leave and liberty, assumption of command, alcoholic beverage control, mail handling, or command security procedures, unless separately detached or an Inspector-Instructor staff. A supplement never contradicts, repeats, or encloses the higher directive, and incorporates it by reference.
- Every listed reference is cited and every cited reference is listed, in order of first appearance; the same for enclosures; a bulletin or MARADMIN reference carries its cancellation date.
- Every major paragraph has a title; a subdivided paragraph has at least two subdivisions; paragraph numbers are cited as "3a(2)(b)".
- Signature: the principal official or a delegate in writing by title, a further delegate by direction, "Acting" when acting; name in capitals, no grade or rank, no title when the signer is the principal official named in the From line. `<SIGNER_CAPS>` until substitution.
- Distribution statement on the letterhead page in the words of paragraph 19; DISTRIBUTION and Copy to on the signature page.
- Review annually, recorded on NAVMC 10974 or a tracking system; revise at 9 years; command directives review within 1 year of a new commander. The order prescribes the review, not a review statement in the text.
- No "I" or "me". No Marine's name, identifier, or case facts; a directive states the rule. No em or en dashes.

## Utility scripts

- `scripts/directive_check.py directive.md`: type is Order or Bulletin (fail otherwise, then checks as whatever the designation line says); identification block with SSIC and point number for an order, SSIC without point number for a bulletin, revision letter not I, O, or Q, date as day month year with the three letter month or "(Date Signed)"; bulletin cancellation line present and within 12 months of the date signed, Canc frp with a Cancellation Contingency last paragraph that does not repeat the date; an order with a cancellation date (fail); designation line in capitals matching the type, From, To: Distribution List, Subj in capitals, a distribution statement with statement A unaltered; references and enclosures listed against cited both ways, a higher directive enclosed (fail), a supplement with no Ref section (fail); the five barred subjects below battalion (fail); order paragraphs present, titled, numbered consecutively, in sequence, Cancellation second and Mission third when present, six paragraphs then and five otherwise, Execution subparagraphs a(1), a(2), b, c present, Command applicability stated, Signal verbatim, a canceled directive with no Cancellation paragraph (fail), a Cancellation paragraph canceling a Headquarters directive or a bulletin without its date (fail); bulletin Purpose first, no order format paragraphs, Reserve Applicability present; a subdivided paragraph with one subdivision (fail); "I" or "me" (fail); strike words (warn); signature block with `<SIGNER_CAPS>`, no rank, no principal's title, By direction and Acting consistent with the header, DISTRIBUTION present (warn); Review section (warn); names, blocked identifiers, blocked content about a person, lifted exemplar phrases, dashes (fail). Exit 1 on any failure.
