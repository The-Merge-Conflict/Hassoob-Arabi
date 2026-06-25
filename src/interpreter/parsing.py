# ---------------------------------------------------------------------------
# src/interpreter/parsing.py
# ANTLR front-end: tashkeel stripping, friendly Arabic syntax-error
# translation, and the parse_program / parse_expression entry points.
# ---------------------------------------------------------------------------
from __future__ import annotations
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
_ROOT = os.path.dirname(_SRC)
for _p in (os.path.join(_ROOT, 'generated'), _SRC):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import unicodedata as _ud
from ast_nodes import ProgramNode


_TATWEEL = "\u0640"  # ـ  kashida / elongation mark


def _strip_tashkeel(source: str) -> str:
    """أزِل التشكيل (الحركات) والتطويل من الشيفرة خارج النصوص والتعليقات.

    حتّى تُقرأ ‹إذِا›/‹إذّا› تمامًا كـ‹إذا›. لا تُغيّر أشكال الحروف
    عمدًا (فـ‹خطأ› تبقى ‹خطأ› ولا تصير ‹خطا›)؛ يُحذف فقط التشكيل
    والتطويل. النصوص ("..." / '...') والتعليقات (# و/* */ وملاحظة)
    تُنسخ كما هي للحفاظ على أيّ حركات مقصودة داخلها.
    """
    source = _ud.normalize("NFC", source)
    out = []
    i, n = 0, len(source)
    while i < n:
        ch = source[i]
        if ch == '"' or ch == "'":            # string literal -> copy verbatim
            quote = ch
            out.append(ch); i += 1
            while i < n:
                c = source[i]; out.append(c)
                if c == "\\" and i + 1 < n:    # keep escape + escaped char
                    out.append(source[i + 1]); i += 2; continue
                i += 1
                if c == quote:
                    break
            continue
        if ch == "#":                          # line comment -> end of line
            while i < n and source[i] not in "\r\n":
                out.append(source[i]); i += 1
            continue
        if ch == "/" and i + 1 < n and source[i + 1] == "*":   # block comment
            out.append("/"); out.append("*"); i += 2
            while i < n:
                if source[i] == "*" and i + 1 < n and source[i + 1] == "/":
                    out.append("*"); out.append("/"); i += 2; break
                out.append(source[i]); i += 1
            continue
        if source.startswith("ملاحظة", i):     # arabic line comment -> EOL
            while i < n and source[i] not in "\r\n":
                out.append(source[i]); i += 1
            continue
        if ch == _TATWEEL or _ud.combining(ch):  # drop diacritic / tatweel
            i += 1
            continue
        out.append(ch); i += 1
    return "".join(out)


# ══ parsing helpers (require the ANTLR-generated parser + antlr4 runtime) ═══════
# ── friendly Arabic translation of ANTLR's raw syntax-error messages ──────────
# ANTLR's default messages (e.g. "extraneous input '=' expecting {...}") are in
# English and dump escaped token names — terrifying for a normal developer.  We
# translate them into calm, cute Arabic with a helpful hint instead.

_EOF = -1  # antlr4 Token.EOF (kept as a constant so this stays import-free)

_TOKEN_AR = {
    "ASSIGN": "=", "ARROW": "=>",
    "PLUS": "+", "MINUS": "-", "STAR": "*", "SLASH": "/", "CARET": "^",
    "PERCENT": "%", "INT_DIV": "÷", "MAT_MUL": "**", "STR_CONCAT": "++",
    "PLUS_ASSIGN": "+=", "MINUS_ASSIGN": "-=", "STAR_ASSIGN": "*=",
    "SLASH_ASSIGN": "/=", "CARET_ASSIGN": "^=", "PERCENT_ASSIGN": "%=",
    "CONCAT_ASSIGN": "++=",
    "EQ": "==", "NEQ": "≠", "LT": "<", "GT": ">", "LTE": "≤", "GTE": "≥",
    "LPAREN": "(", "RPAREN": ")", "LBRACKET": "[", "RBRACKET": "]",
    "LBRACE": "{", "RBRACE": "}", "COMMA": "،", "SEMI": "؛", "COLON": ":",
    "DOT": ".",
    "AND": "و", "OR": "أو", "NOT": "ليس",
    "IDHA": "إذا", "WA_ILLA": "وإلا", "BAYNAMA": "بينما", "LIKULL": "لكل",
    "MIN": "من", "ILA": "إلى", "FI": "في", "BKHUTWA": "بخطوة",
    "DALA": "دالة", "IRJA": "إرجع", "AWQIF": "اوقف", "ISTAMIRR": "استمر",
    "SAHIH": "صح", "KHATA": "خطأ", "FARIG": "فارغ", "RAMZ": "رمز",
    "PI_CONST": "باي", "E_CONST": "هـ", "INF_CONST": "لانهاية",
    "INTEGER_LIT": "عدد صحيح", "FLOAT_LIT": "عدد عشري",
    "STRING_LIT": "نص", "FSTRING_LIT": "نص منسّق", "IDENTIFIER": "اسم",
}


_MATCHING_CLOSE = {"(": ")", "[": "]", "{": "}"}


def _find_unclosed_bracket(recognizer):
    """ابحث عن أوّل قوس فُتِح ولم يُغلق في مجرى الرموز."""
    try:
        stream = recognizer.getInputStream()
        toks = list(getattr(stream, "tokens", []) or [])
    except Exception:
        return None
    names = getattr(recognizer, "symbolicNames", []) or []

    def sym(tok):
        tt = getattr(tok, "type", -1)
        return names[tt] if 0 <= tt < len(names) else None

    closers = {"RPAREN": "LPAREN", "RBRACKET": "LBRACKET", "RBRACE": "LBRACE"}
    openers = set(closers.values())
    stack = []
    for tok in toks:
        s = sym(tok)
        if s in openers:
            stack.append(tok)
        elif s in closers and stack:
            stack.pop()
    return stack[0] if stack else None


def _friendly_syntax_error(recognizer, offending, line, column, msg, is_lexer):
    """Translate an ANTLR syntax error into (message, hint) in cute Arabic."""
    import re as _re
    from errors import to_arabic_digits

    def show(text):
        return to_arabic_digits(str(text))

    # The token we choked on.
    if offending is not None and getattr(offending, "type", None) != _EOF:
        bad = show(offending.text)
    elif offending is not None:
        bad = "نهاية الملف"
    else:  # lexer errors carry no token; pull the offending text out of the raw message
        m = _re.search(r"'(.+?)'", msg or "")
        bad = show(m.group(1)) if m else "رمز"

    if is_lexer:
        return (f"رمز غير مفهوم ‹{bad}›",
                "هذا الرمز غير مُعرَّف في اللغة؛ احذفه أو استبدله برمز صحيح.")

    # If we ran into the end of the file, a bracket was probably left open.
    if bad == "نهاية الملف":
        opener = _find_unclosed_bracket(recognizer)
        if opener is not None:
            br = show(opener.text)
            return (f"قوس ‹{br}› في السطر {show(opener.line)} لم يُغلق",
                    f"أغلق هذا القوس ‹{br}› بإضافة "
                    f"‹{_MATCHING_CLOSE.get(opener.text, '')}› المقابل.")

    # Decode the set of tokens the parser would have accepted here.
    def disp(t):
        if t == _EOF:
            return "نهاية الملف"
        names = getattr(recognizer, "symbolicNames", []) or []
        if 0 <= t < len(names) and names[t] not in (None, "<INVALID>"):
            name = names[t]
            if name in _TOKEN_AR:
                return _TOKEN_AR[name]
        lits = getattr(recognizer, "literalNames", []) or []
        if 0 <= t < len(lits) and lits[t] not in (None, "<INVALID>"):
            return lits[t].strip("'")
        if 0 <= t < len(names) and names[t] not in (None, "<INVALID>"):
            return names[t]
        return None

    expected = []
    try:
        for t in recognizer.getExpectedTokens().toList():
            d = disp(t)
            if d and d not in expected:
                expected.append(d)
    except Exception:
        expected = []

    low = (msg or "").lower()
    if low.startswith("missing"):
        want = expected[0] if expected else None
        message = f"ينقص الرمز ‹{want}›" if want else "ينقص رمز مطلوب"
        hint = (f"أضِف ‹{want}› قبل ‹{bad}›." if want and bad != "نهاية الملف"
                else "أكمِل الجملة بالرمز الناقص.")
        return message, hint

    if "no viable alternative" in low:
        message = f"تركيب غير مفهوم قرب ‹{bad}›"
    else:
        message = f"لم أتوقّع ‹{bad}› هنا"

    if bad == "=":
        hint = ("لإسناد قيمة اكتب ‹الاسم = القيمة› في جملة مستقلّة. "
                "وتذكّر أنّ ‹رمز› لإعلان الرموز فقط بلا إسناد، مثل: ‹رمز س›.")
    elif not expected:
        hint = "تأكّد من اكتمال الجملة السابقة ومن عدم وجود رمز زائد."
    elif len(expected) <= 5:
        hint = "كنت أتوقّع أحد هذه: " + "، ".join(f"‹{x}›" for x in expected) + "."
    else:
        hint = ("يبدو أنّ الجملة السابقة قد اكتملت، فهذا الرمز زائد هنا؛ "
                "ابدأ جملة جديدة أو احذف الرمز الزائد.")
    return message, hint


class _RaisingErrorListener:
    """ANTLR error listener that converts syntax errors into cute Arabic
    ParseError / LexError instances (never the raw English ANTLR message)."""

    def __init__(self, error_cls, is_lexer=False):
        self._error_cls = error_cls
        self._is_lexer = is_lexer

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        try:
            message, hint = _friendly_syntax_error(
                recognizer, offendingSymbol, line, column, msg, self._is_lexer)
        except Exception:
            message, hint = msg, None
        raise self._error_cls(message, line=line, col=column, hint=hint)

    # The remaining ANTLR ErrorListener hooks are no-ops for our purposes.
    def reportAmbiguity(self, *a, **k):  # pragma: no cover
        pass

    def reportAttemptingFullContext(self, *a, **k):  # pragma: no cover
        pass

    def reportContextSensitivity(self, *a, **k):  # pragma: no cover
        pass


def _make_parser(source: str):
    from antlr4 import InputStream, CommonTokenStream
    from HassoobArabiLexer import HassoobArabiLexer
    from HassoobArabiParser import HassoobArabiParser
    from errors import LexError, ParseError

    source = _strip_tashkeel(source)   # CHANGED: ignore harakat/tatweel outside strings
    input_stream = InputStream(source)
    lexer = HassoobArabiLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(_RaisingErrorListener(LexError, is_lexer=True))
    tokens = CommonTokenStream(lexer)
    parser = HassoobArabiParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(_RaisingErrorListener(ParseError, is_lexer=False))
    return parser


def parse_program(source: str) -> ProgramNode:
    """Lex+parse a whole program and return its AST (ProgramNode)."""
    from ast_builder import ASTBuilder
    parser = _make_parser(source)
    tree = parser.program()
    return ASTBuilder().visit(tree)


def parse_expression(source: str):
    """Lex+parse a single expression and return its AST node."""
    from ast_builder import ASTBuilder
    parser = _make_parser(source)
    tree = parser.expression()
    return ASTBuilder().visit(tree)


