# Report A: second-step per-cell and per-position certificates, and what they become at depth three

Notation: κ = slotPrice = 0.749833 (old region, intercept 1). Rᵢ = (kᵢ, Iᵢ) is the region of step i. K(k,I,q) = q/(6(k − qI)). cost(q) = 5 − 6ρ(q). α = 1e-8. b runs over the cells [firstCellTop, slotTop].
- First step: a₁(b) = K(k₁,I₁,q₀)·gap₁(b) + α, with gap₁ = B − I₁ + (6k₁ − λ)b.
- d₁(b) = (gap₁ + 6I₁a₁)/(6k₁) (`fixedDeletion`).
- TA(b) = B − (λ−1)(b − mesh). The child's lengths are A = B − (λ−1)b − d₁, z = b − d₁, M = 1 − 6a₁.

At depth three, R₃ = region(q₂ over old), R₁ = region(q₁ over R₃), and the second step deletes into R₃. Its K₂ = K(k₃,I₃,q₁), and its overshoot is F₂ = A + (6k₃−1)z − I₃M.
- Then a₂ = K₂F₂ + α and d₂ = (F₂ + 6I₃a₂)/(6k₃).
- The grandchild is (A₂, z₂, M₂) = (A − d₂, z − d₂, M − 6a₂). Its overshoot over the old region is g₃ = A₂ + (6κ−1)z₂ − M₂ = **6(κ−k₃)z₂ − (1−I₃)M₂**, which is exact because the grandchild sits on R₃'s boundary.
- a₃ = K(κ,1,q₂)g₃ + α.

My recomputation matches PR #67: highTwo = 2.30e-8 / 2.10e-8.

Scripts: scratch scripts from the analysis session (not included; `certify_depth3.py` recomputes every number used in `PROOF.md`).

## (a) Conditions

Values are given as 2-level → 3-level, at (first cell, top).

1. **Depth-two HIGH margin.** `highTwoAt`, `highTwoMargin` (TwoLevelHigh.lean l.59-65, 164).
   - Formula: (1−ρ(δ)) − δ·TA + (δ−q₀)d₁ − (a₁+a₂)cost(δ), taken at δ = q₁.
   - Consumer: TwoLevelBudget requires it to be ≥ 2e-8 and above lowReserve + ~4e-9.
   - Values: 2.30e-8, 2.10e-8 → 5.86e-8, 5.55e-8 (with a₂ over R₃).
   - The formula is unchanged at depth three; only a₂ changes.
2. **Growth in the bin.** `highTwoGrowth` ≥ 0 (l.68): (50/3)(1−6(a₁+a₂))/(5−2q₁)² − (TA − d₁).
   - Values: 0.334, 0.326 → 0.327, 0.319.
   - Depth-three analogue: (50/3)(1−6Σa)/(5−2q₂)² − (TA − d₁ − t − d₂). Value about 0.34.
3. **Amplifier sum.** a₁ + a₂ ≤ 1/6 (l.181). Values 0.014 → 0.012. At depth three a₁+a₂+a₃ ≤ 0.016.
4. **Child overshoot positive.** `childOvershoot_pos` (TwoLevelSplit l.84): oldOvershoot(A, z, M) > 0.
   - Values: 2.16e-3, 1.95e-3.
   - At depth three the second step needs F₂ > 0: 9.5e-4, 8.3e-4. The third step needs g₃ > 0: 9.3e-4.
5. **Direct-deletion room.** `directDeletionRoom` (TwoLevelSplit l.35): r(1 − 6a₁ − 2W) − [r(oldGap(b) + 6a₁) − a₁], with r = q₀/(6κ) and W = 2/5.
   - Consumer: TwoLevelCertificates.room needs it ≥ lowReserve + r·(1/100 + pads) ≈ 1.42e-3.
   - Values: 0.0244, 0.0204 → 0.0244, 0.0203.
   - Analogue for the second step (normalized by M, rate q₁/(6κ), deficit uses the old gap F̂_old with â₂): 0.027–0.030 at W₃ = 2/5. The requirement is about 1.5e-3.
   - The deficit is worst as F₂ → 0, because r₂(1+6K₂) < K₂.
6. **Width floor `secondStepWidthFloor = 2/5`** (TwoLevelSplit l.21). It enters three places:
   - the slot cap (b−d₁)/W;
   - the direct room through 1 − 6a − 2W, so W must be < (1−6a)/2;
   - SecondLevelComparison through δ_R + ξ_R ≤ W/100.
7. **Reflection margin δ_R = 7/2500, ξ_R = 1/1000** (TwoLevelCertificates; SecondStepArithmetic). Requires childOvershoot + pads ≤ 7/2500 and δ+ξ ≤ (2/5)/100.
   - Value: 2.16e-3 → **2.905e-3 > 2.8e-3. This fails.** It needs δ_R ≈ 2.91e-3 with ξ ≤ 1.09e-3, which is tight against the 4e-3 limit.
   - Grandchild g₃ ≤ 1.95e-3 is fine.
8. **Slot cap bounds** 648/10000 ≤ (b−d₁)/W ≤ 681/10000 (`childSlotCap_le/ge`, Position l.267-283).
   - Values: 0.06797/0.06487 → **0.06858 > 0.0681. Hard-coded, must be re-bracketed.**
   - The third-step cap z₂/W₃ goes up to 0.0686 too, since d₂ → 0.
9. **Position rooms ≥ 1/1000** (`position_rooms`).
   - Formula: childReserve − c·a₂ − (1/50 + ⅔(1/4 − floor)) for c = 4 or 9/2, with floor = shortFloor or comparisonFloor/2. The zero room is childReserve − 6a₂ − (1/380 + 1/20).
   - childReserve = 1 − 6a₁ − TA + d₁.
   - 2-level minimum: zero room 0.00714 (top). 3-level second step minimum: 0.0143.
   - **Third-step analogue** (reserve M₂ − (TA−d₁−t−d₂), amplifier a₃, cap z₂/W₃), evaluated at the vertices t ∈ {0, F₂⁰}:
     - At t = 0: rooms OK, zero room 0.0029 / 0.0014.
     - At t = F₂⁰ (child barely outside R₃, or in R₃∖old): **zero room −0.0025 / −0.0033, exceptional rooms −0.0013.**
   - The exceptional failure is an artifact of the Lean pairing reserve-at-width-1 with cap-at-width-W. The exact per-width condition is concave in M, and its endpoint values are positive.
   - The zero room fails even exactly, at M = M₂: −0.0012 / −0.0005. A smaller `zeroSaving` (currently 1/20, hard-coded in SecondLevelLedger l.112; downstream uses look like they only need it positive) would rescue it: 1/50 is enough. This needs checking.
10. **`childPosition_facts` side hypotheses**: g ≤ 1e-6, ω ≤ 1e-6, s ≤ 1/100, gridSlack 1e-5. Hard-coded uses:
    - K₂ ≤ 3 (also in TwoLevelBudget: hK3, hcost K(1+6κ) ≤ 33/2);
    - 1 + 6κ − λ₂ ≤ 3/2;
    - λ₂ ≤ 5;
    - F ≤ 1/10.
    - At depth three, **K₂ = 3.840 and K₃ = 3.748, both > 3.** Every K ≤ 3 must become K ≤ 4.
    - λ₂ = 6k₁ = 4.0927 and λ₃ = 6k₃ = 4.2908. Both are fine.
11. **Grid.** Mesh 1/G with G ≥ 10¹² (TwoLevelBudget) and g ≤ 1e-6 (Position). `SecondIndex N` = grid points of (intercept, slotTop, windowBottom, sumBottom) whose `Facts` hold.
    - At depth three, the third step needs a family indexed by (SecondIndex, third-step grid). That is finite, so it is fine.
    - Its rounding errors are about 5e-12, far below the 5.6e-8 margins.
12. **`secondLedger` fields** (SecondLevelLedger l.98-216):
    - q₁ ≤ price;
    - 1 ≤ λ₂ ≤ 6·price;
    - lowReserveAt ≤ 1/50;
    - lowReserve ≥ 1e-10 (SecondLevelCell): 6.3e-10 → second step 4.2e-10, third step 4.3e-10;
    - errorReserve_edges: (pf − 1/2)·amp − oldGap/6 ≥ lowReserve, with pf = 3/4 and q/κ ≥ 3/4. With amp = K·(old gap) + α this reduces to K ≥ 2/3, true for any position.
13. **LocalReserves / Constants (first step).**
    - First-step error reserves with pf = 99/100: 1.0e-3 → 8.4e-4 (OK).
    - ρ(q₀) = 0.4289 ∈ [1/4, 23/50].
    - q₀/q₁/q₂ lie in the bracket intervals [3/5, 17/25] and [17/25, 18/25]. q₂ = 0.7179 is close to 0.72.

## (b) Risks, most serious first

1. **`DeletesIntoOldRegion` is structural.** `secondFamily_deletesIntoOldRegion` (SecondLevelCell l.16, proved by rfl rfl) feeds PaidMain, TerminalLedger.low_paid_excess_bound, LowChildDaughter, the GeometryMainLow* files, `low_reserve_old` and `lowRate_eq`.
   - At depth three the second ledger has price k₃ and intercept I₃, so all of these are lost.
   - The second step must instead run the first step's `IsTwoLevelFirstStep`/fixed-deletion machinery, per position, with a nested third family.
2. **The error-branch reserve fails at second-step positions near R₃'s boundary.** `errorReserve_edges` and `SecondPosition.oldGap` hard-code the old-region gap.
   - When amp = K₂F₂ + α but the old gap is F₂ + Δ(ζ), with Δ = 6(κ−k₃)ζ − (1−I₃) ≈ 2e-3, the reserve is negative for small F₂: −3.3e-4 at ζ = 0.028, −1.7e-3 at ζ = 0.0686.
   - Raising pf does not cure F₂ → 0. This needs an error-branch argument against the R₃ gap, or a new branch for small F₂.
3. **The depth-three joint count cannot use the Lean's per-cell decoupling.** Lean bounds a₂ ≤ secondAmp(b), a single per-cell cap.
   - At depth three, g₃ is anti-correlated with d₂ (formula above). A per-cell cap a₃ ≤ K₃·max g₃ (7.3e-3) combined with the zero-extraction d₂ gives highThree = **−1.16e-2**.
   - The certificate must couple d₂, a₂ and a₃ per second-step position.
4. The **third-step zero room fails** (item 9). Fixing it needs zeroSaving lowered, which I have not verified downstream.
5. **The reflection margin 7/2500 is exceeded** (2.905e-3). Retuning makes δ+ξ ≤ W/100 nearly tight at W = 2/5.
6. A **new case** is needed: a first-step child in R₃∖old goes straight to the third step, with a₂ = 0. Its joint row equals the t = F₂⁰ vertex (6.19e-8 / 5.86e-8), which is fine.
7. Further hard-coded constants to re-bracket: K ≤ 3, slot cap 681/10000, and the `SecondPosition` amp/oldGap fixed at (slotPrice, 1).
8. The joint HIGH count is over exactly two label sets (first-level LOW × second-level HIGH, DepthTwo*). Depth three needs three, and a skip pair (first × third).

## (c) Exact depth-three joint HIGH reserve

For a second-step position whose child is shorter than the zero-extraction child by t ∈ [0, F₂⁰(b)], the reserve is

h₃(δ; b, t) = (1−ρ(δ)) − δ·(TA − d₁ − t − d₂) − q₀d₁ − q₁d₂ − (a₁+a₂+a₃)·cost(δ),

where F₂ = F₂⁰ − t, a₂ = K₂F₂ + α, d₂ = (F₂ + 6I₃a₂)/(6k₃), and a₃ = K₃(6(κ−k₃)(z−d₂) − (1−I₃)(M−6a₂)) + α.

This expression is affine in (b, t). So it is certified at the 4 vertices at δ = q₂, together with the growth condition (item 2).

| | t = 0 | t = F₂⁰ |
|---|---|---|
| first cell | 5.939e-8 | 6.188e-8 |
| top | 5.645e-8 | 5.861e-8 |

margins.py `depth3` computes exactly the t = 0 column (5.94e-8, 5.64e-8). That column is the minimum, because h₃ rises with t at about +2.5e-9 per F₂⁰. So the heuristic number is correct, but only for a per-position coupled certificate. The Lean's per-cell decoupled form gives −1.16e-2 instead.

In the 3-level model, the depth-two margin is 5.55e-8, also comfortably above 2e-8.
