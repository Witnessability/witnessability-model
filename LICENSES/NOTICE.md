# Licensing notice

Different parts of this repository are licensed differently. This file states which licence applies
to which path. Where a licence is not yet decided, that is stated as PENDING rather than guessed.

| Path | Content | Licence |
| ---- | ------- | ------- |
| `model/1.0/` | Published WM 1.0 artifact | CC BY 4.0 — as deposited on Zenodo (record 21824436) |
| `model/1.1/` | WM 1.1 review baseline, unreleased | **PENDING** — author decision, recorded before release |
| `paper/` | Paper source (LaTeX, bibliography, metadata) | **PENDING** — follows the released paper licence |
| `scripts/`, `tooling/`, `schemas/`, `.github/` | Build and QA tooling | **PENDING** — proposed: MIT |
| `publication/` | Governance, workflow and provenance records | **PENDING** — proposed: CC BY 4.0 |

## Why PENDING and not a default

The licence asserted on SSRN, the licence asserted on Zenodo, and the licence in this repository
must be the same for a given artifact. WM 1.0 was deposited under CC BY 4.0. The WM 1.1 licence is
an author decision that has not been recorded, and inventing one here would create exactly the kind
of cross-venue divergence `publication/RELEASE-POLICY.md` exists to prevent.

No release may proceed while any licence field relevant to the released artifact is PENDING.

## Third-party material

The paper cites third-party work but vendors none. The build toolchain installs Debian-packaged TeX
Live components inside a container at build time; those carry their own licences and are not
redistributed by this repository.
