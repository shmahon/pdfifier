#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLDS_DIR = ROOT / "scaffolds"
DEFAULT_TEMPLATE = ROOT / "quarto_template" / "quarto_project_scaffold_v0_22"
OUTPUT_DIR = ROOT / "output"
VERSION_RE = re.compile(r"_v(?P<version>\d+(?:_\d+)*)\.zip$")


def parse_version(path: Path) -> tuple[int, ...]:
    match = VERSION_RE.search(path.name)
    if not match:
        raise ValueError(f"zip filename must contain a version suffix like _v0_23.zip: {path.name}")
    return tuple(int(part) for part in match.group("version").split("_"))


def discover_zip_files() -> list[Path]:
    return sorted(SCAFFOLDS_DIR.glob("*.zip"))


def select_zip(explicit: str | None) -> Path:
    if explicit:
        candidate = Path(explicit)
        if not candidate.is_absolute():
            candidate = ROOT / explicit
        if not candidate.exists():
            raise FileNotFoundError(f"zip file not found: {candidate}")
        return candidate

    candidates = discover_zip_files()
    if not candidates:
        raise FileNotFoundError("no project zip files found in scaffolds/")
    return max(candidates, key=parse_version)


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def unzip_modules(zip_path: Path, target_manuscript_dir: Path) -> None:
    modules_dir = target_manuscript_dir / "modules"
    modules_dir.mkdir(parents=True, exist_ok=True)

    with ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        if "modules/MANIFEST.json" not in names:
            raise ValueError(f"{zip_path.name} is missing modules/MANIFEST.json")

        for name in archive.namelist():
            if name.endswith("/"):
                continue
            if name.startswith("modules/"):
                destination = modules_dir / name.removeprefix("modules/")
            elif name == "master.qmd":
                destination = target_manuscript_dir / "master.qmd"
            else:
                continue

            destination.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name) as src, destination.open("wb") as dst:
                shutil.copyfileobj(src, dst)


def normalize_output(scaffold_root: Path, zip_path: Path) -> Path:
    raw = scaffold_root / "output" / "sovereignty_teleology.pdf"
    if not raw.exists():
        raise FileNotFoundError(f"expected PDF was not produced: {raw}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT_DIR / f"{zip_path.stem}.pdf"
    shutil.copy2(raw, destination)
    return destination


def build_project(zip_path: Path, template_dir: Path, image: str) -> Path:
    with tempfile.TemporaryDirectory(prefix=f"{zip_path.stem}_", dir=str(ROOT / "scaffolds")) as temp_dir:
        workdir = Path(temp_dir)
        scaffold_root = workdir / zip_path.stem
        shutil.copytree(template_dir, scaffold_root)

        # Remove scaffold sample content so the zip becomes the source of truth.
        shutil.rmtree(scaffold_root / "manuscript" / "modules", ignore_errors=True)
        master = scaffold_root / "manuscript" / "master.qmd"
        if master.exists():
            master.unlink()

        unzip_modules(zip_path, scaffold_root / "manuscript")
        container_cmd = (
            "apt-get -o Acquire::Retries=10 -o Acquire::http::Timeout=60 update >/dev/null && "
            "apt-get -o Acquire::Retries=10 -o Acquire::http::Timeout=60 install -y --no-install-recommends "
            "lmodern xfonts-encodings xfonts-utils libfontenc1 texlive-fonts-recommended >/dev/null && "
            "make pdf"
        )
        run(["docker", "run", "--rm", "-v", f"{scaffold_root}:/work", "-w", "/work", image, "sh", "-lc", container_cmd], ROOT)
        return normalize_output(scaffold_root, zip_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Quarto project zip with the reusable scaffold.")
    parser.add_argument("--zip", dest="zip_path", help="Path to a specific project zip. Defaults to latest version in scaffolds/.")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE.relative_to(ROOT)), help="Scaffold directory to use.")
    parser.add_argument("--image", default="quarto-pdf", help="Docker image to run for PDF generation.")
    parser.add_argument("--list", action="store_true", help="List discovered project zips and exit.")
    parser.add_argument("--all", action="store_true", help="Attempt to build all discovered project zips in version order.")
    args = parser.parse_args()

    if args.list:
        for path in discover_zip_files():
            print(path.relative_to(ROOT))
        return 0

    template_dir = Path(args.template)
    if not template_dir.is_absolute():
        template_dir = ROOT / template_dir
    if not template_dir.exists():
        raise FileNotFoundError(f"scaffold template not found: {template_dir}")

    if args.all:
        failures = []
        successes = []
        for zip_path in sorted(discover_zip_files(), key=parse_version):
            try:
                pdf_path = build_project(zip_path, template_dir, args.image)
                successes.append((zip_path, pdf_path))
                print(f"Built {pdf_path.relative_to(ROOT)} from {zip_path.relative_to(ROOT)}")
            except Exception as exc:
                failures.append((zip_path, str(exc)))
                print(f"Failed {zip_path.relative_to(ROOT)}: {exc}", file=sys.stderr)

        if successes:
            print(f"Built {len(successes)} zip project(s).")
        if failures:
            print(f"{len(failures)} zip project(s) failed validation or rendering.", file=sys.stderr)
            return 1
        return 0

    zip_path = select_zip(args.zip_path)
    pdf_path = build_project(zip_path, template_dir, args.image)
    print(f"Built {pdf_path.relative_to(ROOT)} from {zip_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
