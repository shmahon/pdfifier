local semantic_classes = {
  logicblock = "logicblock",
  contrastblock = "contrastblock",
  structuraldiagram = "diagramblock",
  hybriddiagram = "hybriddiagram",
}

local legacy_code_classes = {
  text = "logicblock",
  logic = "logicblock",
  contrast = "contrastblock",
  diagram = "diagramblock",
}

local function first_semantic_class(classes, mapping)
  if not classes then
    return nil
  end

  for _, class_name in ipairs(classes) do
    local env = mapping[class_name]
    if env then
      return env
    end
  end
end

local function latex_env(env, text)
  return pandoc.RawBlock("latex", string.format("\\begin{%s}\n%s\n\\end{%s}", env, text, env))
end

local function preserve_linebreaks(blocks)
  return pandoc.walk_block(pandoc.Div(blocks), {
    SoftBreak = function()
      return pandoc.LineBreak()
    end,
  }).content
end

local function latex_for_blocks(blocks)
  local preserved = preserve_linebreaks(blocks)
  local doc = pandoc.Pandoc(preserved)
  local latex = pandoc.write(doc, "latex")
  return latex:gsub("%s+$", "")
end

function Div(el)
  local env = first_semantic_class(el.classes, semantic_classes)
  if not env then
    return nil
  end

  return latex_env(env, latex_for_blocks(el.content))
end

function CodeBlock(el)
  local env = first_semantic_class(el.classes, legacy_code_classes)
  if not env then
    return nil
  end

  return latex_env(env, el.text)
end
