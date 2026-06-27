# ===========================================================================
# conftest.py
# pytest auto-loads this before collecting tests. It puts src/ on sys.path so
# _pathsetup can register every compiler-phase folder (frontend / midend /
# backend / driver) plus the generated parser, letting the test modules import
# language modules by short name (from semantic import ..., etc.).
# ===========================================================================
import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
import _pathsetup  # noqa: E402,F401  (registers all phase roots on sys.path)
