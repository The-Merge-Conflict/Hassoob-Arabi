# ---------------------------------------------------------------------------
# src/interpreter/pipeline.py
# run_source: the full parse -> analyse -> optimise -> interpret pipeline.
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
from evaluator import Interpreter
from parsing import parse_program, parse_program_collecting


def compile_program(source: str, builtin_names=None):
    """Front-end: parse → analyse → optimise, returning a ready-to-run program.

    Two error-handling modes:
      • No syntax errors  → happy path: analyse, then optimise the tree.
      • Syntax errors     → collect-all + cross-phase recovery : every
        syntax error is gathered, the partially-built tree (with ErrorNode
        placeholders) is still analysed to surface semantic errors too, and all
        of them are raised together as a MultiError. A broken program is never
        optimised or executed.
    """
    from optimizer import optimize
    from semantic import analyse, collect_semantic_errors
    from errors import MultiError

    if builtin_names is None:
        builtin_names = list(BUILTINS.keys())

    program, syntax_errors = parse_program_collecting(source)
    if not syntax_errors:
        # analyse → optimise: analysis runs on the tree as written (so static
        # checks see the original constants), then the optimiser runs on the
        # validated tree.
        analyse(program, builtin_names=builtin_names)
        program = optimize(program)
        return program

    # Cross-phase recovery: keep going into the semantic phase on the partial
    # tree so the user sees syntax AND semantic errors at once.
    semantic_errors = collect_semantic_errors(program, builtin_names=builtin_names)
    all_errors = list(syntax_errors) + list(semantic_errors)
    if len(all_errors) == 1:
        raise all_errors[0]
    raise MultiError(all_errors)


def run_source(source: str, repl_mode: bool = False, interp: Optional[Interpreter] = None,
               env: Optional[Environment] = None):
    """Full pipeline: parse → analyse → optimise → interpret a source string."""
    interp = interp or Interpreter(repl_mode=repl_mode)
    program = compile_program(source)
    return interp.run(program, env or interp.global_env)
