import numpy as np
from scipy.optimize import brentq, minimize_scalar
from budget import geom, E, Rstar
dl = np.linspace(1/50, 5/6, 1201)[:, None]; xs = np.linspace(0, 0.5, 101)[None, :]
def maxE(ell, h, alpha, capmult):
    s0 = geom(ell, h)['s0']; R, _ = Rstar(dl, xs, capmult/(6*(2*s0-1)), alpha)
    return E(h, dl, xs, R, ell, h).max()
def edge(alpha=5/6, capmult=1.0):
    f = lambda l: minimize_scalar(lambda h: maxE(l, h, alpha, capmult), bounds=(0.74, 0.9), method='bounded').fun
    if f(1/6) > 0: return None
    lo, hi = 1/6, 0.3
    if f(hi) < 0: return 11/12 - hi/4
    return 11/12 - brentq(f, lo, hi, xtol=1e-7)/4
print("baseline sigma0 edge:", round(edge(), 6))
print("\nIf the sixth-power amplification slope alpha (5/6 in the paper) were smaller:")
for a in [0.80, 0.75, 0.70, 0.65]: print(f"  alpha={a:.2f}: sigma0 = {edge(alpha=a):.4f}")
print("\nIf the plain-moment capacity (1-2m)/(6 kappa) were larger by a factor:")
for c in [1.25, 1.5, 2.0]: print(f"  x{c}: sigma0 = {edge(capmult=c):.4f}")
