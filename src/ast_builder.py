# ───────────────────────────────────────────────────────────────────────────
# src/ast_builder.py  (PROVIDED — do not change)
# CST → AST visitor: turns the ANTLR parse tree into ast_nodes dataclasses.
# ───────────────────────────────────────────────────────────────────────────
import sys, os
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "generated"))
sys.path.insert(0, os.path.join(_ROOT, "src"))

from HassoobArabiVisitor import HassoobArabiVisitor
from HassoobArabiParser  import HassoobArabiParser
from ast_nodes import *


class ASTBuilder(HassoobArabiVisitor):

    # ── Position tracking ────────────────────────────
    # CHANGED: stamp every AST node with its source line/column so semantic
    # and runtime errors can point at the exact spot. visit() runs for every
    # rule context; we copy ctx.start.line / ctx.start.column onto the node it
    # produced (plain attrs -> see ast_nodes._Positioned, equality unaffected).
    # line is 1-based; col is 0-based to match the parser path (errors.py adds
    # +1 when displaying the column).
    def visit(self, tree):
        node = super().visit(tree)
        start = getattr(tree, "start", None)
        if start is not None and getattr(node, "line", "_") is None:
            try:
                node.line = start.line
                node.col = start.column
            except Exception:
                pass
        return node

    # ── Helpers ───────────────────────────────────────────────────────────

    @staticmethod
    def _normalize_digits(text: str) -> str:
        mapping = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
        return text.replace("_", "").translate(mapping)

    @staticmethod
    def _process_string(raw: str) -> str:
        # CHANGED (#6): delegate to lang_utils.decode_escapes, which handles the
        # full ESCAPE_SEQ set (\uXXXX, \b, \f, \0, ...) in one safe pass
        # instead of a fragile ordered .replace() chain.
        q_idx = raw.index('"') if '"' in raw else raw.index("'")
        inner = raw[q_idx + 1: -1]
        from lang_utils import decode_escapes
        return decode_escapes(inner)

    def _build_left_chain(self, sub_exprs, op_tokens):
        result = self.visit(sub_exprs[0])
        for i, op_tok in enumerate(op_tokens):
            result = BinOpNode(left=result, op=op_tok.getText(), right=self.visit(sub_exprs[i + 1]))
        return result

    def _ops_from_children(self, ctx, n_sub):
        return [ctx.getChild(i) for i in range(1, ctx.getChildCount(), 2)]

    def _index_group(self, index_list_ctx):
        # CHANGED (#8): a single bracket group -> scalar index node; a comma
        # group a[i, j] -> TupleNode for N-D access.
        exprs = index_list_ctx.expression()
        if len(exprs) == 1:
            return self.visit(exprs[0])
        return TupleNode(elements=[self.visit(e) for e in exprs])

    def visitIndexList(self, ctx):
        return self._index_group(ctx)

    # ── Program & Block ────────────────────────────────────────────────

    def visitProgram(self, ctx):
        return ProgramNode(statements=[self.visit(s) for s in ctx.statement()])

    def visitBlock(self, ctx):
        return BlockNode(statements=[self.visit(s) for s in ctx.statement()])

    # ── Statement delegates (labeled alternatives) ────────────────────────

    def visitFunctionDefStmt(self, ctx):   return self.visit(ctx.functionDef())
    def visitIfStatement(self, ctx):       return self.visit(ctx.ifStmt())
    def visitWhileStatement(self, ctx):    return self.visit(ctx.whileStmt())
    def visitForEachStatement(self, ctx):  return self.visit(ctx.forEachStmt())
    def visitForRangeStatement(self, ctx): return self.visit(ctx.forRangeStmt())
    def visitReturnStatement(self, ctx):   return self.visit(ctx.returnStmt())
    def visitBreakStatement(self, ctx):    return self.visit(ctx.breakStmt())
    def visitContinueStatement(self, ctx): return self.visit(ctx.continueStmt())
    def visitSymbolDeclStatement(self, ctx): return self.visit(ctx.symbolDecl())
    def visitAssignStatement(self, ctx):   return self.visit(ctx.assignStmt())
    def visitAugAssignStatement(self, ctx): return self.visit(ctx.augAssignStmt())
    def visitIndexAssignStatement(self, ctx): return self.visit(ctx.indexAssignStmt())
    def visitExprStatement(self, ctx):     return self.visit(ctx.exprStmt())

    # ── Declarations ───────────────────────────────────────────────

    def visitFunctionDef(self, ctx):
        name   = ctx.IDENTIFIER().getText()
        params = [t.getText() for t in ctx.paramList().IDENTIFIER()] if ctx.paramList() else []
        return FunctionDefNode(name=name, params=params, body=self.visit(ctx.block()))

    def visitSymbolDecl(self, ctx):
        return SymbolDeclNode(names=[t.getText() for t in ctx.IDENTIFIER()])

    # ── Assignment ───────────────────────────────────────────────

    def visitAssignStmt(self, ctx):
        return AssignNode(name=ctx.IDENTIFIER().getText(), value=self.visit(ctx.expression()))

    def visitAugAssignStmt(self, ctx):
        return AugAssignNode(name=ctx.IDENTIFIER().getText(), op=ctx.augOp().getText(), value=self.visit(ctx.expression()))

    def visitIndexAssignStmt(self, ctx):
        # CHANGED (#8/#9): collect every bracket group so a[i][j] and a[i, j]
        # both work at any depth; the trailing expression is the RHS value.
        groups = [self._index_group(il) for il in ctx.indexList()]
        return IndexAssignNode(
            target=ctx.IDENTIFIER().getText(),
            indices=groups,
            value=self.visit(ctx.expression()),
        )

    def visitExprStmt(self, ctx):
        return ExprStmtNode(expr=self.visit(ctx.expression()))

    # ── Control flow ─────────────────────────────────────────────

    def visitIfStmt(self, ctx):
        branches = [(self.visit(ctx.expression()), self.visit(ctx.block()))]
        for clause in ctx.elseIfClause():
            branches.append((self.visit(clause.expression()), self.visit(clause.block())))
        else_body = self.visit(ctx.elseClause().block()) if ctx.elseClause() else None
        return IfNode(branches=branches, else_body=else_body)

    def visitWhileStmt(self, ctx):
        return WhileNode(condition=self.visit(ctx.expression()), body=self.visit(ctx.block()))

    def visitForEachStmt(self, ctx):
        return ForEachNode(var=ctx.IDENTIFIER().getText(), iterable=self.visit(ctx.expression()), body=self.visit(ctx.block()))

    def visitForRangeStmt(self, ctx):
        exprs = ctx.expression()
        return ForRangeNode(
            var=ctx.IDENTIFIER().getText(),
            start=self.visit(exprs[0]), end=self.visit(exprs[1]),
            step=self.visit(exprs[2]) if ctx.BKHUTWA() else None,
            body=self.visit(ctx.block()))

    def visitReturnStmt(self, ctx):
        return ReturnNode(value=self.visit(ctx.expression()) if ctx.expression() else None)

    def visitBreakStmt(self, ctx):    return BreakNode()
    def visitContinueStmt(self, ctx): return ContinueNode()

    # ── Expressions ──────────────────────────────────────────────

    def visitExpression(self, ctx):
        return self.visit(ctx.lambdaExpr()) if ctx.lambdaExpr() else self.visit(ctx.orExpr())

    def visitSingleParamLambda(self, ctx):
        return LambdaNode(params=[ctx.IDENTIFIER().getText()], body=self.visit(ctx.expression()))

    def visitMultiParamLambda(self, ctx):
        params = [t.getText() for t in ctx.paramList().IDENTIFIER()] if ctx.paramList() else []
        return LambdaNode(params=params, body=self.visit(ctx.expression()))

    def visitOrExpr(self, ctx):
        sub = ctx.andExpr()
        return self.visit(sub[0]) if len(sub) == 1 else self._build_left_chain(sub, ctx.OR())

    def visitAndExpr(self, ctx):
        sub = ctx.notExpr()
        return self.visit(sub[0]) if len(sub) == 1 else self._build_left_chain(sub, ctx.AND())

    def visitNotExpression(self, ctx):
        return UnaryOpNode(op="ليس", operand=self.visit(ctx.notExpr()))

    def visitPassThroughNot(self, ctx):     return self.visit(ctx.equalityExpr())

    def visitEqualityExpr(self, ctx):
        sub = ctx.relationalExpr()
        if len(sub) == 1:
            return self.visit(sub[0])
        from lang_utils import chain_comparisons   # CHANGED (#3)
        ops = [t.getText() for t in self._ops_from_children(ctx, len(sub))]
        return chain_comparisons([self.visit(x) for x in sub], ops)

    def visitRelationalExpr(self, ctx):
        sub = ctx.addExpr()
        if len(sub) == 1:
            return self.visit(sub[0])
        from lang_utils import chain_comparisons   # CHANGED (#3): a < b < c -> (a<b) and (b<c)
        ops = [t.getText() for t in self._ops_from_children(ctx, len(sub))]
        return chain_comparisons([self.visit(x) for x in sub], ops)

    def visitAddExpr(self, ctx):
        sub = ctx.mulExpr()
        return self.visit(sub[0]) if len(sub) == 1 else self._build_left_chain(sub, self._ops_from_children(ctx, len(sub)))

    def visitMulExpr(self, ctx):
        sub = ctx.unaryExpr()
        return self.visit(sub[0]) if len(sub) == 1 else self._build_left_chain(sub, self._ops_from_children(ctx, len(sub)))

    def visitUnaryMinus(self, ctx):      return UnaryOpNode(op="-", operand=self.visit(ctx.unaryExpr()))
    def visitUnaryPlus(self, ctx):       return self.visit(ctx.unaryExpr())
    def visitPassThroughUnary(self, ctx): return self.visit(ctx.powerExpr())

    def visitPowerExpr(self, ctx):
        base = self.visit(ctx.postfixExpr())
        return BinOpNode(left=base, op="^", right=self.visit(ctx.unaryExpr())) if ctx.CARET() else base

    def visitPostfixExpr(self, ctx):
        result   = self.visit(ctx.primary())
        children = list(ctx.children) if ctx.children else []
        if len(children) <= 1:
            return result
        i = 1
        while i < len(children):
            tok = children[i].getText()
            if tok == "(":
                i += 1
                args = []
                kwargs = {}
                if i < len(children) and children[i].getText() != ")":
                    args, kwargs = self.visit(children[i])
                    i += 1
                i += 1
                result = CallNode(callee=result, args=args, kwargs=kwargs)
            elif tok == "[":
                i += 1
                index_expr = self.visit(children[i])
                i += 2
                result = IndexNode(target=result, index=index_expr)
            else:
                i += 1
        return result

    # ── Primaries ────────────────────────────────────────────────

    def visitIntLiteral(self, ctx):
        return IntLiteralNode(value=int(self._normalize_digits(ctx.INTEGER_LIT().getText())))

    def visitFloatLiteral(self, ctx):
        return FloatLiteralNode(value=float(self._normalize_digits(ctx.FLOAT_LIT().getText())))

    def visitStringLiteral(self, ctx):
        return StringLiteralNode(value=self._process_string(ctx.STRING_LIT().getText()))

    def visitFStringLiteral(self, ctx):
        # CHANGED (#7): split template into literal/expr parts at build time and
        # parse each interpolation into a real AST node, so semantic analysis
        # sees the names and runtime no longer re-parses with a regex.
        inner = self._process_string(ctx.FSTRING_LIT().getText())
        from lang_utils import split_fstring
        from interpreter import parse_expression
        parts = []
        for kind, value in split_fstring(inner):
            if kind == "lit":
                parts.append(("lit", value))
            else:
                parts.append(("expr", parse_expression(value)))
        return FStringNode(raw=inner, parts=parts)

    def visitPiConstant(self, ctx):       return PiNode()
    def visitEulerConstant(self, ctx):    return EulerNode()
    def visitInfinityConstant(self, ctx): return InfinityNode()
    def visitTrueLiteral(self, ctx):      return BoolLiteralNode(value=True)
    def visitFalseLiteral(self, ctx):     return BoolLiteralNode(value=False)
    def visitNullLiteral(self, ctx):      return NullLiteralNode()

    def visitIdentifierExpr(self, ctx):
        return IdentifierNode(name=ctx.IDENTIFIER().getText())

    def visitListExpr(self, ctx):
        return self.visit(ctx.listLiteral())

    def visitListLiteral(self, ctx):
        return ListNode(elements=[self.visit(e) for e in ctx.expression()])

    def visitParenExpr(self, ctx):
        return self.visit(ctx.expression())

    def visitTupleLiteral(self, ctx):
        return TupleNode(elements=[self.visit(e) for e in ctx.expression()])

    def visitArgList(self, ctx):
        args = []
        kwargs = {}
        seen_kwarg = False
        expressions = iter(ctx.expression())
        i = 0
        while i < ctx.getChildCount():
            child = ctx.getChild(i)
            if child.getText() == ",":
                i += 1
                continue
            if i + 1 < ctx.getChildCount() and ctx.getChild(i + 1).getText() == "=":
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
