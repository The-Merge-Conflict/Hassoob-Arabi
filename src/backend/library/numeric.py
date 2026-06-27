# ---------------------------------------------------------------------------
# src/library/numeric.py
# Numerical / linear-algebra built-ins (NumPy / SciPy).
# ---------------------------------------------------------------------------
from __future__ import annotations

import numpy as np

from ._shared import _callable_of


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


REGISTRY = {
    "جذر_عددي": _b_numeric_root,
    "نقل": _b_transpose,
    "محدد": _b_det,
    "معكوس": _b_inverse,
    "قيم_ذاتية": _b_eigenvalues,
    "ضرب_نقطي": _b_dot,
    "ضرب_متجهي": _b_cross,
    "حل_خطي": _b_linsolve,
}
