# The analysis file

One JSON file per order, checked by `scripts/analysis_check.py` against the order text. The report is written from it. Plain numbering; no composite identifiers.

| Key | What it holds |
|---|---|
| `order_file` | The captured order text file |
| `legend` | `[{"term": "BW", "meaning": "...", "source": "where it is defined"}]`, every column abbreviation the order uses, decoded from the order or the user's material |
| `resourcing` | `{"attachments": {"quote", "loc"}, "logistics": {"quote", "loc"}}`, read first; it bounds everything else |
| `facts` | `[{"factor": "Mission", "text": "the fact in plain words", "quote": "verbatim", "loc": "3.c.(2)"}]`; factors: Mission, Enemy, Terrain and weather, Troops and support available, Time available, Civil considerations |
| `findings` | `[{"n": 1, "type": "contradiction", "claim": "...", "a": {"quote", "loc"}, "b": {"quote", "loc"}, "consequence": "what a subordinate would do wrong", "computed": [...], "directions": [...], "gate0": "SURVIVES ...", "gate1": "SUBSTANTIVE ..."}]` |
| `rfis` | `["the question for higher, one line each"]` |

`type` is contradiction (two passages of the same order that cannot both be followed), geometry (a grid, distance, or bearing that does not work, computed), sequence (an event placed where it cannot happen, read after the legend), or omission (something the format requires that the order leaves out, stated as an RFI rather than a fault).

`computed`: `[{"from": "grid", "to": "grid", "distance_m": 172, "azimuth_mils": 6007, "stated_distance_m": 500}]`. The checker recomputes every number and fails a stated versus computed gap inside the error budget.

`directions`: `[{"word": "NW", "mils": 5600}]` for any direction word converted in the finding.
