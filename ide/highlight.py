# ───────────────────────────────────────────────────────────────────────────
# ide/highlight.py
# Syntax-highlighting tokenizer for حاسوب عربي.  Pure-Python, NO Tkinter import,
# so it can be unit-tested headlessly and reused by any front-end.
#
# `Highlighter(builtin_names).spans(text)` returns a list of `Span` objects with
# character offsets (start, end) and a tag name.  A Tk front-end can map those
# offsets straight onto a Text widget with  "1.0 + <n> chars".
# ───────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Sequence

# Language keywords (mirrors the ANTLR grammar's reserved words).
KEYWORDS: tuple[str, ...] = (
    "إذا", "وإلا", "بينما", "لكل", "من", "إلى", "في", "بخطوة",
    "دالة", "إرجع", "اوقف", "استمر",
    "صح", "خطأ", "فارغ", "رمز",
    "ليس", "و", "أو",
    "باي", "هـ", "لانهاية",
)

# Named constants we also like to colour as constants rather than identifiers.
CONSTANTS: tuple[str, ...] = ("صح", "خطأ", "فارغ", "باي", "هـ", "لانهاية")

TAGS: tuple[str, ...] = (
    "comment", "string", "number", "keyword", "constant", "builtin", "operator",
)

# A "word" character set that includes Arabic letters, the tatweel, Western and
# Arabic-Indic digits and the underscore — used to build word-boundary guards
# that work for Arabic identifiers (Python's \b is unreliable across scripts).
_WORD = r"[\w\u0640\u0660-\u0669]"


@dataclass(frozen=True)
class Span:
    tag: str
    start: int
    end: int


def _alt(words: Sequence[str]) -> str:
    # Longest-first so e.g. "وإلا" wins over "و".
    ordered = sorted(set(words), key=len, reverse=True)
    return "|".join(re.escape(w) for w in ordered)


class Highlighter:
    """Builds a master regular expression and tokenises source text."""

    def __init__(self, builtin_names: Sequence[str] = ()):  # noqa: D401
        self.builtin_names = tuple(dict.fromkeys(builtin_names))
        self._regex = self._build_regex(self.builtin_names)

    # ── public API ──────────────────────────────────────────────────
    def spans(self, text: str) -> List[Span]:
        """Return non-overlapping highlight spans in document order."""
        out: List[Span] = []
        for m in self._regex.finditer(text):
            tag = m.lastgroup
            if tag is None:
                continue
            out.append(Span(tag, m.start(), m.end()))
        return out

    # ── internals ───────────────────────────────────────────────────
    def _build_regex(self, builtins: Sequence[str]) -> "re.Pattern[str]":
        kw = [w for w in KEYWORDS if w not in CONSTANTS]
        digits = r"0-9\u0660-\u0669"
        parts: list[tuple[str, str]] = [
            # Comments: line comments (# or ملاحظة) and /* block */ comments.
            ("comment", r"\#[^\n]*|ملاحظة[^\n]*|/\*.*?\*/"),
            # Strings: optional f/ف prefix, double or single quoted, escapes.
            ("string",
             r"(?:[fF\u0641])?\"(?:\\.|[^\"\\\n])*\""
             r"|(?:[fF\u0641])?'(?:\\.|[^'\\\n])*'"),
            # Numbers: Western or Arabic-Indic digits, optional fraction.
            ("number", rf"[{digits}][{digits}_]*(?:\.[{digits}]*)?"),
            # Constants (true/false/null/pi/e/inf).
            ("constant", rf"(?<!{_WORD})(?:{_alt(CONSTANTS)})(?!{_WORD})"),
            # Keywords.
            ("keyword", rf"(?<!{_WORD})(?:{_alt(kw)})(?!{_WORD})"),
        ]
        if builtins:
            parts.append(
                ("builtin", rf"(?<!{_WORD})(?:{_alt(builtins)})(?!{_WORD})")
            )
        # Operators last.
        parts.append(
            ("operator",
             r"\*\*|\+\+|--|==|!=|<=|>=|&&|\|\||=>|[-+*/%^=<>!÷≤≥≠]")
        )
        pattern = "|".join(f"(?P<{name}>{pat})" for name, pat in parts)
        return re.compile(pattern, re.DOTALL)
