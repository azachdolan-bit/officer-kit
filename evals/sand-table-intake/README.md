# sand-table-intake harness

Fictional fixture, used by `evals/sand_table_intake_check.py`. Nothing here is a real unit, person, place or order.

- `fixture-base-order.md`: a company defense order to a platoon on the sketch sheet (grid square MG), in the shape a school base order takes: situation, mission, intent, EFST, tasks, timeline, logistics, with the platoon told to develop its own scheme, TCMs, engagement criteria, CASEVAC and signals.
- `fixture-facts.json`: what the intake reads out of it, every value with its paragraph.

The check writes the plan file with `plan_writer.py`, proves every fact is carried and every planner field is blank, passes it through `plan_check.py --intake`, then plants defects one at a time (an unknown field, a bad grid, a select value the page does not offer, a value with no paragraph, an offense field on a defense plan, a planner decision filled, objects on the map, a dash, an unknown sheet) and expects each to fail. The page's own import of the same file is tested on the sand table side (test_stage8u).
