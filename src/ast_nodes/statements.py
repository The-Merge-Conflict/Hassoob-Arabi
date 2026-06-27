# ---------------------------------------------------------------------------
# src/ast_nodes/statements.py
# Statement / control-flow AST nodes.
# ---------------------------------------------------------------------------
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple
from .base import _Positioned


@dataclass
class ProgramNode(_Positioned):
    statements: List[Any]


@dataclass
class BlockNode(_Positioned):
    statements: List[Any]


@dataclass
class FunctionDefNode(_Positioned):
    name:   str
    params: List[str]
    body:   BlockNode


@dataclass
class SymbolDeclNode(_Positioned):
    names: List[str]


@dataclass
class AssignNode(_Positioned):
    name:  str
    value: Any


@dataclass
class AugAssignNode(_Positioned):
    name:  str
    op:    str    # '+=', '-=', '*=', '/=', '^=', '%=', '++='
    value: Any


@dataclass
class IndexAssignNode(_Positioned):
    target:  str
    indices: List[Any]   # one entry per bracket group; scalar node or TupleNode
    value:   Any


@dataclass
class IfNode(_Positioned):
    branches:  List[Tuple[Any, BlockNode]]   # [(condition, body), ...]
    else_body: Optional[BlockNode]


@dataclass
class WhileNode(_Positioned):
    condition: Any
    body:      BlockNode


@dataclass
class ForEachNode(_Positioned):
    var:      str
    iterable: Any
    body:     BlockNode


@dataclass
class ForRangeNode(_Positioned):
    var:   str
    start: Any
    end:   Any
    step:  Optional[Any]   # None → default step of 1
    body:  BlockNode


@dataclass
class ReturnNode(_Positioned):
    value: Optional[Any]


@dataclass
class BreakNode(_Positioned):
    pass


@dataclass
class ContinueNode(_Positioned):
    pass


@dataclass
class ExprStmtNode(_Positioned):
    expr: Any


@dataclass
class ErrorNode(_Positioned):
    """عقدة بديلة لجملة/تعبير تعذّر بناؤه نحويًا (وضع التعافي من الأخطاء).

    Placeholder for a statement (or expression) that could not be built because
    of a syntax error. It is inert: the optimiser and the semantic analyser
    treat it as a no-op, so a syntax error in one statement never blocks
    analysing or reporting errors in the rest of the program.
    """
    message: Optional[str] = None


