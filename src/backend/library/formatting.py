# ---------------------------------------------------------------------------
# src/library/formatting.py
# Value formatting + the اطبع (print) built-in.
# ---------------------------------------------------------------------------
from __future__ import annotations

import numpy as np

from errors import to_arabic_digits


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


def _b_print(*args):
    """اطبع: print all arguments space-separated; returns None."""
    print(" ".join(format_value(a) for a in args))
    return None


REGISTRY = {
    "اطبع": _b_print,
}
