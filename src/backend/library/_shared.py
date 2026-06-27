# ---------------------------------------------------------------------------
# src/library/_shared.py
# Helpers shared across the built-in submodules.
# ---------------------------------------------------------------------------
from __future__ import annotations

import numpy as np

from errors import HassoobRuntimeError


def _sympy():
    try:
        import sympy
        return sympy
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise HassoobRuntimeError(
            "هذه العملية الرمزية تحتاج إلى المكتبة sympy (ثبّتها عبر requirements.txt)"
        ) from exc


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


def _callable_of(f, var):
    """Return a 1-arg numeric python callable from a sympy expr or a callable."""
    if callable(f):
        return f
    sympy = _sympy()
    if isinstance(f, sympy.Basic):
        return sympy.lambdify(var, f, "numpy")
    raise HassoobRuntimeError("كان متوقعًا دالة أو تعبيرًا رمزيًا")
