# Check before raising

Each of these looked like a defect in a real order review and was not. None is a rule that the thing can never be wrong; each is a question to answer before a finding goes out. `analysis_check.py` warns when a finding's wording matches one.

1. **A tactical task that sounds unusual.** Check MCDP 1-0 appendix C before calling a task invalid. "Protect" is a friendly oriented task there.
2. **Sequence read without the columns decoded.** An execution table in parts places events in time, and its column headings are school or unit terms (one school's set expands to Begins With, Ends With, Critical Events, Conditions Set; the example is not a decode). A task in a later column is not out of order. Decode the order's own legend, or the user's school material, before any sequence finding.
3. **Approximate against precise.** A grid given "approximately" in a narrative paragraph and precisely in the control measure table will differ. Plot from the table. It is a finding only if the difference changes where someone goes or shoots, and then it is an RFI.
4. **A distance or bearing inside the error budget.** Two 6 digit grids are each a 100 meter square; a stated distance within about 141 meters of the computed one is not a contradiction. `grid_tool.py measure` prints the budget.
5. **A direction word converted by hand.** Northwest is 5600 mils, not 5400. Use `grid_tool.py dir`.
6. **A weapon "out of range."** Ranges come from the user's own captures and publications, point and area separately, never from general knowledge. A target inside maximum effective area range is in range.
7. **Priority of fires to a supporting effort.** Priority may follow the importance of a unit's task at that time. Read the intent and the parts before calling it wrong.
8. **Expedient materials.** Obstacles built from local material with the tools issued are doctrinal. A short tool list alone is not a defect; the defect, if any, is a task the resourcing cannot meet.
9. **Resourcing the order does not give.** Do not plan, or fault the order for lacking, machine guns, obstacles, or other assets that paragraph 1.C and paragraph 4 do not provide. Bound the analysis by what the order gives.
10. **A doctrinal form used correctly.** A perimeter built from subordinate battle positions is doctrinal; the contradiction, if any, is in how the order describes it.
