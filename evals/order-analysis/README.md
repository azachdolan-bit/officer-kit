# order-analysis tests

`order.txt` is fictional and exists only for the harness (`evals/order_analysis_check.py`, 22 items): grid arithmetic against hand values, the direction table, a target number that reads like a grid, one point given two grids, a good analysis that passes, and a bad one that fails on each planted defect (undecoded columns, an invented quote, a hand computed distance, a missing gate record, a sequence finding before the legend, northwest as 5400 mils, a fact with no paragraph, a legend decoded from the kit's own reference).

## Blind test against a real review (27 Sep 26)

A drafter with only the skill and a school platoon defense order (course material, not included here) was asked, as a platoon commander, for METT-TC, the contradictions, and the questions for the company commander. The same order had already been reviewed by hand, with four verified contradictions, three verified runners up, and three known traps.

- **Found 3 of the 4 verified contradictions** (the no comm plan against the blocking task, the mortar direction of fire against the orientation, the defense named two ways), and all three runners up as RFIs (an assembly area never defined, a company "(-)" with nothing detached, an order with zero grids).
- **Found one contradiction the hand review had missed**: a headquarters placed in one location in paragraph 5 and about two kilometers away in paragraph 1.
- **Avoided all three traps**: no sequence finding from the parts columns, northwest as 5600 mils, no fault found in a valid task.
- **Missed one**: a part whose Ends With (enemy neutralized) cannot be produced by the tasks issued (block). The workflow now runs a tasks against end states pass.
- **Took the column decode from the kit's own reference** because the order had no key. The checker now fails that; with no key in the order or the user's material, the columns are an RFI and sequence findings wait.
