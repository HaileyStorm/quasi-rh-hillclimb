# Report D: LOW-child deletion into region 2, the second step, and supply/width (what a third level needs)

Notation. κ = 2·10499/12000 − 1. ρ(q) = 1 − 10q/(3(5−2q)). cost(q) = 5 − 6ρ(q). K(k,I,q) = q/(6(k−qI)). Rⱼ = (kⱼ,Iⱼ) is the region step j deletes into, and R_old = (κ,1).
- Two levels: R₁ = region(q₁, R_old).
- Three levels: R₃ = region(q₂, R_old) and R₁' = region(q₁, R₃).

Cell b ranges over [firstCellTop, s]. Every per-cell certificate is affine in b and is checked at the two ends of that range.

Values are mpmath runs of an earlier copy of `model.py`.
- PR67 constants: θ = 0.874817064.
- Three levels: q₀ = .638017, q₁ = .687932, q₂ = .717908, s = .0402308.
- Scripts: scratch scripts from the analysis session (not included).

## (a) Conditions

1. **Fixed deletion and child.** In `Optimization/TwoLevelHigh`, used at `LowChildTwoLevel.lean:290-299` as `hqdel`.
   - d₁(b) = (gap(k₁,I₁,λ,B,b) + 6I₁a₁)/(6k₁) and q₀·d₁ ≤ a₁ − lowReserve.
   - Child after deletion: A = B − (λ−1)b − d₁, z = b − d₁, M = 1 − 6a₁.
   - Three levels: the same formula with R₁'. The second step then needs its own d₂ = (g₂ + 6I₃a₂)/(6k₃) and the check q₁d₂ ≤ a₂ − lowRes₂.
2. **Second amplifier.** `secondAmp b` = K(κ,1,q₁)·childOvershoot(b) + lowRW. It is used with `ampSlack` = K(2ω+εpad) + K(1+6κ)/G (`LowChildTwoLevel.lean:327`, `two_level_amp_le`).
   - Three levels: a₂ = K(k₃,I₃,q₁)·g₂ + lowRW, with g₂ = A + (6k₃−1)z − I₃M.
   - a₃ = K(κ,1,q₂)·g₃ + lowRW, with g₃ = (A−d₂) + (6κ−1)(z−d₂) − (M−6a₂).
   - Values at the two cell ends: K₂ = 3.840, K₃ = 3.748 (two levels: 2.482); a₂ = .00365/.00317; a₃ = .00349/.00340.
3. **`TwoLevelCertificates`** (`LowChildTwoLevel.lean:118`, values in `TwoLevelCertificateValues`):
   - **`width`**: Mcap − 1 = 1/100 ≤ 6a₁(firstCellTop). Two levels .0261; three levels .0252. The second-step analogue is Mcap₂ − 1 ≤ 6·min a₂. With a cell-uniform a₂ this is .019; with amp(P) per grid position it is only 6e-8 (amp ≥ lowRW).
   - **`small`**: 2ω + εpad ≤ 9e-7. **`mesh`**: (λ−1)·cellMesh ≤ 1e-7, using λ ≤ 4. λ₁ = 3.734, but the second plane has slope 6k₁' = 4.093 > 4.
   - **`reflect` and `reflect_small`**: childOvershoot_old(b) + ω + εpad ≤ δR ≤ 7/2500. **`reflect_margin`**: δR + ξR ≤ (2/5)/100.
   - **`room`** (branch D): lowRes(R₁,q₀) + r₀(Mcap−1+εpad+2ω) ≤ min_b [r₀(1−6a₁−2M*) − (r₀(oldgap+6a₁) − a₁)], with r₀ = q₀/(6κ) and M* = 2/5. Three levels: .02438/.02033 against .00142 needed. The proof bounds r₀ ≤ 15/100; the second-level rate r₁ = q₁/(6κ) = .1529 exceeds that.
   - **`length`**: secondSlope/G ≤ gridSlack. **`amp`**: as in item 2.
4. **Branch L2** (`two_level_branch_L2`, `second_step_arithmetic_of_child`, `SecondStepArithmetic`): W = width ≥ 2/5; the grid position satisfies `Facts`; W·totalA(P) ≤ length; W·amp(P) ≤ amp; loss ≥ lossFloor; x₁ + x₂ + 6κz − W ≤ 7/2500. The last bound is (2/5)·7/1000, the old-moment comparison margin in `GeometryAffineStateComparison` (hover ≤ 1 + 7/1000).
5. **Branch D** (`two_level_branch_D`): nominal + δ < 2/5 and hprime, κ_q(g−t−V) ≤ (e−p) + κ_q((e−g)+t), which needs κ_q ≤ 1/2. The allowance (e − log rad) together with the cone surplus max(3c−5d−R,0)/6 pays r₀·max(oldgap + 6a₁ − Red, 0). In the label payment (`LowChildAllowancePayment`), Z^lowAllowance turns 1/N(E₂) into 1/N(rad), so the sum over second labels is a per-class count of Z^(p+exponent+…+ε)/N(seed₀).
   - Three levels: the second step needs its own branch D at rate r₁. Its room is r₁(1 − 2M₃* − gap'_old) + a₂'(1 − 12r₁), about .027, which is fine. It also needs the same allowance and count over third-level labels.
6. **Joint HIGH reserve and row-5 payment.** `highTwoAt`, `depth_two_returned_payment`, `lowReturnedFacts_two_level` with hnum at `LowChildFactsTwoLevel.lean:126`:
   - hnum: ω + ε + lossFloor + ¾(εpad + gridSlack) + 23/7·ampSlack < highTwoMargin − lowRes₁ + εwidth/2 + εold + εlabels/2 + lowRate·εpad.
   - The constant ¾ is the top HIGH bin, and 23/7 = cost(3/4).
   - The budget lemma hard-codes highTwoMargin ≥ 2e-8 and K ≤ 3; three levels have K = 3.84.
   - Weight Z^(q₀(d₁+mesh)) with (q − q₀)·target = 0, and bins δ ∈ [q₁, 3/4].
   - Growth condition (50/3)(1−6Σa)/(5−2q)² ≥ TA − Σd. Values .33 and .35.
7. **Rebase Z' = Z^W, W ∈ [2/5, Mcap]** (`SecondStepLedger`, `SecondStepReturnProof`):
   - Bwide ≥ 5/2·Bpun (20 = 5/2·8) and **Bwide ≤ 20** (hard-coded).
   - B − 130 ≥ 5/2·Bv, with Bv = 101/100 + 20 + δ + 1; Bnorm ≥ Mcap·B (190 ≥ 1.01·185.0).
   - τT/Mcap > 2g.τ; Mcap·εc ≤ εold; Mcap·(lossNeeded + εc) ≤ lossFloor ≤ 1e-9 (`secondStepLossFloor_le`); 5/2·Lslot ≤ secondStepMesh.
   - Three levels: every 5/2 becomes 1/(W₂W₃) ≤ 25/4. The mask becomes 50 > 20, the slot mesh needs ≤ (4/25)·mesh₃, and τ, B and εold compound the same way.
8. **Mesh and reserve** (`SecondStepMesh`, `SecondStepFirstLevel`, `CountAffine/Mesh.meshTwoLevel`, which copies the constants 101/100, 28, 28+20 and 1e-10):
   - mesh ≤ lowRW/4 < amplifierFloor/2; 128·μ₂ ≤ lowRes(P) ≥ 1e-10; 3δ_dict ≤ lowRW; secondStepOldLoss ≤ 1e-11.
   - Three-level LOW reserves: lowRes₂ = lowRW(1 − q₁I₃/k₃) = 4.18e-10 and lowRes₃ = 4.26e-10, both ≥ 1e-10.
9. **Supply** (`low_state_dispatch` and siblings): d ≥ Mcap + Bmask + margin (31 ≥ 30.01), w/d ≤ Rwidth, (3 + (3i+2)Z^τ)² ≤ (Z^d)^η. Three levels: d₃ must cover Mcap + 28 + Bwide₃, which is about 80.
10. **Hard-coded constants that become false.** childSlotCap ≤ .0681 (three levels: .06858). The budget's K ≤ 3. r₀ ≤ 15/100 at level 2. λ ≤ 4 at level 2.
11. **`TerminalLedger`.** The identity a − lowRate(g + 6a) = lowReserve uses κ and intercept 1. In R₃ it becomes a − (q/(6k₃))(g + 6I₃a). The third step can use the file unchanged.

## (b) Risks, most serious first

1. **The 7/2500 overshoot bound fails at three levels.** In three levels the first-step child's overshoot over the *old* region is .0029049 (b = firstCellTop) and .0026195 (b = s). That exceeds 7/2500 = .0028; at two levels it is .00216. So `reflect_small`, hcO7 and SecondStepArithmetic's x₁ + x₂ + 6κz − W ≤ 7/2500 fail if the second step keeps the old-moment comparison.
   - Fix: raise the second-step width floor to ≥ .4151. Room is still .0158 at M* = .416, against .0014 needed.
   - Alternatively, rewrite the comparison against R₃.
   - margins.py's "childOvershoot" is the overshoot over R₃ (.00095), which is the wrong quantity for this check.
2. **The second step is hard-wired to delete into the old region.** `secondLedger` sets price := κ and intercept := 1, and `secondFamily_deletesIntoOldRegion` is used in `SecondStepReturnProof:61`. The second step's LOW part is the old-region terminal machinery (`SecondLowProfile*`, `TerminalLedger`). At three levels the second step must carry the whole O/R/L3/D split and its certificates, uniformly over the grid ledgers `secondFamily G i`.
3. **Deletion and amplifier must be uniform in the cell, not per grid position.** If d₂ = d₂(P) and a₂ = amp(P) per position, positions P with small gap g₂ give d₂ ≈ 0. The third-level overshoot over the old region is then about .0029/(W₂W₃), which needs W₃ ≥ .57; branch D at level 2 needs M₃* ≲ .49. These are incompatible.
   - With a cell-uniform a₂(b) and d₂(b) (abs d₂ ≥ d₂(P), since g₂ ≤ g₂c − (1−I₃)r), the third-level overshoot is .00093, or .0058 normalised at width .16, which is under .007.
   - This forces a second-step family indexed by (P, W₂, b).
4. **Children inside R₃ cannot go straight to the third step.** With the Lean's cell-uniform bounds, skipping the second step gives a joint reserve of −.0115 and −.0100. These children must also take the uniform second step.
5. **Joint labels are pairs only.** `SecondStepHighCount.labels` are `NonzeroJointSourceLabel` (first-source label × second label), and `Pays` is hard-coded at `secondJunction` in `SecondStepBody`. Depth three needs triple labels, records paying at q₂, and the q₁(d₂ + mesh₂) weight added inside the second step. The Bool index is only the orientation.
6. **Width cap.** Mcap = 101/100 is hard-coded throughout (loss floor, caps, meshes), and so is Bwide ≤ 20.

## (c) The exact depth-three reserve (the same algebra as `joint_high_split`, applied twice)

highThreeAt(δ, b) = (1−ρ(δ)) − δ·TA(b) + (δ−q₀)·d₁ + (δ−q₁)·d₂ − (a₁ + a₂ + a₃)·cost(δ), for δ ∈ [q₂, 3/4].

- TA = B − (λ−1)(b − cellMesh).
- This equals thirdHigh(q₂, A−d₁−d₂, M−6a₂, a₃) + (a₂ − q₁d₂) + (a₁ − q₀d₁).

This is exactly margins.py `depth3`: 5.939e-8 and 5.645e-8. The two-level formula reproduces Lean's highTwoMargin (2.30e-8 and 2.10e-8).

The heuristic is correct if and only if all of the following hold:
- d₂ and a₂ are fixed by the cell b, as above.
- The growth condition (50/3)(1−6Σa)/(5−2q₂)² ≥ TA − d₁ − d₂ holds; it is .346/.337.
- highTwo is recomputed with a₂ over R₃: 5.86e-8 and 5.55e-8.

The budget also has to subtract lowRes₁ plus ¾(gridSlack₂ + gridSlack₃) + 23/7(ampSlack₂ + ampSlack₃), using K₂ = 3.84 and K₃ = 3.75, plus q₁·mesh₂. All of this is ≲ 2e-9.

Neither margins.py `depth3` nor `side` checks the old-region overshoot ≤ 7/2500·floor, which is risk 1.
