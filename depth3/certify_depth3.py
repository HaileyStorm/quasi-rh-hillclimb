"""Exact certificate of the arithmetic of a three-level affine chain on top of tracker
PR #67 (GTimG/QuasiRiemannTracker, two-level-affine-20261019).

    python certify_depth3.py          # the three-level point (the new claim)
    python certify_depth3.py --pr67   # PR #67's own point, as a check of this port

All rational quantities are computed exactly (fractions.Fraction). Statements over a
range of bins are rational functions of the bin d; they are proved by exact real-root
counting (Sturm, via sympy) on the closed interval plus one exact sign evaluation.
The two quantities that involve square roots (the top-row bound and the window top)
are enclosed with outward-rounded rational interval arithmetic (interval.py).

This checks arithmetic only. What it does NOT check is listed in depth3/PROOF.md
(hypotheses H1-H5): the Lean structure that a third level needs.
"""
import sys
from fractions import Fraction as Q
import sympy as sp

import model as M
from model import Chain, FIRST_CELL_TOP, KAPPA, OLD, amp_ratio, cost, density
from interval import I, isqrt

d = sp.Symbol("d")
RESULTS = []


def check(name, ok, value=""):
    RESULTS.append((name, bool(ok), value))
    print(f"  [{'OK' if ok else 'FAIL'}] {name}" + (f"   {value}" if value != "" else ""))
    return ok


def fl(x, n=6):
    return f"{float(x):.{n}e}"


# ---------------------------------------------------------------- exact positivity on [a, b]
def _np(expr):
    e = sp.cancel(sp.together(sp.nsimplify(expr) if not isinstance(expr, sp.Expr) else expr))
    n, den = sp.fraction(e)
    return e, sp.Poly(n, d), sp.Poly(den, d)


def positive_on(expr, a, b, zero_at_a=False):
    """True iff expr(d) > 0 for all d in [a, b] (or in (a, b] with expr(a) = 0 when
    zero_at_a), proved by exact root counting."""
    a, b = sp.Rational(a.numerator, a.denominator), sp.Rational(b.numerator, b.denominator)
    if not isinstance(expr, sp.Expr):
        expr = sp.Rational(Q(expr).numerator, Q(expr).denominator)
    e, P, D = _np(expr)
    if P.is_zero:
        return False
    if D.count_roots(a, b) != 0:
        return False
    if zero_at_a:
        if P.eval(a) != 0:
            return False
        P = sp.Poly(sp.quo(P.as_expr(), d - a), d)
    if P.degree() > 0 and P.count_roots(a, b) != 0:
        return False
    if P.degree() == 0 and P.as_expr() == 0:
        return False
    mid = (a + b) / 2
    return e.subs(d, mid) > 0


def first_root(expr, a, b):
    e, P, _ = _np(expr)
    rts = [r for r in P.real_roots() if a <= r <= b]
    return min(rts) if rts else None


# ---------------------------------------------------------------- the checks
def certify(junctions, s, theta_claim, label):
    print(f"\n=== {label} ===")
    print("junctions:", ", ".join(f"q{i} = {q} = {float(q):.6f}" for i, q in enumerate(junctions)),
          f"  window top s = {s} = {float(s):.8f}")
    c = Chain(junctions, s)
    q0 = c.q[0]
    L = c.ledger
    lam, B, r = c.lam, c.B, c.r
    ft = FIRST_CELL_TOP
    n = c.n

    print("\n-- regions (step j deletes its LOW children into T_j; T_{n-1} is the old region)")
    for j in range(n):
        T = c.T[j]
        print(f"   T_{j}: price {float(T.price):.12f}, intercept {float(T.intercept):.12f}")
    check("junctions increase and stay below 3/4", all(c.q[i] < c.q[i + 1] for i in range(n - 1)) and c.q[-1] < Q(3, 4))
    check("q0 in [3/5, 17/25]; later junctions in [17/25, 18/25]",
          Q(3, 5) <= q0 <= Q(17, 25) and all(Q(17, 25) <= q <= Q(18, 25) for q in c.q[1:]))
    for j in range(n):
        T = c.T[j]
        check(f"step {j}: price of T_{j} <= slot price (rate gap, TwoLevelRate)", T.price <= KAPPA, fl(T.price, 9))
        check(f"step {j}: k - q I > 0 (amplifier ratio defined)", T.price - c.q[j] * T.intercept > 0)
        check(f"step {j}: amplifier cost 5 - 6 rho(q_j) > 0", cost(c.q[j]) > 0)
    lows = c.low_reserves()
    for j, v in enumerate(lows):
        check(f"step {j}: LOW reserve alpha(1 - q_j I_j/k_j) >= 1e-10", v >= Q(1, 10**10), fl(v, 3))

    print("\n-- first-step ledger (ChannelCertificates.lean, at the new region T_0)")
    W, Wp = L.weight(q0), L.plain_weight(q0, r)
    check("channel sum q + W + W' > 0", q0 + W + Wp > 0)
    fee = L.high_fee(q0, s)
    unm_s = L.unmarked_margin(q0, lam, B, s, d, s)
    root = first_root(unm_s, sp.Rational(31, 50), sp.Rational(3, 4))
    check("HIGH reserve alone reaches the fee below 3/4 (bin top exists)", root is not None)
    bin_top = M.decimal_up(Q(str(sp.N(root, 30))), 12)
    print(f"   bin top {float(bin_top):.12f}")
    check("q0 <= bin top", q0 <= bin_top)
    for b, bn in ((ft, "first cell"), (s, "top cell")):
        r1, r2 = L.rate_channel_parts(q0, lam, B, d, b)
        check(f"rate channel > fee on [q0, binTop] ({bn}, both branches of the common rate)",
              positive_on(r1 - fee, q0, bin_top) and positive_on(r2 - fee, q0, bin_top))
        check(f"linear channel > fee on [q0, binTop] ({bn})",
              positive_on(L.linear_channel(q0, lam, B, d, b) - fee, q0, bin_top))
        check(f"inverse channel > fee on [q0, binTop] ({bn})",
              positive_on(L.inverse_channel(q0, lam, B, r, d, b) - fee, q0, bin_top))
        check(f"capped channel > fee on [q0, binTop] ({bn})",
              positive_on(L.capped_channel(q0, lam, B, r, d, b) - fee, q0, bin_top))
        mix0 = L.mixed_channel(q0, lam, B, r, q0, b) - fee
        check(f"mixed channel = fee at the junction ({bn}, exact)", mix0 == 0)
        check(f"mixed channel > fee on (q0, binTop] ({bn})",
              positive_on(L.mixed_channel(q0, lam, B, r, d, b) - fee, q0, bin_top, zero_at_a=True))
        check(f"HIGH reserve alone > fee on [binTop, 3/4] ({bn})",
              positive_on(L.unmarked_margin(q0, lam, B, s, d, b), bin_top, Q(3, 4)))
        check(f"2 supplied width <= live frequency ({bn})", 2 * M.supplied(b) <= L.plane_freq(q0, lam, B, r, b))
    check("dominance: c(d)(1 - 6r) <= r(6 rho(d) - 1 - tail) on [q0, binTop]",
          positive_on(r * (6 * density(d) - 1 - M.TAIL) - M.cap_coefficient(d) * (1 - 6 * r), q0, bin_top)
          or positive_on(r * (6 * density(d) - 1 - M.TAIL) - M.cap_coefficient(d) * (1 - 6 * r), q0, bin_top, zero_at_a=True))
    check("half gain, inverse cap, plain cap > 0 on [q0, binTop]",
          positive_on(M.half_gain(d), q0, bin_top) and positive_on(M.inverse_cap(d), q0, bin_top)
          and positive_on(M.plain_cap(d), q0, bin_top))
    cr1, cr2 = M.common_rate_parts(d)
    check("2 capCoefficient < common rate on [q0, binTop]",
          positive_on(cr1 - 2 * M.cap_coefficient(d), q0, bin_top) and positive_on(cr2 - 2 * M.cap_coefficient(d), q0, bin_top))
    check("capCoefficient < 1/20 on [q0, binTop]", positive_on(Q(1, 20) - M.cap_coefficient(d), q0, bin_top))

    print("\n-- top row (TopRow.lean) and window top (WindowTangency.lean)")
    a2, a1, a0 = M.root_coeffs(lam, B)
    disc = M.root_disc(lam, B)
    check("plane slope lambda > 0", lam > 0, f"lambda = {float(lam):.12f}")
    print(f"   plane intercept B = {float(B):.12f}")
    check("rootA2 != 0 and discriminant > 0", a2 != 0 and disc > 0)
    lamI, BI = I(lam), I(B)
    ds = M.delta_star(lamI, BI, isqrt)
    check("delta* >= 0", ds.lo >= 0, repr(ds))
    th = M.theta_min(lamI, BI, isqrt)
    h = M.h_star(lamI, BI, isqrt)
    k2 = M.kappa2(lamI, BI, isqrt)
    check("kappa2 >= 0 (square term of the cleared margin)", k2.lo >= 0, repr(k2))
    check("cutoff denominator > 0 on [0, 3/4] (affine: both ends)",
          M.cutoff_den(lam, Q(0)) > 0 and M.cutoff_den(lam, Q(3, 4)) > 0)
    print(f"   class bound thetaMin in {th}   (width {float(th.hi - th.lo):.1e})")
    check(f"class bound <= claimed theta = {theta_claim} = {float(theta_claim):.9f}", th.hi <= theta_claim,
          f"room {fl(theta_claim - th.hi, 3)}")
    bt = M.balanced_top(lamI, BI, th, h, isqrt)
    check("balanced window top <= s (capped top-row line holds on the window)", bt.hi <= s,
          f"balancedTop {bt}, s - top >= {fl(s - bt.hi, 3)}")

    print("\n-- joint HIGH reserves of the nested steps (TwoLevelHigh.lean; depth >= 3 extrapolated, see PROOF.md)")
    out = {}
    for depth in range(2, n + 1):
        qd = c.q[depth - 1]
        v1, v2 = c.high_at(depth, qd, ft), c.high_at(depth, qd, s)
        out[depth] = min(v1, v2)
        check(f"depth {depth}: reserve at q_{depth-1}, first cell > 0", v1 > 0, fl(v1, 4))
        check(f"depth {depth}: reserve at q_{depth-1}, top cell > 0", v2 > 0, fl(v2, 4))
        g1, g2 = c.growth(depth, ft), c.growth(depth, s)
        check(f"depth {depth}: growth in the bin >= 0 at both cells (reserve rises from q_{depth-1} to 3/4)",
              g1 >= 0 and g2 >= 0, f"{float(g1):.4f}, {float(g2):.4f}")
        # affine in the cell: exact second difference (every map in the cascade is affine in b)
        f0, f1, f2 = (c.high_at(depth, qd, Q(x)) for x in (0, 1, 2))
        check(f"depth {depth}: reserve is affine in the cell (exact second difference = 0)", f0 - 2 * f1 + f2 == 0)
        asum = [sum(c.cascade(b)[0][:depth]) for b in (ft, s)]
        check(f"depth {depth}: total amplifier width <= 1/6", max(asum) <= Q(1, 6), f"{float(max(asum)):.5f}")
    return c, th, out


def indicators(c):
    """Quantities that the record bounds by hard-coded constants which a third level
    must re-bracket (hypothesis H4 in PROOF.md). Computed exactly; not pass/fail."""
    print("\n-- indicators for the retuned constants (H4; values, not checks)")
    ft, s = FIRST_CELL_TOP, c.s
    for b, bn in ((ft, "first cell"), (s, "top cell")):
        a, dl, g = c.cascade(b)
        A = c.B - (c.lam - 1) * b - dl[0]
        z = b - dl[0]
        Mw = 1 - 6 * a[0]
        print(f"   {bn}: overshoot of the step-1 child over the OLD region = {float(OLD.overshoot(A, z, Mw)):.6e}"
              f"   (record cap 7/2500 = 2.8e-3)")
        print(f"   {bn}: slot cap (b - d_0)/(2/5) = {float(z / Q(2, 5)):.6f}   (record cap 0.0681)")
        print(f"   {bn}: amplifiers a_j = {[f'{float(x):.6e}' for x in a]}, deletions d_j = {[f'{float(x):.6e}' for x in dl]}")
    for j in range(1, c.n):
        T = c.T[j]
        print(f"   step {j}: amplifier ratio K = {float(amp_ratio(T, c.q[j])):.4f} (record uses K <= 3);"
              f" rate q_{j}/(6 kappa) = {float(c.q[j] / (6 * KAPPA)):.4f} (record: <= 0.15 at level 2)")
    for j in range(c.n - 1):
        print(f"   slope of region T_{j}: 6 k_{j} = {float(6 * c.T[j].price):.4f} (record mesh bound uses <= 4)")
    print(f"   first-step plane slope lambda = {float(c.lam):.4f}")


def main():
    if "--pr67" in sys.argv:
        q = (Q(159503, 250000), Q(702651, 1000000))
        s = Q(1001263, 25000000)
        c, th, out = certify(q, s, Q(174963413, 200000000), "PR #67 (two levels), as a check of the port")
        print("\n   Lean (PR #67): class bound in [0.874817064464, 0.874817064465], highTwo 2.30e-8 / 2.10e-8")
        print(f"   here:          class bound in [{float(th.lo):.12f}, {float(th.hi):.12f}]")
    else:
        q = (Q(319009, 500000), Q(687933, 1000000), Q(179477, 250000))
        s = Q(4023081, 100000000)
        c, th, out = certify(q, s, Q(874812431, 10**9), "three affine levels")
        indicators(c)
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} checks OK" + ("" if not bad else f"; FAILED: {bad}"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
