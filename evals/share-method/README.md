# share-method tests

Every file here is fictional and exists only for the harness (`evals/share_method_check.py`, 29 items). `source.md` is a made up report handout, `product.md` a made up drill file built from it, `peer-source.md` a different made up handout for the peer run. `good-builder.md` must pass both scripts; `bad-builder.md` must fail on each planted defect (an acronym, a name, two values, a copied sentence, a trap pointed at, browser automation, a missing prerequisite). `fp-terms.txt` holds three short terms that sit inside ordinary words, to prove whole word matching.

## Blind test (27 Sep 26)

1. **Drafter.** A fresh agent with only the skill, the product, and its source built a builder. Both scripts passed on the first pass. It then found one leak by reading that no scan can see: a parenthetical list that was the source's lines in their order, in generic words. The skill now reads every builder for a list that mirrors the source's structure, and the scan lists lower case subject words and small numbers for one read, which the drafter named as its blind spots.
2. **Zero content review.** The `source-fidelity-reviewer` in mode 2 passed the builder: no term, value, structure, or trap from the source.
3. **Peer run.** A fresh agent with only the builder and a different handout built a drill file: 22 of 22 reps re-derived with 0 failures, every option covered, and eight places the handout does not settle named at delivery rather than filled. It asked for a read back step that the builder only gave photo sources and hit a conflict between covering every option and never inventing a rule; the template now limits the read back instruction to photos, says the source wins, and has the builder list every silent or ambiguous rule before inventing values.
4. **No source.** Given only the builder and a request for "the report we learned this week", the peer's Claude built nothing and asked for the handout.

## Against the user's own builders

The scan was run, on the author's machine, against three builders the author had already audited by hand, with the author's own products as the comparison set (none of it included here). The two subject agnostic builders, which the hand audit had passed, came back with one generic acronym between them and only method wording shared with the products. The subject specific builder, which the hand audit had passed with one arguable item, came back with five hits naming its subject: the scan made the arguable item concrete, and the author decides whether a subject flavored builder is acceptable.
