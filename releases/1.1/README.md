# Witnessability Model 1.1 — released

| | |
| --- | --- |
| Version | 1.1 (bridge revision of the 1.0 line) |
| Released | 2026-08-16 |
| Version DOI | [10.5281/zenodo.21970802](https://doi.org/10.5281/zenodo.21970802) |
| Concept DOI | [10.5281/zenodo.21824435](https://doi.org/10.5281/zenodo.21824435) — resolves to the latest version |
| GitHub release tag | `wm-v1.1.0` |
| Release commit | `e4f3985a6d1ebcdbe9920bebbc8ba86702e34969` |

## Files here

| File | Bytes | SHA-256 |
| --- | --- | --- |
| `WM-1.1.pdf` | 490 909 | `7d62e3268e930d5ad16aa97bd05eb037e15a08274487194041cafd78167fb902` |
| `WM-1.1-ERRATA-SCHEME-B-FINAL.md` | 9 397 | `8ae0ac5f7ff46aac25770888e5194f276acb48eaeb21949135f5c2fab15450b9` |

`SHA256SUMS.txt` carries the same digests in checkable form:

```
shasum -a 256 -c SHA256SUMS.txt
```

## Relationship to the GitHub release and the Zenodo deposit

The PDF here is **the same object**, byte for byte, as:

- the `WM-1.1.pdf` asset of GitHub release `wm-v1.1.0`, and
- the file deposited at Zenodo under version DOI `10.5281/zenodo.21970802`
  (MD5 `50f0eba967840a67d3e7a04786d853f0`, confirmed against both).

It is tracked here so that a reader can obtain the published paper directly from the repository,
without needing to know that GitHub keeps release assets on a separate page. It is a **copy for
discoverability**, not a second edition:

- **Zenodo** is the archival copy of record and the citable one.
- **The GitHub release** is the distribution copy.
- **This copy** is the discoverable one, bound into git history together with its digest.

If the three ever disagree, Zenodo is authoritative. `scripts/verify-baselines.sh` fails the build
if the tracked copy stops matching the published digest, so a silent divergence cannot survive CI.

## Errata

`WM-1.1-ERRATA-SCHEME-B-FINAL.md` states the correction from the published Version 1.0 to the
Version 1.1 semantics: which passages of 1.0 are affected, their corrected wording, and the
consequences for the WL naming vocabulary. It is part of the release record and applies to the PDF
above.

## Source

The source this artifact was built from is in
[`../../paper/witnessability-model/`](../../paper/witnessability-model/), at release commit
`e4f3985a`. The build is deterministic, and reproducing *this* artifact is a single command:

```
make reproduce-release
```

It rebuilds from source at the timestamp recorded with the release and fails unless the result is
these exact bytes. Verified on `linux/amd64` and `linux/arm64`.

Plain `make paper` is not the same operation: it builds the current source, taking its timestamp from
the last commit that touched `paper/`, so any later commit there changes the output bytes. That is
correct for building what the tree says now and useless for reproducing what was published — hence
the separate command. See [`../../tooling/REPRODUCIBILITY.md`](../../tooling/REPRODUCIBILITY.md).

## Version 1.0

Version 1.0 remains published and is not superseded by deletion — see
[`../1.0/RELEASE-RECORD.md`](../1.0/RELEASE-RECORD.md).
