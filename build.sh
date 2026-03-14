#!/usr/bin/env bash
set -euo pipefail

INPUT=${1:-manuscript/sovereignty_teleology_master_FINAL.md}
OUTPUT=${2:-output/$(basename "${INPUT%.*}").pdf}

make docker-pdf INPUT="$INPUT" OUTPUT="$OUTPUT"
