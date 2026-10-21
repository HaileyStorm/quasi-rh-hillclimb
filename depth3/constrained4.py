from fractions import Fraction as Q
from solve import crossing, argmin, bound, rate, top_at, decimal_up, msqrt
from model import FIRST_CELL_TOP, Chain, OLD
from depth_scan import room  # noqa: E402  (importing runs the scan table first)
NEED = Q(15, 10000)
def metrics(qs, s):
    c = Chain(tuple(qs), s)
    ov = []
    for b in (FIRST_CELL_TOP, s):
        a, d, g = c.cascade(b)
        ov.append(OLD.overshoot(c.B-(c.lam-1)*b-d[0], b-d[0], 1-6*a[0]))
    W = max(Q(2,5), max(ov)/Q(7,1000) + Q(1,1000))
    rm = min(room(c, W, b) for b in (FIRST_CELL_TOP, s))
    return float(c.theta(msqrt)), float(max(ov)), float(W), float(rm)
s = Q(201609,5000000)
for q1 in [Q(x,10**4) for x in (6808, 6830, 6850, 6870, 6890, 6910)]:
    qs = [Q(638021,10**6), q1, Q(702695,10**6), Q(725707,10**6)]
    for _ in range(2):
        qs[2] = argmin(lambda x: bound(tuple(qs[:2]+[x]+qs[3:]), s), q1+Q(1,1000), qs[3]-Q(1,1000))
        qs[3] = argmin(lambda x: bound(tuple(qs[:3]+[x]), s), qs[2]+Q(1,1000), Q(749,1000))
    qs[0] = crossing(lambda q: rate(tuple([q]+qs[1:]), s), Q(3,5), Q(17,25))
    s2 = decimal_up(top_at(tuple(qs), s), 8)
    print([float(x) for x in qs], float(s2), metrics(qs, s2), flush=True)
