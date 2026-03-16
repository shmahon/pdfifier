# PDF Build Pipeline

This repo turns a Markdown manuscript into a publication-quality PDF using Pandoc + XeLaTeX inside Docker. The default input is `manuscript/sovereignty_teleology_master_FINAL.md`.

## Quick Start

This repository supports two build flows:

- a simple top-level Markdown manuscript build through Pandoc
- a Quarto modular-project zip build from `scaffolds/`

### Quick Start: Simple Markdown Manuscript

Build the legacy top-level manuscript with Docker:

```bash
docker build -t theology-pdf .
docker run --rm -v $(pwd):/work -w /work theology-pdf make pdf
```

Or, with Docker Compose:

```bash
docker compose run --rm pdf
```

The default PDF is written to `output/sovereignty_teleology_master_FINAL.pdf`.

### Quick Start: Latest Quarto Zip in `scaffolds/`

Build the latest versioned project zip currently in `scaffolds/`:

```bash
python3 scripts/build_quarto_zip_project.py --zip scaffolds/sovereignty_quarto_modules_v0_29.zip --image quarto-pdf
```

Equivalent `make` entrypoint:

```bash
make quarto-zip-pdf QUARTO_IMAGE=quarto-pdf QUARTO_ZIP=scaffolds/sovereignty_quarto_modules_v0_29.zip
```

The rendered PDF is written to `output/sovereignty_quarto_modules_v0_29.pdf`.

## Options

- Use another manuscript: `make docker-pdf INPUT=manuscript/other.md`
- Run locally (without Docker, requires pandoc + TeX): `make pdf`
- Clean outputs: `make clean`
- With Docker Compose, override inputs on the fly: `INPUT=manuscript/other.md OUTPUT=output/other.pdf docker compose run --rm pdf`
- If a build fails early, re-run with verbose logs: `docker compose build --progress=plain --no-cache`

## Pipeline pieces

- `Dockerfile` installs Pandoc, XeLaTeX, and fonts (Gentium Plus, SBL Hebrew, Libertinus).
- `Makefile` wraps the Pandoc call and Docker convenience targets.
- `pandoc/defaults.yaml` sets engine, template, and fonts; `pandoc/metadata.yaml` holds title data.
- `templates/academic_template.tex` defines the journal-style layout and tcolorbox styles.
- `filters/pandoc_filters.lua` maps fenced code blocks with classes `text`, `logic`, `contrast`, or `diagram` into styled boxes.
- Manuscript lives in `manuscript/`; PDFs land in `output/`.

## Quarto Scaffold

The reusable Quarto modular-project scaffold now lives outside the top-level `manuscript/` directory at `quarto_template/quarto_project_scaffold_v0_22/`.

This is intentional:

- top-level `manuscript/` is reserved for an actual paper project or legacy source manuscript
- `scaffolds/` is an ignored drop zone for project zip files and temporary expansion workspaces
- committed reusable template source lives under `quarto_template/`

Project zip files for Quarto builds should also live in `scaffolds/`. If zip files are accidentally dropped into top-level `manuscript/`, run:

```bash
make move-quarto-zips
```

## Quarto Zip Builds

Drop versioned project zips such as `sovereignty_quarto_modules_v0_23.zip` into `scaffolds/`, then build the latest versioned archive with:

```bash
make quarto-zip-pdf QUARTO_IMAGE=quarto-pdf
```

Or build a specific zip:

```bash
make quarto-zip-pdf QUARTO_IMAGE=quarto-pdf QUARTO_ZIP=scaffolds/sovereignty_quarto_modules_v0_22.zip
```

List discovered zip projects:

```bash
make quarto-zip-list
```

Attempt all discovered zip projects in version order:

```bash
make quarto-zip-pdf-all QUARTO_IMAGE=quarto-pdf
```

The build copies the reusable scaffold from `quarto_template/` into a temporary workspace named from the zip stem under ignored `scaffolds/`, unpacks the selected zip there, renders the PDF in Docker, and writes the result to top-level `output/<zip-stem>.pdf`.

If a dropped zip still contains module YAML front matter or placeholder markers, the build will fail validation and no PDF will be produced for that archive.

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
