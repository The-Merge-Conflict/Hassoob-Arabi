"""الواجهة الأمامية — Front End (lexing + parsing -> AST).

This phase turns raw Arabic source text into an abstract syntax tree. It owns
tashkeel/digit normalisation and the ANTLR front-end (parsing), the AST node
classes (ast_nodes), the parse-tree -> AST translation (ast_builder, kept at
src/ for its pinned layout), and shared lexing helpers (lang_utils).

Public surface: parse_program, parse_program_collecting, parse_expression,
ASTBuilder, plus the ast_nodes and lang_utils modules.
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
    "parse_program": "parsing",
    "parse_program_collecting": "parsing",
    "parse_expression": "parsing",
    "ASTBuilder": "ast_builder",
}
_MODULES = ['ast_nodes', 'lang_utils']

__all__ = list(_EXPORTS) + list(_MODULES)


def __getattr__(name):  # PEP 562 lazy access
    if name in _EXPORTS:
        return getattr(importlib.import_module(_EXPORTS[name]), name)
    if name in _MODULES:
        return importlib.import_module(name)
    raise AttributeError(name)
