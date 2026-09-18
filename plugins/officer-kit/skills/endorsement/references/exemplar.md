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

## Strong: a battalion's second endorsement recommends disapproval, so 9-2.5 makes it significant (spec.json)

```json
{
  "ssic": "1050", "originator_code": "2d Bn", "date": "2026-10-16",
  "endorsement": {"ordinal": "SECOND", "on": "Cpl <MARINE> ltr 1050 of 9 Oct 26"},
  "from": "Commanding Officer, 2d Battalion",
  "to": "Commanding Officer, 2d Marine Regiment",
  "subj": "REQUEST FOR SPECIAL LIBERTY",
  "encls": ["Battalion training schedule for the week of 12 October 2026"],
  "encls_start": "2",
  "copy_to": ["Corporal <MARINE>", "Commanding Officer, Company C"],
  "paragraphs": [
    {"text": "Forwarded, recommending disapproval.  Enclosure (2) puts the battalion command post exercise on the two days requested, and the Marine is one of two qualified radio operators in the section; the second operator is on leave until 22 October 2026."},
    {"text": "A request for 24 through 26 October 2026 would be supported."}
  ],
  "signature": "F. M. LAST"
}
```

Annotation. The action is "forwarded, recommending disapproval", which 9-2.5 lists as significant, so the endorsement carries a copy to block, and the block carries the originator of the basic letter and the activity that endorsed before this one. The enclosure is numbered (2), continuing the basic letter's (1) under 9-2.4, and the paragraph cites it as enclosure (2). The ordinal is SECOND because this is the second endorsement added to the basic letter (9-2.1.b), not because the battalion is the second echelon. Two paragraphs: the disapproval with the fact behind it, and the alternative the requester can act on. `build_letter.py` prints no copy to block and starts an Encl block at (1), so both are corrected on the page before signature; `endorsement_check.py` says so in its output.

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

```
1.  Forwarded, recommending disapproval.  [and no Copy to: block anywhere on the page]
```
[9-2.5 makes a recommendation of disapproval significant, and a significant endorsement carries the originator of the basic letter, each activity that endorsed before, and all earlier copy to addressees in a copy to block. The Marine who wrote the request learns from the block that the request was opposed on the way up.]

```
Encl:  (1) Battalion training schedule
```
[The basic letter already had an enclosure (1). Under 9-2.4 the endorsement's addition continues the sequence and is (2).]
