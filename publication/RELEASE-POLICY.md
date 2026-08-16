# Release policy — witnessability-model

This policy governs how a Witnessability Model version becomes a released artifact and, only
afterwards, an external publication. It is binding on every workflow, script, and manifest in this
repository.

Status of this document: **active**. Status of the WM 1.1 release: **held**.

## 1. The four identities

```
SOURCE  ≠  BUILD OUTPUT  ≠  RELEASE ARTIFACT  ≠  EXTERNAL PUBLICATION RECORD
```

| Identity | Definition | Location | Immutable |
| --- | --- | --- | --- |
| **Source** | Text a human edits: `.tex`, `.bib`, figure sources, metadata | `paper/witnessability-model/` | no — changes via reviewed PR |
| **Import baseline** | Exact bytes received from an upstream process, recorded on arrival | `model/<version>/` | **yes, absolutely** |
| **Build output** | What the pinned toolchain produces from a given source tree | `build/` (git-ignored) | regenerated at will |
| **Release artifact** | A build output that an authorized release has frozen | `releases/<version>/` | **yes, once released** |
| **External publication record** | Receipts from SSRN / Zenodo / other venues | `publication/` | append-only |

Consequences that are not negotiable:

- A build output is never committed into a source directory.
- A build output is never called a release artifact before an authorized release.
- A release artifact is never regenerated; it is only referenced by digest.
- An import baseline is never edited in place. A correction produces a **new object with a new
  identity**, never a mutation of the old one.
- No document may claim a DOI, an SSRN version, or a release status that is not backed by a
  recorded receipt in `publication/`.

## 2. Pipeline order

The order is fixed. Skipping or reordering a stage invalidates the release.

```
source change (PR, reviewed)
  → CI: build + QA gates green
  → release candidate (workflow_dispatch): artifacts for human review
  → governance gates all PASS with evidence
  → founder release authorization (explicit, recorded)
  → git tag + GitHub release           ← first moment a "release artifact" exists
  → human SSRN revision upload
  → authorized Zenodo new version
  → retrieve + verify external artifacts
  → record publication receipts in publication/
```

Everything left of `git tag` is reversible engineering. Everything right of it is public record.

## 3. What this repository will never do automatically

The following are **human actions**, never automated, never performed by an agent, and never
triggered by a workflow:

- creating a release tag;
- publishing a GitHub release;
- uploading a revision to SSRN;
- depositing or versioning on Zenodo;
- minting or asserting a DOI;
- applying a founder signature;
- clearing a release hold.

`.github/workflows/release.yml` exists in inert form so that its gates can be reviewed before it is
ever enabled. It must not be enabled until §5 is satisfied.

## 4. Evidence states

Manifests and gate registers use exactly these states. Any other value is a defect.

| State | Meaning |
| --- | --- |
| `PASS` | Satisfied, with a recorded artifact or receipt proving it |
| `PENDING` | Known to be required, not yet satisfied |
| `BLOCKED` | Cannot proceed until a named external condition changes |
| `NOT_APPLICABLE` | Structurally does not apply to this version |
| `UNAVAILABLE` | Applies, but the evidence cannot currently be obtained |

**A field whose value is unknown is never populated with a plausible guess.** Fabricating a digest,
a DOI, a date, or a consent record is the single worst failure mode this repository is designed to
prevent.

## 5. Release authorization

A WM version may be released only when all of the following hold simultaneously, each with recorded
evidence:

1. The exact commit under review is identified by SHA, and CI is green on that commit.
2. All governance gates for that version are `PASS` in
   `publication/RELEASE-STATE-PUBLIC.json`.
3. Every co-author has recorded explicit consent to release, referencing the exact artifact digest.
4. Founder release authorization is explicit, recorded, and references the same digest.
5. The release identities — artifact digest, tag, commit and external identifiers — are recorded in
   `publication/RELEASE-STATE-PUBLIC.json`, with no state left `PENDING`.

Absent any one of these, the correct terminal state is **NOT READY**, and the reason is named.

## 6. Historical integrity

- WM 1.0 is published. Its bytes are fixed. Nothing in this repository may alter, re-render, or
  supersede the canonical WM 1.0 artifact in place.
- Superseding is expressed by *adding* a new version and recording the supersession relationship —
  never by deleting or rewriting the older record.
- Provenance records are append-only. Corrections are appended with their own timestamp and
  rationale.

## 7. Secrets

No publication credential is required to build, test, or prepare a release candidate in this
repository. The repository must never contain SSRN credentials, Zenodo tokens, GitHub PATs, or DOI
credentials, in any form, including examples and test fixtures. `scripts/scan-secrets.sh` runs in CI
and must be green before any PR is merged.

## 8. Deviations

Any deviation from this policy is recorded in `publication/` as its own document, with the reason,
the authorizing person, and the date, before the deviating action is taken. Silent deviation is a
governance failure regardless of outcome.
