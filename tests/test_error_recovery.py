# ---------------------------------------------------------------------------
# Tests for cross-phase recovery (ErrorNode) + cascade suppression.
# These build AST nodes directly, so they run WITHOUT the antlr4 runtime.
# Run: python3 tests/test_error_recovery.py
# ---------------------------------------------------------------------------
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(_ROOT, "src"), os.path.join(_ROOT, "generated")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ast_nodes import (
    ProgramNode, AssignNode, ExprStmtNode, ErrorNode,
    BinOpNode, IdentifierNode, IntLiteralNode,
)
from semantic import analyse, collect_semantic_errors, SemanticAnalyser
from errors import SemanticError, MultiError
from optimizer import optimize


def _at(node, line, col):
    node.line, node.col = line, col
    return node


def _undef_use(name, line):
    # أ = <name> + 1   (assignment to a fresh var, RHS uses an undefined name)
    return _at(AssignNode(name="أ",
                          value=BinOpNode(_at(IdentifierNode(name), line, 5),
                                          "+", IntLiteralNode(1))),
               line, 1)


def test_cascade_suppression():
    # 'د' is undefined and used on 3 separate lines -> reported exactly ONCE.
    prog = ProgramNode(statements=[
        _undef_use("د", 1),
        _undef_use("د", 2),
        _undef_use("د", 3),
    ])
    errs = collect_semantic_errors(prog)
    assert len(errs) == 1, "expected 1 error, got %d" % len(errs)
    assert isinstance(errs[0], SemanticError)
    assert "د" in errs[0].message
    print("PASS cascade suppression: 1 error for 3 uses")


def test_distinct_undefined_names_each_reported():
    prog = ProgramNode(statements=[_undef_use("د", 1), _undef_use("هـ", 2)])
    errs = collect_semantic_errors(prog)
    assert len(errs) == 2, "expected 2 distinct errors, got %d" % len(errs)
    print("PASS distinct undefined names: 2 errors")


def test_errornode_is_noop_in_semantics():
    # An ErrorNode (syntax-error placeholder) must not crash analysis and must
    # not hide the real semantic error in a sibling statement.
    prog = ProgramNode(statements=[
        _at(ErrorNode(message="<syntax>"), 1, 1),
        _undef_use("د", 2),
        _at(ErrorNode(), 3, 1),
    ])
    errs = collect_semantic_errors(prog)
    assert len(errs) == 1 and "د" in errs[0].message
    print("PASS ErrorNode is inert in semantic phase")


def test_errornode_is_noop_in_optimizer():
    prog = ProgramNode(statements=[_at(ErrorNode(), 1, 1),
                                   ExprStmtNode(IntLiteralNode(1))])
    out = optimize(prog)
    assert any(isinstance(s, ErrorNode) for s in out.statements), \
        "optimizer dropped/changed ErrorNode"
    print("PASS ErrorNode survives the optimizer untouched")


def test_analyse_still_raises():
    # The unchanged happy path: analyse() still raises on semantic errors.
    prog = ProgramNode(statements=[_undef_use("د", 1)])
    try:
        analyse(prog)
    except SemanticError as e:
        assert "د" in e.message
        print("PASS analyse() still raises a single SemanticError")
        return
    raise AssertionError("analyse() did not raise")


def test_analyse_multierror_still_raises():
    prog = ProgramNode(statements=[_undef_use("د", 1), _undef_use("هـ", 2)])
    try:
        analyse(prog)
    except MultiError as e:
        assert len(e.errors) == 2
        print("PASS analyse() still raises MultiError for >1 errors")
        return
    raise AssertionError("analyse() did not raise MultiError")


def test_clean_program_no_errors():
    prog = ProgramNode(statements=[
        _at(AssignNode(name="أ", value=IntLiteralNode(3)), 1, 1),
        ExprStmtNode(_at(IdentifierNode("أ"), 2, 1)),
    ])
    assert collect_semantic_errors(prog) == []
    print("PASS clean program -> 0 errors")


if __name__ == "__main__":
    test_cascade_suppression()
    test_distinct_undefined_names_each_reported()
    test_errornode_is_noop_in_semantics()
    test_errornode_is_noop_in_optimizer()
    test_analyse_still_raises()
    test_analyse_multierror_still_raises()
    test_clean_program_no_errors()
    print("\nALL RECOVERY TESTS PASSED")
