import numpy as np
from scipy.optimize import brentq, minimize_scalar
from budget import geom, E, Rstar
dl = np.linspace(1/50, 5/6, 4001)[:, None]; xs = np.linspace(0, 0.5, 201)[None, :]
def maxE(ell, h):
    s0 = geom(ell, h)['s0']; R, _ = Rstar(dl, xs, 1/(6*(2*s0-1)))
    return E(h, dl, xs, R, ell, h).max()
def best_h(ell):
    r = minimize_scalar(lambda h: maxE(ell, h), bounds=(0.78, 0.85), method='bounded', options={'xatol':1e-7})
    return r.x, r.fun
h0, m0 = best_h(1/6); print(f"ell=1/6: optimal h={h0:.6f} (paper 13/16={13/16:.6f}), margin maxE*={m0:.3e}")
ell_edge = brentq(lambda l: best_h(l)[1], 1/6, 1/6+0.002, xtol=1e-9)
he, _ = best_h(ell_edge)
print(f"edge: ell={ell_edge:.7f} (1/6 + {ell_edge-1/6:.2e}), h={he:.6f}, sigma0 = 11/12 - ell/4 = {11/12-ell_edge/4:.7f}")
print(f"improvement over 7/8: {7/8-(11/12-ell_edge/4):.2e}")
# sensitivity: which (delta,x) bind at the edge
s0=geom(ell_edge,he)['s0']; R,t=Rstar(dl,xs,1/(6*(2*s0-1))); Es=E(he,dl,xs,R,ell_edge,he)
i=np.unravel_index(Es.argmax(),Es.shape); print(f"binding at delta={dl[i[0],0]:.4f}, x={xs[0,i[1]]:.3f}, R*={R[i]:.4f}, t={t[i]:.4f}")
# other constraints at the edge
from optimize import check
check(ell_edge, he, verbose=True)
