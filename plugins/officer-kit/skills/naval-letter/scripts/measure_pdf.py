#!/usr/bin/env python3
"""Measure the rendered PDF of a naval letter. Never eyeball line pitch.

The standard counts LINES on a 13.8 pt pitch. This script reads word positions with
`pdftotext -bbox`, groups them into lines, and checks:

  1. every vertical gap between consecutive lines on a page is a whole number of pitches
  2. the named gaps match the standard (date to From 27.6, To to Subj 27.6, Subj to Ref 27.6,
     Ref to Encl 27.6, Encl to paragraph 1 27.6, last text line to signature 55.2)
  3. the signature line starts at page centre (x about 306 pt)
  4. on continuation pages the Subj line sits on the sixth line (about 82.8 pt from the top of
     the page) and the body resumes on the second line below it

Usage:  python3 measure_pdf.py letter.pdf
Exit 0 = every measured gap within tolerance, 1 = a defect.
Requires pdftotext (poppler).
"""
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

PITCH = 13.8
TOL = 0.9          # points; LibreOffice and Word disagree by fractions of a point
PAGE_CENTRE = 306.0


def lines_for_page(page):
    ns = {"x": "http://www.w3.org/1999/xhtml"}
    words = []
    for w in page.iter("{http://www.w3.org/1999/xhtml}word"):
        words.append((float(w.get("yMin")), float(w.get("xMin")), float(w.get("yMax")), w.text or ""))
    words.sort()
    lines = []
    for y, x, y2, t in words:
        if lines and abs(lines[-1]["y"] - y) < 2.0:
            lines[-1]["words"].append((x, t))
        else:
            lines.append({"y": y, "y2": y2, "words": [(x, t)]})
    for ln in lines:
        ln["words"].sort()
        ln["x"] = ln["words"][0][0]
        ln["text"] = " ".join(t for _, t in ln["words"])
    return lines


def near(v, target, tol=TOL):
    return abs(v - target) <= tol


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    pdf = sys.argv[1]
    xml = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True, check=True).stdout
    xml = re.sub(r"<!DOCTYPE[^>]*>", "", xml)
    root = ET.fromstring(xml)
    pages = list(root.iter("{http://www.w3.org/1999/xhtml}page"))
    fails, notes = [], []

    for pno, page in enumerate(pages, start=1):
        L = [ln for ln in lines_for_page(page) if not re.fullmatch(r"\d+", ln["text"].strip())]  # drop the page number
        if not L:
            continue
        # 1. every gap is a whole number of pitches
        for a, b in zip(L, L[1:]):
            gap = b["y"] - a["y"]
            k = round(gap / PITCH)
            if k == 0 or not near(gap, k * PITCH):
                fails.append(f"p{pno}: gap {gap:.1f} between {a['text'][:30]!r} and {b['text'][:30]!r} is not a whole number of 13.8 pt lines")
        if pno == 1:
            def find(prefix):
                return next((ln for ln in L if ln["text"].startswith(prefix)), None)
            named = {}
            for lab in ("From:", "To:", "Subj:", "Ref:", "Encl:"):
                named[lab] = find(lab)
            # date line: the line just above From:
            if named["From:"]:
                i = L.index(named["From:"])
                date_ln = L[i - 1] if i > 0 else None
                if date_ln:
                    g = named["From:"]["y"] - date_ln["y"]
                    (notes if near(g, 27.6) else fails).append(f"p1: date to From: {g:.1f} (target 27.6)")
                to_ln = named["To:"]
                if to_ln:
                    g = to_ln["y"] - named["From:"]["y"]
                    if not near(g, PITCH) and not near(g, 2 * PITCH):
                        fails.append(f"p1: From: to To: {g:.1f} (target 13.8, or 27.6 if From runs over)")
            # To (or last Via) to Subj: 27.6
            if named["Subj:"]:
                i = L.index(named["Subj:"])
                prev = L[i - 1]
                g = named["Subj:"]["y"] - prev["y"]
                (notes if near(g, 27.6) else fails).append(f"p1: heading to Subj: {g:.1f} (target 27.6)")
            if named["Ref:"] and named["Subj:"]:
                g = named["Ref:"]["y"] - named["Subj:"]["y"]
                if not (near(g, 27.6) or near(g, 3 * PITCH)):
                    fails.append(f"p1: Subj: to Ref: {g:.1f} (target 27.6, or 41.4 if Subj runs over)")
                else:
                    notes.append(f"p1: Subj: to Ref: {g:.1f}")
            if named["Encl:"]:
                i = L.index(named["Encl:"])
                prev = L[i - 1]
                g = named["Encl:"]["y"] - prev["y"]
                (notes if near(g, 27.6) else fails).append(f"p1: last Ref to Encl: {g:.1f} (target 27.6)")
            # first numbered paragraph
            p1 = next((ln for ln in L if re.match(r"1\.\s", ln["text"])), None)
            if p1:
                i = L.index(p1)
                prev = L[i - 1]
                g = p1["y"] - prev["y"]
                (notes if near(g, 27.6) else fails).append(f"p1: heading block to paragraph 1: {g:.1f} (target 27.6)")
        else:
            # continuation page: Subj on the sixth line
            first = L[0]
            if first["text"].startswith("Subj:"):
                off = first["y"]
                (notes if near(off, 6 * PITCH, 2.0) else fails).append(f"p{pno}: Subj line {off:.1f} from the top of the page (target 82.8, the sixth line)")
                subj_lines = 1 + sum(1 for ln in L[1:3] if not re.match(r"(\d+\.|[a-z]\.|\(\d+\)|\([a-z]\))\s", ln["text"]) and ln["y"] - first["y"] < 2 * PITCH)
                body_first = next((ln for ln in L[1:] if re.match(r"(\d+\.|[a-z]\.|\(\d+\)|\([a-z]\))\s", ln["text"]) or ln["y"] - first["y"] >= 2 * PITCH), None)
                if body_first:
                    g = body_first["y"] - first["y"]
                    if not any(near(g, (subj_lines + 1) * PITCH) for _ in [0]):
                        fails.append(f"p{pno}: body resumes {g:.1f} below the Subj line (target {(subj_lines + 1) * PITCH:.1f}, the second line below)")
                    else:
                        notes.append(f"p{pno}: body resumes {g:.1f} below the Subj line")
            else:
                fails.append(f"p{pno}: continuation page does not begin with the Subj line")

    # signature: last page, all caps with initials, at page centre, 55.2 below the last text line
    body = [ln for ln in lines_for_page(pages[-1]) if not re.fullmatch(r"\d+", ln["text"].strip())]
    sig = next((ln for ln in reversed(body) if re.fullmatch(r"[A-Z][A-Z.\s]{3,}", ln["text"].strip()) and "." in ln["text"]), None)
    if sig is None:
        fails.append("no signature line found on the last page")
    else:
        i = body.index(sig)
        prev = body[i - 1]
        g = sig["y"] - prev["y"]
        (notes if near(g, 4 * PITCH) else fails).append(f"signature {g:.1f} below the last text line (target 55.2)")
        (notes if near(sig["x"], PAGE_CENTRE, 4.0) else fails).append(f"signature starts at x={sig['x']:.1f} (target {PAGE_CENTRE:.0f}, page centre)")

    print(f"MEASURE: {pdf}  pages: {len(pages)}")
    for n in notes:
        print(f"  ok    {n}")
    for f in fails:
        print(f"  FAIL  {f}")
    print(f"  -> {len(fails)} failures")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
