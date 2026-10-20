# Results log

Append one row per result. `status` is `certified` (Track A, `certify.py` passes), `proposal` (Track B, the needed lemma isn't proved yet), or `proved` (the lemma is proved; give a reference). All results are conditional on the preprint's 7/8 theorem unless the row says otherwise.

| date | who | track | σ₀ (exact) | point / idea | evidence | status |
|---|---|---|---|---|---|---|
| 2026-09-30 | OpenAI preprint | — | 7/8 | ℓ = 1/6, h = 13/16 | preprint, Lean | preprint |
| 2026-10 | rohanarun + Claude | A | 24499/28000 = 7/8 − 1/28000 | ℓ = 1/6 + 1/7000, h = 4059/5000 | `python certify.py 7000 4059/5000` | certified |
| 2026-10-20 | rohanarun + Claude | A | 20649/23600 = 7/8 − 1/23600 | ℓ = 1/6 + 1/5900, h = 405989/500000 | `python certify.py`; `AUDIT_SUMMARY.md` | certified + audited (not refereed) |
| 2026-10 | rohanarun + Claude | B (negative) | ≥ ~0.864 | perfect row counts + perfect large sieve, other choices frozen | `leverage.py`, README §4 | ceiling (numerical) |
| 2026-10-20 | rohanarun + Claude (`hillclimb.py`) | A | 10195/11652 = 7/8 − 1/23304 | ℓ = 1/6 + 1/5826, h = 405967/500000 | `python certify.py 5826 405967/500000` | certified (final section only; audit edits carry over, constants not re-derived) |
