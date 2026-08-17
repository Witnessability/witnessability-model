#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
#
# Rebuild a released artifact from source and prove it is the published bytes.
#
# `make paper` builds the *current* source, and its timestamp comes from the last commit that
# touched paper/. That is right for building what the tree says now, and wrong for reproducing a
# past release: any later commit under paper/ — even deleting an empty placeholder — moves the
# timestamp and therefore the output bytes. Reproducing a release means pinning the timestamp the
# release was built with, which is recorded with the release rather than inferred from the tree.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="${1:-1.1}"
STATE="$REPO/publication/RELEASE-STATE-PUBLIC.json"

read -r EPOCH EXPECTED ARTIFACT < <(python3 - "$STATE" "$VERSION" <<'PY'
import json, sys
state, version = sys.argv[1], sys.argv[2]
d = json.load(open(state))
rel = d["release"]
if rel.get("model_version", d["subject"]["model_version"]) != version:
    sys.exit(f"FATAL: {state} records release {d['subject']['model_version']}, not {version}")
r = rel["reproduction"]
print(r["source_date_epoch"], rel["artifact"]["sha256"], rel["artifact"]["path"])
PY
)

echo "== reproducing the released WM $VERSION artifact"
echo "   recorded SOURCE_DATE_EPOCH : $EPOCH"
echo "   expected SHA-256           : $EXPECTED"

SOURCE_DATE_EPOCH="$EPOCH" "$REPO/scripts/build-paper.sh" >/dev/null

JOBNAME="$(python3 -c "import json;print(json.load(open('$REPO/tooling/toolchain.lock.json'))['jobname'])")"
BUILT="$REPO/build/$JOBNAME.pdf"
GOT="$(shasum -a 256 "$BUILT" | cut -d' ' -f1)"

echo "   built                      : $GOT"

if [[ "$GOT" != "$EXPECTED" ]]; then
  echo "FATAL: the source no longer reproduces the released artifact." >&2
  echo "       expected $EXPECTED" >&2
  echo "       got      $GOT" >&2
  echo "       Either the source, the toolchain or the recorded timestamp has changed." >&2
  echo "       The published bytes are fixed; find what moved rather than updating the digest." >&2
  exit 1
fi

if ! cmp -s "$BUILT" "$REPO/$ARTIFACT"; then
  echo "FATAL: digest matched but bytes differ from $ARTIFACT — the tracked copy is not the release." >&2
  exit 1
fi

echo "reproduce-release: PASS  (source rebuilds the published WM $VERSION artifact byte for byte)"
