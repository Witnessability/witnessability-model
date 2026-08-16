# releases/1.1 — empty by design

There is no WM 1.1 release.

This directory will hold the release artifact and its manifest **only after** an authorized release
has occurred. Its emptiness is a fact about the world, not an oversight.

- WM 1.1 status: UNRELEASED REVIEW BASELINE, release hold ACTIVE
- Release state: `publication/RELEASE-STATE-PUBLIC.json` (all four states `PENDING`)
- Proposed tag, not created: `wm-v1.1.0`

The bytes currently under review live in `model/1.1/` as an immutable import record. Do not copy
them here: a review baseline is not a release artifact, and moving bytes between those two roles
without an authorized release is precisely the confusion this repository is built to prevent.
