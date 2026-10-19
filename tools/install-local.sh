#!/usr/bin/env bash
# Install without the plugin system: copy the skill into ~/.claude/skills/clean-text.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$HOME/.claude/skills"
cp -R "$here/plugins/clean-text/skills/clean-text" "$HOME/.claude/skills/"
echo "installed to $HOME/.claude/skills/clean-text"
