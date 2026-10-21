import sys
from fractions import Fraction as Q
from solve import crossing, argmin, bound, rate, top_at, decimal_up
from model import FIRST_CELL_TOP, Chain
def solve(n, rounds=4):
    ft=FIRST_CELL_TOP
    qs=[Q(638,1000)]+[Q(69,100)+Q(i,100)*Q(3,n) for i in range(n-1)]
    qs=[qs[0]]+sorted(qs[1:])
    s=ft
    for it in range(rounds):
        for _ in range(3):
            for j in range(1,n):
                lo = qs[j-1]+Q(1,1000) if j>1 else Q(66,100)
                hi = qs[j+1]-Q(1,1000) if j<n-1 else Q(749,1000)
                qs[j]=argmin(lambda x: bound(tuple(qs[:j]+[x]+qs[j+1:]), s), lo, hi)
        qs[0]=crossing(lambda q: rate(tuple([q]+qs[1:]), s), Q(3,5), Q(17,25))
        s=decimal_up(top_at(tuple(qs), s), 8)
        print(n, it, [float(x) for x in qs], float(s), float(bound(tuple(qs), s)), flush=True)
    return qs, s
n=int(sys.argv[1]); qs,s=solve(n)
print("RESULT", [str(x) for x in qs], str(s))
