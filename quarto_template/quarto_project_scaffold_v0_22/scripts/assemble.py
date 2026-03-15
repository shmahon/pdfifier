#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MODULE_DIR = ROOT / "manuscript" / "modules"
MASTER = ROOT / "manuscript" / "master.qmd"

manifest_path = MODULE_DIR / "MANIFEST.json"
if not manifest_path.exists():
    raise SystemExit("MANIFEST.json not found in manuscript/modules")

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

parts = []
for name in manifest:
    path = MODULE_DIR / name
    if not path.exists():
        raise SystemExit(f"Missing module listed in manifest: {name}")
    parts.append(path.read_text(encoding="utf-8").rstrip())

master = "\n\n".join(parts) + "\n"
MASTER.write_text(master, encoding="utf-8")
print(f"Wrote {MASTER}")
