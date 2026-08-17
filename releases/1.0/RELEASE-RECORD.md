# WM 1.0 — release record (retrospective)

WM 1.0 was released and published **before this repository existed**. This record is retrospective:
it documents an existing release, it does not constitute one, and it does not re-issue anything.

| Field | Value | Evidence |
| ----- | ----- | -------- |
| Title | *Toward a Witnessability Model for AI and Software Execution Systems* — A Boundary-Based Framework for Classifying Execution Evidence | Zenodo public API |
| Model version | 1.0 | — |
| Release status | PUBLISHED | Zenodo record 21824436 |
| Artifact | `releases/1.0/WM-1.0.pdf` | in-repo, immutable |
| Bytes | 213 922 | measured |
| SHA-256 | `295eb6cbe3c9f65f3678253dd803b200b3d36632470fdb592f83279b9379389d` | measured |
| MD5 | `e7fb384458653cccbd254c061915b1e3` | measured; matches Zenodo's reported checksum |
| Zenodo version DOI | `10.5281/zenodo.21824436` | Zenodo public API |
| Zenodo concept DOI | `10.5281/zenodo.21824435` | Zenodo public API |
| Publication date | 2026-06-25 | Zenodo public API |
| Licence | CC BY 4.0 | Zenodo public API |
| SSRN abstract | 6994720, Version 1.0 (June 2026) | WM 1.1 source version-identity table |
| Authors | Sergeev, Mikhail A. (1); Ikher, Vladimir (2) | Zenodo public API |
| Git tag in this repository | NONE | the release predates the repository |
| Source | UNAVAILABLE | LaTeX source for 1.0 was not part of the import |

## Verification performed at import

The bytes in `releases/1.0/WM-1.0.pdf` were checked against the Zenodo deposit by size **and** MD5, and
both matched exactly. Six independent on-disk copies were hashed and were byte-identical.

The artifact begins with the `%PDF` magic. This matters: a page-render ZIP has circulated with a
`.pdf` extension, and any candidate for canonical WM 1.0 must be checked for magic bytes and for
size 213 922 before being treated as authoritative.

## Byte-distinct sibling

WM 1.0 exists as **two** byte-distinct artifacts. The one recorded here is the canonical SSRN/Zenodo
deposit. The other — an arXiv-line PDF labelled "Preprint --- June 2026", v0.5.1 file lineage,
digest stated in the WM 1.1 source as `f3339324…1255e` — is the secondary 1.0 line and is **not**
canonical. Its full digest was not recovered from raw bytes and is recorded as UNAVAILABLE rather
than reconstructed from a prefix.

## Immutability

Nothing in this repository may alter, re-render, re-deposit, or supersede these bytes in place.
WM 1.1 supersedes WM 1.0 only when WM 1.1 is itself released, and supersession is recorded by
addition, never by replacement.
