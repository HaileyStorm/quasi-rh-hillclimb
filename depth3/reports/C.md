# Report C: the depth-two joint HIGH count, and what depth three needs

Paths are relative to `Candidate/Cycle63/`. Notation: ρ(δ)=1−10δ/(3(5−2δ)), c(δ)=5−6ρ(δ), and δ=2a−1 is the zero parameter of a bin with real part a.

## How the joint count works in Lean

The second step's HIGH part for a prefix with fixed row v₁ is a `SecondStepHighCount` (Moment/DepthTwoHighCount.lean:49). It is a finite set of classes σ. Each class has some labels, an exponent e, a row-norm exponent q, a missing-radical exponent m₂ and a zero bin. Its count form, the "returned count", is `value = Σ_σ Z^{e_σ}·#labels_σ` (line 97).

The rows of a pair (prefix p, label ℓ) are `jointSourceRow left (v p) (unit p) ℓ`, and v p divides that row (`prefix_dvd_depthTwoRow`, DepthTwoCount.lean:294). The **zero-density estimate is applied once**, to the final pair rows:

1. `card_le_density_mul_fiber` (Density/JointRows.lean:35) bounds the labels: #labels ≤ C(1+T)^J·H^{ρ(2a−1)+loss}·F. This needs 4/5 ≤ a ≤ 7/8 (so δ ∈ [3/5, 3/4]) and H = Z^q. F is the largest number of labels over one row.
2. The fibre over one row w is bounded by d(w)·A·C·Z^{m₂+loss}, where d(w) ≤ C·Z^{loss/2} counts divisors and A is the number of prefixes over one ideal (`composite_row_fiber_card`, `depth_two_source_row_count`, DepthTwoCount.lean:303).
3. Combining these: #pairs ≤ C(1+T)^J·Z^{m₂ + q·ρ(δ) + loss}·A (`depth_two_high_row_count` :393, `second_step_high_selection_count` DepthTwoHighCount.lean:320). The prefix type P is generic.
4. `depth_two_returned_sum` (Physical/InitialMass/DepthTwoReturnedCount.lean:169) bins in 4 coordinates (q, m₂, zeroBin, first-level miss X1₁) with bin loss width·(3+4B). It takes A = Apre·Z^{X1₁}·K.

So the first-level rows contribute only their missing radical X1₁, as a fibre count. Their density factor ρ·X2₁ is never counted. It is moved onto the pair row by the scale identity.

## (a) Conditions

1. **Zero-density range** (Density/FixedDensity.lean:22, JointRows.lean:35): the estimate needs a ∈ [4/5, 7/8], i.e. δ ∈ [3/5, 3/4], and ρ ≤ 1 on [0, 3/4] (Rounding.lean:28). `Pays` asks lo ≤ δ ≤ 3/4. *Depth three:* the third step's bins are [q₂, 3/4] with q₂ = 0.7179, which is inside the range. This is fine.
2. **Density loss** `density_loss_absorb`: loss is split as loss/(2(Q+1)), and Lipschitz/rounding gives ρ(2b−1) ≤ ρ(2a−1)+3e and a ρ drop of at most 2·Δδ. The buffer grid is 51/100 + e·k with ⌈0.49/e⌉ steps (BufferedPartition.lean:35). *Depth three:* unchanged. Binning in one more missing-radical coordinate gives loss width·(4+4B), or width·(3+4B) if X1₁+X1₂ is binned as one coordinate. Both are arbitrary ε.
3. **Fibre bound for prefixes**: `child_prefix_count` (DepthTwoCount.lean:54) gives children over one ideal ≤ C·Z^{m+loss}. *Depth three:* the prefix becomes (row r, level-2 LOW child ℓ₂) with multiplier v₁·c₂. It needs A₁₂ ≤ d(D)·Apre·Z^{X1₁}·C·Z^{X1₂+ε}. `composite_prefix_fiber_card` (DepthTwoCount.lean:236) is exactly this lemma, but **nothing uses it yet**.
4. **Pays** (DepthTwoHighCount.lean:115). For every class: lo ≤ δ ≤ 3/4 and e − m_s + m₂ + ρ(δ)(q − log_Z N v₁) ≤ loss − [m_s(1−ρ) − δ·L − a·c(δ)]. Here m_s is the scale, L the length and a the amplifier of the second-step parent. At the call sites lo = `secondJunction`. *Depth three:* the same predicate for the third step, with lo = q₂ and v₁ replaced by v₁c₂.
5. **Pair exponent bound** `depth_two_pair_exponent_bound` (Physical/InitialMass/DepthTwoPayment.lean). It sums the level-1 reserve h₁ (valid for all δ ∈ [q₁, 3/4], saving γ₁ ≥ 0) and `Pays` h₂, using five inputs:
   - q ≤ X2₂ + Lv;
   - the scale identity m₂ + Lv ≤ X2₁ + κ;
   - the volume A₂ ≤ X3₁ − deleted + pad;
   - fixedDeletion(b) ≤ target ≤ deleted;
   - the caps m₁ ≥ 1, A₁ ≤ TA(b), a₁ ≤ firstAmp(b), a₂ ≤ secondAmp(b)+ω.

   The scale m₂ cancels exactly: −m₂(1−ρ) − ρm₂ + m₂ = 0. The result is ≤ −highTwoAt(δ,b) + losses.
6. **Depth-two reserve** (Optimization/TwoLevelHigh.lean:58):
   `highTwoAt(δ,b) = (1−ρ(δ)) − δ·TA(b) + (δ−q₀)·d₀(b) − (a₁(b)+a₂(b))·c(δ)`, where:
   - TA(b) = B − (λ−1)(b − mesh);
   - d₀ = (gap(b) + 6I₂a₁)/(6k₂), with gap(b) = B − I₂ + (6k₂ − λ)b;
   - a₂ = q₁/(6(κ−q₁))·g + lowRW, with g = A + (6κ−1)z − M for the child at the corner after d₀.

   `highTwoMargin = min_b highTwoAt(q₁, b)` over b ∈ {firstCellTop, slotTop}, using affinity in b. Proved by `bracket` to 12 digits. Its values are 2.30e-8 and **2.10e-8**, which matches margins.py.
7. **Growth in δ**: (50/3)(1−6(a₁+a₂))/(5−2q₁)² − (TA − d₀) ≥ 0 (0.334 / 0.326), and a₁+a₂ ≤ 1/6 (0.0138), both by `bracket`. *Depth three:* (50/3)(1−6Σa)/(5−2q₂)² − (TA − d₀ − d₁) ≥ 0 gives 0.346 / 0.337. Σa = 0.0156 ≤ 1/6. This is fine.
8. **Absorbing the losses** (`depth_two_returned_payment`, LowChildSelectedJoined.lean:262,406). The condition is small₁ + loss₂ + ρκ + δ·pad + q·mesh + (q − q₀)·target + c(δ)·ω ≤ Lmax, and Lmax − highTwoMargin + εA ≤ the error budget. *Depth three:* κ, pad, mesh, the price excess and ω each appear twice (three times for ω), and must fit under the depth-three margin.

## (b) Risks, most serious first

1. **The second step has no first-level-form payment for its LOW children.** At depth three, step 2's LOW children must pay a linear form X0₂ + X1₂ + ρX2₂ + δX3₂ ≤ small₂ − [m₂(1−ρ) − δA₂ − a₂c] − γ₂ for every δ ∈ [q₂, 3/4]. They must also have a **fixed** deletion width d₁ that depends only on the level-1 cell b (as `target = fixedDeletion cell` does now), and a scale identity m₃ + log(N c₂) ≤ X2₂ + κ. Today step 2 returns only class-form `Pays`, and its LOW children go to the old region. If d₁ depends on the child's own state (A, z, M) instead of on b, the reserve is no longer affine in b. The 2-endpoint `bracket` minimum then fails, and a 2-D minimum over (b, level-2 cell) is needed. margins.py takes d₁ at the single corner child.
2. **Hard-coded constants.** `secondAmp`, `childOvershoot` and `oldOvershoot` hard-code the old region (κ, intercept 1). `highTwoAt`, `highTwoMargin` and `depth_two_returned_payment` hard-code `secondJunction`, `fixedDeletion`, `twoLevelTotalA` and `firstAmp`. At 3 levels the depth-two reserve has to be rebuilt over region-3. A new `highThreeAt` and new brackets are needed.
3. **The joint count is written for exactly two label sets.** The Moment layer is generic in the prefix type, so one density application still suffices. But three things are missing: a pair-prefix fibre bound (`composite_prefix_fiber_card`, unused, whose v′ must be independent of the first coordinate; this holds up to units by `normValue_childMultiplier`); a second missing coordinate in `depth_two_returned_sum`, which bins only one; and the cap X1₁ + X1₂ ≤ 2B.
4. **The margin is thin and purely structural.** Both reserves come entirely from regionMargin = 1e-8. With m = 0 they are −4.6e-8 (depth two at 3 levels) and −4.9e-8 (depth three), and they grow about linearly in m. The doubled losses of item 8 must fit in about 5.6e-8. They do if they are ε-small; I did not check that in my files.
5. **Zero-density domain.** The window is δ ≤ 3/4 (`incumbent_beta_upper`, β ≤ 7/8). Fine for q₂ < 3/4.

## (c) The exact depth-three joint HIGH reserve

I summed h₁ + h₂ + h₃ with the scale identities Lv₁ ≤ X2₁ + κ − m₂ and L(c₂) ≤ X2₂ + κ − m₃, and the volumes A₂ ≤ X3₁ − del₀ + pad and A₃ ≤ X3₂ − del₁ + pad. The prices of the two deletions are q₀ and q₁. m₂ and m₃ cancel, and the losses are 2ρκ + 2δ·pad + Σ q_i·mesh + Σ (p_i − q_i)·t_i + c·Σω. What remains is:

highThreeAt(δ,b) = (1−ρ(δ)) − δ·TA(b) + (δ−q₀)·d₀(b) + (δ−q₁)·d₁(b) − (a₁+a₂+a₃)(b)·c(δ)

for δ ∈ [q₂, 3/4], with:
- (k₂,I₂) = region(q₁) over (k₃,I₃), and (k₃,I₃) = region(q₂) over (κ, 1). The plane (λ, B) is built over (k₂,I₂).
- d₀ = (gap + 6I₂a₁)/(6k₂). The child after d₀ has A = B − (λ−1)b − d₀, z = b − d₀ and M = 1 − 6a₁.
- g₂ = A + (6k₃−1)z − I₃M, a₂ = q₁g₂/(6(k₃ − q₁I₃)) + lowRW, and d₁ = (g₂ + 6I₃a₂)/(6k₃).
- g₃ = (A−d₁) + (6κ−1)(z−d₁) − (M−6a₂), and a₃ = q₂g₃/(6(κ−q₂)) + lowRW.

The margin is min over b ∈ {firstCellTop, slotTop} at δ = q₂. It needs the growth condition in item 7, and the depth-two reserve at q₁ over region-3 must also stay positive.

**Comparison with margins.py `depth3`:** it is the same formula term by term. It gives highThree = 5.94e-8 and 5.64e-8 (margin **5.64e-8**). The depth-two reserve at 3 levels is 5.86e-8 and 5.55e-8, versus 2.10e-8 at 2 levels. The heuristic is therefore exact, **provided** risk 1 holds: d₁ fixed per cell b, step 2's deletion priced at q₁, and the step-2 LOW payment in level-1 linear form. That condition is the real gap.
