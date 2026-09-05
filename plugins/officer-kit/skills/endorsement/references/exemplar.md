# Endorsement exemplars, fictional, annotated

Form only. Every number, date, code, and phrase here is invented and is not to be taken into a product; `endorsement_check.py` fails a draft that lifts a sentence from this file. Read this after the intake is done and the fact list is confirmed, never before, so it teaches shape and supplies no answers. The user's own signed endorsements in `Reference/Exemplars/endorsement/` beat this file.

## Strong: a company commander forwards a Marine's request with a recommendation and a reason (spec.json for build_letter.py)

```json
{
  "ssic": "1050", "originator_code": "B Co", "date": "2026-10-06",
  "endorsement": {"ordinal": "FIRST", "on": "Sgt <MARINE> ltr 1050 of 2 Oct 26"},
  "from": "Commanding Officer, Company B",
  "to": "Commanding Officer, 1st Battalion",
  "subj": "REQUEST FOR PERMISSIVE TEMPORARY ADDITIONAL DUTY",
  "paragraphs": [
    {"text": "Forwarded, recommending approval.  The request meets the conditions in the basic letter's reference (a); I verified the leave balance of 31 days on 5 October 2026, and the section's two other licensed operators cover the period requested."},
    {"text": "The Marine is the company's alternate armorer.  The armorer is present for the whole period, so no coverage action is required."}
  ],
  "signature": "F. M. LAST"
}
```

Annotation. The identification line names the basic letter the way the library's figures do: originator, "ltr", SSIC, and date. The Subj is the basic letter's, unchanged. The first sentence is the action; the rest is the reason the battalion commander can check (a balance verified on a date, the coverage stated as a count). No Ref or Encl block, because the endorsement adds neither. Two short paragraphs. The addressee knows in one reading what was done and why.

## Weak, annotated line by line

```
ENDORSEMENT
```
[No ordinal, and nothing after "on". The reader cannot tell which correspondence this rides on or where it sits in the chain. The checker fails the identification line.]

```
Subj:  PTAD REQUEST
```
[The endorsement changed the subject. The basic letter's Subj line is the one every endorsement repeats.]

```
1.  Strongly recommend approval.  Sergeant [a name] is an outstanding Marine and truly deserves this.
```
[Three strike words and a name. No fact the addressee can check: no balance, no coverage, no condition met.]

```
Ref:  (a) MCO 1050.3J
```
[The basic letter already lists this reference. An endorsement's Ref block is for what the endorsement adds.]

```
Respectfully request favorable consideration at your earliest convenience.
```
[Not one of the actions the figures use. The endorser forwards, recommends, concurs, certifies, or directs; the addressee decides the rest.]
