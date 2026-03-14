local function has_class(el, class)
  if not el.classes then return false end
  for _, c in ipairs(el.classes) do
    if c == class then return true end
  end
  return false
end

function CodeBlock(el)
  local env
  if has_class(el, "contrast") then
    env = "contrastblock"
  elseif has_class(el, "diagram") then
    env = "diagramblock"
  elseif has_class(el, "logic") or has_class(el, "text") then
    env = "logicblock"
  end

  if env then
    return pandoc.RawBlock("latex", string.format("\\begin{%s}\n%s\n\\end{%s}", env, el.text, env))
  end
end
