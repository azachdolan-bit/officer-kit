#!/usr/bin/env python3
"""Grid and direction arithmetic for reading an order. Content free.

  python3 grid_tool.py extract <order.txt>             every grid with its paragraph and label, and every named
                                                       point given two different grids
  python3 grid_tool.py measure "TH 815 654" "TH 8150 6534"   distance, grid azimuth (degrees and mils), error budget
  python3 grid_tool.py dir NW                          a direction word in mils and degrees
  python3 grid_tool.py mils 5400                       mils to degrees and the nearest direction word

Grids are MGRS within one 100 km square: two letters, then an even count of digits (4, 6, 8, or 10),
spaced or not. A grid names a square, not a point: a 6 digit grid is a 100 m square, so its point is
the center and each axis is uncertain by half the square. Distances carry that error budget; a
finding that turns on less than the budget is not a finding. The circle is 6400 mils (MCTP 3-10E,
traverse 6400 mils); these are grid azimuths, not magnetic."""
import json, math, re, sys

GRID = re.compile(r"\b([A-HJ-NP-Z]{2})\s?(\d{2,5})\s?(\d{2,5})\b")
DIRS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
WORDS = {"NORTH": "N", "NORTHEAST": "NE", "EAST": "E", "SOUTHEAST": "SE", "SOUTH": "S", "SOUTHWEST": "SW",
         "WEST": "W", "NORTHWEST": "NW"}

def parse(g):
    """'TH 815 654' -> dict(square, e_m, n_m, res_m) with e/n at the center of the named square."""
    m = GRID.search(g.upper()) if isinstance(g, str) else None
    if not m:
        raise ValueError("not a grid: %r" % g)
    sq, e, n = m.groups()
    if len(e) != len(n):
        raise ValueError("easting and northing differ in precision: %r" % g)
    k = len(e)
    res = 10 ** (5 - k)
    return {"square": sq, "e": int(e) * res + res / 2, "n": int(n) * res + res / 2, "res": res, "text": m.group(0)}

def to_mils(deg):
    return deg * 6400.0 / 360.0

def to_deg(mils):
    return mils * 360.0 / 6400.0

def word_of(mils):
    return DIRS[int(((mils % 6400) + 200) // 400) % 16]

def dir_mils(word):
    w = WORDS.get(word.upper(), word.upper())
    if w not in DIRS:
        raise ValueError("not a direction word: %r" % word)
    return DIRS.index(w) * 400

def measure(a, b):
    A, B = parse(a), parse(b)
    if A["square"] != B["square"]:
        raise ValueError("different 100 km squares (%s, %s); measure on the map" % (A["square"], B["square"]))
    de, dn = B["e"] - A["e"], B["n"] - A["n"]
    dist = math.hypot(de, dn)
    az = math.degrees(math.atan2(de, dn)) % 360
    err = (A["res"] + B["res"]) / 2 * math.sqrt(2)  # worst case: each point anywhere in its square
    az_err = math.degrees(math.atan2(err, dist)) if dist else 180.0
    return {"from": A["text"], "to": B["text"], "distance_m": round(dist), "error_budget_m": round(err),
            "azimuth_deg": round(az, 1), "azimuth_mils": round(to_mils(az)), "azimuth_error_mils": round(to_mils(az_err)),
            "direction": word_of(to_mils(az))}

NAMED = re.compile(r"\b(Obj(?:ective)?\s+[A-Z0-9][\w-]*|SBF\s*\d+|NAI\s*[\d-]+|TAI\s*[\d-]+|LZ\s+\w+|TRP\s*\d+|BP\s*\w+|OP\s*\d+|"
                   r"(?:assault|attack)\s+position|ORP|LD|PB|AA|CP|CCP|release point|rally point|start point)\b", re.I)
LOC = re.compile(r"^\s*((?:\d+|[a-z]|\(\d+\)|\([a-z]\))[.)]?\s+[A-Z][^.:]{0,40})")

def extract(text):
    """Every grid with its paragraph and the words before it on its line. Grids outside the order's
    main 100 km square are marked, since a target number (AB 2001) reads like a grid."""
    rows, loc = [], "top"
    for line in text.splitlines():
        m = LOC.match(line)
        if m: loc = m.group(1).strip()[:40]
        elif re.match(r"^\s*[A-Z][\w ,/]*\b(table|matrix|annex|appendix|overlay)\b[.:]?\s*$", line, re.I): loc = line.strip()[:40]
        for g in GRID.finditer(line):
            if len(g.group(2)) != len(g.group(3)): continue
            before = line[:g.start()]
            names = NAMED.findall(before)
            rows.append({"grid": g.group(0), "square": g.group(1), "paragraph": loc, "approx": bool(re.search(r"approx|about|vicinity|IVO", before, re.I)),
                         "context": before.strip()[-50:], "name": (names[-1] if names else "").lower().replace("objective", "obj")})
    if rows:
        from collections import Counter
        main_sq = Counter(r["square"] for r in rows).most_common(1)[0][0]
        for r in rows: r["other_square"] = r["square"] != main_sq
    return rows

def candidates(rows):
    """The same named point given two grids. Each pair is measured; a pair inside the error budget is noted, not raised."""
    out, by = [], {}
    for r in rows:
        if r["name"] and not r["other_square"]:
            by.setdefault(re.sub(r"\s+", " ", r["name"]), []).append(r)
    for name, rs in by.items():
        seen = []
        for r in rs:
            for s_ in seen:
                if parse(s_["grid"])["e"] == parse(r["grid"])["e"] and parse(s_["grid"])["n"] == parse(r["grid"])["n"]:
                    break
            else:
                seen.append(r)
        for i in range(len(seen)):
            for j in range(i + 1, len(seen)):
                m = measure(seen[i]["grid"], seen[j]["grid"])
                out.append({"name": name, "a": seen[i], "b": seen[j], "apart_m": m["distance_m"], "budget_m": m["error_budget_m"],
                            "inside_budget": m["distance_m"] <= m["error_budget_m"]})
    return out

def main(argv):
    if len(argv) < 2: sys.exit(__doc__)
    cmd = argv[1]
    if cmd == "extract":
        rows = extract(open(argv[2], encoding="utf-8", errors="replace").read())
        for r in rows:
            print("%-16s | %-28s | %-14s | %s%s" % (r["grid"], r["paragraph"][:28], r["name"][:14], r["context"], "   [other square: a target number?]" if r["other_square"] else ""))
        print("%d grids" % len(rows))
        c = candidates(rows)
        if c: print("\nSame point, two grids:")
        for x in c:
            print("  %s: %s (%s) vs %s (%s), %d m apart, budget %d m%s" % (x["name"], x["a"]["grid"], x["a"]["paragraph"][:20], x["b"]["grid"], x["b"]["paragraph"][:20],
                  x["apart_m"], x["budget_m"], "  inside budget, not a finding" if x["inside_budget"] else ("  one is marked approximate: plot from the table, RFI only if it changes an action" if x["a"].get("approx") or x["b"].get("approx") else "  CANDIDATE")))
    elif cmd == "measure":
        print(json.dumps(measure(argv[2], argv[3]), indent=1))
    elif cmd == "dir":
        m = dir_mils(argv[2]); print("%s = %d mils = %.1f degrees" % (argv[2], m, to_deg(m)))
    elif cmd == "mils":
        m = float(argv[2]); print("%g mils = %.1f degrees, nearest %s (%d mils)" % (m, to_deg(m), word_of(m), dir_mils(word_of(m))))
    else:
        sys.exit(__doc__)

if __name__ == "__main__":
    main(sys.argv)
