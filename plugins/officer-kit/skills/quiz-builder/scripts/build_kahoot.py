#!/usr/bin/env python3
"""Build Kahoot import files from a quiz spec by filling the user's copy of Kahoot's official template.

Usage: python3 build_kahoot.py <spec.json> --template <KahootQuizTemplate.xlsx> --out <folder>
                               [--source <file> ...] [--report <gate report.md>]

1. Places answers (seeded, balanced, no two adjacent questions on one slot; numeric sets ascending).
2. Checks every rule in references/rules.md; with --source, every answer must be found in the sources.
3. Copies the template once per deck, keeps its instruction rows, merges, and styling, overwrites the
   example row, fills from the first question row down, and extends the time dropdown to every row.
4. Reads each written file back and verifies, cell by cell, that the correct slot resolves to the
   intended answer text, every used answer cell is filled, and every time is one the template allows.
Nothing is written if step 2 fails. Exit 0 only when every step passes."""
import datetime, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiz_lib as Q
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

def template_layout(path):
    wb = load_workbook(path)
    ws = wb.active
    header = None
    for r in range(1, 30):
        v = str(ws.cell(r, 2).value or "")
        if v.lower().startswith("question"):
            header = r; break
    if header is None:
        raise SystemExit("TEMPLATE: no 'Question' header in column B; is this Kahoot's quiz import template?")
    times = None
    for dv in ws.data_validations.dataValidation:
        if dv.formula1 and re.search(r"\d", dv.formula1):
            times = [int(x) for x in re.findall(r"\d+", dv.formula1)]
    return header, times

def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "", name).strip()

def main(argv):
    if len(argv) < 2: sys.exit(__doc__)
    args, spec_path = argv[2:], argv[1]
    tpl, out, report, sources = None, None, None, []
    it = iter(args)
    for a in it:
        if a == "--template": tpl = next(it)
        elif a == "--out": out = next(it)
        elif a == "--report": report = next(it)
        elif a == "--source": sources.append(next(it))
    if not tpl or not os.path.exists(tpl):
        print("NOT BUILT: no template. Download Kahoot's official quiz import template (Kahoot Help Center, "
              "'How to import questions from a spreadsheet to your kahoot'), save it in the working folder, and pass it with --template.")
        return 1
    header, times = template_layout(tpl)
    spec = Q.place(Q.load(spec_path))
    srcs = [open(f, encoding="utf-8", errors="replace").read() for f in sources] or None
    fails, warns = Q.check(spec, srcs, times)
    lines = ["Template: %s (question header row %d, allowed times %s)" % (os.path.basename(tpl), header, times)]
    lines += ["Sources: " + (", ".join(os.path.basename(s) for s in sources) if sources else "NONE GIVEN: answers not traced")]
    lines += ["RULES: %d failures" % len(fails)] + ["   " + f for f in fails] + ["   warn: " + w for w in warns]
    if fails:
        lines.append("RESULT: NOT BUILT"); print("\n".join(lines)); _save(report, lines); return 1
    os.makedirs(out, exist_ok=True)
    tmap = spec.get("time_by_difficulty", Q.DEFAULT_TIMES)
    readback = []
    for d in spec["decks"]:
        wb = load_workbook(tpl); ws = wb.active
        first = header + 1
        last_used = max(ws.max_row, first + len(d["questions"]))
        for r in range(first, last_used + 1):
            for c in range(2, 9): ws.cell(r, c).value = None
        for i, q in enumerate(d["questions"]):
            r = first + i
            ws.cell(r, 1).value = i + 1
            ws.cell(r, 2).value = q["q"]
            for j, o in enumerate(q["o"]): ws.cell(r, 3 + j).value = o
            ws.cell(r, 7).value = Q.time_for(q, tmap, times)
            ws.cell(r, 8).value = str(q["a"] + 1)
        if times:
            ws.data_validations.dataValidation = []
            dv = DataValidation(type="list", formula1='"%s"' % ",".join(str(t) for t in times), allow_blank=True)
            dv.add("G%d:G%d" % (first, first + len(d["questions"]) - 1)); ws.add_data_validation(dv)
        path = os.path.join(out, safe(d["name"]) + ".xlsx")
        wb.save(path)
        # read back
        ws2 = load_workbook(path).active; bad = 0
        for i, q in enumerate(d["questions"]):
            r = first + i
            slot = int(str(ws2.cell(r, 8).value).split(",")[0])
            if ws2.cell(r, 2 + slot).value != q["_intended"]: bad += 1
            if any(not ws2.cell(r, 3 + j).value for j in range(len(q["o"]))): bad += 1
            if times and ws2.cell(r, 7).value not in times: bad += 1
        readback.append((path, len(d["questions"]), bad))
    from collections import Counter
    for path, n, bad in readback:
        lines.append("READ BACK %s: %d questions, %d problems %s" % (os.path.basename(path), n, bad, "PASS" if not bad else "FAIL"))
    for d in spec["decks"]:
        lines.append("   %s slots %s" % (d["name"], dict(sorted(Counter(q["a"] + 1 for q in d["questions"]).items()))))
    ok = all(b == 0 for _, _, b in readback)
    lines.append("RESULT: %s" % ("CLEAN" if ok else "NOT CLEAN"))
    print("\n".join(lines)); _save(report, lines)
    return 0 if ok else 1

def _save(report, lines):
    if report:
        os.makedirs(os.path.dirname(os.path.abspath(report)), exist_ok=True)
        with open(report, "w", encoding="utf-8") as fh:
            fh.write("# Quiz gate report\n\nRun: %s\n\n```\n%s\n```\n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "\n".join(lines)))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
