# Quarto Project Constraint File

Use this file as a mergeable constraint source for future ChatGPT/Codex sessions that must build Quarto-based academic PDFs in this repository style.

## Repository Intent

- The repository may contain both:
  - a legacy Pandoc pipeline for single-file Markdown manuscripts
  - a reusable Quarto modular-project scaffold
- The Quarto scaffold is a reusable template, not the live manuscript.

## Directory Layout

Top-level layout must follow this contract:

```text
repo/
├─ manuscript/                      # actual paper sources or legacy single-file manuscript
├─ output/                          # output for the top-level legacy pipeline
├─ quarto_template/
│  └─ quarto_project_scaffold_v0_22/
│     ├─ _quarto.yml
│     ├─ Dockerfile
│     ├─ Makefile
│     ├─ build.sh
│     ├─ README.md
│     ├─ filters/
│     ├─ styles/
│     ├─ scripts/
│     ├─ manuscript/
│     │  ├─ master.qmd
│     │  └─ modules/
│     └─ output/
├─ filters/                         # top-level legacy pandoc filters
├─ templates/                       # top-level legacy LaTeX templates
├─ pandoc/                          # top-level legacy pandoc defaults/metadata
├─ scaffolds/
│  └─ *.zip                         # ignored drop zone for project archives and temp workspaces
├─ scripts/
│  ├─ build_quarto_zip_project.py
│  └─ move_quarto_zips_to_scaffolds.py
└─ quarto_project_constraint_file.md
```

Directory rules:

- Do not place the reusable Quarto scaffold under top-level `manuscript/`.
- Reserve top-level `manuscript/` for an actual paper project or legacy manuscript input.
- Reserve `scaffolds/` as an ignored drop zone for Quarto project zip files and temporary expansion workspaces.
- Keep the committed reusable scaffold under `quarto_template/`.
- Within the Quarto scaffold, `manuscript/modules/*.qmd` is the source of truth.

## Quarto Project Rules

- Project type is a single PDF article, not a Quarto book.
- Metadata belongs in `_quarto.yml`, not in module YAML front matter.
- `manuscript/master.qmd` is generated and must not be edited directly.
- Module order is controlled only by `manuscript/modules/MANIFEST.json`.
- Modules included in `MANIFEST.json` must not contain placeholders.
- Modules included in `MANIFEST.json` must not contain YAML front matter.

## Semantic Block Rules

Canonical source syntax is fenced Divs:

```markdown
::: {.logicblock}
instruction → equipping → participation in the work of ministry
:::

::: {.contrastblock}
Distortion
salvation = forgiveness only

Instead of
salvation = forgiveness + restored life
:::

::: {.structuraldiagram}
creation → fall → redemption → restored vocation
:::
```

Rendering rules:

- `logicblock`, `contrastblock`, and `structuraldiagram` must all render in PDF.
- Legacy fenced code block classes may be tolerated for backward compatibility, but new authoring should use fenced Divs.
- Validation must fail on unbalanced semantic block fences or invalid semantic class names.

## Validation Rules

Validation must confirm:

- `master_equals_concat`
- `all_modules_present_in_master`
- `manifest_modules_exist`
- `modules_without_yaml_metadata`
- `placeholders_removed_from_master`
- `semantic_blocks_well_formed`

Placeholder detection must fail on these markers in any module listed in `MANIFEST.json`:

- `TODO`
- `TK`
- `TBD`
- `[PLACEHOLDER]`
- `*(placeholder)*`

## Font and Unicode Rules

- Preserve the working multilingual behavior already established in this repo.
- Greek handling uses `Gentium Plus`.
- Hebrew handling uses `Ezra SIL`.
- Do not change Greek/Hebrew behavior merely to satisfy a theoretical preference.
- For the Quarto scaffold, prefer LaTeX-side configuration that works with the installed TeX environment over optimistic system-font assumptions.

## Build Rules

Inside the Quarto scaffold directory:

```bash
make assemble
make validate
make pdf
```

Container build/run pattern:

```bash
docker build -t quarto-pdf ./quarto_template/quarto_project_scaffold_v0_22
docker run --rm -v $(pwd)/quarto_template/quarto_project_scaffold_v0_22:/work -w /work quarto-pdf make pdf
```

Zip-driven build pattern:

```bash
make move-quarto-zips
make quarto-zip-list
make quarto-zip-pdf QUARTO_IMAGE=quarto-pdf
make quarto-zip-pdf-all QUARTO_IMAGE=quarto-pdf
make quarto-zip-pdf QUARTO_IMAGE=quarto-pdf QUARTO_ZIP=scaffolds/sovereignty_quarto_modules_v0_23.zip
```

Zip build rules:

- Quarto project zip files must include a version suffix in the filename, such as `_v0_23.zip`.
- If no explicit zip is given, the builder must select the highest versioned zip in `scaffolds/`.
- The builder may also support batch building all discovered zips in version order.
- The builder must unpack the zip into a temporary project workspace named from the zip stem under ignored `scaffolds/`, using a copy of the reusable scaffold from `quarto_template/` as the base.
- The builder must treat the zip contents as the source of truth for `manuscript/modules/`.
- The builder must write the rendered PDF to top-level `output/<zip-stem>.pdf`.
- The reusable scaffold itself must not be mutated as part of a zip build.
- If a zip violates validation constraints, it must fail clearly rather than being silently normalized into conformance.

Output contract:

- Required stable output path: `output/sovereignty_teleology.pdf`
- If Quarto writes to `output/manuscript/sovereignty_teleology.pdf`, normalize it to `output/sovereignty_teleology.pdf`

## Editing Rules for Future Sessions

- If changing Quarto scaffold behavior, edit files under `quarto_template/quarto_project_scaffold_v0_22/`, not top-level legacy pipeline files, unless the user explicitly asks for both.
- Do not reintroduce a scaffold path under top-level `manuscript/`.
- Do not add module YAML metadata.
- Do not move metadata ownership out of `_quarto.yml`.
- Do not convert the article scaffold into a Quarto book.
- Treat this file as a structural constraint source intended to be merged with other project-specific constraints.
