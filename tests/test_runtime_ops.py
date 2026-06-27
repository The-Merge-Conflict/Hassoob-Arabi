# tests/test_runtime_ops.py  — pure runtime helpers (#1, #2, #4, #8, #9)
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(_ROOT, "src"), os.path.join(_ROOT, "generated")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# register the phase folders (frontend/midend/backend/driver) on sys.path
import _pathsetup  # noqa: F401,E402

import numpy as np
from runtime_ops import check_power, index_key, nested_setitem, raise_binop_value_error
from errors import HassoobRuntimeError


# ---- #4 check_power ----
def test_power_negative_fractional_raises():
    for b, e in [(-1, 0.5), (-1, 1/2), (-8, 1/3)]:
        try:
            check_power(b, e); assert False, (b, e)
        except HassoobRuntimeError:
            pass

def test_power_negative_integer_ok():
    check_power(-1, 2); check_power(-1, 3); check_power(-2, 4.0)  # no raise

def test_power_positive_fractional_ok():
    check_power(4, 0.5); check_power(2, 0.5); check_power(0, 0.5)  # no raise

def test_power_ignores_bool():
    check_power(True, 0.5); check_power(-1, False)  # no raise


# ---- index_key ----
def test_index_key_scalar_and_tuple():
    assert index_key([1, 2], 1) == 1
    assert index_key(np.zeros((2, 2)), (1, 0)) == (1, 0)
    assert index_key("abc", 2) == 2


# ---- #8/#9 nested_setitem ----
def test_nested_setitem_ragged_chained():
    L = [[1, 2, 3], [4, 5]]
    nested_setitem(L, [1, 0], 9)
    assert L == [[1, 2, 3], [9, 5]]

def test_nested_setitem_numpy_tuple_index():
    A = np.zeros((2, 2, 2))
    nested_setitem(A, [(1, 0, 1)], 9)   # a[i, j, k] form
    assert A[1, 0, 1] == 9

def test_nested_setitem_numpy_chained_index():
    A = np.zeros((2, 2))
    nested_setitem(A, [1, 0], 7)        # a[i][j] form
    assert A[1, 0] == 7

def test_nested_setitem_deep_list():
    L = [[[0, 0], [0, 0]]]
    nested_setitem(L, [0, 1, 0], 5)
    assert L[0][1][0] == 5


# ---- #1/#2 dimension-error messages ----
def test_dimension_error_elementwise_arrays():
    a, b = np.zeros((3, 2)), np.zeros((2, 2))
    try:
        raise_binop_value_error("+", a, b, ValueError("boom"))
        assert False
    except HassoobRuntimeError as e:
        assert "٢" in str(e) and "٣" in str(e)   # arabic shape digits present

def test_dimension_error_matmul():
    a, b = np.zeros((2, 3)), np.zeros((2, 2))
    try:
        raise_binop_value_error("**", a, b, ValueError("boom"))
        assert False
    except HassoobRuntimeError:
        pass

def test_dimension_error_generic_op_always_raises():
    try:
        raise_binop_value_error("<", 1, 2, ValueError("x"))
        assert False
    except HassoobRuntimeError:
        pass


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("ok", fn.__name__)
    print("ALL %d PASSED" % len(fns))
