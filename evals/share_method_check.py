#!/usr/bin/env python3
"""share-method harness: the builder template and a good builder carry every safeguard, a bad builder
fails on each missing one, the leak scan passes a clean builder and catches every planted leak in a bad
one (acronym, name, value, copied run, browser automation), whole word matching keeps "not" from
matching OT, allow lines need a reason and never cover browser automation, and wording shared only with
the user's own product is read as method unless it carries a term or a value.
Usage: python3 evals/share_method_check.py"""
import glob, os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, "plugins", "officer-kit", "skills", "share-method")
SC = os.path.join(SK, "scripts")
EV = os.path.join(ROOT, "evals", "share-method")
sys.path.insert(0, SC)
import leak_scan as L, builder_check as B
fails, n = [], 0
def ok(c, m):
    global n
    n += 1
    if not c: fails.append(m)
def run(*a):
    r = subprocess.run([sys.executable] + list(a), capture_output=True, text=True, cwd=EV)
    return r.returncode, r.stdout + r.stderr
rd = lambda f: open(os.path.join(EV, f), encoding="utf-8").read()
src, good, bad = rd("source.md"), rd("good-builder.md"), rd("bad-builder.md")
tpl = open(os.path.join(SK, "references", "builder-template.md"), encoding="utf-8").read().split("\n---\n", 1)[1]
ok(all(c for c, _ in B.check(tpl, app=True)), "the builder template must pass its own check")
ok(all(c for c, _ in B.check(good)), "the good builder must pass the builder check")
badres = dict((m, c) for c, m in B.check(bad))
for key in ("contains no course material", "only authority", "stop and ask", "browser automation"):
    ok(any(key in m and not c for m, c in badres.items()), "the bad builder must fail on: " + key)
code, out = run(os.path.join(SC, "leak_scan.py"), "good-builder.md", "--source", "source.md", "--terms", "fp-terms.txt")
ok(code == 0 and "Verdict: CLEAN" in out, "the good builder must scan clean:\n" + out)
ok(re.search(r"MIST.*OT.*ROUND", out.split("Substring only")[-1]), "OT, MIST, and ROUND must be listed as substring only, not leaks")
r = L.scan(bad, [src])
hit_terms = set(h[0] for h in r["hits"])
for t in ("HWR", "Coastal Watch Station", "45", "250"):
    ok(t in hit_terms, "the bad builder's %s must be a hit" % t)
ok(any("rounds down not up" in x for x in r["runs"]), "the copied tie rule sentence must be a copied run")
ok(any(m[0].lower() == "claude in chrome" for m in r["mechanism"]), "the browser automation line must be caught")
ok(not L.wordrx("OT").search("do not rotate"), "OT must not match inside 'not'")
ok(not L.wordrx("Student Handout", "name").search("a student handout"), "a capitalized name must match only as capitalized")
ok("ROUND" not in L.source_terms("ROUND the value. Always round down."), "an all capitals word the source also writes in lower case is not an acronym")
r2 = L.scan(bad, [src], allow={"Claude in Chrome": "testing", "HWR": "fictional"})
ok(r2["mechanism"] and not r2["clean"], "browser automation can never be allowed")
ok(any(a[0] == "HWR" for a in r2["allowed"]), "an allowed term must be reported as allowed")
tmp = tempfile.mkdtemp(); af = os.path.join(tmp, "allow.txt"); open(af, "w").write("HWR\n")
code, out = run(os.path.join(SC, "leak_scan.py"), "bad-builder.md", "--source", "source.md", "--allow", af)
ok(code != 0 and "no reason" in out, "an allow line with no reason must be refused")
prod = "Keep every turn short and then stop and wait for the student to answer before going on. Report the HWR count within the hour."
r3 = L.scan("Keep every turn short and then stop and wait for the student to answer.", [""], products=[prod])
ok(r3["method_runs"] and not r3["runs"] and r3["clean"], "wording shared only with the product and carrying no term is method wording")
r4 = L.scan("Always report the HWR count within the hour to the station.", [""], products=[prod])
ok(not r4["clean"], "wording shared with the product that carries a term must fail")
r5 = L.scan("Report it only when it moves toward the breakwater and fewer than 2 are seen.\n2. Next step.", [src])
ok("breakwater" in r5["vocab"], "a lower case subject word shared with the source must be listed to read")
ok(r5["small"] == ["2"], "a small threshold in prose must be listed to read, and a list number must not: %s" % r5["small"])
ok("verify" not in L.scan("Verify every worked example before writing.", ["Verify the example."])["vocab"], "a word the kit's own method text uses is not listed")
for f in [os.path.join(SK, "SKILL.md")] + glob.glob(os.path.join(SK, "references", "*.md")):
    ok(not re.search("[–—]", open(f, encoding="utf-8").read()), os.path.relpath(f, ROOT) + " carries an em or en dash")
ok("../../STANDARDS.md" in open(os.path.join(SK, "SKILL.md"), encoding="utf-8").read(), "SKILL.md must read STANDARDS.md")
print("SHARE METHOD CHECK: %d items" % n)
for f in fails: print("  FAIL ", f)
print("-> %d of %d pass" % (n - len(fails), n))
sys.exit(1 if fails else 0)
