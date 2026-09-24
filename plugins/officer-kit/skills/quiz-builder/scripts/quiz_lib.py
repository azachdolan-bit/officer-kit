# -*- coding: utf-8 -*-
"""quiz-builder core: load a quiz spec, place answers, and check every rule a machine can check.
Content free. See ../references/spec.md for the spec and ../references/rules.md for the rules."""
import json, os, random, re, sys
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "study-guide", "scripts"))
from study_lib import norm, _found, pattern_fails  # shared with study-guide

Q_MAX, A_MAX = 120, 75
DEFAULT_TIMES = {"easy": 20, "medium": 20, "hard": 30}
NUM = re.compile(r"^\s*[-+]?\d[\d,]*(\.\d+)?\s*([A-Za-z%]+)?\s*$")

def load(path):
    return json.load(open(path, encoding="utf-8"))

def questions(spec):
    return [(d["name"], q) for d in spec["decks"] for q in d["questions"]]

def numeric_set(opts):
    """All options are numbers with the same unit: present them in ascending order (item writing
    guideline) and leave their position out of the balance."""
    m = [NUM.match(o) for o in opts]
    if not all(m): return False
    units = {(x.group(2) or "").lower() for x in m}
    return len(units) == 1

def num_value(o):
    return float(re.match(r"\s*([-+]?\d[\d,]*(?:\.\d+)?)", o).group(1).replace(",", ""))

def place(spec):
    """Seeded order for each deck that is balanced across the slots and passes every pattern check;
    distractors shuffled. Numeric option sets are sorted ascending and keep the slot their value
    falls in. Records the intended text first so the check can prove nothing moved."""
    rng = random.Random(spec.get("seed", 1))
    for d in spec["decks"]:
        qs = d["questions"]
        for q in qs:
            q["_intended"] = q["o"][q["a"]]
            if numeric_set(q["o"]):
                q["o"] = sorted(q["o"], key=num_value)
                q["a"] = q["o"].index(q["_intended"]); q["_numeric"] = True
        best = None
        for _ in range(5000):
            counts, seq, dead = Counter(), [], False
            for q in qs:
                if q.get("_numeric"):
                    seq.append(q["a"]); continue
                allowed = [x for x in range(len(q["o"])) if not seq or x != seq[-1]]
                if not allowed: dead = True; break
                low = min(counts[x] for x in allowed)
                pick = rng.choice([x for x in allowed if counts[x] <= low + 1])
                counts[pick] += 1; seq.append(pick)
            if dead: continue
            if not pattern_fails(seq):
                best = seq; break
        if best is None:
            raise SystemExit("PLACEMENT: no answer order for deck '%s' passes the pattern checks; add or reword questions" % d["name"])
        for q, pick in zip(qs, best):
            if q.get("_numeric"): continue
            wrong = [o for i, o in enumerate(q["o"]) if i != q["a"]]
            rng.shuffle(wrong)
            q["o"] = wrong[:pick] + [q["_intended"]] + wrong[pick:]
            q["a"] = pick
    return spec

def time_for(q, tmap=None, allowed=None):
    """The author's time, else the level's; a question whose stem and options run past 200 characters
    gets at least 30 seconds so reading time does not become the difficulty."""
    if q.get("time"): return q["time"]
    t = (tmap or DEFAULT_TIMES).get(q.get("d"), 20)
    if len(q.get("q", "")) + sum(len(x) for x in q.get("o", [])) > 200:
        t = max(t, 30)
    if allowed and t not in allowed:
        t = min((x for x in allowed if x >= t), default=max(allowed))
    return t

def check(spec, source_texts=None, allowed_times=None):
    """Returns (fails, warns). source_texts: list of source strings for the traceability rule."""
    fails, warns = [], []
    allowed = set(allowed_times or [5, 10, 20, 30, 60, 90, 120, 240])
    src = norm(" ".join(source_texts)) if source_texts else None
    seen = {}
    for deck, q in questions(spec):
        tag = "%s: %s" % (deck, q.get("q", "")[:50])
        o, stem = q.get("o", []), q.get("q", "")
        if not 2 <= len(o) <= 4: fails.append(tag + ": needs two to four options")
        if any(not str(x).strip() for x in o): fails.append(tag + ": an option is empty")
        if len(set(norm(x) for x in o)) != len(o): fails.append(tag + ": two options are the same")
        if len(stem) > Q_MAX: fails.append(tag + ": question is %d characters, limit %d" % (len(stem), Q_MAX))
        for x in o:
            if len(x) > A_MAX: fails.append(tag + ": option '%s...' is %d characters, limit %d" % (x[:25], len(x), A_MAX))
        if not isinstance(q.get("a"), int) or not 0 <= q["a"] < len(o):
            fails.append(tag + ": answer index out of range"); continue
        if "_intended" in q and o[q["a"]] != q["_intended"]:
            fails.append(tag + ": marked slot does not hold the intended answer after placement")
        if any(re.search(r"\b(all|none|both) of the above\b", x, re.I) for x in o):
            fails.append(tag + ": 'of the above' option; write a real distractor")
        if re.search(r"(?i:\bwhich\b)[^?]*\bnot\b|\bexcept\b", stem):
            fails.append(tag + ": negative stem in lower case; rephrase positively or write NOT or EXCEPT in capitals")
        if q.get("d") not in ("easy", "medium", "hard"): fails.append(tag + ": difficulty must be easy, medium, or hard")
        if not q.get("e"): fails.append(tag + ": no explanation for the host key")
        t = time_for(q, spec.get("time_by_difficulty", DEFAULT_TIMES), None) if not q.get("time") else q["time"]
        if t not in allowed: fails.append(tag + ": time %s is not one of %s" % (t, sorted(allowed)))
        if src is not None and not _found(q.get("src") or o[q["a"]], src):
            fails.append(tag + ": answer not found in the source; give 'src', the source phrase that proves it")
        k = norm(stem)
        if k in seen: fails.append(tag + ": duplicate of a question in " + seen[k])
        seen[k] = deck
    for d in spec["decks"]:
        dq = [q for q in d["questions"] if isinstance(q.get("a"), int) and 0 <= q["a"] < len(q.get("o", []))]
        for i, q in enumerate(dq):
            sw = {w for w in norm(q["q"]).split() if len(w) > 4}
            cw = {w for w in norm(q["o"][q["a"]]).split() if len(w) > 4}
            dw = {w for j, x in enumerate(q["o"]) if j != q["a"] for w in norm(x).split()}
            shared = (sw & cw) - dw
            if shared:
                warns.append("%s Q%d: only the correct option repeats a stem word (%s); a player can match words instead of knowing" % (d["name"], i + 1, ", ".join(sorted(shared))))
            ans = norm(q["o"][q["a"]])
            for j, p in enumerate(dq[:i]):
                if len(ans.split()) >= 3 and (ans in norm(p["q"]) or any(ans == norm(x) for x in p["o"])):
                    warns.append("%s Q%d: its answer already appeared on screen in Q%d" % (d["name"], i + 1, j + 1))
        qs = [q for q in d["questions"] if not q.get("_numeric") and isinstance(q.get("a"), int)]
        if len(qs) >= 4:
            pos = Counter(q["a"] for q in qs)
            width = max(len(q["o"]) for q in qs)
            span = max(pos.values()) - min(pos.get(i, 0) for i in range(width))
            if span > max(2, len(qs) // 8):
                fails.append("%s: answer positions unbalanced %s" % (d["name"], dict(sorted(pos.items()))))
            seq = [q["a"] for q in d["questions"] if isinstance(q.get("a"), int)]
            for pf in pattern_fails(seq):
                fails.append("%s: %s; a player can ride the pattern" % (d["name"], pf))
            longest = sum(1 for q in qs if len(q["o"][q["a"]]) > max(len(x) for i, x in enumerate(q["o"]) if i != q["a"]))
            if len(qs) >= 10 and longest / len(qs) > 0.4:
                fails.append("%s: the correct answer is the longest option in %d of %d questions; students learn to pick the longest" % (d["name"], longest, len(qs)))
        n = len(d["questions"])
        dd = Counter(q.get("d") for q in d["questions"])
        for lvl in ("easy", "hard"):
            if n >= 10 and not .10 <= dd.get(lvl, 0) / n <= .30:
                warns.append("%s: %s questions are %d of %d; target about 20 percent" % (d["name"], lvl, dd.get(lvl, 0), n))
        if n > 40: warns.append("%s: %d questions is long for one live session; split on a natural boundary" % (d["name"], n))
    return fails, warns
