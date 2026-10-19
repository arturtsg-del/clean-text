#!/usr/bin/env bash
# Re-pull the vendored no-ai-slop catalogue from upstream.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
ref="$here/plugins/clean-text/skills/clean-text/references"
tmp="$(mktemp -d)"
git clone -q --depth 1 https://github.com/petergyang/no-ai-slop "$tmp/nas"
cp "$tmp/nas/skills/no-ai-slop/SKILL.md" "$ref/no-ai-slop.md"
cp "$tmp/nas/skills/no-ai-slop/eval.md" "$ref/no-ai-slop-eval.md"
cp "$tmp/nas/LICENSE" "$ref/LICENSE-no-ai-slop"
echo "upstream commit: $(git -C "$tmp/nas" rev-parse --short HEAD) — update ATTRIBUTION.md"
