# For AI agents

1. Read [auto-research.md](auto-research.md) first, then [CONTRIBUTING.md](CONTRIBUTING.md).
2. Check open issues, open PRs, and [auto-research/results.md](auto-research/results.md) before starting, so you don't duplicate work.
3. Install and verify:

   ```
   pip install numpy scipy sympy
   python certify.py
   ```

   It should print `True` and all `OK` within a few seconds.
4. Every claim must be exact (`certify.py` or a proved lemma). Every claim is conditional on the preprint's 7/8 theorem, so say so.
5. Report by appending a row to `auto-research/results.md` and opening a focused PR, or by opening an issue with a handoff. Disclose AI assistance.
