#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Verify that every published artifact still has the bytes its record claims.
#
# This is the anti-drift gate. It covers two things:
#   1. historical published baselines, which must never change;
#   2. the tracked copies of released artifacts, which must stay byte-identical to what was
#      published to the GitHub release and deposited at Zenodo.
#
# The expected digests are recorded here rather than fetched, so the gate needs no network and
# still fails on any divergence. A tracked release copy that drifts from the published object is
# exactly the failure this repository exists to make impossible.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

SUMS=$(cat <<'SUMEOF'
295eb6cbe3c9f65f3678253dd803b200b3d36632470fdb592f83279b9379389d  releases/1.0/WM-1.0.pdf
7d62e3268e930d5ad16aa97bd05eb037e15a08274487194041cafd78167fb902  releases/1.1/WM-1.1.pdf
8ae0ac5f7ff46aac25770888e5194f276acb48eaeb21949135f5c2fab15450b9  releases/1.1/WM-1.1-ERRATA-SCHEME-B-FINAL.md
SUMEOF
)

if command -v shasum >/dev/null 2>&1; then
  echo "$SUMS" | shasum -a 256 -c -
else
  echo "$SUMS" | sha256sum -c -
fi
# The release copy must also agree with the checksum file shipped beside it.
( cd releases/1.1 && { command -v shasum >/dev/null 2>&1 && shasum -a 256 -c SHA256SUMS.txt || sha256sum -c SHA256SUMS.txt; } ) >/dev/null

echo "published artifacts: OK  (WM 1.0 baseline · WM 1.1 release PDF · WM 1.1 errata · release SHA256SUMS)"
echo "  WM 1.1 PDF matches GitHub release wm-v1.1.0 and Zenodo 10.5281/zenodo.21970802"
