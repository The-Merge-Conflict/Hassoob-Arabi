# ───────────────────────────────────────────────────────────────────────────
# src/interpreter.py
# Tree-walking interpreter for حاسوب عربي — the heart of the back-end.
#
# Symbolic vs numeric: if either operand of an operation is a sympy.Basic the
# whole operation is delegated to sympy; otherwise native Python / NumPy is used.
# sympy is imported lazily so the numeric subset still runs without it installed.
# ───────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import os, sys, re, math
from dataclasses import dataclass
from typing import Any, List, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (os.path.join(_ROOT, "generated"), _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from errors import (
    HassoobError, HassoobRuntimeError, SemanticError, ReturnSignal, BreakSignal, ContinueSignal,
    closest_name, to_arabic_digits,
)
from environment import Environment
from _builtins_loader import BUILTINS, format_value
from ast_nodes import (
    ProgramNode, BlockNode, FunctionDefNode, SymbolDeclNode, AssignNode,
    AugAssignNode, IndexAssignNode, IfNode, WhileNode, ForEachNode, ForRangeNode,
    ReturnNode, BreakNode, ContinueNode, ExprStmtNode, BinOpNode, UnaryOpNode,
    CallNode, IndexNode, LambdaNode, IdentifierNode, IntLiteralNode,
    FloatLiteralNode, StringLiteralNode, FStringNode, BoolLiteralNode,
    NullLiteralNode, ListNode, TupleNode, PiNode, EulerNode, InfinityNode,
)

import numpy as np
from runtime_ops import (  # CHANGED: shared, unit-tested runtime helpers
    check_power, index_key as rt_index_key, nested_setitem, raise_binop_value_error,
)


# ══ optional sympy ═══════════════════════════════════════════
try:
    import sympy as _sp
    _HAS_SYMPY = True
    _SympyBasic = _sp.Basic
except ImportError:  # pragma: no cover - depends on environment
    _sp = None
    _HAS_SYMPY = False

    class _SympyBasic:  # sentinel: nothing is ever an instance of this
        pass


def _is_symbolic(x) -> bool:
    return _HAS_SYMPY and isinstance(x, _SympyBasic)


# ══ Arabic-only diagnostics helpers ═════════════════════════════════
import unicodedata as _ud

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


def _arabic_type_name(value) -> str:
    """اسم نوع القيمة بالعربية لرسائل الأخطاء (بدل أسماء بايثون)."""
    if isinstance(value, bool):
        return "قيمة منطقية"
    if _is_symbolic(value):
        return "تعبير رمزي"
    if isinstance(value, (int, float)):
        return "عدد"
    if isinstance(value, str):
        return "نص"
    if value is None:
        return "فارغ"
    if isinstance(value, np.ndarray):
        return "مصفوفة"
    if isinstance(value, (list, tuple)):
        return "قائمة"
    if isinstance(value, dict):
        return "قاموس"
    if callable(value):
        return "دالة"
    return "قيمة"


# ══ first-class function value ══════════════════════════════════
class Function:
    """قيمة دالة (درجة أولى) / a first-class user function or lambda.

    Instances are directly Python-callable so built-ins such as طبّق / صفّي /
    ارسم / جذر_عددي can invoke them like ordinary callables.
    """

    __slots__ = ("name", "params", "body", "env", "interp")

    def __init__(self, name, params, body, env, interp):
        self.name = name
        self.params = params
        self.body = body          # BlockNode (def) or an expression node (lambda)
        self.env = env            # defining environment (for closures)
        self.interp = interp

    def __call__(self, *args, **kwargs):
        return self.interp._call_user(self, list(args), dict(kwargs))

    def __repr__(self):
        label = self.name or "دالة مجهولة"
        joined = "، ".join(self.params)
        return f"<دالة {label}({joined})>"


class Interpreter:
    """المُفسّر / the tree-walking interpreter."""

    def __init__(self, repl_mode: bool = False):
        self.repl_mode = repl_mode
        self.global_env = Environment()
        for name, fn in BUILTINS.items():
            self.global_env.define_builtin(name, fn)
        self.last_value = None

    # ── public entry points ───────────────────────────────────────
    def run(self, program: ProgramNode, env: Optional[Environment] = None):
        env = env or self.global_env
        result = None
        for stmt in program.statements:
            result = self.execute(stmt, env)
        return result

    # ── dispatch ──────────────────────────────────────────────
    def execute(self, node, env: Environment):
        """Execute a statement (or evaluate an expression) and return its value."""
        method = getattr(self, "_x_" + type(node).__name__, None)
        if method is None:
            # Anything without a statement handler is treated as an expression.
            return self.evaluate(node, env)
        try:
            return method(node, env)
        except HassoobError as err:
            self._stamp(err, node)
            raise

    # ══ statements ═══════════════════════════════════════════
    def _x_ProgramNode(self, node, env):
        return self.run(node, env)

    def _exec_block(self, block: BlockNode, env: Environment):
        for stmt in block.statements:
            self.execute(stmt, env)

    def _x_BlockNode(self, node, env):
        self._exec_block(node, env)
        return None

    def _x_AssignNode(self, node, env):
        # CHANGED (#5): Mathematica-like scope. Mutate an existing binding up the
        # chain (so plain = updates an outer/global variable), otherwise define a
        # new binding in the current frame.
        value = self.evaluate(node.value, env)
        env.assign_or_define(node.name, value)
        return None

    def _x_AugAssignNode(self, node, env):
        current = env.get(node.name)
        rhs = self.evaluate(node.value, env)
        base_op = {
            "+=": "+", "-=": "-", "*=": "*", "/=": "/",
            "^=": "^", "%=": "%", "++=": "++",
        }.get(node.op)
        if base_op is None:
            raise HassoobRuntimeError(f"عامل إسناد غير معروف '{node.op}'")
        env.assign(node.name, self._binop(base_op, current, rhs))
        return None

    def _x_IndexAssignNode(self, node, env):
        # CHANGED (#8/#9): support a[i][j] and a[i, j] at any rank by descending
        # through every bracket group, then assigning into the final container.
        target = env.get(node.target)
        groups = [self.evaluate(g, env) for g in node.indices]
        value = self.evaluate(node.value, env)
        try:
            nested_setitem(target, groups, value)
        except (IndexError, KeyError):
            raise HassoobRuntimeError("الدليل خارج النطاق")
        except TypeError:
            raise HassoobRuntimeError("لا يمكن تعديل هذا النوع بالفهرسة")
        return None

    def _x_FunctionDefNode(self, node, env):
        fn = Function(node.name, list(node.params), node.body, env, self)
        env.set(node.name, fn)
        return None

    def _x_SymbolDeclNode(self, node, env):
        if not _HAS_SYMPY:
            raise HassoobRuntimeError(
                "تصريح الرموز (رمز) يحتاج إلى المكتبة sympy"
            )
        for name in node.names:
            env.set(name, _sp.Symbol(name))
        return None

    def _x_IfNode(self, node, env):
        for cond, body in node.branches:
            if self._truthy(self.evaluate(cond, env)):
                self._exec_block(body, env)
                return None
        if node.else_body is not None:
            self._exec_block(node.else_body, env)
        return None

    def _x_WhileNode(self, node, env):
        while self._truthy(self.evaluate(node.condition, env)):
            try:
                self._exec_block(node.body, env)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return None

    def _x_ForEachNode(self, node, env):
        iterable = self.evaluate(node.iterable, env)
        try:
            iterator = iter(iterable)
        except TypeError:
            raise HassoobRuntimeError("القيمة غير قابلة للتكرار في 'لكل ... في'")
        for item in iterator:
            env.set(node.var, item)
            try:
                self._exec_block(node.body, env)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return None

    def _x_ForRangeNode(self, node, env):
        start = self.evaluate(node.start, env)
        end = self.evaluate(node.end, env)
        step = self.evaluate(node.step, env) if node.step is not None else 1
        try:
            start_i, end_i, step_i = int(start), int(end), int(step)
        except (TypeError, ValueError):
            raise HassoobRuntimeError("حدود 'لكل ... من ... إلى' يجب أن تكون أعدادًا صحيحة")
        if step_i == 0:
            raise HassoobRuntimeError("الخطوة لا يمكن أن تكون صفرًا")
        # Inclusive of `end`, in either direction.
        rng = range(start_i, end_i + 1, step_i) if step_i > 0 else range(start_i, end_i - 1, step_i)
        for item in rng:
            env.set(node.var, item)
            try:
                self._exec_block(node.body, env)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return None

    def _x_ReturnNode(self, node, env):
        value = self.evaluate(node.value, env) if node.value is not None else None
        raise ReturnSignal(value)

    def _x_BreakNode(self, node, env):
        raise BreakSignal()

    def _x_ContinueNode(self, node, env):
        raise ContinueSignal()

    def _x_ExprStmtNode(self, node, env):
        value = self.evaluate(node.expr, env)
        self.last_value = value
        if self.repl_mode and value is not None and not isinstance(node.expr, NullLiteralNode):
            print(f"← {format_value(value)}")
        return value

    # ══ expressions ═════════════════════════════════════════
    @staticmethod
    def _stamp(err, node):
        # CHANGED: attach the current node's source position to a language
        # error that has none yet. The innermost evaluate/execute frame wins
        # (its node is the most specific), so outer frames leave it intact.
        if getattr(err, "line", None) is None:
            line = getattr(node, "line", None)
            if line is not None:
                err.line = line
                err.col = getattr(node, "col", None)

    def evaluate(self, node, env: Environment):
        method = getattr(self, "_e_" + type(node).__name__, None)
        if method is None:
            raise HassoobRuntimeError(f"لا يمكن تقييم العقدة {type(node).__name__}")
        try:
            return method(node, env)
        except HassoobError as err:
            self._stamp(err, node)
            raise

    def _e_IdentifierNode(self, node, env):
        return env.get(node.name)

    def _e_IntLiteralNode(self, node, env):   return node.value
    def _e_FloatLiteralNode(self, node, env): return node.value
    def _e_StringLiteralNode(self, node, env): return node.value
    def _e_BoolLiteralNode(self, node, env):  return node.value
    def _e_NullLiteralNode(self, node, env):  return None

    def _e_PiNode(self, node, env):
        return _sp.pi if _HAS_SYMPY else math.pi

    def _e_EulerNode(self, node, env):
        return _sp.E if _HAS_SYMPY else math.e

    def _e_InfinityNode(self, node, env):
        return _sp.oo if _HAS_SYMPY else math.inf

    def _e_FStringNode(self, node, env):
        # CHANGED (#7): evaluate the pre-parsed parts instead of re-parsing the
        # raw template with a regex at runtime.
        if not node.parts:
            return node.raw
        out = []
        for kind, value in node.parts:
            if kind == "lit":
                out.append(value)
            else:
                out.append(format_value(self.evaluate(value, env)))
        return "".join(out)

    def _e_ListNode(self, node, env):
        elements = [self.evaluate(e, env) for e in node.elements]
        return self._maybe_matrix(elements)

    def _e_TupleNode(self, node, env):
        return tuple(self.evaluate(e, env) for e in node.elements)

    def _e_BinOpNode(self, node, env):
        op = node.op
        # Logical operators short-circuit and must not pre-evaluate the RHS.
        if op in ("و", "&&"):
            left = self.evaluate(node.left, env)
            if not self._truthy(left):
                return left
            return self.evaluate(node.right, env)
        if op in ("أو", "||"):
            left = self.evaluate(node.left, env)
            if self._truthy(left):
                return left
            return self.evaluate(node.right, env)
        left = self.evaluate(node.left, env)
        right = self.evaluate(node.right, env)
        return self._binop(op, left, right)

    def _e_UnaryOpNode(self, node, env):
        operand = self.evaluate(node.operand, env)
        if node.op == "-":
            return -operand
        if node.op in ("ليس", "!"):
            return not self._truthy(operand)
        raise HassoobRuntimeError(f"عامل أحادي غير معروف '{node.op}'")

    def _e_CallNode(self, node, env):
        callee = self.evaluate(node.callee, env)
        args = [self.evaluate(a, env) for a in node.args]
        kwargs = {name: self.evaluate(value, env) for name, value in node.kwargs.items()}
        if not callable(callee):
            suggestion = None
            if isinstance(node.callee, IdentifierNode):
                suggestion = closest_name(node.callee.name, env._all_names())
            raise HassoobRuntimeError(
                "هذه القيمة ليست دالة، فلا يمكن نداؤها بالأقواس ()",
                suggestion=suggestion,
                hint="تأكّد أنك تنادي دالة مُعرّفة أو دالة مدمجة.",
            )
        try:
            return callee(*args, **kwargs)
        except (ReturnSignal, BreakSignal, ContinueSignal):
            raise
        except HassoobError:
            raise
        except ZeroDivisionError:
            raise HassoobRuntimeError("القسمة على صفر")
        except RecursionError:
            raise HassoobRuntimeError(
                "تجاوزت الاستدعاءات العمق المسموح (هل هناك تكرار لا يتوقّف؟)",
                hint="تأكّد أنّ كل استدعاء ذاتيّ للدالة يقترب من حالة التوقّف.",
            )
        except TypeError:
            raise HassoobRuntimeError(
                "الوسائط المُمرّرة إلى الدالة غير صحيحة في عددها أو نوعها",
                hint="راجِع عدد الوسائط وأنواعها المتوقّعة لهذه الدالة.",
            )
        except Exception:  # pragma: no cover - defensive
            raise HassoobRuntimeError(
                "تعذّر تنفيذ الدالة بسبب خطأ في القيم المُمرّرة إليها",
                hint="راجِع القيم التي مرّرتها إلى الدالة.",
            )

    def _e_IndexNode(self, node, env):
        target = self.evaluate(node.target, env)
        index = self.evaluate(node.index, env)
        try:
            return target[self._index_key(target, index)]
        except (IndexError, KeyError):
            raise HassoobRuntimeError("الدليل خارج النطاق")
        except TypeError:
            raise HassoobRuntimeError("لا يمكن فهرسة هذا النوع")

    def _e_LambdaNode(self, node, env):
        return Function(None, list(node.params), node.body, env, self)

    # ══ helpers ══════════════════════════════════════════════
    def _call_user(self, fn: "Function", args: List[Any], kwargs: Optional[dict[str, Any]] = None):
        kwargs = kwargs or {}
        params = list(fn.params)
        values = list(args)
        missing = object()
        label = fn.name or "دالة مجهولة"
        if len(values) > len(params):
            raise HassoobRuntimeError(
                f"الدالة ‹{label}› تتوقّع {to_arabic_digits(len(params))} وسيطًا "
                f"لكن وصلها {to_arabic_digits(len(values))}",
                hint="تحقّق من عدد الوسائط المُمرّرة للدالة.",
            )
        for name, value in kwargs.items():
            if name not in params:
                raise HassoobRuntimeError(f"الدالة '{label}' لا تملك وسيطًا باسم '{name}'")
            index = params.index(name)
            if index < len(values) and values[index] is not missing:
                raise HassoobRuntimeError(f"تم تمرير الوسيط '{name}' أكثر من مرة")
            while len(values) < index:
                values.append(missing)
            if index < len(values):
                values[index] = value
            else:
                values.append(value)
        if len(values) != len(params) or any(v is missing for v in values):
            raise HassoobRuntimeError(
                f"الدالة ‹{label}› تتوقّع {to_arabic_digits(len(params))} وسيطًا "
                f"لكن وصلها {to_arabic_digits(len(args) + len(kwargs))}",
                hint="تحقّق من عدد الوسائط المُمرّرة للدالة.",
            )
        local = Environment(parent=fn.env)
        for param, value in zip(params, values):
            local.set(param, value)
        if isinstance(fn.body, BlockNode):
            try:
                self._exec_block(fn.body, local)
            except ReturnSignal as ret:
                return ret.value
            return None
        # lambda: body is a single expression
        return self.evaluate(fn.body, local)

    def _binop(self, op, left, right):
        symbolic = _is_symbolic(left) or _is_symbolic(right)
        try:
            if op == "+":
                return left + right
            if op == "-":
                return left - right
            if op == "*":
                return left * right
            if op == "/":
                return left / right
            if op == "÷":
                return left // right
            if op == "%":
                return left % right
            if op == "^":
                if symbolic:
                    return _sp.Pow(left, right)
                check_power(left, right)   # CHANGED (#4): reject neg base ^ non-integer power
                return left ** right
            if op == "**":
                return np.matmul(np.asarray(left), np.asarray(right))
            if op == "++":
                return f"{format_value(left)}{format_value(right)}"
            if op == "==":
                return self._eq(left, right, symbolic)
            if op in ("!=", "≠"):
                eq = self._eq(left, right, symbolic)
                return (not eq) if isinstance(eq, bool) else _sp.Ne(left, right)
            if op == "<":
                return left < right
            if op == ">":
                return left > right
            if op in ("<=", "≤"):
                return left <= right
            if op in (">=", "≥"):
                return left >= right
        except ZeroDivisionError:
            raise HassoobRuntimeError("القسمة على صفر")
        except HassoobRuntimeError:
            raise
        except ValueError as exc:
            # CHANGED (#1/#2): numpy raises ValueError on shape/dimension mismatch;
            # translate it into a friendly Arabic message (always raises).
            raise_binop_value_error(op, left, right, exc)
        except TypeError:
            raise HassoobRuntimeError(
                f"لا يمكن تطبيق العملية ‹{op}› بين {_arabic_type_name(left)} "
                f"و{_arabic_type_name(right)}",
                hint="تأكّد أنّ نوعَي القيمتين متوافقان مع هذه العملية.",
            )
        raise HassoobRuntimeError(f"عامل ثنائي غير معروف '{op}'")

    def _eq(self, left, right, symbolic):
        if symbolic:
            result = _sp.Eq(left, right)
            if isinstance(result, bool):
                return result
            # sympy may return a BooleanAtom (S.true / S.false)
            if result in (_sp.true, _sp.false):
                return bool(result)
            return result
        try:
            return bool(left == right)
        except ValueError:
            # e.g. element-wise array comparison
            return np.array_equal(np.asarray(left), np.asarray(right))

    def _truthy(self, value) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if _is_symbolic(value):
            try:
                return bool(value)
            except TypeError:
                return True
        if isinstance(value, np.ndarray):
            return bool(value.size) and bool(value.any())
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, (str, list, tuple, dict)):
            return len(value) > 0
        return bool(value)

    def _index_key(self, target, index):
        # CHANGED: delegate to the shared, unit-tested helper.
        return rt_index_key(target, index)

    @staticmethod
    def _maybe_matrix(elements):
        if (elements and all(isinstance(e, list) for e in elements)
                and len({len(e) for e in elements}) == 1
                and all(isinstance(x, (int, float)) and not isinstance(x, bool)
                        for row in elements for x in row)):
            return np.array(elements)
        return elements

    # ── f-string interpolation ──────────────────────────────────────
    # CHANGED (#7): f-strings are parsed into parts at build time (see
    # ast_builder.visitFStringLiteral) and evaluated in _e_FStringNode, so the
    # old runtime regex re-parser (_FSTRING_RE / _eval_fstring) was removed.


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


def run_source(source: str, repl_mode: bool = False, interp: Optional[Interpreter] = None,
               env: Optional[Environment] = None):
    """Full pipeline: parse → optimise → analyse → interpret a source string."""
    from optimizer import optimize
    from semantic import analyse
    interp = interp or Interpreter(repl_mode=repl_mode)
    program = parse_program(source)
    program = optimize(program)
    analyse(program, builtin_names=list(BUILTINS.keys()))
    return interp.run(program, env or interp.global_env)
