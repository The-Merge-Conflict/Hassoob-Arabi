# ---------------------------------------------------------------------------
# src/library/trigonometry.py
# Trigonometric built-ins (الدوال المثلثية): sine (جا/جيب) and
# cosine (جتا/جيب_تمام).
#
# Like the rest of the library, these bridge the numeric and symbolic engines:
#   • symbolic expressions (SymPy)  → a symbolic result, e.g. جا(س) ⇒ sin(س)
#   • matrices / arrays (NumPy)      → element-wise sine/cosine
#   • plain numbers                  → a float via the standard math module
#
# Angles are measured in RADIANS — exactly like math.sin / numpy.sin / SymPy.
# (الزوايا تُقاس بالراديان، وليس بالدرجات.)
# ---------------------------------------------------------------------------
from __future__ import annotations

import math
import sys

import numpy as np

from errors import HassoobRuntimeError


def _sympy_if_symbolic(x):
    """أعد وحدة sympy إن كان x تعبيرًا رمزيًا، وإلا None.

    Return the live sympy module iff ``x`` is a sympy expression. We look the
    module up in ``sys.modules`` (instead of importing it) so a program that
    never touches symbolic math does not pay the SymPy import cost.
    """
    sympy_mod = sys.modules.get("sympy")
    if sympy_mod is not None and isinstance(x, sympy_mod.Basic):
        return sympy_mod
    return None


def _b_sin(x):
    """جا/جيب: sine of x (x in radians; symbolic- and array-aware)."""
    sympy_mod = _sympy_if_symbolic(x)
    if sympy_mod is not None:
        return sympy_mod.sin(x)
    if isinstance(x, np.ndarray):
        return np.sin(x)
    try:
        return math.sin(float(x))
    except (TypeError, ValueError):
        raise HassoobRuntimeError(
            "الدالة ‹جا› تتوقّع عددًا (زاوية بالراديان) أو تعبيرًا رمزيًا",
            hint="مرّر عددًا مثل جا(٠) أو رمزًا مثل جا(س)، لا نصًا أو قائمة.",
        )


def _b_cos(x):
    """جتا/جيب_تمام: cosine of x (x in radians; symbolic- and array-aware)."""
    sympy_mod = _sympy_if_symbolic(x)
    if sympy_mod is not None:
        return sympy_mod.cos(x)
    if isinstance(x, np.ndarray):
        return np.cos(x)
    try:
        return math.cos(float(x))
    except (TypeError, ValueError):
        raise HassoobRuntimeError(
            "الدالة ‹جتا› تتوقّع عددًا (زاوية بالراديان) أو تعبيرًا رمزيًا",
            hint="مرّر عددًا مثل جتا(٠) أو رمزًا مثل جتا(س)، لا نصًا أو قائمة.",
        )


REGISTRY = {
    "جا": _b_sin,
    "جيب": _b_sin,        # مرادف لـ جا (alias of جا)
    "جتا": _b_cos,
    "جيب_تمام": _b_cos,   # مرادف لـ جتا (alias of جتا)
}
