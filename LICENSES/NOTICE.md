# Licensing notice

Different parts of this repository are licensed differently. This file states which licence applies
to which path. Where a licence has not been declared, that is stated plainly rather than guessed.

| Path | Content | Licence |
| ---- | ------- | ------- |
| `releases/1.1/WM-1.1.pdf` | The released Version 1.1 paper | **CC BY 4.0** |
| `releases/1.1/WM-1.1-ERRATA-SCHEME-B-FINAL.md` | Errata for the released paper | **CC BY 4.0** — released with the paper |
| `model/1.0/WM-1.0.pdf` | The published Version 1.0 paper | **CC BY 4.0** |
| `paper/` | Paper source: LaTeX, bibliography, metadata | **CC BY 4.0** — the source of the CC BY 4.0 paper |
| `releases/1.0/`, `publication/` | Release records, policy and workflow documentation | **NOT DECLARED** |
| `scripts/`, `tooling/`, `.github/`, `Makefile` | Build and QA tooling | **NOT DECLARED** |

## Basis for the paper licence

Not a default and not an inference. Both released papers are deposited under CC BY 4.0, and the
deposit records are the primary evidence:

| Version | Deposit | Licence field |
| --- | --- | --- |
| 1.0 | Zenodo record `10.5281/zenodo.21824436` | `cc-by-4.0` |
| 1.1 | Zenodo record `10.5281/zenodo.21970802` | `cc-by-4.0` |

Both were read directly from the Zenodo public API. The deposited 1.1 file is byte-identical to
`releases/1.1/WM-1.1.pdf` (SHA-256 `7d62e326…167fb902`, MD5 `50f0eba9…d853f0`), so the licence
declared on the deposit is the licence of exactly these bytes.

The paper source in `paper/` carries the same licence as the paper it produces: it is the same work
in editable form, and a build of it is byte-identical to the deposited artifact.

## What is not declared, and what that means today

**The repository has no `LICENSE` file, and its GitHub licence metadata is empty.** For the paths
marked NOT DECLARED — the tooling, the release records and the publication documentation — a reader
therefore has no granted permission to copy, modify or redistribute them. Default copyright applies.

This is a gap, not a decision. It does not affect the paper: the paper's licence is established
above and travels with the artifact through Zenodo regardless of what this repository declares.

`publication/RELEASE-POLICY.md` §5 requires that no release proceed while a licence field relevant
to the released artifact is undeclared. For the released artifact that condition is met — the paper
is CC BY 4.0. It is the *repository's own* licence that remains open.

## Third-party material

The paper cites third-party work but vendors none. The build toolchain installs Debian-packaged TeX
Live components inside a container at build time; those carry their own licences and are not
redistributed by this repository.
