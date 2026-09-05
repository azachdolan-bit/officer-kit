# Estimate: Risk Assessment Worksheet, company Table 2 at Range 7

Tier: deliberate, because people can be hurt on a live fire range and the approval level follows from the arithmetic on this sheet. Nothing lowers this below deliberate. Anyone can raise it.

## Task and the outcome it serves

A Risk Assessment Worksheet for a two day company Table 2 shoot at Range 7 in October 2026, so the event is approved at the level the residual risk actually earns and so the OIC and the RSO have something to supervise from on the day.

The requested product is the right one. The outcome named in the tasking is a signature by Friday; the outcome the sheet exists for is a range that is safe with the people who will actually be there. Those come apart in one place worth saying once: the order allows a repeated event to reuse last year's worksheet only after it is updated and every assessment is re verified (040304.B). If last year's sheet exists, sending it to me beats building from nothing, and the fastest honest route to Friday.

## Standard

MCO 5100.29C Volume 2 (15 Oct 2020), paragraphs 030302, 040203, 040302, 040303 and 040304, with Figures 3-2, 3-3 and 3-4. The order itself is not on this machine. I worked from the extracts in the skill's `references/standard.md` and `references/matrix.md`, which record that the figures were read cell by cell from the user's own copy on 5 September 2026. I did not go to the web for it.

Not verified here: the installation's range regulations, the Range 7 standing operating procedure, and any battalion risk management order or worksheet form. None of the three is on disk. The command's form and matrix govern over the order's Figure 3-4 wherever they exist.

## Facts

- The event is Table 2, two days, at Range 7, next month, with the whole company attending (from the tasking).
- The same range ran last year and one Marine became a heat casualty on the second day (from the tasking).
- A corpsman will be present (from the tasking).
- The requester is the OIC and the requester's platoon sergeant is the RSO (from the tasking).
- Battalion wants the sheet by Friday for signature (from the tasking).
- Today is 5 September 2026, so next month is October 2026 (from the calendar).
- No head count, no dates, no installation, no transport method and no ammunition figure were given (from the tasking).

## Assumptions

- The corpsman is present for every live serial on both days and holds a current trauma certification. Becomes a fact from the training record and the company roster. If false, the response plan and two residual levels both move, and the sheet cannot be signed as written, which makes this a blocking question rather than an assumption I am willing to carry.
- Movement to Range 7 is by unit vehicle in the dark before first light rather than on foot from the company area. Confirmed by the training schedule and the transport request. If false, hazards 6, 7 and 14 come off the sheet and nothing else changes.
- The battalion publishes no worksheet form and no matrix of its own, so this sheet uses the order's Figure 3-4 and the kit's default approval table. Confirmed by the battalion safety officer in one call. If false, the levels and the approval line change and the sheet is rebuilt on the command's form.
- October at this location still produces a flag condition that requires a work rest cycle. Confirmed by the installation's flag history for October. If false, nothing changes, because the control is an hourly check that is performed either way.

## Questions

1. What are the two dates, and what is the head count from the company roster? This sets the header, and it changes the water, transport and response figures that everything downstream is sized against.
2. What is the corpsman's trauma certification and its date, and who is the second corpsman if the first one is pulled? This determines whether the response plan stands and whether two residual levels hold. Blocking.
3. What went wrong or nearly went wrong on this range last year besides the heat casualty, and what does range control's own mishap history for Range 7 hold? This changes the hazard list, which is the one part of the sheet nothing mechanical can check.
4. Which installation owns Range 7, and what do its range regulations and range control require for evacuation, radio watch and dud rounds? This changes the response plan from placeholders into something usable on the day.
5. Does the battalion publish its own risk assessment worksheet form or matrix? This changes the levels, the approval line and the form the sheet is transferred onto.

## Will not do

This does not decide what risk the commanding officer accepts, and it does not certify the OIC, the RSO or the corpsman. It does not replace the range regulations or the Range 7 standing operating procedure, neither of which I have. It computes each level from the order's matrix and names the approval authority that follows from the arithmetic. It does not name a single Marine; billets only, with names added on the signature block.

## Checked by

`scripts/raw_check.py raw.md` for the arithmetic in every row, the high risk flag against the residual pairs, the approval line, the required elements, and for names and blocked content in the body. `scripts/estimate_check.py` on this document.

Nothing mechanical can tell you the hazard list is complete, that the corpsman will be there, or that the controls will be executed by the people named in them. Those are the three things that would actually hurt someone, and they are where the signer's own attention has to go.

## Premortem, run before the hazard list

Three Marines were hurt on this event and this sheet is now an enclosure to the investigation. How, written before the hazard list was built rather than after:

1. Heat again, on the second afternoon, because last year's single case was treated as bad luck instead of as this range's signature failure, and because day two is when the water discipline of day one quietly stops.
2. A round went somewhere it should not have, not during the deliberate slow fire but during a transition: a Marine moving between barricade positions with a loaded weapon, or a shooter reacting to hot brass.
3. Nobody was hurt on the range at all. A vehicle rolled on the way out in the dark, or an operator who had been awake since 0330 for two days drove the company home.
4. Someone was hurt on the range and the injury became worse than it needed to be, because the ground evacuation route from Range 7 had never been driven and the corpsman was at the tower when the casualty was at the far lane.

Then the standing question: what appears on every worksheet for an event like this that is not on mine? Heat in August or October. The road, not the range. The transition between serials. Hearing. The police call at the end. The drive home. All six are now on the sheet.
