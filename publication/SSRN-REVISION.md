# SSRN revision — the procedure as executed

This describes what was actually done, once, on 2026-08-17, when SSRN record `6994720` was revised
from Witnessability Model 1.0 to 1.1. Every value here was measured after the fact rather than
planned before it. Where the platform behaved in a way worth knowing, that is recorded as observed
behaviour on that revision — not as a rule about SSRN in general.

## The record

There is one SSRN record for this paper: abstract `6994720`. A revision **updates that record in
place**. It does not create a new paper, and a new paper must never be created for a new version —
doing so would split the citation line and the download history, and it cannot be undone from
outside SSRN.

SSRN mints its own identifier for the record, `10.2139/ssrn.6994720`. It is not the Zenodo DOI and
the two are not interchangeable: SSRN's identifies the record, Zenodo's identifies the exact
deposited bytes.

## Upload the released artifact, unchanged

The file uploaded is the released artifact itself — not a rebuild, not a re-save, not a re-render.
The point of the release identity is that one set of bytes is the paper; a helpfully regenerated PDF
would be a different object wearing the same name.

For WM 1.1:

| | |
| --- | --- |
| Uploaded filename | `WM-1.1.pdf` |
| Bytes | 490 909 |
| SHA-256 | `7d62e3268e930d5ad16aa97bd05eb037e15a08274487194041cafd78167fb902` |

Get it from the GitHub release, from Zenodo, or from `releases/1.1/` in this repository; all three
are the same bytes, and `make reproduce-release` rebuilds them from source.

## Filenames change; identity does not

SSRN serves the paper under its own filename. The name you upload and the name a reader downloads
are different strings, and neither is the identity of the artifact.

| | WM 1.1 |
| --- | --- |
| Uploaded as | `WM-1.1.pdf` |
| Served as | `ssrn-6994720.pdf`, via `Delivery.cfm/6994720.pdf` |

The identity is the digest. Check that, never the name.

## What SSRN served back

Measured after the revision went live, by downloading the PDF from the public page:

| | |
| --- | --- |
| Bytes | 490 909 |
| SHA-256 | `7d62e3268e930d5ad16aa97bd05eb037e15a08274487194041cafd78167fb902` |
| Byte-identical to the released artifact | **yes** — compared byte-wise, not by digest alone |

So for this revision SSRN passed the file through untouched: no cover page prepended, no
re-rendering, the PDF's internal metadata still the original pdfTeX output. That is worth stating
because it is not guaranteed — repositories often stamp what they serve. **Measure it again after
every revision** rather than assuming this holds.

## Observed: the structured DOI field would not take the Zenodo DOI

The revision form offers a DOI field, asking whether the preprint has a published version with a
DOI. Entering `10.5281/zenodo.21970802` returned *"That DOI was not found at Crossref"* and the entry
could not be added.

The apparent reason is that the field resolves through Crossref, while Zenodo DOIs are registered
with DataCite. **This is what happened on this revision, on this form** — not a documented SSRN
policy, and it may not hold later or for other DOI types.

What was done instead: the DOI was left in the abstract text, in a line that states the archival
deposit and the artifact digest:

> Version 1.1 (bridge revision of the 1.0 line). Archival deposit (version-fixed):
> https://doi.org/10.5281/zenodo.21970802 — identical file, sha256 `7d62e326…167fb902`.

What was **not** done: the form's "enter the details myself" path was left alone. It creates a
publication record, and an archival deposit is not a journal publication. A field that refuses
correct data is a limitation to work around visibly, not a reason to enter something untrue.

## Keep the article's identity

Title, authors, author order and the declaration of interest carry across revisions unchanged unless
the revision itself requires otherwise. The author display name is an account-level field on SSRN,
shared by every paper on the account, so changing it for one version would rewrite the record of
earlier ones. Continuity of authorship is asserted by ORCID, which does not need the display string
to change.

## Record after every revision

A revision is not finished when the form is submitted. Record these, from the live record and from
the file it serves:

- **Last Updated** — as SSRN reports it on the record
- **Date Written** — the value set on the form
- **Version** — which WM version the record now carries
- **Public delivery filename**
- **Public SHA-256** — of the PDF downloaded from the public page
- **Status** — SSRN's own status for the record

## WM 1.1 — the recorded values

| | |
| --- | --- |
| Record | `6994720` |
| Revision applied | 2026-08-17 |
| Status | `DISTRIBUTED` — applied directly to the live record; no review queue, no revision ID issued |
| Last Updated | 08/17/2026 |
| Date Written | August 16, 2026 |
| Version | 1.1 |
| Pages | 25 (previously 19) |
| Public delivery filename | `ssrn-6994720.pdf` |
| Public SHA-256 | `7d62e3268e930d5ad16aa97bd05eb037e15a08274487194041cafd78167fb902` |
| Byte-identical to release | yes |
| Version DOI | `10.5281/zenodo.21970802`, carried in the abstract |
| Licence | CC BY 4.0, unchanged — matches [`../LICENSES/NOTICE.md`](../LICENSES/NOTICE.md) |

Four public locations now hold the same bytes: the Zenodo deposit, the GitHub release asset,
`releases/1.1/WM-1.1.pdf` here, and SSRN `6994720`.

The Zenodo side of the same release is described in
[`ZENODO-WORKFLOW.md`](ZENODO-WORKFLOW.md); the release identities are in
[`RELEASE-STATE-PUBLIC.json`](RELEASE-STATE-PUBLIC.json).
