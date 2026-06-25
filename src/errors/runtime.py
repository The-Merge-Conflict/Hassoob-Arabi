# ---------------------------------------------------------------------------
# src/errors/runtime.py
# Runtime errors raised while executing a program (HassoobRuntimeError).
# ---------------------------------------------------------------------------
from __future__ import annotations
from .base import HassoobError


class HassoobRuntimeError(HassoobError):
    """خطأ أثناء التنفيذ: قسمة على صفر، نوع خاطئ، إلخ / runtime failure."""
    kind = "خطأ في التنفيذ"
    emoji = "⚠️"


