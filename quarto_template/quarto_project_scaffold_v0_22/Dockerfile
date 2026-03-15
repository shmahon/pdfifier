# syntax=docker/dockerfile:1.7
FROM ghcr.io/quarto-dev/quarto:latest

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get -o Acquire::Retries=10 -o Acquire::http::Timeout=60 update && \
    apt-get -o Acquire::Retries=10 -o Acquire::http::Timeout=60 install -y --fix-missing --no-install-recommends \
    fontconfig \
    lmodern \
    make \
    python3 \
    fonts-sil-gentiumplus \
    fonts-sil-ezra \
    texlive-xetex \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-lang-greek \
    texlive-lang-other \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work
CMD ["bash"]
