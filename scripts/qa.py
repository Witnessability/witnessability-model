#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""PDF and build quality gates for the Witnessability Model paper.

Run against a built PDF plus the LaTeX log it came from:

    python3 scripts/qa.py --pdf build/WM-1.1.pdf --log build/WM-1.1.latex.log

Or against the imported baseline, which has no log:

    python3 scripts/qa.py --pdf model/1.1/WM-1.1.pdf --baseline

Severities
    ERROR   fails the gate (exit 1)
    WARN    reported, does not fail
    INFO    recorded for the record

A finding listed in publication/known-findings.json is downgraded ERROR->WARN and annotated with the
document that analyses it. That is a deliberate, visible exception — never a silent suppression.
Removing a defect removes its entry; the gate then enforces it as ERROR.

External tools: pdffonts, pdfinfo, pdftotext (poppler). Their absence is an ERROR, not a skip:
a QA gate that quietly does not run is worse than no gate.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import metayaml  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent

# Overfull boxes wider than this many points are reported. Below it, TeX routinely produces
# sub-point overfulls that carry no visual meaning.
OVERFULL_PT_THRESHOLD = 5.0

# An overfull box this wide is not a typographic nicety — it is content running off the page,
# visible to any reader. Treated as an error rather than a warning.
SEVERE_OVERFULL_PT = 20.0

FORBIDDEN_TEXT = ("TODO", "TBD", "FIXME", "PLACEHOLDER", "XXX", "LOREM IPSUM")

# Unicode presentation-form ligatures. Their presence in extracted text means the PDF's ToUnicode
# maps a ligature glyph to its presentation form instead of decomposing it, which breaks text
# search, copy-paste, and every downstream text pipeline.
LIGATURES = {0xFB00: "ff", 0xFB01: "fi", 0xFB02: "fl", 0xFB03: "ffi", 0xFB04: "ffl"}


class Findings:
    def __init__(self, known: dict):
        self.items: list[dict] = []
        self.known = known

    def add(self, fid: str, severity: str, category: str, message: str, detail=None):
        entry = {"id": fid, "severity": severity, "category": category, "message": message}
        if detail is not None:
            entry["detail"] = detail
        if severity == "ERROR" and fid in self.known:
            entry["severity"] = "WARN"
            entry["downgraded_from"] = "ERROR"
            entry["known_finding"] = self.known[fid]
        self.items.append(entry)

    @property
    def errors(self):
        return [i for i in self.items if i["severity"] == "ERROR"]


def run(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        raise SystemExit(f"FATAL: required tool not found: {cmd[0]}")
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"FATAL: {' '.join(cmd)} failed: {e.stderr[:400]}")


# ---------------------------------------------------------------------------------------------
# PDF structure
# ---------------------------------------------------------------------------------------------

def check_pdf(pdf: pathlib.Path, meta: dict, f: Findings) -> dict:
    info_raw = run(["pdfinfo", str(pdf)])
    info = {}
    for line in info_raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            info[k.strip()] = v.strip()

    exp = meta.get("expected_build", {})

    pages = int(info.get("Pages", "0"))
    lo, hi = exp.get("pages_min", 1), exp.get("pages_max", 999)
    if not lo <= pages <= hi:
        f.add("S-01", "ERROR", "BUILD", f"page count {pages} outside expected range {lo}..{hi}")

    # Compare numerically, not as a string: engines round the A4 width differently in this field
    # (xelatex prints 595.28, pdflatex 595.276) and a string match turns that into a false failure.
    if exp.get("page_size") == "A4":
        m = re.search(r"([\d.]+)\s*x\s*([\d.]+)", info.get("Page size", ""))
        ok = m and abs(float(m.group(1)) - 595.276) < 0.5 and abs(float(m.group(2)) - 841.89) < 0.5
        if not ok:
            f.add("S-02", "ERROR", "LAYOUT", f"page size is not A4: {info.get('Page size')}")

    if info.get("Encrypted", "no") != "no":
        f.add("S-03", "ERROR", "BUILD", "PDF is encrypted")

    # Document metadata must match metadata.yaml, which is the single source of truth.
    expected_meta = meta.get("expected_pdf_metadata", {})
    for field, want in expected_meta.items():
        got = info.get(field.capitalize(), "")
        if not got:
            f.add(f"M-{field}", "ERROR", "BUILD",
                  f"PDF document metadata field '{field}' is absent",
                  {"expected": want})
        elif got.strip() != want.strip():
            f.add(f"M-{field}", "ERROR", "CONTENT",
                  f"PDF metadata '{field}' does not match metadata.yaml",
                  {"expected": want, "actual": got})

    # Fonts: everything embedded, nothing referenced from the system.
    fonts_raw = run(["pdffonts", str(pdf)])
    font_rows = [ln for ln in fonts_raw.splitlines()[2:] if ln.strip()]
    not_embedded = []
    no_tounicode = []
    type3 = []
    for row in font_rows:
        # pdffonts columns, read from the right because 'type' and 'encoding' contain spaces:
        #   <name> <type…> <encoding> emb sub uni <object-number> <generation-number>
        cols = row.split()
        if len(cols) < 7:
            continue
        name, emb, uni = cols[0], cols[-5], cols[-3]
        ftype = " ".join(cols[1:-5])
        entry = {"name": name, "type": ftype, "object": cols[-2]}
        if emb != "yes":
            not_embedded.append(entry)
        if uni != "yes":
            no_tounicode.append(entry)
        if ftype.startswith("Type 3"):
            type3.append(entry)
    if not_embedded:
        f.add("F-01", "ERROR", "BUILD", "fonts not embedded", not_embedded)
    if no_tounicode:
        # A Type 3 font is a glyph program, not text: it legitimately has no ToUnicode. Reported at
        # WARN so it stays visible, because whatever it draws is unextractable either way.
        only_type3 = all(e in type3 for e in no_tounicode)
        f.add("F-02", "WARN" if only_type3 else "ERROR", "ENCODING",
              "fonts without a ToUnicode map — their glyphs cannot be extracted as text",
              no_tounicode)
    if type3:
        f.add("F-04", "WARN", "BUILD",
              "Type 3 (bitmap/procedure) fonts present; these do not scale cleanly and are not "
              "searchable", type3)
    f.add("F-03", "INFO", "BUILD", f"{len(font_rows)} font subsets embedded")

    return info


# ---------------------------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------------------------

def check_text(pdf: pathlib.Path, meta: dict, f: Findings) -> str:
    text = run(["pdftotext", str(pdf), "-"])

    suspicious: dict[str, int] = {}
    for ch in text:
        cp = ord(ch)
        if (cp in (0xFFFD, 0xFFFE, 0xFFFF)
                or 0xE000 <= cp <= 0xF8FF
                or (cp < 32 and ch not in "\n\r\t\f")):
            key = f"U+{cp:04X} {unicodedata.name(ch, '<unnamed>')}"
            suspicious[key] = suspicious.get(key, 0) + 1
    if suspicious:
        f.add("E-02", "ERROR", "ENCODING",
              "replacement / private-use / control characters in extracted text", suspicious)

    lig_found = {}
    for cp, ascii_form in LIGATURES.items():
        n = text.count(chr(cp))
        if n:
            lig_found[f"U+{cp:04X} ({ascii_form})"] = n
    if lig_found:
        samples = re.findall(r"\S*[ﬀ-ﬄ]\S*", text)[:6]
        f.add("E-01", "ERROR", "ENCODING",
              "ligature presentation forms leak into extracted text; words containing them are "
              "not findable by search and paste as non-ASCII",
              {"counts": lig_found, "samples": samples})

    if chr(0x00AD) in text:
        f.add("E-03", "ERROR", "ENCODING",
              f"soft hyphens (U+00AD) in extracted text: {text.count(chr(0x00AD))}")

    # Hyphenation broken across a line break must extract as "word-\nrest", never as a lost or
    # substituted character. Zero line-end hyphens in a long justified document is itself a signal.
    line_end_hyphens = len(re.findall(r"[A-Za-z]-\n[a-z]", text))
    f.add("H-01", "INFO", "TYPOGRAPHY", f"line-end hyphenations in extracted text: {line_end_hyphens}")
    broken = re.findall(r"[A-Za-z]{2,}[�￾]\s*\n?[a-z]{2,}", text)
    if broken:
        f.add("H-02", "ERROR", "ENCODING",
              "discretionary hyphen extracted as a replacement character", broken[:10])

    upper = text.upper()
    hits = {w: upper.count(w) for w in FORBIDDEN_TEXT if w in upper}
    if hits:
        f.add("C-01", "ERROR", "CONTENT", "unresolved placeholder markers in the document", hits)

    # Identity assertions: the built document must say what metadata.yaml says it is.
    version = meta.get("model", {}).get("version")
    if version and f"Version {version}" not in text:
        f.add("C-02", "ERROR", "CONTENT", f"title-page version statement 'Version {version}' not found")
    for author in meta.get("authors", []):
        surname = author["name"].split()[-1].strip(",")
        if surname not in text:
            f.add("C-03", "ERROR", "CONTENT", f"author '{author['name']}' not present in document text")

    return text


# ---------------------------------------------------------------------------------------------
# LaTeX log
# ---------------------------------------------------------------------------------------------

def check_log(log_path: pathlib.Path, f: Findings) -> None:
    log = log_path.read_text(errors="replace")

    undefined_refs = re.findall(r"Reference `([^']+)' on page \d+ undefined", log)
    if undefined_refs:
        f.add("L-01", "ERROR", "BUILD", "undefined references", sorted(set(undefined_refs)))

    undefined_cites = re.findall(r"Citation `([^']+)' on page \d+ undefined", log)
    if undefined_cites:
        f.add("L-02", "ERROR", "BUILD", "undefined citations", sorted(set(undefined_cites)))

    dup_labels = re.findall(r"Label `([^']+)' multiply defined", log)
    if dup_labels:
        f.add("L-03", "ERROR", "BUILD", "duplicate labels", sorted(set(dup_labels)))

    # Attribute each overfull box to the page it lands on, by counting the "[N" shipout markers
    # that precede it in the log. §10 asks for defects located page by page, and "somewhere in the
    # document" is not a location.
    def page_at(offset: int) -> int:
        marks = re.findall(r"\[(\d+)[\]{ ]", log[:offset])
        return int(marks[-1]) + 1 if marks else 1

    overfull = []
    severe = []
    for m in re.finditer(r"Overfull \\([hv])box \(([\d.]+)pt too wide\)[^\n]*", log):
        pt = float(m.group(2))
        if pt < OVERFULL_PT_THRESHOLD:
            continue
        item = {"pt": pt, "page": page_at(m.start()), "where": m.group(0)[:120]}
        overfull.append(item)
        if pt >= SEVERE_OVERFULL_PT:
            severe.append(item)
    if overfull:
        f.add("L-04", "WARN", "LAYOUT",
              f"{len(overfull)} overfull boxes over {OVERFULL_PT_THRESHOLD}pt",
              sorted(overfull, key=lambda x: -x["pt"])[:15])
    if severe:
        f.add("L-09", "ERROR", "LAYOUT",
              f"content overflows the page by more than {SEVERE_OVERFULL_PT}pt — visible in the "
              f"rendered PDF, not a sub-point rounding artifact", severe)

    if re.search(r"Font shape .* undefined", log):
        f.add("L-05", "ERROR", "BUILD", "undefined font shape requested")
    if "Rerun to get" in log:
        f.add("L-06", "ERROR", "BUILD", "document requested another LaTeX pass; build did not converge")
    if re.search(r"^! ", log, re.M):
        f.add("L-07", "ERROR", "BUILD", "LaTeX error present in log",
              re.findall(r"^! .*", log, re.M)[:10])

    warnings = re.findall(r"(?:LaTeX|Package \w+) Warning: ([^\n]+)", log)
    f.add("L-08", "INFO", "BUILD", f"{len(warnings)} LaTeX/package warnings",
          sorted(set(w.strip() for w in warnings))[:25])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--log", help="LaTeX .log from the same build")
    ap.add_argument("--metadata", default=str(REPO / "paper/witnessability-model/metadata.yaml"))
    ap.add_argument("--known-findings", default=str(REPO / "publication/known-findings.json"))
    ap.add_argument("--baseline", action="store_true",
                    help="PDF is an imported baseline with no log and no metadata guarantee")
    ap.add_argument("--json-out")
    args = ap.parse_args()

    meta = metayaml.load(pathlib.Path(args.metadata))
    known_path = pathlib.Path(args.known_findings)
    known = json.loads(known_path.read_text()) if known_path.exists() else {}

    f = Findings(known)
    pdf = pathlib.Path(args.pdf)
    info = check_pdf(pdf, meta, f)
    check_text(pdf, meta, f)

    if args.log:
        check_log(pathlib.Path(args.log), f)
    elif not args.baseline:
        f.add("L-00", "ERROR", "BUILD", "no LaTeX log supplied; log-based gates did not run")

    report = {
        "target": str(pdf),
        "mode": "baseline" if args.baseline else "build",
        "pdf_info": info,
        "findings": f.items,
        "summary": {
            "ERROR": sum(1 for i in f.items if i["severity"] == "ERROR"),
            "WARN": sum(1 for i in f.items if i["severity"] == "WARN"),
            "INFO": sum(1 for i in f.items if i["severity"] == "INFO"),
        },
    }

    if args.json_out:
        pathlib.Path(args.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    for i in f.items:
        mark = {"ERROR": "FAIL", "WARN": "warn", "INFO": "info"}[i["severity"]]
        print(f"[{mark}] {i['id']} {i['category']:<10} {i['message']}")
        if "detail" in i:
            print(f"        {json.dumps(i['detail'], ensure_ascii=False)[:300]}")
        if "known_finding" in i:
            print(f"        known finding, see {i['known_finding']}")

    print(f"\n{report['summary']['ERROR']} error(s), {report['summary']['WARN']} warning(s)")
    return 1 if f.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
