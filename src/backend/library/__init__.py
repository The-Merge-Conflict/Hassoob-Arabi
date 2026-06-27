# ---------------------------------------------------------------------------
# src/library/__init__.py
# Assembles the built-in registry for حاسوب عربي from the per-domain submodules.
# Public surface (consumed via _builtins_loader): BUILTINS, BUILTIN_NAMES,
# format_value, to_arabic_digits.
# ---------------------------------------------------------------------------
from __future__ import annotations
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

# Ensure the src/ directory (this package's parent) is importable so the
# submodules can do "from errors import ..." regardless of how we were loaded.
_SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from errors import to_arabic_digits  # noqa: E402  (re-exported for the loader)

from .formatting import format_value  # noqa: E402
from .formatting import REGISTRY as _output  # noqa: E402
from .symbolic import REGISTRY as _symbolic  # noqa: E402
from .numeric import REGISTRY as _numeric  # noqa: E402
from .trigonometry import REGISTRY as _trigonometry  # noqa: E402
from .statistics import REGISTRY as _statistics  # noqa: E402
from .plotting import REGISTRY as _plotting  # noqa: E402
from .text_lists import REGISTRY as _text_lists  # noqa: E402

BUILTINS: dict[str, callable] = {}
for _registry in (_output, _symbolic, _numeric, _trigonometry, _statistics, _plotting, _text_lists):
    BUILTINS.update(_registry)

# Help text: list of builtin names grouped, used by the REPL's مساعدة command.
BUILTIN_NAMES = list(BUILTINS.keys())

__all__ = ["BUILTINS", "BUILTIN_NAMES", "format_value", "to_arabic_digits"]
