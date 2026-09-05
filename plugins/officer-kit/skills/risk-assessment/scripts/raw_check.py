#!/usr/bin/env python3
"""Check a Risk Assessment Worksheet (raw.md from the SKILL's template) against MCO 5100.29C Vol 2.

Usage:  python3 raw_check.py raw.md [--matrix <file with a ## Matrix table>]
Exit 0 = passes (warnings allowed); 1 = arithmetic error, missing required element, or a flag that
disagrees with the residual levels.

Checks: every hazard row has a phase, severity I to IV, probability A to E; initial and residual
levels match the matrix; residual is not worse than initial; no residual improvement without a control;
controls carry a verb of change (warn otherwise); severity drops need a stated reason (warn);
high risk flag equals "any residual in IA, IB, IIA, IIB"; the four required elements present when high
risk; the approval line names the O-5 when high risk; blocked content and names (fail).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import blocked_hits, dashes  # noqa: E402

DEFAULT_MATRIX = {
    "I": {"A": "EH", "B": "EH", "C": "H", "D": "H", "E": "M"},
    "II": {"A": "EH", "B": "H", "C": "H", "D": "M", "E": "L"},
    "III": {"A": "H", "B": "M", "C": "M", "D": "L", "E": "L"},
    "IV": {"A": "M", "B": "L", "C": "L", "D": "L", "E": "L"},
}
RANK = {"EH": 4, "H": 3, "M": 2, "L": 1}
SEV_ORDER = ["I", "II", "III", "IV"]
PROB_ORDER = ["A", "B", "C", "D", "E"]
HIGH_RISK = {"IA", "IB", "IIA", "IIB"}
CONTROL_VERBS = r"\b(?:checks?|holds?|confirms?|positions?|staffs?|limits?|requires?|rehears\w*|inspects?|stages?|clears?|marks?|licens\w*|walks?|escorts?|posts?|ground guides?|closes?|removes?|separates?|reduces?|only)\b"
NOT_CONTROL = r"\b(?:brief\w*|remind\w*|ensure\w*|emphasi\w*|be aware|stress\w*|encourag\w*)\b"
GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj)"


def load_matrix(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^## Matrix\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    block = m.group(1) if m else text
    matrix = {}
    for line in block.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and cells[0] in SEV_ORDER:
            matrix[cells[0]] = dict(zip(PROB_ORDER, cells[1:]))
    return matrix if len(matrix) == 4 else None


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    matrix = DEFAULT_MATRIX
    if "--matrix" in sys.argv:
        loaded = load_matrix(sys.argv[sys.argv.index("--matrix") + 1])
        if loaded:
            matrix = loaded
        else:
            print("  WARN  no usable ## Matrix table in the file given; using the joint matrix")
    text = open(path, encoding="utf-8").read()
    fails, warns = [], []

    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 10 and re.fullmatch(r"\d+", cells[0]):
            rows.append(cells)
    if not rows:
        fails.append("no hazard rows found (numbered rows in the Hazards table)")

    residuals = []
    for c in rows:
        n, phase, hazard, sev, prob, init, controls, rsev, rprob, resid = c[:10]
        tag = f"hazard {n}"
        if not phase:
            fails.append(f"{tag}: no phase")
        if len(hazard.split()) < 4:
            warns.append(f"{tag}: hazard is a category, not a mechanism ('{hazard}'); name what happens, in which phase, under what condition")
        ok = True
        for label, s, p in (("initial", sev, prob), ("residual", rsev, rprob)):
            if s not in SEV_ORDER or p not in PROB_ORDER:
                fails.append(f"{tag}: {label} severity or probability not in I to IV / A to E ({s}{p})")
                ok = False
        if not ok:
            continue
        if init != sev + prob:
            fails.append(f"{tag}: initial level column says {init}; severity and probability give {sev}{prob}")
        if resid != rsev + rprob:
            fails.append(f"{tag}: residual level column says {resid}; residual severity and probability give {rsev}{rprob}")
        li, lr = matrix[sev][prob], matrix[rsev][rprob]
        if RANK[lr] > RANK[li] or SEV_ORDER.index(rsev) < SEV_ORDER.index(sev) or PROB_ORDER.index(rprob) < PROB_ORDER.index(prob):
            fails.append(f"{tag}: residual ({rsev}{rprob}) is worse than initial ({sev}{prob})")
        improved = (rsev, rprob) != (sev, prob)
        has_control = bool(controls.strip()) and controls.strip().lower() not in ("none", "n/a")
        if improved and not has_control:
            fails.append(f"{tag}: residual improved with no control listed")
        if has_control:
            if not re.search(CONTROL_VERBS, controls, re.I):
                warns.append(f"{tag}: controls carry no verb of change ('{controls[:50]}...'); a control is something someone does at a time")
            if re.search(NOT_CONTROL, controls, re.I) and not re.search(CONTROL_VERBS, controls, re.I):
                warns.append(f"{tag}: 'brief', 'ensure', 'remind' describe an intention, not a control")
            if not re.search(r"\b(?:RSO|OIC|corpsman|sergeant|chief|safety|safeties|leader|driver|operator|NCO|platoon|section|squad|instructor)\b", controls, re.I):
                warns.append(f"{tag}: controls do not say who implements them")
        if SEV_ORDER.index(rsev) > SEV_ORDER.index(sev):
            warns.append(f"{tag}: severity dropped from {sev} to {rsev}; severity rarely changes, state the reason (different distance, barrier, PPE) in the controls")
        residuals.append((n, rsev + rprob, lr))

    if residuals:
        worst = max(residuals, key=lambda r: (RANK[r[2]], -SEV_ORDER.index(r[1][:-1]), -PROB_ORDER.index(r[1][-1])))
        hr = any(r[1] in HIGH_RISK for r in residuals)
        m = re.search(r"Highest residual level:\s*([IV]+[A-E])", text)
        if not m:
            fails.append("no 'Highest residual level:' line")
        else:
            worst_pairs = {r[1] for r in residuals if r[2] == worst[2]}
            if m.group(1) not in worst_pairs:
                fails.append(f"highest residual line says {m.group(1)}; the rows give {', '.join(sorted(worst_pairs))} at level {worst[2]}")
        f = re.search(r"High risk training:\s*(yes|no)", text, re.I)
        if not f:
            fails.append("no 'High risk training: yes|no' line")
        elif (f.group(1).lower() == "yes") != hr:
            fails.append(f"high risk training line says {f.group(1)}; the residual levels say {'yes' if hr else 'no'} (IA, IB, IIA, IIB after controls)")
        a = re.search(r"Approval authority:\s*(.+)", text)
        if not a:
            fails.append("no 'Approval authority:' line")
        elif hr and not re.search(r"O-5|battalion commander|squadron commander|lieutenant colonel|commanding officer", a.group(1), re.I):
            fails.append("high risk training; the approval line must name the first O-5 commander in the chain, in writing")
        if hr:
            for elem, pat in (("Emergency action plan", r"^## Emergency action plan"), ("Cease training and training time out", r"^## Cease training"), ("Communications", r"^## Communications"), ("Pre execution checklist", r"^## Pre execution checklist")):
                mm = re.search(pat + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
                if not mm or len(mm.group(1).strip()) < 40:
                    fails.append(f"high risk training requires a {elem} section with content (order paragraph 040304.B)")
                elif elem == "Emergency action plan":
                    eap = mm.group(1)
                    for need, pat in (("primary and alternate communications", r"communicat|net|radio"), ("telephone numbers", r"\d{3}[-. ]\d{4}|number"), ("location of emergency response personnel and equipment", r"location|at the |ECP|corpsman"), ("muster site and control of the scene", r"muster|scene"), ("equipment shutdown", r"shutdown|shut down|cease|stop")):
                        if not re.search(pat, eap, re.I):
                            warns.append(f"EAP minimum content (040304.B.1): {need} not found")
    if not re.search(r"^## Supervision", text, re.M):
        warns.append("no Supervision section: who watches each control and the stop trigger (step five of the order)")

    for mm in re.finditer(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]+", text):
        fails.append(f"a name appears to be in the sheet ('{mm.group(0)}'); billets only, names on the signature block")
        break
    for b in blocked_hits(text, allow=("medical",)):
        fails.append(f"blocked content: {b}")
    if dashes(text):
        fails.append("em or en dash present")

    print(f"RAW CHECK: {path}  {len(rows)} hazards")
    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    if not warns and not fails:
        print("  clean")
    print(f"  -> {len(fails)} failures, {len(warns)} warnings")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
