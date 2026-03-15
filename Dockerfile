# syntax=docker/dockerfile:1.7
FROM debian:stable-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8

# Pin to a Debian snapshot to avoid mirror checksum races
RUN echo "deb http://snapshot.debian.org/archive/debian/20250301T000000Z stable main contrib non-free non-free-firmware" > /etc/apt/sources.list \
 && echo "deb http://snapshot.debian.org/archive/debian-security/20250301T000000Z stable-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list \
 && echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99snapshot

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        fontconfig \
        make \
        pandoc \
        texlive-xetex \
        texlive-latex-recommended \
        texlive-fonts-recommended \
        texlive-latex-extra \
        texlive-lang-arabic \
        texlive-lang-greek \
        texlive-lang-other \
        fonts-sil-gentiumplus \
        fonts-sil-ezra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# Default command builds the PDF specified in the Makefile (INPUT defaults to manuscript/sovereignty_teleology_master_FINAL.md)
CMD ["make", "pdf"]
