# ---------------------------------------------------------------------------
# src/errors/ package
# Re-exports the full public error/signal surface so existing imports like
#   from errors import HassoobError, ParseError, ReturnSignal, ...
# keep working unchanged after the split.
# ---------------------------------------------------------------------------
from .base import to_arabic_digits, closest_name, HassoobError
from .syntax import LexError, ParseError
from .semantic import SemanticError, MultiError
from .runtime import HassoobRuntimeError
from .signals import ReturnSignal, BreakSignal, ContinueSignal

__all__ = [
    'to_arabic_digits', 'closest_name', 'HassoobError',
    'LexError', 'ParseError',
    'SemanticError', 'MultiError',
    'HassoobRuntimeError',
    'ReturnSignal', 'BreakSignal', 'ContinueSignal',
]
