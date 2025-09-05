#!/usr/bin/env python3
"""Safe cleanup utility

Usage examples:
  # dry-run (default paths)
  python scripts/cleanup_temp.py --dry-run

  # actually remove files listed in a file and backup before deletion
  python scripts/cleanup_temp.py --file to_delete.txt --yes

The script moves files to an `archive_backups/` folder (preserving relative paths)
before deletion. It supports --dry-run, --yes (no prompt), and --backup-dir.
"""
from __future__ import annotations
import argparse
import shutil
from pathlib import Path
from datetime import datetime
import sys


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Safe cleanup utility: backs up then removes files")
    p.add_argument(
        "paths",
        nargs="*",
        help="Paths to remove (relative to repo root). If none provided, a small default list is used.",
    )
    p.add_argument("--file", "-f", help="Path to a file containing one path per line to remove")
    p.add_argument("--dry-run", action="store_true", help="Show actions without performing them")
    p.add_argument("--yes", action="store_true", help="Do not prompt for confirmation")
    p.add_argument(
        "--backup-dir",
        default="archive_backups",
        help="Directory where backups will be stored (default: archive_backups)",
    )
    return p.parse_args()


DEFAULT_PATHS = [
    "templates/react_homepage.html",
    "templates/core/home.html",
]


def confirm(prompt: str) -> bool:
    try:
        return input(prompt).strip().lower() in ("y", "yes")
    except EOFError:
        return False


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd()

    paths: list[Path] = []
    if args.paths:
        paths.extend(Path(p) for p in args.paths)
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: listed file not found: {file_path}")
            return 2
        for line in file_path.read_text(encoding="utf8").splitlines():
            line = line.strip()
            if line:
                paths.append(Path(line))
    if not paths:
        paths = [Path(p) for p in DEFAULT_PATHS]

    backup_root = repo_root / args.backup_dir
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    to_process: list[tuple[Path, Path]] = []
    for p in paths:
        abs_p = (repo_root / p).resolve()
        if not abs_p.exists():
            print(f"⚠️  Not found: {p}")
            continue
        # destination preserves relative path under backup_root and appends timestamp
        rel = abs_p.relative_to(repo_root)
        dest = backup_root / rel.parent / (rel.name + "." + timestamp + ".bak")
        to_process.append((abs_p, dest))

    if not to_process:
        print("Nothing to do.")
        return 0

    print("Planned actions:")
    for src, dst in to_process:
        print(f"  Move: {src} -> {dst}")

    if args.dry_run:
        print("Dry-run mode; no changes made.")
        return 0

    if not args.yes:
        if not confirm("Proceed and backup+remove the listed files? [y/N]: "):
            print("Aborted by user.")
            return 1

    for src, dst in to_process:
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            # move the file into backup location
            shutil.move(str(src), str(dst))
            print(f"✅ Backed up and removed: {src} -> {dst}")
        except Exception as exc:  # noqa: BLE001 - broad but desired to continue
            print(f"❌ Failed to move {src}: {exc}")

    print("\n🧹 Cleanup completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
