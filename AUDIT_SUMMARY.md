# Audit of Part II at the new geometry: summary

**Target.** Re s > σ₀ = 20649/23600 = 7/8 − 1/23600, with ℓ = 1/6 + 1/5900 = 2953/17700, h = 405989/500000, M = 1 − ℓ, l_x = 1 + ℓ − h. The contradiction hypothesis is σ₀ < β* ≤ 7/8; the bound β* ≤ 7/8 comes from the preprint. Moment lemmas are applied with κ = 3/4.

**Scope.** Lines 3723–16677 of `paper.tex` were read line by line in six ranges (reports A–F in `audit/`). This covers:

- every Part I lemma that Part II invokes (Euler regions, detector, sextic count, contour accounting, principal residue);
- all of Part II, including the roughly 5,000 lines of inverse-moment and plain-moment inductions.

Lines 1–3723 (preliminaries, unmarked row energy, base probe) were not audited. Part II uses them only through general statements.

**Verdict: the argument goes through with edits. No fatal obstruction was found.** Every edit either replaces a hard-coded constant, or weakens a stated inequality to the one the proof actually uses. The required signs and margins were rechecked with exact fractions.

## Edits that carry mathematical content

1. **Second Euler region: lower x_r ≥ 7/8 to x_r ≥ σ₀.**
   - **Where:** l. 4056, 5574; used at 5525–5530, 6174–6301, 9052–9074, 15553–15652.
   - **Why it is needed:** under σ₀ < β* ≤ 7/8, the principal line Re s = β* + e can lie below 7/8.
   - **Why it works:** at x_r ≥ σ₀ the exponents in Lemma *local-euler* are:
     - good primes: −1.81496 (needs < −1);
     - p | u: −0.82496 (needs < 0);
     - R: −2.23975;
     - the P₀ tail exponent is 0.81496 > 4/5, so c_H = 4/5 survives.

   Consequences:
   - H_η is holomorphic, with |H_η − 1| ≤ 1/2 on Re s > σ₀.
   - B_p = −1 + O(Q^{−σ₀}).
   - κ_P < σ₀ min ℓ_i (l. 15613–15619, 16304–16305). There, 7/(96K) becomes 7ℓ/(16K).
   - The hypotheses "σ₀ ∈ [7/8, 1)" at l. 5811, 6024, 6178, 6345 relax to σ₀ ∈ (1/2, 1). The proofs never use more.
   - At l. 6418, D₁(3/8) becomes D₁(1/4). At l. 9134, ε₀ = 3/8 becomes ε₀ = σ₀ − 1/2.

2. **Completed-row norm (Lemma *probe-row-norm*, l. 8116–8325).**
   - "= Z^{M'}" is false once ℓ > 1/6. The correct bound is Z^{M' + ((d − 1 + 5ℓ)/4)₊}, an extra loss of less than 3/11800, occurring only for d ∈ (1 − 5ℓ, ℓ).
   - Prop. *probe-low* then has f(d) = −d + ((d − 1 + 5ℓ)/8)₊ < 0, so the low bound Z^{l_x/2 + b/12} = Z^{C(σ₀)} stands. The equality C(σ₀) = l_x/2 + b/12 was checked exactly.

3. **Stated length bounds that are now false but stronger than needed.**
   - "M' ≥ 1/2" (minimum 0.49949) and "l_y − d ≥ 5/16" (minimum 0.31147), both at l. 8593–8596.
   - The proof only needs Q, Y' ≥ 1.

4. **Δ, κ bookkeeping.**
   - Replace Δ = β* − 7/8 with Δ' = β* − σ₀ throughout (l. 6812–6841, 8646–8648, the final section). Under the new hypothesis Δ can be ≤ 0.
   - Apply Lemma *plain* with κ = 3/4. Its hypothesis β* ≤ 7/8 is supplied by the preprint's theorem, and only an upper bound on zeros is used. The plain capacity is 2/9.
   - Delete the +Δ/4 capacity comparison. The final comparison becomes E_actual(h) − Δ' < 0.
   - Reword the remarks at l. 12581–12585 and 15097–15106.
   - The case δ = 5/6 becomes vacuous, because δ ≤ κ_act ≤ 3/4.

5. **Constants.** Replace C(s) = s − 11/16, 3/16, 1/48, −7/1200, −79/800, 53/32, 8/39, P_a = Z^{1/8} and the other old-geometry values with the general forms. Report F has the full table; all keep their required signs. The final-section inequalities are certified separately by `certify.py`.

## Remaining caveats

- **Not formally verified.** This is an AI-assisted reading, not a referee report. A human expert should check items 1 and 2 in particular.
- **Depends on the preprint.** The result assumes the preprint's theorem (zero-free for Re s > 7/8). Using it is not circular, but the new constant inherits the preprint's status.
- **Next step.** Write the edits above into a patched `paper.tex`. That makes the claim directly checkable.
