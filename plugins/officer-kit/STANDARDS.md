# Kit standards

Kit standards: 0.12.0

Every Officer Kit tool reads this file before it produces anything. The nine standards apply to every product. If the user's rules file or an `Overrides/<tool>.md` line says otherwise, say so once, naming the standard by number, then do it the user's way.

1. **Save gate.** A product exists only when it is a file in the user's working folder and the reply names its path. Write it, confirm it is there, then present it. Save every revision. If the folder is not connected, the first line of the reply is "NOT SAVED to your computer: <file>" with where to put it. Before the last reply of a session that built anything, list every file created with its path.
2. **Sources only.** Build from the user's notes, captured sources, and cited references. Never fill a gap from general knowledge or the web; name the gap instead. When sources conflict, the school or unit document outranks the general publication, the newer document outranks the older, and the conflict is flagged in the product.
3. **Do not state what is implied.** Cut any sentence that restates what the title, the tasking, or the format already says ("findings are stated as observed," "this enclosure will be updated"). Look for that class of sentence before delivery.
4. **Build only what was asked.** The deliverable named in the current request is the specification. The set delivered last time is not. Ask before building anything extra.
5. **Library first.** Read any order, directive, MARADMIN, ALMAR, or doctrinal publication from the user's library or Reference folder first (`library/scripts/find_order.py <number>`), rendering figure pages as images when the text is a picture. Go to the web only when the publication is not on disk, and say so.
6. **Share the method, never the product.** A product built from course or unit material goes only to the people who helped build it; what gets shared is a builder with zero content. A document meant for other people never describes browser automation.
7. **Teaching products are complete.** The body carries the whole source lesson, verbatim where the source is verbatim. Every quiz answer appears in the body of the section that tests it. Run the `source-fidelity-reviewer` agent before delivery.
8. **Never compress to fit.** Never shrink line spacing, margins, heading space, or signature space to make a page count. Cut words instead.
9. **No em dashes or en dashes** in any product. Rewrite the sentence; do not swap in a colon.
