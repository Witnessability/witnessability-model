#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Bibliography gates.

Runs against the .bib and the .tex without needing a build, so it can gate a source-only change.

It never edits the bibliography and never consults the network. Correcting a reference is a
factual change to the paper and must be a separate, reviewable commit — not a side effect of a QA
run. This script only reports.
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent

DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
ARXIV_RE = re.compile(r"^(\d{4}\.\d{4,5}(v\d+)?|[a-z-]+(\.[A-Z]{2})?/\d{7}(v\d+)?)$")


def parse_bib(text: str) -> dict[str, dict]:
    entries: dict[str, dict] = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),", text):
        kind, key = m.group(1).lower(), m.group(2).strip()
        start = m.end()
        depth, i = 1, start
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[start:i - 1]
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*[,}]?\s*(?=\w+\s*=|$)", body, re.S):
            fields[fm.group(1).lower()] = " ".join(fm.group(2).split())
        entries[key] = {"type": kind, "fields": fields}
    return entries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bib", default=str(REPO / "paper/witnessability-model/bibliography/references.bib"))
    ap.add_argument("--tex", default=str(REPO / "paper/witnessability-model/src/main.tex"))
    ap.add_argument("--json-out")
    args = ap.parse_args()

    bib_text = pathlib.Path(args.bib).read_text(encoding="utf-8", errors="replace")
    tex_text = pathlib.Path(args.tex).read_text(encoding="utf-8", errors="replace")

    entries = parse_bib(bib_text)
    findings: list[dict] = []

    def add(fid, severity, message, detail=None):
        f = {"id": fid, "severity": severity, "category": "REFERENCES", "message": message}
        if detail is not None:
            f["detail"] = detail
        findings.append(f)

    # Duplicate keys survive parsing into a dict, so count them in the raw text.
    keys = re.findall(r"@\w+\s*\{\s*([^,]+),", bib_text)
    dupes = [k for k, n in collections.Counter(k.strip() for k in keys).items() if n > 1]
    if dupes:
        add("R-01", "ERROR", "duplicate bibliography keys", dupes)

    cited: set[str] = set()
    for m in re.finditer(r"\\(?:cite|parencite|textcite|autocite|footcite)\w*"
                         r"(?:\[[^\]]*\])*\{([^}]+)\}", tex_text):
        cited.update(k.strip() for k in m.group(1).split(","))

    missing = sorted(cited - set(entries))
    if missing:
        add("R-02", "ERROR", "cited keys with no bibliography entry", missing)

    unused = sorted(set(entries) - cited)
    if unused:
        add("R-03", "WARN", "bibliography entries never cited", unused)

    bad_doi, bad_arxiv, no_id, bare_doi_url = [], [], [], []
    for key, e in sorted(entries.items()):
        f = e["fields"]
        doi = f.get("doi", "").strip()
        if doi:
            normalized = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi, flags=re.I)
            if not DOI_RE.match(normalized):
                bad_doi.append({key: doi})
            elif normalized != doi:
                bare_doi_url.append({key: doi})
        eprint = f.get("eprint", "").strip()
        if eprint and f.get("eprinttype", "").lower() in ("arxiv", "") and not ARXIV_RE.match(eprint):
            bad_arxiv.append({key: eprint})
        if not (doi or eprint or f.get("url") or f.get("isbn")):
            no_id.append(key)

    if bad_doi:
        add("R-04", "ERROR", "malformed DOI values", bad_doi)
    if bare_doi_url:
        add("R-05", "WARN", "DOI field contains a URL or 'doi:' prefix; store the bare DOI", bare_doi_url)
    if bad_arxiv:
        add("R-06", "ERROR", "malformed arXiv eprint identifiers", bad_arxiv)
    if no_id:
        add("R-07", "WARN", "entries with no DOI, eprint, URL or ISBN", no_id)

    # urldate is required by most styles whenever a bare URL is the only locator.
    missing_urldate = [k for k, e in sorted(entries.items())
                       if e["fields"].get("url") and not e["fields"].get("urldate")
                       and not e["fields"].get("doi")]
    if missing_urldate:
        add("R-08", "WARN", "URL-only entries without an access date (urldate)", missing_urldate)

    add("R-00", "INFO", f"{len(entries)} bibliography entries, {len(cited)} distinct citations")

    report = {"bib": args.bib, "entries": len(entries), "cited": len(cited), "findings": findings}
    if args.json_out:
        pathlib.Path(args.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    for f in findings:
        mark = {"ERROR": "FAIL", "WARN": "warn", "INFO": "info"}[f["severity"]]
        print(f"[{mark}] {f['id']} {f['message']}")
        if "detail" in f:
            print(f"        {json.dumps(f['detail'], ensure_ascii=False)[:400]}")

    errors = [f for f in findings if f["severity"] == "ERROR"]
    print(f"\n{len(errors)} error(s), {sum(1 for f in findings if f['severity']=='WARN')} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
