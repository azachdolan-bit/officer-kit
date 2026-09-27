# The sand table export

The virtual sand table (a browser page a unit or school shares by link) exports two files from its Plan menu. Either one, or both, is what the user attaches.

## `<name>.sandtable.json` (Export file): the whole plan

One JSON object. The keys that matter to an order:

- `name`, `sheet` (which map sheet: the reader maps the id to its grid zone and 100 km square), `aoi` (`e0, n0, e1, n1` UTM corners of the area of operations), `notes`.
- `guide.values`: one object per guided step the planner applied, keyed by step id. Every field the planner filled is here as a string, or as a small object for a unit (`{role, grid}`) or a target (`{num, grid, wpn, trigger, obs, task}`). Grids typed by the planner are 8 digit strings inside the sheet's 100 km square. Multi point drawings are grids separated by newlines.
- `guide.typed`: text the planner typed on a step and never pressed Apply on. It is theirs; use it and mark it "(typed, not applied)".
- `objects[]`: everything on the map. Each has `id` (guide owned objects have stable ids, `g_...`), `label`, `symbol`, `side` (friendly, enemy, neutral), `kind` (point, line, area), `utm` (a list of `[E, N]` metres), and `props`: `task`, `purpose`, `remarks`, and for units and weapons `sector` (`{kind: primary | alternate | supplementary, left, right, range, fpl: {az, len}, pdf: {az, len}}`, azimuths in grid degrees).
- `routes[]`: `name`, `points` (UTM), `pace_kmh`, `notes`.
- `phases[]`: the parts, each with `events[]` (`name`, `trigger`, `narration`); the guide writes the begins with, critical events and ends with as events.

Step ids and what they hold (the reader prints them under these titles): name (operation type, title, notes), ao, mission (mission statement, higher mission and intent, specified and implied tasks), enemy (how sure, size, last known location, activity, unit, time, equipment, capable, limited), terrain (observation, cover, obstacles, weather, key terrain, avenues aa1 to aa3), troops (organic, mortars m60 and m81, adjacent adjl and adjr, fires), time (pace, one third line, gate), emlcoa (avenue used, size, enemy mission, current activity, actions on contact, enemy objective), cgcv (cg, cv, exploitation, form). Defense: ea (engagement area, trigger lines, TRP, why), type (type and method, BP centre, frontage, depth), dist (squads with roles, CP, guns, alternate and supplementary positions, attachments), orient (azimuth, statement), occ (ORP, SRP, method, statement), tcm (LZ, checkpoints), sec (LP/OP, security statement), obst (wire, minefield, existing, engineer). Offense: oform (type of attack, form of manoeuvre, statement, objective, enemy orientation), oto (squads with roles, machine guns, task organisation statement), otcm (assembly area, LD, ORP, SBF cold and hot, assault position, PLD, MSLs, LOA, TRP, routes r1 to r3), oseq (initiation, sequence of events, the five signals, displacement method and criteria). Then parts (p1 to p4: name, begins with, critical events, ends with, conditions set), tasks (t1 to t3 squad tasks, MG statement mgrel, mgunit, mgcond, mgtask, mgtarget, mgpurpose, mgbpt, mggrid), fsp (EFST, targets tg1 to tg4, FPF centre, attitude, length, delivery, trigger), coord (timeline, engagement criteria far and near, other), admin (CCP, CASEVAC route, CASEVAC, EPW, resupply, C2).

## `<name>.sandtable-brief.md` (Export brief for Claude): the plain text

The same plan as prose: every step's values, every check the sand table ran with its level (ok, note, warn) and its source, everything on the map with grids, and every route with legs in distance, magnetic and grid azimuth and minutes at the planning pace. It carries two things the JSON does not: the checks, and magnetic azimuths (the sheet's declination lives on the page). The reader takes both from it when it is given.

## Grids

`plan_reader.py` derives every grid from UTM in code: the 8 digit grid is the 10 metre easting and northing inside the 100 km square. Distances and grid azimuths between points are computed the same way. Magnetic azimuths come only from the brief; without it the order says grid.
