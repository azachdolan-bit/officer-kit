#!/usr/bin/env python3
"""Check a DEOCS command climate action plan (deocs_plan.md) against MARADMIN 306/25 and MCO 5354.1G w/Admin Ch 1
enclosure (2) chapter 9.

Usage:  python3 deocs_plan_check.py deocs_plan.md
Exit 0 = passes (warnings allowed); 1 = an action with no owner, date, or measure; a finding with no action; a
survey date outside the window the MARADMIN states or a change of command CCA outside the order's 90 days; an out
brief or plan due date missing or before the survey close; an individual identified; a claim about the outcome;
a name; a lifted exemplar phrase; blocked content; or a dash.

Timeline note. The MARADMIN states the annual window (1 August to 30 November) and the latest start (31 October)
as calendar dates, and the order states 90 days for a change of command CCA and 30 days for the command team brief.
Neither states an out brief or action plan deadline in days, so for those two dates this script checks presence
and ordering only and says so.
"""
import os
import re
import sys
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_checks import strike_hits, blocked_hits, dashes, words  # noqa: E402

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE = r"\b\d{1,2} (?:" + MONTHS + r") \d{4}\b"
GRADES = r"(?:Private|Lance Corporal|Corporal|Sergeant|Staff Sergeant|Gunnery Sergeant|Master Sergeant|First Sergeant|Master Gunnery Sergeant|Sergeant Major|Second Lieutenant|First Lieutenant|Captain|Major|Lieutenant Colonel|Colonel|PFC|LCpl|Cpl|Sgt|SSgt|GySgt|MSgt|1stSgt|MGySgt|SgtMaj|2ndLt|1stLt|Capt|Maj|LtCol|Col)"
# A billet the plan may name as an owner. Anything else in Owner: is a warning; a name is a failure.
BILLETS = r"\b(?:commander|commanding officer|officer in charge|executive officer|sergeant major|first sergeant|chief of staff|deputy|company commander|platoon commander|platoon sergeant|S-?[1-9]|adjutant|logistics officer|operations officer|training officer|EOA|Equal Opportunity Advisor|Collateral Duty EOA|EOC|Equal Opportunity Coordinator|survey administrator|chaplain|SARC|SJA|IPP|IG|inspector general|career planner|family readiness officer|safety officer|medical officer|surgeon|SEA|senior enlisted advisor|gunner|master guns|battalion|squadron|regiment|company|OIC|SNCOIC|NCOIC|chief|officer|XO|CO|department head|section head|section leader|squad leader|advisor|coordinator|representative|specialist|manager|director|planner|master sergeant)\b"
# Words that point at one person or one respondent. The sources in the library set no minimum respondent count; the
# checker fails the language of identification, not a number.
IDENTIFY = r"\b(?:the (?:" + GRADES + r"|Marine|Sailor|civilian|respondent|person|one|individual) who (?:wrote|said|commented|answered|complained|reported|filed)|one respondent (?:said|wrote|stated|commented)|a respondent (?:said|wrote|stated|commented)|the (?:only|one|single|lone) (?:\w+ ){0,2}(?:" + GRADES + r"|female|male|woman|man|Marine|Sailor|civilian|officer|SNCO|NCO) (?:in|on|at|who|from)|the (?:Marine|Sailor|respondent|person|individual) (?:in|from|behind) finding \d+|was clearly describing|is clearly describing|everyone knows who|we know who|the complainant|the victim)\b"
PROMISE = r"\b(?:(?:is|are|has been|have been|will be|gets|got) fixed|will (?:improve|get better|be better|be higher|go up|rise|increase|eliminate|resolve|solve|restore|raise)|guarantee\w*|no longer (?:a|an) (?:problem|issue|concern)|is (?:fixed|solved|resolved)|has improved|will show improvement|fixes the climate|fix the climate)\b"
EXTRA_STRIKE = ["toxic", "morale problem", "culture problem", "the marines feel", "clearly", "obviously", "root cause", "zero tolerance", "reinforce", "emphasize", "re-emphasize", "continue to"]
# The order itself describes the DEOCS with these words (Appendix B definition 24; chapter 9). A finding may quote a
# report item that carries them; the kit's other blocked content still fails.
ALLOW_IN_FINDINGS = [r"sexual assault response and prevention", r"sexual assault", r"sexual harassment", r"harassment"]
# Phrases from references/exemplar.md and voice.md. A draft that carries one took its content from the example.
LIFTED = [
    "412 invited, 338 responded", "58 percent favorable; the report's comparison figure for the same item is 71",
    "14 of 19 short answer comments name the same subject", "two duty day blocks per company set aside for completion",
    "run one focus group per company with the servicing EOA on the Cohesion item",
    "publish the barracks work order log with open and closed counts",
    "61 percent favorable against a comparison group of 74", "publish the awards board schedule and results by company",
    "awards board results posted for 6 of 6 months",
]

WINDOW_START = (8, 1)    # 1 August, MARADMIN 306/25 paragraph 1; MCO chapter 9 paragraph 6
WINDOW_END = (11, 30)    # 30 November
LATEST_START = (10, 31)  # administration must commence no later than 31 October, MARADMIN paragraph 1
COC_DAYS = 90            # change of command CCA within 90 days after assumption of command, MCO chapter 9 paragraph 5


def parse(s):
    for fmt in ("%d %B %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            pass
    return None


FIELDS = r"(?:Unit|Survey|Opened|Closed|Out brief|Plan due|Commander|Survey administrator|Assumed command|References)"


def fmt(d):
    return f"{d.day} {d:%B %Y}"


def field(head, name):
    m = re.search(r"(?:^|\s)" + name + r":\s*(.+?)(?=\s+" + FIELDS + r":|\n|$)", head)
    return m.group(1).strip() if m else None


def section(text, name):
    m = re.search(r"^## " + name + r"\s*\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else None


def numbered(block):
    """Return {number: text} for lines that start '1.' '2.' '4a.' etc. Continuation lines attach to the item above."""
    items, cur = {}, None
    for line in (block or "").splitlines():
        m = re.match(r"^\s*(\d+[a-z]?)\.\s+(.*)", line)
        if m:
            cur = m.group(1)
            items[cur] = m.group(2)
        elif cur and line.strip():
            items[cur] += " " + line.strip()
    return items


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8").read()
    text = re.sub(r"[ \t]+", " ", raw)
    fails, warns, notes = [], [], []
    head = text.split("\n## ", 1)[0]

    if not re.search(r"^# DEOCS command climate action plan", text, re.M):
        fails.append("title line '# DEOCS command climate action plan' missing")

    # header fields
    unit = field(head, "Unit")
    if not unit:
        fails.append("no 'Unit:' line in the header; the unit by echelon")
    elif not re.search(r"\bunder\b", unit, re.I):
        warns.append("Unit: does not say what it is under; the plan goes up an echelon, name it")
    survey = field(head, "Survey") or ""
    kind = "annual" if re.search(r"annual", survey, re.I) else ("coc" if re.search(r"change of command", survey, re.I) else None)
    if not kind:
        fails.append("Survey: must say 'annual DEOCS' or 'change of command CCA' (MCO 5354.1G chapter 9 paragraphs 5 and 6)")
    cmdr = field(head, "Commander")
    if not cmdr:
        fails.append("no 'Commander:' line; the commander by billet")
    elif not re.search(BILLETS, cmdr, re.I) or re.search(GRADES + r"\s+[A-Z][a-z]{2,}", cmdr):
        fails.append(f"Commander: '{cmdr}' is not a billet; the plan carries billets, never names")
    admin = field(head, "Survey administrator")
    if not admin:
        fails.append("no 'Survey administrator:' line; the EOA, Collateral Duty EOA, or EOC by billet (MARADMIN 306/25 paragraph 3)")
    else:
        if not re.search(r"EOA|Equal Opportunity Advisor|EOC|Equal Opportunity Coordinator", admin):
            fails.append(f"Survey administrator: '{admin}'; MARADMIN 306/25 paragraph 3 names the EOA, Collateral Duty EOA, or Equal Opportunity Coordinator")
        if re.search(r"\bEOR\b|Equal Opportunity Representative", admin):
            warns.append("the order removed the Equal Opportunity Representative (Appendix C paragraph 1.f); the billet is the EOC (chapter 1 paragraph 8)")
        if not re.search(r"Prev 004", admin):
            warns.append("say whether the administrator completed JKO Prev 004 before administering (MARADMIN 306/25 paragraph 3)")

    def hdate(name, required=True):
        v = field(head, name)
        if not v:
            if required:
                fails.append(f"no '{name}:' date in the header")
            return None
        d = parse(v)
        if not d:
            fails.append(f"{name}: '{v}' is not a date as day month year")
        return d

    opened = hdate("Opened", required=False)
    closed = hdate("Closed")
    outbrief = hdate("Out brief")
    due = hdate("Plan due")
    assumed = hdate("Assumed command", required=False)

    # the timeline the sources state
    if closed and kind == "annual":
        ws = date(closed.year, *WINDOW_START); we = date(closed.year, *WINDOW_END)
        if not (ws <= closed <= we):
            fails.append(f"Closed {fmt(closed)} is outside 1 August to 30 November {closed.year} (MARADMIN 306/25 paragraph 1; MCO chapter 9 paragraph 6; paragraph 8: extensions are not permitted)")
        if opened:
            ls = date(opened.year, *LATEST_START)
            if opened > ls:
                fails.append(f"Opened {fmt(opened)} is after 31 October; administration must commence no later than 31 October (MARADMIN 306/25 paragraph 1)")
            if opened < date(opened.year, *WINDOW_START):
                fails.append(f"Opened {fmt(opened)} is before 1 August (MARADMIN 306/25 paragraph 1)")
    if kind == "coc":
        if not assumed:
            fails.append("change of command CCA without an 'Assumed command:' date; the order counts 90 days from assumption (chapter 9 paragraph 5)")
        elif closed:
            limit = assumed + timedelta(days=COC_DAYS)
            if closed > limit:
                fails.append(f"Closed {fmt(closed)} is more than 90 days after assumption of command {fmt(assumed)} (limit {fmt(limit)}; MCO chapter 9 paragraph 5)")
            if closed < assumed:
                fails.append("Closed precedes Assumed command")
    if opened and closed and opened > closed:
        fails.append("Opened is after Closed")
    for name, d in (("Out brief", outbrief), ("Plan due", due)):
        if d and closed and d < closed:
            fails.append(f"{name} {fmt(d)} precedes the survey close {fmt(closed)}; there is no result to brief or plan on before the close")
    if outbrief and due and due < outbrief:
        warns.append("Plan due precedes Out brief; a plan written before the commander is briefed")
    notes.append("out brief and plan due: presence and ordering checked only; neither MARADMIN 306/25 nor MCO 5354.1G states a deadline in days for them (they defer to DoDI 6400.11, not in the library)")

    # findings and actions
    fnd = section(text, "Findings")
    act = section(text, "Actions")
    if fnd is None:
        fails.append("no '## Findings' section")
    if act is None:
        fails.append("no '## Actions' section")
    fitems = numbered(fnd)
    aitems = numbered(act)
    if fnd is not None and not fitems:
        fails.append("## Findings has no numbered finding")
    for n, f in fitems.items():
        if not re.search(r"report section", f, re.I):
            fails.append(f"finding {n} does not name the report section ('Report section ...'); the finding is what the report says, where")
        if not re.search(r"\d", f):
            warns.append(f"finding {n} carries no number from the report")
        if re.search(r"\bbecause\b|\bdue to\b|\bfeel(?:s)? that\b|\bmeans that\b", f, re.I):
            warns.append(f"finding {n} reads a cause into the report; the survey is a perception data point (chapter 9 paragraph 7), the reason is for the focus group")
        if re.search(r'"[^"]{25,}"', f):
            warns.append(f"finding {n} carries a quotation of 25 or more characters; a short answer comment goes on the plan as a theme with a count, not quoted")
    base = lambda k: re.match(r"\d+", k).group(0)
    covered = {base(k) for k in aitems}
    for n in fitems:
        if base(n) not in covered:
            fails.append(f"finding {n} has no action; one action per finding (chapter 9 paragraph 2: an action plan to directly address them)")
    for n in aitems:
        if base(n) not in {base(k) for k in fitems}:
            warns.append(f"action {n} answers no finding")
    for n, a in aitems.items():
        for part in ("Action", "Owner", "Date", "Measure"):
            if not re.search(r"\b" + part + r":", a):
                fails.append(f"action {n} has no '{part}:'")
        own = re.search(r"Owner:\s*(.+?)(?=\s+Date:|\s+Measure:|$)", a)
        if own:
            o = own.group(1).strip()
            if re.search(GRADES + r"\s+(?:[A-Z]\.\s*)?[A-Z][a-z]{2,}\b", o) and not re.search(r"^(?:Sergeant Major|First Sergeant)$", o):
                fails.append(f"action {n} owner '{o}' is a name; owners are billets")
            elif re.search(r"\ball hands\b|\beveryone\b|\bleadership\b$|\bTBD\b", o, re.I) or not re.search(BILLETS, o, re.I):
                fails.append(f"action {n} owner '{o}' is not a billet")
        dt = re.search(r"Date:\s*(.+?)(?=\s+Measure:|$)", a)
        if dt and not re.search(DATE, dt.group(1)):
            fails.append(f"action {n} date '{dt.group(1).strip()}' is not a day month year")
        ms = re.search(r"Measure:\s*(.+)$", a)
        if ms:
            m = ms.group(1)
            if words(m) < 4:
                fails.append(f"action {n} measure '{m.strip()}' is too short to be read off a document")
            if not re.search(r"compar|count|roster|on file|posted|entry|report|number|percent|\d", m, re.I):
                warns.append(f"action {n} measure names nothing that can be compared or counted")
        if re.search(PROMISE, a, re.I):
            fails.append(f"action {n} promises the outcome ('{re.search(PROMISE, a, re.I).group(0)}'); the measure names what will be compared, the next survey says what happened")

    # debrief and reporting
    deb = section(text, "Debrief")
    if deb is None or words(deb) < 8:
        fails.append("no '## Debrief' section with how and when the unit is told")
    else:
        if not re.search(DATE + r"|week of", deb):
            warns.append("Debrief carries no date")
    rep = section(text, "Reporting")
    if rep is None or words(rep) < 8:
        fails.append("no '## Reporting' section with to whom and by when")
    else:
        if not re.search(DATE, rep):
            warns.append("Reporting carries no date")
        if not re.search(r"reference \(am\)|6400\.11|not in the library|Overrides", rep):
            warns.append("Reporting does not say where its deadline and recipient came from; the publications in the library set none (chapter 9 paragraph 11 defers to reference (am))")
    if not re.search(r"^## Not in the library", text, re.M):
        warns.append("no '## Not in the library' section; DoDI 6400.11 governs the out brief and plan timeline and is not in the library")

    # the whole document
    body = text
    for m in sorted({m.group(0) for m in re.finditer(IDENTIFY, body, re.I)}):
        fails.append(f"an individual is identified ('{m}'); the plan names billets and counts, never a respondent or a complainant")
    if re.search(PROMISE, body, re.I):
        m = re.search(PROMISE, body, re.I).group(0)
        if not any(m.lower() in a.lower() for a in aitems.values()):
            fails.append(f"a claim about the outcome ('{m}'); the plan states actions and measures, not results")
    mm = re.search(GRADES + r"\s+(?:[A-Z]\.\s*){0,3}[A-Z][a-z]{2,}\b", re.sub(r"<MARINE>|<UNIT>", "", body))
    if mm and not re.search(r"^(?:Sergeant Major|First Sergeant|Master Gunnery Sergeant|Lieutenant Colonel|Staff Sergeant|Gunnery Sergeant|Master Sergeant|Lance Corporal|Corporal|Sergeant|Second Lieutenant|First Lieutenant) (?:Major|Sergeant|Colonel|Lieutenant|Corporal|Officer)$", mm.group(0)):
        fails.append(f"a name appears ('{mm.group(0)}'); billets only, <MARINE> if a Marine must be referred to")
    for p in LIFTED:
        if p.lower() in body.lower():
            fails.append(f"lifted from the exemplar or voice file: '{p}'; the example teaches shape, the report supplies facts")
    scrubbed = body
    for pat in ALLOW_IN_FINDINGS:
        scrubbed = re.sub(pat, "", scrubbed, flags=re.I)
    for b in blocked_hits(scrubbed):
        fails.append(f"blocked content: {b}; the plan carries the report's aggregate items, nothing about a person or a case")
    for w in strike_hits(body) + [w for w in EXTRA_STRIKE if re.search(r"\b" + re.escape(w) + r"\b", body.lower())]:
        warns.append(f"strike list: '{w}'")
    if dashes(body):
        fails.append("em or en dash present")

    print(f"DEOCS PLAN CHECK: {sys.argv[1]}  {survey or 'no survey type'}  {len(fitems)} findings, {len(aitems)} actions")
    for n in notes:
        print(f"  NOTE  {n}")
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
