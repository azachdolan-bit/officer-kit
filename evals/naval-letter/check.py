#!/usr/bin/env python3
"""Deterministic eval for the naval-letter skill. Exit 0 = all cases pass.

Runs the three cases in cases.json against the skill's own scripts:
golden build passes both gates; withheld identity fails Gate 2 on placeholders;
a two page letter measures correctly on the continuation page.
Requires python-docx, pdftotext, and soffice.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.abspath(os.path.join(HERE, "..", "..", "plugins", "officer-kit", "skills", "naval-letter", "scripts"))
SPEC = os.path.join(HERE, "inputs", "sample_spec.json")


def run(*args, **kw):
    return subprocess.run(list(args), capture_output=True, text=True, **kw)


def to_pdf(docx, cwd):
    r = run("soffice", "--headless", "--convert-to", "pdf", docx, cwd=cwd)
    pdf = os.path.splitext(docx)[0] + ".pdf"
    return pdf if os.path.exists(pdf) else None


def main():
    tmp = tempfile.mkdtemp(prefix="nl-eval-")
    results = []

    # case 1: golden build
    docx = os.path.join(tmp, "golden.docx")
    b = run(sys.executable, os.path.join(SCRIPTS, "build_letter.py"), SPEC, docx)
    q = run(sys.executable, os.path.join(SCRIPTS, "qc_letter.py"), docx, "--encl-title", "Sample Exam Query Form")
    pdf = to_pdf(docx, tmp)
    m = run(sys.executable, os.path.join(SCRIPTS, "measure_pdf.py"), pdf) if pdf else None
    ok = b.returncode == 0 and "placeholders left" not in b.stdout and q.returncode == 0 and m is not None and m.returncode == 0
    results.append(("golden-build", ok, (q.stdout + (m.stdout if m else "no pdf")).strip().splitlines()[-1]))

    # case 2: withheld identity must fail Gate 2
    spec = json.load(open(SPEC))
    for k in ("from", "originator_code", "signature"):
        spec.pop(k, None)
    spec_path = os.path.join(tmp, "anon.json")
    json.dump(spec, open(spec_path, "w"))
    docx2 = os.path.join(tmp, "anon.docx")
    b2 = run(sys.executable, os.path.join(SCRIPTS, "build_letter.py"), spec_path, docx2)
    q2 = run(sys.executable, os.path.join(SCRIPTS, "qc_letter.py"), docx2)
    ok2 = all(p in b2.stdout for p in ("[FROM LINE]", "[ORIGINATOR CODE]", "[SIGNATURE]")) and q2.returncode == 1 and q2.stdout.count("placeholder") >= 3
    results.append(("withheld-identity", ok2, q2.stdout.strip().splitlines()[-1]))

    # case 3: two page letter
    spec = json.load(open(SPEC))
    filler = [{"text": f"Discussion continued, item {i}.  " + "This paragraph exists only to push the letter onto a second page so the continuation page can be measured. " * 2} for i in range(1, 9)]
    spec["paragraphs"] = spec["paragraphs"][:2] + filler + spec["paragraphs"][2:]
    spec_path3 = os.path.join(tmp, "long.json")
    json.dump(spec, open(spec_path3, "w"))
    docx3 = os.path.join(tmp, "long.docx")
    run(sys.executable, os.path.join(SCRIPTS, "build_letter.py"), spec_path3, docx3)
    q3 = run(sys.executable, os.path.join(SCRIPTS, "qc_letter.py"), docx3, "--encl-title", "Sample Exam Query Form")
    pdf3 = to_pdf(docx3, tmp)
    m3 = run(sys.executable, os.path.join(SCRIPTS, "measure_pdf.py"), pdf3) if pdf3 else None
    ok3 = q3.returncode == 0 and m3 is not None and m3.returncode == 0 and "pages: 2" in m3.stdout and "82." in m3.stdout
    results.append(("two-page", ok3, (m3.stdout if m3 else "no pdf").strip().splitlines()[-1]))

    shutil.rmtree(tmp, ignore_errors=True)
    bad = 0
    for name, ok, last in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {last}")
        bad += 0 if ok else 1
    print(f"-> {len(results) - bad} of {len(results)} cases pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
