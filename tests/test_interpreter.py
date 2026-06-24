# ───────────────────────────────────────────────────────────────────────────
# tests/test_interpreter.py
# Interpreter tests using directly-constructed ASTs (no parser dependency).
# ───────────────────────────────────────────────────────────────────────
import os, sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(_ROOT, "src"), os.path.join(_ROOT, "generated")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ast_nodes import (
    ProgramNode, BlockNode, FunctionDefNode, AssignNode, AugAssignNode,
    ReturnNode, IfNode, WhileNode, ForRangeNode, ForEachNode, BreakNode,
    ExprStmtNode, BinOpNode, CallNode, IdentifierNode, IntLiteralNode,
    LambdaNode, ListNode, IndexNode,
)
from interpreter import Interpreter, Function
from environment import Environment
from errors import SemanticError


def _run(statements):
    interp = Interpreter()
    interp.run(ProgramNode(statements=statements), interp.global_env)
    return interp


def _eval(node):
    interp = Interpreter()
    return interp.evaluate(node, interp.global_env)


# ── arithmetic ───────────────────────────────────────────────
def test_addition():
    assert _eval(BinOpNode(IntLiteralNode(3), "+", IntLiteralNode(4))) == 7


def test_power():
    assert _eval(BinOpNode(IntLiteralNode(2), "^", IntLiteralNode(10))) == 1024


def test_floor_division():
    assert _eval(BinOpNode(IntLiteralNode(7), "÷", IntLiteralNode(2))) == 3


def test_string_concat():
    from ast_nodes import StringLiteralNode
    node = BinOpNode(StringLiteralNode("أب"), "++", StringLiteralNode("جد"))
    assert _eval(node) == "أبجد"


def test_division_by_zero():
    from errors import HassoobRuntimeError
    interp = Interpreter()
    try:
        interp.evaluate(BinOpNode(IntLiteralNode(1), "/", IntLiteralNode(0)),
                        interp.global_env)
        assert False, "expected HassoobRuntimeError"
    except HassoobRuntimeError:
        pass


# ── variables & scoping ────────────────────────────────────────
def test_assignment_and_lookup():
    interp = _run([AssignNode("س", IntLiteralNode(42))])
    assert interp.global_env.get("س") == 42


def test_aug_assign():
    interp = _run([
        AssignNode("س", IntLiteralNode(10)),
        AugAssignNode("س", "+=", IntLiteralNode(5)),
    ])
    assert interp.global_env.get("س") == 15


def test_undeclared_raises():
    env = Environment()
    try:
        env.get("غير_موجود")
        assert False
    except SemanticError:
        pass


# ── functions, closures, recursion ─────────────────────────────────
def test_function_call():
    # دالة جمع(أ, ب) { إرجع أ + ب }
    fdef = FunctionDefNode(
        name="جمع", params=["أ", "ب"],
        body=BlockNode([ReturnNode(BinOpNode(IdentifierNode("أ"), "+", IdentifierNode("ب")))]),
    )
    call = ExprStmtNode(CallNode(IdentifierNode("جمع"), [IntLiteralNode(3), IntLiteralNode(9)]))
    interp = Interpreter()
    interp.run(ProgramNode([fdef]), interp.global_env)
    assert interp.execute(call, interp.global_env) == 12


def test_recursion_factorial():
    # دالة عاملي(ن) { إذا (ن <= 1) { إرجع 1 } إرجع ن * عاملي(ن - 1) }
    fdef = FunctionDefNode(
        name="عاملي", params=["ن"],
        body=BlockNode([
            IfNode(branches=[(BinOpNode(IdentifierNode("ن"), "<=", IntLiteralNode(1)),
                              BlockNode([ReturnNode(IntLiteralNode(1))]))], else_body=None),
            ReturnNode(BinOpNode(IdentifierNode("ن"), "*",
                                 CallNode(IdentifierNode("عاملي"),
                                          [BinOpNode(IdentifierNode("ن"), "-", IntLiteralNode(1))]))),
        ]),
    )
    call = ExprStmtNode(CallNode(IdentifierNode("عاملي"), [IntLiteralNode(5)]))
    interp = Interpreter()
    interp.run(ProgramNode([fdef]), interp.global_env)
    assert interp.execute(call, interp.global_env) == 120


def test_closure_counter():
    # دالة صانع(ب) { إرجع س => س + ب }   ؛ إضافة = صانع(١٠) ؛ إضافة(٥) == ١٥
    fdef = FunctionDefNode(
        name="صانع", params=["ب"],
        body=BlockNode([ReturnNode(LambdaNode(params=["س"],
                       body=BinOpNode(IdentifierNode("س"), "+", IdentifierNode("ب"))))]),
    )
    interp = Interpreter()
    interp.run(ProgramNode([
        fdef,
        AssignNode("إضافة", CallNode(IdentifierNode("صانع"), [IntLiteralNode(10)])),
    ]), interp.global_env)
    result = interp.execute(
        ExprStmtNode(CallNode(IdentifierNode("إضافة"), [IntLiteralNode(5)])),
        interp.global_env)
    assert result == 15


# ── loops ──────────────────────────────────────────────────
def test_for_range_sum():
    # مج = 0 ؛ لكل ع من 1 إلى 5 { مج += ع }   → 15
    interp = _run([
        AssignNode("مج", IntLiteralNode(0)),
        ForRangeNode(var="ع", start=IntLiteralNode(1), end=IntLiteralNode(5), step=None,
                     body=BlockNode([AugAssignNode("مج", "+=", IdentifierNode("ع"))])),
    ])
    assert interp.global_env.get("مج") == 15


def test_while_with_break():
    interp = _run([
        AssignNode("ع", IntLiteralNode(0)),
        WhileNode(condition=__import__("ast_nodes").BoolLiteralNode(True),
                  body=BlockNode([
                      AugAssignNode("ع", "+=", IntLiteralNode(1)),
                      IfNode(branches=[(BinOpNode(IdentifierNode("ع"), ">=", IntLiteralNode(3)),
                                        BlockNode([BreakNode()]))], else_body=None),
                  ])),
    ])
    assert interp.global_env.get("ع") == 3


def test_foreach_list():
    interp = _run([
        AssignNode("مج", IntLiteralNode(0)),
        ForEachNode(var="ع", iterable=ListNode([IntLiteralNode(2), IntLiteralNode(3), IntLiteralNode(5)]),
                    body=BlockNode([AugAssignNode("مج", "+=", IdentifierNode("ع"))])),
    ])
    assert interp.global_env.get("مج") == 10


def test_list_indexing():
    interp = Interpreter()
    interp.run(ProgramNode([AssignNode("ق", ListNode([IntLiteralNode(10), IntLiteralNode(20), IntLiteralNode(30)]))]),
               interp.global_env)
    val = interp.evaluate(IndexNode(IdentifierNode("ق"), IntLiteralNode(1)), interp.global_env)
    assert val == 20


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
