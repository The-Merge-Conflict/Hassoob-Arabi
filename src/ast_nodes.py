from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple


class _Positioned:
    """موقع العقدة في الشيفرة (سطر/عمود) للرسائل الخطأ.

    Stored as *plain* attributes, NOT dataclass fields, so node equality and
    repr stay structural (two structurally-equal nodes remain equal even if
    they came from different source positions). ast_builder fills these in;
    raise sites read them via getattr(node, "line"/"col", None).
    """
    line: Optional[int] = None
    col: Optional[int] = None


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
    indices: List[Any]   # CHANGED: one entry per bracket group; scalar node or TupleNode
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
