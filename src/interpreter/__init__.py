# ===========================================================================
# src/interpreter/__init__.py
# Public facade for the language.
#
# The PROVIDED ast_builder and external callers import names such as
# ``parse_expression`` and ``Interpreter`` from ``interpreter``. After the
# phase split the implementations live in frontend/ (parsing), backend/
# (evaluator) and driver/ (pipeline); this package re-exports them behind one
# stable name so those call sites keep working unchanged.
# ===========================================================================
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

from parsing import parse_program, parse_program_collecting, parse_expression  # noqa: E402
from evaluator import Interpreter, Function  # noqa: E402
from pipeline import run_source, compile_program  # noqa: E402

__all__ = [
    "parse_program",
    "parse_program_collecting",
    "parse_expression",
    "Interpreter",
    "Function",
    "run_source",
    "compile_program",
]
