#!/usr/bin/env bash
# Verify that every published baseline still has the bytes its record claims.
# This is the anti-drift gate: if a baseline file were ever edited, this fails loudly.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

SUMS=$(cat <<'SUMEOF'
295eb6cbe3c9f65f3678253dd803b200b3d36632470fdb592f83279b9379389d  model/1.0/WM-1.0.pdf
SUMEOF
)

if command -v shasum >/dev/null 2>&1; then
  echo "$SUMS" | shasum -a 256 -c -
else
  echo "$SUMS" | sha256sum -c -
fi
echo "baselines: OK"
