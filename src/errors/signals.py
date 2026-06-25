# ---------------------------------------------------------------------------
# src/errors/signals.py
# Internal control-flow signals (NOT errors): Return / Break / Continue.
# ---------------------------------------------------------------------------
from __future__ import annotations


# ── Control-flow signals (NOT errors) ────────────────────────────────
# These are raised internally by the interpreter to unwind the Python call stack
# when executing إرجع / اوقف / استمر. They are deliberately *not* subclasses of
# HassoobError so user-facing error handlers never accidentally swallow them.

class ReturnSignal(Exception):
    """إشارة إرجاع قيمة من دالة / carries a function's return value."""

    def __init__(self, value=None):
        self.value = value
        super().__init__("إرجع خارج السياق الصحيح")


class BreakSignal(Exception):
    """إشارة كسر حلقة / loop break."""


class ContinueSignal(Exception):
    """إشارة متابعة حلقة / loop continue."""
