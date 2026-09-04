#!/usr/bin/env python3
"""Reporting senior profile calculator per MCO 1610.7B chapter 8.

Usage:  python3 rs_profile.py ledger.csv [--grade Capt] [--propose D,D,C,D,C,D,C,C,D,C,D,C,D,H]

Ledger columns: grade,label,occasion,date, then 14 attribute letters (A to G, or H for not observed).
Rows with occasion AC, EN, or NO are excluded, as the manual excludes academic, EN, and N/O reports.

Averages: A=1 ... G=7, H excluded, rounded to the nearest hundredth (manual 8.6c).
Relative value: RS average = 90, RS high = 100, linear between them, shown on an 80 to 100 scale (manual 8.7).
The manual gives the anchors, not a formula; the interpolation is this script's.
"""
import csv
import sys

VAL = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7}
EXCLUDE = {"AC", "EN", "NO"}
ATTRS = ["D1 Performance", "D2 Proficiency", "E1 Courage", "E2 Effectiveness under stress", "E3 Initiative",
         "F1 Leading subordinates", "F2 Developing subordinates", "F3 Setting the example",
         "F4 Ensuring well being", "F5 Communication", "G1 PME", "G2 Decision making", "G3 Judgment", "H1 Evaluations"]


def avg(marks):
    vals = [VAL[m] for m in marks if m in VAL]
    return round(sum(vals) / len(vals), 2) if vals else None


def rv(a, rs_avg, rs_high):
    if a is None or rs_avg is None or rs_high is None or rs_high <= rs_avg:
        return None
    v = 90 + 10 * (a - rs_avg) / (rs_high - rs_avg)
    return round(max(80.0, min(100.0, v)), 2)


def third(v):
    if v is None:
        return ""
    return "upper third" if v >= 93.34 else "middle third" if v >= 86.67 else "bottom third"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    grade = sys.argv[sys.argv.index("--grade") + 1] if "--grade" in sys.argv else None
    propose = sys.argv[sys.argv.index("--propose") + 1].upper().split(",") if "--propose" in sys.argv else None

    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    keys = [k for k in rows[0].keys() if k not in ("grade", "label", "occasion", "date")] if rows else []
    if len(keys) != 14:
        sys.exit(f"expected 14 attribute columns after grade,label,occasion,date; found {len(keys)}")
    reports = []
    for r in rows:
        if r.get("occasion", "").upper() in EXCLUDE:
            continue
        if grade and r["grade"].strip().lower() != grade.lower():
            continue
        marks = [r[k].strip().upper() for k in keys]
        reports.append((r["grade"], r["label"], r.get("occasion", ""), r.get("date", ""), marks, avg(marks)))

    print(f"RS PROFILE: {path}" + (f"  grade {grade}" if grade else "  all grades"))
    if not reports:
        print("  no reports in the profile for that grade")
        return 0
    avgs = [a for *_, a in reports if a is not None]
    rs_avg = round(sum(avgs) / len(avgs), 2)
    rs_high, rs_low = max(avgs), min(avgs)
    print(f"  reports: {len(reports)}   RS average: {rs_avg}   high: {rs_high}   low: {rs_low}   spread: {round(rs_high - rs_low, 2)}")
    if len(reports) < 5:
        print("  note: fewer than five reports; each new report moves the anchors, and a follow on report can read as understated (explain in Section I if so)")
    near = sum(1 for a in avgs if abs(a - rs_avg) <= 0.10)
    if len(avgs) >= 4 and near / len(avgs) >= 0.6:
        print(f"  note: {near} of {len(avgs)} reports sit within 0.10 of the average; the profile is compressing and reports lack relative value (manual 8.6b(4)(a))")
    print("  report averages and relative values (linear between RS average = 90 and RS high = 100):")
    for g, lab, occ, d, marks, a in sorted(reports, key=lambda x: -(x[5] or 0)):
        v = rv(a, rs_avg, rs_high)
        print(f"    {a:5.2f}  RV {v if v is not None else '  n/a':>6}  {third(v):<12} {lab} {occ} {d}")
    if propose:
        if len(propose) != 14 or any(m not in VAL and m != "H" for m in propose):
            sys.exit("--propose needs 14 letters A to G or H")
        pa = avg(propose)
        pv = rv(pa, rs_avg, rs_high)
        new_avgs = avgs + [pa]
        new_avg = round(sum(new_avgs) / len(new_avgs), 2)
        new_high = max(rs_high, pa)
        print(f"  proposed report: average {pa}, relative value {pv if pv is not None else 'n/a'} ({third(pv)}) against the current profile")
        print(f"    if added: RS average {rs_avg} -> {new_avg}, high {rs_high} -> {new_high}; RV of the proposed report on the new profile: {rv(pa, new_avg, new_high)}")
        if pa >= rs_high:
            print("    this would be the new high; every earlier report's relative value drops")
        low_marks = [ATTRS[i] for i, m in enumerate(propose) if m in ("A", "B")]
        if low_marks:
            print(f"    marks of A or B on: {', '.join(low_marks)}; the manual expects the Section I word picture to be consistent with them")
    print("  relative value is a boardroom metric; the authoritative figures are on the MBS and the My OMPF tab on MOL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
