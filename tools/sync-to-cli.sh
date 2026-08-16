#!/usr/bin/env bash
# Dev-only: vendor a copy of streamwatch-core into the CLI repo.
# The CLI must NOT depend on this package at runtime; it vendors a copy so the
# two stay in sync. After syncing, run the CLI's parity tests.
#
# Usage: tools/sync-to-cli.sh /path/to/streamwatch-cli
set -euo pipefail

CLI_DIR="${1:-}"
if [[ -z "$CLI_DIR" ]]; then
  echo "usage: $0 /path/to/streamwatch-cli" >&2
  exit 1
fi

CORE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$CLI_DIR/src/streamwatch/core_shared"

echo "Syncing streamwatch-core -> $DEST"
rm -rf "$DEST"
mkdir -p "$DEST"

cp "$CORE_DIR/src/streamwatch_core/models.py" "$DEST/models.py"
cp "$CORE_DIR/src/streamwatch_core/errors.py" "$DEST/errors.py"
cp "$CORE_DIR/src/streamwatch_core/session_pool.py" "$DEST/session_pool.py"
cp "$CORE_DIR/src/streamwatch_core/metadata.py" "$DEST/metadata.py"
cp "$CORE_DIR/src/streamwatch_core/resolution.py" "$DEST/resolution.py"

# Rewrite intra-package imports (streamwatch_core.* -> core_shared.*)
find "$DEST" -name '*.py' -print0 | xargs -0 sed -i 's/from streamwatch_core\./from ..core_shared./g; s/import streamwatch_core/import ..core_shared/g'

echo "Done. Run parity tests in the CLI repo next."