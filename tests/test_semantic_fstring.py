# tests/test_semantic_fstring.py  — f-strings now go through semantic analysis (#7)
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(_ROOT, "src"), os.path.join(_ROOT, "generated")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# register the phase folders (frontend/midend/backend/driver) on sys.path
import _pathsetup  # noqa: F401,E402

from ast_nodes import (
    ProgramNode, ExprStmtNode, AssignNode, FStringNode, IdentifierNode,
    IntLiteralNode, IndexAssignNode, TupleNode,
)
from semantic import analyse
from errors import SemanticError


def _fstr(*parts):
    return FStringNode(raw="", parts=list(parts))


def test_undefined_name_in_fstring_is_caught():
    # ف"{مجهول}"  with مجهول never defined -> SemanticError
    prog = ProgramNode(statements=[
        ExprStmtNode(expr=_fstr(("lit", "x="), ("expr", IdentifierNode("مجهول")))),
    ])
    try:
        analyse(prog)
        assert False, "undefined name inside f-string was not caught"
    except SemanticError:
        pass


def test_defined_name_in_fstring_passes():
    prog = ProgramNode(statements=[
        AssignNode(name="س", value=IntLiteralNode(1)),
        ExprStmtNode(expr=_fstr(("lit", "س="), ("expr", IdentifierNode("س")))),
    ])
    analyse(prog)   # must not raise


def test_fstring_without_interpolation_passes():
    prog = ProgramNode(statements=[
        ExprStmtNode(expr=_fstr(("lit", "مرحبا"))),
    ])
    analyse(prog)   # must not raise


def test_nd_index_assignment_groups_are_analysed():
    # ج[مجهول] = ٩  with ج defined but index name undefined -> SemanticError
    prog = ProgramNode(statements=[
        AssignNode(name="ج", value=IntLiteralNode(0)),
        IndexAssignNode(target="ج", indices=[IdentifierNode("مجهول")], value=IntLiteralNode(9)),
    ])
    try:
        analyse(prog)
        assert False, "undefined index name was not caught"
    except SemanticError:
        pass


def test_nd_index_assignment_tuple_group_ok():
    prog = ProgramNode(statements=[
        AssignNode(name="م", value=IntLiteralNode(0)),
        AssignNode(name="أ", value=IntLiteralNode(0)),
        AssignNode(name="ب", value=IntLiteralNode(0)),
        IndexAssignNode(target="م",
                        indices=[TupleNode(elements=[IdentifierNode("أ"), IdentifierNode("ب")])],
                        value=IntLiteralNode(9)),
    ])
    analyse(prog)   # must not raise


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("ok", fn.__name__)
    print("ALL %d PASSED" % len(fns))
