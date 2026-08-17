#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Assemble the stable human / co-author review package for a release candidate.
#
# It packages what a reviewer needs to judge the candidate and nothing that would imply it is
# released. It sends nothing anywhere: the output is a directory and a checksum file. Transmission
# to a co-author is a separate, explicitly authorized human action.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

LOCK="tooling/toolchain.lock.json"
JOBNAME="$(python3 -c "import json;print(json.load(open('$LOCK'))['jobname'])")"
OUT="build/review-package"

[[ -f "build/$JOBNAME.pdf" ]] || { echo "FATAL: build/$JOBNAME.pdf missing — run 'make paper' first" >&2; exit 2; }

rm -rf "$OUT"; mkdir -p "$OUT/reports" "$OUT/documents" "$OUT/preview"

echo "== assembling review package for $JOBNAME"

cp "build/$JOBNAME.pdf"                         "$OUT/"
cp build/BUILD-MANIFEST.json                    "$OUT/reports/"
for f in QA-REPORT.json QA-SEMANTIC.json REFS-REPORT.json; do
  [[ -f "build/$f" ]] && cp "build/$f" "$OUT/reports/"
done

cp paper/CHANGELOG-WM-1.0-to-1.1.md "$OUT/documents/"
cp paper/CHANGELOG.md                "$OUT/documents/paper-CHANGELOG.md"
cp publication/RELEASE-STATE-PUBLIC.json                  "$OUT/documents/"
cp publication/VERSIONING.md                              "$OUT/documents/"
cp tooling/REPRODUCIBILITY.md                             "$OUT/documents/"

# Page thumbnails: a reviewer should be able to see every page without a LaTeX toolchain.
IMAGE_NAME="$(python3 -c "import json;print(json.load(open('$LOCK'))['image']['name'])")"
case "$(uname -m)" in
  x86_64)        ARCH=amd64 ;;
  aarch64|arm64) ARCH=arm64 ;;
  *)             ARCH="$(uname -m)" ;;
esac
IMAGE_REF="${IMAGE_NAME}:local-${ARCH}"

rm -f build/preview/page-*.png 2>/dev/null || true
mkdir -p build/preview
if docker run --rm -v "$REPO/build:/b" -w /b "$IMAGE_REF" \
     pdftoppm -png -r 72 "$JOBNAME.pdf" preview/page 2>/dev/null; then
  cp build/preview/page-*.png "$OUT/preview/"
  echo "   thumbnails: $(ls -1 "$OUT/preview" | wc -l | tr -d ' ') pages"
else
  echo "   (thumbnails skipped — $IMAGE_REF not available)"
fi

# Baseline comparison, so the reviewer never has to take the delta on trust.
if [[ -f releases/1.1/WM-1.1.pdf ]]; then
  cp releases/1.1/WM-1.1.pdf "$OUT/BASELINE-WM-1.1.pdf"
fi

python3 - "$OUT" "$JOBNAME" <<'PY'
import hashlib, json, pathlib, subprocess, sys
out, jobname = pathlib.Path(sys.argv[1]), sys.argv[2]
repo = pathlib.Path.cwd()

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True).stdout.strip()

manifest = {
    "package": "WM 1.1 RC001 co-author review package",
    "status": "REVIEW CANDIDATE — NOT RELEASED, NOT SUBMITTED, NOT DEPOSITED",
    "git_commit": git("rev-parse", "HEAD"),
    "git_tree": git("rev-parse", "HEAD^{tree}"),
    "candidate": {
        "pdf": f"{jobname}.pdf",
        "pdf_sha256": sha(out / f"{jobname}.pdf"),
        "pdf_bytes": (out / f"{jobname}.pdf").stat().st_size,
        "source_sha256": sha(repo / "paper/src/main.tex"),
        "bibliography_sha256": sha(repo / "paper/bibliography/references.bib"),
    },
    "baseline": (
        {
            "pdf": "BASELINE-WM-1.1.pdf",
            "pdf_sha256": sha(out / "BASELINE-WM-1.1.pdf"),
            "note": "prior artifact, included so the delta can be checked rather than re-derived",
        }
        if (out / "BASELINE-WM-1.1.pdf").exists() else "NOT_APPLICABLE"
    ),
    "not_included_because_not_true": [
        "release tag", "GitHub release", "SSRN submission", "Zenodo deposit",
        "co-author approval", "release authorization",
    ],
}
(out / "PACKAGE-MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")

lines = []
for p in sorted(out.rglob("*")):
    if p.is_file() and p.name != "SHA256SUMS":
        lines.append(f"{sha(p)}  {p.relative_to(out)}")
(out / "SHA256SUMS").write_text("\n".join(lines) + "\n")
print(f"   {len(lines)} files, candidate sha256={manifest['candidate']['pdf_sha256']}")
PY

cat > "$OUT/README.md" <<'EOF'
# Witnessability Model — publication candidate review package

**This is a candidate. It is not released.** No tag exists, no release exists, nothing has been
submitted or deposited, and release is not authorized.

## Contents

- the candidate PDF, and every page as an image in `preview/`
- `documents/CHANGELOG-WM-1.0-to-1.1.md` — what changed against the published Version 1.0
- `documents/paper-CHANGELOG.md` — changes by class: semantic, editorial, build, references
- `documents/REPRODUCIBILITY.md` — the toolchain and what its determinism claim rests on
- `documents/RELEASE-STATE-PUBLIC.json` — the four release states, all `PENDING`
- `reports/` — machine-generated QA output, re-runnable from this repository
- `BASELINE-*.pdf` and `source-delta.diff` where a prior artifact exists, so the delta need not be
  taken on trust

## Verifying

`SHA256SUMS` covers every file. `PACKAGE-MANIFEST.json` binds the candidate to its commit and tree.
Everything here is reproducible with `make paper && make review-package`.
EOF

echo "== review package: $OUT"
