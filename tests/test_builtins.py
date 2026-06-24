# ───────────────────────────────────────────────────────────────────────────
# tests/test_builtins.py
# Tests for built-in functions: ≥5 math, 3 list/string, 1 plotting (Agg backend).
# ───────────────────────────────────────────────────────────────────────
import os, sys, math

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(_ROOT, "src"), os.path.join(_ROOT, "generated")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Force a headless backend before builtins imports matplotlib.
import matplotlib
matplotlib.use("Agg")

from _builtins_loader import BUILTINS


def _b(name):
    return BUILTINS[name]


# ══ math / statistics built-ins (≥ 5) ══════════════════════════════
def test_mean():
    assert abs(_b("متوسط")([2, 4, 6]) - 4.0) < 1e-9


def test_median():
    assert abs(_b("وسيط")([1, 3, 2]) - 2.0) < 1e-9


def test_std():
    assert abs(_b("انحراف_معياري")([2, 2, 2, 2]) - 0.0) < 1e-9


def test_sum_and_prod():
    assert _b("مجموع")([1, 2, 3, 4]) == 10
    assert _b("ناتج")([1, 2, 3, 4]) == 24


def test_range_and_minmax():
    data = [5, 1, 9, 3]
    assert _b("مدى")(data) == 8
    assert _b("أصغر")(data) == 1
    assert _b("أكبر")(data) == 9


def test_determinant():
    # det([[1,2],[3,4]]) == -2
    assert abs(_b("محدد")([[1, 2], [3, 4]]) - (-2.0)) < 1e-9


def test_dot_product():
    assert int(_b("ضرب_نقطي")([1, 2, 3], [4, 5, 6])) == 32


# ══ list / string built-ins (≥ 3) ════════════════════════════════
def test_length():
    assert _b("طول")([1, 2, 3, 4]) == 4


def test_sort():
    assert _b("ترتيب")([3, 1, 2]) == [1, 2, 3]
    assert _b("ترتيب")([3, 1, 2], True) == [3, 2, 1]


def test_map_and_filter():
    assert _b("طبق")(lambda x: x * x, [1, 2, 3]) == [1, 4, 9]
    assert _b("صفي")(lambda x: x % 2 == 0, [1, 2, 3, 4]) == [2, 4]


def test_type_names():
    assert _b("نوع")(3) == "عدد"
    assert _b("نوع")("نص") == "نص"
    assert _b("نوع")(True) == "منطقي"
    assert _b("نوع")([1, 2]) == "قائمة"
    assert _b("نوع")(None) == "فارغ"


def test_join_split():
    assert _b("دمج")("-", ["أ", "ب", "ج"]) == "أ-ب-ج"
    assert _b("قسم")("أ,ب,ج", ",") == ["أ", "ب", "ج"]


# ══ plotting built-in (≥ 1, Agg backend) ══════════════════════════
def test_histogram_saves_file(tmp_path=None):
    import tempfile
    out = os.path.join(tempfile.gettempdir(), "hist_test.png")
    if os.path.exists(out):
        os.remove(out)
    result = _b("مدرج_تكراري")([1, 2, 2, 3, 3, 3, 4], 4, حفظ=out)
    assert result == out
    assert os.path.exists(out)
    os.remove(out)


def test_plot_function_saves_file():
    import tempfile
    out = os.path.join(tempfile.gettempdir(), "plot_test.png")
    if os.path.exists(out):
        os.remove(out)
    # plot a plain python callable so it works without sympy
    result = _b("ارسم")(lambda x: x * x, None, -2, 2, حفظ=out)
    assert result == out
    assert os.path.exists(out)
    os.remove(out)


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
