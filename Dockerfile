FROM debian:stable-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        make \
        pandoc \
        texlive-xetex \
        texlive-fonts-extra \
        texlive-latex-recommended \
        texlive-latex-extra \
        texlive-lang-greek \
        texlive-lang-other \
        fonts-sil-gentiumplus \
        fonts-sil-sbl-hebrew \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# Default command builds the PDF specified in the Makefile (INPUT defaults to manuscript/sovereignty_teleology_master_FINAL.md)
CMD ["make", "pdf"]
