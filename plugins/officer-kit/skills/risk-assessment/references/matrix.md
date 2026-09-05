# The matrix the checker uses

MCO 5100.29C Volume 2, Figure 3-4, Joint Risk Assessment Matrix (page 3-8), read from the order on 5 September 2026 and confirmed cell by cell. Columns are probability A (frequent) to E (unlikely); rows are severity I (catastrophic) to IV (negligible). EH extremely high, H high, M medium, L low.

| Severity | A | B | C | D | E |
|---|---|---|---|---|---|
| I   | EH | EH | H | H | M |
| II  | EH | H  | H | M | L |
| III | H  | M  | M | L | L |
| IV  | M  | L  | L | L | L |

Figure 4-2 (page 4-6) outlines IA, IB, IIA, and IIB in red: those four residual levels are high risk training by definition (paragraph 040302). The checker uses the pair for that flag, because the order defines it by the pair.

The order's own worked example (paragraph 030302.C): Catastrophic (I) and Seldom (D) gives HIGH; Critical (II) and Likely (B) gives HIGH. Both match the table.

Approval authority by level (default; the command's own order replaces it in `Overrides/risk-assessment.md`). The order's example echelons (paragraph 040203.A) are for an installation: RAC 1 base commanding officer, RAC 2 base executive officer, RAC 3 division directors, RAC 4 company grade officers and branch heads, RAC 5 SNCO and first line supervisor. The order says designation of risk management authority is determined by the unit commander. The kit's default for an operating force unit:

| Highest residual | Approves |
|---|---|
| IA, IB, IIA, IIB (high risk training) | first O-5 commander in the chain, in writing (paragraph 040304.A); for multiple unit training, each unit's commander |
| any other EH or H | battalion or squadron commander (O-5) |
| M | company commander or OIC (company grade) |
| L | the OIC, or the SNCO in charge of the event |

To replace the matrix with a command's own, put a table with the same shape under a `## Matrix` heading in the override file; `raw_check.py --matrix Overrides/risk-assessment.md` reads it.
