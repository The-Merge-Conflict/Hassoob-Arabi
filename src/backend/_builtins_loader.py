# ---------------------------------------------------------------------------
# src/_builtins_loader.py
# The built-in registry lives in the src/library/ package, split by domain
# (formatting, symbolic, numeric, statistics, plotting, text_lists). This shim
# keeps the import surface stable so the rest of the codebase is unchanged:
#     from _builtins_loader import BUILTINS, BUILTIN_NAMES, format_value, to_arabic_digits
# ---------------------------------------------------------------------------
# -- source-path bootstrap ---------------------------------------------------
# Hassoob's modules refer to one another by short name (e.g. ``from errors
# import ...``). Register the source root plus every compiler-phase folder so
# those names resolve no matter which module Python imports first.
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "src" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d and _d not in _sys.path:
    _sys.path.insert(0, _d)
import _pathsetup  # noqa: F401,E402  (registers all phase roots on sys.path)

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from library import BUILTINS, BUILTIN_NAMES, format_value, to_arabic_digits  # noqa: E402

__all__ = ["BUILTINS", "BUILTIN_NAMES", "format_value", "to_arabic_digits"]
