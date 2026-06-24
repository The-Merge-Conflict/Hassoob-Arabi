# ───────────────────────────────────────────────────────────────────────────
# tests/test_optimizer.py
# Tests for the optimizer using directly-constructed ASTs (no parser needed).
# ───────────────────────────────────────────────────────────────────────
import os, sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(_ROOT, "src"), os.path.join(_ROOT, "generated")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ast_nodes import (
    ProgramNode, BlockNode, BinOpNode, UnaryOpNode, IntLiteralNode,
    FloatLiteralNode, BoolLiteralNode, IdentifierNode, IfNode, WhileNode,
    ExprStmtNode, ReturnNode, AssignNode,
)
from optimizer import optimize


def _opt_expr(node):
    """Optimise a single expression by wrapping it in a tiny program."""
    prog = optimize(ProgramNode(statements=[ExprStmtNode(expr=node)]))
    return prog.statements[0].expr


# ── constant folding ───────────────────────────────────────────
def test_fold_addition():
    node = BinOpNode(IntLiteralNode(3), "+", IntLiteralNode(4))
    result = _opt_expr(node)
    assert isinstance(result, IntLiteralNode)
    assert result.value == 7


def test_fold_multiplication():
    node = BinOpNode(IntLiteralNode(6), "*", IntLiteralNode(7))
    result = _opt_expr(node)
    assert isinstance(result, IntLiteralNode)
    assert result.value == 42


def test_fold_equality_to_bool():
    node = BinOpNode(IntLiteralNode(3), "==", IntLiteralNode(3))
    result = _opt_expr(node)
    assert isinstance(result, BoolLiteralNode)
    assert result.value is True


def test_fold_float_division():
    node = BinOpNode(FloatLiteralNode(9.0), "/", FloatLiteralNode(2.0))
    result = _opt_expr(node)
    assert isinstance(result, FloatLiteralNode)
    assert result.value == 4.5


# ── algebraic identities ───────────────────────────────────────
def test_identity_add_zero():
    node = BinOpNode(IdentifierNode("س"), "+", IntLiteralNode(0))
    result = _opt_expr(node)
    assert isinstance(result, IdentifierNode)
    assert result.name == "س"


def test_identity_mul_one():
    node = BinOpNode(IdentifierNode("س"), "*", IntLiteralNode(1))
    result = _opt_expr(node)
    assert isinstance(result, IdentifierNode) and result.name == "س"


def test_identity_mul_zero():
    node = BinOpNode(IdentifierNode("س"), "*", IntLiteralNode(0))
    result = _opt_expr(node)
    assert isinstance(result, IntLiteralNode) and result.value == 0


def test_identity_pow_zero():
    node = BinOpNode(IdentifierNode("س"), "^", IntLiteralNode(0))
    result = _opt_expr(node)
    assert isinstance(result, IntLiteralNode) and result.value == 1


def test_double_negation():
    node = UnaryOpNode("-", UnaryOpNode("-", IdentifierNode("س")))
    result = _opt_expr(node)
    assert isinstance(result, IdentifierNode) and result.name == "س"


def test_double_not():
    node = UnaryOpNode("ليس", UnaryOpNode("ليس", IdentifierNode("ب")))
    result = _opt_expr(node)
    assert isinstance(result, IdentifierNode) and result.name == "ب"


# ── strength reduction ────────────────────────────────────────
def test_strength_reduction_square():
    node = BinOpNode(IdentifierNode("س"), "^", IntLiteralNode(2))
    result = _opt_expr(node)
    assert isinstance(result, BinOpNode)
    assert result.op == "*"
    assert isinstance(result.left, IdentifierNode) and result.left.name == "س"
    assert isinstance(result.right, IdentifierNode) and result.right.name == "س"


# ── short-circuit folding ─────────────────────────────────────
def test_or_true_short_circuit():
    node = BinOpNode(BoolLiteralNode(True), "أو", IdentifierNode("س"))
    result = _opt_expr(node)
    assert isinstance(result, BoolLiteralNode) and result.value is True


def test_and_false_short_circuit():
    node = BinOpNode(BoolLiteralNode(False), "و", IdentifierNode("س"))
    result = _opt_expr(node)
    assert isinstance(result, BoolLiteralNode) and result.value is False


# ── dead code elimination ─────────────────────────────────────
def test_dce_if_false_removed():
    if_node = IfNode(branches=[(BoolLiteralNode(False),
                                BlockNode([ExprStmtNode(IntLiteralNode(1))]))],
                     else_body=None)
    prog = optimize(ProgramNode(statements=[if_node]))
    assert prog.statements == []


def test_dce_if_true_keeps_body():
    if_node = IfNode(branches=[(BoolLiteralNode(True),
                                BlockNode([AssignNode("س", IntLiteralNode(5))]))],
                     else_body=BlockNode([AssignNode("س", IntLiteralNode(9))]))
    prog = optimize(ProgramNode(statements=[if_node]))
    assert len(prog.statements) == 1
    assert isinstance(prog.statements[0], AssignNode)
    assert prog.statements[0].value.value == 5


def test_dce_while_false_removed():
    w = WhileNode(condition=BoolLiteralNode(False),
                  body=BlockNode([ExprStmtNode(IntLiteralNode(1))]))
    prog = optimize(ProgramNode(statements=[w]))
    assert prog.statements == []


def test_dce_after_return():
    block = BlockNode([
        ReturnNode(IntLiteralNode(1)),
        ExprStmtNode(IntLiteralNode(999)),
    ])
    while_keep = WhileNode(condition=BoolLiteralNode(True), body=block)
    prog = optimize(ProgramNode(statements=[while_keep]))
    kept = prog.statements[0].body.statements
    assert len(kept) == 1
    assert isinstance(kept[0], ReturnNode)


def test_optimizer_is_pure():
    original = BinOpNode(IntLiteralNode(3), "+", IntLiteralNode(4))
    _opt_expr(original)
    # original node must be untouched
    assert isinstance(original, BinOpNode)
    assert original.left.value == 3 and original.right.value == 4


if __name__ == "__main__":
    import traceback
    funcs = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in funcs:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {fn.__name__}")
            traceback.print_exc()
    print(f"\n{len(funcs) - failed}/{len(funcs)} passed")
    sys.exit(1 if failed else 0)
