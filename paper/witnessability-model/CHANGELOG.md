# Paper changelog

Changes are recorded under six headings, kept separate so that a build fix can never be mistaken
for a change to the model. This distinction is the point of the file.

| Heading | Meaning |
| ------- | ------- |
| `SEMANTIC` | The model or its claims changed. Requires a model-version decision. |
| `EDITORIAL` | Wording, structure, or presentation changed; claims did not. |
| `BUILD` | How the artifact is produced changed. Output bytes change; content does not. |
| `REFERENCES` | Bibliography entries added, corrected, or removed. |
| `PROVENANCE` | Identity, digest, or version records changed. |
| `GOVERNANCE` | Gates, authorizations, or policy changed. |

## [Unreleased] — WM 1.1 working line

### PROVENANCE
- Imported WM 1.1 review baseline as an immutable record: `WM-1.1.tex`
  (`bc019077…e95cc`, 76 011 B), `WM-1.1.pdf` (`69a51fb1…90615`, 185 211 B),
  `references.bib` (`7f7443bb…b363f5`, 13 811 B).
- Seeded `src/main.tex` and `bibliography/references.bib` byte-identical from that baseline. They
  are working sources from this point on; the baseline keeps its own identity in `model/1.1/`.
- Imported the canonical WM 1.0 artifact and verified it against the Zenodo deposit by size and
  MD5.

### BUILD
- No change to the source. The paper is byte-identical to the imported baseline.
- Two build-class defects are **identified and not fixed**, because fixing either changes the
  artifact identity and requires a reviewed decision:
  - ligature presentation forms in extracted text;
  - absent PDF document metadata, a regression against WM 1.0.

### REFERENCES
- No reference was added, removed, or altered. Three uncited entries and six URL-only entries
  without access dates are recorded for a separate reviewed change.

### SEMANTIC
- None. No semantic content was changed under the pipeline-preparation task.

### GOVERNANCE
- WM 1.1 recorded as UNRELEASED. Release state: all four public states `PENDING`.

## 1.1 — not released

Bridge revision inside the 1.0 line. Changes against canonical 1.0 are recorded in
`model/1.1/CHANGELOG-WM-1.0-to-1.1.md`, which is an imported historical document and is not
rewritten here.

## 1.0 — released 2026-06-25

Published. See `releases/1.0/RELEASE-RECORD.md`.
