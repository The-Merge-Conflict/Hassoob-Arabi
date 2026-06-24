# ───────────────────────────────────────────────────────────────────────────
# ide/  ──  بيئة التطوير المتكاملة لحاسوب عربي / Hassoob Arabi IDE package
#
# Public surface:
#   * ide.engine.HassoobEngine   — headless run/REPL engine (no GUI deps)
#   * ide.highlight.Highlighter  — syntax-highlighting tokenizer (no GUI deps)
#   * ide.editor.launch()        — launch the Tkinter desktop IDE
#
# The engine and highlighter are intentionally free of any Tkinter import so
# they can be unit-tested headlessly and reused by other front-ends.
# ───────────────────────────────────────────────────────────────────────────

from .engine import HassoobEngine
from .highlight import Highlighter

__all__ = ["HassoobEngine", "Highlighter", "launch"]


def launch():
    """تشغيل واجهة بيئة التطوير الرسومية / launch the graphical IDE.

    Prefers the Qt (PySide6) front-end, which supports a TRUE right-to-left base
    paragraph direction — so Arabic code such as  اطبع("...")  reads correctly
    from the right.  If PySide6 is not installed we fall back to the Tkinter
    front-end (which can only right-align, not truly reorder RTL runs) and tell
    the user how to enable the proper RTL editor.

    Everything is imported lazily so that merely importing :mod:`ide` (for the
    engine or the highlighter) never requires a GUI toolkit.
    """
    import importlib.util

    if importlib.util.find_spec("PySide6") is not None:
        from .editor_qt import launch as _launch
        return _launch()

    print(
        "ℹ\ufe0f  للحصول على محرّر يميني (RTL) صحيح الاتجاه، ثبّت PySide6:\n"
        "      pip install PySide6\n"
        "   (يُفتح الآن محرّر Tkinter البديل الذي يحاذي لليمين فقط.)"
    )
    from .editor import launch as _launch
    return _launch()
