#!/usr/bin/env bash
# Build dist/clean-text.zip for upload to claude.ai (Settings → Capabilities → Skills).
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$here/dist"
cd "$here/plugins/clean-text/skills"
rm -f "$here/dist/clean-text.zip"
TZ=UTC zip -qrX "$here/dist/clean-text.zip" clean-text -x '*/__pycache__/*' '*.DS_Store'
echo "$here/dist/clean-text.zip"
