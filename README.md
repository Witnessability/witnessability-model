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
| Release | tag [`wm-v1.1.0`](https://github.com/Witnessability/witnessability-model/releases/tag/wm-v1.1.0), released 2026-08-16 |
| Source | [`paper/witnessability-model/src/main.tex`](paper/witnessability-model/src/main.tex) |
| Build it yourself | `make reproduce-release` — rebuilds the released PDF and checks it is the published bytes |
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
LICENSES/                       licence texts and the path-to-licence map
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
make paper              # build the current source into build/
make reproduce-release  # rebuild the released artifact and prove it is the published bytes
make qa                 # run all QA gates against the built PDF
make verify             # verify published artifacts still match their recorded digests
make all                # paper + qa + verify
```

Every build emits `build/BUILD-MANIFEST.json` binding source digests, toolchain identity,
environment, and output digest.

`make paper` builds *the current source*, and its timestamp comes from the last commit that touched
`paper/`. Reproducing a *past release* is a different operation: the release's timestamp is recorded
with the release, and `make reproduce-release` uses it, then compares the result against the
published bytes.

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
| Licensing | CC BY 4.0 (paper) · Apache-2.0 (software) — map in `LICENSES/NOTICE.md` |

Release state is machine-readable in
[`publication/RELEASE-STATE-PUBLIC.json`](publication/RELEASE-STATE-PUBLIC.json): four generic
states, all `PASS` for 1.1, plus the release identities.

## Licensing

Two kinds of work live here and they are licensed separately:

| | Licence | Covers |
| --- | --- | --- |
| **Paper and publication record** | [CC BY 4.0](LICENSES/CC-BY-4.0.txt) | `paper/`, `model/`, `releases/`, `publication/`, this README |
| **Software** | [Apache-2.0](LICENSES/Apache-2.0.txt) | `scripts/`, `tooling/`, `.github/workflows/`, `Makefile` |

No single licence covers the repository, so there is no top-level `LICENSE` file and GitHub's licence
badge may show nothing — the structure is not bent to satisfy automatic detection.
[`LICENSES/NOTICE.md`](LICENSES/NOTICE.md) is authoritative: it maps every tracked path to exactly one
licence, states the attribution required by CC BY 4.0, and records the licence texts as the only
third-party material present.

The paper's CC BY 4.0 is not a new decision — it is what both Zenodo deposits already declare.
