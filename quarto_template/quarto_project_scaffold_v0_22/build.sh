#!/usr/bin/env bash
set -euo pipefail
python3 scripts/assemble.py
python3 scripts/validate.py
quarto render manuscript/master.qmd --to pdf
if [ -f output/manuscript/sovereignty_teleology.pdf ]; then
  mv output/manuscript/sovereignty_teleology.pdf output/sovereignty_teleology.pdf
fi
