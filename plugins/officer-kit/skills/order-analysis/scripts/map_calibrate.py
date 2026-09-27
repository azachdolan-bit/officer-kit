#!/usr/bin/env python3
"""Fit a map image to the grid from control points, and report whether the map can be measured.

Usage: python3 map_calibrate.py <points.json>
points.json: [{"px": [x, y], "grid": "TH 86000 77000"}, ...]  at least three, grid line crossings are best.

Prints the affine fit, the residual at every point, and meters per pixel separately east-west and
north-south. A scan whose axes differ by more than 2 percent is not square (printing, scanning, or a
photo at an angle): every distance measured on it carries that error, and any finding that turns on
less is not a finding. Plot the order's grids with the fit and check them against features you can see."""
import json, math, sys

def fit(points):
    import numpy as np
    E = np.array([[p["e"], p["n"], 1.0] for p in points])
    X = np.array([p["px"][0] for p in points]); Y = np.array([p["px"][1] for p in points])
    cx, *_ = np.linalg.lstsq(E, X, rcond=None); cy, *_ = np.linalg.lstsq(E, Y, rcond=None)
    res = [math.hypot(E[i] @ cx - X[i], E[i] @ cy - Y[i]) for i in range(len(points))]
    return cx, cy, res

def main(path):
    sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
    from grid_tool import parse
    pts = json.load(open(path))
    if len(pts) < 3: sys.exit("need at least three control points")
    for p in pts:
        g = parse(p["grid"]); p["e"], p["n"] = g["e"] / 1000.0, g["n"] / 1000.0
    cx, cy, res = fit(pts)
    px_e = math.hypot(cx[0], cy[0]); px_n = math.hypot(cx[1], cy[1])
    skew = abs(px_e - px_n) / ((px_e + px_n) / 2) * 100
    print("pixels per km: east-west %.1f, north-south %.1f (axes differ %.1f%%)" % (px_e, px_n, skew))
    for p, r in zip(pts, res): print("  %-18s residual %.1f px (%.0f m)" % (p["grid"], r, r / ((px_e + px_n) / 2) * 1000))
    print("x = %.4f*E + %.4f*N + %.2f ; y = %.4f*E + %.4f*N + %.2f (E, N in km)" % (cx[0], cx[1], cx[2], cy[0], cy[1], cy[2]))
    if skew > 2: print("NOT SQUARE: treat every map measurement as +/- %.0f percent" % skew)
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
