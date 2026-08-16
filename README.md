# Witnessability Model

Canonical, reproducible publication repository for the **Witnessability Model (WM)** and its
accompanying paper.

## Witnessability Model 1.1 — current released version

| | |
| --- | --- |
| **Read the paper** | **[`releases/1.1/WM-1.1.pdf`](releases/1.1/WM-1.1.pdf)** — 25 pages |
| **Cite this version** | **[10.5281/zenodo.21970802](https://doi.org/10.5281/zenodo.21970802)** |
| Cite the work as a whole | [10.5281/zenodo.21824435](https://doi.org/10.5281/zenodo.21824435) — concept DOI, always resolves to the latest version |
| Errata | [`releases/1.1/WM-1.1-ERRATA-SCHEME-B-FINAL.md`](releases/1.1/WM-1.1-ERRATA-SCHEME-B-FINAL.md) |
| Release | tag [`wm-v1.1.0`](../../releases/tag/wm-v1.1.0), released 2026-08-16 |
| Source | [`paper/witnessability-model/src/main.tex`](paper/witnessability-model/src/main.tex) |
| Build it yourself | `make paper` — reproduces the released PDF byte for byte |
| Release record | [`releases/1.1/README.md`](releases/1.1/README.md) |

The previous version remains published: [`releases/1.0/RELEASE-RECORD.md`](releases/1.0/RELEASE-RECORD.md),
DOI [10.5281/zenodo.21824436](https://doi.org/10.5281/zenodo.21824436).

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
model/1.0/WM-1.0.pdf            the published Version 1.0 artifact, kept for provenance
paper/witnessability-model/     working source lineage
  src/main.tex                  paper source
  bibliography/references.bib   bibliography source of truth
  figures/                      figure sources (none yet; the paper is TikZ-only)
  metadata.yaml                 title, authors, ORCIDs, keywords, version identity
  CHANGELOG.md                  paper-revision changelog
releases/                       released artifacts and their records, by version
  1.0/                          record of the published 1.0 release
  1.1/                          the released PDF, its errata and their digests
tooling/                        pinned toolchain definition (image + digest)
scripts/                        build and QA entry points
publication/                    governance, workflows, baselines, QA reports
.github/workflows/              CI and read-only publication verification
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
| WM 1.0 | Published 2026-06-25 · DOI 10.5281/zenodo.21824436 · not modifiable |
| WM 1.1 | **Published 2026-08-16** · DOI 10.5281/zenodo.21970802 |
| Release tag | `wm-v1.1.0` |
| GitHub release | Witnessability Model 1.1 |
| Zenodo deposit | made — new version under the same concept DOI |
| Repository licence | **not yet declared** — see `LICENSES/NOTICE.md` |

Release state is machine-readable in
[`publication/RELEASE-STATE-PUBLIC.json`](publication/RELEASE-STATE-PUBLIC.json): four generic
states, all `PASS` for 1.1, plus the release identities.

## Licensing

See [`LICENSES/`](LICENSES/). The paper text and the repository tooling are licensed separately;
`LICENSES/NOTICE.md` states which licence applies to which path.
