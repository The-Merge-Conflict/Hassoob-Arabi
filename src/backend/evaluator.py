# ---------------------------------------------------------------------------
# src/interpreter/evaluator.py
# Tree-walking evaluator: the first-class Function value and the Interpreter
# class (statement execution + expression evaluation + runtime helpers).
# ---------------------------------------------------------------------------
from __future__ import annotations
# -- source-path bootstrap ---------------------------------------------------
# Hassoob's modules refer to one another by short name (e.g. ``from errors
# import ...``). Register the source root plus every compiler-phase folder so
# those names resolve no matter which module Python imports first.
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "src" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d and _d not in _sys.path:
    _sys.path.insert(0, _d)
import _pathsetup  # noqa: F401,E402  (registers all phase roots on sys.path)

import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
_ROOT = os.path.dirname(_SRC)
for _p in (os.path.join(_ROOT, 'generated'), _SRC):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import math
from typing import Any, List, Optional

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
        # Mathematica-like scope. Mutate an existing binding up the
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
        # support a[i][j] and a[i, j] at any rank by descending
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
        #  attach the current node's source position to a language
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
        # evaluate the pre-parsed parts instead of re-parsing the
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
                check_power(left, right)   # reject neg base ^ non-integer power
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
            # numpy raises ValueError on shape/dimension mismatch;
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
        # delegate to the shared, unit-tested helper.
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
    # f-strings are parsed into parts at build time (see
    # ast_builder.visitFStringLiteral) and evaluated in _e_FStringNode.


