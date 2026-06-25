# ---------------------------------------------------------------------------
# src/errors/semantic.py
# Static-analysis errors: SemanticError and the MultiError batch wrapper.
# ---------------------------------------------------------------------------
from __future__ import annotations
from .base import HassoobError, to_arabic_digits


class SemanticError(HassoobError):
    """خطأ دلالي: متغير غير معرّف، عدد وسائط خاطئ، إلخ / static-analysis failure."""
    kind = "خطأ دلالي"
    emoji = "🔍"


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


