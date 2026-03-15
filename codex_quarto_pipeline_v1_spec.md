
# Codex Quarto Pipeline v1 Specification

## Purpose
This document defines the exact rules and architecture Codex should follow when extending the Quarto PDF pipeline for the paper *“Sovereignty, Teleology, and the Christian Life.”*

The goal is to eliminate ambiguity so that the renderer, modular assembly, and validation system remain stable.

---

# 1. Canonical Source Format

Source of truth:

manuscript/modules/*.qmd

Each module represents a section of the manuscript.

The assembled document:

manuscript/master.qmd

is **generated** and must never be edited directly.

Pipeline:

modules
↓
MANIFEST.json
↓
assemble.py
↓
master.qmd
↓
validate.py
↓
quarto render

Raw `.md` files are considered **legacy input only**.

Future papers should be authored directly in modular `.qmd`.

---

# 2. Metadata Ownership

All document metadata must live in:

_quarto.yml

Fields:

- title
- subtitle
- author
- date
- pdf engine
- fonts
- section numbering

Modules must **not contain YAML metadata**.

---

# 3. Quarto Project Type

This manuscript is an **academic article**, not a book.

The project should render a **single PDF article**.

Do NOT use:

project.type: book

---

# 4. Module Assembly Model

Assembly is deterministic and controlled by:

MANIFEST.json

The manifest defines module order.

Example:

[
  "00_frontmatter.qmd",
  "01_introduction.qmd",
  "02_section_1.qmd",
  "03_section_2.qmd",
  "04_section_3.qmd",
  "05_section_4.qmd",
  "06_section_5.qmd",
  "07_section_6.qmd",
  "08_conclusion.qmd"
]

`assemble.py` concatenates the modules into:

manuscript/master.qmd

---

# 5. Visual Artifact Syntax

The manuscript uses semantic blocks that must render consistently.

## Logic Blocks

::: {.logicblock}
instruction → equipping → participation in the work of ministry
:::

## Contrast Blocks

::: {.contrastblock}
Distortion

salvation = forgiveness only

Instead of

salvation = forgiveness + restored life
:::

## Structural Diagrams

::: {.structuraldiagram}
creation → fall → redemption → restored vocation
:::

All three block types must be supported in v1.

---

# 6. Styling Technology

Allowed styling methods:

- Quarto styling
- custom LaTeX environments
- Lua filters

Quarto-native styling alone is insufficient for the final layout.

---

# 7. TeX Engine

Required engine:

xelatex

Reason: reliable Unicode handling for Greek and Hebrew.

---

# 8. Fonts

Required defaults:

Main serif:
Libertinus Serif

Sans:
Libertinus Sans

Mono:
Libertinus Mono

Greek support:
Libertinus Serif or Gentium Plus

Hebrew support:
Preferred: SBL Hebrew

If SBL Hebrew cannot be installed reproducibly in Docker, provide documented fallback.

---

# 9. Validation Rules

The validator must confirm:

master_equals_concat

all_modules_present_in_master

placeholders_removed_from_master

Additional checks:

- modules listed in MANIFEST exist
- modules do not contain YAML metadata
- required fenced Div classes are well formed

---

# 10. Output Targets

v1 target:

PDF only

Future formats (HTML/DOCX) may be added later.

---

# 11. Asset Layout

Project-level assets only:

assets/
styles/
filters/

Modules must not maintain separate asset directories.

---

# 12. Placeholder Policy

Render builds must not contain placeholders.

If placeholders are needed during drafting they must be excluded from MANIFEST.json.

---

# 13. Repository Intent

First objective:

Make this paper render correctly.

Second objective:

Evolve this repository into a reusable Quarto renderer template.

---

# Implementation Summary

Codex should implement:

- modular assembly
- deterministic validation
- xelatex rendering
- Libertinus font stack
- support for logicblock / contrastblock / structuraldiagram
- reproducible Docker build
