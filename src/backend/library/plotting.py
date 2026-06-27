# ---------------------------------------------------------------------------
# src/library/plotting.py
# Plotting built-ins (Matplotlib).
# ---------------------------------------------------------------------------
from __future__ import annotations

import os
import sys

import numpy as np

# Matplotlib backend selection:
#   * Under pytest, or when HASSOOB_HEADLESS is set, force the non-interactive
#     Agg backend so plotting never blocks or crashes in CI / sandboxes.
#   * Otherwise leave matplotlib's automatic backend selection alone.
import matplotlib
if "pytest" in sys.modules or os.environ.get("HASSOOB_HEADLESS"):
    try:
        matplotlib.use("Agg")
    except Exception:
        pass
import matplotlib.pyplot as plt

from ._shared import _sympy, _as_number_list, _callable_of


def _setup_rtl_font():
    """Best-effort RTL-friendly font configuration for Arabic plot labels.

    Only selects a font family that is actually installed, so machines without
    Amiri / Noto fall back silently to matplotlib's bundled DejaVu Sans instead
    of flooding the console with "findfont: Font family ... not found" warnings
    for every label.
    """
    try:
        from matplotlib import font_manager
        matplotlib.rcParams["axes.unicode_minus"] = False
        available = {f.name for f in font_manager.fontManager.ttflist}
        for fam in ("Amiri", "Noto Naskh Arabic", "Noto Sans Arabic",
                    "Arial", "DejaVu Sans"):
            if fam in available:
                matplotlib.rcParams["font.family"] = fam
                break
        # If none of the preferred families exist, leave matplotlib's default.
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


REGISTRY = {
    "ارسم": _b_plot,
    "ارسم_وسيط": _b_plot_parametric,
    "ارسم_ثلاثي": _b_plot3d,
    "ارسم_بيانات": _b_plot_data,
    "مدرج_تكراري": _b_histogram,
    "مخطط_أعمدة": _b_bar,
}
