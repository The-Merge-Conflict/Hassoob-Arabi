# Generated from HassoobArabi.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .HassoobArabiParser import HassoobArabiParser
else:
    from HassoobArabiParser import HassoobArabiParser

# This class defines a complete generic visitor for a parse tree produced by HassoobArabiParser.

class HassoobArabiVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HassoobArabiParser#program.
    def visitProgram(self, ctx:HassoobArabiParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#FunctionDefStmt.
    def visitFunctionDefStmt(self, ctx:HassoobArabiParser.FunctionDefStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#IfStatement.
    def visitIfStatement(self, ctx:HassoobArabiParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#WhileStatement.
    def visitWhileStatement(self, ctx:HassoobArabiParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#ForEachStatement.
    def visitForEachStatement(self, ctx:HassoobArabiParser.ForEachStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#ForRangeStatement.
    def visitForRangeStatement(self, ctx:HassoobArabiParser.ForRangeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#ReturnStatement.
    def visitReturnStatement(self, ctx:HassoobArabiParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#BreakStatement.
    def visitBreakStatement(self, ctx:HassoobArabiParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#ContinueStatement.
    def visitContinueStatement(self, ctx:HassoobArabiParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#SymbolDeclStatement.
    def visitSymbolDeclStatement(self, ctx:HassoobArabiParser.SymbolDeclStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#AssignStatement.
    def visitAssignStatement(self, ctx:HassoobArabiParser.AssignStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#AugAssignStatement.
    def visitAugAssignStatement(self, ctx:HassoobArabiParser.AugAssignStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#IndexAssignStatement.
    def visitIndexAssignStatement(self, ctx:HassoobArabiParser.IndexAssignStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#ExprStatement.
    def visitExprStatement(self, ctx:HassoobArabiParser.ExprStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#functionDef.
    def visitFunctionDef(self, ctx:HassoobArabiParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#paramList.
    def visitParamList(self, ctx:HassoobArabiParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#block.
    def visitBlock(self, ctx:HassoobArabiParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#ifStmt.
    def visitIfStmt(self, ctx:HassoobArabiParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#elseIfClause.
    def visitElseIfClause(self, ctx:HassoobArabiParser.ElseIfClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#elseClause.
    def visitElseClause(self, ctx:HassoobArabiParser.ElseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#whileStmt.
    def visitWhileStmt(self, ctx:HassoobArabiParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#forEachStmt.
    def visitForEachStmt(self, ctx:HassoobArabiParser.ForEachStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#forRangeStmt.
    def visitForRangeStmt(self, ctx:HassoobArabiParser.ForRangeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#returnStmt.
    def visitReturnStmt(self, ctx:HassoobArabiParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#breakStmt.
    def visitBreakStmt(self, ctx:HassoobArabiParser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#continueStmt.
    def visitContinueStmt(self, ctx:HassoobArabiParser.ContinueStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#symbolDecl.
    def visitSymbolDecl(self, ctx:HassoobArabiParser.SymbolDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#assignStmt.
    def visitAssignStmt(self, ctx:HassoobArabiParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#augAssignStmt.
    def visitAugAssignStmt(self, ctx:HassoobArabiParser.AugAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#augOp.
    def visitAugOp(self, ctx:HassoobArabiParser.AugOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#indexAssignStmt.
    def visitIndexAssignStmt(self, ctx:HassoobArabiParser.IndexAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#exprStmt.
    def visitExprStmt(self, ctx:HassoobArabiParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#expression.
    def visitExpression(self, ctx:HassoobArabiParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#SingleParamLambda.
    def visitSingleParamLambda(self, ctx:HassoobArabiParser.SingleParamLambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#MultiParamLambda.
    def visitMultiParamLambda(self, ctx:HassoobArabiParser.MultiParamLambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#orExpr.
    def visitOrExpr(self, ctx:HassoobArabiParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#andExpr.
    def visitAndExpr(self, ctx:HassoobArabiParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#NotExpression.
    def visitNotExpression(self, ctx:HassoobArabiParser.NotExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#PassThroughNot.
    def visitPassThroughNot(self, ctx:HassoobArabiParser.PassThroughNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#equalityExpr.
    def visitEqualityExpr(self, ctx:HassoobArabiParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#relationalExpr.
    def visitRelationalExpr(self, ctx:HassoobArabiParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#addExpr.
    def visitAddExpr(self, ctx:HassoobArabiParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#mulExpr.
    def visitMulExpr(self, ctx:HassoobArabiParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#UnaryMinus.
    def visitUnaryMinus(self, ctx:HassoobArabiParser.UnaryMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#UnaryPlus.
    def visitUnaryPlus(self, ctx:HassoobArabiParser.UnaryPlusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#PassThroughUnary.
    def visitPassThroughUnary(self, ctx:HassoobArabiParser.PassThroughUnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#powerExpr.
    def visitPowerExpr(self, ctx:HassoobArabiParser.PowerExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#postfixExpr.
    def visitPostfixExpr(self, ctx:HassoobArabiParser.PostfixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#argList.
    def visitArgList(self, ctx:HassoobArabiParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#IntLiteral.
    def visitIntLiteral(self, ctx:HassoobArabiParser.IntLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#FloatLiteral.
    def visitFloatLiteral(self, ctx:HassoobArabiParser.FloatLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#StringLiteral.
    def visitStringLiteral(self, ctx:HassoobArabiParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#FStringLiteral.
    def visitFStringLiteral(self, ctx:HassoobArabiParser.FStringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#PiConstant.
    def visitPiConstant(self, ctx:HassoobArabiParser.PiConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#EulerConstant.
    def visitEulerConstant(self, ctx:HassoobArabiParser.EulerConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#InfinityConstant.
    def visitInfinityConstant(self, ctx:HassoobArabiParser.InfinityConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#TrueLiteral.
    def visitTrueLiteral(self, ctx:HassoobArabiParser.TrueLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#FalseLiteral.
    def visitFalseLiteral(self, ctx:HassoobArabiParser.FalseLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#NullLiteral.
    def visitNullLiteral(self, ctx:HassoobArabiParser.NullLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#IdentifierExpr.
    def visitIdentifierExpr(self, ctx:HassoobArabiParser.IdentifierExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#ListExpr.
    def visitListExpr(self, ctx:HassoobArabiParser.ListExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#ParenExpr.
    def visitParenExpr(self, ctx:HassoobArabiParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#TupleLiteral.
    def visitTupleLiteral(self, ctx:HassoobArabiParser.TupleLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#listLiteral.
    def visitListLiteral(self, ctx:HassoobArabiParser.ListLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HassoobArabiParser#indexList.
    def visitIndexList(self, ctx:HassoobArabiParser.IndexListContext):
        return self.visitChildren(ctx)



del HassoobArabiParser