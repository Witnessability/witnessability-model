# SSRN publication workflow

Intended process for publishing a Witnessability Model paper revision on SSRN.

**Nothing in this document is executed automatically.** SSRN has no supported submission API for
this workflow. Every SSRN step below is performed by a human, in a browser, after the governance
gates in `RELEASE-POLICY.md` §5 are satisfied.

**No SSRN submission has been performed under the task that created this repository.**

## 1. Position of SSRN in the pipeline

```
authorized GitHub release (tag + release artifact, digest frozen)
  → human downloads the exact release artifact
  → human uploads it as a REVISION of the existing SSRN paper
  → SSRN processing / editorial review
  → published version appears under the same abstract ID
  → human retrieves the published PDF
  → verify retrieved bytes against the release digest
  → record the receipt in publication/receipts/
```

SSRN comes **after** the GitHub release, never before it. The artifact uploaded to SSRN must be
byte-identical to the released artifact; if SSRN re-renders or stamps the file, that difference is
recorded explicitly as an external transformation (see §6).

## 2. Target record

| Field | Value |
| --- | --- |
| SSRN abstract ID | `6994720` |
| Existing paper | *Toward a Witnessability Model for AI and Software Execution Systems* |
| Current SSRN version | Version 1.0 (June 2026), two authors |
| WM 1.1 action | **REVISION of the existing paper** — not a new submission |
| Authoritative artifact for the current SSRN version | `295eb6cb…9389d`, 213 922 bytes |

WM 1.1 is expected to be a revision of the existing SSRN paper. Creating a *new* SSRN paper instead
would fork the citation record and orphan the existing abstract ID; that decision is reserved to the
authors and must be recorded here before it is acted on.

## 3. Required metadata for the revision

Values are taken from `paper/witnessability-model/metadata.yaml`, which is the single source of
truth. Do not retype them from memory.

| Field | Source |
| --- | --- |
| Title | `paper.title` + `paper.subtitle` |
| Abstract | abstract block of the released `main.tex` |
| Keywords | `keywords` |
| Author order | `authors[].order` — Sergeev (1), Ikher (2). Order is normative and must not be altered. |
| Author display name | **`Mikhail A. Sergeev`** — founder-decided canonical form for WM 1.1. Do **not** retype the WM 1.0 form. |
| ORCID per author | `authors[].orcid` |

### Author-name continuity

The existing SSRN record for WM 1.0 carries the display form `Mikhail Anatolievich Sergeev`. WM 1.1
uses `Mikhail A. Sergeev`. This is a **historical publication-name variation**, recorded in
`metadata.yaml` under `name_variation_record`, and it is deliberate:

- the WM 1.0 deposit is **not** edited to normalize the old form;
- identity continuity is established by **ORCID `0009-0001-6443-855X`**, which is the same on both
  records, never by string equality of the display names.

When SSRN's revision form pre-fills the author name from the existing record, update it to the
canonical form and ensure the ORCID field is populated. If SSRN refuses to change a display name on
an existing record, leave it and record the refusal here — do not create a second author entry, and
do not open a new paper to work around it.
| Version statement | `paper_revision.date_statement` |
| Licence | see §4 |
| Date | release date of the corresponding GitHub release |

## 4. Licence

The licence asserted on SSRN must match `LICENSES/NOTICE.md` and must match the licence asserted on
Zenodo for the same artifact. A divergence between venues is a governance defect, not a formatting
detail.

WM 1.0 was deposited on Zenodo under CC BY 4.0. The licence choice for WM 1.1 is **PENDING** and is
an author decision, recorded here before upload.

## 5. Pre-upload checklist

Every item must be confirmed immediately before upload, from a fresh command, not from memory:

- [ ] The GitHub release exists and is the authorized one.
- [ ] The file to be uploaded is the release artifact, downloaded from that release.
- [ ] `shasum -a 256` of the local file equals the digest in the release manifest.
- [ ] Exact PDF SHA-256 recorded in this document's receipt section **before** upload.
- [ ] Author list, order, and ORCIDs match `metadata.yaml`.
- [ ] Version statement on the title page matches the release.
- [ ] Licence matches Zenodo and `LICENSES/NOTICE.md`.
- [ ] Co-author consent for this exact digest is recorded.

## 6. Post-publication verification

After SSRN publishes the revision:

1. Download the published PDF from the public abstract page.
2. Compute its SHA-256.
3. Compare with the release digest.
   - **Identical** → record `external_artifact_identical: true`.
   - **Different** → SSRN transformed the file. Record both digests, the observed difference, and do
     **not** describe the SSRN copy as the release artifact. The release artifact remains the one in
     `releases/<version>/`.
4. Verify on the public page: title, author order, ORCIDs, version statement, date, keywords,
   licence.
5. Write a receipt to `publication/receipts/SSRN-<version>-<date>.json` containing the abstract ID,
   the published URL, the retrieval timestamp, both digests, and the verification result.

`.github/workflows/publication-verify.yml` performs step 2–3 read-only against a URL supplied by a
human. It never uploads.

## 7. Prohibited

- Automated SSRN submission or revision.
- Storing SSRN credentials anywhere in this repository.
- Recording an SSRN version as published without a retrieved artifact and a computed digest.
- Uploading a build output that has not been frozen as a release artifact.
