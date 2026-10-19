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
python3 "$audit" "$here/tests/compare_draft.md" --compare "$here/tests/compare_style_only.md" >/dev/null \
  && echo "ok   facts check passes a style-only edit" || { echo "FAIL: facts check flagged a style-only edit"; fail=1; }
python3 "$audit" "$here/tests/compare_draft.md" --compare "$here/tests/compare_lost_facts.md" >/dev/null \
  && { echo "FAIL: facts check missed lost hedges, condition and negation"; fail=1; } || echo "ok   facts check flags lost and added facts"
exit $fail
