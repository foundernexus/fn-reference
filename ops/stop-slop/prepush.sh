#!/usr/bin/env bash
# Founder Decisions stop-slop pre-push gate. Local only; never called by Vercel.
# Runs: check.py --changed (HARD must be 0), facts_guard.py vs origin/main, build.py.
# The manual read against ops/stop-slop/RULES.md is still required.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git fetch -q origin main || echo "stop-slop: git fetch failed; comparing against local origin/main" >&2
echo "== stop-slop: mechanical check (changed owned pages) =="
python3 ops/stop-slop/check.py --changed
echo "== stop-slop: facts guard vs origin/main =="
python3 ops/stop-slop/facts_guard.py origin/main
echo "== build =="
python3 build.py >/dev/null
echo "stop-slop gate: PASS (mechanical). Manual read against ops/stop-slop/RULES.md still required."
