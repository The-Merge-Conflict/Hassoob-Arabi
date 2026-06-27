# ---------------------------------------------------------------------------
# src/ast_nodes/expressions.py
# Expression AST nodes (operators, calls, indexing, lambdas, identifiers).
# ---------------------------------------------------------------------------
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple
from .base import _Positioned


@dataclass
class BinOpNode(_Positioned):
    left:  Any
    op:    str
    right: Any


@dataclass
class UnaryOpNode(_Positioned):
    op:      str
    operand: Any


@dataclass
class CallNode(_Positioned):
    callee: Any
    args:   List[Any]
    kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass
class IndexNode(_Positioned):
    target: Any
    index:  Any


@dataclass
class LambdaNode(_Positioned):
    params: List[str]
    body:   Any


@dataclass
class IdentifierNode(_Positioned):
    name: str


