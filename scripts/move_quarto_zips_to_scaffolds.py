#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = ROOT / "manuscript"
SCAFFOLDS_DIR = ROOT / "scaffolds"


def main() -> int:
    SCAFFOLDS_DIR.mkdir(parents=True, exist_ok=True)
    moved = 0
    for path in sorted(MANUSCRIPT_DIR.glob("*_quarto_*.zip")) + sorted(MANUSCRIPT_DIR.glob("*_modules_v*.zip")):
        destination = SCAFFOLDS_DIR / path.name
        if destination.exists():
            continue
        shutil.move(str(path), str(destination))
        print(f"Moved {path.relative_to(ROOT)} -> {destination.relative_to(ROOT)}")
        moved += 1
    if moved == 0:
        print("No new project zip files found in manuscript/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
