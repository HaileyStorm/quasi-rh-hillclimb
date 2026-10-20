"""Exponent budget of Part II (7/8 proof), generalized to free geometry (ell, h).
Derived relations from the paper:
  l_x = 1 + ell - h,  M + ell = 1  =>  b = 2h - 1 - 3 ell,  l_y = l_x + b = h - 2 ell
  low exponent  = l_x/2 + b/12  (Prop. probe-low);   C(s) = l_x/2 + s - 1 + h/6
  boundary sigma0 solves C(sigma0) = low  =>  sigma0 = 1 - h/6 + b/12 = 11/12 - ell/4
High exponent at d (Lemma high-bin, first line), a=(1+delta)/2, q = x delta:
  E(d) = a - sigma0 + h(z0-1/6) - a l_y - (1-a) ell - (delta/2-q) ell + d(R + delta/2 - z0)
Row counts (Prop. detector-counts) with plain capacity c_P = 1/(6 kappa0), kappa0 = 2 sigma0 - 1.
"""
from fractions import Fraction as Fr
import numpy as np

def geom(ell, h):
    b = 2*h - 1 - 3*ell; lx = 1 + ell - h; ly = h - 2*ell
    s0 = 11/12 - ell/4
    return dict(b=b, lx=lx, ly=ly, s0=s0)

def E(d, delta, x, R, ell, h, z0=17/50):
    g = geom(ell, h); a = (1+delta)/2; q = x*delta
    return a - g['s0'] + h*(z0-1/6) - a*g['ly'] - (1-a)*ell - (delta/2-q)*ell + d*(R + delta/2 - z0)

def Rstar(delta, x, cP, alpha=5/6):
    """balanced count: R_short(t) = L(t), with general plain capacity cP (paper: 2/9)."""
    D = 3 - x - 4*x*cP
    # R_short(t) = 1 - delta*[ (2-4x cP) x + (1-x) 2 x cP + (1-x)(2-4x cP) t ] / D
    A0 = ((2-4*x*cP)*x + (1-x)*2*x*cP) / D
    A1 = (1-x)*(2-4*x*cP) / D
    # L(t) = 1 - delta + (alpha-delta)(t-1)
    # solve 1 - delta*(A0 + A1 t) = 1 - delta + (alpha-delta)(t-1)
    # -> delta*(1 - A0 - A1 t) = (alpha-delta)(t-1)
    t = (delta*(1-A0) + (alpha-delta)) / (delta*A1 + (alpha-delta))
    t = np.clip(t, 1, 1.5)
    Rs = 1 - delta*(A0 + A1*t); Lt = 1 - delta + (alpha-delta)*(t-1)
    return np.maximum(Rs, Lt), t

if __name__ == "__main__":
    ell, h = 1/6, 13/16
    g = geom(ell, h); print("geometry check:", {k: round(v, 6) for k, v in g.items()}, " expect b=1/8 lx=17/48 ly=23/48 s0=7/8")
    # paper's closed forms at c_P = 2/9: R_short = 1 - delta + delta P_x (3/2 - t)/D_x
    dl = np.linspace(1/50, 5/6, 2001)[:, None]; xs = np.linspace(0, 0.5, 501)[None, :]
    R, t = Rstar(dl, xs, 2/9)
    Dx = 3 - 17*xs/9; Px = (2 - 8*xs/9)*(1 - xs); J = (5/6 - dl)*Dx + dl*Px
    tp = 1 + dl*Px/(2*J); Rp = 1 - dl + dl*Px/Dx*(1.5 - tp)
    print("R* matches paper closed form: max |diff| =", float(np.abs(R - Rp).max()))
    Es = E(h, dl, xs, R, ell, h)
    i = np.unravel_index(Es.argmax(), Es.shape)
    print(f"max E_* = {Es.max():.7f}  at delta={dl[i[0],0]:.4f} x={xs[0,i[1]]:.3f};  paper certificate: -E_* >= 49/440640 = {49/440640:.7f}")
    # floor, large-delta endpoint, intermediate d=1/2, small-row margin
    d0 = 1/50
    print("floor E(h):", E(h, d0, 0.5, 1, ell, h), " paper -7/1200 =", -7/1200)
    print("delta=alpha endpoint:", E(h, 5/6, 0.5, 1-5/6, ell, h), " paper -1/48-(5/6)/16 =", -1/48-5/96)
    dd = np.linspace(1/50, 5/6, 500); print("intermediate max E(1/2):", max(E(0.5, x, 0.5, 76/75-2*x/3, ell, h) for x in dd), " paper <= -49/14400 =", -49/14400)
    print("small-row margin:", h*(17/50-1/6) - g['ly']/2, " paper -79/800 =", -79/800)
