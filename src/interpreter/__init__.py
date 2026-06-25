# ---------------------------------------------------------------------------
# src/interpreter/ package
# Re-exports the public surface so `from interpreter import Interpreter,
# Function, parse_program, parse_expression, run_source` keeps working.
# ---------------------------------------------------------------------------
from __future__ import annotations
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
_ROOT = os.path.dirname(_SRC)
for _p in (os.path.join(_ROOT, 'generated'), _SRC):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from .evaluator import Interpreter, Function
from .parsing import parse_program, parse_expression
from .pipeline import run_source

__all__ = ['Interpreter', 'Function', 'parse_program', 'parse_expression', 'run_source']
