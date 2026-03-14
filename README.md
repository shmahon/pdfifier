# PDF Build Pipeline

This repo turns a Markdown manuscript into a publication-quality PDF using Pandoc + XeLaTeX inside Docker. The default input is `manuscript/sovereignty_teleology_master_FINAL.md`.

## Quick start

```bash
docker build -t theology-pdf .
docker run --rm -v $(pwd):/work -w /work theology-pdf make pdf
```

Or, with Docker Compose (builds the image and runs the render in one command):

```bash
docker compose run --rm pdf
```

The PDF is written to `output/sovereignty_teleology_master_FINAL.pdf`.

## Options

- Use another manuscript: `make docker-pdf INPUT=manuscript/other.md`
- Run locally (without Docker, requires pandoc + TeX): `make pdf`
- Clean outputs: `make clean`
- With Docker Compose, override inputs on the fly: `INPUT=manuscript/other.md OUTPUT=output/other.pdf docker compose run --rm pdf`

## Pipeline pieces

- `Dockerfile` installs Pandoc, XeLaTeX, and fonts (Gentium Plus, SBL Hebrew, Libertinus).
- `Makefile` wraps the Pandoc call and Docker convenience targets.
- `pandoc/defaults.yaml` sets engine, template, and fonts; `pandoc/metadata.yaml` holds title data.
- `templates/academic_template.tex` defines the journal-style layout and tcolorbox styles.
- `filters/pandoc_filters.lua` maps fenced code blocks with classes `text`, `logic`, `contrast`, or `diagram` into styled boxes.
- Manuscript lives in `manuscript/`; PDFs land in `output/`.

## Styling logic blocks

Fenced code blocks tagged in Markdown are rendered as follows:

- ```text ... ``` or ```{.logic} ... ``` → `logicblock`
- ```{.contrast} ... ``` → `contrastblock`
- ```{.diagram} ... ``` → `diagramblock`

These boxes preserve alignment and use monospaced text with subtle color cues.

## Fonts

The Docker image installs Gentium Plus (Greek), SBL Hebrew (Hebrew), and Libertinus families. If you need different fonts, adjust `pandoc/defaults.yaml` and the `apt-get` list in `Dockerfile`.

## Notes

- The template sets running headers with the short title and author name from metadata.
- If you add images or other assets, place them beside the manuscript or update `resource-path` in `pandoc/defaults.yaml`.
