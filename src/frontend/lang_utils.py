# ───────────────────────────────────────────────────────────────────────────
# src/lang_utils.py
# Pure helpers used by the AST builder (no ANTLR / numpy dependency, so they are
# unit-testable in isolation):
#   * decode_escapes   — robust single-pass string-escape decoding
#   * split_fstring    — split an f-string body into literal/expression parts
#   * chain_comparisons— desugar a<b<c into (a<b) و (b<c)
# ───────────────────────────────────────────────────────────────────────────
from __future__ import annotations
# -- source-path bootstrap ---------------------------------------------------
# Hassoob's modules refer to one another by short name (e.g. ``from errors
# import ...``). Register the source root plus every compiler-phase folder so
# those names resolve no matter which module Python imports first.
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "src" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d and _d not in _sys.path:
    _sys.path.insert(0, _d)
import _pathsetup  # noqa: F401,E402  (registers all phase roots on sys.path)

import os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from errors import ParseError
from ast_nodes import BinOpNode

# Recognised single-character escapes (mirrors the lexer's ESCAPE_SEQ set).
_SIMPLE_ESCAPES = {
    "n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "0": "\0",
    "\\": "\\", '"': '"', "'": "'",
}
_HEX = set("0123456789abcdefABCDEF")


def decode_escapes(inner: str) -> str:
    """فكّ ترميز المحارف الهاربة فكًّا آمنًا في مرور واحد.

    Decodes \\n \\t \\r \\b \\f \\0 \\\\ \\" \\' and \\uXXXX in a single left-to-right
    pass (so overlapping replacements can't clobber each other). An unknown
    escape keeps its backslash literally instead of silently vanishing.
    """
    out = []
    i, n = 0, len(inner)
    while i < n:
        ch = inner[i]
        if ch == "\\" and i + 1 < n:
            nxt = inner[i + 1]
            if nxt == "u" and i + 6 <= n and all(c in _HEX for c in inner[i + 2:i + 6]):
                out.append(chr(int(inner[i + 2:i + 6], 16)))
                i += 6
                continue
            if nxt in _SIMPLE_ESCAPES:
                out.append(_SIMPLE_ESCAPES[nxt])
                i += 2
                continue
            out.append(ch)   # unknown escape → keep the backslash literally
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def split_fstring(template: str):
    """قسّم جسم السلسلة المنسَّقة إلى أجزاء ('lit', نص) و ('expr', مصدر).

    Handles doubled braces ( and ) as literal braces and balanced nested
    braces inside an interpolation. Raises ParseError on an unbalanced '{'.
    Returns an ordered list so the interpreter can rebuild the string exactly.
    """
    parts = []
    buf = []
    i, n = 0, len(template)
    while i < n:
        ch = template[i]
        if ch == "{":
            if i + 1 < n and template[i + 1] == "{":
                buf.append("{"); i += 2; continue
            if buf:
                parts.append(("lit", "".join(buf))); buf = []
            i += 1
            depth = 1
            expr = []
            while i < n and depth > 0:
                c = template[i]
                if c == "{":
                    depth += 1; expr.append(c)
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        i += 1; break
                    expr.append(c)
                else:
                    expr.append(c)
                i += 1
            if depth > 0:
                raise ParseError(
                    "سلسلة منسَّقة غير مكتملة: قوس '{' بلا '}' مقابل",
                    hint="أغلق كل '{' بـ '}'، أو اكتب '{{' و '}}' لطباعة قوس حرفي.",
                )
            parts.append(("expr", "".join(expr).strip()))
        elif ch == "}":
            if i + 1 < n and template[i + 1] == "}":
                buf.append("}"); i += 2; continue
            buf.append("}"); i += 1
        else:
            buf.append(ch); i += 1
    if buf:
        parts.append(("lit", "".join(buf)))
    return parts


def chain_comparisons(operands, ops):
    """حوّل المقارنة المتسلسلة a<b<c إلى (a<b) و (b<c).

    ``operands`` is a list of AST nodes (length == len(ops)+1); ``ops`` is the
    list of operator strings between them. A single comparison is returned
    unchanged. Note: the shared middle operand node is referenced twice, so a
    side-effecting middle term is evaluated twice at runtime (acceptable for
    pure comparisons; documented in the change report).
    """
    if len(ops) == 1:
        return BinOpNode(left=operands[0], op=ops[0], right=operands[1])
    comparisons = [
        BinOpNode(left=operands[i], op=ops[i], right=operands[i + 1])
        for i in range(len(ops))
    ]
    result = comparisons[0]
    for nxt in comparisons[1:]:
        result = BinOpNode(left=result, op="و", right=nxt)
    return result
