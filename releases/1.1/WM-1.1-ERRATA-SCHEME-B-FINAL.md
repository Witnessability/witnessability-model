# Errata — Witnessability Model 1.0 → 1.1

*Toward a Witnessability Model for AI and Software Execution Systems*

| | |
| --- | --- |
| Corrected artifact | Witnessability Model 1.0, SHA-256 `295eb6cb…9379389d`, 213 922 bytes |
| Correcting artifact | Witnessability Model 1.1, publication candidate, source SHA-256 `84d7a88c…7cf48e94` |
| Status | Errata of record for the 1.0 → 1.1 line |

Version 1.0 asserts two propositions that cannot both hold. This errata identifies each affected
passage, states the corrected wording, and sets out the consequences for naming.

## The inconsistency being corrected

Version 1.0 §6.1 bounds the honest claim by the strongest boundary **"controlled or independently
verified"** by the witness. Version 1.0 §6.3 states, as a corollary:

> **Verifiability does not raise the captured level.** A verifiable record of an observation remains
> an observation; independent verification proves the record is genuine, not that a higher boundary
> was controlled.

If independent verification can set the ceiling, then verifying an observation raises what may be
claimed about it — which the corollary denies. **The corollary is correct and is preserved. The
ceiling definition is corrected to match it.**

---

## E-1 — §6.1, Central Result: Principle 1 (Boundary Ceiling Principle)

**Published (1.0):**

> Let W be a witness, A an action, and B(W) the strongest execution-relevant boundary **controlled or
> independently verified** by W. Then the strongest execution-evidence claim W can honestly assert
> about A is bounded by the level supported by B(W): ClaimLevel(W, A) ≤ BoundaryLevel(B(W)).

**Corrected (1.1):**

> Let W be a witness, A an action, and B(W) the strongest execution-relevant boundary **controlled
> by W, or grounded by W's record on a boundary controlled by another party**. Then the strongest
> execution-evidence claim W can honestly assert about A is bounded by the level supported by B(W):
> ClaimLevel(W, A) ≤ BoundaryLevel(B(W)). Independent verification qualifies a claim at its captured
> content level and is not an input to this bound.

*Grounding* is defined in 1.1: a record is grounded on a boundary when bound evidence establishes
the identity of that boundary and its connection to the claimed action, assessable under the
applicable evaluation profile. It is how a witness may rely on a boundary another party controls
without verification substituting for control.

## E-2 — §6.2, Rationale: replaced, not reworded

**Published (1.0):** §6.2 offers a rationale that derives the bound from the definition of
witnessability, and repeats the same construction inside the derivation:

> The proof follows from the definition of witnessability as the maximum honest evidence claim
> supported by a boundary. […] A witness that mediates invocation cannot establish the internal
> semantics of an external execution it does not own **or independently verify**.

The derivation is circular: the definition already contains the bound, so deriving the bound from
the definition establishes nothing.

**Corrected (1.1):** the subsection is **replaced**, not reworded. Version 1.1 carries
*Status and Basis of the Axiom* in its place, which states the commitment honestly:

> Version 1.0 presented this bound with a proof sketch that derived it from the definition of
> witnessability — a circular derivation, since the definition already contains the bound. This
> revision states the commitment honestly: the cap assignment is an *axiom* of the model, grounded
> in (not derived from) the operational definitions.

The disjunction quoted above therefore has no counterpart in 1.1: the sentence containing it does
not survive the replacement. It is recorded here because a reader comparing the two versions must be
able to see what became of it, rather than find it silently absent.

## E-3 — §6.3, Corollaries: "Invocation does not imply execution ownership"

**Published (1.0):**

> A mediated tool call does not prove the internal behavior of the invoked tool unless the witness
> owns **or verifies** that execution boundary.

**Corrected (1.1):**

> A mediated tool call does not prove the internal behavior of the invoked tool unless the witness
> owns that execution boundary **or has grounded its record on it**.

## E-4 — §5.6, "WL5: Independent Verification"

**Published (1.0):**

> WL0–WL4 describe content levels of execution evidence. WL5 describes independent verifiability of
> a claim at any lower level.

This sentence already carries the qualification reading, while the accompanying level table presents
WL5 as a further rung of a cumulative ladder. The table is the part that is wrong.

**Corrected (1.1):** content levels are WL0–WL3 and are cumulative. Provenance linkage and
independent verifiability are **qualifiers** over a content level, not further content levels:

> A witnessability state is a pair (ℓ, Q) where ℓ ∈ {WL0, WL1, WL2, WL3} is the content level and
> Q ⊆ {PROV, IV} is a set of qualifiers. IV may attach at any content level; PROV presupposes an
> executed action and attaches at WL3. **Qualifiers never raise the content level.**

---

## Preserved unchanged

The following passages of 1.0 are correct and are carried into 1.1 without alteration.

**§6.3 corollary, verbatim:**

> **Verifiability does not raise the captured level.** A verifiable record of an observation remains
> an observation; independent verification proves the record is genuine, not that a higher boundary
> was controlled.

**§6.4, Common False Inferences:** the entry *Verification ≠ Higher Evidence Level*.

## Naming consequence

The scalar labels of 1.0 are retained as **display labels** for specific states:

- `"WL4"` displays (WL3, {PROV})
- `"WL5"` displays (WL3, {IV})

**Prose "WL5" denotes (WL3, {IV}) and nothing else.** It is not a family label for states carrying
IV: (WL2, {IV}) is not "a kind of WL5"; it is a typed state that the legacy vocabulary cannot name.

### Structural qualification is not legacy/display naming

These are two different things and are not interchangeable:

| Structural qualification | Legacy / display naming |
| --- | --- |
| A property of the claim: which qualifiers hold | A convention for printing a state |
| Total — IV may attach at any content level | Partial — names exist for only some states |
| Authoritative for comparison and composition | **Never** authoritative; never a sort key |
| Written (ℓ, Q) | Written WL4, WL5, or WLn[PROV], WLn[IV], WL3[PROV,IV] |

A display label is a projection of the typed state. The projection never exceeds the state it
projects, and it is never the authority for it.

### The name gap

Because IV may qualify any content level while the legacy vocabulary names only some states, the
model describes more states than 1.0 can name. This gap is accepted, not closed:

- **(WL3, {PROV, IV}) — the strongest state the model defines — has no bare scalar label.**
- (WL0, {IV}), (WL1, {IV}), (WL2, {IV}) have no legacy label. Records produced under 1.0 could not
  have asserted them; they arise only in new records.

**A valid typed state does not require a bare legacy label.** A state is valid because it is a
well-formed (ℓ, Q) pair. Any procedure that rejects a state for lacking a scalar name is using the
display projection as a validity test, which it is not.

## Consequences stated explicitly

**Independent verification does not raise captured or base strength.** IV attaches to a claim at the
content level that claim already captured. It changes who can check the record, not what the record
establishes about the action.

**The Boundary Ceiling is qualifier-blind.** The ceiling is computed from content levels alone,
over boundaries the witness controls or has grounded its record on. Neither PROV nor IV is an input
to that computation.

**No scalar WL verdict arithmetic.** States are compared componentwise:

> (ℓ, Q) ≤ (ℓ′, Q′) if and only if ℓ ≤ ℓ′ **and** Q ⊆ Q′

This is a **partial** order. (WL3, {PROV}) and (WL3, {IV}) — "WL4" and "WL5" — are **incomparable**;
neither dominates the other. Any totally ordered presentation of the six labels, including ladder
figures, is a display projection: usable for presentation and for backward-compatible encodings,
**never for comparing, bounding, composing, or accepting claims**.

## Migration of Version 1.0 records

Two mappings, which must not be conflated:

| | Direction | Property |
| --- | --- | --- |
| Display projection | state → label | total, lossy by design, **not invertible** |
| Semantic migration | legacy record → state | exact for honestly produced legacy records |

A record produced under the cumulative reading asserted, at level *n*, all levels below it.
A cumulative-era `WL5` record therefore migrates to **(WL3, {PROV, IV})**: the cumulative reading
included provenance, and dropping it would silently weaken the record's own claim.

## Scope

This errata corrects the passages listed above and nothing else. It does not alter the WL vocabulary,
the taxonomy of boundaries, the classification examples, or any empirical claim of Version 1.0.

The published Version 1.0 artifacts are **not** rewritten. They remain available as published, and
supersession is recorded by addition. Each released artifact is identified by its SHA-256 digest.
