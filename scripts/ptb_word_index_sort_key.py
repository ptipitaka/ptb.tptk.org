"""
Sort key for word-index person terms: Thai collation on the stem after optional
honorific prefixes. Does not change `term` text — only for ordering lists.

See docs: .cursor/rules/ptb-word-index.mdc (การเรียงลำดับรายการไม่ใช้คำนำหน้า)
"""

from __future__ import annotations

import locale

# Longest first so e.g. พระเจ้า is matched before พระ (if พระ is ever added)
_DEFAULT_PREFIXES: tuple[str, ...] = (
    "พระเจ้า",
    "พระนาง",
    "พระบาท",
    "สมเด็จพระ",
    "สมเด็จ",
)


def term_for_sort(term: str, prefixes: tuple[str, ...] | None = None) -> str:
    """Return string used for dictionary order (prefixes stripped from the start only)."""
    pfx = prefixes if prefixes is not None else _DEFAULT_PREFIXES
    t = term.strip()
    ordered = sorted(pfx, key=len, reverse=True)
    for p in ordered:
        if t.startswith(p):
            rest = t[len(p) :].strip()
            return rest if rest else t
    return t


def sort_key_tuple(term: str, prefixes: tuple[str, ...] | None = None) -> tuple[str, str]:
    """(collated_key, term) for stable sort."""
    stem = term_for_sort(term, prefixes=prefixes)
    try:
        return (locale.strxfrm(stem), term)
    except Exception:
        return (stem, term)


def set_thai_locale() -> None:
    for name in ("th_TH.UTF-8", "Thai", "th_TH", "C"):
        try:
            locale.setlocale(locale.LC_COLLATE, name)
            return
        except locale.Error:
            continue
