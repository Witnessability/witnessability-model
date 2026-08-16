# Repository-owned TeX toolchain for the Witnessability Model paper.
#
# Why a repository-owned image rather than a published TeX Live image:
#   - the package set is explicit and reviewable, instead of "whatever the tag contains today";
#   - the base is pinned by digest, so the same Dockerfile resolves to the same base forever;
#   - it is ~2 GB instead of ~7 GB, which matters for CI cold starts;
#   - it carries the QA tooling (python3, poppler) so the gates run in the same environment as the
#     build, on every platform, with no host dependency.
#
# Base pinned by multi-arch index digest. The index resolves per platform, so the same reference
# builds on linux/amd64 (CI) and linux/arm64 (Apple Silicon).
FROM debian:bookworm-slim@sha256:abd67ffcfa541b485a3dff59865ab629aa048a6c613e639d36e7456b0b229241

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Package set derived from the paper preamble, not guessed:
#   fontenc/T1, lmodern, cmap, geometry, booktabs, array, graphicx, longtable,
#   tabularx, amsmath, amssymb, hyperref        -> latex-base / latex-recommended / fonts-recommended
#   enumitem, xurl                              -> latex-extra
#   tikz + positioning/arrows.meta/backgrounds  -> pictures
#   biblatex with backend=bibtex                -> bibtex-extra (+ bibtex binary from binaries)
#   xelatex (the engine that produced the WM 1.1 baseline)
#                                               -> xetex
# python3 and poppler-utils are the QA gates' only external dependencies.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      texlive-latex-base \
      texlive-latex-recommended \
      texlive-latex-extra \
      texlive-fonts-recommended \
      texlive-pictures \
      texlive-bibtex-extra \
      texlive-xetex \
      latexmk \
      python3 \
      poppler-utils \
      ca-certificates \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# lmodern is a separate Debian package, and texlive-fonts-recommended only *recommends* it — so
# --no-install-recommends above silently omits it and the build dies on a missing lmodern.sty.
# The paper loads \usepackage{lmodern}, so it is installed explicitly rather than by luck.
RUN apt-get update \
 && apt-get install -y --no-install-recommends lmodern \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Record the exact resolved versions inside the image so the lock file is generated from
# observation rather than from the Dockerfile's intent.
RUN { \
      echo "tex_live=$(kpsewhich -var-value TEXMFDIST | xargs -I{} sh -c 'cat {}/../texmf-dist/web2c/../../release-texlive.txt 2>/dev/null | head -1' || true)"; \
      echo "xelatex=$(xelatex --version | head -1)"; \
      echo "latexmk=$(latexmk --version 2>&1 | head -1)"; \
      echo "bibtex=$(bibtex --version | head -1)"; \
      echo "python3=$(python3 --version)"; \
      echo "pdftotext=$(pdftotext -v 2>&1 | head -1)"; \
      echo "debian=$(cat /etc/debian_version)"; \
    } > /toolchain-versions.txt

WORKDIR /work
