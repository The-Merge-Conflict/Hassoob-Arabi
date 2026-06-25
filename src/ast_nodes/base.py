# ---------------------------------------------------------------------------
# src/ast_nodes/base.py
# _Positioned: optional source line/col mix-in shared by every AST node.
# ---------------------------------------------------------------------------
from __future__ import annotations
from typing import Optional


class _Positioned:
    """موقع العقدة في الشيفرة (سطر/عمود) للرسائل الخطأ.

    Stored as *plain* attributes, NOT dataclass fields, so node equality and
    repr stay structural (two structurally-equal nodes remain equal even if
    they came from different source positions). ast_builder fills these in;
    raise sites read them via getattr(node, "line"/"col", None).
    """
    line: Optional[int] = None
    col: Optional[int] = None


