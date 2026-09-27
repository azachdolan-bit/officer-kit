#!/usr/bin/env python3
"""Check an order analysis before anyone reads it.

Usage: python3 analysis_check.py <analysis.json> <order.txt>

Fails when:
- a quote is not in the order word for word (whitespace and quote marks normalized)
- a contradiction lacks two quotes, or both quotes are the same passage
- a computed distance or azimuth does not match grid_tool for the grids named
- a stated versus computed gap is inside the grids' error budget
- a direction word is given the wrong mils value
- the order uses column abbreviations (BW, EW, CE, CS, or any declared in the legend) and the analysis
  has no legend decoding them from the order or the user's material, or a sequence finding comes
  without one
- a finding carries no consequence, or no Gate 0 and Gate 1 verdicts (a gate with no record did not run)
- a METT-T fact carries no locator or quote
Warns when a finding's claim matches the not-a-defect list in references/not-a-defect.md."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid_tool as G

def norm(s):
    s = (s or "").replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return re.sub(r"\s+", " ", s).strip().lower()

NOT_DEFECT = [
    (r"\bprotect\b.*\b(not|invalid|isn't)\b.*\btask\b", "protect is a tactical task in MCDP 1-0 appendix C"),
    (r"\bpriority of fires?\b.*\b(supporting effort|SE)\b.*\b(wrong|error|should)\b", "priority of fires may go to a supporting effort when its task matters most; check the intent first"),
    (r"\b(shovel|pick|pickaxe|expedient)\b.*\bobstacle", "expedient obstacles from local material are doctrinal; the tool count alone is not a defect"),
    (r"\bapproximate(ly)?\b.*\bgrid", "a grid marked approximate in a narrative paragraph is expected to differ from the control measure table; plot from the table and raise an RFI only if the difference changes an action"),
]

def main(ap, op):
    A = json.load(open(ap, encoding="utf-8"))
    order = open(op, encoding="utf-8", errors="replace").read()
    O = norm(order)
    fails, warns = [], []
    def q_ok(q, where):
        if not q or not q.get("quote"):
            fails.append(where + ": no quote"); return
        if norm(q["quote"]) not in O:
            fails.append(where + ": quote not in the order word for word: " + q["quote"][:70])
        if not q.get("loc"):
            fails.append(where + ": no locator (paragraph)")
    legend = {norm(x.get("term")): x for x in A.get("legend", [])}
    used = set(re.findall(r"\b(BW|EW|CE|CS)\b", order))
    for t in used:
        if norm(t) not in legend:
            fails.append("the order uses %s; decode it in 'legend' from the order's own key or the user's material before judging sequence" % t)
    for t, x in legend.items():
        if not x.get("meaning") or not x.get("source"):
            fails.append("legend %s: needs meaning and source" % t)
        elif re.search(r"not-a-defect|references/|the kit|plugin", x["source"], re.I):
            fails.append("legend %s: decoded from the kit's own reference; decode it from the order or the user's material, or make it an RFI and hold sequence findings" % t)
    for i, f in enumerate(A.get("facts", []), 1):
        if f.get("factor") not in ("Mission", "Enemy", "Terrain and weather", "Troops and support available", "Time available", "Civil considerations"):
            fails.append("fact %d: factor must be one of the METT-T factors (or Civil considerations)" % i)
        q_ok(f, "fact %d" % i)
    for f in A.get("findings", []):
        tag = "finding %s" % f.get("n", "?")
        if not f.get("consequence"): fails.append(tag + ": no consequence (what a subordinate would do wrong)")
        for g in ("gate0", "gate1"):
            if not f.get(g): fails.append(tag + ": no %s verdict recorded" % g)
        if f.get("type") == "contradiction":
            q_ok(f.get("a"), tag + " side a"); q_ok(f.get("b"), tag + " side b")
            if f.get("a") and f.get("b") and norm(f["a"].get("quote")) == norm(f["b"].get("quote")) and f["a"].get("loc") == f["b"].get("loc"):
                fails.append(tag + ": both sides are the same passage")
        elif f.get("type") in ("geometry", "omission", "sequence"):
            if f.get("a"): q_ok(f["a"], tag)
        else:
            fails.append(tag + ": type must be contradiction, geometry, sequence, or omission")
        if f.get("type") == "sequence" and not legend and used:
            fails.append(tag + ": a sequence finding before the order's columns are decoded")
        for c in f.get("computed", []):
            try:
                m = G.measure(c["from"], c["to"])
            except ValueError as e:
                fails.append(tag + ": " + str(e)); continue
            if "distance_m" in c and abs(c["distance_m"] - m["distance_m"]) > 1:
                fails.append(tag + ": distance %s to %s is %d m, not %d" % (c["from"], c["to"], m["distance_m"], c["distance_m"]))
            if "azimuth_mils" in c and abs(c["azimuth_mils"] - m["azimuth_mils"]) > 1:
                fails.append(tag + ": azimuth %s to %s is %d mils, not %d" % (c["from"], c["to"], m["azimuth_mils"], c["azimuth_mils"]))
            if "stated_distance_m" in c and abs(c["stated_distance_m"] - m["distance_m"]) <= m["error_budget_m"]:
                fails.append(tag + ": stated %d m vs computed %d m is inside the %d m error budget; not a finding" % (c["stated_distance_m"], m["distance_m"], m["error_budget_m"]))
            if "stated_azimuth_mils" in c:
                gap = abs((c["stated_azimuth_mils"] - m["azimuth_mils"] + 3200) % 6400 - 3200)
                if gap <= m["azimuth_error_mils"]:
                    fails.append(tag + ": stated azimuth is within the %d mil error budget; not a finding" % m["azimuth_error_mils"])
        for d in f.get("directions", []):
            if G.dir_mils(d["word"]) != d["mils"]:
                fails.append(tag + ": %s is %d mils, not %d" % (d["word"], G.dir_mils(d["word"]), d["mils"]))
        for pat, why in NOT_DEFECT:
            if re.search(pat, f.get("claim", ""), re.I):
                warns.append(tag + ": check the not-a-defect list: " + why)
    if not A.get("rfis"): warns.append("no RFIs listed; an order with nothing to ask is rare")
    print("ANALYSIS CHECK: %d facts, %d findings, %d RFIs" % (len(A.get("facts", [])), len(A.get("findings", [])), len(A.get("rfis", []))))
    for x in fails: print("  FAIL ", x)
    for x in warns: print("  warn ", x)
    print("  clean" if not fails else "  NOT CLEAN")
    return 1 if fails else 0

if __name__ == "__main__":
    if len(sys.argv) != 3: sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
