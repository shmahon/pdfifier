
# Codex Quarto Pipeline v1 Addendum

## Critical Instruction

Do NOT modify the currently working Hebrew and Greek font configuration in the existing pipeline.

Codex has already achieved a functioning multilingual rendering pipeline after substantial effort.
Preserving that working configuration is more important than aligning the implementation to any
theoretical font preference listed in the original specification.

If the existing pipeline renders Greek and Hebrew correctly, Codex must leave that configuration unchanged.

---

# 1. Hebrew Font Fallback Policy

If Codex’s current pipeline already renders Hebrew correctly, that configuration becomes the canonical implementation.

Fallback policy therefore becomes:

Primary rule:
Preserve the currently working Hebrew-capable font already configured in the pipeline.

Named fallback (documentation only):
Use any already-installed Hebrew-capable font present in the working pipeline environment.

Codex should **not change fonts merely to satisfy the spec**.

---

# 2. Definition of “Well‑Formed” Semantic Blocks

Validation should treat a required semantic block as well‑formed if:

1. It begins with a fenced Div opener:

::: {.logicblock}
::: {.contrastblock}
::: {.structuraldiagram}

2. It ends with a matching closing fence:

:::

3. The block fences are balanced.
4. The class name is exactly one of:

logicblock
contrastblock
structuraldiagram

5. Nested Markdown content is allowed.

Validation behavior:

Hard failure:
- Unbalanced fences
- Invalid required class names

Warning only:
- Unknown additional classes

---

# 3. 00_frontmatter.qmd Policy

Metadata must live exclusively in:

_quarto.yml

The file:

00_frontmatter.qmd

may remain as a content module, but it must not contain YAML metadata.

It may contain:

- abstract
- epigraph
- opening prose
- acknowledgements

If no such content exists it may remain empty or be removed from MANIFEST.json.

---

# 4. Placeholder Detection Policy

Validator must detect placeholders using two mechanisms.

Generic markers:

TODO
TK
TBD
[PLACEHOLDER]
*(placeholder)*

Legacy known placeholder strings from earlier drafts may also remain in validation checks.

Render builds must fail if placeholders appear inside any module listed in MANIFEST.json.

Draft placeholders are allowed only in files that are excluded from MANIFEST.json.

---

# 5. Output PDF Contract

Rendered PDF location:

output/

Preferred stable filename:

output/sovereignty_teleology.pdf

Codex may optionally include a versioned filename for archival builds, but the default build target should produce the stable filename above.

---

# 6. Semantic Block Authoring Standard

Canonical syntax going forward:

fenced Div blocks

Example:

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

Legacy fenced code block classes may be tolerated for backward compatibility, but all new authoring should use fenced Div syntax.

---

# Summary

This addendum clarifies:

• Preserve the working Hebrew/Greek font pipeline exactly.
• Define precise validation rules for semantic blocks.
• Ensure metadata remains in _quarto.yml.
• Standardize placeholder detection.
• Define the PDF output path and filename.
• Establish fenced Divs as the canonical syntax for semantic visual blocks.
