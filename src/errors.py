# ───────────────────────────────────────────────────────────────────────────
# src/errors.py
# Custom exception hierarchy for حاسوب عربي. All user-facing messages are
# Arabic, friendly ("cute"), and — when possible — include a "did you mean…"
# (هل تقصد) suggestion plus a helpful hint.
# ───────────────────────────────────────────────────────────────────────
from __future__ import annotations
from typing import Iterable, Optional
import difflib


# ══ text normalisation ═════════════════════════════════════════
_WESTERN_TO_ARABIC = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def to_arabic_digits(s) -> str:
    """تحويل الأرقام اللاتينية (0-9) إلى أرقام عربية (٠-٩).

    Convert any Western digits in a string to Arabic-Indic digits. Used so that
    every value printed by the language comes out with Arabic numerals,
    regardless of whether the source used Arabic or Western digits.
    """
    return str(s).translate(_WESTERN_TO_ARABIC)


def closest_name(name, candidates: Iterable[str], n: int = 1, cutoff: float = 0.6) -> Optional[str]:
    """أقرب اسم مشابه لاقتراح «هل تقصد» / closest match for a 'did you mean' hint.

    Returns the single best fuzzy match for ``name`` among ``candidates`` (or
    ``None`` if nothing is close enough). Powered by difflib.
    """
    try:
        pool = [str(c) for c in candidates if str(c) != str(name)]
        matches = difflib.get_close_matches(str(name), pool, n=n, cutoff=cutoff)
    except Exception:
        return None
    return matches[0] if matches else None


class HassoobError(Exception):
    """الصنف الأساس لكل أخطاء اللغة / base class for all language errors.

    Carries an optional line/column, an optional "did you mean" ``suggestion``
    and an optional ``hint``. The main line keeps the canonical shape:
        خطأ في السطر {line}، العمود {col}: {message}
    and is prefixed with a small friendly emoji.
    """

    #: A short Arabic label describing the error category (overridden by subclasses).
    kind: str = "خطأ"
    #: A cute emoji shown before the message.
    emoji: str = "💡"

    def __init__(self, message: str, line: Optional[int] = None, col: Optional[int] = None,
                 suggestion: Optional[str] = None, hint: Optional[str] = None):
        self.message = message
        self.line = line
        self.col = col
        self.suggestion = suggestion
        self.hint = hint
        super().__init__(self.formatted())

    def formatted(self) -> str:
        """Return the fully formatted, cute Arabic error string."""
        if self.line is not None and self.col is not None:
            # ANTLR/token columns are 0-based internally; display them 1-based
            # so they match what the user sees in their editor.
            head = (f"{self.emoji} خطأ في السطر {to_arabic_digits(self.line)}، "
                    f"العمود {to_arabic_digits(self.col + 1)}: {self.message}")
        elif self.line is not None:
            head = f"{self.emoji} خطأ في السطر {to_arabic_digits(self.line)}: {self.message}"
        else:
            head = f"{self.emoji} {self.kind}: {self.message}"
        lines = [head]
        if self.suggestion:
            lines.append(f"   ↪ هل تقصد ‹{self.suggestion}›؟")
        if self.hint:
            lines.append(f"   💡 {self.hint}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.formatted()


class LexError(HassoobError):
    """فشل في التحليل اللفظي / tokenisation failure."""
    kind = "خطأ لفظي"
    emoji = "🔤"


class ParseError(HassoobError):
    """مخالفة لقواعد اللغة / grammar violation."""
    kind = "خطأ نحوي"
    emoji = "📝"


class SemanticError(HassoobError):
    """خطأ دلالي: متغير غير معرّف، عدد وسائط خاطئ، إلخ / static-analysis failure."""
    kind = "خطأ دلالي"
    emoji = "🔍"


class HassoobRuntimeError(HassoobError):
    """خطأ أثناء التنفيذ: قسمة على صفر، نوع خاطئ، إلخ / runtime failure."""
    kind = "خطأ في التنفيذ"
    emoji = "⚠️"


class MultiError(HassoobError):
    """عدّة أخطاء مجمّعة من تحليل واحد / a batch of collected analysis errors.

    Used by the semantic pass to report every independent problem it found in a
    single run instead of stopping at the first. Sub-errors are ordered by
    position (line then column); position-less errors keep their discovery order.
    """
    kind = "أخطاء متعددة"
    emoji = "📚"

    def __init__(self, errors):
        _BIG = 1 << 30
        self.errors = sorted(
            errors,
            key=lambda e: (e.line if e.line is not None else _BIG,
                           e.col if e.col is not None else _BIG),
        )
        super().__init__(
            f"عُثر على {to_arabic_digits(len(self.errors))} خطأ في الكود"
        )

    def formatted(self) -> str:
        lines = [f"{self.emoji} {self.kind}: {self.message}"]
        for i, e in enumerate(self.errors, start=1):
            block = e.formatted()
            indented = "\n".join("   " + ln for ln in block.split("\n"))
            lines.append(f" ({to_arabic_digits(i)})\n{indented}")
        lines.append(
            "��️ قد تكون بعض الأخطاء التالية ناتجةً عن الأول، "
            "فأصلِح الأول أوّلًا ثم أعِد التشغيل."
        )
        return "\n".join(lines)


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
