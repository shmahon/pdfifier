# Biblical Studies Authoring Style
Persistent configuration for academic biblical manuscripts.

## Activation Phrase
Use Biblical Studies Authoring Style.

## Core Principles
1. Text-governed exegesis.
2. Canonical coherence over rhetorical convenience.
3. Teleological reading of redemption (creation → fall → redemption → restored vocation).
4. Explicit distinction between:
   - descriptive
   - theological
   - paraenetic (ethical exhortation).

## Exegetical Method
Every interpretive claim should pass through:
1. Textual observation
2. Lexical analysis (Hebrew/Greek)
3. Literary context
4. Canonical placement
5. Theological synthesis

## Argument Compression Structures
Use semantic argument blocks where helpful:

### Logic Block
::: {.logicblock}
instruction → equipping → participation in ministry
:::

### Contrast Block
::: {.contrastblock}
Distortion
salvation = forgiveness only

Instead of
salvation = forgiveness + restored life
:::

### Structural Diagram
::: {.structuraldiagram}
creation
↓
fall
↓
redemption
↓
restored vocation
:::

### Hybrid Diagram
::: {.hybriddiagram}
creation purpose
→ humanity created for God's glory

fall
→ corruption and bondage

redemption
→ justification through Christ
:::

Renderer-aware authoring constraints:

- Use `logicblock` only when the semantic chain should read left-to-right in the final PDF.
- Keep left-to-right relations on the same authored line inside `logicblock`.
- Use `structuraldiagram` only when the argument should read as vertically staged flow.
- Use `hybriddiagram` when each stage has a governing label plus a subordinate arrow line or subordinate stage content.
- Do not split a left-to-right pair across lines unless the intended PDF result is hierarchical rather than inline.
- Do not expect the PDF renderer to infer whether a block should become left-to-right, top-to-bottom, or hierarchical if the markdown source does not encode that choice explicitly.
- When comparison structure matters rhetorically, use `contrastblock` rather than plain paragraphs.

## Narrative Architecture for Papers
Typical structure:

1. Introduction – statement of theological problem
2. Biblical Dataset – textual evidence
3. Interpretive Distortions – diagnostic analysis
4. Canonical Topology – theological reconstruction
5. Paraenesis – implications for Christian life
6. Ecclesial Implications
7. Conclusion

## Theological Emphasis
The authoring style assumes:

- redemption restores vocation
- salvation produces visible transformation
- doctrine and life are inseparable
- Christian witness vindicates the gospel publicly

## Writing Tone
Preferred style:

- analytical
- text-driven
- minimal rhetorical inflation
- dense conceptual compression
- clear structural scaffolding
