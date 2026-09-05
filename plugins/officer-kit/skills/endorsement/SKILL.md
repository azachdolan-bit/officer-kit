---
name: endorsement
description: >
  Drafts and builds an endorsement on correspondence moving up or down the chain, on the naval
  letter grid the kit already measures: the identification line (FIRST ENDORSEMENT on the
  originator's ltr, SSIC, code, and date), From, To, and Via, the basic letter's own Subj, a Ref
  or Encl block only for what the endorsement adds, and numbered paragraphs whose first sentence
  is the endorser's action (forwarded recommending approval or disapproval, concur, certify,
  direct, readdressed) with the reason the addressee can check. Built from the endorsements the
  library's own orders reproduce; the governing manual, SECNAV M-5216.5, is not in the library,
  so the tool is marked incomplete and names what it could not verify (later ordinals, same page
  endorsements, continued lettering, copy to). Use when the user says "endorse this request",
  "first endorsement on", "forward this recommending approval", "chop this up the chain", "the
  battalion needs my endorsement", or "readdress and forward".
metadata:
  version: "0.1.0"
  status: incomplete
---

# Endorsement

The addressee has the basic letter in hand and reads the endorsement for one thing: what did this endorser do with it, and why. The four endorsements reproduced in orders in the user's library agree on the layout (identification line, From, To, Via, the same Subj, numbered paragraphs, signature) and on the voice (first person: "I do not recommend", "I concur", "I certify", "I direct"). The tool asks for the basic correspondence's identifiers so the identification line is exact, asks what the endorser did and on what facts, writes the action in the first sentence and the reason after it, and builds the page on the kit's measured grid. It drafts; the endorser signs. **Incomplete:** SECNAV M-5216.5, the Department of the Navy Correspondence Manual, governs endorsements and is not in the library. What it alone settles (the ordinal sequence past FIRST, same page endorsements, how added references and enclosures are lettered against the basic letter's, the copy to block, returning without action) is listed in `references/standard.md` and marked unverified in any product that touches it. Nothing is filled from memory; `library` downloads the manual into Reference, and `Overrides/endorsement.md` records the command's practice until then.

## Read first

1. `references/standard.md`: the four figures from the library (MCO 1900.16 Figures 6-5 and L-10; NAVMC 4000.5D enclosure (12) pages 119 and 129), what they settle, what only the manual settles.
2. `references/intake.md`: the questions, one at a time.
3. `references/voice.md`: the actions in the figures' own words, the strike list.
4. `references/exemplar.md`: read only after the fact list is confirmed (step 5). It teaches shape and its content is not to be taken; the checker fails a lifted phrase.
5. `naval-letter/references/standard.md`: the grid, identity block, references and enclosures, and gates the endorsement inherits.

## Your own material (read first, every time)

1. `Overrides/endorsement.md`: how this command endorses (one line or reasons; same page or new page; letterhead or none; who signs by direction). The command's way wins; say in one line what it changed.
2. `Reference/Exemplars/endorsement/`: endorsements this command signed, sanitized. They beat the plugin's fictional exemplar.
3. Identity from the rules file's correspondence block: From line, originator code, signature form. Nothing guessed; a missing field is a placeholder the gate refuses.
4. `<MARINE>` in the body and in the identification line's originator where the originator is a Marine; the name goes on with `security-check/scripts/substitute.py` on the user's computer.
5. When an endorsement comes back changed, `aar` captures why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question. The basic letter's identifiers and the endorser's action are the questions this product turns on.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

## Workflow

```
Endorsement:
- [ ] 1. The basic correspondence: originator by billet, type, SSIC, code, date, and its Subj word for word; where this endorsement sits in the chain
- [ ] 2. The endorser's action (forward, recommend approval or disapproval, concur, certify, direct, return, readdress) and the facts it rests on, with dates and counts
- [ ] 3. Anything the endorsement adds (a reference or enclosure by exact title) and nothing it repeats
- [ ] 4. Routing: To, Via, who signs and how; identity from the rules file
- [ ] 5. Read back the fact list; the user confirms; nothing else goes in. Now read exemplar.md for shape
- [ ] 6. Write spec.json (below) with the endorsement block; mark any "Not in the library" item this endorsement touches as unverified in a note to the signer
- [ ] 7. python3 scripts/endorsement_check.py spec.json --basic-subj "<the basic Subj>" --basic-refs "<each basic ref>" exits 0
- [ ] 8. python3 ../naval-letter/scripts/build_letter.py spec.json "<name>.docx"; python3 ../naval-letter/scripts/qc_letter.py "<name>.docx" --kind endorsement exits 0
- [ ] 9. Rendered to PDF; python3 ../naval-letter/scripts/measure_pdf.py "<name>.pdf" exits 0; the page read as a picture
- [ ] 10. Saved to Correspondence/<subject> <ordinal> endorsement <date>.docx and .pdf; the basic letter and prior endorsements travel with it
- [ ] 11. Learning: what came back, via aar
```

## The product (spec.json for build_letter.py)

```json
{
  "ssic": "<the basic letter's SSIC>", "originator_code": "<from the rules file>", "date": "<ISO date>",
  "endorsement": {"ordinal": "FIRST", "on": "<originator by billet or label> ltr <SSIC> <code> of <d Mon yy>"},
  "from": "<from the rules file>", "to": "<addressee by billet>", "via": ["<only when there is routing>"],
  "subj": "<THE BASIC LETTER'S SUBJ, UNCHANGED>",
  "refs": ["<only what this endorsement adds>"], "encls": ["<only what this endorsement adds>"],
  "paragraphs": [{"text": "<Action in the first sentence.  The reason, with the date and count the addressee can check.>"}],
  "signature": "<F. M. LAST from the rules file>"
}
```

## Rules

- The identification line names the basic correspondence the way the library's figures do: ordinal in capitals, ENDORSEMENT, "on", originator, type ("ltr", "AA form", "report"), SSIC and code for a letter, and "of" or "dated" with its date. A placeholder in it fails the gate.
- The Subj is the basic letter's, unchanged. A Ref or Encl block appears only for what the endorsement adds.
- The first sentence is the action, in first person or the figures' passive ("Forwarded, recommending approval."). The reason follows, with dates and counts. A recommendation with no reason is warned; a disapproval with no fact is warned; a promise about the decision fails.
- Past FIRST, on the same page as the basic letter, with added references or enclosures, or with a copy to block: the product carries a one line note to the signer that the rule comes from SECNAV M-5216.5, which is not in the library, and that the command's practice in `Overrides/endorsement.md` was followed.
- The grid is the letter's: 13.8 pt pitch, identification line on the second line below the date, From on the second line below it, Subj on the second line below the heading, signature on the fourth line below the text. Never compressed to fit a page.
- `<MARINE>` until substitution. Nothing medical, family, financial, or from an investigation in an endorsement that goes in a record. No em or en dashes.

## Utility scripts

- `scripts/endorsement_check.py spec.json [--basic-subj ...] [--basic-refs ...]`: identification line complete (written ordinal, type, SSIC for a letter, date); Subj unchanged against the basic letter; From and To present; first sentence states the action; a reference the basic letter already lists (fail); strike words (warn); promises about the decision, names, lifted phrases, blocked content, dashes (fail); notes on each item only the manual settles.
- `../naval-letter/scripts/build_letter.py spec.json out.docx` renders it (the `endorsement` block prints the identification line); `../naval-letter/scripts/qc_letter.py out.docx --kind endorsement` is Gate 2a; `../naval-letter/scripts/measure_pdf.py out.pdf` is Gate 2b.
