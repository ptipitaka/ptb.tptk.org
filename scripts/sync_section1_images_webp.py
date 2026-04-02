# -*- coding: utf-8 -*-
"""Build docs/public/.../section-1/01.webp … from Initial_source JPGs (merge split manuscript pages)."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "Initial_source" / "html5" / "04-web-resources" / "image"
OUT_DIR = ROOT / "docs" / "public" / "images" / "07-part-2-historical-documents" / "section-1"

# (top, bottom, optional_premerged_basename) — ถ้ามีไฟล์รวมใน SRC แล้วจะใช้แทนการต่อ
Merge3 = tuple[str, str, str | None]

# Order after merge (matches build_part2_historical_documents.collapse_section1_merged_pairs)
SOURCES: list[str | Merge3] = [
    "IMG_03.jpg",
    "IMG_04.jpg",
    ("A4-02-002.jpg", "A4-02-0021.jpg", "A4-02-002-0021.jpg"),
    ("A4-04.jpg", "A4-041.jpg", "A4-04-041.jpg"),
    "A4-05.jpg",
    "A4-06.jpg",
    "A4-07.jpg",
    "A4-08.jpg",
    "A4-09.jpg",
    "A4-101.jpg",
    "A4-11.jpg",
    "A4-12.jpg",
    "A4-13.jpg",
]

WEBP_QUALITY = 88


def load_rgb(path: Path) -> Image.Image:
    im = Image.open(path)
    if im.mode in ("RGBA", "P"):
        return im.convert("RGB")
    if im.mode != "RGB":
        return im.convert("RGB")
    return im


def merge_vertical(top: Path, bottom: Path) -> Image.Image:
    a = load_rgb(top)
    b = load_rgb(bottom)
    w = max(a.width, b.width)
    h = a.height + b.height
    out = Image.new("RGB", (w, h), (255, 255, 255))
    out.paste(a, (0, 0))
    out.paste(b, (0, a.height))
    return out


def source_image_for_slot(entry: str | Merge3, slot_index: int) -> Image.Image:
    if isinstance(entry, str):
        p = SRC_DIR / entry
        if not p.is_file():
            sys.exit(f"Missing source image: {p}")
        return load_rgb(p)
    top, bottom, merged_opt = entry
    if merged_opt:
        merged_path = SRC_DIR / merged_opt
        if merged_path.is_file():
            return load_rgb(merged_path)
    pa, pb = SRC_DIR / top, SRC_DIR / bottom
    if not pa.is_file() or not pb.is_file():
        need = f"{SRC_DIR / merged_opt}" if merged_opt else f"{pa} + {pb}"
        sys.exit(f"Slot {slot_index:02d}: need {need}")
    return merge_vertical(pa, pb)


def main() -> None:
    if not SRC_DIR.is_dir():
        sys.exit(f"Source directory not found: {SRC_DIR}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, entry in enumerate(SOURCES, start=1):
        im = source_image_for_slot(entry, i)
        out_path = OUT_DIR / f"{i:02d}.webp"
        im.save(out_path, "WEBP", quality=WEBP_QUALITY, method=6)
        print(f"Wrote {out_path.relative_to(ROOT)}")

    # Remove stray assets in section-1 (keep README)
    allowed = {f"{i:02d}.webp" for i in range(1, len(SOURCES) + 1)} | {"README.txt"}
    for f in OUT_DIR.iterdir():
        if f.is_file() and f.name not in allowed:
            f.unlink()
            print(f"Removed stray file {f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
