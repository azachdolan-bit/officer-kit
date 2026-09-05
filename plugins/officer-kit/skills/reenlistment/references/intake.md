# Reenlistment intake

One question at a time. "I do not know" is recorded as a gap, never filled. Ask what this request raises, not what reenlistment requests usually raise. Never put a candidate answer inside the question.

## 1. Frame
1. Which block are you signing on the RELM (35a NCOIC/SNCOIC, 35b OIC, 35c First Sergeant, 35d Company Commander, 35e Sergeant Major, 35f Executive Officer, 35g Commanding Officer), and is the request a reenlistment, an extension, or a lateral move?
2. Who is the certifying officer at 35g, and is that officer signing personally, or is the executive officer recommending on the CO's behalf? (The order lets the XO recommend for the CO, and does not let anyone but the CO give "with reservation" or "not recommended".)
3. The Marine's grade, PMOS, billet, and time in the billet under you. ECC and EAS as dates. First term or career?

## 2. The tier is a population claim
4. How many Marines of this grade does the certifying officer know well enough to rank? (Not the unit's strength; the ones actually known.)
5. Where does this Marine stand among them, as a number of that number? The tier follows from the answer: top quarter is "with enthusiasm", top half is "with confidence". If the officer cannot put a number on it, the top two tiers are not available and the record should say why.

## 3. Conduct, performance, potential (the order's three heads, paragraph 4.b)
6. Conduct on this contract: what is in the record, as dated facts? (An NJP by date and a Page 11 by date are facts the prerequisites screen needs; the story behind them is not.)
7. Performance: what did the Marine do in this billet that can be counted, and against what? Climb the ladder on each note: action, scope, result, comparison, consequence; stop where you can defend it.
8. Future potential as it relates to rank, age, experience, and maturity: what has the Marine been given beyond the billet, and what happened? What would the next grade require that you have or have not seen?

## 4. The prerequisites (35g, or whoever prepares the CO's certification)
9. Walk the 21 basic prerequisites in standard.md paragraph 5.a as yes, no, or unknown, plus 5.b for a first term Marine and 5.c for a career Marine. For each "no": is it one HQMC may waive or may not? A waiver needs the CG's own endorsement, not by direction, and a letter from the Marine.
10. Fitness reports: any missing report or a gap of 30 days or more in the last five years or on this contract? (Prerequisite (20); MMEA-6 can grant a short extension to fix it.)

## 5. Reservation or not recommended
11. What is the reason, as facts with dates? The form says comments are mandatory; the order says the CO must indicate the reason and that this authority may not be delegated.
12. For "not recommended": on what date did the commanding officer personally interview the Marine (the order requires it), and which RE code does the CO assign? (The CO, not a delegate, assigns anything other than RE-1A; the request still goes to MMEA-6, which decides.)

## 6. Windows
13. Which required interview is this attached to, and was it in its window: initial 26 to 24 months before ECC, FTAP or careerist 14 to 12 months before ECC, EAS interview 8 to 6 months before EAS? `scripts/reenlistment_windows.py --ecc <date> --eas <date>` computes them.

## 7. The reader
14. How does the CO and the Career Planner want block 35 comments written (paragraphs, sentence fragments, result first)? Record it in `Overrides/reenlistment.md`.

## The quantification ladder
| Rung | Question |
|---|---|
| Action | What did the Marine do? |
| Scope | For how many, how often, how long? |
| Result | What changed, in a number? |
| Comparison | Against what: the other Marines of that grade you know, the unit's standard, last year? |
| Consequence | What did the unit get? |
Stop at the rung the certifying officer can defend to MMEA-6.
