#!/usr/bin/env python3
"""Deterministic evals for the Path D core tools (reenlistment, mrow-input, jepes-input, directive, board-prep,
meritorious-mast, deocs-plan, memo, endorsement). Exit 0 = all pass."""
import os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, "..", "plugins", "officer-kit", "skills")
def run(*a, **kw): return subprocess.run([sys.executable, *a], capture_output=True, text=True, **kw)
res = []
def case(name, script, inp, exit_code, *needles, extra=()):
    r = run(f"{S}/{script}", *( [f"{H}/{inp}"] if inp else [] ), *extra)
    ok = r.returncode == exit_code and all(n in r.stdout for n in needles)
    if not ok:
        print(f"--- {name}: exit {r.returncode}\n{r.stdout}{r.stderr}")
    res.append((name, ok))
# reenlistment
case("reenlistment good", "reenlistment/scripts/reenlistment_check.py", "reenlistment/inputs/good.md", 0, "clean")
case("reenlistment bad", "reenlistment/scripts/reenlistment_check.py", "reenlistment/inputs/bad.md", 1, "population claim", "promise about the decision", "family or personal", "certification line", "windows do not match", "Corporal Brandt")
case("reenlistment notrec delegated", "reenlistment/scripts/reenlistment_check.py", "reenlistment/inputs/notrec_bad.md", 1, "may not be delegated", "commanding officer's interview", "dated facts")
case("reenlistment over tier", "reenlistment/scripts/reenlistment_check.py", "reenlistment/inputs/over_tier.md", 1, "top 60%", "requires the top 50 percent")
case("reenlistment windows", "reenlistment/scripts/reenlistment_windows.py", None, 0, "19 June 2025 to 19 August 2025", "19 June 2026 to 19 August 2026", "19 December 2026 to 19 February 2027", "standard:", extra=("--ecc", "19 August 2027", "--today", "2026-09-05"))
case("reenlistment windows immediate", "reenlistment/scripts/reenlistment_windows.py", None, 0, "immediate: 75 days", extra=("--ecc", "2027-03-31", "--today", "2027-01-15"))
# mrow-input
case("mrow-input good", "mrow-input/scripts/mrow_input_check.py", "mrow-input/inputs/good.md", 0, "clean")
case("mrow-input bad", "mrow-input/scripts/mrow_input_check.py", "mrow-input/inputs/bad.md", 1, "From <day month year> To <day month year>", "no 'RS:' billet", "superlative 'BEST'", "not in bulleted text format", "exclamation is not permitted", "'Awarded' is an award or commendatory material", "'potential' is a personal quality", "selection board or court-martial", "'NJP' falls under unacceptable comments", "a claim about the marks", "Staff Sergeant Okafor")
case("mrow-input awards in c", "mrow-input/scripts/mrow_input_check.py", "mrow-input/inputs/awards_in_c.md", 1, "'Awarded' is an award or commendatory material", "selection board or court-martial (6.b Note", "PME or schooling appears in the accomplishments")
# jepes-input
case("jepes-input good", "jepes-input/scripts/jepes_input_check.py", "jepes-input/inputs/good.md", 0, "clean")
case("jepes-input bad", "jepes-input/scripts/jepes_input_check.py", "jepes-input/inputs/bad.md", 1, "grade 'Sergeant' is not covered", "do not make recommended command input marks", "is not a SA end date", "more than 45 days before", "no dated fact under the mark", "requires formal commendatory material", "is 'Exceeds Expectations' in the order's bands, not 'Meets Expectations'", "no fact dated inside the period", "the order places it on counseling", "a promise about promotion", "family or personal", "Corporal Hastings")
case("jepes-input exceptional unsupported", "jepes-input/scripts/jepes_input_check.py", "jepes-input/inputs/exceptional_bad.md", 1, "4.5 is Exceptional", "requires formal commendatory material", "no fact dated inside the period 1 August 2025 to 31 January 2026")
case("jepes-input counseling good", "jepes-input/scripts/jepes_input_check.py", "jepes-input/inputs/counseling_good.md", 0, "clean")
case("jepes-input dates", "jepes-input/scripts/jepes_dates.py", None, 0, "1 February 2026 to 31 July 2026", "submit no earlier than: 16 June 2026", "initial written counseling due: 12 October 2025", extra=("--occasion", "SA", "--to", "31 July 2026", "--supervision", "12 September 2025"))
case("jepes-input dates wrong month", "jepes-input/scripts/jepes_dates.py", None, 1, "not a TO date the order fixes for SA", extra=("--occasion", "SA", "--to", "30 June 2026"))
# directive
case("directive good", "directive/scripts/directive_check.py", "directive/inputs/good.md", 0, "clean")
case("directive bad", "directive/scripts/directive_check.py", "directive/inputs/bad.md", 1, "Type: 'SOP'", "below the battalion or squadron level", "Situation must be the first paragraph", "mandatory paragraph 'Mission' missing", "Coordinating Instructions", "Signal altered", "reference (b) is listed and never cited", "distribution statement A altered", "grade or rank in the signature block", "J. R. HOLLISTER", "lifted from the exemplar")
case("directive bulletin no canc", "directive/scripts/directive_check.py", "directive/inputs/bulletin_no_canc.md", 1, "self-canceling provision", "1 failures")
# board-prep
case("board-prep good", "board-prep/scripts/board_prep_check.py", "board-prep/inputs/good.md", 0, "clean")
case("board-prep bad", "board-prep/scripts/board_prep_check.py", "board-prep/inputs/bad.md", 1, "disagrees with the table", "not two weeks prior to the convening date", "verified with no date", "gap without its dates", "does not name the course", "ties PME to promotion", "not a title ALMAR 024/25 prints", "paragraph 8.a", "paragraph 8.b", "a prediction of the result", "Captain Reyes", "medical", "lifted from the exemplar", "em or en dash present")
case("board-prep letter rules", "board-prep/scripts/board_prep_check.py", "board-prep/inputs/letter_bad.md", 1, "paragraph 8.d", "will not become part of an officer's OMPF", "Late correspondence will not be accepted", "request for non selection")
# meritorious-mast
case("meritorious-mast good", "meritorious-mast/scripts/meritorious_mast_check.py", "meritorious-mast/inputs/good.md", 0, "clean")
case("meritorious-mast certcom good", "meritorious-mast/scripts/meritorious_mast_check.py", "meritorious-mast/inputs/certcom_good.md", 0, "clean")
case("meritorious-mast bad", "meritorious-mast/scripts/meritorious_mast_check.py", "meritorious-mast/inputs/bad.md", 1, "level check says the facts are a Certificate of Commendation", "below the echelon the order sets", "numbers in the text not found in ## Facts", "a promise", "family or personal", "routing sends something to CMC (MMMA)", "does not send a copy to CMC (MMSB)", "a unit is named", "Corporal Ostrander", "lifted from the exemplar", "em or en dash present")
case("meritorious-mast level decoration", "meritorious-mast/scripts/meritorious_mast_check.py", "meritorious-mast/inputs/level_bad.md", 1, "level check says the facts are a personal decoration", "shall not be conducted", "-> 1 failures")
# deocs-plan
case("deocs-plan good", "deocs-plan/scripts/deocs_plan_check.py", "deocs-plan/inputs/good.md", 0, "clean")
case("deocs-plan bad", "deocs-plan/scripts/deocs_plan_check.py", "deocs-plan/inputs/bad.md", 1, "is not a billet; the plan carries billets", "outside 1 August to 30 November", "after 31 October", "precedes the survey close", "does not name the report section", "finding 3 has no action", "action 1 has no 'Measure:'", "promises the outcome ('will improve')", "The Sergeant who wrote", "Lieutenant Colonel Harmon", "lifted from the exemplar", "blocked content: SAPR or investigation ('NJP')")
case("deocs-plan identify", "deocs-plan/scripts/deocs_plan_check.py", "deocs-plan/inputs/identify_bad.md", 1, "more than 90 days after assumption of command", "one respondent said", "the only female Sergeant in", "the Marine in finding 2", "a claim about the outcome ('will improve')")
# endorsement
case("endorsement good", "endorsement/scripts/endorsement_check.py", "endorsement/inputs/good.json", 0, "clean")
case("endorsement bad", "endorsement/scripts/endorsement_check.py", "endorsement/inputs/bad.json", 1, "is not a written ordinal", "does not carry the basic correspondence's date", "Subj changed", "does not state the endorser's action", "already on the basic letter", "a promise about the decision", "Corporal Brandt", "family or personal", extra=("--basic-subj", "REQUEST FOR SPECIAL LIBERTY", "--basic-refs", "MCO 1050.3J"))
case("endorsement later ordinal", "endorsement/scripts/endorsement_check.py", "endorsement/inputs/later.json", 0, "9-2.1.b", "the ordinal counts the endorsements already on it", "no reason")
# memo
case("memo mfr good", "memo/scripts/memo_check.py", "memo/inputs/good.md", 0, "clean")
case("memo mfr bad", "memo/scripts/memo_check.py", "memo/inputs/bad.md", 1, "no originator Code", "not in capitals", "without a Signer line", "no date in the paragraphs", "it does not argue", "Gunny Ostrowski")
case("memo point paper", "memo/scripts/memo_check.py", "memo/inputs/point_paper.md", 0, "clean")
# A bare "Memorandum" is now ambiguous rather than out of scope: chapter 10 prints five and they
# are not interchangeable, so the checker names them and refuses to guess.
case("memo kind must be named", "memo/scripts/memo_check.py", "memo/inputs/from_to_memo.md", 1, "does not say which", "10-2.2", "10-2.6")
# The SECNAV M-5216.5 formats, added 18 September 2026 once the manual reached the library.
case("memo from to", "memo/scripts/memo_check.py", "memo/inputs/from_to_good.md", 0, "clean")
case("memo plain paper with decision block", "memo/scripts/memo_check.py", "memo/inputs/plain_paper_decision.md", 0, "clean")
case("memo agreement", "memo/scripts/memo_check.py", "memo/inputs/moa_good.md", 0, "clean")
case("memo business letter", "memo/scripts/memo_check.py", "memo/inputs/business_letter_good.md", 0, "clean")
# The trap this format exists to catch: a Marine writing a business letter the way he writes a
# naval letter. Every failure below is a habit that carries over and should not.
case("memo business letter with naval habits", "memo/scripts/memo_check.py", "memo/inputs/business_letter_bad.md", 1,
     "is not the civilian format", "a '## Ref' block on a business letter", "a '## Encl' block on a business letter",
     "without calling them references or enclosures", "11-2.8 gives one and only one", "Do not number main paragraphs")
# the endorsement renders and passes the correspondence gates
import tempfile, subprocess as _sp
_t = tempfile.mkdtemp()
_r1 = run(f"{S}/naval-letter/scripts/build_letter.py", f"{H}/endorsement/inputs/good.json", f"{_t}/e.docx")
_r2 = run(f"{S}/naval-letter/scripts/qc_letter.py", f"{_t}/e.docx", "--kind", "endorsement")
_sp.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", _t, f"{_t}/e.docx"], capture_output=True)
_r3 = run(f"{S}/naval-letter/scripts/measure_pdf.py", f"{_t}/e.pdf")
import zipfile as _zf
_xml = _zf.ZipFile(f"{_t}/e.docx").read("word/document.xml").decode() if os.path.exists(f"{_t}/e.docx") else ""
res.append(("endorsement renders and passes the letter gates", _r1.returncode == 0 and _r2.returncode == 0 and _r3.returncode == 0 and "FIRST ENDORSEMENT on" in _xml))

# find_order.py: a publication saved as bare digits is still that publication, while a file that
# claims a different family is still rejected. Both halves failed silently once, in opposite
# directions: the library path never resolved, and SECNAV M-1650.1 matched MCO 1650.19J.
_FO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "plugins", "officer-kit", "skills", "library", "scripts")
sys.path.insert(0, _FO)
import find_order as _fo  # noqa: E402
import tempfile as _tf, pathlib as _pl  # noqa: E402
_d = _tf.mkdtemp()
_pl.Path(_d, "5216.5  CH-1.pdf").write_text("x")
_pl.Path(_d, "MCOs").mkdir()
_pl.Path(_d, "MCOs", "MCO_1650.19J.pdf").write_text("x")
_h, _ = _fo.find("SECNAV M-5216.5", [_d])
res.append(("bare number filename resolves for a SECNAV manual", len(_h) == 1 and "5216.5" in _h[0]))
_h2, _ = _fo.find("SECNAV M-1650.1", [_d])
res.append(("a file claiming another family is still rejected", not _h2))
_h3, _ = _fo.find("MCO 1650.19J", [_d])
res.append(("the MCO still resolves for its own query", len(_h3) == 1))

bad = 0
for n, ok in res:
    print(f"{'PASS' if ok else 'FAIL'}  {n}"); bad += 0 if ok else 1
print(f"-> {len(res) - bad} of {len(res)} pass"); sys.exit(1 if bad else 0)
