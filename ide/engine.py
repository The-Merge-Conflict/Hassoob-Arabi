# ───────────────────────────────────────────────────────────────────────────
# ide/engine.py
# Headless execution engine that powers the IDE.  NO Tkinter import — so it can
# be unit-tested and reused by any front-end.
#
# It wraps the language pipeline (parse → optimise → analyse → interpret),
# captures everything printed to stdout, and turns any failure into a cute,
# fully-Arabic message (reusing HassoobError.formatted()).
# ───────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import contextlib
import io
import os
import sys
from dataclasses import dataclass, field
from typing import List, Optional

# Make the project's src/ and generated/ importable no matter how we are run
# (python -m ide, main.py --ide, or `import ide` from the project root).
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (os.path.join(_ROOT, "generated"), os.path.join(_ROOT, "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from errors import HassoobError  # noqa: E402
from interpreter import Interpreter, compile_program  # noqa: E402
from _builtins_loader import BUILTINS, BUILTIN_NAMES, format_value, to_arabic_digits  # noqa: E402


_PARSER_MISSING_MSG = (
    "🔧 لم يتم توليد المُحلِّل النحوي بعد.\n"
    "   ولِّد ملفات ANTLR من جذر المشروع ثم أعد المحاولة:\n"
    "   antlr4 -Dlanguage=Python3 -visitor -o generated HassoobArabi.g4"
)


@dataclass
class RunResult:
    """Outcome of running a snippet or a REPL line."""

    ok: bool = True
    output: str = ""            # everything printed via اطبع / stdout
    error: Optional[str] = None  # cute Arabic error text, if any
    value: Optional[str] = None  # formatted REPL result (← ...), if any


class HassoobEngine:
    """Stateful engine: keeps one interpreter so REPL lines share state."""

    def __init__(self) -> None:
        self.reset()

    # ── session control ─────────────────────────────────────────────
    def reset(self) -> None:
        """Start a fresh interpreter session (clears all user state)."""
        self.interp = Interpreter()

    @property
    def builtin_names(self) -> List[str]:
        return list(BUILTIN_NAMES)

    # ── running ─────────────────────────────────────────────────────
    def run_source(self, source: str, *, fresh: bool = True) -> RunResult:
        """Run a whole program. When *fresh* is True, reset state first."""
        if fresh:
            self.reset()
        return self._execute(source, capture_value=False)

    def eval_line(self, source: str) -> RunResult:
        """Evaluate a single REPL line against the persistent session."""
        return self._execute(source, capture_value=True)

    # ── diagnostics (headless; powers IDE squiggles + underlines) ──
    def diagnose(self, source: str):
        """Analyse *source* WITHOUT running it and return structured diagnostics.

        Each problem is listed ONCE (the analyser de-duplicates an undefined
        name per scope). In addition, EVERY textual occurrence of each
        undefined name is returned as an underline span, so a front-end can
        highlight all of its uses while the list still shows it once. Never
        raises: on a parser/analyser failure it returns whatever it could
        collect (possibly an empty report).
        """
        try:
            from .diagnostics import build, Diagnostics
        except ImportError:  # imported without package context
            import sys as _sys
            if _HERE not in _sys.path:
                _sys.path.insert(0, _HERE)
            from diagnostics import build, Diagnostics  # type: ignore
        try:
            from interpreter.parsing import parse_program_collecting
            from semantic import collect_semantic_errors
        except Exception:
            return Diagnostics()
        try:
            program, syntax_errors = parse_program_collecting(source)
        except Exception:
            return Diagnostics()
        try:
            semantic_errors = collect_semantic_errors(
                program, builtin_names=self.builtin_names)
        except Exception:
            semantic_errors = []
        return build(source, syntax_errors, semantic_errors)

    # ── internals ───────────────────────────────────────────────────
    def _execute(self, source: str, *, capture_value: bool) -> RunResult:
        result = RunResult()
        buf = io.StringIO()
        try:
            program = compile_program(source, builtin_names=self.builtin_names)
            with contextlib.redirect_stdout(buf):
                self.interp.run(program)
            if capture_value:
                result.value = self._format_result(self._last_value())
        except HassoobError as err:
            result.ok = False
            result.error = err.formatted()
        except ModuleNotFoundError as err:
            result.ok = False
            result.error = self._module_error(err)
        except RecursionError:
            result.ok = False
            result.error = "⚠️ خطأ في التنفيذ: تجاوُز عمق الاستدعاء (تكرار غير منتهٍ؟)"
        except Exception as err:  # pragma: no cover - defensive catch-all
            result.ok = False
            result.error = f"🌸 عذرًا، حدث خطأ غير متوقّع: {err}"
        result.output = buf.getvalue()
        return result

    def _last_value(self):
        # The interpreter records the last evaluated expression statement's
        # value (mirrors the REPL).  Be tolerant about the attribute name.
        for attr in ("last_value", "_last_value", "result"):
            if hasattr(self.interp, attr):
                return getattr(self.interp, attr)
        return None

    @staticmethod
    def _format_result(value) -> Optional[str]:
        if value is None:
            return None
        sympy = sys.modules.get("sympy")
        if sympy is not None and isinstance(value, sympy.Basic):
            return to_arabic_digits(sympy.pretty(value, use_unicode=True))
        return format_value(value)

    @staticmethod
    def _module_error(err: ModuleNotFoundError) -> str:
        name = (err.name or "")
        if name.startswith("HassoobArabi") or name == "antlr4":
            return _PARSER_MISSING_MSG
        return (
            f"🔧 المكتبة المطلوبة ‹{name}› غير مُثبّتة.\n"
            "   ثبِّت المتطلبات: pip install -r requirements.txt"
        )
