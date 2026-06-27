"""الواجهة الخلفية — Back End (tree-walking execution + runtime).

This phase executes a validated AST. It owns the tree-walking interpreter
(evaluator), the lexical scope chain (environment), runtime operator/index
helpers (runtime_ops), the standard library (library) and its loader
(_builtins_loader).

Public surface: Interpreter, Function (evaluator), Environment (environment),
plus the runtime_ops, _builtins_loader and library modules.
"""
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

import importlib  # noqa: E402

_EXPORTS = {
    "Interpreter": "evaluator",
    "Function": "evaluator",
    "Environment": "environment",
}
_MODULES = ['runtime_ops', '_builtins_loader', 'library']

__all__ = list(_EXPORTS) + list(_MODULES)


def __getattr__(name):  # PEP 562 lazy access
    if name in _EXPORTS:
        return getattr(importlib.import_module(_EXPORTS[name]), name)
    if name in _MODULES:
        return importlib.import_module(name)
    raise AttributeError(name)
