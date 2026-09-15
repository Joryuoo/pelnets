"""Report unused Files/ images; move them only with an explicit --move flag."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parent
OBSIDIAN = re.compile(r"!\[\[([^\]]+)\]\]")
MARKDOWN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def references(root: Path) -> set[str]:
    names = set()
    for note in root.rglob("*.md"):
        if ".git" in note.parts:
            continue
        content = note.read_text(encoding="utf-8", errors="replace")
        for link in OBSIDIAN.findall(content):
            names.add(Path(link.split("|", 1)[0].strip()).name)
        for link in MARKDOWN.findall(content):
            names.add(Path(link.split("?", 1)[0].strip()).name)
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--move", action="store_true", help="Move reported images into unused_images_dummy/")
    args = parser.parse_args()
    root = args.root.resolve()
    files_dir = root / "Files"
    if not files_dir.is_dir():
        parser.error(f"Missing Files directory: {files_dir}")
    image_files = sorted(path for path in files_dir.rglob("*")
                         if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES)
    used = references(root)
    unused = [path for path in image_files if path.name not in used]
    print(f"Found {len(image_files)} images; {len(unused)} have no Markdown embed.")
    for path in unused:
        print(path.relative_to(root))
    if not args.move:
        print("Read-only report. Pass --move to relocate these files.")
        return 0
    destination = root / "unused_images_dummy"
    conflicts = [destination / path.relative_to(files_dir) for path in unused
                 if (destination / path.relative_to(files_dir)).exists()]
    if conflicts:
        parser.error(f"Refusing to overwrite {len(conflicts)} destination image(s)")
    for path in unused:
        target = destination / path.relative_to(files_dir)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(target))
    print(f"Moved {len(unused)} images into {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
