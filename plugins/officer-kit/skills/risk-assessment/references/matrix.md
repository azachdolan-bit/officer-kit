# The matrix the checker uses

Joint Risk Assessment Matrix, as the order's Figure 3-4 presents it and as the joint and Army risk management publications tabulate it. Columns are probability A (frequent) to E (unlikely); rows are severity I (catastrophic) to IV (negligible). EH extremely high, H high, M medium, L low.

| Severity | A | B | C | D | E |
|---|---|---|---|---|---|
| I   | EH | EH | H | H | M |
| II  | EH | H  | H | M | L |
| III | H  | M  | M | L | L |
| IV  | M  | L  | L | L | L |

High risk training per the order: any residual of IA, IB, IIA, IIB. The checker uses the pair, not the joint level, for that flag, because the order defines it by the pair.

Approval authority by level (default; replace in `Overrides/risk-assessment.md` with the command's own):

| Highest residual | Approves |
|---|---|
| IA, IB, IIA, IIB (high risk training) | first O-5 commander in the chain, in writing |
| any other EH or H | battalion or squadron commander (O-5) |
| M | company commander or OIC (company grade) |
| L | the OIC, or the SNCO in charge of the event |

The command's matrix wins. To replace this one, put a table with the same shape under a `## Matrix` heading in the override file; `raw_check.py --matrix Overrides/risk-assessment.md` reads it. Confirm Figure 3-4 against the user's copy of the order once; the cell values here were not read from the figure itself.
