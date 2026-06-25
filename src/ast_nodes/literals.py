# ---------------------------------------------------------------------------
# src/ast_nodes/literals.py
# Literal / constant AST nodes (numbers, strings, lists, pi/e/infinity).
# ---------------------------------------------------------------------------
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple
from .base import _Positioned


@dataclass
class IntLiteralNode(_Positioned):
    value: int


@dataclass
class FloatLiteralNode(_Positioned):
    value: float


@dataclass
class StringLiteralNode(_Positioned):
    value: str


@dataclass
class FStringNode(_Positioned):
    raw: str                                 # inner text with {expr} placeholders intact
    parts: List[Any] = field(default_factory=list)  # CHANGED: [("lit", str) | ("expr", node)] built at parse time


@dataclass
class BoolLiteralNode(_Positioned):
    value: bool


@dataclass
class NullLiteralNode(_Positioned):
    pass


@dataclass
class ListNode(_Positioned):
    elements: List[Any]


@dataclass
class TupleNode(_Positioned):
    elements: List[Any]


@dataclass
class PiNode(_Positioned):
    pass


@dataclass
class EulerNode(_Positioned):
    pass


@dataclass
class InfinityNode(_Positioned):
    pass
