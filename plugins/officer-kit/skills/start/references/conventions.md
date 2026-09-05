# Conventions every tool follows

Five conventions make the kit yours instead of the author's, and make its thinking visible. Every product tool reads them at its first step. They live in the user's working folder, never in the plugin, so a plugin update never overwrites them.

## 1. Names stay out of the session

Another Marine's name never goes into a prompt or a saved draft. The tools work on a label, `<MARINE>` by default (`<MARINE_CAPS>` where the product is in capitals, `<LAST>` and `<LAST_CAPS>` for the surname alone), with grade and billet kept because the criteria need them. When the product is finished, the user runs `security-check/scripts/substitute.py <file>` on their own computer; it asks for the name once, writes a named copy beside the labeled original, and stores nothing. The named copy is submitted and deleted; the labeled original is the record.

Why: DoDI 5200.48 forbids official business involving CUI on non DoD systems, NAVMC 5239.1 makes the user responsible for what goes into a public AI system, and GenAI.mil, the government's own platform, prohibits PII. A draft on a named Marine is PII. The label is how the kit makes the safe way the easy way; it is a mitigation, not a permission, and the officer decides.

The user may pick a working label they prefer ("the Sgt", "M1"); the tools use whatever the rules file records under "Working label".

## 2. Overrides: how your command does it

`Overrides/<tool>.md` in the working folder, one file per tool, plain text. Anything in it wins over the tool's defaults: the approval authority's reading habits (result first, bullets or paragraphs, what they strike), the command's local order and its enclosure list, the format the S-1 actually accepts, a lesson learned from the last package. Every tool reads its override file first and says so in one line. `inspect` writes to these files when a lesson is approved; the user can write to them any time.

Format: a heading per topic and short lines under it. No names of other Marines. Example, `Overrides/award.md`:

```
## Reader
- Battalion CO reads result first; strikes "instrumental" and "pivotal" on sight; wants SOA in paragraphs
## Command
- Adjutant requires the SOA and citation as one PDF, citation page first
## Lessons
- 2026-09-01: board downgraded a NC written to four units; scope must name the effect on each unit, not the count
```

## 3. Exemplars: your command's approved products

`Reference/Exemplars/<tool>/` in the working folder holds patterns from products the user's own command approved, put there by `add-exemplar`, which strips identifiers, keeps the shape and the numbers, and writes an annotation. The plugin ships fictional exemplars so every tool works on day one; a real approved product from the user's own command beats them, and every tool reads the user's folder before the plugin's file.

## 4. Lessons: the kit learns in your folder

`LEARNINGS.md` in the working folder is the user's lessons queue, written by `aar` (or by hand) when a product came back with edits, a board answered differently than the tool expected, or a reviewer caught something. `inspect` turns approved lessons into override lines or, when a lesson belongs in the plugin itself, into a change proposal the user can send to the kit's repository. The plugin's own `LEARNINGS.md` is the author's queue; the user's is theirs.

## 5. Thinking is proportional, and it is written down

Every product tool runs at a consequence tier. **Deliberate** when someone can be hurt, when it enters a record that cannot be removed, when it has legal effect, or when a board decides something irreversible from it. **Rapid** when it goes to a decision maker and is reversible. **Running** for routine work. The tool says which tier it is running and why, in one line, and anyone can raise a tier.

At the deliberate tier the tool writes an estimate before it drafts: the task and the outcome it serves, the standard and whether it is on disk, facts separated from tested assumptions, the questions whose answers change the product, what it will not do, and how it gets checked. Before delivery it runs the check: premortem, expected but absent, adversarial read, reconciliation, single rapid reading, and a plain statement of what was not checked.

This is not a promise of better answers, and the `think` skill says so with the evidence. Structured technique tested on fifty intelligence analysts moved accuracy from 33 to 36 percent, which is nothing. What it moved was whether they considered the diagnosticity of their evidence, from 32 to 80 percent. What the estimate buys is a record the signer can read: what was assumed, what was considered, what would change the answer, and what nothing checked.

## The line every rendered product carries

"Drafted with AI assistance (Officer Kit). The signer owns the words." In the document's file properties (comments field), not in the body. The Army's generative AI guidance asks for labeling; the Marine Corps' says distrust and verify. The line is there so nobody has to guess, and so the signer remembers who owns the words.
