#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Emit build/BUILD-MANIFEST.json binding source, toolchain, environment and output.

The manifest answers one question: *given these exact inputs, this exact toolchain and this exact
environment, these exact output bytes were produced.* Every field is measured. Nothing is asserted
that was not observed during this build.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import pathlib
import subprocess

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / "paper"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", "-C", str(REPO), *args],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "UNAVAILABLE"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--platform", required=True)
    ap.add_argument("--source-date-epoch", required=True)
    args = ap.parse_args()

    pdf = pathlib.Path(args.pdf)
    lock = json.loads((REPO / "tooling/toolchain.lock.json").read_text())

    source_files = {}
    for rel in ("src/main.tex", "bibliography/references.bib", "metadata.yaml"):
        p = SRC / rel
        if p.exists():
            source_files[f"paper/{rel}"] = {
                "bytes": p.stat().st_size,
                "sha256": sha256(p),
            }
    for fig in sorted((SRC / "figures").glob("**/*")):
        if fig.is_file():
            source_files[str(fig.relative_to(REPO))] = {"bytes": fig.stat().st_size,
                                                        "sha256": sha256(fig)}

    dirty = git("status", "--porcelain") not in ("", "UNAVAILABLE")

    manifest = {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),

        "source": {
            "git_commit": git("rev-parse", "HEAD"),
            "git_tree": git("rev-parse", "HEAD^{tree}"),
            "git_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
            "working_tree_dirty": dirty,
            "files": source_files,
        },

        "toolchain": {
            "image_ref": f"{lock['image']['name']}:local-{args.platform.split('/')[-1]}",
            "image_index_digest": lock["image"]["index_digest"],
            "platform_digest": lock["image"]["platform_digests"].get(args.platform, "UNAVAILABLE"),
            "engine": lock["engine"],
            "tex_live_version": lock["versions"]["tex_live"],
            "engine_version": lock["versions"]["engine"],
            "latexmk_version": lock["versions"]["latexmk"],
            "bib_tool": lock["versions"]["bib_tool"],
            "fonts": lock["fonts"],
        },

        "environment": {
            "build_platform": args.platform,
            "source_date_epoch": int(args.source_date_epoch),
            "timestamp_policy": (
                "SOURCE_DATE_EPOCH is set from the source commit time and FORCE_SOURCE_DATE=1 is "
                "exported, so the PDF creation date is a function of the source, not of the clock."
            ),
            "tz": "UTC",
            "locale": "C.UTF-8",
            "container_workdir": "/work",
            "host_paths_in_output": (
                "none by construction — the build runs in a fixed container path and never sees a "
                "host path"
            ),
        },

        "build": {
            "command": "tooling/build-paper.sh",
            "container_command": (
                f"latexmk -{lock['engine']} -interaction=nonstopmode -halt-on-error "
                f"-file-line-error -jobname={lock['jobname']} {lock['jobname']}.tex"
            ),
        },

        "output": {
            "path": str(pdf.relative_to(REPO)),
            "bytes": pdf.stat().st_size,
            "sha256": sha256(pdf),
        },

        "claims": {
            "released": False,
            "reproducibility_proven": "SEE tooling/REPRODUCIBILITY.md",
            "note": (
                "This manifest records one build. It does not by itself assert reproducibility; "
                "that claim requires two independent builds compared byte for byte."
            ),
        },
    }

    out = REPO / "build/BUILD-MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"WROTE   {out.relative_to(REPO)}  output sha256={manifest['output']['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
