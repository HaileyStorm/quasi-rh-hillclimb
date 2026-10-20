"""Track B: how far would sigma0 move if one input of the Part II budget improved?

Numerical (floating point) -- it finds the feasibility edge of the budget, it proves nothing.
Knobs (paper values in brackets):
  --alpha  sixth-power amplification slope          [5/6]
  --cap    multiplier on the plain capacity 2/9      [1.0]
  --floor  detector floor delta0 (Re s = (1+d0)/2)   [1/50]
  --z0     contour Re z                              [17/50]
Example:  python auto-research/whatif.py --alpha 0.75 --cap 1.5
"""
import argparse, os, sys
import numpy as np
from scipy.optimize import minimize_scalar
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from budget import geom, E, Rstar

ap = argparse.ArgumentParser()
ap.add_argument("--alpha", type=float, default=5/6)
ap.add_argument("--cap", type=float, default=1.0)
ap.add_argument("--floor", type=float, default=1/50)
ap.add_argument("--z0", type=float, default=17/50)
ap.add_argument("--grid", type=int, default=1201)
a = ap.parse_args()

dl = np.linspace(0, a.alpha, a.grid)[:, None]; xs = np.linspace(0, 0.5, 101)[None, :]
R, _ = Rstar(dl, xs, a.cap * 2/9, a.alpha)
dd = np.linspace(a.floor, a.alpha, 400)

def worst(ell, h):
    """max over all budget constraints; feasible iff < 0."""
    g = geom(ell, h)
    c = [
        E(h, dl, xs, R, ell, h, a.z0).max(),                               # adaptive endpoint
        E(h, a.floor, 0.5, 1.0, ell, h, a.z0),                             # floor bin (no witness, R=1)
        E(h, a.alpha, 0.5, 1 - a.alpha, ell, h, a.z0),                     # delta = alpha endpoint
        max(E(0.5, dd, 0.5, 76/75 - 2*dd/3, ell, h, a.z0)),                # intermediate d = 1/2
        h*(a.z0 - 1/6) - g["ly"]/2 + 2/100,                                # small rows
        -g["b"],                                                           # b > 0
        -(g["ly"] - ell - 11*g["b"]/6),                                    # low-side length
        7/37 - ell/h,                                                      # prime supply
        h - 5*ell,                                                         # extension room
    ]
    return max(c)

def best(ell):
    r = minimize_scalar(lambda h: worst(ell, h), bounds=(0.6, 0.99), method="bounded", options={"xatol": 1e-8})
    return r.x, r.fun

feas = [l for l in np.arange(0.12, 0.33, 0.005) if best(l)[1] < 0]
if not feas:
    sys.exit("no feasible ell in [0.12, 0.33] with these knobs")
lo, hi = feas[-1], 0.33
for _ in range(60):
    mid = (lo + hi) / 2
    (lo, hi) = (mid, hi) if best(mid)[1] < 0 else (lo, mid)
h, _ = best(lo)
print(f"knobs: alpha={a.alpha:.4f} cap x{a.cap:.3f} floor={a.floor:.4f} z0={a.z0:.4f}")
print(f"edge: ell = {lo:.7f}  h = {h:.6f}  ->  sigma0 = 11/12 - ell/4 = {11/12 - lo/4:.7f}"
      f"  ({'below' if 11/12 - lo/4 < 7/8 else 'above'} 7/8 by {abs(7/8 - (11/12 - lo/4)):.3e})")
