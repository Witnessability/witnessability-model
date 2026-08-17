#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Build the paper from a clean checkout using the repository-owned, digest-pinned toolchain.
#
# The ambient TeX installation is never used. If Docker is unavailable, this script fails; it does
# not silently fall back to a host TeX, because a host build is not the pipeline's build.
#
# Output goes to build/ only. Nothing is ever written into a source directory.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK="$REPO/tooling/toolchain.lock.json"
SRC="$REPO/paper/witnessability-model"
OUT="$REPO/build"

jqget() { python3 -c "import json,sys;print(json.load(open('$LOCK'))$1)"; }

IMAGE_NAME="$(jqget "['image']['name']")"
ENGINE="$(jqget "['engine']")"
PLATFORM="${BUILD_PLATFORM:-$(jqget "['default_platform']")}"
JOBNAME="$(jqget "['jobname']")"

# One image per platform, built from this repository's Dockerfile. The tag encodes the
# architecture so an amd64 build can never silently run an arm64 image or the reverse.
IMAGE_REF="${IMAGE_NAME}:local-${PLATFORM##*/}"

# latexmk selects the engine by flag, and the flag name is not the engine name: pdflatex is -pdf,
# and a bare -pdflatex would be read as the "set the pdflatex command" option with an empty value.
case "$ENGINE" in
  pdflatex) ENGINE_FLAG="-pdf" ;;
  xelatex)  ENGINE_FLAG="-xelatex" ;;
  lualatex) ENGINE_FLAG="-lualatex" ;;
  *) echo "FATAL: unsupported engine '$ENGINE' in toolchain.lock.json" >&2; exit 2 ;;
esac

# Deterministic timestamp: when the PAPER last changed, not when HEAD was written.
#
# Using HEAD's commit time looked right until CI proved otherwise: a pull_request build checks out
# a synthetic merge commit whose timestamp differs from the branch commit, so the same source
# produced two different PDFs on two platforms for no reason but the checkout mechanism. Deriving
# it from the last commit touching paper/ makes the timestamp a function of the document, which is
# what it was supposed to be all along.
if [[ -n "${SOURCE_DATE_EPOCH:-}" ]]; then
  : # caller supplied it
elif git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1 \
     && [[ -n "$(git -C "$REPO" log -1 --format=%ct -- paper/ 2>/dev/null)" ]]; then

  # A shallow clone does not contain the commit that last touched paper/, so git silently reports
  # the checkout commit instead and the timestamp — and therefore the PDF — changes. Refuse rather
  # than produce bytes that look reproducible and are not.
  if [[ "$(git -C "$REPO" rev-parse --is-shallow-repository 2>/dev/null)" == "true" ]]; then
    echo "FATAL: shallow clone. SOURCE_DATE_EPOCH would be taken from the checkout commit," >&2
    echo "       not from the paper's own history, and the build would not be reproducible." >&2
    echo "       Fix: git fetch --unshallow   (in CI: actions/checkout with fetch-depth: 0)" >&2
    echo "       Or set SOURCE_DATE_EPOCH explicitly if you know what you are doing." >&2
    exit 2
  fi
  SOURCE_DATE_EPOCH="$(git -C "$REPO" log -1 --format=%ct -- paper/)"
else
  SOURCE_DATE_EPOCH="$(jqget "['fallback_source_date_epoch']")"
fi
export SOURCE_DATE_EPOCH

echo "== witnessability-model paper build"
echo "   image      : $IMAGE_REF"
echo "   platform   : $PLATFORM"
echo "   engine     : $ENGINE"
echo "   SOURCE_DATE_EPOCH: $SOURCE_DATE_EPOCH"

command -v docker >/dev/null 2>&1 || { echo "FATAL: docker not available; pinned toolchain cannot run" >&2; exit 2; }

if ! docker image inspect "$IMAGE_REF" >/dev/null 2>&1; then
  echo "== toolchain image $IMAGE_REF absent; building it from tooling/Dockerfile"
  docker build --platform "$PLATFORM" -t "$IMAGE_REF" -f "$REPO/tooling/Dockerfile" "$REPO/tooling/"
fi

rm -rf "$OUT"
mkdir -p "$OUT"

# Stage sources into a flat, path-stable working directory. The container always sees /work,
# regardless of where the repository lives on the host, so no host path can leak into the PDF.
STAGE="$OUT/.stage"
mkdir -p "$STAGE"
cp "$SRC/src/main.tex" "$STAGE/$JOBNAME.tex"
cp "$SRC/bibliography/references.bib" "$STAGE/references.bib"
if compgen -G "$SRC/figures/*" >/dev/null; then cp -R "$SRC/figures/." "$STAGE/"; fi

docker run --rm \
  --platform "$PLATFORM" \
  -v "$STAGE:/work" \
  -w /work \
  -e SOURCE_DATE_EPOCH="$SOURCE_DATE_EPOCH" \
  -e FORCE_SOURCE_DATE=1 \
  -e TZ=UTC \
  -e LANG=C.UTF-8 \
  -e LC_ALL=C.UTF-8 \
  "$IMAGE_REF" \
  latexmk "$ENGINE_FLAG" -interaction=nonstopmode -halt-on-error -file-line-error \
          -jobname="$JOBNAME" "$JOBNAME.tex" \
  > "$OUT/build.log" 2>&1 || {
    echo "FATAL: build failed — see build/build.log" >&2
    tail -40 "$OUT/build.log" >&2
    exit 1
  }

cp "$STAGE/$JOBNAME.pdf" "$OUT/$JOBNAME.pdf"
# Keep the LaTeX .log next to our driver log; QA parses the LaTeX one.
cp "$STAGE/$JOBNAME.log" "$OUT/$JOBNAME.latex.log"

python3 "$REPO/scripts/make-build-manifest.py" \
  --pdf "$OUT/$JOBNAME.pdf" \
  --platform "$PLATFORM" \
  --source-date-epoch "$SOURCE_DATE_EPOCH"

echo "== built: build/$JOBNAME.pdf"
shasum -a 256 "$OUT/$JOBNAME.pdf" 2>/dev/null || sha256sum "$OUT/$JOBNAME.pdf"
