# Base order to sand table: which paragraph feeds which field

The sand table's guided build is a list of steps, each with fields; `guide_fields.json` beside this file is the page's own list (step id, field key, type, label, options). A plan file carries `guide.values[step][key]`. The page builds the map from the values when it imports the file, so a grid in a place field becomes a symbol and a grid list in a draw field becomes a line.

## Sheets the page carries

| sheet id | what it is | grid square |
|---|---|---|
| `ta16` | TA16 (FEX II sheet) | 18S TH |
| `stex` | MG STEX (Agray Corridor sketch) | 18S MG |

The exercise decides the sheet. A file on another sheet still imports: the page switches sheets and finishes the import after its reload.

## Higher's half: fill these from the order

| step / key | from the order |
|---|---|
| name / optype | the operation: platoon defense, platoon offense, squad offense (the user's task paragraph decides; ask when it does not) |
| name / name | plan title (unit and exercise) |
| mission / mission | the user's own unit's task paragraph under 3.c Tasks, verbatim, as the mission statement |
| mission / higher | higher's mission (1.b.(1)), the issuing unit's mission (para 2) and intent (3.a), verbatim |
| mission / specified | specified and implied tasks: from the task paragraph, coordinating instructions (back briefs, rehearsals, recon, sketches due, what the platoon must develop), admin (CASEVAC to develop), signal (plan to write) |
| enemy / size, unit, activity, time, equipment | 1.a.(1) composition, disposition, strength |
| enemy / lkl | the last known location grid when 1.a.(1) gives one; a distance from a hill is not a grid and goes into activity |
| enemy / capable, limited | 1.a.(2), one line per capability (defend, reinforce, attack, withdraw, delay) |
| enemy / hemlcoa | 1.a.(3), higher's EMLCOA, verbatim |
| terrain / obs, cover, obst | the Orientation paragraph: observation and fields of fire, cover and concealment, obstacles (named trails and roads with trafficability) |
| terrain / kt, ktnote | key terrain grids when given; named hills without grids go in ktnote |
| terrain / weather | light data and forecast when the order gives them |
| troops / organic, attach | the user's unit; attachments from 1.c and from a tasks paragraph that attaches something |
| troops / m60, m81, pof | supporting fires: positions when given, priority of fires and allocation |
| troops / adjln, adjl, adjrn, adjr | the adjacent units from 1.b.(2) or the other platoons' task paragraphs, name and grid; left and right only when the order says which |
| time / now, exec, timeline, constraints, restraints, log, civil | 3.d timeline (now = order complete or the order's time; exec = the NLT), constraints and restraints named in the order, paragraph 4 logistics, the general situation's civil facts |
| fsp / efst | 3.b.(2) EFST verbatim (task, purpose, method, effects), with the target allocation |
| fsp / fpfwpn | the tube the order gives (60mm or 81mm) when only one is available |
| coord / timeline, other | the timeline again; company control measures with grids (assembly area, CCP, company CP), signals available |
| admin / resupply, epw, c2, casevac | paragraph 4 and 5 facts higher fixes (company CCP, radios, rounds); the platoon's own CASEVAC plan stays out |

## Higher's positions and control measures: put them on the map as objects

Anything the order places with a grid that the guide has no field for goes in facts.json under `objects`, one per item, with the order's own label and the paragraph: the adjacent companies and platoons (inf_company, inf_platoon), a known enemy position (inf_squad or inf_platoon on side enemy; a described location such as "3 km south of Hill 300" may be derived from the sheet and labeled "derived, confirm" in remarks), the company assembly area, CCP and CP (point, ccp, cp), checkpoints, LZs and passage points, phase lines and boundaries (pl, boundary, 2 or more grids), a route higher fixes (route). The page draws each one labeled, on the enemy layer for enemy objects and the control measure layer for lines and areas. Key terrain the order names and the sheet locates (a labeled hill) goes in terrain/kt with the sheet as its source, not as an object; the sheet's own named places already show on the map.

## The planner's half: leave these blank

emlcoa (all), cgcv (all), ea, type, dist, orient, occ, sec, obst, oform, oto, otcm, oseq, parts, tasks, fsp targets tg1 to tg4 and the FPF (fpfc, fpfatt, fpflen, fpftrig), coord engfar and engnear, tcm cps, admin ccp and casroute. `plan_check.py --intake` fails a file that fills any of them. Higher's own EMLCOA, CG and CV belong in mission/higher and enemy/hemlcoa, where the planner reads them while writing their own.

## Shapes

- Text fields: strings; newlines separate items in a list (specified tasks, timeline lines, capabilities).
- Grid fields (place, points, draw, area): 4, 6 or 8 digit grids inside the sheet's square, separated by newlines or spaces.
- Units (sq1 to sq3): `{role, grid}`; targets (tg1 to tg4): `{num, grid, wpn, trigger, obs, task}`. The intake leaves both blank.
- Selects: one of the field's options in guide_fields.json, or "".
