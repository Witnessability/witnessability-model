#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Loader for this repository's metadata.yaml.

Uses PyYAML when it is available. When it is not — the pinned toolchain image and a bare macOS
python3 both lack it — it falls back to a recursive-descent parser for the YAML subset this
repository actually uses: nested mappings, sequences of mappings, sequences of scalars, quoted and
bare scalars, comments, and folded block scalars (`>-`, `>`, `|`).

The fallback deliberately supports no more than that. Anything outside the subset raises, rather
than being silently misparsed — a metadata file that parses into the wrong shape would make every
identity gate downstream meaningless.

Self-test:  python3 tooling/metayaml.py paper/metadata.yaml
"""

from __future__ import annotations

import pathlib
import re
import sys


def load(path: pathlib.Path) -> dict:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except ImportError:
        pass

    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        lines.append((len(raw) - len(raw.lstrip()), raw.strip()))

    value, idx = _block(lines, 0, lines[0][0])
    if idx != len(lines):
        raise ValueError(f"metayaml: unconsumed input at line index {idx}: {lines[idx]}")
    return value


def _block(lines, i: int, indent: int):
    if lines[i][1].startswith("- "):
        return _sequence(lines, i, indent)
    return _mapping(lines, i, indent)


def _mapping(lines, i: int, indent: int):
    out: dict = {}
    while i < len(lines):
        ind, text = lines[i]
        if ind < indent:
            break
        if ind > indent:
            raise ValueError(f"metayaml: unexpected indent at {text!r}")
        if text.startswith("- "):
            break
        if ":" not in text:
            raise ValueError(f"metayaml: expected 'key: value' at {text!r}")

        key, rest = text.split(":", 1)
        key, rest = key.strip(), rest.strip()
        i += 1

        if rest in (">-", ">", "|", "|-"):
            out[key], i = _folded(lines, i, indent, literal=rest.startswith("|"))
        elif rest == "":
            if i < len(lines) and lines[i][0] > indent:
                out[key], i = _block(lines, i, lines[i][0])
            else:
                out[key] = None
        else:
            out[key] = _scalar(rest)
    return out, i


def _sequence(lines, i: int, indent: int):
    out: list = []
    while i < len(lines):
        ind, text = lines[i]
        if ind < indent or not text.startswith("- "):
            break
        item = text[2:].strip()
        i += 1

        if ":" in item and not _looks_scalar(item):
            # Inline first key of a mapping item; its siblings follow at deeper indent.
            key, rest = item.split(":", 1)
            key, rest = key.strip(), rest.strip()
            if rest in (">-", ">", "|", "|-"):
                # Block scalar opened on the item line: its body is the deeper-indented run.
                value, i = _folded(lines, i, indent, literal=rest.startswith("|"))
                entry = {key: value}
            else:
                entry = {key: _scalar(rest)}
                if i < len(lines) and lines[i][0] > indent:
                    more, i = _mapping(lines, i, lines[i][0])
                    entry.update(more)
            out.append(entry)
        else:
            out.append(_scalar(item))
    return out, i


def _folded(lines, i: int, indent: int, literal: bool):
    parts = []
    while i < len(lines) and lines[i][0] > indent:
        parts.append(lines[i][1])
        i += 1
    return ("\n" if literal else " ").join(parts), i


def _looks_scalar(item: str) -> bool:
    """Distinguish a mapping item ('name: X') from a scalar containing a colon ('a: b' in quotes)."""
    return item.startswith('"') or item.startswith("'")


def _scalar(v: str):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v in ("true", "True", "yes"):
        return True
    if v in ("false", "False", "no"):
        return False
    if v in ("null", "~", ""):
        return None
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


if __name__ == "__main__":
    import json
    target = pathlib.Path(sys.argv[1])
    data = load(target)

    # Shape assertions for this repository's metadata.yaml — the loader is only useful if the
    # shape is right, so failing loudly here is the point.
    assert isinstance(data["authors"], list), "authors must parse to a list"
    assert data["authors"][0]["orcid"] == "0009-0001-6443-855X"
    assert data["authors"][1]["name"] == "Vladimir Ikher"
    assert isinstance(data["name_variation_record"], list) and len(data["name_variation_record"]) == 3
    assert isinstance(data["name_variation_record"][2]["note"], str)
    assert data["model"]["version"] == "1.1"
    assert data["expected_build"]["pages_min"] == 20
    assert data["expected_build"]["fonts_all_embedded"] is True
    assert len(data["keywords"]) == 15, f"expected 15 keywords, got {len(data['keywords'])}"
    assert data["expected_pdf_metadata"]["author"] == "Mikhail A. Sergeev and Vladimir Ikher"
    assert isinstance(data["model"]["scope_note"], str) and len(data["model"]["scope_note"]) > 40
    assert data["paper_revision"]["released"] is False
    assert data["version_identity"]["wm_1_0_canonical"]["bytes"] == 213922

    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("\nmetayaml self-test: OK", file=sys.stderr)
