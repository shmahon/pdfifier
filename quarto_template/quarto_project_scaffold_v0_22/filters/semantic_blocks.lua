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

local function latex_for_inlines(inlines)
  local doc = pandoc.Pandoc({ pandoc.Plain(inlines) })
  local latex = pandoc.write(doc, "latex")
  local trimmed = latex:gsub("%s+$", "")
  return trimmed
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
  local trimmed = latex:gsub("%s+$", "")
  return trimmed
end

local function split_inlines_on_breaks(inlines)
  local lines = {}
  local current = {}

  local function push_current()
    if #current > 0 then
      table.insert(lines, current)
      current = {}
    end
  end

  for _, inline in ipairs(inlines) do
    if inline.t == "SoftBreak" or inline.t == "LineBreak" then
      push_current()
    else
      table.insert(current, inline)
    end
  end

  push_current()
  return lines
end

local function render_hybrid_block(el)
  local parts = { "\\begin{hybriddiagram}" }
  local after_divider = false

  for _, block in ipairs(el.content) do
    if block.t == "Para" or block.t == "Plain" then
      local lines = split_inlines_on_breaks(block.content)

      if #lines == 1 then
        local text = pandoc.utils.stringify(lines[1]):gsub("^%s+", ""):gsub("%s+$", "")
        local latex = latex_for_inlines(lines[1])

        if text == "↓" then
          table.insert(parts, string.format("\\hybriddivider{%s}", latex))
          after_divider = true
        else
          if after_divider then
            table.insert(parts, string.format("\\hybridnode{%s}", latex))
          else
            table.insert(parts, string.format("\\hybridlabel{%s}", latex))
          end
          after_divider = false
        end
      elseif #lines > 1 then
        local label = latex_for_inlines(lines[1])
        local details = {}

        for i = 2, #lines do
          table.insert(details, latex_for_inlines(lines[i]))
        end

        table.insert(parts, string.format("\\hybridstage{%s}{%s}", label, table.concat(details, " \\\\ ")))
        after_divider = false
      end
    else
      table.insert(parts, latex_for_blocks({ block }))
      after_divider = false
    end
  end

  table.insert(parts, "\\end{hybriddiagram}")
  return pandoc.RawBlock("latex", table.concat(parts, "\n"))
end

function Div(el)
  local env = first_semantic_class(el.classes, semantic_classes)
  if not env then
    return nil
  end

  if env == "hybriddiagram" then
    return render_hybrid_block(el)
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
