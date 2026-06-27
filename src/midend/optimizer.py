# ───────────────────────────────────────────────────────────────────────────
# src/optimizer.py
# Pure AST → AST optimiser. Never mutates a node; only returns new ones. Applies
# constant folding, algebraic identities, short-circuit folding, dead-code
# elimination and strength reduction, iterating to a fixed point.
# ───────────────────────────────────────────────────────────────────────────
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
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from ast_nodes import (
    ProgramNode, BlockNode, FunctionDefNode, SymbolDeclNode, AssignNode,
    AugAssignNode, IndexAssignNode, IfNode, WhileNode, ForEachNode, ForRangeNode,
    ReturnNode, BreakNode, ContinueNode, ExprStmtNode, BinOpNode, UnaryOpNode,
    CallNode, IndexNode, LambdaNode, IdentifierNode, IntLiteralNode,
    FloatLiteralNode, StringLiteralNode, FStringNode, BoolLiteralNode,
    NullLiteralNode, ListNode, TupleNode, PiNode, EulerNode, InfinityNode,
)

# Operator groups -------------------------------------------------------------
_NUMERIC_FOLDABLE = {"+", "-", "*", "/", "÷", "%", "^"}
_COMPARISON = {"==", "!=", "≠", "<", ">", "<=", ">=", "≤", "≥"}
_AND_OPS = {"و", "&&"}
_OR_OPS = {"أو", "||"}
_SIDE_EFFECT_FREE = (
    IdentifierNode, IntLiteralNode, FloatLiteralNode, BoolLiteralNode,
    StringLiteralNode, PiNode, EulerNode, InfinityNode,
)


class Optimizer:
    """محسّن الشجرة المجرّدة / a pure AST optimiser."""

    # ── public entry point ──────────────────────────────────────────
    def optimize(self, program: ProgramNode) -> ProgramNode:
        """Optimise ``program`` repeatedly until it stops changing."""
        current = program
        for _ in range(1000):  # generous guard against pathological non-convergence
            nxt = self._opt(current)
            if nxt == current:
                return nxt
            current = nxt
        return current

    # ── dispatch ──────────────────────────────────────────────────
    def _opt(self, node):
        if node is None:
            return None
        method = getattr(self, "_opt_" + type(node).__name__, None)
        if method is None:
            return node
        return self._carry_pos(node, method(node))

    @staticmethod
    def _carry_pos(src, dst):
        """انسخ السطر/العمود من العقدة الأصلية إلى المعاد بناؤها.

        The optimiser builds fresh nodes, which start with line/col = None.
        Copy the source position onto any rebuilt node that lacks one so a
        later semantic/runtime error can still point at the original spot.
        """
        if dst is not None and dst is not src and getattr(dst, "line", None) is None:
            src_line = getattr(src, "line", None)
            if src_line is not None:
                dst.line = src_line
                dst.col = getattr(src, "col", None)
        return dst

    def _opt_block(self, node: BlockNode) -> BlockNode:
        return BlockNode(statements=self._opt_stmts(node.statements))

    # ── statement-list handling (dead-code elimination lives here) ─────────────
    def _opt_stmts(self, stmts):
        out = []
        for s in stmts:
            optimised = self._opt(s)
            for piece in self._expand_stmt(optimised):
                out.append(piece)
                # Statements after a terminator are unreachable → drop the rest.
                if isinstance(piece, (ReturnNode, BreakNode, ContinueNode)):
                    return out
        return out

    def _expand_stmt(self, stmt):
        """Turn one optimised statement into 0+ statements (for DCE / inlining)."""
        if isinstance(stmt, IfNode):
            return self._reduce_if(stmt)
        if isinstance(stmt, WhileNode) and self._is_false(stmt.condition):
            return []  # بينما (خطأ) { ... } → removed entirely
        if stmt is None:
            return []
        return [stmt]

    def _reduce_if(self, node: IfNode):
        """Apply dead-code elimination to an already-optimised IfNode."""
        live_branches = []
        for cond, body in node.branches:
            if self._is_false(cond):
                continue  # branch can never run → drop it
            if self._is_true(cond):
                if not live_branches:
                    # Unconditionally taken → inline its (already optimised) body.
                    return list(body.statements)
                # Preceding live branches exist; this one becomes the final else.
                live_branches.append((cond, body))
                return [IfNode(branches=live_branches, else_body=None)]
            live_branches.append((cond, body))
        if not live_branches:
            if node.else_body is not None:
                return list(node.else_body.statements)
            return []
        return [IfNode(branches=live_branches, else_body=node.else_body)]

    # ── structural nodes ───────────────────────────────────────────
    def _opt_ProgramNode(self, node):
        return ProgramNode(statements=self._opt_stmts(node.statements))

    def _opt_BlockNode(self, node):
        return self._opt_block(node)

    def _opt_FunctionDefNode(self, node):
        return FunctionDefNode(name=node.name, params=list(node.params),
                               body=self._opt_block(node.body))

    def _opt_AssignNode(self, node):
        return AssignNode(name=node.name, value=self._opt(node.value))

    def _opt_AugAssignNode(self, node):
        return AugAssignNode(name=node.name, op=node.op, value=self._opt(node.value))

    def _opt_IndexAssignNode(self, node):
        return IndexAssignNode(target=node.target,
                               indices=[self._opt(g) for g in node.indices],
                               value=self._opt(node.value))

    def _opt_IfNode(self, node):
        branches = [(self._opt(c), self._opt_block(b)) for c, b in node.branches]
        else_body = self._opt_block(node.else_body) if node.else_body is not None else None
        return IfNode(branches=branches, else_body=else_body)

    def _opt_WhileNode(self, node):
        return WhileNode(condition=self._opt(node.condition), body=self._opt_block(node.body))

    def _opt_ForEachNode(self, node):
        return ForEachNode(var=node.var, iterable=self._opt(node.iterable),
                           body=self._opt_block(node.body))

    def _opt_ForRangeNode(self, node):
        return ForRangeNode(var=node.var, start=self._opt(node.start),
                            end=self._opt(node.end),
                            step=self._opt(node.step) if node.step is not None else None,
                            body=self._opt_block(node.body))

    def _opt_ReturnNode(self, node):
        return ReturnNode(value=self._opt(node.value) if node.value is not None else None)

    def _opt_ExprStmtNode(self, node):
        return ExprStmtNode(expr=self._opt(node.expr))

    def _opt_CallNode(self, node):
        return CallNode(
            callee=self._opt(node.callee),
            args=[self._opt(a) for a in node.args],
            kwargs={name: self._opt(value) for name, value in node.kwargs.items()},
        )

    def _opt_IndexNode(self, node):
        return IndexNode(target=self._opt(node.target), index=self._opt(node.index))

    def _opt_LambdaNode(self, node):
        return LambdaNode(params=list(node.params), body=self._opt(node.body))

    def _opt_ListNode(self, node):
        return ListNode(elements=[self._opt(e) for e in node.elements])

    def _opt_TupleNode(self, node):
        return TupleNode(elements=[self._opt(e) for e in node.elements])

    # ── binary operators ───────────────────────────────────────────
    def _opt_BinOpNode(self, node):
        left = self._opt(node.left)
        right = self._opt(node.right)
        op = node.op

        # 1) short-circuit folding (must run before generic folding) -----------
        if op in _OR_OPS:
            if self._is_true(left):
                return BoolLiteralNode(True)
            if self._is_false(left):
                return right
        elif op in _AND_OPS:
            if self._is_false(left):
                return BoolLiteralNode(False)
            if self._is_true(left):
                return right

        # 2) constant folding --------------------------------------------------
        folded = self._fold(op, left, right)
        if folded is not None:
            return folded

        # 3) algebraic identities ---------------------------------------------
        identity = self._identity(op, left, right)
        if identity is not None:
            return identity

        # 4) strength reduction -----------------------------------------------
        reduced = self._strength_reduce(op, left, right)
        if reduced is not None:
            return reduced

        return BinOpNode(left=left, op=op, right=right)

    def _opt_UnaryOpNode(self, node):
        operand = self._opt(node.operand)
        op = node.op
        if op == "-":
            if isinstance(operand, (IntLiteralNode, FloatLiteralNode)):
                return self._make_lit(-operand.value)
            if isinstance(operand, UnaryOpNode) and operand.op == "-":
                return operand.operand              # -(-x) → x
        elif op in ("ليس", "!"):
            if isinstance(operand, BoolLiteralNode):
                return BoolLiteralNode(not operand.value)
            if isinstance(operand, UnaryOpNode) and operand.op in ("ليس", "!"):
                return operand.operand              # not(not(x)) → x
        return UnaryOpNode(op=op, operand=operand)

    # ── folding helpers ────────────────────────────────────────────
    def _fold(self, op, left, right):
        # string concatenation folding
        if isinstance(left, StringLiteralNode) and isinstance(right, StringLiteralNode) and op in ("+", "++"):
            return StringLiteralNode(left.value + right.value)

        if not (self._is_num_lit(left) and self._is_num_lit(right)):
            return None
        a, b = self._lit_value(left), self._lit_value(right)
        try:
            if op == "+":   r = a + b
            elif op == "-": r = a - b
            elif op == "*": r = a * b
            elif op == "/": r = a / b
            elif op == "÷": r = a // b
            elif op == "%": r = a % b
            elif op == "^": r = a ** b
            elif op in _COMPARISON: r = self._compare(op, a, b)
            else:
                return None  # '**' (matmul) and '++' on numbers are not folded
        except (ZeroDivisionError, ValueError, OverflowError, TypeError):
            # Never fold an operation that itself raises; return None so the
            # original node survives and the proper friendly Arabic error is
            # produced at the right phase instead of crashing the optimiser.
            #
            # On division-by-zero specifically: a CONSTANT divisor of zero
            # (e.g. ٩ / ٠) is already rejected by the SEMANTIC phase, which runs
            # BEFORE the optimiser (see pipeline.compile_program: analyse →
            # optimise). So a constant x / 0 can never reach this point; this
            # guard therefore defers only genuinely dynamic arithmetic edge
            # cases (overflow, bad operand types, …) to runtime.
            return None
        # negative base ^ non-integer power yields a complex number: do NOT fold
        # it to a literal (would crash _make_lit) — defer to runtime so it raises a
        # friendly Arabic error via check_power.
        if isinstance(r, complex):
            return None
        return self._make_lit(r)

    @staticmethod
    def _compare(op, a, b):
        if op == "==":           return a == b
        if op in ("!=", "≠"):    return a != b
        if op == "<":            return a < b
        if op == ">":            return a > b
        if op in ("<=", "≤"):    return a <= b
        if op in (">=", "≥"):    return a >= b
        return None

    def _identity(self, op, left, right):
        l_zero, r_zero = self._is_zero(left), self._is_zero(right)
        l_one, r_one = self._is_one(left), self._is_one(right)
        if op == "+":
            if r_zero: return left
            if l_zero: return right
        elif op == "-":
            if r_zero: return left
        elif op == "*":
            if r_one: return left
            if l_one: return right
            # x * 0 → 0 only when the dropped operand is side-effect-free, so we
            # never silently discard a call like اطبع("مرحبا") * ٠.
            if r_zero and isinstance(left, _SIDE_EFFECT_FREE):
                return IntLiteralNode(0)
            if l_zero and isinstance(right, _SIDE_EFFECT_FREE):
                return IntLiteralNode(0)
        elif op == "/":
            # Division is intentionally NOT simplified by an identity rule.
            # Folding 0 / x → 0 would be WRONG: x may be 0 at runtime and that
            # case must still raise a division-by-zero error, not be silently
            # optimised away. (A constant c / 0 is caught even earlier, as a
            # static SEMANTIC error — see semantic._check_const_zero_division —
            # so the optimiser never has to reason about constant zero divisors.)
            pass
        elif op == "^":
            if r_one: return left                              # x ^ 1 → x
            if r_zero: return IntLiteralNode(1)                # x ^ 0 → 1
        return None

    def _strength_reduce(self, op, left, right):
        if op != "^" or not isinstance(left, _SIDE_EFFECT_FREE):
            return None
        if isinstance(right, IntLiteralNode):
            if right.value == 2:
                return BinOpNode(left=left, op="*", right=left)            # x^2 → x*x
            if right.value == 3:
                return BinOpNode(left=BinOpNode(left=left, op="*", right=left),
                                 op="*", right=left)                       # x^3 → x*x*x
        return None

    # ── literal predicates ──────────────────────────────────────────
    @staticmethod
    def _is_num_lit(node):
        return isinstance(node, (IntLiteralNode, FloatLiteralNode, BoolLiteralNode))

    @staticmethod
    def _lit_value(node):
        return node.value

    @staticmethod
    def _is_zero(node):
        return isinstance(node, (IntLiteralNode, FloatLiteralNode)) and node.value == 0

    @staticmethod
    def _is_one(node):
        return isinstance(node, (IntLiteralNode, FloatLiteralNode)) and node.value == 1

    @staticmethod
    def _is_true(node):
        return isinstance(node, BoolLiteralNode) and node.value is True

    @staticmethod
    def _is_false(node):
        return isinstance(node, BoolLiteralNode) and node.value is False

    @staticmethod
    def _make_lit(value):
        # bool must be checked before int (bool is a subclass of int).
        if isinstance(value, bool):
            return BoolLiteralNode(value)
        if isinstance(value, int):
            return IntLiteralNode(value)
        if isinstance(value, float):
            return FloatLiteralNode(value)
        if isinstance(value, str):
            return StringLiteralNode(value)
        raise TypeError(f"cannot build a literal node for {value!r}")


def optimize(program: ProgramNode) -> ProgramNode:
    """دالة مُيسّرة / convenience wrapper around :class:`Optimizer`."""
    return Optimizer().optimize(program)
