# -*- coding: utf-8 -*-
"""Reorder PtbWordIndexEntry blocks in rulers/index.md by Thai sort on term without honorific prefixes."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ptb_word_index_sort_key import set_thai_locale, sort_key_tuple

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs/10-part-5-academic-notes-and-index/word-index/persons/rulers/index.md"

H11 = "### ๑.๑ ก่อนพุทธกาล จนถึงในสมัยพุทธกาล {.ptb-h-block}\n"
H12 = "### ๑.๒ หลังพุทธกาล {.ptb-h-block}\n"
H2 = "## ผู้ครองนคร มหาอำมาตย์ และผู้นำชุมชน {.ptb-h-block}\n"


def sort_blocks_in_body(body: str) -> str:
    blocks = re.findall(r"<PtbWordIndexEntry[\s\S]*?</PtbWordIndexEntry>", body)

    def key(block: str) -> tuple:
        tm = re.search(r'term="([^"]*)"', block)
        if not tm:
            raise ValueError("missing term")
        return sort_key_tuple(tm.group(1))

    sorted_blocks = sorted(blocks, key=key)
    return "\n".join(sorted_blocks) + ("\n" if sorted_blocks else "")


def replace_between(text: str, start: str, end: str) -> str:
    i0 = text.index(start) + len(start)
    i1 = text.index(end, i0)
    return text[:i0] + sort_blocks_in_body(text[i0:i1]) + text[i1:]


def main() -> None:
    set_thai_locale()
    text = PATH.read_text(encoding="utf-8")
    text = replace_between(text, H11, H12)
    text = replace_between(text, H12, H2)
    # กลุ่ม ๒ … EOF
    i0 = text.index(H2) + len(H2)
    text = text[:i0] + sort_blocks_in_body(text[i0:])
    PATH.write_text(text, encoding="utf-8")
    print("OK", PATH)


if __name__ == "__main__":
    main()
