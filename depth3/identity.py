"""Symbolic check of the two algebraic identities behind the depth-three reserve
(iterating TwoLevelHigh/SecondLevel `joint_high_split` once more).

    python identity.py   ->  prints two zeros
"""
import sympy as sp

dl, q0, q1, TA, d0, d1, a1, a2, a3 = sp.symbols("delta q0 q1 TA d0 d1 a1 a2 a3")
rho = 1 - 10 * dl / (3 * (5 - 2 * dl))
cost = 5 - 6 * rho


def step_high(A, Mw, a):
    """secondHigh delta A M a = (1 - rho) M - delta A - a cost(delta)"""
    return (1 - rho) * Mw - dl * A - a * cost


# depth three reserve, as certified
high3 = (1 - rho) - dl * TA + (dl - q0) * d0 + (dl - q1) * d1 - (a1 + a2 + a3) * cost
# = HIGH reserve of the last step at the grandchild + the two LOW reserves after deletion
split3 = step_high(TA - d0 - d1, 1 - 6 * a1 - 6 * a2, a3) + (a1 - q0 * d0) + (a2 - q1 * d1)
print(sp.simplify(high3 - split3))

# the growth identity: high3(delta) - high3(q) = (delta - q)((50/3)(1-6 sum a)/((5-2delta)(5-2q)) - (TA - d0 - d1))
q = sp.Symbol("q")
h = sp.Lambda(dl, high3)
growth = (dl - q) * (sp.Rational(50, 3) * (1 - 6 * (a1 + a2 + a3)) / ((5 - 2 * dl) * (5 - 2 * q)) - (TA - d0 - d1))
print(sp.simplify(h(dl) - h(q) - growth))
