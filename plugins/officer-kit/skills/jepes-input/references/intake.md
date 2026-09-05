# JEPES input intake

One question at a time. "I do not know" is recorded as a gap, never filled. Ask what this occasion raises, not what JEPES occasions usually raise. Never put a candidate answer inside the question.

## 1. Frame
1. What is your role in this Marine's reporting chain: First Line Supervisor, Evaluator, or Reviewer? (Chapter 1 paragraph 5. A Senior Enlisted Reviewer or Command Reviewer advises and does not make recommended marks; if that is the role, the product is a comment to the chain, not marks.)
2. Who is the Approver, by billet? (The O-5 level commander or OIC equivalent, or the one leader appointed by letter when the Approver cannot act.)
3. The Marine's grade, PMOS, billet, and the date your supervision of the Marine began. The order covers Private through Corporal; a Sergeant is evaluated under MCO 1610.7B, not here.

## 2. The occasion
4. Which occasion is this, by the order's code: PR, TR, CD, TD, TC, AN, SA, AT, DC, RD, DD, RT? If two occur at once, the higher on the list is used (chapter 2 paragraph 2.b).
5. The FROM and TO dates. For SA the TO date is 31 July or 31 January and the FROM date is 1 February or 1 August unless a previous occasion ended later; for AN, 1 January to 31 December. For the event driven occasions, the TO date is the one the order fixes for that code (PR: the day prior to the new date of rank; CD: the date prior to the change of duty; DC: the day before discharge; TR, TD: the date of departure; RD: the last day at the previous rank). `scripts/jepes_dates.py` computes the period, the 45 day submission window, and the Approver's due date.
6. On what date are you submitting? Recommended marks may not be submitted earlier than 45 days before the end of the period (chapter 1 paragraph 6.c). Was the Marine observed for 30 days or more (chapter 2 paragraph 2.c)?
7. Did another occasion under this command end within 30 days of this period's end, or did the Marine arrive with an evaluation from a previous unit within 30 days of it? (Chapter 2 paragraph 2.d omits the AN or SA when it did.)

## 3. Initial counseling (when the relationship is new)
8. On what date was the reporting chain established or your supervision of the Marine begin? The FLS owes an initial written counseling within 30 days of that date (chapter 2 paragraph 1.b(1)); the due date is on the header.
9. For that counseling, in your words: the Marine's billet description; the Marine's role in the unit; the responsibilities; the performance expectations. Which objective scores (rifle, MCMAP, PFT, CFT, informal PME, self education) did you and the Marine validate, and what corrective action was started?

## 4. Facts under the three categories, in the order's order
Individual Character; MOS and/or Mission Accomplishment; Leadership. For each:
10. What did the Marine do during this period, as a fact with a date? Billet accomplishments the Marine submitted through the MRO Dashboard count (appendix E); what does not count: required annual training, an award for actions in a previous period, hobbies.
11. Climb the ladder on each note: action, scope (how many, how often, how long), result in a number, comparison (against peers of the grade, the unit's standard, last period), consequence for the unit. Stop where you can defend it to the Approver.
12. Which facts fall outside the FROM and TO dates? They come out; the order says command input "must be based on the Marine's accomplishments [...] during the reporting period" (chapter 1 paragraph 3.b(2)).

## 5. The mark, from the facts
13. Start at 2.5 in each category (chapter 2 paragraph 3.a(3)). What fact moves it, and which way?
14. For a mark of 4.1 or above: what formal commendatory material, by type and date, is visible in JEPES for this period? Without it the order places the Marine at 4.0 or below ("Solid performers whose accomplishments did not rate formal commendatory material"). Which directed comment from the drop-down list will you select?
15. For a mark of 0.9 or below: what counseling, documented or informal, occurred during this period, and on what date? Which directed comment will you select? (This band is not adverse and does not by itself NOT REC the Marine.)
16. Have you read Figure 1-2 for this occasion? It is not in the kit's library; the mark is chosen against it, not against a unit or personal standard (chapter 1 paragraph 4.c).

## 6. Promotion recommendation
17. Is the Marine recommended for promotion (the default), or is a NOT REC recommended? A NOT REC needs a directed justified comment; the order's adverse material list (pending or completed legal action, notification of separation proceedings, BCP or MAP assignment, PFT or CFT failure, training failure, subject of a CRB) is stated by category and date, not by story. A 0.0 in any category is a NOT REC by default.

## 7. The debrief
18. When and by whom will the Marine be debriefed after approval (chapter 1 paragraph 6.f)? What should the Marine focus on next period, as facts from this one?

## 8. The reader
19. How does this Approver want justifications written (one line, result first, the directed comment named)? Record it in `Overrides/jepes-input.md`.

## The quantification ladder
| Rung | Question |
|---|---|
| Action | What did the Marine do? |
| Scope | For how many, how often, how long? |
| Result | What changed, in a number? |
| Comparison | Against what: peers of the grade, the unit's standard, last period? |
| Consequence | What did the unit get? |
Stop at the rung the preparer can defend to the Approver.
