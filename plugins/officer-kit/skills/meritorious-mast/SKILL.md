---
name: meritorious-mast
description: >
  Drafts the two lightest recognitions that enter an enlisted Marine's record under MCO 1650.19J
  w/Ch 1: the Meritorious Mast text for the NAVMC 10935 and the Certificate of Commendation text
  for the NAVMC 10631, each with the level check the order implies (a Mast is not conducted when
  the service is recognized by a Letter of Appreciation, a Certificate of Commendation, or a
  personal decoration), who may sign each (the commander at battalion or equivalent echelon; a
  general officer or a commander with Achievement Medal authority), dated and counted facts, a
  text that carries no number the facts do not, and the routing the order sets (a copy to CMC
  (MMSB) for the OMPF, nothing to CMC (MMMA), no awards processing system entry). Use when the
  user says "meritorious mast for", "mer mast", "write up a mast", "certificate of commendation
  for", "certcom", "is this a mast or a certcom", "recognize this Marine short of a NAM", or
  pastes what a Marine did and asks for something lighter than a medal.
metadata:
  version: "0.1.0"
---

# Meritorious Mast and Certificate of Commendation

The order lays out a ladder: proficiency and conduct marks and the fitness report; then a Meritorious Mast or a Letter of Appreciation; then a field or CMC Certificate of Commendation "in those cases where none of the above is considered appropriate"; then a personal decoration, "limited to those cases in which the performance of duty was so exceptionally superior that its significance and contribution to the Marine Corps are clearly recognized by superiors and contemporaries alike" (enclosure (2) paragraph 1). It names two factors for the step, the magnitude of the achievement and the level of responsibility of the Marine, and says grade is not one (paragraph 6). It then closes the ladder from below: "A Meritorious Mast shall not be conducted when the service or performance of the Marine is recognized through the awarding of a Letter of Appreciation, Certificate of Commendation, or a personal decoration" (8.g(1)). One recognition per service. The tool puts the facts on that ladder before it writes a word, drafts the text the commander signs from those facts and nothing else, and writes the routing the order sets: a copy to CMC (MMSB) for the OMPF and nothing to CMC (MMMA), on the form, outside the awards processing system. The reader decides two things from the page: whether the facts reach this recognition and no higher, and whether what the text says happened. Routing here is the 2001 order's paper routing; the iAPS MARADMIN is not in the library, so the command's current electronic practice, if any, comes from `Overrides/meritorious-mast.md`.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its nine standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Read first

1. `references/standard.md`: enclosure (2) paragraph 1 (the ladder), 6 (level of award), 8.f (Certificates of Commendation: who issues, who recommends, where copies go), 8.g (Meritorious Mast: threshold, the observer's report, the commander, 8.g(1) and the form), 8.h (Letter of Appreciation, for the boundary); enclosure (1) 1.l(5) (NA authority), 9.a and 9.b (the certificate forms and the green copy), 5.a (presentation). The "Not in the library" section says what SECNAV M-1650.1 and MARADMIN 024/22 would settle.
2. `references/intake.md`: the questions, one at a time.
3. `references/voice.md`: the order's threshold words as the test, the shape, the strike list.
4. `references/exemplar.md`: read only after the fact list is confirmed (step 5). It teaches shape and its content is not to be taken; the checker fails a lifted phrase.

## Your own material (read first, every time)

1. `Overrides/meritorious-mast.md`: how this commander wants the text written, the command's closing line if it has one, whether the copy to MMSB goes by green copy or through the current electronic system, who in the unit forwards it. The command's way wins; say in one line what it changed.
2. `Reference/Exemplars/meritorious-mast/`: Masts and certificates this command signed, sanitized. They beat the plugin's fictional exemplar.
3. `<MARINE>` throughout, and the unit by echelon, not by name; the name and the unit go on the form on the user's computer with `security-check/scripts/substitute.py`. The social security number the green copy needs (enclosure (1) 9.a) is added there too, never in the draft.
4. When the commander changes the level, or the Mast comes back as a certificate, `aar` captures why.

## Before you draft

1. **Assume it already failed** and write three reasons before you build anything, then check each against the draft. Reasons written after rereading a draft are a list of what the draft already covers.
2. **Ask only what changes the product,** and never put a candidate answer inside the question.
3. **Say what you assumed** and mark it in the product so it cannot be signed without being closed. Never write that the rest is covered; `think/scripts/precision_check.py` fails a product that claims it.
4. **Before it is signed:** the `red-team` agent, blind, with the standard and an exemplar.

## Workflow

```
Meritorious Mast or Certificate of Commendation:
- [ ] 1. Frame: who observed the performance (billet); who will sign (billet, echelon, and for a certificate the authority: general officer, or commander with NA authority); the Marine (label, grade, billet, unit by echelon); enlisted, for a Mast
- [ ] 2. Prior recognition: is this service recognized, or being drafted, as a Letter of Appreciation, a Certificate of Commendation, or a personal decoration? If yes, no Mast (8.g(1)); the product is that recognition or nothing
- [ ] 3. Facts, one question at a time: what, for how many, how long, what changed in a number, against what, at what level of responsibility; climb the ladder on each note and stop where the signer can defend it to the formation
- [ ] 4. Level: put the facts on the order's ladder with its two factors; name one recognition and say why the facts stop there, in both directions; if the answer is a Letter of Appreciation, hand off to letter-of-appreciation; if a personal decoration, hand off to award
- [ ] 5. Read back the fact list; the user confirms; nothing else goes in. Now read exemplar.md for shape
- [ ] 6. Draft mer_mast.md or certcom.md in the shape below; every number in the Text is in the Facts
- [ ] 7. Routing per the order: the observer's report and the commander for a Mast; the recommender and the issuing officer's authority for a certificate; the form; the copy to CMC (MMSB) for the OMPF; nothing to CMC (MMMA); not through the awards processing system; presentation in the presence of Marines
- [ ] 8. python3 scripts/meritorious_mast_check.py <file> exits 0
- [ ] 9. Strike pass with voice.md
- [ ] 10. Saved to Admin/Awards/<label> <Mast | CertCom> <date>.md; the officer copies the text onto the form; the awards clerk routes the copy
- [ ] 11. Learning: what the commander changed, via aar
```

## The product (mer_mast.md or certcom.md)

```
# Meritorious Mast                                  (or: # Certificate of Commendation)
Marine: <MARINE>, <grade>, <billet>   Unit: <echelon, not name>   Awarding officer: <billet, echelon; for a certificate the authority>   Date: <day month year>
Reported by: <billet of the officer who observed the performance>   (Mast; for a certificate: Recommended by: <billet>)
References: MCO 1650.19J w/Ch 1 enclosure (2) paragraph 8.g; NAVMC 10935   (certificate: paragraph 8.f; enclosure (1) paragraphs 1.l(5) and 9.a; NAVMC 10631 and NAVMC 10631A)

## Level check
Recognition: <Meritorious Mast | Certificate of Commendation | Letter of Appreciation | personal decoration>   (one, on this line alone)
<why the facts reach this step and not the next, in the order's two factors: magnitude, level of responsibility; the 8.g threshold words for a Mast; the 8.g(1) sentence and whether it applies>

## Facts
- <date or period>: <what, for how many, how long, what changed, against what>
- ...

## Text
<the text the commander signs: what the Marine is recognized for with billet and dates; two to four sentences each carrying one fact from the Facts; one sentence on what the unit got>

## Routing
- <Mast: the observer's report to the commander (8.g); NAVMC 10935; signed by the commander at battalion or equivalent echelon>
- <certificate: signature line per 8.e(5); recommender and the issuing officer's authority (8.f(1), (2)); not via the HQMC APS, no 1650 (EF); NAVMC 10631 original to the Marine; NAVMC 10631A green copy to CMC (MMSB), social security number added on the user's computer>
- Copy to CMC (MMSB) for the OMPF. Do not forward a copy to CMC (MMMA).
- Presentation in the presence of Marines (enclosure (1) 5.a); the red presentation folder (9.f)
- Current electronic routing, if the command uses one, per Overrides/meritorious-mast.md
```

## Rules

- One recognition per service. The Recognition line in the level check names one, and the product type follows it. The checker fails a Meritorious Mast whose level check names a Certificate of Commendation, a Letter of Appreciation, or a personal decoration, quoting 8.g(1), and a certificate whose level check names anything else. A level check that says the facts stay in the marks and the fitness report means no product.
- The level in the order's factors: magnitude of the achievement or service and level of responsibility of the Marine (enclosure (2) paragraph 1); "not the grade of the individual" (paragraph 6). The threshold for a Mast is the order's: "noteworthy or commendable beyond the usual requirements of duty" or "exceptional industry, judgment, or initiative" (8.g).
- A Meritorious Mast is for an enlisted Marine and is held by the Marine's Commander, battalion or equivalent echelon, on the report of the senior person who observed the performance (8.g). The checker fails a Mast for an officer grade and a Mast whose awarding officer is below that echelon or signs by direction.
- A Certificate of Commendation is issued by a general officer or a commander with delegated NA authority, which enclosure (1) 1.l(5) gives to Special Courts Martial Convening Authorities; any other officer recommends to that officer and does not issue (8.f(1), (2)). It is not submitted via the HQMC APS and needs no 1650 (EF) (8.f(2)). A CMC Certificate of Commendation is the exception and goes to CMC (MMMA) on the HQMC APS with a Summary of Action and proposed citation (8.f(5)); that is the `award` tool's process.
- Facts are dated and counted. Every number in the Text appears in the Facts; the checker fails one that does not (the award tool's citation versus Summary of Action rule).
- Routing per the order: a copy to CMC (MMSB) for the OMPF; nothing to CMC (MMMA) (8.g(2); 8.f(2); enclosure (1) 9.a). The checker fails routing that omits MMSB, omits the MMMA prohibition, or sends anything to MMMA, and a certificate routed through the HQMC APS. The Letter of Appreciation goes to neither and does not enter the OMPF (8.h); if that is the recognition, this tool is the wrong tool.
- Format: the order sets none for the text of either product. The all capitals, 9 point, landscape, 1200 character rule is for the NC and NA certificates (8.e(6)) and is not applied. The signature line rule at 8.e(5) (name, grade, official title, unit identification) is followed for the certificate's signature line as the nearest rule the order has, and is marked as such.
- Nothing about a board, a promotion, or a future award. No medical, family, financial, disciplinary, or investigation content.
- `<MARINE>` until substitution on the user's computer; the unit by echelon; no social security number in the draft. No em or en dashes.

## Utility scripts

- `scripts/meritorious_mast_check.py <mer_mast.md | certcom.md>`: title names the product; `<MARINE>`, Unit, and Awarding officer in the header; a Mast for an enlisted grade, held by a commander at battalion or equivalent echelon, not by direction (fail); a certificate signed by a general officer or a commander, not by direction (fail), with the authority stated (warn); Level check with one Recognition line that agrees with the product type (fail otherwise, with 8.g(1) quoted), citing 8.g(1) and the order's factors (warn); Facts present, dated, counted (fail); Text present, every number in the Facts (fail), strike words and abbreviations (warn), promises and blocked content (fail); Routing with the form number, the MMSB copy, and the MMMA prohibition (fail), a certificate not through the HQMC APS (fail if routed through it), presentation line (warn); a unit by name, a name, a lifted exemplar phrase, blocked content, or a dash (fail). Exit 1 on any failure.
