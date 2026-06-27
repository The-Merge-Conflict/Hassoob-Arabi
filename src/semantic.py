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

    # division-family operators whose right operand must be non-zero
    _DIV_OPS = ("/", "÷", "%")
    # sentinel: "this expression is not a statically-known constant"
    _NO_CONST = object()

    def __init__(self, builtin_names=()):
        self.builtins = set(builtin_names)
        self.scopes: list[dict] = []   # each: name -> ('func', arity) | ('var', None)
        self.loop_depth = 0
        self.func_depth = 0
        self.errors: list = []
        # cascade suppression: names already reported as undefined in the
        # CURRENT scope. Each undefined name is reported once per function (the
        # set is reset on entering each function body in _function), instead of
        # on every later use.
        self._reported_undeclared: set = set()

    # ── public API ──────────────────────────────────────────────
    def analyse(self, program: ProgramNode) -> ProgramNode:
        self._collect(program)
        if len(self.errors) == 1:
            raise self.errors[0]
        if self.errors:
            raise MultiError(self.errors)
        return program

    def _collect(self, program: ProgramNode) -> list:
        """Run the full analysis, gathering every error into self.errors
        WITHOUT raising. Shared by analyse() (which then raises) and the
        cross-phase recovery path (which merges these with the syntax errors)."""
        scope: dict = {}
        self._hoist(program.statements, scope)
        self.scopes.append(scope)
        for stmt in program.statements:
            self._safe_stmt(stmt)
        self.scopes.pop()
        return self.errors

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
        if self._lookup(name) is not None:
            return
        # cascade suppression: "one error per NAME, per scope".
        # Report each undefined name only ONCE. After the first report we treat
        # it as already-seen, so its every later use no longer spawns a fresh
        # duplicate error. This mirrors the "error-type poisoning" real compilers
        # use to avoid drowning the user in thousands of knock-on errors that all
        # share ONE root cause (a single typo, or a name we forgot to define).
        #
        # We deliberately do NOT lose the other occurrences: the problem LIST
        # stays short (one entry), while the IDE still underlines EVERY use of
        # the name in the editor (via `err.symbol` below, which
        # ide/diagnostics.build() expands into one underline span per
        # occurrence). So the user gets one clear, non-overwhelming message in
        # the list AND can still see every place that needs fixing.
        if name in self._reported_undeclared:
            return
        self._reported_undeclared.add(name)
        err = SemanticError(
            f"الاسم ‹{name}› غير معرّف (لا متغيّر ولا دالة)",
            line=getattr(node, "line", None), col=getattr(node, "col", None),
            suggestion=closest_name(name, self._known_names()),
            hint="ربّما هو خطأ إملائي، أو نسيت تعريفه أولاً، انظر للمتغيرات التي تظهر باللون الأحمر على الشاشة فهي غير معرفة بعد.",
        )
        # expose the offending identifier so a front-end (e.g. the IDE) can
        # underline EVERY occurrence of it while this error is still listed once.
        err.symbol = name  # type: ignore[attr-defined]
        raise err

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
            for group in s.indices:        # one entry per bracket group
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
                    "‹توقف› تُستخدم داخل حلقة فقط",
                    line=getattr(s, "line", None), col=getattr(s, "col", None),
                    hint="‹توقف› توقف حلقة ‹بينما› أو ‹لكل›.",
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
        self.loop_depth = 0  # توقف/استمر cannot cross a function boundary
        # per-scope cascade suppression (the GCC model): each undefined name is
        # reported once per function it appears in. Reset the already-reported
        # set on entering this body and restore the outer set on exit, so a typo
        # inside one function never silences the same name elsewhere, while many
        # uses within one body still collapse to a single error.
        saved_reported = self._reported_undeclared
        self._reported_undeclared = set()
        for st in node.body.statements:
            self._safe_stmt(st)
        self._reported_undeclared = saved_reported
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
            # interpolated expressions are parsed at build time, so an
            # undefined name inside an f-string is caught here, not only at runtime.
            for kind, val in e.parts:
                if kind == "expr":
                    self._expr(val)
        elif isinstance(e, BinOpNode):
            self._expr(e.left)
            self._expr(e.right)
            self._check_const_zero_division(e)
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

    # ── static constant checks ──────────────────────
    def _check_const_zero_division(self, node: BinOpNode):
        """Flag a guaranteed division-by-zero whose divisor is a compile-time
        constant — e.g. ٩ / ٠, or أ / ٠ once أ folds to a constant.

        When the divisor is a pure constant expression we already KNOW — without
        running anything — that this division can only ever fail. There is no
        input, branch or program state that could ever make ٩ / ٠ valid, so it
        is obvious at analysis time and does not need to reach runtime to be
        caught. Reporting it statically lets us point at the exact line/column
        and refuse to run a program that is provably broken, instead of waiting
        for the divide to be *reached* at runtime (it might sit in a rarely-taken
        branch, or never run on a given input, silently hiding the bug). This is
        exactly why real compilers reject a literal `1/0` at compile time.

        Only CONSTANT divisors are checked. Anything involving a variable, a
        call or any other dynamic value is deliberately LEFT TO RUNTIME: its
        value cannot be known statically, and we must never reject a program
        that could be perfectly valid (e.g. a divisor that is only 0 for some
        inputs). Static checks must have ZERO false positives."""
        if node.op not in self._DIV_OPS:
            return
        divisor = self._const_eval(node.right)
        if divisor is self._NO_CONST:
            return
        if divisor == 0:
            raise SemanticError(
                "القسمة على صفر",
                line=getattr(node, "line", None), col=getattr(node, "col", None),
                hint="المقسوم عليه ثابتٌ قيمته صفر، والقسمة على صفر غير معرّفة.",
            )

    def _const_eval(self, node):
        """Evaluate a PURELY constant numeric expression (int/float literals
        combined with + - * / ÷ % ^ and unary signs) and return its value, or
        self._NO_CONST if it is not such a constant or could not be evaluated
        (contains a variable, or evaluating it would itself raise). Booleans and
        symbolic constants are treated as NON-constant here on purpose, to avoid
        surprising static errors."""
        try:
            if isinstance(node, IntLiteralNode):
                return node.value
            if isinstance(node, FloatLiteralNode):
                return node.value
            if isinstance(node, UnaryOpNode):
                v = self._const_eval(node.operand)
                if v is self._NO_CONST:
                    return self._NO_CONST
                if node.op == "-":
                    return -v
                if node.op == "+":
                    return +v
                return self._NO_CONST
            if isinstance(node, BinOpNode):
                a = self._const_eval(node.left)
                if a is self._NO_CONST:
                    return self._NO_CONST
                b = self._const_eval(node.right)
                if b is self._NO_CONST:
                    return self._NO_CONST
                op = node.op
                if op == "+":
                    return a + b
                if op == "-":
                    return a - b
                if op == "*":
                    return a * b
                if op == "/":
                    return a / b
                if op == "÷":
                    return a // b
                if op == "%":
                    return a % b
                if op == "^":
                    return a ** b
                return self._NO_CONST
            return self._NO_CONST
        except (ZeroDivisionError, ValueError, OverflowError, TypeError):
            return self._NO_CONST


def analyse(program: ProgramNode, builtin_names=()) -> ProgramNode:
    """دالة مُيسّرة / convenience wrapper."""
    return SemanticAnalyser(builtin_names).analyse(program)


def collect_semantic_errors(program: ProgramNode, builtin_names=()) -> list:
    """Like analyse() but RETURNS the list of semantic errors instead of
    raising. Used by the cross-phase recovery path so syntax + semantic errors
    can be reported together in one MultiError."""
    analyser = SemanticAnalyser(builtin_names)
    analyser._collect(program)
    return list(analyser.errors)
