# ─── ide/diagnostics.py ───
# Headless helpers (NO Tkinter, NO antlr import) that turn parser/analyser
# errors into editor-ready diagnostics plus "underline every occurrence" spans.
#
# The analyser already de-duplicates an undefined name to ONE error per scope
# (cascade suppression). To still help the user find ALL uses of a mistyped
# name in a long file, build() also returns an Underline span (character
# offsets into the ORIGINAL source) for every textual occurrence of each
# undefined name — outside strings and comments.
#
# Offsets:
#   * Underline spans come from a direct text scan, so they line up EXACTLY
#     with what the editor shows (Tk: "1.0 + <n> chars").
#   * A diagnostic's primary start/end come from the error's (line, col). The
#     parser strips harakat/tatweel OUTSIDE strings first, so the squiggle can
#     be off by the number of harakat before the token on its line.
#     Identifiers rarely carry harakat, so this is exact in practice; the
#     underline spans are always exact regardless.
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple

# Arabic-aware "word" char (mirrors ide/highlight.py): letters, tatweel,
# Western + Arabic-Indic digits, underscore. Python's \b is unreliable here.
_WORD = r"[\w\u0640\u0660-\u0669]"

# Spans we must NOT search inside: comments and string literals (mirrors the
# tokens ide/highlight.py colours as "comment"/"string").
_MASK_RE = re.compile(
    r"\#[^\n]*|ملاحظة[^\n]*|/\*.*?\*/"            # line + block comments
    r"|(?:[fF\u0641])?\"(?:\\.|[^\"\\\n])*\""          # "..."  (optional f/ف)
    r"|(?:[fF\u0641])?'(?:\\.|[^'\\\n])*'",            # '...'  (optional f/ف)
    re.DOTALL,
)


@dataclass
class Diagnostic:
    """One problem to show in the list/gutter (already de-duplicated)."""
    severity: str                       # "syntax" | "semantic"
    message: str
    hint: Optional[str] = None
    suggestion: Optional[str] = None
    line: Optional[int] = None
    col: Optional[int] = None
    start: Optional[int] = None         # char offset in source (see header note)
    end: Optional[int] = None
    symbol: Optional[str] = None        # the offending name, if any


@dataclass
class Underline:
    """One occurrence to underline. start/end are exact char offsets."""
    name: str
    start: int
    end: int


@dataclass
class Diagnostics:
    diagnostics: List[Diagnostic] = field(default_factory=list)
    underlines: List[Underline] = field(default_factory=list)


def line_starts(source: str) -> List[int]:
    """Char offset at which each (0-based) line begins."""
    starts = [0]
    for i, ch in enumerate(source):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def offset_of(starts: Sequence[int], line: Optional[int], col: Optional[int]):
    """Map a 1-based line + 0-based col to an absolute char offset, or None."""
    if line is None or col is None:
        return None
    i = line - 1
    if 0 <= i < len(starts):
        return starts[i] + col
    return None


def _masked_spans(source: str) -> List[Tuple[int, int]]:
    return [(m.start(), m.end()) for m in _MASK_RE.finditer(source)]


def occurrences(source: str, name: str,
                masked: Optional[Sequence[Tuple[int, int]]] = None
                ) -> List[Tuple[int, int]]:
    """Every whole-word occurrence of name in source, EXCLUDING matches inside
    strings/comments. Returns (start, end) char-offset pairs."""
    if not name:
        return []
    if masked is None:
        masked = _masked_spans(source)

    def inside(pos: int) -> bool:
        return any(a <= pos < b for a, b in masked)

    pat = re.compile(r"(?<!%s)%s(?!%s)" % (_WORD, re.escape(name), _WORD))
    return [(m.start(), m.end()) for m in pat.finditer(source)
            if not inside(m.start())]


def build(source: str, syntax_errors, semantic_errors, *, sort: bool = True
          ) -> Diagnostics:
    """Assemble editor-ready diagnostics + underline spans from already-
    collected parser/analyser errors. Pure: no parsing or analysis here."""
    out = Diagnostics()
    starts = line_starts(source)

    for err in (syntax_errors or []):
        s = offset_of(starts, getattr(err, "line", None), getattr(err, "col", None))
        out.diagnostics.append(Diagnostic(
            severity="syntax",
            message=getattr(err, "message", str(err)),
            hint=getattr(err, "hint", None),
            suggestion=getattr(err, "suggestion", None),
            line=getattr(err, "line", None), col=getattr(err, "col", None),
            start=s, end=(s + 1 if s is not None else None),
        ))

    undefined: List[str] = []
    for err in (semantic_errors or []):
        sym = getattr(err, "symbol", None)
        s = offset_of(starts, getattr(err, "line", None), getattr(err, "col", None))
        if s is not None and sym:
            end = s + len(sym)
        elif s is not None:
            end = s + 1
        else:
            end = None
        out.diagnostics.append(Diagnostic(
            severity="semantic",
            message=getattr(err, "message", str(err)),
            hint=getattr(err, "hint", None),
            suggestion=getattr(err, "suggestion", None),
            line=getattr(err, "line", None), col=getattr(err, "col", None),
            start=s, end=end, symbol=sym,
        ))
        if sym:
            undefined.append(sym)

    masked = _masked_spans(source)
    seen = set()
    for name in undefined:
        if name in seen:
            continue
        seen.add(name)
        for (a, b) in occurrences(source, name, masked):
            out.underlines.append(Underline(name=name, start=a, end=b))

    if sort:
        _BIG = 1 << 30
        out.diagnostics.sort(key=lambda d: d.start if d.start is not None else _BIG)
        out.underlines.sort(key=lambda u: u.start)
    return out
