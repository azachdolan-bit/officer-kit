#!/usr/bin/env python3
"""Build the study guide document (.docx) from a spec.
Usage: python3 build_guide.py <spec.json> <out.docx>
Builds the guide, and also the handout and whiteboard formats (mode in the spec): those carry the
title, skeleton if given, objectives, and the sections; a whiteboard adds a coverage index.
Order: title, how to use, skeleton, objectives, knowledge sections, practice scenarios with the
answer key on its own page, practice quiz with the answer key on its own page, flashcards if given.
Needs python-docx (pip install python-docx)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import study_lib as L
from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Pt, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def runs(par, text):
    for part in re.split(r"(\*\*.+?\*\*|`.+?`)", text):
        if not part: continue
        if part.startswith("**"): par.add_run(part[2:-2]).bold = True
        elif part.startswith("`"): r = par.add_run(part[1:-1]); r.font.name = "Consolas"
        else: par.add_run(part.replace("*", ""))

def render(doc, md):
    for kind, p in L.md_blocks(md):
        if kind == "h2": doc.add_heading(p, level=2)
        elif kind == "h3": doc.add_heading(p, level=3)
        elif kind == "p":
            if p.startswith("Table: "):
                para = doc.add_paragraph(); r = para.add_run(p[7:]); r.bold = True; r.italic = True
                para.paragraph_format.keep_with_next = True
            else:
                runs(doc.add_paragraph(), p)
        elif kind == "ul":
            for x in p: runs(doc.add_paragraph(style="List Bullet"), x)
        elif kind == "ol":
            for k, x in enumerate(p, 1):
                para = doc.add_paragraph(); para.paragraph_format.left_indent = Inches(0.3)
                para.paragraph_format.first_line_indent = Inches(-0.25); runs(para, "%d. %s" % (k, x))
        elif kind == "callout":
            t, body = p
            para = doc.add_paragraph(); r = para.add_run(t + ": "); r.bold = True
            runs(para, " ".join(x for x in body if x))
        elif kind == "table":
            t = doc.add_table(rows=len(p), cols=max(len(r) for r in p)); t.style = "Table Grid"
            for i, row in enumerate(p):
                for j, c in enumerate(row):
                    cell = t.cell(i, j); cell.text = ""
                    runs(cell.paragraphs[0], c)
                    if i == 0:
                        for r in cell.paragraphs[0].runs: r.bold = True
            for i, row in enumerate(t.rows):
                trPr = row._tr.get_or_add_trPr()
                trPr.append(OxmlElement("w:cantSplit"))
                if i == 0:
                    trPr.append(OxmlElement("w:tblHeader"))
                if i < len(t.rows) - 1 and len(t.rows) <= 12:
                    for cell in row.cells:
                        for para in cell.paragraphs: para.paragraph_format.keep_with_next = True
            doc.add_paragraph()

def lines(doc, n):
    for k in range(n):
        para = doc.add_paragraph("_" * 78)
        if k < n - 1: para.paragraph_format.keep_with_next = True

def keep(par):
    par.paragraph_format.keep_with_next = True
    return par

def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def main(spec_path, out):
    spec = L.balance(L.load(spec_path))
    fails, _ = L.quiz_fails(spec)
    if fails:
        print("NOT BUILT: quiz rules fail"); [print("  ", f) for f in fails]; return 1
    doc = Document()
    doc.styles["Normal"].font.size = Pt(11)
    for name, size in (("Heading 1", 18), ("Heading 2", 13), ("Heading 3", 11.5)):
        doc.styles[name].font.size = Pt(size)
    doc.add_heading(spec["title"], level=0)
    if spec.get("subtitle"): doc.add_paragraph(spec["subtitle"])
    mode = spec.get("mode", "guide")
    if mode == "guide":
      doc.add_heading("How to use this guide", level=1)
      doc.add_paragraph("Learn the skeleton first, then read each section in full. Work the scenarios and the quiz "
                      "without looking, then check the answer keys, which sit on their own pages. Retake the quiz "
                      "in a few days; spacing the practice is what makes it stick.")
    if spec.get("assumptions"):
        doc.add_heading("What this guide assumed", level=1); render(doc, spec["assumptions"])
    if spec.get("skeleton"):
        doc.add_heading("Skeleton", level=1); render(doc, spec["skeleton"])
    if spec.get("objectives"):
        doc.add_heading("Learning objectives", level=1)
        render(doc, "| Code | Objective |\n|---|---|\n" + "\n".join("| %s | %s |" % (o.get("code", ""), o["text"]) for o in spec["objectives"]))
    for s in spec["sections"]:
        doc.add_heading(s["title"], level=1)
        render(doc, s.get("body", ""))
    if mode == "whiteboard" and spec.get("objectives"):
        page_break(doc); doc.add_heading("Coverage index", level=1)
        render(doc, "| Code | Section |\n|---|---|\n" + "\n".join("| %s | %s |" % (o.get("code", ""), o.get("section", "")) for o in spec["objectives"]))
    if mode != "guide":
        doc.save(out); print("written", out, "mode", mode, "sections", len(spec["sections"])); return 0
    sc = spec.get("scenarios", [])
    if sc:
        page_break(doc); doc.add_heading("Practice scenarios", level=1)
        for i, x in enumerate(sc, 1):
            start = len(doc.paragraphs)
            doc.add_heading("Scenario %d. %s" % (i, x["title"]), level=2); render(doc, x["situation"])
            lines(doc, 4)
            for para in doc.paragraphs[start:-1]:
                para.paragraph_format.keep_with_next = True  # the whole scenario stays on one page
        page_break(doc); doc.add_heading("Scenario answer key", level=1)
        for i, x in enumerate(sc, 1):
            doc.add_heading("Scenario %d" % i, level=2); render(doc, x["key"])
    qs = spec.get("quiz", [])
    if qs:
        page_break(doc); doc.add_heading("Practice quiz", level=1)
        for i, q in enumerate(qs, 1):
            keep(doc.add_paragraph("%d. %s" % (i, q["q"])))
            if L.is_recall(q):
                lines(doc, 3)
                continue
            for j, o in enumerate(q["o"]):
                para = doc.add_paragraph("%s. %s" % ("ABCD"[j], o)); para.paragraph_format.left_indent = Inches(0.3)
                if j < 3: keep(para)
        page_break(doc); doc.add_heading("Quiz answer key", level=1)
        for i, q in enumerate(qs, 1):
            p = keep(doc.add_paragraph())
            p.add_run("%d. %s" % (i, q["answer"] if L.is_recall(q) else "%s. %s" % ("ABCD"[q["a"]], q["o"][q["a"]]))).bold = True
            where = L.locate(spec, q)
            doc.add_paragraph(q["e"] + ("  Where it is: %s." % where if where else ""))
    fc = spec.get("flashcards", [])
    if fc:
        page_break(doc); doc.add_heading("Flashcards", level=1)
        render(doc, "| Front | Back |\n|---|---|\n" + "\n".join("| %s | %s |" % (c["front"], c["back"]) for c in fc))
    doc.save(out)
    print("written", out, "sections", len(spec["sections"]), "quiz", len(qs), "scenarios", len(sc))
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 3: sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
