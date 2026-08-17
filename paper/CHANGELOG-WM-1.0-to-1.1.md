# Changelog — Witnessability Model 1.0 → 1.1 (bridge revision)

This document accompanies *Toward a Witnessability Model for AI and Software Execution Systems*,
Version 1.1, and records what changed against Version 1.0.

**Baseline.** Version 1.0 exists as two byte-distinct artifacts. The canonical one is the SSRN
deposit (abstract 6994720), SHA-256 `295eb6cb…9389d`; the secondary is an arXiv-line PDF,
SHA-256 `f3339324…1255e`. Both are superseded by this revision. Neither is rewritten: published
artifacts are frozen, and supersession is recorded by addition.

**Status.** Version 1.1 is a bridge revision inside the 1.0 line. It retains the WL vocabulary and
the Boundary Ceiling. A typed reformulation of the model, replacing the scalar vocabulary entirely,
is reserved for Version 2.0 and will be released only in synchrony with the revision of the
Witnessed Execution Protocol that encodes it.

Changes are grouped by what they affect. **Semantic** changes alter what the model asserts;
everything else does not.

---

## Semantic

### S1 — The cumulative ladder is bounded at WL3

Version 1.0 described WL4 and WL5 both as further rungs of a cumulative ladder *and* as
qualifications applicable to a claim at any lower level whose verification "does not raise the
captured level". Those two readings are inconsistent.

Version 1.1 resolves the inconsistency **in favour of the qualification reading**, which Version
1.0's own corollaries already entailed. Cumulativity is now stated only for WL0–WL3. The affected
table, figure and section introduction are aligned with that reading.

### S2 — Qualified states (new section)

A witnessability state is a pair $(\ell, Q)$ where $\ell \in \{\mathrm{WL0},…,\mathrm{WL3}\}$ is the
content level and $Q \subseteq \{\mathrm{PROV}, \mathrm{IV}\}$ is a set of qualifiers.

- `PROV` — the claimed action is linked to verifiable origin by a bound provenance artifact.
- `IV` — the specific claim is independently verifiable by a non-participant.
- IV may attach at any content level; PROV presupposes an executed action and attaches at WL3.
- **Qualifiers never raise the content level.**

The scalar labels of Version 1.0 are retained as *display labels*: "WL4" displays
$(\mathrm{WL3},\{\mathrm{PROV}\})$ and "WL5" displays $(\mathrm{WL3},\{\mathrm{IV}\})$. Each state
has exactly one canonical display. The top state $(\mathrm{WL3},\{\mathrm{PROV},\mathrm{IV}\})$ has
no bare scalar label.

States are compared componentwise, which makes the ordering a **partial** order: "WL4" and "WL5" are
**incomparable**. Any totally ordered presentation of the six labels, including the ladder figures,
is a profile-defined display projection. It may be used for presentation and for
backward-compatible encodings; it must not be used for verdict arithmetic.

### S3 — Theorem 1 becomes Axiom BC

Version 1.0 presented the Boundary Ceiling as a theorem with a proof sketch that derived it from the
definition of witnessability — a circular derivation, since the definition already contained the
bound.

Version 1.1 states the commitment honestly as an **axiom**. The `cap` assignment from boundary type
to deepest content level is enumerated explicitly, and the ceiling is the maximum `cap` over the
boundaries the witness **controls**. Provenance linkage and independent verification qualify a claim
at its captured content level; they do not raise it.

**Erratum against Version 1.0.** Version 1.0 stated the ceiling over the strongest boundary the
witness "controls *or can independently verify*", while its own corollary held that "verifiability
does not raise the captured level". The two cannot both be right for content levels. This revision
resolves the tension in favour of the corollary: the content ceiling ranges over *controlled*
boundaries only, and independent verification enters as the IV qualifier.

### S4 — Status and basis of the axiom (replaces the proof sketch)

The section formerly titled "Proof Sketch" is replaced by an honest statement of the axiom's status:
it is grounded in, not derived from, the operational definitions; the corollaries are consequences
of the axiom together with the `cap` assignment and are not independent evidence for it; and the
axiom is falsifiable in the ordinary way for classificatory frameworks, by exhibiting a boundary type
whose honest supportable claims systematically exceed its designated cap.

### S5 — Ceiling statements aligned throughout

The abstract, the contribution list and the conclusion are brought into line with Axiom BC. The
Version 1.0 phrasing "or can independently verify" no longer appears on the determining side of the
bound.

### S6 — Two definitions added

- **Grounded.** A record is grounded on a boundary when bound evidence establishes the identity of
  that boundary and its connection to the claimed action, assessable under the applicable evaluation
  profile. Grounding decides whether a record may rely on a boundary attested by another party; an
  ungrounded boundary designation is an attributed self-description.
- **Binding.** Binding evidence connects records to one another, or a record to its action, such
  that the connection is itself assessable. Binding is a precondition of composition.

Witnessability is additionally declared a specialization of the Witnessability Conceptual Core.

### S7 — Acceptance and appraisal semantics (new section)

The relation between a claimed state and an attainable state is one of `equal`, `lower` or
`incomparable`. A claim is accepted only under same-base dominance, or when the requirements of the
claimed level are met — depth does not entail satisfaction, which closes the counterexample of
inferring intent from execution. The section also introduces a bottom outcome, distinguishes an
evidence limit from an evaluation limit, admits counter-evidence as an input, and makes an
unresolved defeater block acceptance.

### S8 — Composition of segmented claims (new section)

Composition is componentwise — minimum over content levels, intersection over qualifiers — subject
to preconditions on binding, provenance coverage and independence of verification roots. A claim
about a chain is distinguished from a claim about the terminal action. A closure lemma is stated
with a proof, together with its algebraic consequences. Six normative test vectors, V1–V6, are
included.

The numeric-minimum rule is attributed to the protocol draft that introduced it, not to Version 1.0.

### S9 — Migration and display of Version 1.0 labels (new section)

Two mappings are distinguished and must not be conflated:

- **display projection** (state → label): total, lossy by design, not invertible;
- **semantic migration** (legacy record → state): exact for honestly produced legacy records.

A cumulative-era WL5 record migrates to $(\mathrm{WL3},\{\mathrm{PROV},\mathrm{IV}\})$, because the
cumulative reading included provenance; dropping it would silently weaken the record's own claim.
States with no legacy label are enumerated explicitly.

### S10 — Relation to the Conceptual Core (new section and appendix)

Version 1.1 states the model as a specialization of the Witnessability Conceptual Core to the
execution class of target propositions, with a correspondence vocabulary and an explicit
out-of-scope list. The appendix records the item-by-item Conceptual Consistency Mapping, CCM-1
through CCM-18, including two justified not-applicable entries.

---

## Editorial

### E1 — Title page

The version is printed on the title page ("Version 1.1 (bridge revision)"). The author list is
aligned with the canonical SSRN deposit. An Author Note records a competing-interest disclosure.

### E2 — Related work

A new subsection covers W3C PROV — including a disambiguation of the `PROV` label as used in this
model — the RATS architecture (RFC 9334), SCITT (RFC 9943), an evidentiary-adequacy criterion, and a
decision-evidence maturity model. A short note on the word *witness* distinguishes this model's use
from in-toto Witness, transparency-log cosigning, zero-knowledge settings and blockchain usage.

---

## References and metadata

### R1 — Version identity and provenance

A new front-matter table records both Version 1.0 artifacts with their SHA-256 digests, marks which
is canonical, and states that both are superseded. From this revision onward the rule is explicit:
**each released artifact is identified by its digest**, and the version number is printed on the
title page of every artifact.

### R2 — Bibliography

Six entries were added, covering the Conceptual Core, W3C PROV, RFC 9334, RFC 9943, the
evidentiary-adequacy criterion and the decision-evidence maturity model.

---

## Build

### B1 — Known build characteristics at 1.1 draft

The 1.1 draft built to PDF with line-overflow warnings in wide tables, recorded at the time as
cosmetic and deferred to publication typesetting. They are addressed in the publication candidate
built from this source; see `tooling/REPRODUCIBILITY.md` for the current toolchain and its
determinism properties.

---

## Deliberately out of scope for 1.1

- The typed model as the primary formulation — reserved for Version 2.0.
- Formalization of topology — not claimed in 1.1; the term is not used in the 1.x line.
- Rewriting the published Version 1.0 artifacts — they are frozen and superseded, not edited.

---

## About this document

This is a **public artifact derived** from the revision's internal working changelog. It is not a
byte-identical translation and makes no claim to be one: it restates the same changes for an
external reader, omits internal process references that carry no public meaning, and adds no
semantic claim that the revision does not make.

The original working changelog is retained privately, unmodified, as the provenance input for this
document.
