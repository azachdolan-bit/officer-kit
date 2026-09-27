---
name: share-method
description: >
  Turns a study product the user built from course or unit material (a study guide, a drill file,
  a quiz, a simulator, a walkthrough) into a builder a peer can run on their own material: a method
  file with zero content, the user's own sharing policy quoted from disk with its arbiter named,
  emphasis converted into exhaustive extraction, the safeguards checked by section, a leak scan
  against every source with each hit shown in context, and a blind run of the builder before it
  goes out. Use when the user says "make this shareable", "share the method", "can I share this",
  "my buddy wants my study guide", "turn this into a builder", or "is this builder clean to send".
metadata:
  version: "0.1.0"
---

# Share method

A product built from course material usually cannot go to someone who did not help build it, and a peer who asks for it wants what made it good, not the file itself. What can go is the method: a builder with no content that makes the peer's own Claude build the peer's own product from the peer's own source. A builder fails in three ways. It leaks a term, a value, or a sentence from the source. It leaks the author's emphasis, the traps they found, which no word scan sees. Or it is so thin that the peer's Claude fills the gaps from general knowledge and trains the peer on the textbook version instead of their school's.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Standard 6 is this tool's reason to exist. Where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Your own material (read first, every time)

1. `Overrides/share-method.md` in the working folder, if it exists: the user's way wins. Say in one line what it changed.
2. The user's own sharing or academic integrity policy, from disk. Find it (search the working folder for "policy", "integrity", "academics", leaving out the kit's own files), quote the paragraph that governs sharing study products verbatim with its locator, and name the person or office it makes the arbiter. If no policy is on disk, build the builder anyway, and put this at the top of the reply: no policy was found, nothing about sharing was checked, and the user should read theirs before sending anything. Never tell the user sharing is allowed: say what the policy says and who decides.
3. The product, and every source it was built from. The leak scan is only as good as its source list, so find them all.

## Before you draft

1. **Assume it already failed** and write three reasons first. The usual ones: an acronym from the source survived in an example, a trap the author found is written in as a warning, and the prerequisite lets the peer's Claude build with no source attached.
2. **Ask only what changes the builder:** subject agnostic (works on any source of its kind, the strongest posture) or lightly subject flavored (the user's choice, still naming nothing), and whether the product is an interactive page, meaning an HTML file the student clicks through (then the self test is required; a drill file for a voice chat is not a page). Keep the photographs section unless the source can never be a picture. Unattended, choose agnostic and say so.

## Workflow

```
Share method:
- [ ] 1. Policy quoted with its locator; arbiter named
- [ ] 2. Product and every source located
- [ ] 3. Method inventory (references/method-inventory.md): method kept, content stripped, emphasis converted into categories
- [ ] 4. Builder written from references/builder-template.md
- [ ] 5. python3 scripts/builder_check.py <builder> [--app] exits 0
- [ ] 6. python3 scripts/leak_scan.py <builder> --source <every source> --product <the product> --terms <file> [--allow <file>] --report "<builder name> - leak scan.md" exits 0
- [ ] 7. source-fidelity-reviewer agent, mode 2, blind, with the builder and the sources
- [ ] 8. Peer run: a fresh agent given only the builder and a different source of the same kind builds a working product, and stops and asks when given no source
- [ ] 9. Save the builder and the scan report beside the product; name both paths
```

**The terms file.** Always write one: the source's subject words in lower case (option names, key nouns, units), the ones the scan's capitalization rules cannot see. One per line.

**Judging leak scan hits.** Every hit is shown with its line. A real hit is fixed by rewriting the line as a category or deleting it. A hit that is not a leak (a plain English word the source happens to use as a term, a number that is the builder's own, like a turn length) goes in an allow file as `term | reason`; the reason is required and shows in the report. A mention of browser automation is never allowed: the builder tells the peer to attach files, and says nothing about how anything was captured.

**The read once list.** The report lists every longer word the builder shares with the sources that the kit's own method text never uses, and every small number it shares with them. Read each in context: a subject word or a threshold that survived goes; an ordinary word stays.

**Judging emphasis and structure.** The scan sees words, not shape, so read the builder twice more. Once for any sentence that tells the peer where to look ("watch the", "most people miss", "the tricky one"); convert each into its category or cut it. Once for any list that mirrors the source's own structure (its fields, steps, or options, in its order, even in generic words); a list like that is the source's format in disguise, so replace it with the category ("every line, in the order printed").

## Reply

The builder's path, the scan report's path, the verdicts of steps 5 through 8, the posture (agnostic or flavored), and one line: share the builder file only; the product stays with the people who built it, and the peer's product is theirs under their own policy.

## Why it is built this way

- **Clean room design** separates the people who examine the original from the people who build, and passes only a functional specification between them, reviewed for protected material. The builder is that specification; the leak scan and the blind reviewer are the review; the peer run is the independent build.
- **Keyword matching in data loss prevention** matches whole words by default and lets a term be case sensitive, because partial matches drown the real hits. The scan matches whole words, treats an all capitals term as case sensitive, and lists substring matches separately as not leaks.
- **Document fingerprinting** (winnowing) catches copied passages after case, spacing, and punctuation are normalized, with a minimum run length that filters coincidence. The scan's copied run pass does the same with an eight word minimum, which catches a sentence the term list missed.
- **Anthropic's guidance on reducing hallucinations** is to restrict the model to the provided documents and to allow it to say it does not know. The prerequisite, the unreadable rule, and the gap rule in every builder are those two instructions.

## Scripts

- `scripts/leak_scan.py`: terms, values, copied runs, and mechanism mentions, every hit in context.
- `scripts/builder_check.py`: the safeguards, found by section.

Reads .md, .txt, .html, and .csv; .docx with python-docx; .pdf with pdftotext.
