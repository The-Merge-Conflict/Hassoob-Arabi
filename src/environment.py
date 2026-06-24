# ───────────────────────────────────────────────────────────────────────────
# src/environment.py
# Lexical scope chain: a linked list of dict frames supporting closures.
# ───────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import os, sys
from typing import Any, Callable, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from errors import SemanticError, closest_name


class Environment:
    """إطار نطاق واحد في سلسلة النطاقات / one frame in the scope chain.

    Parameters
    ----------
    parent:
        The enclosing scope, or ``None`` for the global frame.
    """

    __slots__ = ("vars", "parent")

    def __init__(self, parent: Optional["Environment"] = None):
        self.vars: dict[str, Any] = {}
        self.parent = parent

    # ── lookup ──────────────────────────────────────────────────────
    def _all_names(self) -> set:
        """جمع كل الأسماء المعرّفة في السلسلة (لاقتراحات «هل تقصد»)."""
        names: set = set()
        env: Optional[Environment] = self
        while env is not None:
            names.update(env.vars.keys())
            env = env.parent
        return names

    def get(self, name: str) -> Any:
        """Walk the chain upward and return the value bound to ``name``."""
        env: Optional[Environment] = self
        while env is not None:
            if name in env.vars:
                return env.vars[name]
            env = env.parent
        raise SemanticError(
            f"المتغيّر ‹{name}› غير معرّف بعد",
            suggestion=closest_name(name, self._all_names()),
            hint="تأكّد من كتابة الاسم صحيحًا أو عرّفه قبل استخدامه.",
        )

    def has(self, name: str) -> bool:
        """Return True if ``name`` is bound anywhere along the chain."""
        env: Optional[Environment] = self
        while env is not None:
            if name in env.vars:
                return True
            env = env.parent
        return False

    # ── mutation ──────────────────────────────────────────────────
    def set(self, name: str, value: Any) -> None:
        """Bind ``name`` in the *current* frame (used for new variables)."""
        self.vars[name] = value

    def assign(self, name: str, value: Any) -> None:
        """Update an *existing* binding wherever it lives in the chain."""
        env: Optional[Environment] = self
        while env is not None:
            if name in env.vars:
                env.vars[name] = value
                return
            env = env.parent
        raise SemanticError(
            f"لا يمكن الإسناد إلى متغيّر غير معرّف ‹{name}›",
            suggestion=closest_name(name, self._all_names()),
            hint="عرّف المتغيّر أولاً بإسناد قيمة له.",
        )

    # ── globals / builtins ──────────────────────────────────────────
    def assign_or_define(self, name: str, value: Any) -> None:
        """إسناد على نمط ماثيماتيكا / Mathematica-like assignment.

        Mutate an existing binding wherever it lives along the scope chain; if
        the name is bound nowhere, define it in the *current* frame. This makes
        plain ``=`` update an existing outer (e.g. global) variable instead of
        silently creating a local shadow, matching ``+=`` (env.assign) for
        existing names while still allowing first-time definitions.
        """
        env: Optional[Environment] = self
        while env is not None:
            if name in env.vars:
                env.vars[name] = value
                return
            env = env.parent
        self.vars[name] = value

    def global_frame(self) -> "Environment":
        """Return the root (parent-less) frame of the chain."""
        env = self
        while env.parent is not None:
            env = env.parent
        return env

    def define_builtin(self, name: str, fn: Callable) -> None:
        """Register a built-in callable in the global frame."""
        self.global_frame().vars[name] = fn

    def child(self) -> "Environment":
        """Create and return a new scope nested directly under this one."""
        return Environment(parent=self)

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"Environment(keys={list(self.vars)}, has_parent={self.parent is not None})"
