#!/usr/bin/env bash
# Dev-only: vendor a copy of streamwatch-core into the CLI repo.
# The CLI must NOT depend on this package at runtime; it vendors a copy so the
# two stay in sync. After syncing, run the CLI's parity tests.
#
# Usage: tools/sync-to-cli.sh /path/to/streamwatch-cli
#        tools/sync-to-cli.sh /path/to/streamwatch-cli --check   (drift check only)
set -euo pipefail

CLI_DIR="${1:-}"
CHECK_MODE="${2:-}"
if [[ -z "$CLI_DIR" ]]; then
  echo "usage: $0 /path/to/streamwatch-cli [--check]" >&2
  exit 1
fi

CORE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$CLI_DIR/src/streamwatch/core_shared"

MODULES=(models errors session_pool metadata resolution __init__)

drift=0
for mod in "${MODULES[@]}"; do
  src="$CORE_DIR/src/tukiwatch_core/$mod.py"
  dst="$DEST/$mod.py"
  if [[ ! -f "$dst" ]]; then
    echo "MISSING: $dst" >&2
    drift=1
    continue
  fi
  if ! diff <(sed 's/^from \./from tukiwatch_core./; s/^import \./import tukiwatch_core./' "$dst") "$src" >/dev/null; then
    echo "DRIFTED: $mod" >&2
    drift=1
  fi
done

if [[ "$CHECK_MODE" == "--check" ]]; then
  if [[ $drift -eq 0 ]]; then
echo "OK: vendored core_shared matches tukiwatch-core."
  else
    echo "DRIFT DETECTED. Run tools/sync-to-cli.sh $CLI_DIR to refresh." >&2
  fi
  exit $drift
fi

echo "Syncing tukiwatch-core -> $DEST"
rm -rf "$DEST"
mkdir -p "$DEST"

cp "$CORE_DIR/src/tukiwatch_core/models.py" "$DEST/models.py"
cp "$CORE_DIR/src/tukiwatch_core/errors.py" "$DEST/errors.py"
cp "$CORE_DIR/src/tukiwatch_core/session_pool.py" "$DEST/session_pool.py"
cp "$CORE_DIR/src/tukiwatch_core/metadata.py" "$DEST/metadata.py"
cp "$CORE_DIR/src/tukiwatch_core/resolution.py" "$DEST/resolution.py"
cp "$CORE_DIR/src/tukiwatch_core/__init__.py" "$DEST/__init__.py"

# Rewrite intra-package imports (tukiwatch_core. -> .) for the vendored copy
find "$DEST" -name '*.py' -print0 | xargs -0 sed -i 's/from tukiwatch_core\./from ./g; s/import tukiwatch_core/import ./g'

echo "Done. Run the CLI test suite next."