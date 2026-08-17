#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Run the QA gates inside the pinned toolchain image.
#
# The gates are never run against the host's poppler. A text-extraction gate whose extractor
# version varies by machine is not a gate — it is a coin flip: pdftotext's handling of unmapped
# glyphs is exactly what findings E-01 and H-02 turn on. The image pins the extractor along with
# the engine, so a finding means the same thing on a laptop and on a runner.
#
# Usage: tooling/qa-run.sh [arguments passed through to tooling/qa.py]

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK="$REPO/tooling/toolchain.lock.json"

IMAGE_NAME="$(python3 -c "import json;print(json.load(open('$LOCK'))['image']['name'])")"
PLATFORM="${BUILD_PLATFORM:-$(python3 -c "import json;print(json.load(open('$LOCK'))['default_platform'])")}"
IMAGE_REF="${IMAGE_NAME}:local-${PLATFORM##*/}"

command -v docker >/dev/null 2>&1 || { echo "FATAL: docker required to run the pinned QA gates" >&2; exit 2; }

if ! docker image inspect "$IMAGE_REF" >/dev/null 2>&1; then
  echo "== toolchain image $IMAGE_REF absent; building it"
  docker build --platform "$PLATFORM" -t "$IMAGE_REF" -f "$REPO/tooling/Dockerfile" "$REPO/tooling/"
fi

exec docker run --rm \
  --platform "$PLATFORM" \
  -v "$REPO:/repo" \
  -w /repo \
  -e LC_ALL=C.UTF-8 \
  -e LANG=C.UTF-8 \
  "$IMAGE_REF" \
  python3 tooling/qa.py "$@"
