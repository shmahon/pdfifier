local semantic_classes = {
  logicblock = "logicblock",
  contrastblock = "contrastblock",
  structuraldiagram = "diagramblock",
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

function Div(el)
  local env = first_semantic_class(el.classes, semantic_classes)
  if not env then
    return nil
  end

  local content = pandoc.write(pandoc.Pandoc(el.content), "plain")
  return latex_env(env, content:gsub("%s+$", ""))
end

function CodeBlock(el)
  local env = first_semantic_class(el.classes, legacy_code_classes)
  if not env then
    return nil
  end

  return latex_env(env, el.text)
end
