#!/usr/bin/env bash
# Smoke test: slop samples must fail the gate, clean samples must pass.
set -uo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
audit="$here/plugins/clean-text/skills/clean-text/scripts/audit.py"
fail=0
for f in "$here"/tests/slop_*.md; do
  python3 "$audit" "$f" --only-gate >/dev/null && { echo "FAIL: $f passed the gate"; fail=1; } || echo "ok   $f (gate failed as expected)"
done
for f in "$here"/tests/clean_*.md; do
  python3 "$audit" "$f" --only-gate >/dev/null && echo "ok   $f (gate passed)" || { echo "FAIL: $f failed the gate"; fail=1; }
done
exit $fail
