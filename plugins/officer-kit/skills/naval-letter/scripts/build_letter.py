#!/usr/bin/env python3
"""Render a naval letter (.docx) from a JSON spec, to the student handout standard
(B020069XQ Military Correspondence over SECNAV M-5216.5).

Usage:  python3 build_letter.py spec.json out.docx

Spec (all identity fields optional; a missing one renders as a [PLACEHOLDER] that
qc_letter.py will refuse to pass, so nothing ships half filled):

{
  "ssic": "1500",
  "originator_code": "BOC 4-26",
  "date": "2026-09-04",                      ISO date; rendered as "4 Sep 26"
  "from": "Second Lieutenant ... , Billet, Unit",
  "to": "Company Academics Officer, Delta Company",
  "via": ["Commanding Officer, ..."],        optional; omit entirely when no routing
  "subj": "REQUEST FOR ...",                 rendered in all caps
  "refs": ["Title of document one", "..."],  one document per entry
  "encls": ["Exact title of enclosure"],
  "paragraphs": [
    {"text": "Purpose.  ..."},
    {"text": "...", "subs": [
        {"text": "...", "subs": [ {"text": "..."} ]}
    ]}
  ],
  "poc": "My point of contact information is ...",   optional; becomes the last numbered paragraph
  "signature": "A. Z. DOLAN",
  "author": "Name for the file properties",         optional
  "kind": "mfr",                                    optional; memorandum for the record (no From/To, centered caption)
  "letterhead": ["UNITED STATES MARINE CORPS", "..."],   optional; centered lines above the heading block
  "signature_lines": ["Billet", "Grade USMC"],      optional; lines under the signature name (MFR)
  "endorsement": {"ordinal": "FIRST", "on": "CO ltr 1500 BOC 4-26 of 4 Sep 26"}   optional; identification line
}

Layout rules encoded here (see references/standard.md):
- Times New Roman 12, 1 inch margins, no letterhead.
- Line pitch pinned at 13.8 pt; every blank line is a real empty paragraph, so the
  "second line below" and "fourth line below" measurements are exact.
- SSIC block left aligned on a common tab 2 inches from the right edge of the paper.
- From/To/Via/Subj/Ref/Encl labels at the margin, text at a 0.5 inch tab.
- Paragraphs 1. / a. / (1) / (a), first line indented by level, runover to the margin.
- Signature on the fourth line below the last line of text, starting at page centre.
- Continuation pages repeat the Subj line on the sixth line; page number centred in the foot.
"""
import json, re, sys
from datetime import datetime

try:
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    sys.exit("python-docx is required: pip install python-docx")

LINE = Pt(13.8)
TAB = 0.5
SSIC_INDENT = 5.5          # 6.5 inches from the left edge of the paper inside a 1 inch margin
LEVELS = ["{n}.", "{a}.", "({n})", "({a})"]
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def placeholder(name):
    return f"[{name.upper()}]"


def fmt_date(s):
    if not s:
        return placeholder("date")
    try:
        d = datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        return s  # already in letter form, e.g. "4 Sep 26"
    return f"{d.day} {d.strftime('%b %y')}"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]

    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    st.paragraph_format.space_after = Pt(0)
    st.paragraph_format.space_before = Pt(0)
    st.paragraph_format.line_spacing = LINE
    sec = d.sections[0]
    sec.top_margin = sec.bottom_margin = sec.left_margin = sec.right_margin = Inches(1.0)
    sec.footer_distance = Inches(0.5)
    sec.header_distance = Inches(0.5)
    sec.different_first_page_header_footer = True

    def para(text="", left=0.0, hang=0.0, first=0.0, align=None, tabs=None):
        p = d.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Inches(left)
        if hang:
            pf.first_line_indent = Inches(-hang)
        elif first:
            pf.first_line_indent = Inches(first)
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        if align is not None:
            p.alignment = align
        if tabs:
            for pos in tabs:
                pf.tab_stops.add_tab_stop(Inches(pos), WD_TAB_ALIGNMENT.LEFT)
        if text:
            p.add_run(text)
        return p

    def blank(n=1):
        for _ in range(n):
            para()

    def labelled(label, text):
        p = para(left=TAB, hang=TAB, tabs=[TAB])
        p.add_run(f"{label}\t{text}")
        return p

    def listed(label, marker, text):
        p = para(left=TAB + 0.4, hang=TAB + 0.4, tabs=[TAB, TAB + 0.4])
        p.add_run(f"{label}\t{marker}\t{text}")
        return p

    # ---- heading block ----------------------------------------------------
    kind = (spec.get("kind") or "letter").lower()      # letter | mfr
    for line in spec.get("letterhead") or []:          # optional; a student letter carries none
        para(line, align=WD_ALIGN_PARAGRAPH.CENTER)
    if spec.get("letterhead"):
        blank()
    if kind == "mfr":
        # Memorandum for the record, to the MCTP 3-30A Appendix D shape: code and date at the right,
        # the caption centered on the second line below, Subj on the second line below that, no From or To.
        for t in (spec.get("originator_code") or placeholder("originator code"), fmt_date(spec.get("date"))):
            para(t, left=SSIC_INDENT)
        blank()
        para("MEMORANDUM FOR THE RECORD", align=WD_ALIGN_PARAGRAPH.CENTER)
    else:
        for t in (spec.get("ssic") or placeholder("ssic"),
                  spec.get("originator_code") or placeholder("originator code"),
                  fmt_date(spec.get("date"))):
            para(t, left=SSIC_INDENT)
        if spec.get("endorsement"):
            # Endorsement identification line on the second line below the date, From on the second line
            # below it, as the endorsements reproduced in MCO 1900.16 Figures 6-5 and L-10 and NAVMC 4000.5D
            # enclosure (12) lay it out: "FIRST ENDORSEMENT on <originator> ltr <SSIC> <code> of <date>".
            e = spec["endorsement"]
            blank()
            para(f"{(e.get('ordinal') or placeholder('ordinal')).upper()} ENDORSEMENT on {e.get('on') or placeholder('basic letter')}")
        blank()                                        # From: on the second line below
        labelled("From:", spec.get("from") or placeholder("from line"))
        labelled("To:", spec.get("to") or placeholder("to line"))
        for v in spec.get("via") or []:
            labelled("Via:", v)
    blank()                                            # Subj on the second line below
    subj = (spec.get("subj") or placeholder("subject")).upper()
    labelled("Subj:", subj)
    refs = spec.get("refs") or []
    encls = spec.get("encls") or []
    if refs:
        blank()
        for i, r in enumerate(refs):
            listed("Ref:" if i == 0 else "", f"({LETTERS[i]})", r)
    if encls:
        blank()
        for i, e in enumerate(encls):
            listed("Encl:" if i == 0 else "", f"({i + 1})", e)
    blank()                                            # paragraph 1 on the second line below

    # ---- body -------------------------------------------------------------
    def emit(items, level, counters):
        for idx, it in enumerate(items):
            if isinstance(it, str):
                it = {"text": it}
            n = idx + 1
            marker = LEVELS[level].format(n=n, a=LETTERS[idx])
            p = para(first=0.25 * level)
            p.add_run(f"{marker}  {it['text']}")
            blank()
            if it.get("subs"):
                emit(it["subs"], level + 1, counters)

    paragraphs = list(spec.get("paragraphs") or [])
    if spec.get("poc"):
        paragraphs.append({"text": spec["poc"]})
    if not paragraphs:
        paragraphs = [{"text": placeholder("body")}]
    emit(paragraphs, 0, {})

    # ---- signature: fourth line below the text ----------------------------
    # emit() already left one blank line after the last paragraph; two more make three.
    blank(2)
    para(spec.get("signature") or placeholder("signature"), left=3.25)
    for line in spec.get("signature_lines") or []:     # MFR: billet and grade under the name (MCTP 3-30A App D)
        para(line, left=3.25)

    # ---- continuation page furniture --------------------------------------
    h = sec.header.paragraphs[0]
    h.paragraph_format.tab_stops.add_tab_stop(Inches(TAB), WD_TAB_ALIGNMENT.LEFT)
    h.paragraph_format.space_before = Pt(46.2)         # Subj on the sixth line: 6 x 13.8 from the top
    h.paragraph_format.space_after = Pt(13.8)          # text resumes on the second line below
    r = h.add_run("Subj:\t" + subj)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    f = sec.footer.paragraphs[0]
    f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = f.add_run()
    for tag in ("begin",):
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tag); run._r.append(e)
    e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = "PAGE"; run._r.append(e)
    e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end"); run._r.append(e)
    for rr in f.runs:
        rr.font.name = "Times New Roman"
        rr.font.size = Pt(12)

    if spec.get("author"):
        d.core_properties.author = spec["author"]
        d.core_properties.last_modified_by = spec["author"]
    d.core_properties.title = subj.title()
    d.core_properties.comments = "Drafted with AI assistance (Officer Kit). The signer owns the words."
    d.save(out)

    missing = re.findall(r"\[[A-Z ]+\]", "\n".join(p.text for p in d.paragraphs))
    print(f"wrote {out}")
    if missing:
        print("placeholders left (fill the identity fields in the spec or the rules file): "
              + ", ".join(sorted(set(missing))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
