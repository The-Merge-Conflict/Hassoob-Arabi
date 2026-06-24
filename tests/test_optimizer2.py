# tests/test_optimizer2.py
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(_ROOT, "src"), os.path.join(_ROOT, "generated")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ast_nodes import (
    ProgramNode, ExprStmtNode, BinOpNode, IntLiteralNode, FloatLiteralNode,
    IdentifierNode, CallNode, BoolLiteralNode,
)
from optimizer import optimize
from lang_utils import chain_comparisons


def _opt(node):
    return optimize(ProgramNode(statements=[ExprStmtNode(expr=node)])).statements[0].expr


# ---- #4: x * 0 must NOT drop a side-effecting call ----
def test_mul_zero_with_call_not_folded():
    call = CallNode(callee=IdentifierNode("اطبع"), args=[], kwargs={})
    node = BinOpNode(left=call, op="*", right=IntLiteralNode(0))
    result = _opt(node)
    assert isinstance(result, BinOpNode), "call*0 was incorrectly folded away"
    assert isinstance(result.left, CallNode)

def test_mul_zero_with_identifier_still_folds():
    node = BinOpNode(left=IdentifierNode("x"), op="*", right=IntLiteralNode(0))
    result = _opt(node)
    assert isinstance(result, IntLiteralNode) and result.value == 0


# ---- #4: 0 / x must NOT be folded to 0 (x may be 0 at runtime) ----
def test_zero_div_identifier_not_folded():
    node = BinOpNode(left=IntLiteralNode(0), op="/", right=IdentifierNode("م"))
    result = _opt(node)
    assert isinstance(result, BinOpNode) and result.op == "/"


# ---- #4: (-1) ^ 0.5 must not crash the optimizer; left for runtime ----
def test_negative_fractional_power_not_folded():
    node = BinOpNode(left=IntLiteralNode(-1), op="^", right=FloatLiteralNode(0.5))
    result = _opt(node)               # must not raise
    assert isinstance(result, BinOpNode) and result.op == "^"

def test_negative_integer_power_still_folds_or_reduces():
    node = BinOpNode(left=IntLiteralNode(-1), op="^", right=IntLiteralNode(2))
    result = _opt(node)               # must not raise
    # may be folded to 1 or strength-reduced to (-1)*(-1); just must not crash
    assert result is not None


# ---- #3: chained comparison desugars and folds to a constant ----
def test_chained_comparison_folds_false():
    # (3 < 2) و (2 < 1)  ->  False
    operands = [IntLiteralNode(3), IntLiteralNode(2), IntLiteralNode(1)]
    desugared = chain_comparisons(operands, ["<", "<"])
    result = _opt(desugared)
    assert isinstance(result, BoolLiteralNode) and result.value is False

def test_chained_comparison_folds_true():
    operands = [IntLiteralNode(1), IntLiteralNode(2), IntLiteralNode(3)]
    desugared = chain_comparisons(operands, ["<", "<"])
    result = _opt(desugared)
    assert isinstance(result, BoolLiteralNode) and result.value is True


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("ok", fn.__name__)
    print("ALL %d PASSED" % len(fns))
