# Nested affine levels: θ ≤ 0.874812431 (three levels), θ ≤ 0.874810187 (four levels) and θ ≤ 0.874809963 (seven levels), conditionally

**Status: conditional, not Lean-verified.** This is a proposal for the Lean tracker
([GTimG/QuasiRiemannTracker](https://github.com/GTimG/QuasiRiemannTracker)), whose record
is ArviFoxy's PR #67, 174963413/200000000 ≈ 0.874817065. Everything here builds on PR #67
and its chain of earlier submissions (Collet's affine step, Gao's balanced marked ledger,
Levy's weighted numerator, and the others listed in PR #67's `metadata.json`). The tracker
accepts only bounds whose full proof checks in Lean, so this does **not** set a record.

## Claim

> **Theorem (conditional).** Assume the structural hypotheses H1–H5 below. Then the
> all-moduli Dirichlet boundary of PR #67 holds at
>
>   **θ = 874812431/1000000000 = 0.874812431**,
>
> about 4.63·10⁻⁶ below the record.

The numbers are the class bound of a three-level chain, enclosed exactly:

| | record (PR #67, two levels) | this note (three levels) |
|---|---|---|
| junctions | q₀ = 0.638012, q₁ = 0.702651 | q₀ = 0.638018, q₁ = 0.687933, q₂ = 0.717908 |
| window top s | 0.04005052 | 0.04023081 |
| class bound | 0.874817064464461… | **0.874812430304221…** |
| claimed rational | 174963413/200000000 | 874812431/10⁹ |
| least depth-2 HIGH reserve | 2.10·10⁻⁸ | 5.55·10⁻⁸ |
| least depth-3 HIGH reserve | — | 5.64·10⁻⁸ |

The exact junctions are q₀ = 319009/500000, q₁ = 687933/1000000, q₂ = 179477/250000 and
s = 4023081/100000000.

## What the third level is

PR #67 deletes each LOW child of the first step by a width fixed by the parent cell, into
the region T₀ of a second affine step at q₁. That second step deletes into the old region.
A third level inserts one more step:

- step 2 runs at q₂ and deletes into the old region;
- step 1 runs at q₁ and deletes into T₁ = region(q₂ over old), not into the old region;
- step 0 (the first step) runs at q₀ on the plane of T₀ = region(q₁ over T₁).

`region(q over base)` is PR #67's `SecondLevel.regionSlope / regionIntercept / regionPrice`
with the old region (slotPrice, 1) replaced by an arbitrary base region (k, I): the states on
which a step at q that deletes into the base pays its LOW and HIGH reserves with one amplifier,
with margin 10⁻⁸. For base = old it is the Lean definition verbatim (`model.region_over`).

Because T₀ sits lower than PR #67's region (price 0.68212 against 0.69812), the first step's
plane gets a better slope and intercept, and the top-row class bound falls. That is the whole
source of the gain. The deeper steps only have to be paid for.

## Proof, given H1–H5

The bound is produced by the first-step top-row certificate (`TopRow.margin_hStar_lower`) at
the plane (λ, B) of the first-step ledger. As in PR #67, the proof needs three things.

**1. The first-step ledger keeps its fee in every bin and cell.** This is
`ChannelCertificates.lean`: the rate, linear, inverse and capped channels exceed the fee on
[q₀, binTop], the mixed channel equals the fee at q₀ and exceeds it above, the HIGH reserve
alone exceeds it on [binTop, 3/4], plus dominance of the root cutoff and the gain facts. All of
it is statements about rational functions of the bin d at the new region T₀.
**Certified exactly** (`certify_depth3.py`, section "first-step ledger").

**2. The top row and the window top.** δ* ≥ 0, κ₂ ≥ 0, a positive cutoff denominator on
[0, 3/4], class bound ≤ θ, and balanced window top ≤ s. **Certified** with outward-rounded
rational intervals (the only square roots in the argument).

**3. Every LOW child of the first step is paid.** This is where the depth matters.

- *LOW reserves.* At each step j, after the cell-fixed deletion the LOW reserve is
  α(1 − q_j I_j/k_j). PR #67's `low_reserve_cancel` and `first_low_reserve_eq` are written for
  a general region. **Certified ≥ 10⁻¹⁰** at all three steps (7.3·10⁻¹⁰, 4.2·10⁻¹⁰, 4.3·10⁻¹⁰).
- *Joint HIGH reserves.* The HIGH rows of step 1 are counted jointly with the labels of
  step 0, as in PR #67, and the HIGH rows of step 2 jointly with the labels of steps 0 and 1.
  Iterating `joint_high_split` once more gives the depth-three reserve

  highThree(δ, b) = (1 − ρ(δ)) − δ·TA(b) + (δ − q₀)·d₀(b) + (δ − q₁)·d₁(b) − (a₀ + a₁ + a₂)(b)·(5 − 6ρ(δ)),

  which equals the last step's HIGH reserve at the grandchild plus the two LOW reserves
  (`identity.py`, exact symbolic check). Here d₀, a₀ are PR #67's `fixedDeletion`,
  `firstAmp`; a₁ = K(T₁, q₁)·g₁ + α and d₁ = (g₁ + 6 I₁ a₁)/(6 k₁) are fixed by the cell b
  through the zero-extraction child's overshoot g₁ over T₁; a₂ = K(old, q₂)·g₂ + α.
  Every map is affine in b, so the reserve is affine in the cell, and
  highThree(δ) − highThree(q₂) = (δ − q₂)·[(50/3)(1 − 6Σa)/((5 − 2δ)(5 − 2q₂)) − (TA − d₀ − d₁)]
  (`identity.py`), so it suffices to check both window ends at δ = q₂ together with the growth
  term. **Certified:** depth-3 reserve ≥ 5.64·10⁻⁸, depth-2 reserve ≥ 5.55·10⁻⁸, growth
  terms ≥ 0.32, Σa ≤ 0.016 ≤ 1/6.
- *The rest of the LOW dispatch* (the O/R/L/D split, reflection, direct deletion, the
  per-position families, the counting) is hypothesis H1–H4.

The loss terms absorbed by the reserves (H5) are all ε-sized allowances, ≲ 2·10⁻⁹ in total
at PR #67's settings against a margin of 5.64·10⁻⁸ − LR₀ − LR₁ ≈ 5.5·10⁻⁸.

## Hypotheses (what Lean would still have to prove)

Each one is a generalization of a lemma that PR #67 proves at two levels. Line-level detail
is in `reports/` (four independent readings of PR #67's Lean, each of which first reproduced
PR #67's own margins exactly).

**H1. A step that deletes into a non-old region.** PR #67's generic step
`GeometryAffineAtStateStatement` requires `[DeletesIntoOldRegion]`, because the step's LOW
children are paid by the baseline moment, which holds only in the old region. Step 1 now
deletes into T₁, so it needs its own O/R/L3/D dispatch: PR #67's first-step machinery
(`IsTwoLevelFirstStep`, fixed deletion, row-5 payment) run once more, per second-step grid
position, with a nested family for step 2. The deletion d₁ and amplifier a₁ must be fixed by
the first-level cell b (not by each child's own position, which collapses the reserve to
−1.2·10⁻²); the family is then indexed by (position, width, cell).

**H2. Triple-label joint count.** `SecondStepHighCount`, `Pays` (pinned to `secondJunction`),
`Ret` and `depth_two_returned_sum` extended from label pairs to label triples, with a second
missing-radical coordinate, a 2B cap on X1₁ + X1₂, and the currently unused
`composite_prefix_fiber_card`. The zero-density estimate is still applied once, to the final
rows; its range δ ≤ 3/4 covers q₂ = 0.718. `secondJunction`, which plays two roles in 37
files, must be split.

**H3. Children between T₁ and the old region.** Children of step 0 that lie in T₁ but not in
the old region, or overshoot T₁ by less than about 4·10⁻⁴, fail `errorReserve_edges` with the
step-1 amplifier K·g + α. Proposed fix: floor that amplifier at
a₁ ≥ (g_old/6 + LR₁)/(pf − ½), paid from a depth-two slack of about 0.005–0.01. (Routing them
directly to step 2 is not safe under cell-uniform bounds: Report D finds a −0.0115 reserve.)

**H4. Re-bracketed constants.** Hard-coded caps in PR #67 that the new constants exceed. The
values are printed by `certify_depth3.py` (section "indicators"):

| quantity | value here | PR #67's cap | proposed |
|---|---|---|---|
| step-0 child's overshoot over the old region (+ pads) | 2.905·10⁻³ | δ_R = 7/2500 = 2.8·10⁻³ | δ_R ≈ 2.95·10⁻³ (needs δ_R + ξ_R ≤ 4·10⁻³; ~9·10⁻⁵ to spare), or width floor ≥ 0.4151 |
| third-step zero room | down to −7·10⁻⁵ | ≥ 0 | `zeroSaving` 1/20 → 1/50 (downstream effect unchecked) |
| slot cap (b − d₀)/(2/5) | 0.06858 | 0.0681 | re-bracket |
| amplifier ratios K₁, K₂ | 3.840, 3.748 | K ≤ 3 | K ≤ 4 |
| level-2 rate q₁/(6κ) | 0.1529 | ≤ 0.15 | re-bracket |
| region slopes 6k₀, 6k₁ | 4.093, 4.291 | λ ≤ 4 (mesh bound) | re-bracket |
| mask Bwide under two rebases | 5/2 compounds to 25/4 | ≤ 20 | ≈ 50; supply then needs d ≈ 80 |

**H5. Loss absorption.** The depth-three budget (the analogue of `TwoLevelBudget` and
`depth_two_returned_payment`): every allowance (κ, pad, mesh, price excess, ω, appearing up to
three times) fits under highThreeMargin − LR₀ − LR₁. All are arbitrary-ε quantities in PR #67.

None of H1–H5 should move the class bound, which depends only on the first step's plane. But
until they are written in Lean the theorem is conditional, and any of them could fail in a way
this note does not foresee.

## Update: four levels, θ ≤ 0.874810282 (same hypotheses)

Nesting one more step gives **θ ≤ 437405141/500000000 = 0.874810282**, another 2.15·10⁻⁶
below the three-level bound and 6.78·10⁻⁶ below the tracker record. It needs H1–H5 at depth
four; if H1 is written once as a recursive step (a step that deletes into the region of the
next step), depth four needs no new structure, only the deeper instance and larger H4 caps.

Point: q₀ = 31901/50000, q₁ = 687/1000, q₂ = 4419/6250, q₃ = 36399/50000, window top
s = 4031793/100000000. Class bound 0.8748102817…; `python certify_depth3.py --four`:
**65/65 checks**, including depth-2, 3 and 4 HIGH reserves ≥ 8·10⁻⁸.

**Why q₁ is not the unconstrained optimum.** Deeper chains push the step-0 child further over
the old region, so the reflection / old-moment margin of H4 needs a higher second-step width
floor W ≈ overshoot/(7/1000), which eats the branch-D direct-deletion room (it must stay
above ≈ 1.42·10⁻³). `depth_scan.py` shows the trade-off at the unconstrained optima:

| levels | class bound | overshoot over old | width floor | branch-D room |
|---|---|---|---|---|
| 2 (record) | 0.8748170645 | 2.16·10⁻³ | 0.400 | 0.0204 |
| 3 | 0.8748124303 | 2.90·10⁻³ | 0.416 | 0.0158 |
| 4 (unconstrained) | 0.8748100879 | 3.28·10⁻³ | 0.470 | 0.0004 ✗ |
| 5 (unconstrained) | 0.8748086741 | 3.51·10⁻³ | 0.503 | −0.0090 ✗ |
| 8 (unconstrained) | 0.8748065489 | 3.86·10⁻³ | 0.553 | −0.0231 ✗ |

Raising q₁ to 0.687 (`constrained4.py`) cuts the overshoot to 3.24·10⁻³ and restores a room
of 2.32·10⁻³, at a cost of 2·10⁻¹⁰ in the bound. Five or more levels would need a different
H4 fix (raising δ_R with a smaller ξ_R, or rewriting the comparison against the new region);
the bound would then approach ≈ 0.87480.

The room formula is our reading of `TwoLevelSplit.directDeletionRoom` (it reproduces the
record's 0.0204), so this check is evidence for H4's feasibility, not part of the proof.

## Update: constrained re-optimisation, θ ≤ 0.874810187 (four levels) and θ ≤ 0.874809963 (seven levels)

The four-level point above raised q₁ until the branch-D room was 2.32·10⁻³, but the
certifier's threshold is 1.5·10⁻³ (PROOF's own estimate of the requirement is ≈ 1.42·10⁻³).
`constrained_n.py` minimises the class bound directly with the certifier's constraints as
penalties (room ≥ 1.52·10⁻³, LOW reserves ≥ 1.15·10⁻¹⁰, HIGH reserves ≥ 10⁻⁹). Holding the
room at the threshold instead of above it lets deeper chains in: the reason five or more
levels looked infeasible was only that their *unconstrained* optima overshoot the room, and
re-optimising under the constraint costs much less than a level gains.

| levels | claimed θ | below PR #67 record | below four-level (0.874810282) | `certify_depth3.py` | room | max K | min LOW reserve |
|---|---|---|---|---|---|---|---|
| 4 (previous) | 0.874810282 | 6.78·10⁻⁶ | — | `--four` 65/65 | 2.32·10⁻³ | 5.74 | 2.8·10⁻¹⁰ |
| 4, tightened | **874810187/10⁹** | 6.88·10⁻⁶ | 9.5·10⁻⁸ | `--four-tight` 65/65 | 1.52·10⁻³ | 5.56 | 2.9·10⁻¹⁰ |
| 5 | 437405017/(5·10⁸) = 0.874810034 | 7.03·10⁻⁶ | 2.48·10⁻⁷ | `--five` 74/74 | 1.52·10⁻³ | 8.94 | 1.8·10⁻¹⁰ |
| 6 | 218702497/(2.5·10⁸) = 0.874809988 | 7.08·10⁻⁶ | 2.94·10⁻⁷ | `--six` 83/83 | 1.52·10⁻³ | 12.99 | 1.3·10⁻¹⁰ |
| 7 | **874809963/10⁹** | 7.10·10⁻⁶ | 3.19·10⁻⁷ | `--seven` 92/92 | 1.52·10⁻³ | 14.11 | 1.2·10⁻¹⁰ |

Points (q₀ = 31901/50000 in all; exact values in `certify_depth3.py`):

- 4, tightened: q = 0.685207 / 0.705852 / 0.727369, s = 2016033/50000000.
- 7: q = 0.69749 / 0.706412 / 0.714969 / 0.723575 / 0.732142 / 0.741078, s = 4033753/100000000.

**What changes in the hypotheses.**

- *Four levels, tightened* needs exactly the H1–H5 of the previous four-level point, and on
  every H4 indicator except the room it is at or inside that point's envelope (K 5.56 vs
  5.74, region slopes ≤ 4.353 vs 4.357, rates ≤ 0.1617 vs 0.1618, total amplifier 0.0166 vs
  0.0167). It is slightly outside on two: overshoot over old 3.256·10⁻³ vs 3.236·10⁻³ (the
  width floor absorbs it: that is what the room check measures) and slot cap 0.06886 vs
  0.06884 (both already above the record's 0.0681). The room is at the threshold
  (1.52·10⁻³ ≥ 1.5·10⁻³) instead of above it. **This is the safest of the new claims.**
- *Five to seven levels* need H1–H5 at that depth (one recursive step, as above) and larger
  H4 caps: the amplifier ratio K grows to 9–14 (record K ≤ 3; four levels already needed
  K ≤ 6), and the LOW reserves fall towards the 10⁻¹⁰ floor because the junctions bunch
  together. Region slopes reach 4.44.
- Past seven levels the gain per level is below 3·10⁻⁸ and the LOW reserves are the binding
  constraint; the constrained ceiling of this architecture looks like ≈ 0.87480995.

Reproduce: `python certify_depth3.py --four-tight` (and `--five`, `--six`, `--seven`); saved
outputs `certify_four_tight_output.txt` etc. The search is `python constrained_n.py N "[q1,...]" s`.

## What is checked here, and how

```
pip install sympy mpmath
python certify_depth3.py          # 56/56 checks, the three-level point (about 1 s)
python certify_depth3.py --four   # 65/65 checks, the four-level point
python certify_depth3.py --pr67   # 47/47 checks at PR #67's point, as a test of the port
python depth_scan.py              # bound and H4 indicators for 2-8 levels
python identity.py                # prints 0 0: the reserve split and growth identities
python solve.py three             # how the junctions were found (search only)
```

- `model.py` is a line-by-line port of PR #67's `Optimization/*.lean` (constants, channels,
  plane, top row, window tangency, `TwoLevelHigh`), generalized so the steps nest to any depth.
  At two levels it reproduces PR #67 exactly: junctions 0.638012 / 0.702651, window top
  0.04005052, class bound 0.874817064464461 (Lean encloses it in [0.874817064464,
  0.874817064465]), highTwo 2.30·10⁻⁸ / 2.10·10⁻⁸.
- `certify_depth3.py` proves every arithmetic condition listed in sections 1–3 exactly:
  rational arithmetic, exact real-root counting for statements over a range of bins, and
  outward-rounded rational intervals for the two square roots. Saved output:
  `certify_output.txt`, `certify_four_output.txt`, `certify_pr67_output.txt`, `depth_scan_output.txt`.
- `reports/` holds the four readings of PR #67's Lean (A: per-cell certificates; B: LOW
  dispatch; C: joint HIGH count; D: physical LOW child and second step) and their synthesis
  `DEPTH3_ANALYSIS.md`. They were run at a slightly earlier solution of the chain
  (q₀ = 0.638017, q₁ = 0.687932, s = 0.0402308); the certified point differs by about 10⁻⁶,
  and every margin quoted above was recomputed at the certified point.

AI assistance: the port, the certificate and the reports were produced with Claude.

## Next steps

1. Post this on the tracker as a proposal issue, crediting PR #67's chain of authors.
2. Or implement it: H1 first (it is most of the work), then H2–H5. Expect a change about the
   size of PR #67 (~128k lines), and a machine with at least 16 GB of RAM for the build.
