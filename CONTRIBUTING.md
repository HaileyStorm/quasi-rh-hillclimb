# Contributing

All contributions are welcome, from humans and automated research agents alike. Open an issue or a pull request.

## Open tasks, roughly in order of value

1. **Expert review of the two substantive edits** in `AUDIT_SUMMARY.md`:
   - lowering the second Euler region from x_r ≥ 7/8 to x_r ≥ σ₀;
   - the extra loss in the completed-row norm, which needs Lemma *probe-row-norm* to take ((d − 1 + 5ℓ)/4)₊.
2. **Patched `paper.tex`.** Write every edit from `AUDIT_SUMMARY.md` and `audit/*.md` into a copy of the preprint's `build/paper.tex`, so the claim can be checked directly.
3. **Re-read lines 1–3723** of `paper.tex`, which the audit did not cover.
4. **Lean.** Formalize the inequalities that `certify.py` checks: Bernstein positivity on boxes, and the side constraints.
5. **Hill-climb further.** Within the frozen architecture the edge is σ₀ ≈ 7/8 − 4.29·10⁻⁵, which leaves little room. Real gains need a structural change, such as a new probe, a cheaper floor bin, or a different trade-off between low estimates and slots. `leverage.py` shows how much each input would buy.

## Ground rules

- Any new constant must come with an exact certificate. Rational arithmetic or interval arithmetic is fine; floating point alone is not.
- Say clearly what is proved and what is assumed. Everything here is conditional on the preprint's 7/8 theorem.
