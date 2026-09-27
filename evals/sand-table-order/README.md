# sand-table-order tests

`fixture.sandtable.json` and `fixture.sandtable-brief.md` are a fictional platoon defense exported by the virtual sand table (every name and grid invented; no course material). `evals/sand_table_order_check.py` (19 items): the reader lays out every field, typed but unapplied text marked as such, 37 objects with 8 digit grids derived from UTM, a squad's sector of fire and a gun's FPL azimuth, three routes with computed legs, two parts, the AO corners, and the brief's checks; `good-order.md` passes the checker; `bad-order.md` fails on each planted defect (an invented grid, a dropped position, a dropped field, a warning not carried, an en dash).

The good order doubles as the shape of the product: every paragraph from the plan, grids copied from facts.md, the two closing lists.
