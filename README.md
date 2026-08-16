# Witnessability Model

Canonical, reproducible publication repository for the **Witnessability Model (WM)** and its
accompanying paper.

> **Status of this repository:** infrastructure preparation. The WM 1.1 objects held here are
> **unreleased review baselines** under an **active release hold**. Nothing in this repository
> constitutes a release, a deposit, or a publication.

## Repository role

This repository owns three things and nothing else:

1. **Model source** — the Witnessability Model versions and their paper source.
2. **Reproducible paper build** — a repository-owned, pinned toolchain that turns source into a PDF.
3. **Release provenance** — the records that bind a model version to an exact artifact and to its
   external publication receipts.

It is explicitly **not**:

- the Witnessability Conceptual Core repository (`witnessability-core`);
- the Witnessed Execution Protocol repository (`WEXP-dev`);
- a product repository;
- the sole normative authority for Witnessability;
- an SSRN mirror.

| Repository               | Scope                                              |
| ------------------------ | -------------------------------------------------- |
| `witnessability-core`    | Witnessability Conceptual Core                      |
| `witnessability-model`   | Witnessability Model + paper + release records      |
| `witnessability-research`| Research / preregistration / experiments (if created) |
| `WEXP-dev`               | Downstream protocol engineering                     |

## The identity rule

The single rule this repository exists to enforce:

```
SOURCE  ≠  BUILD OUTPUT  ≠  RELEASE ARTIFACT  ≠  EXTERNAL PUBLICATION RECORD
```

Every one of those four is a distinct object with its own identity (its own SHA-256), its own
location, and its own lifecycle. They are never conflated, never overwritten with one another, and
never silently promoted from one role to the next.

| Identity                     | Lives in                        | Mutable?                  |
| ---------------------------- | ------------------------------- | ------------------------- |
| Source                       | `paper/witnessability-model/`   | yes, via reviewed changes |
| Import baseline              | `model/<version>/`              | **never**                 |
| Build output                 | `build/` (git-ignored)          | regenerated               |
| Release artifact             | `releases/<version>/`           | **never**, once released  |
| External publication record  | `publication/`                  | append-only               |

## Layout

```
model/                          immutable imported baselines, by model version
  1.0/                          canonical published WM 1.0 artifact
  1.1/                          WM 1.1 review baseline (UNRELEASED)
paper/witnessability-model/     working source lineage
  src/main.tex                  paper source
  bibliography/references.bib   bibliography source of truth
  figures/                      figure sources (none yet; the paper is TikZ-only)
  metadata.yaml                 title, authors, ORCIDs, keywords, version identity
  CHANGELOG.md                  paper-revision changelog
releases/                       release artifacts and receipts, by version
tooling/                        pinned toolchain definition (image + digest)
scripts/                        build and QA entry points
schemas/                        JSON schemas for manifests
publication/                    governance, workflows, baselines, QA reports
.github/workflows/              CI, release-candidate, inert release, verification
build/                          build output only — git-ignored, never a source
```

## Build

The build never uses an ambient TeX installation. It runs inside a container image pinned by
digest in [`tooling/toolchain.lock.json`](tooling/toolchain.lock.json).

```bash
make paper      # build into build/
make qa         # run all QA gates against the built PDF
make verify     # verify imported baselines still match their recorded digests
make all        # paper + qa + verify
```

Every build emits `build/BUILD-MANIFEST.json` binding source digests, toolchain identity,
environment, and output digest.

## Versioning

Three identities are tracked separately and must never be collapsed:

- **Model version** — e.g. Witnessability Model 1.1
- **Paper revision** — the revision of *Toward a Witnessability Model…* corresponding to it
- **Release artifact** — the exact bytes released, identified by SHA-256

See [`publication/VERSIONING.md`](publication/VERSIONING.md) for the tag naming convention.

## Current state

| Item | State |
| ---- | ----- |
| WM 1.0 | Published. Canonical artifact imported as historical baseline. Not modifiable. |
| WM 1.1 | **UNRELEASED REVIEW BASELINE — RELEASE HOLD ACTIVE** |
| Release tag | none |
| GitHub release | none |
| SSRN revision | not submitted |
| Zenodo deposit | not made |

WM 1.1 release blockers are tracked in
[`publication/RELEASE-STATE-PUBLIC.json`](publication/RELEASE-STATE-PUBLIC.json), which carries four
generic states. No state may be `PASS` without the corresponding prerequisites being satisfied.

## Licensing

See [`LICENSES/`](LICENSES/). The paper text and the repository tooling are licensed separately;
`LICENSES/NOTICE.md` states which licence applies to which path.
