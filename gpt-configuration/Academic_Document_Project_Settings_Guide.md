# Academic Document Project Settings — Usage Guide

This document explains how to use the Academic Document Project Settings configuration.

## What This Configuration Does

The configuration provides a reproducible system for producing professional academic PDFs from modular manuscripts.

It integrates:

- Quarto
- Docker
- LaTeX
- validation tooling
- semantic argument structures

The result is a publishing environment similar to those used in professional academic workflows.

---

# How to Activate

When working in a ChatGPT project containing this file, activate the configuration by stating:

Use Academic Document Project Settings.

This instructs the assistant to:

- structure manuscripts modularly
- enforce validation rules
- generate Quarto‑compatible modules
- maintain multilingual typography
- produce versioned manuscript builds
- author semantic blocks using the exact syntax expected by the PDF renderer

---

# How It Fits Into Your Research System

Your workflow now has three layers.

## 1 Authoring Style

Biblical_Studies_Authoring_Style.md

Controls:

- theological argument structure
- exegetical method
- semantic argument blocks

## 2 Research Workflow

Biblical_Research_Notebook_Framework.md

Controls:

- research phases
- dataset building
- canonical topology analysis

## 3 Publishing Pipeline

Academic_Document_Project_Settings.md

Controls:

- document structure
- rendering pipeline
- validation rules
- PDF generation

It also controls renderer-aware source syntax for any manuscript feature whose final appearance depends on the Quarto-to-LaTeX pipeline.

## Renderer-Aware Authoring Rule

If a future session needs a block, diagram, comparison, or other visually distinct structure to render correctly in PDF, it must choose from the semantic block classes already supported by the pipeline and author the source accordingly.

Use:

- `logicblock` for left-to-right chains authored on one line
- `structuraldiagram` for true top-to-bottom flow
- `hybriddiagram` for staged hierarchical blocks with subordinate arrow lines or mixed vertical/horizontal progression
- `contrastblock` for visible comparison blocks

Do not rely on plain paragraphs, ad hoc indentation, or “the renderer will figure it out later” authoring. The pipeline expects explicit semantic block syntax.

---

# Typical Workflow

1 Define research problem

2 Build research notebook

3 Convert notebook into manuscript modules

modules/

00_frontmatter
01_introduction
02_dataset
03_analysis
04_theological_topology
05_paraenesis
06_ecclesial_implications
07_conclusion

4 Validate manuscript

5 Build PDF

---

# Benefits

Using this system ensures:

- reproducible academic documents
- stable typography
- modular research development
- reliable multilingual typesetting
- containerized builds
- versioned manuscript archives

---

# Recommended Use

Upload the following files as project Sources:

Academic_Document_Project_Settings.md
Biblical_Studies_Authoring_Style.md
Biblical_Research_Notebook_Framework.md

Then activate them in future sessions with:

Use Academic Document Project Settings.
Use Biblical Studies Authoring Style.
Use Biblical Research Notebook Framework.

If the session will draft or revise Quarto manuscript modules, it should also be told to follow the semantic block syntax required by the PDF pipeline, especially when authoring diagrams, logical chains, or comparison blocks.
