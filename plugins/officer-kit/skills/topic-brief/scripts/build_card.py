#!/usr/bin/env python3
"""Build a keyword cue card from a small JSON file and check it.

Usage: python3 build_card.py <card.json> <out.html> [--script <script.md>] [--pdf <out.pdf>]

card.json: {"title": "...", "size": "5x3", "faces": [{"lines": [{"t": "0:00", "text": "keywords"},
            {"quote": "exact words", "cite": "source"}]}]}
Checks (after speaker notes guidance: key words and phrases, not sentences; large print; one side;
numbered; only an exact quotation written in full, with its citation):
  1. no keyword line over eight words      2. no face over nine printed lines (a quote counts its wrap and citation)
  3. time marks in order across faces     4. every quote carries a citation
  5. with --script: every quote is word for word in the script, and every card time mark is one of the script's marks
  6. no em or en dashes   7. no clock time in m:ss form in a keyword line   8. a time mark on every face
Writes the HTML (one face per page at the card size) whatever the checks say; writes the PDF with
Playwright's Chromium when it is installed. Exit 0 when every check passes, 1 otherwise."""
import argparse, html, json, re, sys

def norm(t):
    t = t.replace("’", "'").replace("“", '"').replace("”", '"')
    return " ".join(re.sub(r"[^a-z0-9' ]+", " ", t.lower()).split())

def mmss(s):
    m, sec = s.split(":")
    return int(m) * 60 + int(sec)

def check(card, script=None):
    res = []
    def ok(c, m):
        res.append((bool(c), m))
    faces = card.get("faces", [])
    ok(faces, "the card has at least one face")
    long_lines, marks, uncited, all_text = [], [], [], json.dumps(card, ensure_ascii=False)
    for fi, f in enumerate(faces, 1):
        lines = f.get("lines", [])
        units = sum((2 + len(ln["quote"]) // 46) if "quote" in ln else 1 for ln in lines)
        ok(units <= 9, "face %d fits: nine printed lines or fewer, a quote counting its wrapped lines and citation (%d)" % (fi, units))
        for ln in lines:
            if "quote" in ln:
                if not ln.get("cite"):
                    uncited.append(ln["quote"][:40])
                continue
            n = len(ln.get("text", "").split())
            if n > 8:
                long_lines.append("face %d: %s (%d words)" % (fi, ln.get("text", "")[:40], n))
            if ln.get("t"):
                marks.append(mmss(ln["t"]))
    clock = [ln.get("text", "") for f in faces for ln in f.get("lines", []) if "quote" not in ln and re.search(r"(?<![\d:])\d{1,2}:\d{2}(?![\d:])", ln.get("text", ""))]
    ok(not clock, "no clock time written as m:ss in a keyword line, where it reads as a pacing mark (write 0230)" + ("; " + "; ".join(clock) if clock else ""))
    unmarked = [str(i) for i, f in enumerate(faces, 1) if not any(ln.get("t") for ln in f.get("lines", []))]
    ok(not unmarked, "every face carries at least one time mark" + ("; face " + ", ".join(unmarked) if unmarked else ""))
    ok(not long_lines, "every keyword line is eight words or fewer" + ("; " + "; ".join(long_lines) if long_lines else ""))
    ok(marks == sorted(marks), "time marks run in order across the faces")
    ok(not uncited, "every quote carries its citation" + ("; " + "; ".join(uncited) if uncited else ""))
    if script:
        s = norm(script)
        bad = [ln["quote"] for f in faces for ln in f.get("lines", []) if "quote" in ln and norm(ln["quote"]) not in s]
        ok(not bad, "every quote on the card is word for word in the script" + ("; not found: " + " | ".join(bad) if bad else ""))
        smarks = set(mmss(m) for m in re.findall(r"^##.*?(\d{1,2}:\d{2})\s*$", script, re.M))
        stray = [m for m in marks if m not in smarks]
        ok(not stray, "every time mark on the card is one of the script's section marks" + ("; stray: " + ", ".join("%d:%02d" % (m // 60, m % 60) for m in stray) if stray else ""))
    ok(not re.search("[–—]", all_text), "no em or en dashes")
    return res

def render(card):
    w, h = (card.get("size") or "5x3").lower().split("x")
    pages = []
    n = len(card["faces"])
    for i, f in enumerate(card["faces"], 1):
        rows = []
        for ln in f.get("lines", []):
            if "quote" in ln:
                rows.append('<div class="q">&ldquo;%s&rdquo;<span class="c">%s</span></div>' % (html.escape(ln["quote"]), html.escape(ln.get("cite", ""))))
            else:
                rows.append('<div class="l"><span class="t">%s</span>%s</div>' % (html.escape(ln.get("t", "")), html.escape(ln.get("text", ""))))
        pages.append('<section><header>%s<span>%d of %d</span></header>%s</section>' % (html.escape(card.get("title", "")), i, n, "".join(rows)))
    css = """@page{size:%sin %sin;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif}
section{width:%sin;height:%sin;padding:.18in .22in;page-break-after:always;overflow:visible}
header{display:flex;justify-content:space-between;font-size:9pt;font-weight:bold;border-bottom:1.5pt solid #000;margin-bottom:.06in}
.l{font-size:13pt;line-height:1.25;margin:.02in 0}.t{display:inline-block;width:.55in;font-weight:bold}
.q{font-size:11pt;font-style:italic;margin:.05in 0 .05in .55in}.c{display:block;font-size:9pt;font-style:normal}""" % (w, h, w, h)
    return "<!doctype html><html><head><meta charset='utf-8'><style>%s</style></head><body>%s</body></html>" % (css, "".join(pages))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("card")
    ap.add_argument("out")
    ap.add_argument("--script")
    ap.add_argument("--pdf")
    a = ap.parse_args()
    card = json.load(open(a.card, encoding="utf-8"))
    script = open(a.script, encoding="utf-8").read() if a.script else None
    res = check(card, script)
    doc = render(card)
    open(a.out, "w", encoding="utf-8").write(doc)
    if a.pdf:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b = p.chromium.launch()
                pg = b.new_page()
                pg.set_content(doc)
                pg.pdf(path=a.pdf, prefer_css_page_size=True, print_background=True)
                b.close()
            print("wrote", a.pdf)
        except Exception as e:
            print("PDF not written (%s): open %s in a browser and print it at actual size" % (type(e).__name__, a.out))
    for i, (c, m) in enumerate(res, 1):
        print("%2d. %s  %s" % (i, "PASS" if c else "FAIL", m))
    bad = sum(1 for c, _ in res if not c)
    print("-> %d of %d pass" % (len(res) - bad, len(res)))
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
