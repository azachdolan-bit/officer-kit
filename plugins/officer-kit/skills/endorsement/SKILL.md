---
name: endorsement
description: >
  Drafts and builds an endorsement on correspondence moving up or down the chain, to SECNAV M-5216.5 chapter 9 and on the naval letter grid the kit measures: the identification line (the ordinal, ENDORSEMENT on, and the basic letter in reference style), From, To and the remaining Via addressees, the basic letter's own Subj, references and enclosures lettered and numbered by continuing the basic letter's sequence rather than restarting, same page or new page by whether it fits on the signature page, the Copy to block that the manual requires when an endorsement is significant rather than routine, and numbered paragraphs whose first sentence is the endorser's action with a reason the addressee can check. Use when the user says "endorse this request", "first endorsement on", "forward this recommending approval", "chop this up the chain", "the battalion needs my endorsement", or "readdress and forward".
metadata:
  version: "0.2.0"
---

# Endorsement

The addressee has the basic letter in hand and reads the endorsement for one thing: what did this endorser do with it, and why. The four endorsements reproduced in orders in the user's library agree on the layout (identification line, From, To, Via, the same Subj, numbered paragraphs, signature) and on the voice (first person: "I do not recommend", "I concur", "I certify", "I direct"). The tool asks for the basic correspondence's identifiers so the identification line is exact, asks what the endorser did and on what facts, writes the action in the first sentence and the reason after it, and builds the page on the kit's measured grid. It drafts; the endorser signs. The governing manual, SECNAV M-5216.5, is in the library, and its Chapter 9 settles what the tool used to leave open: the ordinal counts the endorsements added to the basic letter and not the echelons (9-2.1.b); a short endorsement that fits the signature page may be typed there and may omit the SSIC, subject, and the basic letter's identification (9-1, 9-2.1.a); added references and enclosures continue the basic letter's letters and numbers (9-2.3, 9-2.4); and a significant endorsement, which 9-2.5 defines by example against a routine one, carries a copy to block naming the originator, every prior endorser, and the earlier copy to addressees. Chapter 9 does not reach everything, and what it leaves open (a return without action, what makes a comment substantive, whether a level may be skipped) stays a named gap in `references/standard.md`, filled from `Overrides/endorsement.md` where the command has a practice and from nothing else.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Read first

1. `references/standard.md`: SECNAV M-5216.5 Chapter 9 quoted with its paragraph numbers, the four figures from the library (MCO 1900.16 Figures 6-5 and L-10; NAVMC 4000.5D enclosure (12) pages 119 and 129) under it, what Chapter 9 does not settle, and what the builder cannot yet render.
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
- [ ] 3. Anything the endorsement adds (a reference or enclosure by exact title) and nothing it repeats; through what letter and what number the basic letter and previous endorsements already run (9-2.3, 9-2.4)
- [ ] 4. Routing: To, Via, who signs and how; identity from the rules file. Name the action, then apply 9-2.5: significant or routine, and if significant, the originator, every prior endorser, and the earlier copy to addressees go in the copy to block
- [ ] 5. Read back the fact list; the user confirms; nothing else goes in. Now read exemplar.md for shape
- [ ] 6. Write spec.json (below) with the endorsement block; where this endorsement touches something Chapter 9 leaves open (a return without action, whether a comment is substantive, a skipped level), say so in a note to the signer with what was assumed
- [ ] 7. python3 scripts/endorsement_check.py spec.json --basic-subj "<the basic Subj>" --basic-refs "<each basic ref>" --basic-encls "<each basic encl>" --originator "<the originator>" --prior-endorsers "<each>" exits 0
- [ ] 8. python3 ../naval-letter/scripts/build_letter.py spec.json "<name>.docx"; python3 ../naval-letter/scripts/qc_letter.py "<name>.docx" --kind endorsement exits 0
- [ ] 9. Rendered to PDF; python3 ../naval-letter/scripts/measure_pdf.py "<name>.pdf" exits 0; the page read as a picture. The builder prints no copy to block and letters a Ref block from (a): type the block and correct the letters on the page before signature
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
  "refs_start": "<the letter the first added reference carries, continuing the basic letter's>", "encls_start": "<the same for enclosures>",
  "copy_to": ["<on a significant endorsement: the originator, each prior endorser, the earlier copy to addressees>"],
  "same_page": false,
  "paragraphs": [{"text": "<Action in the first sentence.  The reason, with the date and count the addressee can check.>"}],
  "signature": "<F. M. LAST from the rules file>"
}
```

## Rules

- The identification line names the basic correspondence the way the library's figures do: ordinal in capitals, ENDORSEMENT, "on", originator, type ("ltr", "AA form", "report"), SSIC and code for a letter, and "of" or "dated" with its date. A placeholder in it fails the gate.
- The Subj is the basic letter's, unchanged. A Ref or Encl block appears only for what the endorsement adds.
- The first sentence is the action, in first person or the figures' passive ("Forwarded, recommending approval."). The reason follows, with dates and counts. A recommendation with no reason is warned; a disapproval with no fact is warned; a promise about the decision fails.
- The ordinal is the endorsement's place in the sequence in which endorsements were added to the basic letter (9-2.1.b), not the endorser's place in the chain. A reference or enclosure the endorsement adds continues the basic letter's sequence (9-2.3, 9-2.4): after references through (f), the first added one is (g).
- Name the action, then apply 9-2.5. Significant ("forwarded, recommending disapproval", "readdressed and forwarded", substantive comments): the copy to block carries the originator of the basic letter, each activity that endorsed before, and all copy to addressees from the basic letter and previous endorsements, with "(complete)" beside any of them receiving the basic letter for the first time from this endorser (9-2.6.c). Routine ("forwarded", "forwarded for consideration", "forwarded, recommending approval"): the manual does not require the block. The product carries a one line note to the signer on what the tool cannot render (the copy to block, continued lettering, a same page endorsement) and on anything Chapter 9 leaves open that this endorsement touches.
- The grid is the letter's: 13.8 pt pitch, identification line on the second line below the date, From on the second line below it, Subj on the second line below the heading, signature on the fourth line below the text. Never compressed to fit a page.
- `<MARINE>` until substitution. Nothing medical, family, financial, or from an investigation in an endorsement that goes in a record. No em or en dashes.

## Utility scripts

- `scripts/endorsement_check.py spec.json [--basic-subj ...] [--basic-refs ...]`: identification line complete (written ordinal, type, SSIC for a letter, date); Subj unchanged against the basic letter; From and To present; first sentence states the action; a reference the basic letter already lists (fail); strike words (warn); promises about the decision, names, lifted phrases, blocked content, dashes (fail); the 9-2.5 significant or routine test, which decides whether a copy to block is required and who is in it (fail); an enclosure the basic letter already lists (fail); and the letters and numbers 9-2.3 and 9-2.4 require of what this endorsement adds.
- `../naval-letter/scripts/build_letter.py spec.json out.docx` renders it (the `endorsement` block prints the identification line); `../naval-letter/scripts/qc_letter.py out.docx --kind endorsement` is Gate 2a; `../naval-letter/scripts/measure_pdf.py out.pdf` is Gate 2b.
