# ---------------------------------------------------------------------------
# src/_builtins_loader.py
# The built-in registry lives in the src/library/ package, split by domain
# (formatting, symbolic, numeric, statistics, plotting, text_lists). This shim
# keeps the import surface stable so the rest of the codebase is unchanged:
#     from _builtins_loader import BUILTINS, BUILTIN_NAMES, format_value, to_arabic_digits
# ---------------------------------------------------------------------------
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from library import BUILTINS, BUILTIN_NAMES, format_value, to_arabic_digits  # noqa: E402

__all__ = ["BUILTINS", "BUILTIN_NAMES", "format_value", "to_arabic_digits"]
