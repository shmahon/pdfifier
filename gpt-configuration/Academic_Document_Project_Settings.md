# Academic Document Project Settings
Persistent configuration for building modular academic manuscripts into high‑quality PDFs.

## Activation Phrase
Use Academic Document Project Settings.

## Purpose
This configuration defines the technical environment for writing and publishing academic papers using:

- Modular Quarto manuscripts
- Docker‑based reproducible builds
- LaTeX PDF rendering
- Semantic argument blocks
- Validation‑driven compilation

The system ensures that manuscripts remain:

- structurally stable
- reproducible
- versioned
- typographically correct
- compatible with multilingual academic writing.

---

# Core Principles

1. **Modular manuscript structure**
2. **Separation of authoring and rendering**
3. **Validation before rendering**
4. **Stable typography**
5. **Reproducible container builds**
6. **Semantic argument structures**

---

# Repository Structure

A repository using this configuration should follow:

repo/
├─ manuscript/
├─ output/
├─ filters/
├─ templates/
├─ pandoc/
├─ scaffolds/
│  └─ quarto_project_scaffold_v0_22/
│     ├─ _quarto.yml
│     ├─ Dockerfile
│     ├─ Makefile
│     ├─ build.sh
│     ├─ filters/
│     ├─ styles/
│     ├─ scripts/
│     ├─ manuscript/
│     │  ├─ master.qmd
│     │  └─ modules/
│     └─ output/
├─ scripts/
└─ quarto_project_constraint_file.md

---

# Modular Manuscript Rules

Source of truth:

manuscript/modules/*.qmd

Module order:

MANIFEST.json

Rules:

- modules must not contain YAML metadata
- modules must not contain placeholders
- metadata belongs only in `_quarto.yml`

---

# Semantic Block System

logicblock

::: {.logicblock}
instruction → equipping → participation
:::

contrastblock

::: {.contrastblock}
Distortion
salvation = forgiveness only

Instead of
salvation = forgiveness + restored life
:::

structuraldiagram

::: {.structuraldiagram}
creation → fall → redemption → restored vocation
:::

---

# Validation Requirements

Before building PDFs the system must confirm:

master_equals_concat
all_modules_present_in_master
manifest_modules_exist
modules_without_yaml_metadata
placeholders_removed_from_master
semantic_blocks_well_formed

Placeholder detection must fail on:

TODO
TK
TBD
[PLACEHOLDER]
*(placeholder)*

---

# Multilingual Font Configuration

Greek:
Gentium Plus

Hebrew:
Ezra SIL

The rendering pipeline must preserve these working font settings.

---

# Build Workflow

make assemble
make validate
make pdf

Docker execution:

docker build -t quarto-pdf ./scaffolds/quarto_project_scaffold_v0_22

docker run --rm -v $(pwd)/scaffolds/quarto_project_scaffold_v0_22:/work -w /work quarto-pdf make pdf

---

# Zip Manuscript Builds

Versioned manuscript packages may be built automatically.

Example:

sovereignty_quarto_modules_v0_24.zip

Rules:

- zip contains modules
- builder unpacks modules into scaffold
- scaffold itself is never modified

Output:

output/<zip-name>.pdf

---

# Output Contract

Stable final output:

output/sovereignty_teleology.pdf

If Quarto produces nested output paths they must be normalized.

---

# Editing Constraints

Future editing sessions must:

- not add YAML to modules
- not move metadata from `_quarto.yml`
- not convert article projects into Quarto books
- not alter font pipeline without explicit instruction
