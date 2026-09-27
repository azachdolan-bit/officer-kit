#!/usr/bin/env python3
"""topic-brief harness: a good brief, script, and card pass; a bad brief fails on the opening that
misses the topic, a two paragraph context, an untraced number, a line it was told not to say, and a
dash; a bad script fails on run time, a time mark out of place, untraced numbers, a quote no source
carries, a forbidden line, and a doctrine named but not quoted; a bad card fails on a sentence where
key words belong, marks out of order, an uncited quote, a quote not in the script, a stray mark, and a dash.
Usage: python3 evals/topic_brief_check.py"""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, "plugins", "officer-kit", "skills", "topic-brief")
EV = os.path.join(ROOT, "evals", "topic-brief")
sys.path.insert(0, os.path.join(SK, "scripts"))
import brief_check as BC, build_card as CD
fails, n = [], 0
def ok(c, m):
    global n
    n += 1
    if not c: fails.append(m)
rd = lambda f: open(os.path.join(EV, f), encoding="utf-8").read()
S = [os.path.join(EV, "source.md"), os.path.join(EV, "doctrine.md")]
def failed(res, key):
    return any(key in m and not c for c, m in res)
r = BC.check(rd("good-brief.md"), "brief")
ok(all(c for c, _ in r), "the good brief must pass: %s" % [m for c, m in r if not c])
r = BC.check(rd("bad-brief.md"), "brief")
for key in ("opening paragraph names the topic", "context is one paragraph", "every number is traced", "no line from lines not to say", "no em or en dashes"):
    ok(failed(r, key), "the bad brief must fail on: " + key)
r = BC.check(rd("good-script.md"), "script", S, "FN 7", [0.5, 1, 0.5])
ok(all(c for c, _ in r), "the good script must pass: %s" % [m for c, m in r if not c])
r = BC.check(rd("bad-script.md"), "script", S, "FN 7")
for key in ("run time", "every time mark is within", "every number is traced", "verbatim in a source", "no line from lines not to say", "the sources table names FN 7", "quotes FN 7"):
    ok(failed(r, key), "the bad script must fail on: " + key)
ok(BC.numbers("the 23d and 24th Marines, 1,375 meters, E/2/23") == ["23", "24", "1375", "2", "23"], "numbers read through ordinals, commas, and unit designators")
ok(BC.traced("1375", "| range 1,375 meters |") and not BC.traced("37", "| 375 |"), "a number is traced only as a whole number")
safe = '# T\n\nTopic: x\n\n## Where every fact comes from\n| a | b |\n\n## Lines not to say\n- A toll higher than "at least 53." Sources differ.\n\nBody says at least 53.\n'
ok(not failed(BC.check(safe, "brief"), "no line from lines not to say"), "a quoted safe line inside a bullet's reason is not a forbidden line")
card = json.loads(rd("card.json"))
r = CD.check(card, rd("good-script.md"))
ok(all(c for c, _ in r), "the good card must pass: %s" % [m for c, m in r if not c])
r = CD.check(json.loads(rd("bad-card.json")), rd("good-script.md"))
for key in ("eight words or fewer", "time marks run in order", "carries its citation", "word for word in the script", "one of the script's section marks", "no em or en dashes"):
    ok(failed(r, key), "the bad card must fail on: " + key)
clk = {"faces": [{"lines": [{"t": "0:00", "text": "Diary: 2:30, grenades"}]}, {"lines": [{"text": "no mark here"}]}]}
r = CD.check(clk)
ok(failed(r, "no clock time written as m:ss"), "a clock time in m:ss form on a card line must fail")
ok(failed(r, "every face carries at least one time mark"), "a face with no time mark must fail")
html = CD.render(card)
ok("@page{size:5in 3in" in html and html.count("<section>") == 2, "the card renders one page per face at 5 by 3 inches")
for f in [os.path.join(SK, "SKILL.md")] + glob.glob(os.path.join(SK, "references", "*.md")):
    ok(not re.search("[–—]", open(f, encoding="utf-8").read()), os.path.relpath(f, ROOT) + " carries an em or en dash")
ok("../../STANDARDS.md" in open(os.path.join(SK, "SKILL.md"), encoding="utf-8").read(), "SKILL.md must read STANDARDS.md")
print("TOPIC BRIEF CHECK: %d items" % n)
for f in fails: print("  FAIL ", f)
print("-> %d of %d pass" % (n - len(fails), n))
sys.exit(1 if fails else 0)
