# Zenodo publication workflow

The other external channel is SSRN; the procedure actually executed there is in
[`SSRN-REVISION.md`](SSRN-REVISION.md).

The process for depositing a Witnessability Model release on Zenodo. It has been followed once, for
WM 1.1, and the deposit it produced is `10.5281/zenodo.21970802`.

**Nothing here is executed automatically.** Every deposit step is performed by a human, in a browser,
holding credentials this repository does not have and must never hold.

## 1. Concept DOI vs version DOI

These are different objects and are never used interchangeably.

| | Concept DOI | Version DOI |
| --- | --- | --- |
| Identifies | the *record line* across all versions | one *specific deposited artifact* |
| Resolves to | the latest version | that exact version, forever |
| Current value | `10.5281/zenodo.21824435` | `10.5281/zenodo.21970802` (WM 1.1); `10.5281/zenodo.21824436` (WM 1.0) |
| Changes on new version | never | **always** — a new version DOI is minted |
| Cite in the paper for "this work" | concept DOI | — |
| Cite for "the exact artifact reviewed" | — | version DOI |

Verified against the Zenodo public API on import; the retrieval record is
[`../releases/1.0/RELEASE-RECORD.md`](../releases/1.0/RELEASE-RECORD.md).

The WM 1.1 deposit did reuse the line: record `21970802` carries concept DOI
`10.5281/zenodo.21824435`, the one WM 1.0 established. Every later version must do the same — a *new
version* of the existing record, never a new record.

## 2. Position in the pipeline

```
authorized GitHub release (tag + release artifact, digest frozen)
  → human opens the existing Zenodo record 21824435 (concept)
  → "New version"
  → upload the exact release artifact
  → metadata from paper/metadata.yaml
  → publish → new version DOI minted
  → retrieve record via public API
  → verify artifact digest + metadata
  → run publication-verify.yml against the new record
  → record the release identities in publication/RELEASE-STATE-PUBLIC.json
```

Creating a **new record** instead of a **new version** breaks concept-DOI continuity and cannot be
undone. This is the single highest-risk manual step in the pipeline.

## 3. Metadata mapping

| Zenodo field | Source |
| --- | --- |
| Title | `paper.title` + `": "` + `paper.subtitle` (matching the WM 1.0 record's convention) |
| Creators | `authors[]` in order, `Family, Given` form, with ORCIDs — `Sergeev, Mikhail A.` and `Ikher, Vladimir` |
| Publication date | release date |
| Version | `model.version` (e.g. `1.1`) |
| Licence | must equal the licence in `LICENSES/NOTICE.md` and on SSRN |
| Related identifiers | `isNewVersionOf` → previous version DOI; `isIdenticalTo`/`isSupplementTo` → SSRN abstract URL |
| Description | abstract from the released source |

The WM 1.0 record uses `Sergeev, Mikhail A.` and `Ikher, Vladimir`, CC BY 4.0, publication date
2026-06-25. Deviating from that convention without cause fragments the record line.

**Author-name continuity.** The founder-decided canonical display form for WM 1.1 is
`Mikhail A. Sergeev`, which in Zenodo's `Family, Given` convention is `Sergeev, Mikhail A.` — the
form the WM 1.0 record already carries. Zenodo therefore needs **no name change** across versions.
The variation exists only against the WM 1.0 *PDF metadata* string
(`Mikhail Anatolievich Sergeev`), which is not edited. Continuity is asserted by ORCID
`0009-0001-6443-855X` on both records; the ORCID field must be populated on the new version, not
left to be inferred from the name.

## 4. Pre-deposit checklist

Confirmed from fresh commands immediately before deposit:

- [ ] Authorized GitHub release exists; artifact downloaded from it.
- [ ] `shasum -a 256` matches the release manifest digest.
- [ ] MD5 of the file recorded too — Zenodo reports MD5 in its API and that is the field used for
      post-deposit verification.
- [ ] Acting on record `21824435` via **New version**, not **New upload**.
- [ ] Licence identical to SSRN and `LICENSES/NOTICE.md`.
- [ ] Co-author consent recorded for this exact digest.
- [ ] Founder release authorization recorded.

## 5. Post-deposit verification

1. `GET https://zenodo.org/api/records/<new_id>` (public, no credential).
2. Assert: `doi` is the new version DOI; `conceptdoi` equals `10.5281/zenodo.21824435`.
3. Assert: `files[0].size` equals the release artifact size and `files[0].checksum` MD5 equals the
   recorded MD5.
4. Assert: creators, order, ORCIDs, version, licence, publication date.
5. Record the release identities — both DOIs, the artifact digest and the tag — in
   `publication/RELEASE-STATE-PUBLIC.json`, and the artifact digests in
   `releases/<version>/SHA256SUMS.txt`.
6. Re-run `make verify`: it fails if the tracked copy of the released artifact stops matching the
   digest the deposit carries.

`.github/workflows/publication-verify.yml` performs steps 1–4 read-only. It has no Zenodo token and
cannot deposit.

## 6. Prohibited

- Automated deposit, publish, or DOI minting.
- Storing a Zenodo token in this repository or in repository secrets.
- Writing a DOI into any manifest before it has been retrieved from the Zenodo API.
- Creating a new Zenodo record for a version that belongs to the existing concept line.
