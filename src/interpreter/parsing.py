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
from ast_nodes import ProgramNode, BlockNode, ErrorNode


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
# translate them into calm Arabic with a helpful hint instead.

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
    "DALA": "دالة", "IRJA": "إرجع", "AWQIF": "توقف", "ISTAMIRR": "استمر",
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


class _CollectingErrorListener:
    """ANTLR error listener that *collects* syntax errors (as cute Arabic
    LexError / ParseError instances) into a shared list instead of raising on
    the first one. Combined with ANTLR's default error-recovery this lets us
    report every syntax error in a single run (choice B)."""

    def __init__(self, error_cls, sink, is_lexer=False):
        self._error_cls = error_cls
        self._sink = sink
        self._is_lexer = is_lexer

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        try:
            message, hint = _friendly_syntax_error(
                recognizer, offendingSymbol, line, column, msg, self._is_lexer)
        except Exception:
            message, hint = msg, None
        self._sink.append(self._error_cls(message, line=line, col=column, hint=hint))

    # The remaining ANTLR ErrorListener hooks are no-ops for our purposes.
    def reportAmbiguity(self, *a, **k):  # pragma: no cover
        pass

    def reportAttemptingFullContext(self, *a, **k):  # pragma: no cover
        pass

    def reportContextSensitivity(self, *a, **k):  # pragma: no cover
        pass


def _make_parser(source: str, error_sink=None):
    from antlr4 import InputStream, CommonTokenStream
    from HassoobArabiLexer import HassoobArabiLexer
    from HassoobArabiParser import HassoobArabiParser
    from errors import LexError, ParseError

    source = _strip_tashkeel(source)   # ignore harakat/tatweel outside strings
    input_stream = InputStream(source)
    lexer = HassoobArabiLexer(input_stream)
    lexer.removeErrorListeners()
    if error_sink is None:
        # fail-fast: raise on the first lexical/syntax error (parse_expression).
        lexer.addErrorListener(_RaisingErrorListener(LexError, is_lexer=True))
        tokens = CommonTokenStream(lexer)
        parser = HassoobArabiParser(tokens)
        parser.removeErrorListeners()
        parser.addErrorListener(_RaisingErrorListener(ParseError, is_lexer=False))
    else:
        # collect-all: gather every error into error_sink and let ANTLR's
        # default error-recovery keep parsing so we can report them together.
        lexer.addErrorListener(_CollectingErrorListener(LexError, error_sink, is_lexer=True))
        tokens = CommonTokenStream(lexer)
        parser = HassoobArabiParser(tokens)
        parser.removeErrorListeners()
        parser.addErrorListener(_CollectingErrorListener(ParseError, error_sink, is_lexer=False))
    return parser


def parse_program(source: str) -> ProgramNode:
    """Lex+parse a whole program and return its AST (ProgramNode)."""
    from ast_builder import ASTBuilder
    parser = _make_parser(source)
    tree = parser.program()
    return ASTBuilder().visit(tree)


def _arg_list_with_arabic_comma(self, ctx):
    
    args = []
    kwargs = {}
    seen_kwarg = False
    expressions = iter(ctx.expression())
    i = 0
    n = ctx.getChildCount()
    while i < n:
        child = ctx.getChild(i)
        if child.getText() in (",", "،"):      # ASCII or Arabic comma
            i += 1
            continue
        if i + 1 < n and ctx.getChild(i + 1).getText() == "=":
            seen_kwarg = True
            kwargs[child.getText()] = self.visit(next(expressions))
            i += 3
        else:
            if seen_kwarg:
                from errors import ParseError
                raise ParseError("positional argument follows named argument")
            args.append(self.visit(next(expressions)))
            i += 1
    return args, kwargs


# ── f-string interpolation position ───────────────────────
# WHY THIS EXISTS:
# An f-string such as  ف"القيمة {ص ++ }"  is built by parsing every {interpolation}
# as its OWN tiny program through parse_expression(). That fragment is handed to
# a fresh ANTLR InputStream that starts counting at line 1, column 0 — so a
# syntax error inside the interpolation used to be reported at "line 1" RELATIVE
# TO THE FRAGMENT, never at the real place of the f-string in the user's file.

def _fstring_interp_positions(raw_token, base_line, base_col):
    """Absolute (line, col) of the FIRST expression character of every
    {interpolation} in an f-string token, in source coordinates.

    Mirrors split_fstring's brace handling: '{{' is a literal brace, braces
    nest, and the leading whitespace that split_fstring's .strip() removes is
    skipped so the reported column lands on the first real character of the
    expression. All columns are 0-based (the error formatter adds +1 on show).
    """
    q = raw_token.find('"')
    if q == -1:
        q = raw_token.find("'")
    if q == -1:
        return []
    inner = raw_token[q + 1:-1]            # text between the quotes
    line = base_line
    col = base_col + q + 1                 # source position of inner[0]

    def adv(ch, line, col):
        # advance one source character, tracking newlines (an f-string may span
        # several lines; the column resets to 0 after a literal newline).
        if ch == "\n":
            return line + 1, 0
        return line, col + 1

    positions = []
    i, n = 0, len(inner)
    while i < n:
        ch = inner[i]
        if ch == "{":
            if i + 1 < n and inner[i + 1] == "{":      # '{{' -> literal '{'
                line, col = adv(ch, line, col)
                line, col = adv(inner[i + 1], line, col)
                i += 2
                continue
            line, col = adv(ch, line, col)             # step past the '{'
            i += 1
            while i < n and inner[i] in " \t":         # skip stripped whitespace
                line, col = adv(inner[i], line, col)
                i += 1
            positions.append((line, col))
            depth = 1                                  # skip to the matching '}'
            while i < n and depth > 0:
                c = inner[i]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        line, col = adv(c, line, col)
                        i += 1
                        break
                line, col = adv(c, line, col)
                i += 1
            continue
        line, col = adv(ch, line, col)
        i += 1
    return positions


def _rebase_fstring_error(exc, pos):
    """Move a parse error from fragment-local coordinates (where line 1 is the
    start of the interpolation fragment) to the absolute source position *pos*
    of that interpolation, so the message points at the real line/column."""
    start_line, start_col = pos
    inner_line = getattr(exc, "line", None)
    inner_col = getattr(exc, "col", None)
    if inner_line is None or inner_line <= 1:
        
        exc.line = start_line
        exc.col = start_col + (inner_col or 0)
    else:
        
        exc.line = start_line + (inner_line - 1)
        exc.col = inner_col if inner_col is not None else 0


def _patched_builder_class():
    from ast_builder import ASTBuilder
    from ast_nodes import FStringNode

    class _PatchedASTBuilder(ASTBuilder):
        visitArgList = _arg_list_with_arabic_comma

        def visitFStringLiteral(self, ctx):
            # wraps each per-interpolation parse_expression() call so a failure
            # is rebased onto the f-string's real source coordinates (see
            # _fstring_interp_positions / _rebase_fstring_error above). When
            # nothing fails, the behaviour is identical to the provided builder.
            from lang_utils import split_fstring
            from interpreter import parse_expression
            from errors import HassoobError

            token = ctx.FSTRING_LIT().getSymbol()
            raw_token = token.text
            base_line = getattr(token, "line", 1) or 1
            base_col = getattr(token, "column", 0) or 0

            inner = self._process_string(ctx.FSTRING_LIT().getText())
            positions = _fstring_interp_positions(raw_token, base_line, base_col)

            try:
                parts = []
                k = 0
                for kind, value in split_fstring(inner):
                    if kind == "lit":
                        parts.append(("lit", value))
                        continue
                    pos = positions[k] if k < len(positions) else (base_line, base_col)
                    k += 1
                    try:
                        node = parse_expression(value)
                    except HassoobError as exc:
                        _rebase_fstring_error(exc, pos)
                        raise
                    parts.append(("expr", node))
                return FStringNode(raw=inner, parts=parts)
            except HassoobError as exc:
                # split_fstring's own errors (e.g. an unbalanced '{') carry no
                # position; at least anchor them to the f-string's own line so
                # the report never falls back to a misleading "line 1".
                if getattr(exc, "line", None) is None:
                    exc.line = base_line
                    exc.col = base_col
                raise

    return _PatchedASTBuilder


def _recovering_builder():
    """Build an ASTBuilder subclass that tolerates a partially-broken parse
    tree: any statement that fails to build becomes an ErrorNode, so the rest
    of the program can still be built and analysed (cross-phase
    recovery via error nodes). Build-time HassoobErrors are captured rather than lost."""
    base = _patched_builder_class()
    from errors import HassoobError

    class _RecoveringASTBuilder(base):
        def __init__(self):
            super().__init__()
            self.build_errors = []

        @staticmethod
        def _error_node_for(ctx):
            node = ErrorNode()
            start = getattr(ctx, "start", None)
            if start is not None:
                try:
                    node.line = start.line
                    node.col = start.column
                except Exception:
                    pass
            return node

        def _safe_statements(self, ctx):
            out = []
            for s in ctx.statement():
                try:
                    node = self.visit(s)
                except HassoobError as exc:
                    # A language-level build error (e.g. a malformed f-string
                    # interpolation): record it and substitute an inert
                    # ErrorNode so the rest of the program is still built and
                    # analysed.
                    self.build_errors.append(exc)
                    node = self._error_node_for(s)
                if node is not None:
                    out.append(node)
            return out

        def visitProgram(self, ctx):
            return ProgramNode(statements=self._safe_statements(ctx))

        def visitBlock(self, ctx):
            return BlockNode(statements=self._safe_statements(ctx))

    return _RecoveringASTBuilder()


def parse_program_collecting(source: str):
    """Lex+parse a whole program, COLLECTING every syntax error instead of
    stopping at the first. Returns (program, syntax_errors).

    The returned ProgramNode may contain ErrorNode placeholders where a
    statement could not be built, so the caller can still run the semantic
    phase over everything that *did* parse."""
    syntax_errors: list = []
    parser = _make_parser(source, error_sink=syntax_errors)
    tree = parser.program()
    builder = _recovering_builder()
    program = builder.visit(tree)
    errors = list(syntax_errors) + list(builder.build_errors)
    _BIG = 1 << 30
    errors.sort(key=lambda e: (e.line if e.line is not None else _BIG,
                               e.col if e.col is not None else _BIG))
    return program, errors


def parse_expression(source: str):
    """Lex+parse a single expression and return its AST node.

    Anchored to EOF: parser.expression() does NOT consume trailing tokens, so
    an input that ends with a dangling operator would parse only its leading
    part and silently drop the rest. We require the whole fragment to be
    consumed, raising a friendly ParseError otherwise. This closes a soundness
    hole and makes malformed f-string interpolations fail loudly instead of
    silently dropping part of the expression."""
    from antlr4 import Token
    from errors import ParseError
    parser = _make_parser(source)
    tree = parser.expression()
    tok = parser.getCurrentToken()
    if tok is not None and tok.type != Token.EOF:
        raise ParseError(
            "تركيب غير مفهوم قرب ‹%s›" % tok.text,
            line=getattr(tok, "line", None), col=getattr(tok, "column", None),
            hint="تأكّد من اكتمال التعبير ومن عدم وجود رمز زائد.",
        )
    return _patched_builder_class()().visit(tree)


