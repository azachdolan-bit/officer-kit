# Standard: MCTP 3-30A, MAGTF Command and Staff Action (28 July 2020), chapter 3 and appendices A to E; MCO 5216.20B w/Admin Ch 4 (Marine Corps Supplement to the Department of the Navy Correspondence Manual, 10 Mar 2016 basic) chapter 13 on the Memorandum For

Status: INCOMPLETE for the From/To memorandum and the business letter. Read from `Doctrine/03_Operations_and_Readiness/MCTP_3-30A.pdf` and `MCOs/05_General_Admin_and_Management/MCO_5216.20B.pdf` in the user's publications library on 5 September 2026 (pdftotext; curly quotation marks written straight; line breaks inside sentences joined; nothing paraphrased inside a quote; elisions marked [...]). The memorandum for the record and the four staff papers are governed by the doctrinal publication quoted below, which is on disk. The plain memorandum (From and To lines, used between offices in the same activity) and the business letter are governed by SECNAV M-5216.5, which `find_order.py` reported NOT IN THE LIBRARY; those two formats are not built here and are listed at the end.

## MCTP 3-30A, chapter 3, Staff Action Papers and Formats (page 3-1)
> A staff officer will typically be required to prepare or produce outlines or documents that will assist superiors in making rapid and accurate decisions based on authoritative information. As such, staff officers should be familiar with and able to prepare the named papers provided in this appendix. The primary reference publications for correspondence formats are Secretary of the Navy Manual-5216.5, Department of the Navy Correspondence Manual, and Marine Corps Order 5216.20B, Marine Corps Supplement to the Department of the Navy Correspondence Manual, which provide the purpose for and examples of staff action papers. Minor differences exist between commands based on the command's organizational mission and the preferences of the commander. There are no major differences; however, and a general description of the types of staff action papers is found in the following paragraphs.

### Memorandum for the record (page 3-2)
> A memorandum for the record is prepared to record the impressions, information, conclusions, or decisions that arise out of formal or informal discussions, conferences, meetings, or telephone conversations. This document is frequently used as an in-house record of significant information that would otherwise not be recorded in writing. Often the memorandum for the record is a record of action underway and reasons for the action. The staff can also use this document to pass information up the chain of command in order to keep senior leaders apprised of events or actions within the author's purview. Refer to Appendix D for an example.

### Point paper (page 3-2)
> A point paper is a concise document designed to present key points, facts, positions, or questions in a brief and orderly fashion. It is normally used as a reminder and assumes complete knowledge of the subject by the intended user. The point paper usually does not exceed one page. It should be written in a brief, "telegraphic" style that can stand alone; however, graphs, schedules, and background data may be attached. A standard point paper will include the following: a heading; the subject in concise terms; salient points listed in short, concise statements; and a concise summary that may include any conclusion or position as appropriate. Refer to Appendix B for an example.

### Position/decision paper (page 3-1)
> An AO prepares a position/decision paper to develop, recommend, and obtain an official position on a particular proposition. It includes a clear statement of why an official position/decision is required, essential background on the problem or subject, and a rationale for the recommended position. [...] The heading contains the classification of the paper, the office code of the originator, the date, and the caption "POSITION/DECISION PAPER." The subject is indicated in simple terms. If references are used, they should be standard and self-explanatory. The problem statement identifies the problem for which the position is being developed. The author should also state why a position/decision is required. The background states what has taken place before. The positions of other agencies are addressed when appropriate; otherwise, "Not Applicable" is stated. The recommended position is stated in clear, concise terms. The rationale includes statements which support the position taken. The recommendation is the action you recommend to be taken, (e.g., "approve attached statement" or "study") as well as a decision block for the decision to be recorded.

### Talking paper (page 3-2)
> A talking paper is a narrative form used to advance a point of view or summarize an action or proposal. It includes concise comments for use during a meeting or oral presentation. The talking paper should stand by itself without reference to backup material. It is used as a memory aid or quick reference outline. Refer to Appendix C for an example.

### Information paper (pages 3-2 and 3-3)
> An information paper is typically used to provide factual information in concise terms to prepare the recipient for discussions and/or meetings. Only essential facts concerning the subject should be included and developed in an orderly and logical manner. Information papers are self-explanatory and will not refer to enclosures except for additional tabs containing data, charts, etc. Information papers are typically attached to other documents, hand-carried, or transmitted by informal note. They do not require an address or signature block. Place the appropriate originating office symbol/code and date in the upper right hand corner of the page. The date is the day of dispatch from the originating agency. The format may be altered to meet specific needs. Refer to Appendix E for an example.

## Appendix D, Format for Memorandum for the Record (page D-1), the model the tool builds
```
                               UNITED STATES MARINE CORPS
                           II MARINE EXPEDITIONARY BRIGADE
                             II MARINE EXPEDITIONARY FORCE
                                      PSC BOX 20080
                                CAMP LEJEUNE, NC 28542-0080

                                                                                      Code/Office
                                                                                      DD MM YY

                            MEMORANDUM FOR THE RECORD

Subj: THE SUBJECT MATTER IS INDICATED BRIEFLY BUT IN SUFFICIENT DETAIL TO
FACILITATE FILING AND FUTURE REFERENCE

1. Use a "Memorandum for the Record" (MFR) as an internal document to record information in
the record that is not recorded elsewhere. Examples include results of meetings, telephone
conversations, oral agreements, and other relevant information.

2. Type or handwrite these most informal memorandums. If it is only two or three lines, include it
on the file copy of your document. Leave out the subject line if you add your MFR to the file copy.

3. A full "signature" block and identification symbols are not required. However, it should be
dated, signed, and show the signatories' organizational code.

                                      I. M. RESPONSIBLE
                                         OPS, AC/S G-2
                                          LtCol USMC
```
(The letterhead and the three signature lines, name, billet, grade and service, are the appendix's own; the unit in the sample is the publication's example, not the user's.)

## Appendix B, Format for Point Paper (page B-1)
Letterhead; "Orig. Code" and "Date" at the right; the caption POINT PAPER centered; "To: Commanding General, or Deputy Commanding General, or Chief of Staff"; "Subj: THE SUBJECT MATTER IS INDICATED BRIEFLY BUT IN SUFFICIENT DETAIL TO FACILITATE FILING AND FUTURE REFERENCE"; then:
> 1. BACKGROUND. The background sets forth in concise terms what has gone on before; it provides answers to potential questions such as, "Is this an ongoing thing," or "Did something suddenly create this requirement?"
> 2. DISCUSSION
> a. The discussion is a concise narrative of all the salient points related to the topic under discussion.
> b. References that are used as a source are cited in the discussion.
> 3. RECOMMENDATION. Reduce recommendations to clear, concise statements that permit straightforward approval or disapproval by the approving authority.
> Prepared by: [...] Approved by: [...] Rank, First/Last Name / Billet [...]
> Derived From ______________ Declassify On (if applicable [...])_____

## Appendix A, Format for Position/Decision Paper (page A-1)
Caption POSITION/DECISION PAPER; "(Code)" and "(Date)" at the right; Subj; then:
> 1. Purpose. BLUF. Briefly state who the paper is for and why. [...]
> 2. Major Points. Briefly summarize major points to be made. a. State each point in one sentence. b. Major points should stand alone and not require amplification by subordinate points.
> 3. Discussion. a. This format is used to examine issues/unresolved matters, courses of action for implementation/resolution; provide rational to support a recommended position/decision the reader should take/make. b. Tailor the discussion to needs and knowledge of the reader. c. Write in short, clear, direct conversational style for the reader understands the key points and arrives at a logical conclusion. Use the active voice and avoid jargon; brevity is expected; identify all acronyms. d. General format is not as important as content. Tailor the paper to fit the need. Sub paragraphs such as, "Participants", "Facts", "Opposing Views", "Other Staff/Service Views", "Fallback Position", "Conclusion", and others may be used. e. Limit to one page unless issue is complex; do not exceed two pages. If greater detail is needed, attach tabs with supporting documents and address in content. f. Include preparer and approving official at the bottom of the page per below. [...]
> 4. Recommendation. The recommendation(s) must flow logically from major points and discussion. State in direct and positive language; provide a discussion grid to route through the chain to the decision making authority. [...]
> Prepared by: Grade and Name, Office Code, phone number / Approved by: Grade and Name, Office Code, phone number

## Appendix C, Format for Talking Paper (page C-1)
Caption TALKING PAPER; "Code/Office" and "Date" at the right; then the labelled parts:
> (U) FOR USE BY: List the name or title of person for whose use the paper is prepared.
> (U) SUBJECT: Indicate briefly but in enough detail for filing and reference.
> (U) BACKGROUND Indicate concisely what has gone before. Does it provide answers to such questions as is this an ongoing thing? Did something suddenly create this requirement?
> (U) DISCUSSION A concise narrative of all the salient points related to the topic under discussion. References used as a source are cited in the discussion.
> (U) RECOMMENDATION Reduce to clear, concise statements permitting simple approval or disapproval by the approving authority.
> (U) APPROVAL Provide an approval block for authentication by the approving authority.
> (U) ACTION OFFICER Indicate the action officer who prepared the paper.

## Appendix E, Format for Information Paper (page E-1)
Caption INFORMATION PAPER; "(Code)" and "(Date)" at the right; "Subject:"; then:
> 1. Purpose. Why is the information being provided?
> 2. Key Points. [in tick and bullet form] Use these papers to convey information for the readers use in preparing for a meeting or briefing. Present facts and use clear, concise wording. Tick and bullet format is preferred. Use key words and phrases. General format is not as important as content. Tailor the paper to fit the need. Convey information the audience (usually a principle) would need to know if being introduced to the subject issue or meeting for the first time. Address objectives the reader or participants may have for the meeting. Alert the reader to potential trouble areas. Identify hidden agendas. A length of one page is preferred. Two pages is the maximum. If meeting one-on-one with someone the reader does not know, attach a biographical sketch.
> Prepared by: I. M. Motivator, Capt, USMC / Agency, Section, Phone Number

## MCO 5216.20B, chapter 13 paragraph 2.b(1)(c) (page 13-51): the Memorandum For, HQMC's form
> (c) Memorandum For. This form of correspondence (does not have a "From" or "To" line) is the style of memorandum appropriate for signature by the Commandant. Type the signature line on the fourth line following the last line of text beginning from the center of the page (see Figure 13-12). (No complimentary close.)
(HQMC procedure, quoted because it is the only rule on disk for a memorandum's signature placement: the fourth line from centre, as on a letter.)

## From the kit's correspondence standard
The MFR is built on the naval letter grid (`naval-letter/references/standard.md`): Times New Roman 12, 1 inch margins, 13.8 pt pitch, the caption on the second line below the date, Subj on the second line below the caption, paragraphs single spaced within and double between, the signature name on the fourth line below the text from page centre with the billet and grade lines under it as Appendix D shows, no dashes.

## Not in the library
- SECNAV M-5216.5: the plain memorandum with From and To lines (between offices in one activity), the business letter, the memorandum's formal rules (whether a Subj line is required, whether "MEMORANDUM" is typed as a caption, the "Copy to" block), and whatever it says that qualifies Appendix D's "Type or handwrite" and "A full signature block and identification symbols are not required." The tool builds the MFR to Appendix D and says so; the user's command may want the manual's form.
- The command's own staff SOP, which MCTP 3-30A says sets the "minor differences"; `Overrides/memo.md` records it.
