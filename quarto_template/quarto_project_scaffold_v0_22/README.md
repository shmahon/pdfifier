# Quarto Article Pipeline

This scaffold renders a modular Quarto manuscript as a single academic PDF article.

Source of truth lives in `manuscript/modules/*.qmd`. `manuscript/master.qmd` is generated from `MANIFEST.json` and should not be edited directly.

## Workflow

1. Edit modules in `manuscript/modules/`
2. Keep module order in `manuscript/modules/MANIFEST.json`
3. Run:

```bash
make pdf
```

This will:

- assemble `manuscript/master.qmd`
- validate manifest integrity, module shape, placeholders, and semantic blocks
- render `output/sovereignty_teleology.pdf` through Quarto

## Commands

```bash
make assemble
make validate
make pdf
make clean
```

## Metadata

Document metadata is owned by `_quarto.yml`. Modules must not contain YAML front matter.

## Semantic Blocks

Canonical authoring syntax uses fenced Divs:

```markdown
::: {.logicblock}
instruction → equipping → participation in the work of ministry
:::
```

Supported semantic classes:

- `logicblock`
- `contrastblock`
- `structuraldiagram`

Legacy fenced code block classes remain supported for backward compatibility.

## Fonts

The Quarto scaffold preserves the working multilingual font behavior from the existing pipeline:

- serif typography via the LaTeX `libertinus` package
- Greek transitions: Gentium Plus
- Hebrew transitions: Ezra SIL

## Docker

Build and run the scaffold in Docker:

```bash
docker build -t quarto-pdf ./quarto_template/quarto_project_scaffold_v0_22
docker run --rm -v $(pwd)/quarto_template/quarto_project_scaffold_v0_22:/work -w /work quarto-pdf make pdf
```
