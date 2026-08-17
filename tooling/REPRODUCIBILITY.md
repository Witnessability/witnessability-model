# Reproducibility — what is proven and what is not

This document exists so that no one has to guess how strong the reproducibility claim is. The claim
is stated at exactly the strength the evidence supports, and no higher.

## The three distinct questions

They are routinely conflated. They are not the same question and they do not have the same answer.

| # | Question | Answer |
| - | -------- | ------ |
| 1 | Does the pipeline produce byte-identical output when run twice in the same environment? | **YES** — gated in CI |
| 2 | Does the pipeline produce byte-identical output on macOS arm64 and Linux amd64? | **YES — proven** |
| 3 | Does the pipeline reproduce the imported WM 1.1 baseline PDF byte for byte? | **NO — and it is not expected to** |

Question 2 was `NOT YET PROVEN` until the comparison was actually run. It is now proven, at commit
`5458ee7`, `SOURCE_DATE_EPOCH=1786868784`:

| Platform | Where | SHA-256 |
| --- | --- | --- |
| `linux/arm64` | macOS Apple Silicon, Docker Desktop | `bb20aef5feb6b359a745191909afc578ce1be46f0b0eba0e4d930ae661f1e024` |
| `linux/amd64` | GitHub Actions `ubuntu-latest` | `bb20aef5feb6b359a745191909afc578ce1be46f0b0eba0e4d930ae661f1e024` |

Same bytes. Notably, the font subset tags — the divergence candidate that usually breaks this — are
identical too, so `xdvipdfmx` derives them from content rather than from anything platform-bound.

Getting there took two fixes, both found by running the comparison rather than reasoning about it:
the timestamp source (see below) and a shallow CI clone. Neither would have been visible in a
single-platform build, which is the argument for gating this rather than testing it once.

## Question 3 — why the imported baseline cannot be reproduced

The imported `WM-1.1.pdf` was produced on 2026-07-30 by `xdvipdfmx (0.1)` on an unknown machine with
an unknown TeX Live installation. Reproducing those exact bytes would require reconstructing that
installation, which was never recorded.

This is not a defect in the baseline and not a failure of the pipeline. It is the reason the
pipeline exists: from the first build produced here onward, the environment **is** recorded, in
`build/BUILD-MANIFEST.json`, and the question becomes answerable.

The imported baseline is therefore not tracked here at all: it is identified by digest in
`paper/CHANGELOG.md`, and nothing in this repository is claimed to be it.

## Reproducing a release is not the same as building the source

`SOURCE_DATE_EPOCH` is derived from the last commit that touched `paper/`. For building the current
source that is exactly right — the output moves when the paper moves, and not otherwise.

It is the wrong input for reproducing a *published* artifact. Any later commit touching `paper/`
advances the timestamp and therefore the bytes, even a commit that changes no text at all: removing
an empty `figures/.gitkeep` placeholder moved the epoch from `1786879871` to `1786923086` and the
built PDF from `7d62e326…167fb902` to `672efce0…72be2975`. Same source, same toolchain, different
bytes.

So the release's timestamp is recorded *with the release*, in
`publication/RELEASE-STATE-PUBLIC.json` under `release.reproduction`, and `make reproduce-release`
builds with it and fails unless the result is the published bytes. Reproducing what was published is
a claim this repository can check on demand rather than a property it hopes it still has.

## Platform default

`BUILD_PLATFORM` selects the image architecture. Unset, the build now follows the host: a fixed
default is a trap, because on the other architecture it builds an image the host cannot execute and
the failure arrives as `exec /bin/sh: exec format error` from inside `apt`, which points at nothing.
CI sets it explicitly on every step regardless, so the platform is stated rather than inferred where
it matters. Cross-building stays possible and stays deliberate.

## A constraint that must not be tidied away

**The build jobname is load-bearing for the released artifact.** `tooling/toolchain.lock.json` sets
`jobname` to `WM-1.1-RC002`, and that string reaches the PDF: rebuilding the release commit with
`jobname` changed to `WM-1.1` produces `a6663a56…d52060` instead of the published
`7d62e326…167fb902`. Same source, same toolchain, same timestamp — different bytes.

The name therefore looks like a leftover from the candidate stage and is not one. Renaming it for
tidiness would silently end the repository's ability to reproduce the artifact it published, which
is the one property the release record depends on. Measured, not assumed: the substitution was tried
and reverted.

If the name is ever to change, it changes for the *next* release, together with a new artifact.

## Determinism measures in place

- **Timestamps.** `SOURCE_DATE_EPOCH` is the commit time of the last commit touching `paper/`,
  never the clock and never `HEAD`, and `FORCE_SOURCE_DATE=1` makes the TeX engine honour it. The
  PDF creation date is a function of the document.

  It was `HEAD`'s commit time until CI disproved that choice: a `pull_request` build checks out a
  synthetic merge commit whose timestamp differs from the branch commit, so the same source
  produced two different PDFs on two platforms for no reason but the checkout mechanism. That is
  the class of bug this document exists to catch, and it was caught by running the comparison
  rather than by asserting the property.
- **Paths.** The build runs in a fixed container working directory `/work`. Host paths cannot enter
  the output because the container never sees one.
- **Locale and timezone.** `LANG`/`LC_ALL=C.UTF-8`, `TZ=UTC`, fixed in both the image and the run.
- **Toolchain.** Built from `tooling/Dockerfile`, whose base image is pinned by multi-arch index
  digest. The package set is explicit and reviewable.
- **Fonts.** Latin Modern from the `lmodern` package, embedded as subsets. Font subsetting is a
  known source of nondeterminism across TeX versions; this is why the toolchain is pinned rather
  than merely specified.
- **The QA extractor is pinned too.** `tooling/qa-run.sh` runs the gates inside the same image, so
  `pdftotext` has one version everywhere. Findings E-01 and H-02 turn on how the extractor treats
  unmapped glyphs, so a gate running against whatever poppler a machine happens to have is not a
  gate.

## Proven so far

| Property | Result | Evidence |
| --- | --- | --- |
| Two builds, same environment, same path | **byte-identical** | run locally and gated in CI |
| Two builds, same commit, **different checkout paths** | **byte-identical** | a working tree and a fresh clone at a different path produce the same digest |
| macOS arm64 vs Linux amd64 | pending | see below |

The different-path result is the one that proves no host path leaks into the output. It is a
stronger check than rebuilding in place, and it is why the build stages sources into a fixed
container path instead of mounting the repository directly.

**A rewritten commit changes the digest, by design.** An earlier pair of runs proved the same
property at digest `8558f182…479647ed` before the branch was rebased. The rebase gave the commit
touching `paper/` a new committer date, so `SOURCE_DATE_EPOCH` moved and the bytes moved with it.
That is the timestamp policy working, not failing: the PDF is a function of the commit, so a
different commit is a different artifact. It is also the reason a release manifest binds a digest to
a commit — a digest quoted without its commit means nothing.

## Question 1 — same-environment determinism

`.github/workflows/ci.yml` builds twice in the same job and compares the two PDFs byte for byte.
A difference fails CI. This is the cheapest reproducibility property to hold and the first to break
when something non-deterministic is introduced, so it is enforced continuously rather than tested
once.

## Question 2 — cross-platform determinism

Status: **PROVEN** (digests above). Re-verified on every CI run, and re-checkable locally at any
time with the procedure below.

The comparison requires the same commit built on:

- local macOS arm64, via `linux/arm64`;
- Linux x86_64, via `linux/amd64` (GitHub Actions `ubuntu-latest`).

The procedure:

```bash
BUILD_PLATFORM=linux/arm64 ./tooling/build-paper.sh && cp build/WM-1.1.pdf /tmp/arm64.pdf
BUILD_PLATFORM=linux/amd64 ./tooling/build-paper.sh && cp build/WM-1.1.pdf /tmp/amd64.pdf
cmp /tmp/arm64.pdf /tmp/amd64.pdf
```

Candidates to check first if a future change breaks it:

1. TeX binary version differences between the arm64 and amd64 Debian builds.
2. Font subset tags — `xdvipdfmx` derives the six-letter subset prefix (e.g. `MYLVOM+`) from a hash;
   if the input to that hash ever includes anything platform-dependent, every font object differs
   while the rendered pages stay identical.
3. Floating-point differences in TikZ coordinate computation.
4. Compression-level differences in the zlib build used by the engine.
5. **Shallow clone.** Fixed, and `build-paper.sh` now refuses one outright: with `depth=1` the
   commit that last touched `paper/` is absent, so git reports the checkout commit and the
   timestamp follows the CI mechanism instead of the document.

If bytes ever differ, the correct outcome is to identify **which** of these it is and normalise it —
not to weaken the claim to "reproducible enough".

## How the claim is recorded

`build/BUILD-MANIFEST.json` records one build; it never asserts reproducibility by itself. The
release manifest field `toolchain_digest.reproducibility.byte_identical_across_platforms` carries
`true`, `false`, or `NOT_YET_PROVEN`, and `platforms_compared` lists what was actually compared.
