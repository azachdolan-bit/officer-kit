# Script and cue card

## Script

`brief_check.py --kind script` reads this layout.

```
# <Title>

Topic: <the topic exactly as assigned>
Limit: <m:ss>   Pace: <words per minute, 140 if the user has not timed themselves>

## 1 · <SECTION NAME> 0:00
<spoken text>

## 2 · <SECTION NAME> <m:ss>
<spoken text> *(OPTIONAL CUT)*

## CLOSE <m:ss>
<spoken text>

## Where every fact comes from
| Line | Source |
|---|---|

## Lines not to say
- "<line>" <why>
```

1. **Time marks** are where each section starts at the stated pace. The checker recomputes them from the word counts and fails a mark more than 20 seconds off, so rehearsal matches the page.
2. **The format** comes from the user's guide, quoted in the reply. For a guide that splits the time (one minute in, three in the body, one out), pass `--format 1,3,1`: the body must start by the end of the first part plus 30 seconds, and the close must start no earlier than the last part's start minus 30 seconds.
3. **Optional cuts** are marked `*(OPTIONAL CUT)*` after the sentence, so the speaker knows what goes first when running long. The checker still counts them.
4. **Quotes** of four words or more must be verbatim in a source file passed with `--sources`. The check ignores punctuation, so a source's dash inside a quotation is written as a comma (standard 9) and the words still verify.
5. **A doctrinal element** (`--doctrine "MCDP 1"`) must be quoted in the script and named in the sources table: naming the concept is not showing it.
6. **Hooks are allowed.** A talk may open on a person or a moment before it states the topic; the brief may not.

## Cue card

`build_card.py` takes a JSON file:

```json
{"title": "Short title", "size": "5x3",
 "faces": [
   {"lines": [
     {"t": "0:00", "text": "Keyword phrase, eight words at most"},
     {"quote": "An exact quotation, in full", "cite": "Source, chapter"}
   ]}
 ]}
```

1. **Key words and phrases,** not sentences: eight words at most on a line.
2. **Only an exact quotation** goes on the card in full, with its citation; it must match the script word for word.
3. **Time marks** in order, matching the script's marks, at least one on every face. A clock time in the content is written as four digits (0230), never m:ss, which reads as a pacing mark.
4. **One side per face,** numbered, nine printed lines at most, large print. A quotation counts its wrapped lines and its citation, so a face with three quotes will not fit; split it.
5. Render, then run the `visual-reviewer` agent on the rendered pages until it returns SHIP.
