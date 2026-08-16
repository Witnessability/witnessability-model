#!/usr/bin/env python3
"""Semantic invariant gates for the Witnessability Model paper.

These gates protect one commitment, stated by Axiom BC and by the paper's own erratum:

    The Boundary Ceiling ranges over CONTROLLED (or grounded) boundaries.
    PROV and IV are qualifiers. They qualify a claim at its captured content level.
    They never raise it. The ceiling is qualifier-blind.

Why this is not a grep
----------------------
The struck Version 1.0 proposition — that the ceiling ranges over boundaries the witness
"controls or can independently verify" — must not survive *as an assertion*. But the paper must
still be able to *quote* it in order to record that it was struck; deleting the quotation would
destroy the erratum and hide the correction. A single grep cannot tell an assertion from an
attributed, explicitly superseded quotation, and would force the paper to choose between failing
the gate and losing its own change record.

So the gate parses sentences, finds the semantic pattern (a ceiling-determining disjunction that
admits verification as an alternative to control), and exempts an occurrence only when the same
sentence carries an explicit supersession marker. Every exemption is printed with its sentence, so
a reviewer sees exactly what was allowed through and why.

Usage: python3 scripts/qa-semantic.py [--tex PATH] [--json-out PATH]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_TEX = REPO / "paper/witnessability-model/src/main.tex"

# A sentence is about the ceiling if it talks about the bound itself.
CEILING_CONTEXT = re.compile(
    r"\b(ceiling|ClaimLevel|BoundaryLevel|honest(?:ly)?\s+(?:claim|assert|support)|"
    r"maximum\s+honest|does not reach WL|cannot honestly claim|strongest\s+\S*\s*boundary|"
    r"supportable claim|unless the witness|execution boundary|corresponding boundary)\b",
    re.I,
)

# The struck construction: control disjoined with verification as a route to the same bound.
STRUCK_DISJUNCTION = re.compile(
    r"\b(control(?:s|led)?|own(?:s|ed)?)\b[^.]{0,80}?\bor\b[^.]{0,40}?"
    r"\b(independently\s+verif\w+|verif(?:y|ies|ied)|can\s+independently)\b",
    re.I,
)

# An occurrence is a historical quotation, not an assertion, only if the sentence says so.
SUPERSESSION_MARKER = re.compile(
    r"\b(Version\s+1\.0\s+(stated|described|presented)|erratum|this revision resolves|"
    r"cannot both be right|superseded|struck|resolves the tension)\b",
    re.I,
)

REQUIRED_PROPOSITIONS = {
    "iv-non-amplification": (
        r"[Vv]erifiability does not raise the captured level",
        "the corollary that verification does not raise the captured level",
    ),
    "qualifiers-never-raise": (
        r"[Qq]ualifiers never raise the content level",
        "the explicit statement that qualifiers never raise the content level",
    ),
    "no-verdict-arithmetic": (
        r"must not be used for verdict arithmetic",
        "the prohibition on using a display projection for verdict arithmetic",
    ),
    "name-gap": (
        r"has no bare scalar label",
        "the explicit name gap for the top typed state",
    ),
    "partial-order": (
        r"\bincomparable\b",
        "preserved incomparability of (WL3,{PROV}) and (WL3,{IV})",
    ),
    "ceiling-over-controlled": (
        r"content ceiling ranges over \\emph\{controlled\} boundaries only",
        "the erratum fixing the ceiling to controlled boundaries",
    ),
}


def strip_comments(tex: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", tex)


def sentences(tex: str):
    """Split into sentence-ish units, keeping a line number for each."""
    out, line = [], 1
    for chunk in re.split(r"(?<=\.)\s+|\n\n+", tex):
        if chunk.strip():
            out.append((line, " ".join(chunk.split())))
        line += chunk.count("\n")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", default=str(DEFAULT_TEX))
    ap.add_argument("--json-out")
    args = ap.parse_args()

    raw = pathlib.Path(args.tex).read_text(encoding="utf-8")
    tex = strip_comments(raw)

    violations, exemptions = [], []
    for lineno, s in sentences(tex):
        if not CEILING_CONTEXT.search(s):
            continue
        m = STRUCK_DISJUNCTION.search(s)
        if not m:
            continue
        entry = {"line": lineno, "match": m.group(0), "sentence": s[:400]}
        (exemptions if SUPERSESSION_MARKER.search(s) else violations).append(entry)

    missing = []
    for key, (pattern, description) in REQUIRED_PROPOSITIONS.items():
        if not re.search(pattern, tex):
            missing.append({"id": key, "expected": description, "pattern": pattern})

    results = {
        "NO-STRUCK-REDUCTIO": "PASS" if not violations else "FAIL",
        "BOUNDARY-CEILING-QUALIFIER-BLIND": "PASS" if not violations and not missing else "FAIL",
        "SCALAR-VERDICT-ARITHMETIC-ABSENT":
            "PASS" if not any(m["id"] == "no-verdict-arithmetic" for m in missing) else "FAIL",
        "SCHEME-B-NAME-GAP-PRESERVED":
            "PASS" if not any(m["id"] in ("name-gap", "partial-order") for m in missing) else "FAIL",
        "IV-NON-AMPLIFICATION-PRESERVED":
            "PASS" if not any(m["id"] in ("iv-non-amplification", "qualifiers-never-raise")
                              for m in missing) else "FAIL",
    }

    report = {
        "target": args.tex,
        "results": results,
        "asserted_violations": violations,
        "quoted_exemptions": exemptions,
        "missing_required_propositions": missing,
    }
    if args.json_out:
        pathlib.Path(args.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    for gate, verdict in results.items():
        print(f"[{'PASS' if verdict == 'PASS' else 'FAIL'}] {gate}")

    if violations:
        print(f"\n{len(violations)} asserted ceiling-disjunction(s) — these must not survive:")
        for v in violations:
            print(f"  line ~{v['line']}: …{v['match']}…")
            print(f"    {v['sentence'][:220]}")
    if missing:
        print(f"\n{len(missing)} required proposition(s) missing:")
        for m in missing:
            print(f"  {m['id']}: expected {m['expected']}")

    if exemptions:
        print(f"\n{len(exemptions)} quoted occurrence(s) exempted as explicitly superseded "
              f"(shown so the exemption is reviewable, not hidden):")
        for e in exemptions:
            print(f"  line ~{e['line']}: {e['sentence'][:240]}")

    failed = any(v == "FAIL" for v in results.values())
    print(f"\n{'SEMANTIC GATES: FAIL' if failed else 'SEMANTIC GATES: PASS'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
