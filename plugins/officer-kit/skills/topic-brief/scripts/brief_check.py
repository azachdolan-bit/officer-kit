#!/usr/bin/env python3
"""Check a topic brief or a timed talk script against references/brief-shape.md and script-and-card.md.

Usage:
  python3 brief_check.py <brief.md> --kind brief [--sources <file> ...] [--numbers]
  python3 brief_check.py <script.md> --kind script [--sources <file> ...] [--doctrine "MCDP 1"] [--format 1,3,1] [--numbers]

Both kinds: a Topic line, every number traced to a row of the sources table, a lines not to say list
(a bullet that opens with a quoted line is a line that must never appear in the text),
and no em or en dashes.
Brief: the opening paragraph names the topic; one Context section, one paragraph, 120 words or fewer.
With --sources, every quote of four words or more is verbatim in a source (brief and script).
--numbers lists every number with its sentence and its table rows, for the scope read the checker cannot do.
Script: run time at the stated pace inside the Limit (reported at 130 and 150 too; a number of three
digits or more is counted as the words it takes to say it); every time mark
within 20 seconds of where the words put it; the format split when --format is given; every quote of
four words or more verbatim in a source; no line from lines not to say spoken; with --doctrine, the
publication named in the sources table and quoted in the script.
Exit 0 when everything passes, 1 otherwise. Sources may be .md, .txt, .html, .pdf (pdftotext), .docx."""
import argparse, os, re, subprocess, sys, zipfile

STOP = set("""the and for with from that this into over under about their there then than when what which while
were been being have has had does done will would could should defense against during after before where
more most less least very just only also each every other some such""".split())
FACT_HEAD = re.compile(r"where every fact|sources? table|^sources?$", re.I)
NOT_SAY_HEAD = re.compile(r"lines? (?:not to|to not) say|do not say", re.I)
AFTER_HEADS = re.compile(r"where every fact|^sources?$|lines? (?:not to|to not) say|do not say|^gaps?$|^maps?", re.I)

def read(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
        return r.stdout
    if ext == ".docx":
        x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8", "ignore")
        return re.sub(r"<[^>]+>", " ", x.replace("</w:p>", "\n"))
    return open(path, encoding="utf-8", errors="ignore").read()

def sections(text):
    out, head, buf = [], None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*)", line)
        if m:
            out.append((head, "\n".join(buf)))
            head, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    out.append((head, "\n".join(buf)))
    return out

def spoken(body):
    body = re.sub(r"\*\([^)]*\)\*", " ", body)
    body = re.sub(r"\[[^\]]*\]", " ", body)
    return re.sub(r"[*_`>#]", " ", body)

def words(t):
    return re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?", t)

def spoken_count(t):
    """Words as spoken: a number of three digits takes two words aloud, four or more three."""
    n = 0
    for w in words(t):
        n += 1
        if w.isdigit() and len(w) >= 3:
            n += 1 if len(w) == 3 else 2
    return n

def norm(t):
    t = t.replace("’", "'").replace("“", '"').replace("”", '"')
    return " ".join(re.sub(r"[^a-z0-9' ]+", " ", t.lower()).split())

NUMRX = re.compile(r"(?<![A-Za-z0-9.,])(\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:st|nd|rd|th|d)?(?![A-Za-z0-9])")

def numbers(t):
    return [m.group(1).replace(",", "") for m in NUMRX.finditer(t)]

def traced(n, table):
    return re.search(r"(?<!\d)" + re.escape(n) + r"(?!\d)", table.replace(",", "")) is not None

def mmss(s):
    m, sec = s.split(":")
    return int(m) * 60 + int(sec)

def fmt(sec):
    return "%d:%02d" % (sec // 60, round(sec % 60))

def quotes(t):
    t = t.replace("“", '"').replace("”", '"')
    return [q.strip() for q in re.findall(r'"([^"]+)"', t)]

def check(text, kind, sources=(), doctrine=None, fmt_split=None):
    res = []
    def ok(c, m):
        res.append((bool(c), m))
    tm = re.search(r"^Topic:\s*(.+)$", text, re.M)
    ok(tm, "has a Topic line with the topic as assigned")
    topic = tm.group(1) if tm else ""
    secs = sections(text)
    table = "\n".join(b for h, b in secs if h and FACT_HEAD.search(h))
    ok(table.strip(), "has a 'Where every fact comes from' sources table")
    notsay = "\n".join(b for h, b in secs if h and NOT_SAY_HEAD.search(h))
    bullets = [l for l in notsay.splitlines() if l.strip().startswith(("-", "*"))]
    ok(bullets, "has a lines not to say list with at least one line")
    content = [(h, b) for h, b in secs if not (h and AFTER_HEADS.search(h))]
    body_text = "\n".join(b for h, b in content)
    body_text = re.sub(r"^(Topic|Limit|Pace|Run time|Built|Braids|Cue card).*$", "", body_text, flags=re.M | re.I)
    if kind == "script":
        body_text = "\n".join(spoken(b) for h, b in content if h and re.search(r"\d{1,2}:\d{2}\s*$", h))
    untraced = sorted(set(n for n in numbers(body_text) if not traced(n, table)), key=lambda x: int(x))
    ok(not untraced, "every number is traced to a row of the sources table" + ("; untraced: " + ", ".join(untraced) if untraced else ""))
    said = norm(body_text)
    spoken_bad = []
    for b in bullets:
        m = re.match(r'^\s*[-*]\s*["\u201c]([^"\u201d]+)["\u201d]', b)
        if m and norm(m.group(1)) and norm(m.group(1)) in said:
            spoken_bad.append(m.group(1))
    ok(not spoken_bad, "no line from lines not to say appears in the text" + ("; found: " + "; ".join(spoken_bad) if spoken_bad else ""))
    ok(not re.search("[–—]", text), "no em or en dashes")
    if kind == "brief" and sources:
        src_all = [norm(read(x)) for x in sources]
        bq = [q for q in quotes(body_text) if len(words(q)) >= 4]
        miss = [q for q in bq if not any(norm(q) in t for t in src_all)]
        ok(not miss, "every quote of four words or more is verbatim in a source" + ("; not found: " + " | ".join(miss) if miss else ""))
    if kind == "brief":
        topic_words = [w.lower() for w in words(topic) if len(w) >= 4 and w.lower() not in STOP]
        first = ""
        for h, b in secs[:1]:
            paras = [p.strip() for p in re.split(r"\n\s*\n", b) if p.strip() and not p.strip().startswith(("#", "Topic:"))]
            first = paras[0] if paras else ""
        hit = [w for w in topic_words if w in first.lower()]
        ok(topic_words and len(hit) * 2 >= len(topic_words), "the opening paragraph names the topic (%d of %d topic words)" % (len(hit), len(topic_words)))
        ctx = [(h, b) for h, b in secs if h and re.search(r"context|background", h, re.I)]
        ok(len(ctx) == 1, "exactly one Context section (found %d)" % len(ctx))
        if ctx:
            paras = [p for p in re.split(r"\n\s*\n", ctx[0][1]) if p.strip()]
            n = len(words(ctx[0][1]))
            ok(len(paras) == 1 and n <= 120, "context is one paragraph of 120 words or fewer (%d paragraphs, %d words)" % (len(paras), n))
        return res
    lm = re.search(r"^Limit:\s*(\d{1,2}:\d{2})", text, re.M)
    pm = re.search(r"Pace:\s*(\d+)", text)
    ok(lm, "has a Limit line")
    limit = mmss(lm.group(1)) if lm else 0
    pace = int(pm.group(1)) if pm else 140
    timed = [(h, spoken(b)) for h, b in content if h and re.search(r"\d{1,2}:\d{2}\s*$", h)]
    ok(timed, "sections carry time marks")
    counts = [spoken_count(b) for h, b in timed]
    total = sum(counts)
    run = total * 60.0 / pace
    ok(limit and run <= limit, "run time %s at %d wpm is inside the %s limit (%d words as spoken; %s at 130, %s at 150)" % (fmt(run), pace, fmt(limit), total, fmt(total * 60 / 130), fmt(total * 60 / 150)))
    marks = [mmss(re.search(r"(\d{1,2}:\d{2})\s*$", h).group(1)) for h, b in timed]
    ok(marks and marks[0] == 0 and marks == sorted(marks), "time marks start at 0:00 and run in order")
    off, cum = [], 0
    for (h, b), c, mk in zip(timed, counts, marks):
        at = cum * 60.0 / pace
        if abs(at - mk) > 20:
            off.append("%s marked %s, words put it at %s" % (re.sub(r"\s*\d{1,2}:\d{2}\s*$", "", h), fmt(mk), fmt(at)))
        cum += c
    ok(not off, "every time mark is within 20 seconds of where the words put it" + ("; " + "; ".join(off) if off else ""))
    if fmt_split:
        a, b_, c = fmt_split
        ok(len(marks) > 1 and marks[1] <= a * 60 + 30, "the body starts by %s (format %s)" % (fmt(a * 60 + 30), ",".join("%g" % x for x in fmt_split)))
        ok(marks and marks[-1] >= (a + b_) * 60 - 30, "the close starts no earlier than %s (format %s)" % (fmt((a + b_) * 60 - 30), ",".join("%g" % x for x in fmt_split)))
    src_text = {s: norm(read(s)) for s in sources}
    long_q = [q for q in quotes(body_text) if len(words(q)) >= 4]
    if sources:
        missing = [q for q in long_q if not any(norm(q) in t for t in src_text.values())]
        ok(not missing, "every quote of four words or more is verbatim in a source" + ("; not found: " + " | ".join(missing) if missing else ""))
    if doctrine:
        ok(doctrine.lower() in table.lower(), "the sources table names %s" % doctrine)
        key = re.sub(r"[^a-z0-9]", "", doctrine.lower())
        dsrc = [t for s, t in src_text.items() if key in re.sub(r"[^a-z0-9]", "", (os.path.basename(s) + t[:3000]).lower())]
        if dsrc:
            ok(any(norm(q) in t for q in long_q for t in dsrc), "the script quotes %s, not just names it" % doctrine)
        else:
            ok(long_q, "the script quotes %s (pass its library copy with --sources to verify the words)" % doctrine)
    return res

def numbers_report(text, kind):
    """Every number, the sentence it is said in, and the table rows that carry it: the checker proves a
    number is sourced, not that it is said at the right scope, so this list is for that read."""
    secs = sections(text)
    rows = [l for h, b in secs if h and FACT_HEAD.search(h) for l in b.splitlines() if l.startswith("|")]
    body = [b for h, b in secs if not (h and AFTER_HEADS.search(h))]
    if kind == "script":
        body = [spoken(b) for h, b in secs if h and re.search(r"\d{1,2}:\d{2}\s*$", h)]
    out = ["Numbers to read for scope (number | sentence | rows):"]
    for sent in re.split(r"(?<=[.!?])\s+", " ".join(" ".join(body).split())):
        for n in dict.fromkeys(numbers(sent)):
            hits = [r.strip() for r in rows if traced(n, r)]
            out.append("- %s | %s | %s" % (n, sent[:140], " || ".join(hits) or "NO ROW"))
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--kind", choices=["brief", "script"], required=True)
    ap.add_argument("--sources", nargs="*", default=[])
    ap.add_argument("--doctrine")
    ap.add_argument("--format")
    ap.add_argument("--numbers", action="store_true", help="also list every number with its sentence and its table rows, for the scope read")
    a = ap.parse_args()
    split = [float(x) for x in a.format.split(",")] if a.format else None
    text = open(a.file, encoding="utf-8").read()
    res = check(text, a.kind, a.sources, a.doctrine, split)
    if a.numbers:
        print(numbers_report(text, a.kind))
    for i, (c, m) in enumerate(res, 1):
        print("%2d. %s  %s" % (i, "PASS" if c else "FAIL", m))
    bad = sum(1 for c, _ in res if not c)
    print("-> %d of %d pass" % (len(res) - bad, len(res)))
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
