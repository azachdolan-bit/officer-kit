#!/usr/bin/env python3
"""The interview windows MCO 1040.31 sets, computed from the Marine's ECC and EAS.

Usage:  python3 reenlistment_windows.py --ecc <date> [--eas <date>] [--today <date>] [--fmcr]

  dates as 2027-08-19 or "19 August 2027"; --eas defaults to --ecc

Prints, from enclosure (1) chapter 3 paragraph 2.b:
  initial interview        26 to 24 months before ECC   (first term Marines; the Career Planner)
  FTAP or careerist        14 to 12 months before ECC   (Career Planner; the CO's FTAP interview is Part III-B of the contact record)
  EAS interview             8 to  6 months before EAS   (Career Planner and Commanding Officer)
  --fmcr                    4 to 14 months before EAS   (the FMCR request window, paragraph 2.b(3)(f))
and, with --today, the reenlistment type by time remaining (chapter 4 paragraph 1.c): immediate under 90 days,
standard more than three months and less than twelve, early more than 12 months.

The windows are the order's; the dates are arithmetic. Anything else about the case comes from the intake.
"""
import argparse
import datetime as dt
import re
import sys

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def parse(s):
    s = s.strip()
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", s)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r"^(\d{1,2}) ([A-Za-z]+) (\d{4})$", s)
    if m and m.group(2).capitalize() in MONTHS:
        return dt.date(int(m.group(3)), MONTHS.index(m.group(2).capitalize()) + 1, int(m.group(1)))
    raise SystemExit(f"date not understood: {s!r} (use 2027-08-19 or '19 August 2027')")


def minus_months(d, n):
    y, m = d.year, d.month - n
    while m < 1:
        m += 12
        y -= 1
    last = (dt.date(y + (m // 12), (m % 12) + 1, 1) - dt.timedelta(days=1)).day
    return dt.date(y, m, min(d.day, last))


def fmt(d):
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def window(anchor, far, near):
    return f"{fmt(minus_months(anchor, far))} to {fmt(minus_months(anchor, near))}"


def windows(ecc, eas, fmcr=False):
    out = [
        ("Initial interview (26 to 24 months before ECC)", window(ecc, 26, 24)),
        ("FTAP or careerist interview (14 to 12 months before ECC)", window(ecc, 14, 12)),
        ("EAS interview (8 to 6 months before EAS)", window(eas, 8, 6)),
    ]
    if fmcr:
        out.append(("FMCR request (4 to 14 months before EAS)", f"{fmt(minus_months(eas, 14))} to {fmt(minus_months(eas, 4))}"))
    return out


def reenlistment_type(today, ecc):
    days = (ecc - today).days
    if days < 0:
        return f"ECC has passed ({-days} days ago); the Marine must reenlist before midnight of the last day of the current contract (paragraph 1.a)"
    if days < 90:
        return f"immediate: {days} days remaining, under 90 (paragraph 1.c(1))"
    if minus_months(ecc, 12) <= today:
        return f"standard: {days} days remaining, more than three months and less than twelve (paragraph 1.c(2))"
    return f"early: {days} days remaining, more than 12 months; normally authorized only when a duty assignment requires obligated service (paragraph 1.c(3))"


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--ecc", required=True)
    ap.add_argument("--eas")
    ap.add_argument("--today")
    ap.add_argument("--fmcr", action="store_true")
    a = ap.parse_args()
    ecc = parse(a.ecc)
    eas = parse(a.eas) if a.eas else ecc
    print(f"ECC {fmt(ecc)}   EAS {fmt(eas)}   (MCO 1040.31 enclosure (1) chapter 3 paragraph 2.b)")
    for name, w in windows(ecc, eas, a.fmcr):
        print(f"  {name}: {w}")
    if a.today:
        print(f"  Reenlistment type as of {fmt(parse(a.today))}: {reenlistment_type(parse(a.today), ecc)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
