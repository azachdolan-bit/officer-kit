# Directive voice

The reader is a Marine in the unit who opens the directive to find out what to do, and the Directives Control Point, which checks format before it goes to the commander. A directive is read for years by people who were not there when it was written. It states the rule and who does what; it never argues.

## The order's own words (use them exactly, never a paraphrase)
Paragraph titles: Situation. Cancellation. Mission. Execution. Commander's Intent and Concept of Operations. Commander's Intent. Concept of Operations. Subordinate Element Missions. Coordinating Instructions. Administration and Logistics. Command and Signal. Command. Signal. For a bulletin: Purpose. Cancellation. Background. Action. Reserve Applicability. Cancellation Contingency.

Statements: "This Order is applicable to the Marine Corps Total Force." or "This Order is applicable to the Marine Corps Reserve." (a company order says to whom it applies in the same shape). "This Order is effective the date signed." "This Bulletin is applicable to the Marine Corps Total Force." "Canc: Sep 2007." "Canc frp: Sep 2007." "DISTRIBUTION STATEMENT A: Approved for public release; distribution is unlimited."

Citations: "reference (a)", "references (b) and (c)", "enclosure (1)", "enclosures (1) and (2)", paragraph numbers as "3a(2)(b)" without periods or spaces.

## Sentences that carry a tasking
These sentences show shape only. No number, billet, or fact in them is to be taken into a product; the intake supplies those, and `directive_check.py` fails a draft that lifts a phrase from here.

"The platoon sergeants inventory the serialized gear in their platoon on the last training day of each month and report the count to the company gunnery sergeant before 1600." (Who, what, when, to whom.)
"The company gunnery sergeant is the main effort and reconciles the three platoon counts against the consolidated memorandum receipt before the first duty day of the following month." (The main effort, with the standard it is measured against.)
"Discrepancies of one item or more are reported to the executive officer the same day they are found." (A threshold and a clock.)
"The property record and the monthly count sheets are retained for two years and then destroyed per reference (b)." (A records instruction that names the disposition and the reference.)
"This Bulletin is canceled when the fiscal year inventory is complete and reported to reference (a)." (A cancellation contingency that names the condition and not the date.)

## Verbs that carry a task
inventories, reports, reconciles, submits, maintains, retains, destroys, inspects, certifies, publishes, approves, forwards, briefs, conducts, trains

## Strike on sight
See scripts/common_checks.py STRIKE. Add for this product: "all hands", "it is imperative", "at all times", "as appropriate" without saying who decides, "every effort", "ensure that" as a substitute for naming who does it, "and/or", "etc." in a tasking, "in a timely manner", "as soon as possible", "utilize", "is responsible for ensuring", "the utmost importance". Personal pronouns "I" and "me" (chapter 1 paragraph 15.b); "he" or "she" alone as a generic pronoun.

## Never
- A third directive type. The order issues an Order or a Bulletin; an SOP that is a permanent reference is an order, and a letter of instruction is outside the program.
- A bulletin without its cancellation line, or one that cancels more than 12 months out.
- A Cancellation paragraph anywhere but second, or a Mission that is not the next paragraph after it.
- A supplement below battalion or squadron on leave and liberty, assumption of command, alcoholic beverage control, mail handling, or command security procedures.
- A reference listed and never cited, or cited and never listed.
- A signature block with a grade or rank, or with the principal official's own title under the principal's name.
- A directive that decides a case about one Marine, or carries a Marine's name, service number, or medical, family, financial, or disciplinary facts. A directive states the rule; a record entry states the case.
- Em or en dashes.

## Professionalism rules
- Every major paragraph has a title; two subdivisions at least whenever a paragraph is subdivided; never past the eighth level.
- Dates as day month year with the three letter month in the identification block ("31 Aug 2003"); "(Date Signed)" until the commander signs.
- Acronyms spelled out at first use with the acronym in parentheses; no acronym used once.
- "Order" and "Bulletin" capitalized only when the directive refers to itself.
- Two spaces after a period and one after a parenthesis in the typed directive; Courier or Courier New 10 or 12 point; one inch margins; titles underlined. These are the word processor's job on the user's computer, not the draft's.
