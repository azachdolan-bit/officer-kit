# The quiz spec

One JSON file per set of decks. `example-spec.json` is a complete fictional example built from the study-guide example source; copy its shape, never its content.

| Key | Required | What it holds |
|---|---|---|
| `title` | yes | The set's title, for the host key |
| `seed` | yes | Any integer; makes the placement reproducible |
| `time_by_difficulty` | no | Seconds per level; default easy 20, medium 20, hard 30 |
| `decks` | yes | `[{"name": "...", "questions": [...]}]`; the name becomes the file name |

A question: `{"q": "stem", "o": ["two to four options"], "a": 0, "e": "why, in the source's words", "d": "easy|medium|hard", "src": "optional exact source phrase", "ref": "section heading and page", "time": optional seconds}`. Author the correct answer anywhere; the builder moves it.

A study-guide spec's questions can be copied into a quiz spec as they are; add `ref` and `d` where missing.
