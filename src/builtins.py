# ───────────────────────────────────────────────────────────────────────────
# src/builtins.py
# The built-in function registry for حاسوب عربي.
#
# Dependency strategy (so the module imports even on a minimal machine):
#   * numpy / matplotlib are imported at module load (always required).
#   * sympy / scipy are imported lazily inside the functions that need them,
#     so list/stats/plotting still work when only numpy+matplotlib exist.
# ───────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import os, sys, math, random

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from errors import HassoobRuntimeError, to_arabic_digits

import numpy as np

# Matplotlib backend selection:
#   * Under pytest, or when HASSOOB_HEADLESS is set, force the non-interactive
#     Agg backend so plotting never blocks or crashes in CI / sandboxes.
#   * Otherwise leave matplotlib's automatic backend selection alone so that the
#     IDE and the CLI can pop up real plot windows on any OS (Windows / macOS /
#     Linux), where matplotlib auto-detects an interactive backend and falls
#     back to Agg only when no display is available.
import matplotlib
if "pytest" in sys.modules or os.environ.get("HASSOOB_HEADLESS"):
    try:
        matplotlib.use("Agg")
    except Exception:
        pass
import matplotlib.pyplot as plt


# ══ lazy optional dependencies ═══════════════════════════════════════
def _sympy():
    try:
        import sympy
        return sympy
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise HassoobRuntimeError(
            "هذه العملية الرمزية تحتاج إلى المكتبة sympy (ثبّتها عبر requirements.txt)"
        ) from exc


# ══ formatting helpers ═════════════════════════════════════════════
def format_value(v) -> str:
    """التمثيل النصي الودود المستخدم في اطبع والـ REPL.

    Human-friendly string form used by اطبع and the REPL. Always normalises
    digits to Arabic-Indic numerals (٠-٩) so output is consistently Arabic,
    whether the source used Arabic or Western digits.
    """
    return to_arabic_digits(_format_raw(v))


def _format_raw(v) -> str:
    """Internal string form (before Arabic-digit normalisation)."""
    if v is None:
        return "فارغ"
    if isinstance(v, bool):
        return "صح" if v else "خطأ"
    if isinstance(v, np.ndarray):
        return np.array2string(v, separator="، ")
    if isinstance(v, (list, tuple)):
        opener, closer = ("[", "]") if isinstance(v, list) else ("(", ")")
        return opener + "، ".join(_format_raw(x) for x in v) + closer
    return str(v)


def _as_number_list(x):
    """Coerce a list / ndarray / tuple into something numpy can reduce over."""
    if isinstance(x, np.ndarray):
        return x
    if isinstance(x, (list, tuple)):
        return list(x)
    raise HassoobRuntimeError("كان متوقعًا قائمة أو مصفوفة")


def _to_int_index(i):
    try:
        return int(i)
    except (TypeError, ValueError):
        raise HassoobRuntimeError("دليل غير صالح (يجب أن يكون عددًا صحيحًا)")


def _setup_rtl_font():
    """Best-effort RTL-friendly font configuration for Arabic plot labels."""
    try:
        matplotlib.rcParams["axes.unicode_minus"] = False
        for fam in ("Amiri", "Noto Naskh Arabic", "DejaVu Sans", "Arial"):
            matplotlib.rcParams["font.family"] = fam
            break
    except Exception:
        pass


def _finish_plot(حفظ):
    """Either save the current figure or show it, then clean up."""
    if حفظ:
        plt.savefig(حفظ, bbox_inches="tight")
        plt.close()
        return حفظ
    if matplotlib.get_backend().lower() == "agg":
        # Non-interactive backend: nothing to show, so just close cleanly.
        plt.close()
        return None
    if os.environ.get("HASSOOB_IDE"):
        # Inside the IDE: pop up the native Matplotlib window (with its save /
        # zoom / pan navigation toolbar) WITHOUT blocking the IDE event loop,
        # which already keeps the figure interactive.
        plt.show(block=False)
        plt.pause(0.001)
    else:
        # CLI / script: block until the user closes the window.
        plt.show()
    return None


def _callable_of(f, var):
    """Return a 1-arg numeric python callable from a sympy expr or a callable."""
    if callable(f):
        return f
    sympy = _sympy()
    if isinstance(f, sympy.Basic):
        return sympy.lambdify(var, f, "numpy")
    raise HassoobRuntimeError("كان متوقعًا دالة أو تعبيرًا رمزيًا")


# ══ output ══════════════════════════════════════════════════════
def _b_print(*args):
    """اطبع: print all arguments space-separated; returns None."""
    print(" ".join(format_value(a) for a in args))
    return None


# ══ symbolic math (SymPy) ═══════════════════════════════════════
def _b_simplify(expr):
    return _sympy().simplify(expr)


def _b_expand(expr):
    return _sympy().expand(expr)


def _b_factor(expr):
    return _sympy().factor(expr)


def _b_subs(expr, var, val):
    sympy = _sympy()
    if not isinstance(expr, sympy.Basic):
        expr = sympy.sympify(expr)
    return expr.subs(var, val)


def _b_diff(expr, var, order=1):
    return _sympy().diff(expr, var, int(order))


def _b_integrate(expr, var, a=None, b=None):
    sympy = _sympy()
    if a is None and b is None:
        return sympy.integrate(expr, var)
    return sympy.integrate(expr, (var, a, b))


def _b_limit(expr, var, point):
    return _sympy().limit(expr, var, point)


def _b_series(expr, var, point, n):
    return _sympy().series(expr, var, point, int(n))


def _b_solve(expr_or_eq, var):
    return _sympy().solve(expr_or_eq, var)


def _b_solve_system(eqs_list, vars_list):
    return _sympy().solve(list(eqs_list), list(vars_list))


def _b_dsolve(ode, func, var=None):
    return _sympy().dsolve(ode, func)


# ══ numerical (NumPy / SciPy) ══════════════════════════════════
def _b_numeric_root(f, var, x0):
    """جذر_عددي: numeric root via scipy.newton, with a manual Newton fallback."""
    func = _callable_of(f, var)
    try:
        from scipy import optimize
        return float(optimize.newton(func, float(x0)))
    except ImportError:
        # Manual Newton's method (finite-difference derivative).
        x = float(x0)
        for _ in range(200):
            fx = func(x)
            h = 1e-7 * (abs(x) + 1.0)
            dfx = (func(x + h) - func(x - h)) / (2 * h)
            if dfx == 0:
                break
            x_new = x - fx / dfx
            if abs(x_new - x) < 1e-12:
                return float(x_new)
            x = x_new
        return float(x)


def _b_transpose(matrix):
    return np.transpose(np.asarray(matrix))


def _b_det(matrix):
    return float(np.linalg.det(np.asarray(matrix, dtype=float)))


def _b_inverse(matrix):
    return np.linalg.inv(np.asarray(matrix, dtype=float))


def _b_eigenvalues(matrix):
    return np.linalg.eigvals(np.asarray(matrix, dtype=float))


def _b_dot(a, b):
    return np.dot(np.asarray(a), np.asarray(b))


def _b_cross(a, b):
    return np.cross(np.asarray(a), np.asarray(b))


def _b_linsolve(A, b):
    return np.linalg.solve(np.asarray(A, dtype=float), np.asarray(b, dtype=float))


# ══ statistics (NumPy) ══════════════════════════════════════════
def _b_mean(lst):   return float(np.mean(_as_number_list(lst)))
def _b_median(lst): return float(np.median(_as_number_list(lst)))
def _b_var(lst):    return float(np.var(_as_number_list(lst)))
def _b_std(lst):    return float(np.std(_as_number_list(lst)))
def _b_min(lst):    return min(_as_number_list(lst))
def _b_max(lst):    return max(_as_number_list(lst))
def _b_range(lst):
    data = _as_number_list(lst)
    return max(data) - min(data)
def _b_sum(lst):    return sum(_as_number_list(lst))
def _b_prod(lst):   return np.prod(_as_number_list(lst)).item()
def _b_corr(a, b):  return float(np.corrcoef(_as_number_list(a), _as_number_list(b))[0, 1])


def _b_random(n=None):
    if n is None:
        return random.random()
    return np.random.rand(int(n))


# ══ plotting (Matplotlib) ══════════════════════════════════════
def _b_plot(f_or_list, var, a, b, نقاط=300, عنوان=None, لون=None, حفظ=None):
    """ارسم: 2D line plot of one or more functions over [a, b]."""
    _setup_rtl_font()
    xs = np.linspace(float(a), float(b), int(نقاط))
    funcs = f_or_list if isinstance(f_or_list, (list, tuple)) else [f_or_list]
    plt.figure()
    for idx, f in enumerate(funcs):
        func = _callable_of(f, var)
        ys = np.array([float(func(x)) for x in xs], dtype=float)
        kwargs = {}
        if لون and len(funcs) == 1:
            kwargs["color"] = لون
        plt.plot(xs, ys, label=f"دالة {idx + 1}" if len(funcs) > 1 else None, **kwargs)
    if عنوان:
        plt.title(عنوان)
    if len(funcs) > 1:
        plt.legend()
    plt.grid(True)
    return _finish_plot(حفظ)


def _b_plot_parametric(x_expr, y_expr, t_var, t_a, t_b, نقاط=300, عنوان=None, حفظ=None):
    """ارسم_وسيط: parametric 2D plot."""
    _setup_rtl_font()
    ts = np.linspace(float(t_a), float(t_b), int(نقاط))
    fx = _callable_of(x_expr, t_var)
    fy = _callable_of(y_expr, t_var)
    xs = np.array([float(fx(t)) for t in ts], dtype=float)
    ys = np.array([float(fy(t)) for t in ts], dtype=float)
    plt.figure()
    plt.plot(xs, ys)
    if عنوان:
        plt.title(عنوان)
    plt.grid(True)
    return _finish_plot(حفظ)


def _b_plot3d(f, x_var, x_a, x_b, y_var, y_a, y_b, نقاط=50, عنوان=None, حفظ=None):
    """ارسم_ثلاثي: 3D surface plot."""
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)
    _setup_rtl_font()
    xs = np.linspace(float(x_a), float(x_b), int(نقاط))
    ys = np.linspace(float(y_a), float(y_b), int(نقاط))
    X, Y = np.meshgrid(xs, ys)
    sympy = _sympy() if not callable(f) else None
    if callable(f):
        Z = np.vectorize(lambda a, b: float(f(a, b)))(X, Y)
    else:
        func = sympy.lambdify((x_var, y_var), f, "numpy")
        Z = func(X, Y)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis")
    if عنوان:
        ax.set_title(عنوان)
    return _finish_plot(حفظ)


def _b_plot_data(points_list, نوع="نقاط", عنوان=None, حفظ=None):
    """ارسم_بيانات: scatter (or line) plot from points or two lists."""
    _setup_rtl_font()
    pts = list(points_list)
    if len(pts) == 2 and all(isinstance(c, (list, tuple, np.ndarray)) for c in pts):
        xs, ys = list(pts[0]), list(pts[1])
    else:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
    plt.figure()
    if نوع == "خط":
        plt.plot(xs, ys)
    else:
        plt.scatter(xs, ys)
    if عنوان:
        plt.title(عنوان)
    plt.grid(True)
    return _finish_plot(حفظ)


def _b_histogram(data, bins=10, عنوان=None, حفظ=None):
    """مدرج_تكراري: histogram."""
    _setup_rtl_font()
    plt.figure()
    plt.hist(_as_number_list(data), bins=int(bins))
    if عنوان:
        plt.title(عنوان)
    plt.grid(True)
    return _finish_plot(حفظ)


def _b_bar(labels, values, عنوان=None, حفظ=None):
    """مخطط_أعمدة: vertical bar chart."""
    _setup_rtl_font()
    plt.figure()
    plt.bar([str(l) for l in labels], list(values))
    if عنوان:
        plt.title(عنوان)
    plt.grid(True, axis="y")
    return _finish_plot(حفظ)


# ══ lists / strings ════════════════════════════════════════════
def _b_len(x):
    try:
        return len(x)
    except TypeError:
        raise HassoobRuntimeError("لا يمكن حساب طول هذا النوع")


def _b_slice(s, start, end):
    return s[_to_int_index(start):_to_int_index(end)]


def _b_replace(s, old, new):
    return str(s).replace(str(old), str(new))


def _b_split(s, sep):
    return str(s).split(str(sep))


def _b_join(sep, lst):
    return str(sep).join(str(x) for x in lst)


def _b_type_name(x):
    sympy_mod = sys.modules.get("sympy")
    if x is None:
        return "فارغ"
    if isinstance(x, bool):
        return "منطقي"
    if isinstance(x, (int, float)):
        return "عدد"
    if isinstance(x, str):
        return "نص"
    if isinstance(x, np.ndarray):
        return "مصفوفة"
    if sympy_mod is not None and isinstance(x, sympy_mod.Basic):
        return "رمزي"
    if isinstance(x, (list, tuple)):
        return "قائمة"
    if callable(x):
        return "دالة"
    return "غير معروف"


def _b_list_from(start, end, step=1):
    return list(range(_to_int_index(start), _to_int_index(end) + 1, _to_int_index(step)))


def _b_sort(lst, عكسي=False):
    return sorted(list(lst), reverse=bool(عكسي))


def _b_reverse(lst_or_str):
    if isinstance(lst_or_str, str):
        return lst_or_str[::-1]
    return list(reversed(list(lst_or_str)))


def _b_map(fn, lst):
    if not callable(fn):
        raise HassoobRuntimeError("الوسيط الأول لـ طبّق يجب أن يكون دالة")
    return [fn(x) for x in lst]


def _b_filter(fn, lst):
    if not callable(fn):
        raise HassoobRuntimeError("الوسيط الأول لـ صفّي يجب أن يكون دالة")
    return [x for x in lst if fn(x)]


# ══ registry ═════════════════════════════════════════════════
BUILTINS: dict[str, callable] = {
    # output
    "اطبع": _b_print,
    # symbolic math
    "بسط": _b_simplify,
    "وسع": _b_expand,
    "حلل": _b_factor,
    "عوض": _b_subs,
    "اشتق": _b_diff,
    "كامل": _b_integrate,
    "نهاية": _b_limit,
    "متسلسلة": _b_series,
    "حل": _b_solve,
    "حل_منظومة": _b_solve_system,
    "حل_تفاضلي": _b_dsolve,
    # numerical
    "جذر_عددي": _b_numeric_root,
    "نقل": _b_transpose,
    "محدد": _b_det,
    "معكوس": _b_inverse,
    "قيم_ذاتية": _b_eigenvalues,
    "ضرب_نقطي": _b_dot,
    "ضرب_متجهي": _b_cross,
    "حل_خطي": _b_linsolve,
    # statistics
    "متوسط": _b_mean,
    "وسيط": _b_median,
    "تباين": _b_var,
    "انحراف_معياري": _b_std,
    "أصغر": _b_min,
    "أكبر": _b_max,
    "مدى": _b_range,
    "مجموع": _b_sum,
    "ناتج": _b_prod,
    "ارتباط": _b_corr,
    "عشوائي": _b_random,
    # plotting
    "ارسم": _b_plot,
    "ارسم_وسيط": _b_plot_parametric,
    "ارسم_ثلاثي": _b_plot3d,
    "ارسم_بيانات": _b_plot_data,
    "مدرج_تكراري": _b_histogram,
    "مخطط_أعمدة": _b_bar,
    # lists / strings
    "طول": _b_len,
    "قطعة": _b_slice,
    "استبدل": _b_replace,
    "قسم": _b_split,
    "دمج": _b_join,
    "نوع": _b_type_name,
    "قائمة_من": _b_list_from,
    "ترتيب": _b_sort,
    "عكس": _b_reverse,
    "طبق": _b_map,
    "صفي": _b_filter,
    "اختر": _b_filter,   # اختر is an alias of صفّي
}

# Help text: list of builtin names grouped, used by the REPL's مساعدة command.
BUILTIN_NAMES = list(BUILTINS.keys())
