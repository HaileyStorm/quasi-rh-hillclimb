# Quasi-RH: pushing the zero-free half-plane slightly past 7/8

A follow-up to OpenAI's preprint *The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re(s) > 7/8*
(30 September 2026, `openai/math`, preprints/The-Quasi-Riemann-Hypothesis-September-30-2026).
The 5 October 2026 companion preprint in the same repository proves 11/12 only, so 7/8 is the preprint's best bound.

## Claim (conditional, see Status)

Assume the preprint's theorem (zero-free for Re s > 7/8). Then every finite-order Hecke L-function over Q(√-3) has no zeros in

  **Re s > 20649/23600 = 7/8 − 1/23600 ≈ 0.8749576**

This covers every Dirichlet L-function, including ζ(s). It comes from re-running the preprint's Part II with the slot geometry

  ℓ = 2953/17700 (= 1/6 + 1/5900),  h = 405989/500000,

applying the edits listed in `AUDIT_SUMMARY.md`. This point is about 99% of the way to the method's limit: with every other structural choice frozen, the edge of feasibility is σ₀ ≈ 7/8 − 4.29·10⁻⁵. An earlier version of this note claimed 7/8 − 1/28000.

## Main structural facts

1. **Closed form of the boundary.** With l_x = 1 + ℓ − h and M + ℓ = 1, the low estimate Z^{l_x/2 + b/12} and the Mellin exponent C(s) = l_x/2 + s − 1 + h/6 meet at **σ₀ = 11/12 − ℓ/4** (h cancels). Part I (ℓ = 0) gives 11/12, and the preprint's ℓ = 1/6 gives 7/8.
2. **The preprint's constants are near-optimal.** The binding inequality is Lemma *balanced-endpoint*. Its true slack is about 2.3·10⁻⁴ (the paper certifies 1.1·10⁻⁴). The edge of feasibility is ℓ ≈ 1/6 + 1.717·10⁻⁴.
3. **M + ℓ = 1 is the right choice.** Freeing M gives σ₀ = 5/6 + M/12 − ℓ/6. The most efficient direction needs M + ℓ > 1, and the completed-row norm lemma rules that out.
4. **Ceiling of the architecture.** Keep the other structural choices frozen: the detector floor at 51/100, the contour at Re z = 17/50, and the probe scale relations. Then:
   - perfect row counts give σ₀ ≥ 167/192 ≈ 0.8698;
   - a perfect additive large sieve gives about 0.864.

   The obstruction is the floor bin, not the moment estimates.

## What is checked, and how

- **Exactly** (`certify.py`, rational arithmetic, about 1 second):
  - the adaptive endpoint inequality, via Bernstein positivity on 18 boxes;
  - every other inequality of the final section;
  - as a sanity check, the preprint's own point (1/6, 13/16) also certifies.
- **By a line-by-line reading** of lines 3723–16677 of `build/paper.tex`: every Part I lemma that Part II invokes, and all of Part II, including the moment inductions. Reports A–F are in `audit/`, and `AUDIT_SUMMARY.md` lists every required edit. Most are constant changes. Two carry mathematical content:
  - the preprint's second Euler region (x_r ≥ 7/8) must be lowered to x_r ≥ σ₀, which holds with wide margins;
  - the completed-row norm picks up an extra loss below 3/11800, which the low estimate absorbs.

## Status: read before citing

- **Not formally verified.** The audit is an AI-assisted reading, not a referee report. A human expert should check the Euler-region and row-norm edits in particular. Lines 1–3723 were not re-read.
- **Inherits the preprint's status.** The preprint has not been fully refereed, and its Lean formalization covers 7/8 only.
- **Next step.** Write the edits into a patched `paper.tex`.

Contributions welcome:

- a Lean check of `certify.py`;
- an expert review of `AUDIT_SUMMARY.md`;
- a structural change that beats the ceiling.

## Files

- `budget.py`: the Part II exponent budget for general (ℓ, h).
- `certify.py`: an exact certificate. By default it checks (ℓ, h) = (2953/17700, 405989/500000). Run `python certify.py N h` to check ℓ = 1/6 + 1/N.
- `optimize.py`, `edge.py`: a numerical search for the feasibility edge.
- `leverage.py`: sensitivity to the amplification slope and the plain capacity.
- `AUDIT_SUMMARY.md`, `audit/*.md`: the line-by-line audit.
- `auto-research.md`, `auto-research/`: instructions and tools for agents continuing the hill-climb (`hillclimb.py`, `whatif.py`, `results.md`, `proposals/`). The pipeline already found a slightly better final-section certificate, 7/8 − 1/23304; see `auto-research/results.md`.
- `upload.sh`: pushes this folder to GitHub.
