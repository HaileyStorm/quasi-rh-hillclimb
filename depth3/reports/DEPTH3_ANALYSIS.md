# Third affine level: what the Lean actually requires

Target: beat the tracker record 174963413/200000000 ≈ 0.874817065 (PR #67) with a third affine step.

The model predicts **θ ≈ 0.874812430**, with junctions q₀ = 0.638017, q₁ = 0.687932, q₂ = 0.717908 and window top 0.04023082.

Method: four independent line-by-line reads of PR #67's Lean (reports A–D in `reports/`), covering:

- arithmetic certificates;
- LOW-branch dispatch;
- the depth-two HIGH count and zero density;
- the physical LOW-child and second-step modules.

All four reproduce PR #67's margins exactly (highTwo = 2.30·10⁻⁸ / 2.10·10⁻⁸).

## Verdict

No fatal obstruction was found, and the predicted bound looks reachable. But a third level is not "one more instance": the second step needs its own full LOW dispatch, which is roughly a re-implementation of PR #67's own contribution one level down. Three hard-coded checks fail at the new constants and need retuning, and one coverage gap needs a new rule.

## Confirmed

- **Depth-three joint HIGH reserve.** All four reports derive it from the Lean's `joint_high_split` and `depth_two_pair_exponent_bound`:

  highThree(δ,b) = (1−ρ(δ)) − δ·TA(b) + (δ−q₀)d₁ + (δ−q₁)d₂ − (a₁+a₂+a₃)(5−6ρ(δ)),  δ ∈ [q₂, 3/4]

  It equals the third step's region slack plus the two LOW reserves. The minimum is **5.64·10⁻⁸**, at q₂ and the window top; PR #67 runs at 2.1·10⁻⁸. This matches the earlier heuristic exactly. The growth-in-δ condition (≈ 0.34) and Σa ≤ 1/6 (≈ 0.016) hold.
- **Depth-two reserve at 3 levels:** 5.55·10⁻⁸.
- **The zero-density estimate** is applied once, to the final rows. Its domain δ ≤ 3/4 covers q₂ = 0.718.
- **Branch D rooms** pass at both steps: ≈ 0.020 at step 1 and ≈ 0.027 at step 2, against ≈ 0.0014 needed.
- **LOW reserves** stay above 10⁻¹⁰: 4.2·10⁻¹⁰ at step 2 and 4.3·10⁻¹⁰ at step 3.
- **The nested grid works:** SecondIndex × third grid, with rounding ≈ 5·10⁻¹².

## Must change (structural)

1. **Step 2 needs its own O/R/L3/D dispatch.** The generic step `GeometryAffineAtStateStatement` only accepts ledgers that delete into the old region (`DeletesIntoOldRegion`, `secondFamily_deletesIntoOldRegion` by rfl). The second step's LOW children are paid by the baseline moment, which holds only in the old region. Pointing step 2 at region 3 therefore means running the first-step machinery (`IsTwoLevelFirstStep`, fixed deletion, the row-5 payment) per second-step position, with a nested third family.
2. **The deletion width d₂ and amplifier a₂ must be tied to the first-level cell b.** If they depend on each child's own position instead, children just past region 3 delete almost nothing, so their third-step overshoot and a₃ double. The certificate then fails (−1.2·10⁻² reserve) and no width floor works. With the cell-uniform choice the reserve is the 5.64·10⁻⁸ above, and the family is indexed by (position, width, cell). Report A notes the reserve is affine in (b, t), so a 4-vertex certificate suffices.
3. **HIGH labels go from pairs to triples.** `SecondStepHighCount`, `Pays` (pinned to `secondJunction`), the return type `Ret` and `depth_two_returned_sum` all need a third layer. They also need a second missing-radical coordinate, a 2B cap on X1₁ + X1₂, and the unused `composite_prefix_fiber_card`.
4. **`secondJunction` appears in 37 files** in two roles (step-2 junction and region-2 junction), and these must be split.

## Fails at the new constants (retune)

| check | value at 3 levels | limit | fix |
|---|---|---|---|
| reflection margin: step-1 child's overshoot over the old region | 2.905·10⁻³ | 7/2500 = 2.8·10⁻³ | raise δ_R to ≈ 2.95·10⁻³ (ceiling 0.004 − ξ_R, about 9·10⁻⁵ of slack), or raise the width floor to ≥ 0.4151 |
| third-step zero room | down to −1.2·10⁻³ / −7·10⁻⁵ | ≥ 0 | lower `zeroSaving` from 1/20 to ≈ 1/50 (downstream impact unchecked) |
| `childSlotCap ≤ 681/10000` | 0.06858 | 0.0681 | re-bracket |
| K ≤ 3 (TwoLevelBudget, positions) | 3.84 / 3.75 | 3 | K ≤ 4 |
| level-2 rate ≤ 0.15 | q₁/(6κ) = 0.153 | 0.15 | re-bracket |
| plane slope λ ≤ 4 (mesh bound) | 4.09 / 4.29 | 4 | re-bracket |
| mask Bwide ≤ 20 under rebase | 5/2 compounds to 25/4 | 20 | Bwide ≈ 50; supply then needs d ≈ 80 |

## Coverage gap (needs a new rule)

Some step-1 children lie inside region 3 but outside the old region, or overshoot region 3 only slightly (0 < g₂ ≲ 4·10⁻⁴). For them the step-2 amplifier K·g₂ + α fails `errorReserve_edges` and `amp_first_pos`, because the gap over the old region is g₂ + Δ with Δ ≈ 1.9·10⁻³. Reports A and B propose a fix:

- floor the step-2 amplifier at a₂ ≥ (g_old/6 + LR₂)/(pf − ½);
- or route g₂ ≤ 0 children straight to step 3.

Either is paid from a depth-two slack of ≈ 0.005–0.01. The reports disagree on whether routing straight to step 3 is safe under the cell-uniform bounds (D says not), so the amplifier floor is the safer choice.

## Effort

PR #67 itself was about 128k added lines, on top of PR #64. A third level means:

- the dispatch above;
- triple-label counting;
- re-bracketing about 10 constants;
- new `highThreeAt` certificates.

That is comparable in size to PR #67. A full build and kernel check needs more than 8 GB of RAM (11 GB peak export) and several CPU-hours.
