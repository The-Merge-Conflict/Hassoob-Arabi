# ---------------------------------------------------------------------------
# src/library/symbolic.py
# Symbolic math built-ins (SymPy, imported lazily).
# ---------------------------------------------------------------------------
from __future__ import annotations

from ._shared import _sympy


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


REGISTRY = {
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
}
