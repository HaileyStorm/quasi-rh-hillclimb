from fractions import Fraction as Q
from model import Chain, FIRST_CELL_TOP, KAPPA, OLD
from solve import msqrt
PTS = {
 2: ((Q(159503,250000),Q(702651,10**6)), Q(1001263,25000000)),
 3: ((Q(319009,500000),Q(687933,10**6),Q(179477,250000)), Q(4023081,10**8)),
 4: ((Q(638021,10**6),Q(170187,250000),Q(140539,200000),Q(725707,10**6)), Q(201609,5000000)),
 5: ((Q(319011,500000),Q(338207,500000),Q(693689,10**6),Q(355841,500000),Q(182599,250000)), Q(4037663,10**8)),
 6: ((Q(638023,10**6),Q(673383,10**6),Q(11,16),Q(702227,10**6),Q(717551,10**6),Q(146687,200000)), Q(808263,20000000)),
 8: ((Q(25521,40000),Q(669447,10**6),Q(679457,10**6),Q(689971,10**6),Q(701021,10**6),Q(356297,500000),Q(4529,6250),Q(737081,10**6)), Q(2022929,50000000)),
}
def room(c, W, b):
    a, d, g = c.cascade(b)
    q0 = c.q[0]; r = q0/(6*KAPPA)
    oldgap = c.B - 1 + (6*KAPPA - c.lam)*b
    return r*(1 - 6*a[0] - 2*W) - (r*(oldgap + 6*a[0]) - a[0])
for n,(q,s) in PTS.items():
    c = Chain(q, s)
    th = float(c.theta(msqrt))
    ov = []
    for b in (FIRST_CELL_TOP, s):
        a, d, g = c.cascade(b)
        A = c.B - (c.lam-1)*b - d[0]; z = b - d[0]; M = 1 - 6*a[0]
        ov.append(OLD.overshoot(A, z, M))
    W = max(Q(2,5), max(ov)/Q(7,1000) + Q(1,1000))   # width floor that restores the 7/2500-at-2/5 margin
    rm = min(room(c, W, b) for b in (FIRST_CELL_TOP, s))
    hs = [min(c.high_at(k, c.q[k-1], b) for b in (FIRST_CELL_TOP, s)) for k in range(2, n+1)]
    print(f"n={n}  theta={th:.10f}  maxOvershootOld={float(max(ov)):.3e}  widthFloor={float(W):.4f}  roomD(W)={float(rm):.4f}  "
          f"minHigh={float(min(hs)):.2e}  qlast={float(q[-1]):.4f}")
