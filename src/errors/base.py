# ---------------------------------------------------------------------------
# src/errors/base.py
# Text-normalisation helpers (to_arabic_digits, closest_name) and the base
# HassoobError class that every language error derives from.
# ---------------------------------------------------------------------------
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


