#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Fail if anything that looks like a publication credential is present in the tree.
# No credential is needed to build, test, or prepare a release candidate here, so any hit is a
# defect regardless of whether the value is live.
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

PATTERNS=(
  'gh[pousr]_[A-Za-z0-9]{36,}'
  'github_pat_[A-Za-z0-9_]{20,}'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  '(zenodo|ssrn)[_-]?(token|api[_-]?key|password)[[:space:]]*[:=][[:space:]]*[A-Za-z0-9_-]{8,}'
  'AKIA[0-9A-Z]{16}'
  'xox[baprs]-[A-Za-z0-9-]{10,}'
  '(client_secret|api[_-]?key|secret[_-]?key)[[:space:]]*[:=][[:space:]]*["'"'"'][A-Za-z0-9_\-]{16,}'
)

status=0
for p in "${PATTERNS[@]}"; do
  if hits=$(grep -rEIn --exclude-dir=.git --exclude-dir=build --exclude=scan-secrets.sh "$p" . 2>/dev/null); then
    echo "SECRET-LIKE MATCH for /$p/:"
    echo "$hits"
    status=1
  fi
done

if [ "$status" -eq 0 ]; then echo "secret scan: clean"; fi
exit "$status"
