# The spec

One JSON file per lesson drives every format. Write it from the capture, run `scripts/gates.py` on it, then build. `example-spec.json` is a complete fictional example; copy its shape, never its content.

| Key | Required | What it holds |
|---|---|---|
| `mode` | yes | `guide`, `walkthrough`, `handout`, or `whiteboard` |
| `title`, `subtitle` | yes, no | The lesson's own title and designation as the source prints them |
| `seed` | yes | Any integer; makes the answer shuffle reproducible |
| `skeleton` | guide, walkthrough | The whole lesson compressed: numbered topics, lists as terse chains, key numbers, the source's own acronyms |
| `objectives` | when the source has them | `[{"code": "...", "text": "..."}]`, verbatim |
| `sections` | yes | In source order. Each: `id`, `title`, `body` (Markdown subset), optional `eyebrow`, `lede`, `branch`, `map`, `asis`, `quiz`, `final` |
| `sections[].map` | walkthrough, first section | `{"root", "note", "branches": [{"label", "sec", "leaves": [...]}]}`; `sec` names the section that teaches the branch |
| `sections[].asis` | walkthrough | `[["label", "the complete source text for this section"], ...]`, shown behind "Read it as issued" |
| `sections[].quiz` | walkthrough | Questions (below); the last section, or one marked `"final": true`, may draw on every section |
| `quiz` | guide | The guide's practice quiz; may draw on any section |
| `scenarios` | guide, where judgment is graded | `[{"title", "situation", "key"}]`; `key` prints on its own page |
| `flashcards` | when asked | `[{"front", "back"}]` |
| `assumptions` | when the tool had to choose | Markdown; printed under "What this guide assumed" |
| `excluded` | when a source line is not teaching text | `[{"text": "a phrase from the line", "reason": "why it is not carried"}]` |
| `score_label`, `good`, `bad`, `commit`, `bands` | no | Walkthrough wording; neutral defaults are used when absent |

A question: `{"q": "...", "o": ["four", "options", "all", "filled"], "a": 0, "e": "why, in the source's words", "d": "easy|medium|hard", "src": "optional exact body phrase that proves the answer"}`. Author the correct answer anywhere; the builders move it. A free recall question in the guide quiz is `{"type": "recall", "q": "...", "answer": "...", "e": "...", "d": "...", "src": "optional"}`.

Body Markdown: `##` and `###` headings, paragraphs, `-` and `1.` lists, `| tables |`, `**bold**`, `*italic*`, `` `code` ``, a table caption as a paragraph `Table: caption` directly above the table, and callouts written `> TRAP: text` (any capitalized label: TRAP, KEY NUMBER, MEMORY HOOK, DISCRIMINATOR, SOURCE CONFLICT).
