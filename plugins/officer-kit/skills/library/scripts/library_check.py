#!/usr/bin/env python3
"""Inventory a Reference folder and report starter set coverage per module.

Usage:  python3 library_check.py "<Reference folder>" [--modules correspondence,admin,planning,training]
Exit 0 always; this is a report, not a gate.
"""
import os
import re
import sys

STARTER = {
    "correspondence": [("SECNAV M-5216.5", r"5216\.5")],
    "admin": [("MCO 1610.7", r"1610\.7"), ("SECNAV M-1650.1", r"1650\.1"), ("MCO 1500.58", r"1500\.58")],
    "planning": [("MCDP 1", r"MCDP[ _-]?1(?![-\d])"), ("MCDP 1-0", r"MCDP[ _-]?1-0"), ("MCTP 3-10A", r"3-10A")],
    "training": [("MCDP 7", r"MCDP[ _-]?7")],
}
DOC_EXT = (".pdf", ".docx", ".doc", ".pptx", ".md", ".txt")


def page_count(path):
    try:
        from pypdf import PdfReader
        return len(PdfReader(path).pages)
    except Exception:
        return None


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1]
    mods = list(STARTER)
    if "--modules" in sys.argv:
        mods = [m.strip().lower() for m in sys.argv[sys.argv.index("--modules") + 1].split(",")]
    if not os.path.isdir(root):
        print(f"LIBRARY: {root} does not exist. Create it and put your manuals there.")
        return 0
    files = []
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if fn.lower().endswith(DOC_EXT) and not fn.startswith("~$"):
                p = os.path.join(dp, fn)
                files.append((os.path.relpath(p, root), os.path.getsize(p), page_count(p) if fn.lower().endswith(".pdf") else None))
    print(f"LIBRARY: {root}")
    print(f"  documents: {len(files)}")
    for rel, size, pages in sorted(files):
        pg = f"{pages} pp" if pages else ""
        print(f"  {size / 1e6:6.1f} MB  {pg:>7}  {rel}")
    print("  starter set coverage:")
    names = " | ".join(rel for rel, _, _ in files)
    for m in mods:
        for title, pat in STARTER.get(m, []):
            have = re.search(pat, names, re.I) is not None
            print(f"    {'have   ' if have else 'MISSING'}  {m:<15} {title}")
    print("  A missing publication is not an error; the tool that needs it will ask for it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
