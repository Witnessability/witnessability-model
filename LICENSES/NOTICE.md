# Licensing notice

This repository holds two different kinds of work, and they are licensed differently.

The **paper and its publication record** are licensed under
**[Creative Commons Attribution 4.0 International (CC BY 4.0)](CC-BY-4.0.txt)**.

The **software** — build tooling, QA gates, CI — is licensed under
**[Apache License 2.0](Apache-2.0.txt)**.

No single licence covers the whole repository, and none is claimed to. The map below assigns every
tracked path to exactly one licence.

## The map

### CC BY 4.0 — publication material

| Path | What it is |
| --- | --- |
| `paper/` | Paper source: LaTeX, bibliography, metadata, changelogs |
| `model/1.0/WM-1.0.pdf` | The published Version 1.0 artifact |
| `releases/` | Released artifacts, their errata, digests and release records |
| `publication/` | Release policy, versioning, external-publication workflows and records |
| `README.md`, `LICENSES/NOTICE.md` | Repository documentation |

### Apache-2.0 — software

| Path | What it is |
| --- | --- |
| `scripts/` | Build, QA, verification and packaging tooling |
| `tooling/` | Pinned toolchain definition, container build, reproducibility documentation |
| `.github/workflows/` | CI and publication-verification workflows |
| `Makefile`, `.gitignore` | Build entry points and repository configuration |

Every source file in the Apache-2.0 set carries an `SPDX-License-Identifier: Apache-2.0` line, so the
licence travels with the file if it is copied out of the repository. Four cannot: JSON admits no
comments, so `tooling/toolchain.lock.json` and the three JSON records under `publication/` are
governed by this map alone.

## Attribution under CC BY 4.0

CC BY 4.0 requires attribution. Credit the work as deposited:

> Sergeev, Mikhail A. (ORCID [0009-0001-6443-855X](https://orcid.org/0009-0001-6443-855X)) and
> Ikher, Vladimir (ORCID [0009-0000-0084-704X](https://orcid.org/0009-0000-0084-704X)),
> *Toward a Witnessability Model*, Version 1.1, 2026. DOI
> [10.5281/zenodo.21970802](https://doi.org/10.5281/zenodo.21970802).

Those names, in that form, are the creators recorded on the Zenodo deposits for both 1.0 and 1.1.

## This agrees with what is already published

The licence here is not a new decision imposed on published work. Both deposits already carry
`cc-by-4.0`:

| Version | Deposit | Licence field |
| --- | --- | --- |
| 1.0 | Zenodo record [10.5281/zenodo.21824436](https://doi.org/10.5281/zenodo.21824436) | `cc-by-4.0` |
| 1.1 | Zenodo record [10.5281/zenodo.21970802](https://doi.org/10.5281/zenodo.21970802) | `cc-by-4.0` |

Both were read from the Zenodo public API. The deposited 1.1 file is byte-identical to
`releases/1.1/WM-1.1.pdf` (SHA-256 `7d62e326…167fb902`, MD5 `50f0eba9…d853f0`), so the licence
declared on the deposit is the licence of exactly these bytes. Declaring CC BY 4.0 here states in the
repository what the deposit already established; the published bytes are unchanged.

## Third-party material

There is none in the tracked source. No vendored code, no file carrying another party's copyright or
licence header — checked across every tracked file.

Two exceptions exist, and they are the licence texts themselves:

| File | Status |
| --- | --- |
| `LICENSES/CC-BY-4.0.txt` | Verbatim CC BY 4.0 legal code, from creativecommons.org |
| `LICENSES/Apache-2.0.txt` | Verbatim Apache License 2.0 text, from apache.org |

These are reproductions of the licences, not works licensed under them. Both stewards permit verbatim
reproduction and neither permits modification; they are included unchanged and must stay unchanged.

The build toolchain installs Debian-packaged TeX Live components inside a container at build time.
Those carry their own licences and are not redistributed by this repository.

## A note on automatic licence detection

GitHub shows a single licence per repository and infers it from a top-level `LICENSE` file. A
path-scoped repository has no single answer to give it, so the badge may show nothing or show only
one of the two. That is a limitation of the display, not of the licensing: the map above governs.

The model is not distorted to satisfy detection. Adding a top-level `LICENSE` file would state, to
every automated reader, that one licence covers everything here — which is false.
