#!/usr/bin/env bash
# Build the installable .plugin file for a plugin in this repo.
# Usage: scripts/package.sh [plugin-name]   (default: officer-kit)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NAME="${1:-officer-kit}"
SRC="$ROOT/plugins/$NAME"
OUT="$ROOT/dist"
[ -f "$SRC/.claude-plugin/plugin.json" ] || { echo "no plugin.json under $SRC" >&2; exit 1; }
VER="$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['version'])" "$SRC/.claude-plugin/plugin.json")"
mkdir -p "$OUT"
rm -f "$OUT/$NAME.plugin"
( cd "$SRC" && zip -qr "$OUT/$NAME.plugin" . -x "*.DS_Store" -x "__pycache__/*" -x "node_modules/*" )
echo "built $OUT/$NAME.plugin (version $VER)"
unzip -l "$OUT/$NAME.plugin" | tail -1
