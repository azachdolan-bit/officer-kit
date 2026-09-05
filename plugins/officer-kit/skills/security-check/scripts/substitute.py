#!/usr/bin/env python3
"""Put a name back into a finished product, on the user's own computer, at the last step.

Usage:  python3 substitute.py <file.docx|file.txt|file.md> --label "<MARINE>" [--out file]
The name is asked for on the terminal and is never written anywhere except the output file.
Case forms are handled: <MARINE> -> "Sergeant J. M. Okafor" as typed; <MARINE_CAPS> -> the same in capitals;
<LAST> -> the last word of the name; <LAST_CAPS> -> the last word in capitals.

Why: the tools work on a label so that another Marine's name never travels through a commercial model or
sits in a saved draft. This script is the only place the name meets the document.
"""
import getpass
import os
import re
import sys
import zipfile


def forms(label, name):
    base = label.strip("<>")
    last = name.split()[-1] if name.split() else name
    return {
        f"<{base}>": name,
        f"<{base}_CAPS>": name.upper(),
        "<LAST>": last,
        "<LAST_CAPS>": last.upper(),
        f"<{base}'S>": name + "'s",
        f"<{base}'S_CAPS>": name.upper() + "'S",
    }


def sub_text(text, table, xml=False):
    for k, v in table.items():
        if xml:
            v = v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            text = text.replace(k.replace("<", "&lt;").replace(">", "&gt;"), v)
        text = text.replace(k, v)
    return text


def sub_docx(src, dst, table):
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith("word/") and item.filename.endswith(".xml"):
                text = data.decode("utf-8")
                # placeholders may be split across runs; collapse the common split of "<" "MARINE" ">" is not attempted;
                # build_letter writes each placeholder inside one run, so a straight replace works.
                text = sub_text(text, table, xml=True)
                data = text.encode("utf-8")
            zout.writestr(item, data)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    label = sys.argv[sys.argv.index("--label") + 1] if "--label" in sys.argv else "<MARINE>"
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else re.sub(r"(\.[^.]+)$", r" named\1", src)
    name = getpass.getpass("Name as it should print (not echoed, not stored): ").strip()
    if not name:
        sys.exit("no name given; nothing written")
    table = forms(label, name)
    if src.lower().endswith(".docx"):
        sub_docx(src, out, table)
    else:
        text = open(src, encoding="utf-8").read()
        open(out, "w", encoding="utf-8").write(sub_text(text, table))
    remaining = 0
    if not src.lower().endswith(".docx"):
        remaining = len(re.findall(r"<[A-Z_']+>", open(out, encoding="utf-8").read()))
    print(f"wrote {out}" + (f"; {remaining} placeholder(s) still present" if remaining else ""))
    print("The original with the label is unchanged. Delete the named copy when it has been submitted.")


if __name__ == "__main__":
    main()
