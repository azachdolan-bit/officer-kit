# -*- coding: utf-8 -*-
"""Shared code for the study-guide builders and gates. Content free: every word of a product comes
from the spec the session writes from the user's own source.

The spec (JSON) is described in ../references/spec.md. Section bodies are a small Markdown subset:
## and ### headings, paragraphs, - and 1. lists, | tables |, **bold**, *italic*, `code`, and
> callouts (first line "> TITLE: text"). Walkthrough sections may also carry raw HTML in "html"."""
import html, json, random, re
from collections import Counter

# ---------------------------------------------------------------- markdown subset -> html
def _inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", t)
    t = re.sub(r"`(.+?)`", r'<span class="k">\1</span>', t)
    return t

def md_blocks(md):
    """Parse the Markdown subset into blocks: (kind, payload). Shared by the HTML and docx renderers."""
    lines = (md or "").replace("\r", "").split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith("### "):
            out.append(("h3", ln[4:].strip())); i += 1; continue
        if ln.startswith("## "):
            out.append(("h2", ln[3:].strip())); i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            out.append(("table", rows)); continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip()); i += 1
            m = re.match(r"([A-Z][A-Z0-9 ]{1,30}):\s*(.*)", buf[0])
            title, first = (m.group(1), m.group(2)) if m else ("NOTE", buf[0])
            out.append(("callout", (title, [first] + buf[1:]))); continue
        for kind, pat in (("ul", r"^\s*- "), ("ol", r"^\s*\d+\. ")):
            if re.match(pat, ln):
                items = []
                while i < len(lines):
                    if re.match(pat, lines[i]):
                        items.append(re.sub(pat, "", lines[i])); i += 1
                    elif not lines[i].strip() and i + 1 < len(lines) and re.match(pat, lines[i + 1]):
                        i += 1  # a blank line between items does not end the list
                    else:
                        break
                out.append((kind, items)); break
        else:
            kind = None
        if kind:
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{2,3} |\||>|\s*- |\s*\d+\. )", lines[i]):
            buf.append(lines[i].strip()); i += 1
        out.append(("p", " ".join(buf)))
    return out

def md_html(md):
    h = []
    for kind, p in md_blocks(md):
        if kind == "h2": h.append("<h2>%s</h2>" % _inline(p))
        elif kind == "h3": h.append("<h3>%s</h3>" % _inline(p))
        elif kind == "p": h.append("<p>%s</p>" % _inline(p))
        elif kind == "ul": h.append("<ul>%s</ul>" % "".join("<li>%s</li>" % _inline(x) for x in p))
        elif kind == "ol": h.append('<ol class="steps">%s</ol>' % "".join("<li>%s</li>" % _inline(x) for x in p))
        elif kind == "callout":
            t, body = p
            h.append('<div class="callout"><div class="ct">%s</div>%s</div>' % (html.escape(t), "".join("<p>%s</p>" % _inline(x) for x in body if x)))
        elif kind == "table":
            head, rows = p[0], p[1:]
            h.append('<div class="scroller"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
                "".join("<th>%s</th>" % _inline(c) for c in head),
                "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % _inline(c) for c in r) for r in rows)))
    return "\n".join(h)

# ---------------------------------------------------------------- text normalization
def strip_html(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h or ""))).strip()

def plain(md):
    """Markdown subset to plain text, for gates."""
    t = re.sub(r"[*`>|#]", " ", md or "")
    return re.sub(r"\s+", " ", t).strip()

def norm(s):
    s = html.unescape(s or "").lower().replace("’", "'").replace("—", " ").replace("–", " ").replace("-", " ")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()

def section_text(s):
    parts = [plain(s.get("body", "")), strip_html(s.get("html", ""))]
    m = s.get("map")
    if m:
        parts += [m.get("root", ""), m.get("note", "")] + [b["label"] + " " + " ".join(b["leaves"]) for b in m["branches"]]
    for lab, txt in s.get("asis", []):
        parts.append(plain(txt))
    return " ".join(parts)

def load(path):
    return json.load(open(path, encoding="utf-8"))

# ---------------------------------------------------------------- quiz: balance and verify
def all_questions(spec):
    qs = [(s["id"], q) for s in spec["sections"] for q in s.get("quiz", [])]
    qs += [("guide-quiz", q) for q in spec.get("quiz", [])]
    return qs

def is_recall(q):
    return q.get("type") == "recall"

def answer_text(q):
    return q["answer"] if is_recall(q) else q["o"][q["a"]]

def balance(spec):
    """Balanced, de-patterned correct-answer positions across the whole product, distractors shuffled,
    seeded so the result is reproducible. Records the intended answer text first and verifies it after."""
    rng = random.Random(spec.get("seed", 1))
    qs = [q for _, q in all_questions(spec) if not is_recall(q)]
    for q in qs:
        q["_intended"] = q["o"][q["a"]]
    n = len(qs)
    order = [i % 4 for i in range(n)]
    for _ in range(2000):
        rng.shuffle(order)
        if all(order[i] != order[i - 1] for i in range(1, n)):
            break
    else:
        raise SystemExit("could not place answers without adjacent repeats")
    for q, tgt in zip(qs, order):
        wrong = [o for i, o in enumerate(q["o"]) if i != q["a"]]
        rng.shuffle(wrong)
        q["o"] = wrong[:tgt] + [q["_intended"]] + wrong[tgt:]
        q["a"] = tgt
    return spec

def quiz_fails(spec):
    """Every failure the quiz rules define. Empty list means clean."""
    fails, warns = [], []
    qs = all_questions(spec)
    seen = {}
    for sid, q in qs:
        tag = "%s: %s" % (sid, q.get("q", "")[:60])
        if is_recall(q):
            if not str(q.get("answer", "")).strip(): fails.append(tag + ": recall question has no answer")
            if not q.get("e"): fails.append(tag + ": no explanation")
            if q.get("d") not in ("easy", "medium", "hard"): fails.append(tag + ": difficulty must be easy, medium, or hard")
            k = norm(q.get("q", ""))
            if k in seen: fails.append(tag + ": duplicate of a question in " + seen[k])
            seen[k] = sid
            continue
        o = q.get("o", [])
        if len(o) != 4: fails.append(tag + ": needs exactly four options")
        if any(not str(x).strip() for x in o): fails.append(tag + ": an option is empty")
        if len(set(norm(x) for x in o)) != len(o): fails.append(tag + ": two options are the same")
        if not isinstance(q.get("a"), int) or not 0 <= q["a"] < len(o): fails.append(tag + ": answer index out of range"); continue
        if "_intended" in q and o[q["a"]] != q["_intended"]:
            fails.append(tag + ": marked answer is not the intended text after the shuffle")
        if not q.get("e"): fails.append(tag + ": no explanation")
        if q.get("d") not in ("easy", "medium", "hard"): fails.append(tag + ": difficulty must be easy, medium, or hard")
        k = norm(q.get("q", ""))
        if k in seen: fails.append(tag + ": duplicate of a question in " + seen[k])
        seen[k] = sid
    mc = [(sid, q) for sid, q in qs if not is_recall(q)]
    rc = len(qs) - len(mc)
    if spec.get("quiz") and len(spec["quiz"]) >= 8 and sum(1 for q in spec["quiz"] if is_recall(q)) < len(spec["quiz"]) / 4:
        fails.append("the guide quiz needs at least a quarter free recall questions (type recall); multiple choice alone lets a student pass by elimination")
    n = len(mc)
    if n:
        pos = Counter(q["a"] for _, q in mc)
        if max(pos.values()) - min(pos.get(i, 0) for i in range(4)) > 1:
            fails.append("answer positions unbalanced: %s" % dict(sorted(pos.items())))
        seq = [q["a"] for _, q in mc]
        adj = sum(1 for i in range(1, n) if seq[i] == seq[i - 1])
        if adj: fails.append("%d adjacent questions share a correct position" % adj)
        n = len(qs)
        d = Counter(q.get("d") for _, q in qs)
        for lvl, lo, hi in (("easy", .10, .30), ("hard", .10, .30)):
            share = d.get(lvl, 0) / n
            if n >= 10 and not lo <= share <= hi:
                warns.append("%s questions are %.0f%% of the quiz; target about 20%%" % (lvl, share * 100))
    return fails, warns

# ---------------------------------------------------------------- gates
def _grams(words, k=3):
    return {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}

def sentences(text):
    t = re.sub(r"\s+", " ", text)
    return [x.strip() for x in re.split(r"(?<=[.!?:;])\s+|\s[•·]\s|\s\|\s", t) if len(x.split()) >= 6]

def coverage(spec, source_texts, cover=0.6):
    """Gate 1. Every source sentence of six words or more must be carried by the product: at least
    `cover` of its word triples appear somewhere in the product text. Sentences the spec excludes
    (spec['excluded'], each with a reason) are skipped. Returns (covered, total, missing list)."""
    body = norm(" ".join(section_text(s) for s in spec["sections"]) + " " + " ".join(
        plain(x.get("situation", "")) + " " + plain(x.get("key", "")) for x in spec.get("scenarios", [])))
    bg = _grams(body.split())
    excl = [norm(e["text"]) for e in spec.get("excluded", []) if e.get("reason")]
    total, got, missing = 0, 0, []
    for src in source_texts:
        for s in sentences(src):
            n = norm(s)
            if any(e and e in n for e in excl):
                continue
            g = _grams(n.split())
            if not g:
                continue
            total += 1
            if len(g & bg) / len(g) >= cover:
                got += 1
            else:
                missing.append(s)
    return got, total, missing

def _found(ans, body):
    a = norm(ans); toks = a.split()
    if a and a in body: return True
    for L in range(len(toks), 3, -1):
        for st in range(len(toks) - L + 1):
            if " ".join(toks[st:st + L]) in body:
                return True
    return False

def trace(spec):
    """Gate 2. Every teaching section's quiz answer is learnable from that section's own text; the
    final section (the last one, or any with "final": true) may draw on every section. The guide's
    own quiz may draw on any section. When the answer is worded differently from the body, the
    question carries "src": the exact body phrase that proves it, and that phrase is checked instead. Returns a list of untraceable (section, question, answer)."""
    secs = spec["sections"]
    allb = norm(" ".join(section_text(s) for s in secs))
    flags = []
    for i, s in enumerate(secs):
        final = s.get("final") or (i == len(secs) - 1 and len(secs) > 1 and spec.get("mode") == "walkthrough")
        b = allb if final else norm(section_text(s))
        for q in s.get("quiz", []):
            proof = q.get("src") or answer_text(q)
            if not _found(proof, b):
                flags.append((s["id"], q["q"][:70], answer_text(q)[:70]))
    for q in spec.get("quiz", []):
        if not _found(q.get("src") or answer_text(q), allb):
            flags.append(("guide-quiz", q["q"][:70], answer_text(q)[:70]))
    return flags

def locate(spec, q):
    """The section whose text carries the answer, for the answer key's 'where it is' line."""
    proof = q.get("src") or answer_text(q)
    words = {w for w in norm(q.get("q", "") + " " + q.get("e", "")).split() if len(w) > 4}
    best, score = "", -1
    for s in spec["sections"]:
        if s.get("final"):
            continue
        t = norm(section_text(s))
        if not _found(proof, t):
            continue
        sc = sum(1 for w in words if w in t)
        if sc > score:
            best, score = s["title"], sc
    return best

def dash_hits(spec):
    return [k for k in ("title", "subtitle") if re.search("[–—]", spec.get(k, ""))] + [
        s["id"] for s in spec["sections"] if re.search("[–—]", json.dumps(s, ensure_ascii=False))]
