"""Search (not a certificate): minimise the class bound of an n-level chain subject to the
checks that certify_depth3.py enforces and that the unconstrained optima of depth_scan.py
violate:
    branch-D direct-deletion room at the width floor >= NEED  (certifier: >= 1.5e-3)
    LOW reserve at every step >= 1.15e-10                   (certifier: >= 1e-10)
    joint HIGH reserves >= 1e-9
q0 is the rate crossing and s the decimal-up window top, as in solve.py.
    python constrained_search.py 5 "[0.6935,0.708,0.722,0.736]" 201661/5000000
    python constrained_search.py 6 "[0.6662,0.6822,0.6986,0.7153,0.7324]" 4039727/100000000 -1 7   # PR #68 framework
"""
import sys, ast
from fractions import Fraction as Q
from scipy.optimize import minimize
from solve import crossing, rate, top_at, decimal_up, msqrt
from model import FIRST_CELL_TOP as FT, Chain, OLD, KAPPA, amp_ratio

NEED = 1.52e-3   # set to -1 for the PR #68 framework (no room condition)
KCAP = 99        # PR #68 framework: 7 (its proved amplifierRatio cap)


def room(c, W, b):
    a, d, g = c.cascade(b)
    r = c.q[0] / (6 * KAPPA)
    oldgap = c.B - 1 + (6 * KAPPA - c.lam) * b
    return r * (1 - 6 * a[0] - 2 * W) - (r * (oldgap + 6 * a[0]) - a[0])


def metrics(qs, s):
    c = Chain(tuple(qs), s)
    ov = []
    for b in (FT, s):
        a, d, g = c.cascade(b)
        ov.append(OLD.overshoot(c.B - (c.lam - 1) * b - d[0], b - d[0], 1 - 6 * a[0]))
    W = max(Q(2, 5), max(ov) / Q(7, 1000) + Q(1, 1000))
    rm = min(room(c, W, b) for b in (FT, s))
    hs = min(c.high_at(k, c.q[k - 1], b) for b in (FT, s) for k in range(2, c.n + 1))
    return c, rm, hs, min(c.low_reserves())


def snap(x):
    return [Q(int(round(v * 1e6)), 10**6) for v in x]


def objective(x, s):
    free = snap(x)
    if any(free[i] >= free[i + 1] for i in range(len(free) - 1)) or free[-1] >= Q(749, 1000) or free[0] <= Q(64, 100):
        return 1.0
    q0 = crossing(lambda q: rate(tuple([q] + free), s), Q(3, 5), Q(17, 25))
    if q0 >= free[0]:
        return 1.0
    c, rm, hs, lows = metrics([q0] + free, s)
    K = max(float(amp_ratio(c.T[j], c.q[j])) for j in range(1, c.n))
    return (float(c.theta(msqrt)) + max(0, K - KCAP) * 1e-3 + max(0, NEED - float(rm)) * 1e-3
            + max(0, 1e-9 - float(hs)) * 10 + max(0, 1.15e-10 - float(lows)) * 1e4)


def complete(free, s):
    qs = [Q(638, 1000)] + list(free)
    for _ in range(2):
        qs[0] = crossing(lambda q: rate(tuple([q] + qs[1:]), s), Q(3, 5), Q(17, 25))
        s = decimal_up(top_at(tuple(qs), s), 8)
    return qs, s


if __name__ == "__main__":
    n = int(sys.argv[1]); x0 = ast.literal_eval(sys.argv[2]); s = Q(sys.argv[3])
    if len(sys.argv) > 4: NEED = float(sys.argv[4])
    if len(sys.argv) > 5: KCAP = float(sys.argv[5])
    assert len(x0) == n - 1
    for rnd in range(6):
        r = minimize(lambda x: objective(x, s), x0, method="Nelder-Mead",
                     options=dict(xatol=1e-6, fatol=1e-14, maxiter=4000, adaptive=True))
        x0 = list(r.x)
        qs, s = complete(snap(x0), s)
        c, rm, hs, lows = metrics(qs, s)
        K = max(float(amp_ratio(c.T[j], c.q[j])) for j in range(1, c.n))
        print(rnd, [str(v) for v in qs], s, f"theta={float(c.theta(msqrt)):.13f} room={float(rm):.4e} "
              f"high={float(hs):.3e} low={float(lows):.3e} Kmax={K:.3f}", flush=True)
