"""Search only: n-level chains with the H4 width-floor fix enforced as a constraint.

depth_scan.py checks the branch-D room only at the unconstrained optima, where it fails
for n >= 4. constrained4.py rescues n = 4 by holding q1 higher. This does the same for
any n: minimize the class bound over (q1, ..., q_{n-1}) subject to the room test of
certify_depth3.width_floor_room (room >= NEED), with q0 at the rate crossing and s at the
window top, as in solve_n.py. The certificate is certify_depth3.py.

    python constrained_n.py 5
"""
import sys
from fractions import Fraction as Q
from solve import crossing, argmin, rate, top_at, decimal_up, msqrt
from model import FIRST_CELL_TOP, Chain, OLD, KAPPA

NEED = Q(15, 10000)          # the threshold certify_depth3.width_floor_room checks
BIG = Q(1)


def room(qs, s):
    """Least branch-D room over the two cell corners, at the width floor the overshoot
    forces (same formulas as certify_depth3.width_floor_room)."""
    c = Chain(tuple(qs), s)
    cells = (FIRST_CELL_TOP, s)
    ov = []
    for b in cells:
        a, dl, _ = c.cascade(b)
        ov.append(OLD.overshoot(c.B - (c.lam - 1) * b - dl[0], b - dl[0], 1 - 6 * a[0]))
    W = max(Q(2, 5), max(ov) / Q(7, 1000) + Q(1, 1000))
    rooms = []
    for b in cells:
        a, dl, _ = c.cascade(b)
        r = c.q[0] / (6 * KAPPA)
        oldgap = c.B - 1 + (6 * KAPPA - c.lam) * b
        rooms.append(r * (1 - 6 * a[0] - 2 * W) - (r * (oldgap + 6 * a[0]) - a[0]))
    return min(rooms), max(ov), W


def penalized(qs, s):
    """Class bound if the room test passes, else 1 + shortfall (pushes back to feasible).
    The LOW-reserve floor is not enforced here (as a penalty it breaks the golden-section
    search); certify_depth3 checks it, and it fails at seven levels."""
    rm, _, _ = room(qs, s)
    th = Chain(tuple(qs), s).theta(msqrt)
    return th if rm >= NEED else BIG + (NEED - rm)


def solve(n, rounds=4, seed=None):
    s = FIRST_CELL_TOP
    qs = seed or [Q(638, 1000)] + [Q(69, 100) + Q(i, 100) * Q(3, n) for i in range(n - 1)]
    for it in range(rounds):
        for _ in range(3):
            for j in range(1, n):
                lo = qs[j - 1] + Q(1, 1000) if j > 1 else Q(66, 100)
                hi = qs[j + 1] - Q(1, 1000) if j < n - 1 else Q(749, 1000)
                qs[j] = argmin(lambda x: penalized(qs[:j] + [x] + qs[j + 1:], s), lo, hi)
        qs[0] = crossing(lambda q: rate(tuple([q] + qs[1:]), s), Q(3, 5), Q(17, 25))
        s = decimal_up(top_at(tuple(qs), s), 8)
        rm, ov, W = room(qs, s)
        th = Chain(tuple(qs), s).theta(msqrt)
        print(n, it, [float(x) for x in qs], float(s), f"theta={float(th):.10f}",
              f"room={float(rm):.4e} ov={float(ov):.4e} W={float(W):.4f}", flush=True)
    return qs, s


if __name__ == "__main__":
    n = int(sys.argv[1])
    # optional seed: comma-separated junctions, e.g. a shorter chain's result plus one more level
    seed = [Q(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else None
    qs, s = solve(n, seed=seed)
    print("RESULT", [str(x) for x in qs], str(s))
