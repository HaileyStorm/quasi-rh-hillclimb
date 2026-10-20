#!/usr/bin/env bash
# Push this folder to https://github.com/rohanarun/quasi-rh-hillclimb
# Run from inside the unzipped qrh_followup folder:  bash upload.sh
set -euo pipefail
REPO="https://github.com/rohanarun/quasi-rh-hillclimb.git"
cd "$(dirname "$0")"
rm -rf __pycache__ auto-research/__pycache__
if [ ! -d .git ]; then git init -q; fi
git checkout -q -B main
git add -A
git commit -q -m "Quasi-RH past 7/8: certificate, audit, auto-research harness" || echo "(nothing new to commit)"
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO"
git push -u origin main
echo "Done: https://github.com/rohanarun/quasi-rh-hillclimb"
