#!/usr/bin/env python3
"""
List docs/**/*.md grouped into batches for AI-led Thai spacing / wrap review.

Excludes .vitepress. Default: human-readable list; use --json for machine output.
Does not modify files.

Batch modes:
  coarse  — one batch per top-level folder under docs/ (e.g. 09-part-4-...)
  folder  — one batch per parent directory of each file (recommended default)
  volume  — each vol-*.md is its own batch; other files grouped by parent dir
  file    — one batch per file (smallest units)
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def iter_md_under_docs(docs: Path) -> list[Path]:
    out: list[Path] = []
    for p in sorted(docs.rglob("*.md")):
        if ".vitepress" in p.parts:
            continue
        out.append(p)
    return out


def batch_key(rel: Path, mode: str) -> str:
    if mode == "file":
        return rel.as_posix()
    if mode == "coarse":
        return rel.parts[0] if rel.parts else rel.as_posix()
    if mode == "folder":
        parent = rel.parent
        if parent == Path("."):
            return "__docs_root__"
        return parent.as_posix()
    if mode == "volume":
        if rel.name.startswith("vol-") and rel.suffix == ".md":
            return rel.as_posix()
        parent = rel.parent
        if parent == Path("."):
            return "__docs_root__"
        return parent.as_posix()
    raise ValueError(f"unknown mode: {mode}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    repo = Path(__file__).resolve().parent.parent
    ap.add_argument(
        "--docs-root",
        type=Path,
        default=repo / "docs",
        help="Docs root (default: <repo>/docs)",
    )
    ap.add_argument(
        "--mode",
        choices=("coarse", "folder", "volume", "file"),
        default="folder",
        help="How to group files into batches (default: folder)",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON { batch_id: [rel paths, ...] }",
    )
    args = ap.parse_args()
    docs = args.docs_root.resolve()
    if not docs.is_dir():
        print(f"Not a directory: {docs}", file=sys.stderr)
        return 1

    rel_paths = [p.relative_to(docs).as_posix() for p in iter_md_under_docs(docs)]
    batches: dict[str, list[str]] = defaultdict(list)
    for rp in rel_paths:
        key = batch_key(Path(rp), args.mode)
        batches[key].append(rp)
    for k in batches:
        batches[k].sort()

    ordered = dict(sorted(batches.items()))
    if args.json:
        print(json.dumps(ordered, ensure_ascii=False, indent=2))
        return 0

    total_files = len(rel_paths)
    print(f"docs root: {docs}")
    print(f"mode: {args.mode}  |  batches: {len(ordered)}  |  .md files: {total_files}\n")
    for bid, files in ordered.items():
        print(f"## {bid}  ({len(files)} files)")
        for f in files:
            print(f"  {f}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
