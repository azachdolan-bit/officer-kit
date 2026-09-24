#!/usr/bin/env python3
"""Build a single file interactive walkthrough from a spec.
Usage: python3 build_walkthrough.py <spec.json> <out.html>
Balances answer positions (seeded), verifies the quiz rules, and writes one self contained HTML file:
a mind map section with recall modes, one teaching section per chapter with its own check, the
complete source text for the section behind "Read it as issued", and a final check across all."""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import study_lib as L
HERE = os.path.dirname(os.path.abspath(__file__))

def main(spec_path, out):
    spec = L.balance(L.load(spec_path))
    fails, _ = L.quiz_fails(spec)
    if fails:
        print("NOT BUILT: quiz rules fail"); [print("  ", f) for f in fails]; return 1
    S = []
    for s in spec["sections"]:
        body = L.md_html(s.get("body", "")) + s.get("html", "")
        if s.get("asis"):
            inner = "".join('<div class="al">%s</div>%s' % (html.escape(lab), L.md_html(t)) for lab, t in s["asis"])
            body += '<details class="asis"><summary>Read it as issued<span>the complete source text for this section</span></summary><div class="asisb">%s</div></details>' % inner
        S.append({"id": s["id"], "title": html.escape(s["title"]), "eyebrow": html.escape(s.get("eyebrow", "")),
                  "lede": html.escape(s.get("lede", "")), "body": body, "map": s.get("map"), "branch": s.get("branch"),
                  "quiz": [{"q": html.escape(q["q"]), "o": [html.escape(o) for o in q["o"]], "a": q["a"], "e": html.escape(q["e"])} for q in s.get("quiz", [])]})
    ids = {s["id"] for s in S}
    for s in S:
        if s.get("map"):
            for b in s["map"]["branches"]:
                assert b.get("sec") in ids, "map branch points to no section: %s" % b.get("sec")
    bands = spec.get("bands") or [["Ready", "You can recall and apply this lesson. Come back in a few days and take the final check cold."],
                                  ["Close", "Rerun the sections where you dropped questions, then take the final check again."],
                                  ["Building", "Go back to the map, recall each branch from memory, then work the missed sections."],
                                  ["Start over", "Start at the map. Learn the branches first so the details have somewhere to attach."]]
    head = open(os.path.join(HERE, "engine_head.html"), encoding="utf-8").read()
    tail = open(os.path.join(HERE, "engine_tail.html"), encoding="utf-8").read()
    for k, v in (("{{TITLE}}", html.escape(spec["title"])), ("{{SUBTITLE}}", html.escape(spec.get("subtitle", ""))),
                 ("{{NSEC}}", "%02d" % len(S)), ("{{LABEL}}", html.escape(spec.get("score_label", "SCORE")))):
        head = head.replace(k, v)
    consts = "const GOOD=%s, BAD=%s, COMMIT=%s, BANDS=%s;\nconst SECTIONS = %s;\n" % (
        json.dumps(spec.get("good", "Correct")), json.dumps(spec.get("bad", "Missed")),
        json.dumps(spec.get("commit", "Answers lock once chosen.")),
        json.dumps(bands, ensure_ascii=False), json.dumps(S, ensure_ascii=False, indent=1))
    open(out, "w", encoding="utf-8").write(head + consts + tail)
    print("written", out, "sections", len(S), "questions", sum(len(s["quiz"]) for s in S))
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 3: sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
