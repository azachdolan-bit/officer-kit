#!/usr/bin/env python3
"""The JEPES dates MCO 1616.1 sets, computed from an occasion and a date.

Usage:  python3 jepes_dates.py --occasion SA --to <date>            the semiannual or annual period that ends on that date
        python3 jepes_dates.py --occasion SA --date <date>          the semiannual period a date falls in
        python3 jepes_dates.py --occasion <code> --to <date> [--from <date>]   an event driven occasion
        python3 jepes_dates.py --supervision <date>                 the initial counseling due date

  dates as 2026-07-31 or "31 July 2026"

Prints, from enclosure (1):
  the occasion's FROM and TO dates (chapter 2 paragraph 2.b; SA runs 1 February to 31 July and 1 August to 31 January, AN 1 January to 31 December)
  the day recommended marks may first be submitted, 45 days before the TO date (chapter 1 paragraphs 3.c and 6.c)
  the Approver's completion due date, the TO date (chapter 2 paragraph 2.e)
  the observation length against the 30 day minimum (chapter 2 paragraph 2.c)
  with --supervision, the date the FLS's initial written counseling is due, 30 days after the relationship was established (chapter 2 paragraph 1.b(1))

The dates are the order's; the arithmetic is the script's. Anything else about the case comes from the intake.
"""
import argparse
import datetime as dt
import re
import sys

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# The order's occasions, chapter 2 paragraph 2.b, with the TO date rule as the order states it.
# fixed: (from_day, from_month, to_day, to_month) pairs the order fixes; None where the event sets the date.
OCCASIONS = {
    "PR": {"name": "Promotion", "to": "The day prior to the MRO's new date of rank", "fixed": None},
    "TR": {"name": "Transfer", "to": "The MRO's date of transfer", "fixed": None},
    "CD": {"name": "Change of Primary Duty", "to": "Date prior to the date of change of duty", "fixed": None},
    "TD": {"name": "To TAD", "to": "The MRO's date of departure to TAD", "fixed": None},
    "TC": {"name": "TAD Complete", "to": "The MRO's date of departure from TAD site", "fixed": None},
    "AN": {"name": "Annual", "to": "31 December", "fixed": [((1, 1), (31, 12))]},
    "SA": {"name": "Semi-Annual", "to": "31 July/31 January", "fixed": [((1, 2), (31, 7)), ((1, 8), (31, 1))]},
    "AT": {"name": "Completion of Annual Training", "to": "Last day of annual training", "fixed": None},
    "DC": {"name": "Discharge", "to": "Day before discharge", "fixed": None},
    "RD": {"name": "Reduction", "to": "Last day at previous rank", "fixed": None},
    "DD": {"name": "Declared Deserter", "to": "First day Marine in Deserter Status", "fixed": None},
    "RT": {"name": "Active Duty Operational Support", "to": "Last day of ADOS", "fixed": None},
}
SUBMIT_DAYS = 45
MIN_OBSERVATION = 30
COUNSELING_DAYS = 30


def parse(s):
    s = s.strip()
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", s)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r"^(\d{1,2}) ([A-Za-z]+) (\d{4})$", s)
    if m and m.group(2).capitalize() in MONTHS:
        return dt.date(int(m.group(3)), MONTHS.index(m.group(2).capitalize()) + 1, int(m.group(1)))
    raise SystemExit(f"date not understood: {s!r} (use 2026-07-31 or '31 July 2026')")


def fmt(d):
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def fixed_period_for(code, to):
    """The order's FROM date for a fixed period occasion (SA, AN) ending on `to`, or None when `to` is not a TO date the order fixes."""
    for (fd, fm), (td, tm) in OCCASIONS[code]["fixed"]:
        if (to.day, to.month) == (td, tm):
            year = to.year - 1 if fm > tm else to.year
            return dt.date(year, fm, fd)
    return None


def period_containing(code, date):
    """The fixed period (SA or AN) a date falls in."""
    for (fd, fm), (td, tm) in OCCASIONS[code]["fixed"]:
        for year in (date.year - 1, date.year, date.year + 1):
            start = dt.date(year, fm, fd)
            end = dt.date(year + 1 if fm > tm else year, tm, td)
            if start <= date <= end:
                return start, end
    return None


def lines(code, start, end):
    out = [f"{code} ({OCCASIONS[code]['name']}): {fmt(start)} to {fmt(end)}"]
    out.append(f"submit no earlier than: {fmt(end - dt.timedelta(days=SUBMIT_DAYS))}   ({SUBMIT_DAYS} days before the TO date, chapter 1 paragraph 6.c)")
    out.append(f"Approver's completion due date: {fmt(end)}   (chapter 2 paragraph 2.e; delinquent after it)")
    days = (end - start).days + 1
    note = "" if days >= MIN_OBSERVATION else f"   under the {MIN_OBSERVATION} day minimum, chapter 2 paragraph 2.c (service schools under 30 days excepted)"
    out.append(f"observation: {days} days{note}")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--occasion", choices=sorted(OCCASIONS), help="the order's occasion code")
    ap.add_argument("--to", help="the TO date")
    ap.add_argument("--from", dest="from_", help="the FROM date (event driven occasions; defaults to the day after the previous occasion, which the intake supplies)")
    ap.add_argument("--date", help="a date inside a fixed period (SA or AN)")
    ap.add_argument("--supervision", help="the date the reporting relationship was established")
    a = ap.parse_args()
    out = []
    if a.occasion:
        code = a.occasion
        if OCCASIONS[code]["fixed"]:
            if a.to:
                to = parse(a.to)
                start = fixed_period_for(code, to)
                if start is None:
                    raise SystemExit(f"{fmt(to)} is not a TO date the order fixes for {code}; {code} ends {OCCASIONS[code]['to']} (chapter 2 paragraph 2.b)")
                if a.from_:
                    f = parse(a.from_)
                    if not (start <= f <= to):
                        raise SystemExit(f"FROM {fmt(f)} is outside the {code} period {fmt(start)} to {fmt(to)}")
                    start = f
                out += lines(code, start, to)
            elif a.date:
                p = period_containing(code, parse(a.date))
                out += lines(code, *p)
            else:
                raise SystemExit("give --to or --date for SA or AN")
        else:
            if not a.to:
                raise SystemExit(f"{code} needs --to: {OCCASIONS[code]['to']} (chapter 2 paragraph 2.b)")
            to = parse(a.to)
            if a.from_:
                out += lines(code, parse(a.from_), to)
            else:
                out.append(f"{code} ({OCCASIONS[code]['name']}): TO {fmt(to)}, the order's rule: {OCCASIONS[code]['to']}")
                out.append("FROM date: the day following the last day of the previous occasion (chapter 2 paragraph 2.b); give it with --from")
    if a.supervision:
        s = parse(a.supervision)
        out.append(f"initial written counseling due: {fmt(s + dt.timedelta(days=COUNSELING_DAYS))}   ({COUNSELING_DAYS} days after the relationship was established {fmt(s)}, chapter 2 paragraph 1.b(1))")
    if not out:
        ap.print_help()
        return 2
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as ex:
        if isinstance(ex.code, str):
            print(ex.code)
            sys.exit(1)
        raise
