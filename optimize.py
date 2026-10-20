import numpy as np
from budget import geom, E, Rstar
dl = np.linspace(1/50, 5/6, 321)[:, None]; xs = np.linspace(0, 0.5, 101)[None, :]
ts = np.linspace(1, 1.5, 201)

def capacities(cP):
    x = np.linspace(0, 0.5, 401)[:, None]; t = ts[None, :]
    D = 3 - x - 4*x*cP
    rs = (2*x*cP + (2-4*x*cP)*t - x) / D
    zM = (1 - rs.min())/2; m_min = (t - rs).min(); zP = cP*(1 - 2*m_min)
    return zM, zP, rs.min(), rs.max()

def check(ell, h, z0=17/50, verbose=False):
    g = geom(ell, h); s0 = g['s0']; cP = 1/(6*(2*s0-1))
    R, _ = Rstar(dl, xs, cP)
    c = {}
    c['adaptive maxE*'] = E(h, dl, xs, R, ell, h, z0).max()
    c['floor'] = E(h, 1/50, 0.5, 1, ell, h, z0)
    c['delta=alpha'] = E(h, 5/6, 0.5, 1/6, ell, h, z0)
    d = np.linspace(1/50, 5/6, 400)
    c['intermediate d=1/2'] = max(E(0.5, d, 0.5, 76/75-2*d/3, ell, h, z0))
    c['small rows'] = h*(z0-1/6) - g['ly']/2 + 2/100
    zM, zP, rmin, rmax = capacities(cP)
    c['supply: cap - ell/h'] = max(zM, zP) - ell/h
    c['r_* <= 1'] = rmax - 1 - 1e-12
    c['b > 0'] = -g['b']
    c['Y >= P^(11/6)'] = -(g['ly'] - ell - 11*g['b']/6)
    c['l_x > ell'] = -(g['lx'] - ell)
    ok = all(v < 0 for v in c.values())
    if verbose:
        print(f"ell={ell:.5f} h={h:.5f} -> sigma0={s0:.6f}  cP={cP:.4f}  caps zM={zM:.4f} zP={zP:.4f}")
        for k, v in c.items(): print(f"   {k:22s} {v:+.6f} {'OK' if v < 0 else 'FAIL'}")
    return ok, c

print("== paper's point"); check(1/6, 13/16, verbose=True)
H = np.linspace(0.70, 0.99, 117)
res = []
for ell in np.arange(1/6, 0.26, 0.002):
    feas = [h for h in H if check(ell, h)[0]]
    res.append((ell, feas[0] if feas else None, feas[-1] if feas else None))
good = [r for r in res if r[1] is not None]
best = max(good, key=lambda r: r[0])
print("== largest feasible ell:", round(best[0],5), " h range", best[1], best[2])
check(best[0], 0.5*(best[1]+best[2]), verbose=True)
nxt = best[0] + 0.002
print("== just beyond:")
hh = min(H, key=lambda h: max(check(nxt, h)[1].values()))
check(nxt, hh, verbose=True)
