# ---------------------------------------------------------------------------
# src/library/__init__.py
# Assembles the built-in registry for حاسوب عربي from the per-domain submodules.
# Public surface (consumed via _builtins_loader): BUILTINS, BUILTIN_NAMES,
# format_value, to_arabic_digits.
# ---------------------------------------------------------------------------
from __future__ import annotations

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
from .statistics import REGISTRY as _statistics  # noqa: E402
from .plotting import REGISTRY as _plotting  # noqa: E402
from .text_lists import REGISTRY as _text_lists  # noqa: E402

BUILTINS: dict[str, callable] = {}
for _registry in (_output, _symbolic, _numeric, _statistics, _plotting, _text_lists):
    BUILTINS.update(_registry)

# Help text: list of builtin names grouped, used by the REPL's مساعدة command.
BUILTIN_NAMES = list(BUILTINS.keys())

__all__ = ["BUILTINS", "BUILTIN_NAMES", "format_value", "to_arabic_digits"]
