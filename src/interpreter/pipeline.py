# ---------------------------------------------------------------------------
# src/interpreter/pipeline.py
# run_source: the full parse -> optimise -> analyse -> interpret pipeline.
# ---------------------------------------------------------------------------
from __future__ import annotations
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
_ROOT = os.path.dirname(_SRC)
for _p in (os.path.join(_ROOT, 'generated'), _SRC):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from typing import Optional
from environment import Environment
from _builtins_loader import BUILTINS
from .evaluator import Interpreter
from .parsing import parse_program


def run_source(source: str, repl_mode: bool = False, interp: Optional[Interpreter] = None,
               env: Optional[Environment] = None):
    """Full pipeline: parse → optimise → analyse → interpret a source string."""
    from optimizer import optimize
    from semantic import analyse
    interp = interp or Interpreter(repl_mode=repl_mode)
    program = parse_program(source)
    program = optimize(program)
    analyse(program, builtin_names=list(BUILTINS.keys()))
    return interp.run(program, env or interp.global_env)
