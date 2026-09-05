#!/usr/bin/env python3
"""Find a publication in the user's library and get its text, before anyone goes to the web.

Usage:  python3 find_order.py <number> [--roots <dir> ...] [--text] [--page N --png <out.png>] [--grep <regex>]

  number     an order number as people say it: 5100.29C, "MCO 1900.16", 1553.3, "NAVMC 3500.14", "MARADMIN 056/25"
  --roots    directories to search; default: the Library path and Reference folder named in CLAUDE.md in the
             current folder or its parents, then ./Reference, then the working folder itself
  --text     print the full text (pdftotext -layout) to stdout
  --grep     print the lines matching the regex with 3 lines of context (implies text extraction)
  --page N   render page N to --png (pdftoppm, 110 dpi) so a figure can be read as an image

Exit 0 when found, 1 when not found. When not found, the message says so and names the roots searched,
so the caller can say "not in the library" and only then look elsewhere.

The rule this script exists for: read the order from the user's own library first. The web is for
publications that are not on disk, and the tool says which those were.
"""
import os
import re
import signal
import subprocess
import sys

signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def norm(s):
    s = s.upper().replace("_", " ").replace("-", " ")
    s = re.sub(r"\bW/?CH\b.*", "", s)
    s = re.sub(r"[^A-Z0-9./ ]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def key(s):
    """The number alone: '5100.29C' from 'MCO 5100.29C', 'P1400.32D' -> '1400.32D'."""
    n = norm(s)
    m = re.search(r"(?:P)?(\d{3,5}\.\d+[A-Z]?)", n)
    if m:
        return m.group(1)
    m = re.search(r"(\d{3}/\d{2})", n)
    return m.group(1) if m else n


def candidates(path):
    """A Windows path from the rules file, and where the same folder appears when the session runs
    somewhere else: the Cowork device shell mounts connected folders under $HOME/mnt/<folder name>,
    and the cloud container stages them under /mnt/user-data/uploads/<folder name>."""
    out = [path]
    m = re.match(r"^[A-Za-z]:[\\/](.*)$", path)
    if m:
        rel = m.group(1).replace("\\", "/")
        home = os.path.expanduser("~")
        out.append(os.path.join(home, "mnt", rel))
        out.append(os.path.join("/mnt/user-data/uploads", rel))
    return out


def roots_from_rules(start):
    roots = []
    d = os.path.abspath(start)
    for _ in range(6):
        p = os.path.join(d, "CLAUDE.md")
        if os.path.exists(p):
            for line in open(p, encoding="utf-8", errors="ignore"):
                m = re.search(r"(?:Library path|Publications library|Reference folder)\s*:\s*(.+)", line, re.I)
                if m:
                    v = m.group(1).strip().strip("`").strip()
                    if v and "not recorded" not in v.lower():
                        for cand in candidates(v):
                            if os.path.isdir(cand):
                                roots.append(cand)
                                break
            break
        nd = os.path.dirname(d)
        if nd == d:
            break
        d = nd
    for c in (os.path.join(start, "Reference"), start):
        if os.path.isdir(c):
            roots.append(c)
    return roots


def find(number, roots):
    k = key(number)
    base = k.rstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    hits, near = [], []
    for r in roots:
        for dp, dn, fn in os.walk(r):
            dn[:] = [x for x in dn if not x.startswith(".") and x not in ("node_modules", "__pycache__", "_build")]
            for f in fn:
                if not f.lower().endswith((".pdf", ".txt", ".md", ".docx")):
                    continue
                fk = norm(f)
                if k in fk:
                    hits.append(os.path.join(dp, f))
                elif base and re.search(re.escape(base) + r"[A-Z]?\b", fk):
                    near.append(os.path.join(dp, f))
    return hits, near


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    number = sys.argv[1]
    args = sys.argv[2:]
    roots = []
    if "--roots" in args:
        i = args.index("--roots") + 1
        while i < len(args) and not args[i].startswith("--"):
            roots.append(args[i]); i += 1
    if not roots:
        roots = roots_from_rules(os.getcwd())
    hits, near = find(number, roots)
    if not hits and near:
        print(f"no exact match for {number}; a different edition is in the library:")
        for n in near:
            print(f"  {n}")
        print("Use the edition on disk and say so, or download the current one into Reference.")
        return 1
    if not hits:
        print(f"NOT IN THE LIBRARY: {number}. Searched: {'; '.join(roots) or 'no roots (no CLAUDE.md with a Library path, no Reference folder)'}")
        print("Say that it is not on disk, then and only then read it from the web, and mark what came from the web.")
        return 1
    hits = sorted(set(hits), key=len)
    path = hits[0]
    print(f"FOUND: {path}")
    if len(hits) > 1:
        for h in hits[1:]:
            print(f"  also: {h}")
    if "--page" in args:
        n = args[args.index("--page") + 1]
        out = args[args.index("--png") + 1] if "--png" in args else f"page{n}"
        out = re.sub(r"\.png$", "", out)
        subprocess.run(["pdftoppm", "-f", n, "-l", n, "-r", "110", "-png", path, out], check=True)
        print(f"rendered page {n} to {out}-*.png; read it as an image")
    if ("--text" in args or "--grep" in args) and path.lower().endswith(".pdf"):
        text = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
        if "--grep" in args:
            pat = re.compile(args[args.index("--grep") + 1], re.I)
            lines = text.splitlines()
            for i, l in enumerate(lines):
                if pat.search(l):
                    print(f"--- line {i + 1}")
                    print("\n".join(lines[max(0, i - 3):i + 4]))
        else:
            print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
