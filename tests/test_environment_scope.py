# tests/test_environment_scope.py  — Mathematica-like plain = scope (#5)
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(_ROOT, "src"), os.path.join(_ROOT, "generated")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from environment import Environment


def test_assign_or_define_mutates_outer():
    g = Environment()
    g.set("س", 0)
    local = g.child()
    local.assign_or_define("س", 5)   # س exists up the chain -> mutate global
    assert g.vars["س"] == 5
    assert "س" not in local.vars       # no local shadow created


def test_assign_or_define_defines_new_in_current_frame():
    g = Environment()
    local = g.child()
    local.assign_or_define("جديد", 7)  # name bound nowhere -> define locally
    assert local.vars["جديد"] == 7
    assert "جديد" not in g.vars


def test_assign_or_define_top_level_creates_global():
    g = Environment()
    g.assign_or_define("س", 1)
    assert g.vars["س"] == 1


def test_assign_or_define_mutates_local_when_local():
    g = Environment()
    g.set("س", 0)
    local = g.child()
    local.set("س", 9)              # س is a genuine local
    local.assign_or_define("س", 3)  # should mutate the local, not the global
    assert local.vars["س"] == 3
    assert g.vars["س"] == 0


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("ok", fn.__name__)
    print("ALL %d PASSED" % len(fns))
