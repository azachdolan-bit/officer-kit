#!/usr/bin/env python3
"""Run the study-guide gates on a spec before anything is built from it.

Usage: python3 gates.py <spec.json> <source file> [<source file> ...] [--cover 0.6] [--min 0.97] [--report <file.md>]

Gate 1 coverage: source sentences carried by the product (at least --min, default 0.97, of all
       sentences not excluded in the spec with a reason). Every missing sentence is printed; read each
       one and either carry it or exclude it with a reason. Calibrated on four real walkthroughs whose
       "Read it as issued" blocks carry the whole source: 97 to 99 percent at --cover 0.6.
Gate 2 traceability: every quiz answer is learnable from its own section (the final section from all).
Gate 3 quiz rules: four filled, distinct options; answer text verified; balanced, unrepeated positions;
       an explanation and a difficulty on every question; no duplicate questions; no dashes.
Exit 0 only when all three pass. With --report the result is saved as the gate artifact the
delivered product names (kit standard: a gate that leaves no artifact did not run)."""
import os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import study_lib as L

def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cover, need, report, files = 0.6, 0.97, None, []
    it = iter(argv[1:])
    for a in it:
        if a == "--cover": cover = float(next(it))
        elif a == "--min": need = float(next(it))
        elif a == "--report": report = next(it)
        else: files.append(a)
    spec = L.balance(L.load(files[0]))
    srcs = [open(f, encoding="utf-8", errors="replace").read() for f in files[1:]]
    out, bad = [], False
    got, tot, miss = L.coverage(spec, srcs, cover)
    pct = 100.0 * got / tot if tot else 0.0
    condensed = spec.get("mode") in ("handout", "whiteboard")
    ok1 = condensed or (tot > 0 and got / tot >= need)
    out.append("GATE 1 coverage: %d of %d source sentences carried (%.1f%%) %s" % (got, tot, pct, "REPORT ONLY (condensed format): read every missing line" if condensed else ("PASS" if ok1 else "FAIL")))
    for m in miss[:40]:
        out.append("   missing: " + m[:160])
    if len(miss) > 40: out.append("   ... and %d more" % (len(miss) - 40))
    fl = L.trace(spec)
    out.append("GATE 2 traceability: %d answers not learnable from their section %s" % (len(fl), "PASS" if not fl else "FAIL"))
    for f in fl: out.append("   %s | %s | answer: %s" % f)
    qf, qw = L.quiz_fails(spec)
    dh = L.dash_hits(spec)
    if dh: qf.append("em or en dash in: " + ", ".join(dh))
    out.append("GATE 3 quiz rules: %d failures %s" % (len(qf), "PASS" if not qf else "FAIL"))
    for f in qf: out.append("   " + f)
    for w in qw: out.append("   warn: " + w)
    bad = not (ok1 and not fl and not qf)
    out.append("RESULT: %s" % ("CLEAN" if not bad else "NOT CLEAN"))
    text = "\n".join(out)
    print(text)
    if report:
        with open(report, "w", encoding="utf-8") as fh:
            fh.write("# Gate report\n\nSpec: %s\nSources: %s\nRun: %s\n\n```\n%s\n```\n" % (
                os.path.basename(files[0]), ", ".join(os.path.basename(f) for f in files[1:]),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), text))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
