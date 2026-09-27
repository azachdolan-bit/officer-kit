#!/usr/bin/env python3
"""Pull the text out of a base order so it can be read paragraph by paragraph. No packages needed.

Usage: python3 order_text.py <order.docx | order.pptx | order.txt | order.md> [--out order.txt]

A .docx gives one line per paragraph (tables included, cells joined with " | "); a .pptx gives one block per slide; a text
file is copied through. The paragraph numbers the order carries stay in the text, so every fact taken from it can be
cited by paragraph. A PDF is captured with capture-source first.
"""
import re
import sys
import zipfile


def docx_text(path):
    z = zipfile.ZipFile(path)
    x = z.read("word/document.xml").decode("utf-8")
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", x, flags=re.S):
        t = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))
        t = t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'")
        if t.strip():
            out.append(t)
    return "\n".join(out)


def pptx_text(path):
    z = zipfile.ZipFile(path)
    names = sorted([n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)], key=lambda n: int(re.findall(r"\d+", n)[-1]))
    out = []
    for n in names:
        t = " | ".join(re.findall(r"<a:t>([^<]*)</a:t>", z.read(n).decode("utf-8")))
        out.append("[%s] %s" % (n.split("/")[-1][:-4], t))
    return "\n".join(out)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    src = argv[1]
    out = None
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    low = src.lower()
    if low.endswith(".docx"):
        text = docx_text(src)
    elif low.endswith(".pptx"):
        text = pptx_text(src)
    elif low.endswith((".txt", ".md")):
        text = open(src, encoding="utf-8").read()
    else:
        print("capture a PDF or image with capture-source first; this reads .docx, .pptx, .txt and .md")
        return 1
    out = out or re.sub(r"\.[a-z]+$", "", src) + ".txt"
    open(out, "w", encoding="utf-8").write(text)
    print("wrote %s: %d lines, %d characters" % (out, text.count("\n") + 1, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
