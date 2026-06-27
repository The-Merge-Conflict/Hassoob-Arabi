"""الواجهة الوسطى — Middle End (semantic analysis + optimisation).

This phase works purely on the AST, between the front end and the back end. It
performs static semantic analysis (scope and arity checks, misplaced control
flow, constant divide-by-zero), collecting every diagnostic rather than
stopping at the first, and then applies semantics-preserving AST optimisation.

Public surface: analyse, collect_semantic_errors (semantic) and optimize
(optimizer).
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
    "analyse": "semantic",
    "collect_semantic_errors": "semantic",
    "optimize": "optimizer",
}
_MODULES = ['semantic', 'optimizer']

__all__ = list(_EXPORTS) + list(_MODULES)


def __getattr__(name):  # PEP 562 lazy access
    if name in _EXPORTS:
        return getattr(importlib.import_module(_EXPORTS[name]), name)
    if name in _MODULES:
        return importlib.import_module(name)
    raise AttributeError(name)
