# ───────────────────────────────────────────────────────────────────────────
# src/_builtins_loader.py
# The built-in registry lives in src/builtins.py (as required by the project
# layout). That filename collides with Python's standard-library `builtins`
# module, which is *always* present in sys.modules, so a plain
# `from builtins import ...` would resolve to the stdlib instead of ours.
#
# This shim loads our file explicitly by path under the private module name
# `hassoob_builtins` (cached/shared via sys.modules) and re-exports its public
# surface, so every other module can simply do:
#     from _builtins_loader import BUILTINS, BUILTIN_NAMES, format_value, to_arabic_digits
# ───────────────────────────────────────────────────────────────────────
import os
import sys
import importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

_NAME = "hassoob_builtins"


def _load():
    if _NAME in sys.modules:
        return sys.modules[_NAME]
    spec = importlib.util.spec_from_file_location(_NAME, os.path.join(_HERE, "builtins.py"))
    module = importlib.util.module_from_spec(spec)
    # Register before exec so any self-references resolve to the same instance.
    sys.modules[_NAME] = module
    spec.loader.exec_module(module)
    return module


_mod = _load()

BUILTINS = _mod.BUILTINS
BUILTIN_NAMES = _mod.BUILTIN_NAMES
format_value = _mod.format_value
to_arabic_digits = _mod.to_arabic_digits
