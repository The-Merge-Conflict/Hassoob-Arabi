# ===========================================================================
# src/_pathsetup.py
# Single source of truth for Hassoob's import roots.
#
# The language source is organised by compiler phase: frontend (lexing +
# parsing -> AST), midend (semantic analysis + optimisation), and backend
# (tree-walking execution + runtime), with a small driver that wires the
# phases together. The modules address one another by short name, so this
# helper places the source root, each phase folder, the driver folder, and the
# generated ANTLR parser on sys.path. Importing it is idempotent.
# ===========================================================================
import os
import sys

_SRC = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_SRC)

_ROOTS = (
    os.path.join(_ROOT, "generated"),
    _SRC,
    os.path.join(_SRC, "frontend"),
    os.path.join(_SRC, "midend"),
    os.path.join(_SRC, "backend"),
    os.path.join(_SRC, "driver"),
)

for _p in _ROOTS:
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)
