# Versioning — witnessability-model

Three identities. They are related but never equal, and never collapsed into one number.

## 1. Model version

The version of the **Witnessability Model** as a conceptual object: its levels, its axioms, its
composition and acceptance semantics.

- Format: `MAJOR.MINOR`
- Current: **Witnessability Model 1.1**
- A model version changes only when the model changes. Rebuilding the paper, fixing typography, or
  correcting a reference does **not** produce a new model version.
- Per the WM 1.1 source, version 1.1 stays inside the 1.0 line: the WL vocabulary and the Boundary
  Ceiling are retained. A typed reformulation is reserved for 2.0 and is to be released only in
  synchrony with the corresponding revision of the Witnessed Execution Protocol.

## 2. Paper revision

The revision of the paper *Toward a Witnessability Model for AI and Software Execution Systems — A
Boundary-Based Framework for Classifying Execution Evidence* that expresses a given model version.

- Format: `<model-version>` plus, if a paper is re-issued without a model change, a revision
  suffix: `1.1`, `1.1-r2`, …
- Current: paper revision corresponding to **WM 1.1**
- Editorial or build-only corrections increment the paper revision, never the model version.

## 3. Release artifact

The exact bytes released. Identified by SHA-256, not by a name.

- WM 1.0 canonical artifact:
  `295eb6cbe3c9f65f3678253dd803b200b3d36632470fdb592f83279b9379389d` (213 922 bytes)
- WM 1.1 review baseline (**unreleased**):
  `69a51fb1ce70e67ec4f73d8fad74a2b0dfbefe003bcda30c2eea619209190615` (185 211 bytes)

Two artifacts with different bytes are different release artifacts even if the model version and
paper revision are identical. WM 1.0 already demonstrates this: it exists as two byte-distinct
artifacts (the SSRN canonical deposit and a secondary arXiv-line PDF), which is precisely why
digests, not names, are authoritative here.

## 4. Tag naming convention

**Chosen convention: `wm-v<MAJOR>.<MINOR>.<PATCH>`**

Example for the current line: `wm-v1.1.0`.

Rationale for choosing this over `wm-paper-v1.1.0`:

- The repository releases one thing — the Witnessability Model together with its paper. A
  `wm-paper-` prefix would imply a second, separately tagged `wm-model-` line that does not exist
  and would immediately create ambiguity about which tag is authoritative.
- The `wm-` prefix keeps the namespace clear if this repository ever also tags tooling
  (`tooling-v*`) or schemas (`schema-v*`).
- The third component carries release-artifact revisions that do not change the model: a rebuild
  that corrects a build defect after `wm-v1.1.0` would be `wm-v1.1.1`, leaving the model version
  visibly untouched.

Mapping:

| Tag component | Bound to |
| --- | --- |
| `MAJOR.MINOR` | model version |
| `PATCH` | paper revision / release artifact revision at the same model version |

**No tag exists yet.** `wm-v1.1.0` is a *proposal* recorded here. Creating it is a human action
gated by `publication/RELEASE-POLICY.md` §5.

## 5. Supersession

Supersession is recorded, never enacted by deletion:

- `releases/<version>/RELEASE-MANIFEST.json` carries a `supersedes` field naming the prior release
  artifact by digest.
- The superseded release record stays in place, unchanged, with its original receipts.
