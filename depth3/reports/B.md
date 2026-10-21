# Report B: LOW-branch dispatch (O/R/L2/D) and the second step, extended to three levels

The numbers come from scratch scripts of the analysis session (not included), built on an earlier copy of `model.py`. "3L" means the solved chain q0=.638017, q1=.687932, q2=.717908, s=.0402308. The regions are k2=.68212, I2=.99155 (step-1 target), k3=.71514, I3=.99615 and κ=.749833. Cells are evaluated at b ∈ {firstCellTop, s}. ρ(q) = 1 − 10q/(3(5−2q)), cost(q) = 5 − 6ρ(q), and K(k,I,q) = q/(6(k − qI)).

## (a) Conditions

1. **Fixed deletion pays** (TwoLevelBridge `fixedDel_pays`; Dispatch hyp `q*del ≤ amp − reserve`). With d = (gap + 6·I·a)/(6k): q·d = a − α(1 − qI/k). This holds for any AffineLedger, so it is depth-generic. 3L step 2: d2 = (g2 + 6·I3·a2)/(6k3) and LR2 = α(1 − q1·I3/k3) = 4.18e-10.
2. **Old-region test O, reflection test R** (Dispatch `OldRegionTest`, `ReflectionTest`). O: x1 + x2 + 6κ(zJ − del) ≤ W. R: overshoot ≤ δR, and a reflected factor leaves margin δR. Both are always against the **old** region (κ, intercept 1), because O and R consume the baseline moment (`original_incumbent`, `remaining_energy_bound`). 3L: the same tests are used at step 1 and again at step 2.
3. **Reflection margin** (TwoLevelCertificates `reflect`, `reflect_margin`, `reflect_small`; SecondStepOfChild `hcO`; SecondLevelFamily `SecondStepArithmetic` last clause; SecondLevelComparison). Conditions: childOvershoot_old(b) + ωmax + εpad ≤ δR = 7/2500, δR + ξR ≤ (1/100)(2/5), ξR = 1/1000. Here childOvershoot_old(b) = (A0 − d1) + (6κ − 1)(b − d1) − (1 − 6a1).
   - PR67: max is 2.157e-3 ≤ 2.8e-3 (Lean enclosure ≤ 2.3e-3).
   - **3L step 1: 2.905e-3 > 2.8e-3. This fails.** It is the overshoot over the OLD region, not over region 3 (margins.py `side` reports 9.5e-4 over region 3). The fix is to raise the hard-coded 7/2500 (it appears in 6 files) toward 3e-3 − pads. The ceiling is δR ≤ .004 − ξR. The slack left is about 9e-5.
   - 3L step 2 (its children after d2): overshoot over old is .00093 at zero extraction but up to about .0019 for other children. This is OK.
4. **Width floor / wide test** (`secondStepWidthFloor = 2/5`; hW2, hδR2 2δR ≤ ν + δ). The same 2/5 is needed at step 2 for its step-3 children (in step-2 units).
5. **Direct room, branch D** (TwoLevelSplit `directDeletionRoom`; certificate `room`). With rate r = q0/(6κ): r(1 − 6a1 − 2·(2/5)) − (r(g_old + 6a1) − a1) ≥ LR1 + r((Mcap − 1) + εpad + 2ωmax).
   - PR67: min room .02043 against .00142.
   - 3L step 1: .02033. 3L step 2, with rate q1/(6κ) in step-2 units: about .0259. Both pass.
6. **Width slack** (`width`): Mcap − 1 = 1/100 ≤ 6·a1(firstCellTop). PR67 .0261; 3L .0252. **Step-2 analogue:** a2 is the per-child grid-position amp, whose only floor is α = 1e-8, so a width slack δ ≤ 6·a2 cannot be uniform (`hWu : ν + δ ≤ 1`).
7. **Rate gap** (TwoLevelRate `rate_lt_lowRate`): q/(6κ) < q/(6·price), i.e. price < κ. 3L: k2 = .682 and k3 = .715 are both below .7498, so this passes. The reflection loss is (q/6)(1/k − 1/κ)·εpad·Mmin.
8. **Step-2 position Facts** (SecondLevelLedger `Facts`): zero is amp + 1/380 + 1/20 ≤ 1 − totalA − 5·amp. fixedInducing and exceptional each need ≥ 1/50 + (2/3)·plc. Also needed: oldGap_pos and comparison_room. These are in child units: totalA = A/M, amp = a/M.
   - PR67 step 2: zero slack .0099.
   - 3L step 2: .0204. 3L step 3 at zero extraction: .0056. **3L step 3 minimum over children: −7e-5. This fails** for step-1 children near the region-3 boundary (g2 ≈ 0, full slot), where a3/M reaches .0073.
9. **errorReserve_edges** (AffineLedger field; SecondLevelLedger proof): LR ≤ (pf − ½)·amp − g_old/6, with pf = 3/4. Today g_old equals the region gap, so this is automatic because K/4 > 1/6.
   - 3L step-2 ledger: amp = K(k3, I3, q1)·g2 + α with K = 3.84, but g_old = g2 + Δ, Δ ≈ .0019. It **fails for g2 ≲ 4e-4** (pf = 3/4), or g2 ≲ 1.9e-4 with pf = .99.
   - The step-1 LR is in the error reserves: proved via q/κ ≥ 3/4. 3L ratios: .958 and .957, so this passes.
10. **Second-ledger reserves** (SecondLevelCell `secondFamily_lowReserve_ge` ≥ 1e-10; SecondStepReturnProof `hres` 128·μ ≤ LR). PR67 6.29e-10. 3L: step 2 4.18e-10, step 3 4.26e-10. Both pass.
11. **Amplifier of the parent of step 2** (`childPosition_amp_le`, `two_level_amp_le`, cert `amp`): a ≤ K(κ, 1, q1)·(n1 + n2 + 6κζ − 1 + (1 + 6κ)g) + α. This is hard-coded to the old region. 3L step 2 needs K(k3, I3, q1)·(n1 + n2 + 6k3ζ − I3 + (1 + 6k3)g) + α.
12. **Budget** (TwoLevelBudget): ωmax + ε + lossFloor + ¾(εpad + λ2/G) + (23/7)·K·(…) < highTwoMargin − LR1 + …. The proof uses K ≤ 3 and K(1 + 6κ) ≤ 33/2. **3L: K = 3.84 (step 2) and 3.75 (step 3), both above 3.** The inequality still holds numerically, but these constants need re-deriving.
13. **HIGH growth and amplifier sum** (TwoLevelHigh `highTwoGrowth ≥ 0`, a1 + a2 ≤ 1/6, bins δ ∈ [q, 3/4]). Growth = (50/3)(1 − 6Σa)/(5 − 2q)² − (TA − Σd). 3L depth 2: .319; depth 3: .337; Σa ≤ .0156. All pass.
14. **Joint HIGH margin** (`highTwoMargin`, `highTwo_certificate`; DepthTwoPayment). PR67: 2.10e-8 (Lean ≥ 2e-8). 3L depth 2: 5.55e-8. 3L depth 3: 5.64e-8. See (c).
15. **Rescaling** (SecondStepReturnProof): 5/2·Bpun ≤ Bwide ≤ 20, 5/2·Lslot ≤ mesh, 5/2·Bv ≤ B − 130, Mcap·εc ≤ εold. If the step-3 floor 2/5 is relative to the step-2 unit, every 5/2 becomes 25/4 (for example Bpun ≤ 3.2).

## (b) Risks, most serious first

1. **The step-2 LOW handling relies on the baseline moment holding only in the old region.** The generic step `GeometryAffineAtStateStatement` quantifies over `[AffineLedger][DeletesIntoOldRegion]`, and PaidMain/Payment/TerminalLedger require `DeletesIntoOldRegion`. `actual_paid_low_main` returns a remaining state with R = J or capacity ≤ s.width. That is the old region, which is then paid by the incumbent. With region 3, step 2 must itself run a full O/R/L3/D dispatch; the generic step cannot be reused. Only step 3, which deletes into the old region, can reuse the existing `secondLedger`/`secondFamily`, after parameterising q and the slope.
2. **A gap case: the step-1 dispatch needs a fifth branch or a modified amplifier.**
   - Some children are in region 3 but not in the old region (g2 ∈ (−Δ, 0], Δ ≈ .0019). For them the step-2 amp K·g2 + α ≤ α violates `amp_first_pos` and errorReserve (item 9).
   - For g2 ∈ (0, ~4e-4), step 2 fails errorReserve, and step 3 run directly has a negative HIGH reserve.
   - Fix: give step 2 an amplifier floor a2 ≥ (g_old/6 + LR2)/(pf − ½). Depth-2 slack there is large, R2 ≈ .005–.01. Children with g2 ≤ 0 could alternatively be routed to step 3 directly. The model has neither branch.
3. **The zero-extraction child is not the worst case at depth 3.** d2 is set by the child's own step-2 grid position, not by the cell b. A child just above region 3 deletes about 0 at step 2 and keeps a full slot, so g3 doubles (.00093 → .0019) and a3 doubles. This breaks the 2-level pattern of a cell-only bound (`ha₂ : a₂ ≤ secondAmp b + ω`, `childOvershoot b`, affine-in-b brackets). A decoupled worst case (a2max + a3max) loses about .012 of reserve, which kills the margin. Item 8's zero fact also goes negative.
4. **Hard-coded depth two.**
   - `secondJunction` appears in 37 files and plays two roles: it is both the junction of step 2 and the junction of region 2.
   - `IsTwoLevelFirstStep` fixes the ledger constants.
   - `SecondStepReturnAt`/`low_state_dispatch` return a single HIGH layer, Ret = Z^{q(del+mesh)}·Σ_b Hb.value, with `Pays secondJunction`.
   - The `SecondStepHighCount` labels are `NonzeroJointSourceLabel`, a pair of first- and second-level labels, with one Bool orientation.
   - Depth 3 needs nested Ret (Z^{q0(d1+mesh) + q1(d2+mesh)}·count3), label triples, and Bool² orientations.
5. **Hard-coded old-region constants:** `secondRatio`/`regionSlope`/`regionIntercept`/`oldOvershoot`/`secondAmplifier` (they use slotPrice and 1), `secondLedger.price := slotPrice, intercept := 1`, 7/2500, K ≤ 3, 33/2.
6. **What is already generic:**
   - The `AffineLedger` class allows any price and intercept.
   - `fixedDel`/`low_reserve`/`region_deletion_boundary` are generic.
   - `NaturalState.rebase`/`unitState` compose for any c > 0, but the 5/2 factors compound (item 15).
   - `low_state_dispatch` is generic in q, del, amp and reserve, apart from the Pays junction and the SecondStepReturnAt form.
   - `DepthTwoChildAnchor` (`family_element_supported`, `selfNaturalRow`) holds for any η, so it iterates to depth 3.
   - `InitialAffineAt` is ledger-generic.

## (c) Depth-three joint HIGH reserve

Iterating `joint_high_split`:

R3(δ, b) = (1 − ρ(δ)) − δ·TA(b) + (δ − q0)·d1 + (δ − q1)·d2 − (a1 + a2 + a3)·cost(δ)
         = secondHigh(δ, A0 − d1 − d2, 1 − 6a1 − 6a2, a3) + (a1 − q0·d1) + (a2 − q1·d2),

where a1 − q0·d1 = LR1 = α(1 − q0·I2/k2) and a2 − q1·d2 = LR2 = α(1 − q1·I3/k3).

This is exactly margins.py `depth3`. My values match: 5.939e-8 and 5.645e-8, with depth 2 at 5.863e-8 and 5.553e-8.

Varying the child shows that R3 is invariant across children (7.6–8.1e-8 with plain length A, against TA in the margin), even while a2, d2 and a3 swing widely. So the heuristic is right **as a value**: R3 = (step-3 region slack) + LR1 + LR2, which is at least mM2/K + LR1 + LR2 whenever the child after d2 is on or inside region 3.

The Lean, however, cannot certify R3 as the 2-level code does, with a1, a2, a3 bounded separately by cell functions. It must use the coupled identity: a2 = K(k3, I3, q1)·g2 + α, with d2 tied to that same a2.

The budget becomes R3min − LR1 − LR2 > losses (3L: 5.64e-8 − 1.14e-9). The `Pays` analogue needs lo = q2, length = the step-3 total, and amp = a3, combined with three payments in a `depth_two_pair_exponent_bound`-style lemma that carries the extra terms (δ − q1)·d2 and price·(target2 + mesh).
