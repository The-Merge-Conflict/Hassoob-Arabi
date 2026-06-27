# tests/test_lang_utils.py  — pure AST-builder helpers (#3, #6, #7)
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(_ROOT, "src"), os.path.join(_ROOT, "generated")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# register the phase folders (frontend/midend/backend/driver) on sys.path
import _pathsetup  # noqa: F401,E402

from lang_utils import decode_escapes, split_fstring, chain_comparisons
from ast_nodes import BinOpNode, IdentifierNode, IntLiteralNode
from errors import ParseError

LB, RB = chr(123), chr(125)   # { and } (avoid literal braces in source noise)


# ---- #6 string escapes ----
def test_unicode_escape():
    assert decode_escapes(r"\u0041") == "A"
    assert decode_escapes(r"\u0623") == "\u0623"

def test_simple_escapes_bf0():
    assert decode_escapes(r"a\bb") == "a\bb"
    assert decode_escapes(r"a\fb") == "a\fb"
    assert decode_escapes(r"a\0b") == "a\0b"
    assert decode_escapes(r"\n\t\r") == "\n\t\r"

def test_backslash_and_quotes():
    assert decode_escapes(r"a\\b") == "a\\b"
    assert decode_escapes(r"\"q\"") == '"q"'

def test_unknown_escape_keeps_backslash():
    # \q is not a known escape -> backslash kept literally
    assert decode_escapes(r"a\qb") == "a\\qb"

def test_incomplete_unicode_is_literal():
    assert decode_escapes(r"\u12") == "\\u12"


# ---- #7 f-string splitting ----
def test_split_basic():
    assert split_fstring("x=" + LB + "a+b" + RB + "!") == [
        ("lit", "x="), ("expr", "a+b"), ("lit", "!")]

def test_split_multiple_exprs():
    t = LB + "a" + RB + "-" + LB + "b" + RB
    assert split_fstring(t) == [("expr", "a"), ("lit", "-"), ("expr", "b")]

def test_split_doubled_braces_literal():
    t = LB + LB + "x" + RB + RB
    assert split_fstring(t) == [("lit", LB + "x" + RB)]

def test_split_nested_braces():
    t = LB + "f(" + LB + "x" + RB + ")" + RB
    assert split_fstring(t) == [("expr", "f(" + LB + "x" + RB + ")")]

def test_split_unbalanced_raises():
    try:
        split_fstring("oops " + LB + "a+b")
        assert False, "expected ParseError"
    except ParseError:
        pass


# ---- #3 chained comparison desugaring ----
def test_single_comparison_unchanged():
    a, b = IdentifierNode("a"), IdentifierNode("b")
    node = chain_comparisons([a, b], ["<"])
    assert isinstance(node, BinOpNode) and node.op == "<"
    assert node.left is a and node.right is b

def test_chain_three_operands():
    a, b, c = IdentifierNode("a"), IdentifierNode("b"), IdentifierNode("c")
    node = chain_comparisons([a, b, c], ["<", "<"])
    # expect (a<b) و (b<c)
    assert isinstance(node, BinOpNode) and node.op == "و"
    assert node.left.op == "<" and node.left.left is a and node.left.right is b
    assert node.right.op == "<" and node.right.left is b and node.right.right is c

def test_chain_four_operands_left_assoc():
    ops = ["<", "<=", "<"]
    operands = [IntLiteralNode(i) for i in range(4)]
    node = chain_comparisons(operands, ops)
    # ((a<b) و (b<=c)) و (c<d)
    assert node.op == "و" and node.left.op == "و" and node.right.op == "<"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("ok", fn.__name__)
    print("ALL %d PASSED" % len(fns))
