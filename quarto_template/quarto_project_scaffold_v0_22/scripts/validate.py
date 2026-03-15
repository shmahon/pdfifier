#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MODULE_DIR = ROOT / "manuscript" / "modules"
MASTER = ROOT / "manuscript" / "master.qmd"
MANIFEST_PATH = MODULE_DIR / "MANIFEST.json"
VALID_CLASSES = {"logicblock", "contrastblock", "structuraldiagram"}
PLACEHOLDER_PATTERNS = [
    "TODO",
    "TK",
    "TBD",
    "[PLACEHOLDER]",
    "*(placeholder)*",
    "Section 4 — Scriptural Density Index *(placeholder)*",
    "Section 5 — Historical Distortion Timeline *(placeholder)*",
    "Section 6 — Doctrinal Compression Mapping *(placeholder)*",
    "Conclusion — Counter-Thesis and Ethical Consequences *(placeholder)*",
    "# Appendix / Notes",
]
DIV_OPEN_RE = re.compile(r"^:::\s*\{([^}]*)\}\s*$")
FRONT_MATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|$)", re.DOTALL)


def load_manifest():
    if not MANIFEST_PATH.exists():
        raise SystemExit("MANIFEST.json not found in manuscript/modules")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def module_has_yaml_front_matter(text: str) -> bool:
    return bool(FRONT_MATTER_RE.match(text))


def find_placeholders(text: str):
    return [pattern for pattern in PLACEHOLDER_PATTERNS if pattern in text]


def validate_semantic_blocks(text: str):
    errors = []
    warnings = []
    stack = []

    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped == ":::":  # closing fence
            if stack:
                stack.pop()
            continue

        match = DIV_OPEN_RE.match(stripped)
        if not match:
            continue

        classes = [token[1:] for token in match.group(1).split() if token.startswith(".")]
        recognized = [cls for cls in classes if cls in VALID_CLASSES]
        unknown = [cls for cls in classes if cls not in VALID_CLASSES]

        if recognized:
            if len(recognized) != 1:
                errors.append(f"line {lineno}: semantic block must declare exactly one valid class")
            stack.append((recognized[0], lineno))
            if unknown:
                warnings.append(f"line {lineno}: unknown semantic block class(es): {', '.join(unknown)}")
        elif classes:
            warnings.append(f"line {lineno}: unknown semantic block class(es): {', '.join(unknown)}")

    for class_name, lineno in stack:
        errors.append(f"line {lineno}: unbalanced semantic block fence for .{class_name}")

    return errors, warnings


def main():
    manifest = load_manifest()
    parts = []
    module_presence = {}
    missing_modules = []
    modules_with_yaml = {}
    placeholders_by_module = {}
    semantic_errors = {}
    semantic_warnings = {}

    for name in manifest:
        path = MODULE_DIR / name
        if not path.exists():
            missing_modules.append(name)
            continue

        content = path.read_text(encoding="utf-8")
        normalized = content.rstrip()
        parts.append(normalized)

        if module_has_yaml_front_matter(content):
            modules_with_yaml[name] = True

        placeholders = find_placeholders(content)
        if placeholders:
            placeholders_by_module[name] = placeholders

        block_errors, block_warnings = validate_semantic_blocks(content)
        if block_errors:
            semantic_errors[name] = block_errors
        if block_warnings:
            semantic_warnings[name] = block_warnings

    if not MASTER.exists():
        raise SystemExit("master.qmd not found. Run assemble first.")

    master_actual = MASTER.read_text(encoding="utf-8")
    master_expected = "\n\n".join(parts) + "\n"
    for name in manifest:
        path = MODULE_DIR / name
        if path.exists():
            module_presence[name] = path.read_text(encoding="utf-8").rstrip() in master_actual

    result = {
        "master_equals_concat": master_actual == master_expected,
        "all_modules_present_in_master": all(module_presence.values()) and not missing_modules,
        "module_presence": module_presence,
        "manifest_modules_exist": not missing_modules,
        "missing_modules": missing_modules,
        "modules_without_yaml_metadata": not modules_with_yaml,
        "modules_with_yaml_metadata": sorted(modules_with_yaml),
        "placeholders_removed_from_master": not placeholders_by_module and not find_placeholders(master_actual),
        "placeholders_by_module": placeholders_by_module,
        "semantic_blocks_well_formed": not semantic_errors,
        "semantic_block_errors": semantic_errors,
        "semantic_block_warnings": semantic_warnings,
    }

    out = MODULE_DIR / "VALIDATION.build.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

    if not all([
        result["master_equals_concat"],
        result["all_modules_present_in_master"],
        result["manifest_modules_exist"],
        result["modules_without_yaml_metadata"],
        result["placeholders_removed_from_master"],
        result["semantic_blocks_well_formed"],
    ]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
