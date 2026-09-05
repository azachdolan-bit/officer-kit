#!/usr/bin/env python3
"""Check a unit directive draft (directive.md) against MCO 5215.1K w/Admin Ch 3, enclosure (1):
chapter 1 (definitions, supplements, signature, identification, paragraphs), chapter 2 (orders, figure 2-2),
chapter 3 (bulletins, figures 3-1 and 3-2).

Usage:  python3 directive_check.py directive.md
Exit 0 = passes (warnings allowed); 1 = a directive type the order does not issue, a required paragraph or
subparagraph missing or out of order, a required statement missing or altered, a bulletin without its cancellation
line or past 12 months, a supplement the order bars at this echelon, a reference listed and not cited or cited
and not listed, a signature block with a rank or the principal's title, a name, blocked content about a person,
a lifted exemplar phrase, or an em or en dash.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes  # noqa: E402

ORDER_SEQ = ["Situation", "Cancellation", "Mission", "Execution", "Administration and Logistics", "Command and Signal"]
EXEC_SUBS = ["Commander's Intent and Concept of Operations", "Subordinate Element Missions", "Coordinating Instructions"]
MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
MONTH_NUM = {m: i + 1 for i, m in enumerate(MONTHS.split("|"))}
CANC = r"Canc(?: frp)?:\s*(" + MONTHS + r")\w*\s+(\d{4})"
SIGNED_DATE = r"\(Date Signed\)|\b\d{1,2} (?:" + MONTHS + r") (?:\d{4}|\d{2})\b"
BELOW_BN = r"\b(?:company|battery|detachment|platoon|section|troop)\b"
BARRED = r"leave and liberty|\bliberty\b|\bleave\b|assumption of command|alcohol|mail ?handling|mail ?room|command security|security procedures|classified material"
RANKS = r"\b(?:General|Colonel|Lieutenant Colonel|Major|Captain|Lieutenant|Sergeant Major|Master Gunnery Sergeant|First Sergeant|Master Sergeant|Gunnery Sergeant|Staff Sergeant|Sergeant|Corporal|Gen|Col|LtCol|Maj|Capt|1stLt|2ndLt|CWO\d|SgtMaj|MGySgt|1stSgt|MSgt|GySgt|SSgt|Sgt|Cpl|LCpl|USMC|USMCR|U\.S\. Marine Corps)\b"
GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|Colonel|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|2ndLt|1stLt|Capt|Maj|LtCol|Col)"
TITLE_WORDS = r"(?:Major|Sergeant|Commander|Officer|Corporal|Gunnery|Staff|Master|First|Second|Lance|General|Colonel)"
DIST_A = "DISTRIBUTION STATEMENT A: Approved for public release; distribution is unlimited."
EXTRA_STRIKE = ["all hands", "it is imperative", "at all times", "every effort", "and/or", "in a timely manner", "as soon as possible", "utilize", "is responsible for ensuring", "the utmost importance"]
# Phrases from references/exemplar.md and voice.md. A draft that carries one took its content from the example.
LIFTED = [
    "COMPANY ARMORY DRAW AND TURN IN PROCEDURES",
    "the count on the armory board equal to the count in the consolidated memorandum receipt",
    "one platoon at the window at a time",
    "No weapon is drawn for cleaning after 1700",
    "a lost card is reported in writing to the executive officer within one working day",
    "inventory the serialized gear in their platoon on the last training day of each month",
    "reconciles the three platoon counts against the consolidated memorandum receipt",
    "Discrepancies of one item or more are reported to the executive officer the same day",
    "canceled when the fiscal year inventory is complete",
]


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else None


def majors(body):
    """[(number, title, block_text)] for lines that open a major paragraph: '3. Execution' or '1. Situation. text'."""
    out = []
    lines = body.split("\n")
    idx = [i for i, ln in enumerate(lines) if re.match(r"^\d{1,2}\.\s+\S", ln)]
    for k, i in enumerate(idx):
        m = re.match(r"^(\d{1,2})\.\s+(.+)$", lines[i])
        title = re.split(r"\.(?:\s|$)", m.group(2), 1)[0].strip()
        end = idx[k + 1] if k + 1 < len(idx) else len(lines)
        out.append((int(m.group(1)), title, "\n".join(lines[i:end])))
    return out


def sub_titles(block, level):
    """Titles at one level inside a major block: level 'a' -> 'a. Title', level '1' -> '(1) Title'."""
    pat = r"^\s*([a-z])\.\s+(.+)$" if level == "a" else r"^\s*\((\d+)\)\s+(.+)$"
    found = []
    for ln in block.split("\n")[1:]:
        m = re.match(pat, ln)
        if m:
            found.append((m.group(1), re.split(r"\.(?:\s|$)", m.group(2), 1)[0].strip()))
    return found


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8").read()
    text = re.sub(r"[ \t]+", " ", raw)
    fails, warns = [], []
    head = text.split("\n## ", 1)[0]
    letter = section(text, "Letterhead page") or ""
    body = section(text, "Body") or ""
    sig = section(text, "Signature page") or ""
    review = section(text, "Review")

    if not re.search(r"^# Directive\s*$", text, re.M):
        fails.append("title line '# Directive' missing")
    tm = re.search(r"Type:\s*([A-Za-z ]+?)(?=\s{2,}|\s+\w+:|\n|$)", head)
    dtype = tm.group(1).strip() if tm else ""
    if dtype.lower() not in ("order", "bulletin"):
        fails.append(f"Type: '{dtype or 'none'}'; MCO 5215.1K issues directives as an Order or a Bulletin only (basic order 4a(1)(b)1, chapter 1 paragraph 3). A standing procedure that is a permanent reference is an order; a letter of instruction is outside the program (paragraph 4i)")
        # check the rest as whatever the designation line says it is
        dtype = "Bulletin" if re.search(r"\bBULLETIN\b", letter) and not re.search(r"\bORDER\b", letter) else "Order" if re.search(r"\bORDER\b", letter) else ""
        shown = f"{tm.group(1).strip() if tm else 'no type'} (checked as {dtype or 'nothing'})"
    else:
        dtype = dtype.capitalize()
        shown = dtype
    em = re.search(r"Echelon:\s*([A-Za-z ]+?)(?=\s{2,}|\s+\w+:|\n|$)", head)
    echelon = em.group(1).strip().lower() if em else ""
    if not em:
        warns.append("no 'Echelon:' in the header; chapter 1 paragraph 5c turns on whether the command is below battalion or squadron")
    detached = re.search(r"separately detached|inspector-instructor", head, re.I)

    # identification block
    ident = re.search(r"Identification:\s*(\S.*?)(?=\s{2,}|\s+Sponsor|\n|$)", head)
    idn = ident.group(1).strip() if ident else ""
    if not idn:
        fails.append("no 'Identification:' line (abbreviated directive type, SSIC, point number; chapter 1 paragraph 21a)")
    else:
        if dtype == "Order":
            om = re.search(r"\b\d{4,5}R?\.(\d+)([A-Z]?)\b", idn)
            if not om:
                fails.append(f"order identification '{idn}' lacks the SSIC and consecutive point number (paragraph 21c, 21d); an order is 'SSIC.point', a bulletin carries no point")
            elif om.group(2) in ("I", "O", "Q"):
                fails.append(f"revision suffix '{om.group(2)}' in '{idn}'; paragraph 21e(1): do not use the letters I, O, and Q")
        if dtype == "Bulletin":
            if re.search(r"\b\d{4,5}R?\.\d", idn):
                fails.append(f"bulletin identification '{idn}' carries a consecutive point number; paragraph 21d(4): bulletins are identified by their SSIC and the date issued")
            elif not re.search(r"\b\d{4,5}R?\b", idn):
                fails.append(f"bulletin identification '{idn}' has no four or five digit SSIC (paragraph 21c)")
    dm = re.search(r"Date signed:\s*(.+?)(?=\s{2,}|\n|$)", head)
    if dm and not re.fullmatch(SIGNED_DATE, dm.group(1).strip()):
        fails.append(f"date signed '{dm.group(1).strip()}' is not day-month-year with the three letter month, or '(Date Signed)' (paragraph 21a)")
    signed_date = None
    if dm:
        sd = re.search(r"\b(\d{1,2}) (" + MONTHS + r") (\d{4}|\d{2})\b", dm.group(1))
        if sd:
            y = int(sd.group(3)); y = y + 2000 if y < 100 else y
            signed_date = (y, MONTH_NUM[sd.group(2)])

    # cancellation line: required for a bulletin, wrong on an order
    canc = re.search(CANC, head + "\n" + letter)
    frp = bool(re.search(r"Canc frp:", head + "\n" + letter))
    if dtype == "Bulletin":
        if not canc:
            fails.append("bulletin without its cancellation line ('Canc: Mon YYYY' or 'Canc frp: Mon YYYY' above the SSIC); chapter 1 paragraph 3c: a bulletin must have a self-canceling provision; chapter 3 paragraph 2")
        elif signed_date:
            cy, cm = int(canc.group(2)), MONTH_NUM[canc.group(1)]
            months = (cy - signed_date[0]) * 12 + (cm - signed_date[1])
            if months > 12:
                fails.append(f"bulletin cancels {months} months after signature; chapter 1 paragraph 3c: up to 12 months, but no longer. A requirement that must last longer is an order")
            elif months < 0:
                fails.append("bulletin cancellation date is before the date signed")
    if dtype == "Order" and canc:
        fails.append("an order carries a cancellation date; an order is continuing authority meant as a permanent reference (chapter 1 paragraph 3b). If this is one time or brief term, it is a bulletin")

    # letterhead lines
    if not letter:
        fails.append("no '## Letterhead page' section")
    else:
        desig = [ln.strip() for ln in letter.split("\n") if re.search(r"\b(ORDER|BULLETIN)\b", ln) and not ln.strip().startswith("Subj") and ln.strip() == ln.strip().upper() and re.search(r"[A-Z]{4}", ln)]
        if not desig:
            fails.append("no designation line in all capital letters (e.g. 'BATTALION ORDER 3500.1'; chapter 2 paragraph 2b, figure 2-2)")
        else:
            d = desig[0]
            if dtype == "Order" and "BULLETIN" in d and "ORDER" not in d:
                fails.append(f"Type is Order but the designation line reads '{d}'")
            if dtype == "Bulletin" and "ORDER" in d and "BULLETIN" not in d:
                fails.append(f"Type is Bulletin but the designation line reads '{d}'")
        if not re.search(r"^From:\s*\S", letter, re.M):
            fails.append("no 'From:' line with the principal official's title (paragraph 23a)")
        if not re.search(r"^To:\s*Distribution List\s*$", letter, re.M):
            fails.append("'To:' line must read 'Distribution List' (paragraph 23b)")
        sm = re.search(r"^Subj:\s*(.+)$", letter, re.M)
        if not sm:
            fails.append("no 'Subj:' line (paragraph 23c)")
        elif re.search(r"[a-z]", sm.group(1)):
            fails.append("'Subj:' line must be in all capital letters (paragraph 23c(1))")
        if DIST_A.split(":")[0] not in text:
            fails.append("no distribution statement; chapter 2 paragraph 2h and chapter 3 paragraph 10: show it at the bottom of the letterhead page (paragraph 19 lists A through X)")
        else:
            am = re.search(r"DISTRIBUTION STATEMENT A:\s*(.+)", text)
            if am and am.group(1).strip() != DIST_A.split(": ", 1)[1]:
                fails.append(f"distribution statement A altered: '{am.group(1).strip()}'; paragraph 19 prescribes '{DIST_A}'")

    # references and enclosures, listed against cited
    ref_lines = re.findall(r"^\s*(?:Ref:)?\s*\(([a-z]{1,2})\)\s+(.+)$", letter, re.M)
    listed = [r[0] for r in ref_lines]
    if listed:
        cited = set(re.findall(r"\breferences? \(([a-z]{1,2})\)", body, re.I)) | set(re.findall(r"(?:references?|and|,) \(([a-z]{1,2})\)", body, re.I))
        cited |= set(m for pair in re.findall(r"references? \(([a-z]{1,2})\) (?:and|through) \(([a-z]{1,2})\)", body, re.I) for m in pair)
        for r in listed:
            if r not in cited and not (len(listed) == 1 and re.search(r"\bthe reference\b", body)):
                fails.append(f"reference ({r}) is listed and never cited; paragraph 24b: all references must be used in the text")
        for r in sorted(cited):
            if r not in listed:
                fails.append(f"reference ({r}) is cited in the text and not listed under Ref: (paragraph 24)")
        for r, title in ref_lines:
            if re.search(r"Bul\b|MARADMIN", title) and not re.search(r"\(canc:", title, re.I):
                warns.append(f"reference ({r}) is a bulletin or MARADMIN without its cancellation date '(canc: Mon YY)' (paragraph 24e)")
    elif re.search(r"\breferences? \([a-z]\)", body, re.I):
        fails.append("the text cites a reference and the letterhead lists none (paragraph 24)")
    encl_block = re.search(r"^Encl:(.*?)(?=^\S|\Z)", letter, re.M | re.S)
    encl_listed = re.findall(r"\((\d+)\)", encl_block.group(1)) if encl_block else []
    encl_cited = set(re.findall(r"\benclosures? \((\d+)\)", body, re.I)) | set(re.findall(r"(?:enclosures?|and|,) \((\d+)\)", body, re.I))
    for e in encl_listed:
        if e not in encl_cited:
            fails.append(f"enclosure ({e}) is listed and never cited (paragraph 26d: listed in the sequence they first appear in the text)")
    for e in sorted(encl_cited):
        if e not in encl_listed:
            fails.append(f"enclosure ({e}) is cited and not listed under Encl: (paragraph 26)")
    if encl_block and re.search(r"\b(?:MCO|MCBul|MARADMIN|SECNAV|OPNAV|DoD)\b", encl_block.group(1)):
        fails.append("a higher authority's directive is enclosed; chapter 1 paragraph 5a: supplemental directives shall not enclose the higher authority's directive")
    sup = re.search(r"Supplements:\s*(.+?)(?=\s{2,}|\n|$)", head)
    if sup and sup.group(1).strip().lower() not in ("none", "no", "n/a", "") and not re.search(r"^Ref:", letter, re.M):
        fails.append(f"a supplement to '{sup.group(1).strip()}' with no Ref: section; paragraph 5b: the supplemental directive must incorporate by reference the higher authority's directive")

    # echelon and barred subjects
    sj = re.search(r"^Subj:\s*(.+)$", letter, re.M)
    subj = sj.group(1) if sj else ""
    M = majors(body)
    first_para = M[0][2] if M else ""
    if echelon and re.search(BELOW_BN, echelon) and not detached:
        hit = re.search(BARRED, subj + " " + first_para, re.I)
        if hit:
            fails.append(f"'{hit.group(0)}' at {echelon} level; chapter 1 paragraph 5c: do not issue supplements below the battalion or squadron level on leave and liberty, assumption of command, alcoholic beverage control, mail handling, or command security procedures (exception: separately detached commands or Inspectors-Instructors)")

    # the paragraphs
    titles = [t for _, t, _ in M]
    nums = [n for n, _, _ in M]
    if not body or not M:
        fails.append("no '## Body' with numbered major paragraphs")
    else:
        if nums != list(range(1, len(nums) + 1)):
            fails.append(f"major paragraphs numbered {nums}; number consecutively from 1 (paragraph 32b, 33)")
        for n, t, _ in M:
            if not t or not re.search(r"[A-Za-z]", t):
                fails.append(f"paragraph {n} has no title; paragraph 32c: include a title for all major paragraphs")
        for n, t, blk in M:
            a = sub_titles(blk, "a")
            if len(a) == 1:
                fails.append(f"paragraph {n} '{t}' has one lettered subparagraph; paragraph 32h: when a paragraph is subdivided, it must have at least two subdivisions")
            p = sub_titles(blk, "1")
            if len(p) == 1:
                fails.append(f"paragraph {n} '{t}' has one numbered subparagraph '(1)'; paragraph 32h and 33: a(1) must have a (2)")
        if dtype == "Order":
            has_canc = "Cancellation" in titles
            want = ORDER_SEQ if has_canc else [x for x in ORDER_SEQ if x != "Cancellation"]
            if titles[0] != "Situation":
                fails.append(f"first paragraph is '{titles[0]}'; chapter 2 paragraph 3a: Situation must be the first paragraph of the directive" + (" (Purpose opens a bulletin, not an order)" if titles[0] == "Purpose" else ""))
            for w in want:
                if w not in titles:
                    fails.append(f"mandatory paragraph '{w}' missing (chapter 2 paragraphs 3 to 5; figure 2-2)")
            if has_canc:
                if titles.index("Cancellation") != 1:
                    fails.append("Cancellation is not the second paragraph; chapter 2 paragraph 3b: always the second paragraph, if needed")
                if "Mission" in titles and titles.index("Mission") != 2:
                    fails.append("with a Cancellation paragraph, Mission is paragraph 3 (chapter 2 paragraph 3c)")
                if len(M) != 6 and all(w in titles for w in want):
                    fails.append(f"{len(M)} paragraphs; with Cancellation and Mission both used the directive has 6 (chapter 2 paragraph 3c)")
            else:
                if "Mission" in titles and titles.index("Mission") != 1:
                    fails.append("Mission is not paragraph 2; without a Cancellation paragraph the five paragraphs are Situation, Mission, Execution, Administration and Logistics, Command and Signal")
                if all(w in titles for w in want) and [t for t in titles if t in want] != want:
                    fails.append(f"paragraph order {titles}; the order is {want}")
                if re.search(r"\b(?:cancel\w*|supersed\w*)\s+(?:[A-Za-z0-9/]+O|[A-Za-z]*Bul|MCO)\s+\d{4}", body, re.I):
                    fails.append("the text cancels a directive and there is no Cancellation paragraph; chapter 2 paragraph 3c: a cancellation paragraph is required when canceling other directives")
            if "Execution" in titles:
                blk = M[titles.index("Execution")][2]
                a_titles = [t for _, t in sub_titles(blk, "a")]
                for s in EXEC_SUBS:
                    if not any(t.startswith(s) for t in a_titles):
                        fails.append(f"Execution lacks subparagraph '{s}' (chapter 2 paragraph 3d; figure 2-2 paragraph 3)")
                p_titles = [t for _, t in sub_titles(blk, "1")]
                for s in ("Commander's Intent", "Concept of Operations"):
                    if not any(t.startswith(s) and not t.startswith("Commander's Intent and") for t in p_titles):
                        fails.append(f"Execution paragraph a lacks '({'1' if s.startswith('Comm') else '2'}) {s}' (chapter 2 paragraph 3d(1); figure 2-2)")
            if "Command and Signal" in titles:
                blk = M[titles.index("Command and Signal")][2]
                cmd = re.search(r"^\s*a\.\s+Command\.\s*(.+)$", blk, re.M)
                sgn = re.search(r"^\s*b\.\s+Signal\.\s*(.+)$", blk, re.M)
                if not cmd:
                    fails.append("Command and Signal lacks 'a. Command.' with the applicability statement (chapter 2 paragraph 5a)")
                elif not re.search(r"\b(?:is|are) (?:not )?applicable to\b", cmd.group(1)):
                    fails.append(f"Command subparagraph does not state applicability ('This Order is applicable to ...'); chapter 2 paragraph 5a; figure 2-2 'Reserve applicability'")
                if not sgn:
                    fails.append("Command and Signal lacks 'b. Signal.' (chapter 2 paragraph 5b)")
                elif not re.fullmatch(r"This (?:Order|Directive) is effective the date signed\.?", sgn.group(1).strip()):
                    fails.append(f"Signal altered: '{sgn.group(1).strip()}'; chapter 2 paragraph 5b prescribes 'This Order is effective the date signed.'")
            if "Cancellation" in titles:
                cblk = M[titles.index("Cancellation")][2]
                if re.search(r"\bMCO\b|MCBul|MARADMIN", cblk) and not re.search(r"\bHQMC\b", echelon):
                    fails.append("the Cancellation paragraph cancels a Headquarters directive; chapter 2 paragraph 3b: only cancel directives you sponsor")
                for b in re.findall(r"[A-Za-z]*Bul \d{4,5}[^\n]*", cblk):
                    if not re.search(r"\bof \d{1,2} (?:" + MONTHS + r")\w* \d{2,4}|\d{1,2} (?:" + MONTHS + r")\w* \d{4}", b):
                        fails.append(f"'{b.strip()}' canceled without the date of the basic bulletin (chapter 2 paragraph 3b)")
        if dtype == "Bulletin":
            if titles[0] != "Purpose":
                fails.append(f"first paragraph is '{titles[0]}'; chapter 3 paragraph 11a: Purpose is always first" + (" (Situation opens an order, not a bulletin)" if titles[0] == "Situation" else ""))
            if any(t in titles for t in ("Situation", "Mission", "Execution", "Command and Signal")):
                fails.append("bulletin written in the five paragraph order format; chapter 1 paragraph 3c: bulletins are written in the format of chapter 3 (Purpose, Cancellation, Background, Action, Reserve Applicability, Cancellation Contingency)")
            if "Cancellation" in titles and titles.index("Cancellation") != 1:
                fails.append("Cancellation is not the second paragraph (chapter 3 paragraph 11b)")
            ra = [i for i, t in enumerate(titles) if t == "Reserve Applicability"]
            if not ra:
                fails.append("no 'Reserve Applicability' paragraph; chapter 3 paragraph 11e: the applicability statement ('This Bulletin is applicable to ...'); figures 3-1 and 3-2")
            elif not re.search(r"\b(?:is|are) (?:not )?applicable to\b", M[ra[0]][2]):
                fails.append("Reserve Applicability paragraph does not state applicability (chapter 3 paragraph 11e)")
            if frp:
                if titles[-1] != "Cancellation Contingency":
                    fails.append("'Canc frp:' without a 'Cancellation Contingency' last paragraph; chapter 3 paragraph 2b and 11f")
                elif canc and re.search(canc.group(1) + r"\w*\s+" + canc.group(2), M[-1][2]):
                    fails.append("the Cancellation Contingency paragraph repeats the cancellation date; chapter 3 paragraph 11f: state the contingency, but do not repeat the cancellation date")
            elif "Cancellation Contingency" in titles:
                fails.append("a 'Cancellation Contingency' paragraph with 'Canc:' rather than 'Canc frp:'; chapter 3 paragraph 2b and 2c")
            if "Cancellation" in titles:
                cblk = M[titles.index("Cancellation")][2]
                if re.search(r"\bMCO\b|MCBul|MARADMIN", cblk) and not re.search(r"\bHQMC\b", echelon):
                    fails.append("the Cancellation paragraph cancels a Headquarters directive; chapter 3 paragraph 11b: only cancel directives you sponsor")

        # language
        if re.search(r"\bI (?=[a-z])|\bme\b", body) and not re.search(r"ASSUMPTION OF COMMAND", subj):
            fails.append("personal pronoun 'I' or 'me' in the text; chapter 1 paragraph 15b")
        for w in strike_hits(body) + [w for w in EXTRA_STRIKE if w in body.lower()]:
            warns.append(f"strike list: '{w}'")
        if re.search(r"\betc\.", body):
            warns.append("'etc.' in a tasking; name the items or the deciding billet")

    # signature page
    if not sig:
        fails.append("no '## Signature page' section (chapter 1 paragraph 37)")
    else:
        if "<SIGNER" not in sig:
            fails.append("signature block does not carry <SIGNER_CAPS>; the label stays until substitution on the user's computer, and the order wants the name in capitals (paragraph 37a)")
        if re.search(RANKS, sig):
            fails.append(f"grade or rank in the signature block ('{re.search(RANKS, sig).group(0)}'); paragraph 37a: do not use the signer's grade or rank")
        frm = re.search(r"^From:\s*(.+)$", letter, re.M)
        if frm and re.search(r"^\s*" + re.escape(frm.group(1).strip()) + r"\s*$", sig, re.M | re.I) and not re.search(r"by direction|acting", sig, re.I):
            fails.append(f"'{frm.group(1).strip()}' under the signer's name; paragraph 37a(1): do not show the title of the principal officer named in the From: line")
        sb = re.search(r"Signed by:\s*(.+?)(?=\s{2,}|\n|$)", head)
        if sb:
            who = sb.group(1).lower()
            if "by direction" in who and not re.search(r"By direction", sig):
                fails.append("header says the signer is by direction and the signature block does not say 'By direction' (chapter 1 paragraph 7)")
            if "acting" in who and not re.search(r"^\s*Acting\s*$", sig, re.M):
                fails.append("header says the signer is acting and the signature block has no 'Acting' line (paragraph 37a(3))")
            if "by title" in who and len([ln for ln in sig.split("\n") if ln.strip() and not ln.strip().startswith(("DISTRIBUTION", "Copy to", "<SIGNER"))]) == 0:
                fails.append("header says the signer signs by title and the signature block shows no title (paragraph 37a(2))")
        else:
            warns.append("no 'Signed by:' in the header; say whether the principal official, a delegate by title, a further delegate by direction, or someone acting signs (chapter 1 paragraph 7)")
        if "DISTRIBUTION:" not in sig:
            warns.append("no 'DISTRIBUTION:' section on the signature page (paragraph 37b)")

    if review is None:
        warns.append("no '## Review' section; the order imposes an annual review recorded on NAVMC 10974 or a tracking system, revision at 9 years, and a review within 1 year of a new commander (basic order 4b(2)(d); chapter 1 paragraphs 13 and 14)")
    elif not re.search(r"NAVMC 10974|tracking system", review):
        warns.append("Review section does not say where the annual review is recorded (NAVMC 10974 or an automated tracking system, chapter 1 paragraph 14c)")

    # names, blocked content about a person, lifted phrases, dashes
    scrub = re.sub(r"<[A-Z_']+>", "", text)
    mm = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]{2,}\b", scrub)
    if mm and not re.fullmatch(GRADES + r" " + TITLE_WORDS, mm.group(0)):
        fails.append(f"a name appears ('{mm.group(0)}'); a directive states the rule and carries no Marine's name")
    nm = re.search(r"^\s*([A-Z]\. (?:[A-Z]\. )?[A-Z]{3,})\s*$", sig, re.M)
    if nm:
        fails.append(f"a name in the signature block ('{nm.group(1)}'); <SIGNER_CAPS> until substitution on the user's computer")
    for b in blocked_hits(text, allow=("medical", "family or personal", "substance", "SAPR or investigation", "financial")):
        fails.append(f"blocked content: {b}; no identifier belongs in a directive")
    for sent in re.split(r"(?<=[.;])\s+", body):
        if re.search(r"<MARINE>|" + GRADES + r"\s+[A-Z][a-z]{2,}", sent):
            for b in blocked_hits(sent, allow=("SSN pattern", "EDIPI or ten digit id")):
                fails.append(f"blocked content about a person: {b}; a directive states the rule, a record entry states the case")
    for p in LIFTED:
        if p.lower() in text.lower():
            fails.append(f"lifted from the exemplar or voice file: '{p}'; the example teaches shape, the intake supplies facts")
    if dashes(text):
        fails.append("em or en dash present")

    print(f"DIRECTIVE CHECK: {sys.argv[1]}  {shown}  {len(M) if body else 0} major paragraphs")
    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    if not warns and not fails:
        print("  clean")
    print(f"  -> {len(fails)} failures, {len(warns)} warnings")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
