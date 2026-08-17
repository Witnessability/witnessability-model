# SPDX-License-Identifier: Apache-2.0
# Canonical entry points. Everything CI runs, a human can run identically with one word.

SHELL := /bin/bash
JOBNAME := $(shell python3 -c "import json;print(json.load(open('tooling/toolchain.lock.json'))['jobname'])" 2>/dev/null || echo WM-1.1)

.PHONY: all paper qa qa-baseline refs verify secrets clean toolchain help reproduce-release

help:
	@echo "make paper        build the paper into build/ using the pinned toolchain"
	@echo "make qa           run PDF + text-extraction gates against the built PDF"
	@echo "make qa-baseline  run the same gates against the imported WM 1.1 baseline"
	@echo "make refs         run bibliography gates (no build required)"
	@echo "make reproduce-release  rebuild the released artifact and prove it is the published bytes"
	@echo "make verify       verify published baselines still match their recorded digests"
	@echo "make secrets      scan the working tree for credentials"
	@echo "make toolchain    build the pinned image and regenerate tooling/toolchain.lock.json"
	@echo "make review-package  assemble the human/co-author review bundle into build/review-package"
	@echo "make all          verify + refs + paper + qa"

all: verify semantic refs paper qa

toolchain:
	./tooling/lock-toolchain.sh

paper:
	./tooling/build-paper.sh

qa:
	@test -f build/$(JOBNAME).pdf || { echo "no build/$(JOBNAME).pdf — run 'make paper' first" >&2; exit 2; }
	./tooling/qa-run.sh --pdf build/$(JOBNAME).pdf --log build/$(JOBNAME).latex.log \
	        --json-out build/QA-REPORT.json

qa-baseline:
	@mkdir -p build
	./tooling/qa-run.sh --pdf releases/1.1/WM-1.1.pdf --baseline \
	        --json-out build/QA-BASELINE.json

refs:
	python3 tooling/qa-references.py

semantic:
	@mkdir -p build
	python3 tooling/qa-semantic.py --json-out build/QA-SEMANTIC.json

verify:
	./tooling/verify-baselines.sh

secrets:
	./tooling/scan-secrets.sh

review-package:
	@test -f build/$(JOBNAME).pdf || { echo "no build/$(JOBNAME).pdf — run 'make paper' first" >&2; exit 2; }
	./tooling/make-review-package.sh

clean:
	rm -rf build

reproduce-release:
	./tooling/reproduce-release.sh
