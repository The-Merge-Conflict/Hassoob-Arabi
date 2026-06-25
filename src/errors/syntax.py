# ---------------------------------------------------------------------------
# src/errors/syntax.py
# Lexing / parsing errors: LexError (tokeniser) and ParseError (grammar).
# ---------------------------------------------------------------------------
from __future__ import annotations
from .base import HassoobError


class LexError(HassoobError):
    """فشل في التحليل اللفظي / tokenisation failure."""
    kind = "خطأ لفظي"
    emoji = "🔤"


class ParseError(HassoobError):
    """مخالفة لقواعد اللغة / grammar violation."""
    kind = "خطأ نحوي"
    emoji = "📝"


