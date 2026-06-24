# ───────────────────────────────────────────────────────────────────────────
# src/semantic.py
# Static analysis pass: scope/arity checks and misplaced control-flow detection.
# Dynamically typed — no type checking here (type errors surface at runtime).
# ───────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import os, sys
from typing import Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from errors import SemanticError, MultiError, closest_name, to_arabic_digits
from ast_nodes import (
    ProgramNode, BlockNode, FunctionDefNode, SymbolDeclNode, AssignNode,
    AugAssignNode, IndexAssignNode, IfNode, WhileNode, ForEachNode, ForRangeNode,
    ReturnNode, BreakNode, ContinueNode, ExprStmtNode, BinOpNode, UnaryOpNode,
    CallNode, IndexNode, LambdaNode, IdentifierNode, IntLiteralNode,
    FloatLiteralNode, StringLiteralNode, FStringNode, BoolLiteralNode,
    NullLiteralNode, ListNode, TupleNode, PiNode, EulerNode, InfinityNode,
)


class SemanticAnalyser:
    """المحلل الدلالي / scope-and-arity analyser.

    Names are *hoisted* per scope (function bodies and the top level), so a
    function may legitimately reference itself (recursion) or another function
    defined later in the same scope without a false "undeclared" error. Blocks
    (إذا / بينما / لكل) do *not* introduce a new scope — matching the
    interpreter, where only function/lambda calls push a new frame.
    """

    def __init__(self, builtin_names=()):
        self.builtins = set(builtin_names)
        self.scopes: list[dict] = []   # each: name -> ('func', arity) | ('var', None)
        self.loop_depth = 0
        self.func_depth = 0
        self.errors: list = []

    # ── public API ──────────────────────────────────────────────
    def analyse(self, program: ProgramNode) -> ProgramNode:
        scope: dict = {}
        self._hoist(program.statements, scope)
        self.scopes.append(scope)
        for stmt in program.statements:
            self._safe_stmt(stmt)
        self.scopes.pop()
        if len(self.errors) == 1:
            raise self.errors[0]
        if self.errors:
            raise MultiError(self.errors)
        return program

    # ── one error per statement: collect & continue ─────────────
    def _safe_stmt(self, s):
        """حلّل جملةً واحدة، والتقط خطأها الدلالي (إن وُجد) لمتابعة بقية الجمل."""
        try:
            self._stmt(s)
        except SemanticError as exc:
            self.errors.append(exc)

    # ── hoisting ────────────────────────────────────────────────
    def _hoist(self, stmts, scope):
        for s in stmts:
            self._hoist_stmt(s, scope)

    def _hoist_stmt(self, s, scope):
        if isinstance(s, FunctionDefNode):
            scope[s.name] = ("func", len(s.params))
        elif isinstance(s, AssignNode):
            scope.setdefault(s.name, ("var", None))
        elif isinstance(s, AugAssignNode):
            scope.setdefault(s.name, ("var", None))
        elif isinstance(s, SymbolDeclNode):
            for n in s.names:
                scope[n] = ("var", None)
        elif isinstance(s, ForEachNode):
            scope.setdefault(s.var, ("var", None))
            self._hoist(s.body.statements, scope)
        elif isinstance(s, ForRangeNode):
            scope.setdefault(s.var, ("var", None))
            self._hoist(s.body.statements, scope)
        elif isinstance(s, WhileNode):
            self._hoist(s.body.statements, scope)
        elif isinstance(s, IfNode):
            for _, body in s.branches:
                self._hoist(body.statements, scope)
            if s.else_body is not None:
                self._hoist(s.else_body.statements, scope)

    # ── lookup helpers ───────────────────────────────────────────
    def _lookup(self, name) -> Optional[tuple]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        if name in self.builtins:
            return ("builtin", None)
        return None

    def _known_names(self) -> set:
        """كل الأسماء المرئية هنا (متغيرات + دوال + مدمجات) لاقتراحات «هل تقصد»."""
        names: set = set(self.builtins)
        for scope in self.scopes:
            names.update(scope.keys())
        return names

    def _require_declared(self, name, node=None):
        if self._lookup(name) is None:
            raise SemanticError(
                f"الاسم ‹{name}› غير معرّف (لا متغيّر ولا دالة)",
                line=getattr(node, "line", None), col=getattr(node, "col", None),
                suggestion=closest_name(name, self._known_names()),
                hint="ربّما هو خطأ إملائي، أو نسيت تعريفه أولاً.",
            )

    # ── statements ──────────────────────────────────────────────
    def _stmt(self, s):
        if isinstance(s, FunctionDefNode):
            self._function(s)
        elif isinstance(s, AssignNode):
            self._expr(s.value)
        elif isinstance(s, AugAssignNode):
            self._require_declared(s.name, s)
            self._expr(s.value)
        elif isinstance(s, IndexAssignNode):
            self._require_declared(s.target, s)
            for group in s.indices:        # CHANGED: one entry per bracket group
                self._expr(group)
            self._expr(s.value)
        elif isinstance(s, SymbolDeclNode):
            pass  # names already hoisted
        elif isinstance(s, IfNode):
            for cond, body in s.branches:
                self._expr(cond)
                for st in body.statements:
                    self._safe_stmt(st)
            if s.else_body is not None:
                for st in s.else_body.statements:
                    self._safe_stmt(st)
        elif isinstance(s, WhileNode):
            self._expr(s.condition)
            self.loop_depth += 1
            for st in s.body.statements:
                self._safe_stmt(st)
            self.loop_depth -= 1
        elif isinstance(s, ForEachNode):
            self._expr(s.iterable)
            self.loop_depth += 1
            for st in s.body.statements:
                self._safe_stmt(st)
            self.loop_depth -= 1
        elif isinstance(s, ForRangeNode):
            self._expr(s.start)
            self._expr(s.end)
            if s.step is not None:
                self._expr(s.step)
            self.loop_depth += 1
            for st in s.body.statements:
                self._safe_stmt(st)
            self.loop_depth -= 1
        elif isinstance(s, ReturnNode):
            if self.func_depth == 0:
                raise SemanticError(
                    "‹إرجع› تُستخدم داخل دالة فقط",
                    line=getattr(s, "line", None), col=getattr(s, "col", None),
                    hint="ضع جملة ‹إرجع› داخل جسم دالة.",
                )
            if s.value is not None:
                self._expr(s.value)
        elif isinstance(s, BreakNode):
            if self.loop_depth == 0:
                raise SemanticError(
                    "‹اوقف› تُستخدم داخل حلقة فقط",
                    line=getattr(s, "line", None), col=getattr(s, "col", None),
                    hint="‹اوقف› توقف حلقة ‹بينما› أو ‹لكل›.",
                )
        elif isinstance(s, ContinueNode):
            if self.loop_depth == 0:
                raise SemanticError(
                    "‹استمر› تُستخدم داخل حلقة فقط",
                    line=getattr(s, "line", None), col=getattr(s, "col", None),
                    hint="‹استمر› تتخطّى إلى الدورة التالية في الحلقة.",
                )
        elif isinstance(s, ExprStmtNode):
            self._expr(s.expr)
        # any other node type: nothing to check

    def _function(self, node: FunctionDefNode):
        scope: dict = {}
        for p in node.params:
            scope[p] = ("var", None)
        self._hoist(node.body.statements, scope)
        self.scopes.append(scope)
        self.func_depth += 1
        saved_loop = self.loop_depth
        self.loop_depth = 0  # اوقف/استمر cannot cross a function boundary
        for st in node.body.statements:
            self._safe_stmt(st)
        self.loop_depth = saved_loop
        self.func_depth -= 1
        self.scopes.pop()

    # ── expressions ─────────────────────────────────────────────
    def _expr(self, e):
        if isinstance(e, IdentifierNode):
            self._require_declared(e.name, e)
        elif isinstance(e, (IntLiteralNode, FloatLiteralNode, StringLiteralNode,
                            BoolLiteralNode, NullLiteralNode, PiNode, EulerNode,
                            InfinityNode)):
            return
        elif isinstance(e, FStringNode):
            # CHANGED: interpolated expressions are parsed at build time, so an
            # undefined name inside an f-string is caught here, not only at runtime.
            for kind, val in e.parts:
                if kind == "expr":
                    self._expr(val)
        elif isinstance(e, BinOpNode):
            self._expr(e.left)
            self._expr(e.right)
        elif isinstance(e, UnaryOpNode):
            self._expr(e.operand)
        elif isinstance(e, CallNode):
            self._expr(e.callee)
            for a in e.args:
                self._expr(a)
            for value in e.kwargs.values():
                self._expr(value)
            self._check_arity(e)
        elif isinstance(e, IndexNode):
            self._expr(e.target)
            self._expr(e.index)
        elif isinstance(e, LambdaNode):
            scope = {p: ("var", None) for p in e.params}
            self.scopes.append(scope)
            self._expr(e.body)
            self.scopes.pop()
        elif isinstance(e, (ListNode, TupleNode)):
            for el in e.elements:
                self._expr(el)
        # literals / unknown: nothing to do

    def _check_arity(self, call: CallNode):
        callee = call.callee
        if not isinstance(callee, IdentifierNode):
            return
        info = self._lookup(callee.name)
        if info is None:
            return
        kind, arity = info
        if kind == "func" and arity is not None:
            passed = len(call.args) + len(call.kwargs)
            if passed != arity:
                raise SemanticError(
                    f"الدالة ‹{callee.name}› تتوقّع {to_arabic_digits(arity)} وسيطًا "
                    f"لكن وصلها {to_arabic_digits(passed)}",
                    line=getattr(call, "line", None), col=getattr(call, "col", None),
                    hint="تحقّق من عدد الوسائط المُمرّرة للدالة.",
                )
            # annotate the call node with its resolved arity
            call.arity = arity  # type: ignore[attr-defined]


def analyse(program: ProgramNode, builtin_names=()) -> ProgramNode:
    """دالة مُيسّرة / convenience wrapper."""
    return SemanticAnalyser(builtin_names).analyse(program)
