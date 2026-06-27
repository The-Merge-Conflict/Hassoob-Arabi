// Generated from c:/HIAST/4thyear/S2/Compiler/HassobArabiNew/HassoobArabi.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link HassoobArabiParser}.
 */
public interface HassoobArabiListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(HassoobArabiParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(HassoobArabiParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by the {@code FunctionDefStmt}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterFunctionDefStmt(HassoobArabiParser.FunctionDefStmtContext ctx);
	/**
	 * Exit a parse tree produced by the {@code FunctionDefStmt}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitFunctionDefStmt(HassoobArabiParser.FunctionDefStmtContext ctx);
	/**
	 * Enter a parse tree produced by the {@code IfStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterIfStatement(HassoobArabiParser.IfStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code IfStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitIfStatement(HassoobArabiParser.IfStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code WhileStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterWhileStatement(HassoobArabiParser.WhileStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code WhileStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitWhileStatement(HassoobArabiParser.WhileStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ForEachStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterForEachStatement(HassoobArabiParser.ForEachStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ForEachStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitForEachStatement(HassoobArabiParser.ForEachStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ForRangeStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterForRangeStatement(HassoobArabiParser.ForRangeStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ForRangeStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitForRangeStatement(HassoobArabiParser.ForRangeStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ReturnStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterReturnStatement(HassoobArabiParser.ReturnStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ReturnStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitReturnStatement(HassoobArabiParser.ReturnStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code BreakStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterBreakStatement(HassoobArabiParser.BreakStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code BreakStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitBreakStatement(HassoobArabiParser.BreakStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ContinueStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterContinueStatement(HassoobArabiParser.ContinueStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ContinueStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitContinueStatement(HassoobArabiParser.ContinueStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code SymbolDeclStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterSymbolDeclStatement(HassoobArabiParser.SymbolDeclStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code SymbolDeclStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitSymbolDeclStatement(HassoobArabiParser.SymbolDeclStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code AssignStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterAssignStatement(HassoobArabiParser.AssignStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code AssignStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitAssignStatement(HassoobArabiParser.AssignStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code AugAssignStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterAugAssignStatement(HassoobArabiParser.AugAssignStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code AugAssignStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitAugAssignStatement(HassoobArabiParser.AugAssignStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code IndexAssignStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterIndexAssignStatement(HassoobArabiParser.IndexAssignStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code IndexAssignStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitIndexAssignStatement(HassoobArabiParser.IndexAssignStatementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ExprStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterExprStatement(HassoobArabiParser.ExprStatementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ExprStatement}
	 * labeled alternative in {@link HassoobArabiParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitExprStatement(HassoobArabiParser.ExprStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#functionDef}.
	 * @param ctx the parse tree
	 */
	void enterFunctionDef(HassoobArabiParser.FunctionDefContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#functionDef}.
	 * @param ctx the parse tree
	 */
	void exitFunctionDef(HassoobArabiParser.FunctionDefContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#paramList}.
	 * @param ctx the parse tree
	 */
	void enterParamList(HassoobArabiParser.ParamListContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#paramList}.
	 * @param ctx the parse tree
	 */
	void exitParamList(HassoobArabiParser.ParamListContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#block}.
	 * @param ctx the parse tree
	 */
	void enterBlock(HassoobArabiParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#block}.
	 * @param ctx the parse tree
	 */
	void exitBlock(HassoobArabiParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void enterIfStmt(HassoobArabiParser.IfStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void exitIfStmt(HassoobArabiParser.IfStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#elseIfClause}.
	 * @param ctx the parse tree
	 */
	void enterElseIfClause(HassoobArabiParser.ElseIfClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#elseIfClause}.
	 * @param ctx the parse tree
	 */
	void exitElseIfClause(HassoobArabiParser.ElseIfClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#elseClause}.
	 * @param ctx the parse tree
	 */
	void enterElseClause(HassoobArabiParser.ElseClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#elseClause}.
	 * @param ctx the parse tree
	 */
	void exitElseClause(HassoobArabiParser.ElseClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#whileStmt}.
	 * @param ctx the parse tree
	 */
	void enterWhileStmt(HassoobArabiParser.WhileStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#whileStmt}.
	 * @param ctx the parse tree
	 */
	void exitWhileStmt(HassoobArabiParser.WhileStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#forEachStmt}.
	 * @param ctx the parse tree
	 */
	void enterForEachStmt(HassoobArabiParser.ForEachStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#forEachStmt}.
	 * @param ctx the parse tree
	 */
	void exitForEachStmt(HassoobArabiParser.ForEachStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#forRangeStmt}.
	 * @param ctx the parse tree
	 */
	void enterForRangeStmt(HassoobArabiParser.ForRangeStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#forRangeStmt}.
	 * @param ctx the parse tree
	 */
	void exitForRangeStmt(HassoobArabiParser.ForRangeStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void enterReturnStmt(HassoobArabiParser.ReturnStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void exitReturnStmt(HassoobArabiParser.ReturnStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#breakStmt}.
	 * @param ctx the parse tree
	 */
	void enterBreakStmt(HassoobArabiParser.BreakStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#breakStmt}.
	 * @param ctx the parse tree
	 */
	void exitBreakStmt(HassoobArabiParser.BreakStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#continueStmt}.
	 * @param ctx the parse tree
	 */
	void enterContinueStmt(HassoobArabiParser.ContinueStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#continueStmt}.
	 * @param ctx the parse tree
	 */
	void exitContinueStmt(HassoobArabiParser.ContinueStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#symbolDecl}.
	 * @param ctx the parse tree
	 */
	void enterSymbolDecl(HassoobArabiParser.SymbolDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#symbolDecl}.
	 * @param ctx the parse tree
	 */
	void exitSymbolDecl(HassoobArabiParser.SymbolDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#assignStmt}.
	 * @param ctx the parse tree
	 */
	void enterAssignStmt(HassoobArabiParser.AssignStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#assignStmt}.
	 * @param ctx the parse tree
	 */
	void exitAssignStmt(HassoobArabiParser.AssignStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#augAssignStmt}.
	 * @param ctx the parse tree
	 */
	void enterAugAssignStmt(HassoobArabiParser.AugAssignStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#augAssignStmt}.
	 * @param ctx the parse tree
	 */
	void exitAugAssignStmt(HassoobArabiParser.AugAssignStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#augOp}.
	 * @param ctx the parse tree
	 */
	void enterAugOp(HassoobArabiParser.AugOpContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#augOp}.
	 * @param ctx the parse tree
	 */
	void exitAugOp(HassoobArabiParser.AugOpContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#indexAssignStmt}.
	 * @param ctx the parse tree
	 */
	void enterIndexAssignStmt(HassoobArabiParser.IndexAssignStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#indexAssignStmt}.
	 * @param ctx the parse tree
	 */
	void exitIndexAssignStmt(HassoobArabiParser.IndexAssignStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#exprStmt}.
	 * @param ctx the parse tree
	 */
	void enterExprStmt(HassoobArabiParser.ExprStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#exprStmt}.
	 * @param ctx the parse tree
	 */
	void exitExprStmt(HassoobArabiParser.ExprStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(HassoobArabiParser.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(HassoobArabiParser.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code SingleParamLambda}
	 * labeled alternative in {@link HassoobArabiParser#lambdaExpr}.
	 * @param ctx the parse tree
	 */
	void enterSingleParamLambda(HassoobArabiParser.SingleParamLambdaContext ctx);
	/**
	 * Exit a parse tree produced by the {@code SingleParamLambda}
	 * labeled alternative in {@link HassoobArabiParser#lambdaExpr}.
	 * @param ctx the parse tree
	 */
	void exitSingleParamLambda(HassoobArabiParser.SingleParamLambdaContext ctx);
	/**
	 * Enter a parse tree produced by the {@code MultiParamLambda}
	 * labeled alternative in {@link HassoobArabiParser#lambdaExpr}.
	 * @param ctx the parse tree
	 */
	void enterMultiParamLambda(HassoobArabiParser.MultiParamLambdaContext ctx);
	/**
	 * Exit a parse tree produced by the {@code MultiParamLambda}
	 * labeled alternative in {@link HassoobArabiParser#lambdaExpr}.
	 * @param ctx the parse tree
	 */
	void exitMultiParamLambda(HassoobArabiParser.MultiParamLambdaContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#orExpr}.
	 * @param ctx the parse tree
	 */
	void enterOrExpr(HassoobArabiParser.OrExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#orExpr}.
	 * @param ctx the parse tree
	 */
	void exitOrExpr(HassoobArabiParser.OrExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#andExpr}.
	 * @param ctx the parse tree
	 */
	void enterAndExpr(HassoobArabiParser.AndExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#andExpr}.
	 * @param ctx the parse tree
	 */
	void exitAndExpr(HassoobArabiParser.AndExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code NotExpression}
	 * labeled alternative in {@link HassoobArabiParser#notExpr}.
	 * @param ctx the parse tree
	 */
	void enterNotExpression(HassoobArabiParser.NotExpressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code NotExpression}
	 * labeled alternative in {@link HassoobArabiParser#notExpr}.
	 * @param ctx the parse tree
	 */
	void exitNotExpression(HassoobArabiParser.NotExpressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code PassThroughNot}
	 * labeled alternative in {@link HassoobArabiParser#notExpr}.
	 * @param ctx the parse tree
	 */
	void enterPassThroughNot(HassoobArabiParser.PassThroughNotContext ctx);
	/**
	 * Exit a parse tree produced by the {@code PassThroughNot}
	 * labeled alternative in {@link HassoobArabiParser#notExpr}.
	 * @param ctx the parse tree
	 */
	void exitPassThroughNot(HassoobArabiParser.PassThroughNotContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#equalityExpr}.
	 * @param ctx the parse tree
	 */
	void enterEqualityExpr(HassoobArabiParser.EqualityExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#equalityExpr}.
	 * @param ctx the parse tree
	 */
	void exitEqualityExpr(HassoobArabiParser.EqualityExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#relationalExpr}.
	 * @param ctx the parse tree
	 */
	void enterRelationalExpr(HassoobArabiParser.RelationalExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#relationalExpr}.
	 * @param ctx the parse tree
	 */
	void exitRelationalExpr(HassoobArabiParser.RelationalExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#addExpr}.
	 * @param ctx the parse tree
	 */
	void enterAddExpr(HassoobArabiParser.AddExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#addExpr}.
	 * @param ctx the parse tree
	 */
	void exitAddExpr(HassoobArabiParser.AddExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#mulExpr}.
	 * @param ctx the parse tree
	 */
	void enterMulExpr(HassoobArabiParser.MulExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#mulExpr}.
	 * @param ctx the parse tree
	 */
	void exitMulExpr(HassoobArabiParser.MulExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code UnaryMinus}
	 * labeled alternative in {@link HassoobArabiParser#unaryExpr}.
	 * @param ctx the parse tree
	 */
	void enterUnaryMinus(HassoobArabiParser.UnaryMinusContext ctx);
	/**
	 * Exit a parse tree produced by the {@code UnaryMinus}
	 * labeled alternative in {@link HassoobArabiParser#unaryExpr}.
	 * @param ctx the parse tree
	 */
	void exitUnaryMinus(HassoobArabiParser.UnaryMinusContext ctx);
	/**
	 * Enter a parse tree produced by the {@code UnaryPlus}
	 * labeled alternative in {@link HassoobArabiParser#unaryExpr}.
	 * @param ctx the parse tree
	 */
	void enterUnaryPlus(HassoobArabiParser.UnaryPlusContext ctx);
	/**
	 * Exit a parse tree produced by the {@code UnaryPlus}
	 * labeled alternative in {@link HassoobArabiParser#unaryExpr}.
	 * @param ctx the parse tree
	 */
	void exitUnaryPlus(HassoobArabiParser.UnaryPlusContext ctx);
	/**
	 * Enter a parse tree produced by the {@code PassThroughUnary}
	 * labeled alternative in {@link HassoobArabiParser#unaryExpr}.
	 * @param ctx the parse tree
	 */
	void enterPassThroughUnary(HassoobArabiParser.PassThroughUnaryContext ctx);
	/**
	 * Exit a parse tree produced by the {@code PassThroughUnary}
	 * labeled alternative in {@link HassoobArabiParser#unaryExpr}.
	 * @param ctx the parse tree
	 */
	void exitPassThroughUnary(HassoobArabiParser.PassThroughUnaryContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#powerExpr}.
	 * @param ctx the parse tree
	 */
	void enterPowerExpr(HassoobArabiParser.PowerExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#powerExpr}.
	 * @param ctx the parse tree
	 */
	void exitPowerExpr(HassoobArabiParser.PowerExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#postfixExpr}.
	 * @param ctx the parse tree
	 */
	void enterPostfixExpr(HassoobArabiParser.PostfixExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#postfixExpr}.
	 * @param ctx the parse tree
	 */
	void exitPostfixExpr(HassoobArabiParser.PostfixExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#argList}.
	 * @param ctx the parse tree
	 */
	void enterArgList(HassoobArabiParser.ArgListContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#argList}.
	 * @param ctx the parse tree
	 */
	void exitArgList(HassoobArabiParser.ArgListContext ctx);
	/**
	 * Enter a parse tree produced by the {@code IntLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterIntLiteral(HassoobArabiParser.IntLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code IntLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitIntLiteral(HassoobArabiParser.IntLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code FloatLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterFloatLiteral(HassoobArabiParser.FloatLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code FloatLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitFloatLiteral(HassoobArabiParser.FloatLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code StringLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterStringLiteral(HassoobArabiParser.StringLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code StringLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitStringLiteral(HassoobArabiParser.StringLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code FStringLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterFStringLiteral(HassoobArabiParser.FStringLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code FStringLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitFStringLiteral(HassoobArabiParser.FStringLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code PiConstant}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterPiConstant(HassoobArabiParser.PiConstantContext ctx);
	/**
	 * Exit a parse tree produced by the {@code PiConstant}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitPiConstant(HassoobArabiParser.PiConstantContext ctx);
	/**
	 * Enter a parse tree produced by the {@code EulerConstant}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterEulerConstant(HassoobArabiParser.EulerConstantContext ctx);
	/**
	 * Exit a parse tree produced by the {@code EulerConstant}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitEulerConstant(HassoobArabiParser.EulerConstantContext ctx);
	/**
	 * Enter a parse tree produced by the {@code InfinityConstant}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterInfinityConstant(HassoobArabiParser.InfinityConstantContext ctx);
	/**
	 * Exit a parse tree produced by the {@code InfinityConstant}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitInfinityConstant(HassoobArabiParser.InfinityConstantContext ctx);
	/**
	 * Enter a parse tree produced by the {@code TrueLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterTrueLiteral(HassoobArabiParser.TrueLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code TrueLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitTrueLiteral(HassoobArabiParser.TrueLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code FalseLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterFalseLiteral(HassoobArabiParser.FalseLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code FalseLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitFalseLiteral(HassoobArabiParser.FalseLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code NullLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterNullLiteral(HassoobArabiParser.NullLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code NullLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitNullLiteral(HassoobArabiParser.NullLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code IdentifierExpr}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterIdentifierExpr(HassoobArabiParser.IdentifierExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code IdentifierExpr}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitIdentifierExpr(HassoobArabiParser.IdentifierExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ListExpr}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterListExpr(HassoobArabiParser.ListExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ListExpr}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitListExpr(HassoobArabiParser.ListExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ParenExpr}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterParenExpr(HassoobArabiParser.ParenExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ParenExpr}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitParenExpr(HassoobArabiParser.ParenExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code TupleLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterTupleLiteral(HassoobArabiParser.TupleLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code TupleLiteral}
	 * labeled alternative in {@link HassoobArabiParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitTupleLiteral(HassoobArabiParser.TupleLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#listLiteral}.
	 * @param ctx the parse tree
	 */
	void enterListLiteral(HassoobArabiParser.ListLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#listLiteral}.
	 * @param ctx the parse tree
	 */
	void exitListLiteral(HassoobArabiParser.ListLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link HassoobArabiParser#indexList}.
	 * @param ctx the parse tree
	 */
	void enterIndexList(HassoobArabiParser.IndexListContext ctx);
	/**
	 * Exit a parse tree produced by {@link HassoobArabiParser#indexList}.
	 * @param ctx the parse tree
	 */
	void exitIndexList(HassoobArabiParser.IndexListContext ctx);
}