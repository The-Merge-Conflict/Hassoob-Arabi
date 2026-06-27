// Generated from c:/HIAST/4thyear/S2/Compiler/HassobArabiNew/HassoobArabi.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class HassoobArabiParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		IDHA=1, WA_ILLA=2, BAYNAMA=3, LIKULL=4, MIN=5, ILA=6, FI=7, BKHUTWA=8, 
		DALA=9, IRJA=10, AWQIF=11, ISTAMIRR=12, SAHIH=13, KHATA=14, FARIG=15, 
		RAMZ=16, PI_CONST=17, E_CONST=18, INF_CONST=19, AND=20, OR=21, NOT=22, 
		PLUS_ASSIGN=23, MINUS_ASSIGN=24, STAR_ASSIGN=25, SLASH_ASSIGN=26, CARET_ASSIGN=27, 
		PERCENT_ASSIGN=28, CONCAT_ASSIGN=29, MAT_MUL=30, STR_CONCAT=31, PLUS=32, 
		MINUS=33, STAR=34, SLASH=35, INT_DIV=36, PERCENT=37, CARET=38, ARROW=39, 
		EQ=40, NEQ=41, LTE=42, GTE=43, LT=44, GT=45, ASSIGN=46, LPAREN=47, RPAREN=48, 
		LBRACKET=49, RBRACKET=50, LBRACE=51, RBRACE=52, COMMA=53, SEMI=54, COLON=55, 
		DOT=56, INTEGER_LIT=57, FLOAT_LIT=58, STRING_LIT=59, FSTRING_LIT=60, IDENTIFIER=61, 
		LINE_COMMENT=62, ARABIC_COMMENT=63, BLOCK_COMMENT=64, WS=65;
	public static final int
		RULE_program = 0, RULE_statement = 1, RULE_functionDef = 2, RULE_paramList = 3, 
		RULE_block = 4, RULE_ifStmt = 5, RULE_elseIfClause = 6, RULE_elseClause = 7, 
		RULE_whileStmt = 8, RULE_forEachStmt = 9, RULE_forRangeStmt = 10, RULE_returnStmt = 11, 
		RULE_breakStmt = 12, RULE_continueStmt = 13, RULE_symbolDecl = 14, RULE_assignStmt = 15, 
		RULE_augAssignStmt = 16, RULE_augOp = 17, RULE_indexAssignStmt = 18, RULE_exprStmt = 19, 
		RULE_expression = 20, RULE_lambdaExpr = 21, RULE_orExpr = 22, RULE_andExpr = 23, 
		RULE_notExpr = 24, RULE_equalityExpr = 25, RULE_relationalExpr = 26, RULE_addExpr = 27, 
		RULE_mulExpr = 28, RULE_unaryExpr = 29, RULE_powerExpr = 30, RULE_postfixExpr = 31, 
		RULE_argList = 32, RULE_primary = 33, RULE_listLiteral = 34, RULE_indexList = 35;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "statement", "functionDef", "paramList", "block", "ifStmt", 
			"elseIfClause", "elseClause", "whileStmt", "forEachStmt", "forRangeStmt", 
			"returnStmt", "breakStmt", "continueStmt", "symbolDecl", "assignStmt", 
			"augAssignStmt", "augOp", "indexAssignStmt", "exprStmt", "expression", 
			"lambdaExpr", "orExpr", "andExpr", "notExpr", "equalityExpr", "relationalExpr", 
			"addExpr", "mulExpr", "unaryExpr", "powerExpr", "postfixExpr", "argList", 
			"primary", "listLiteral", "indexList"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'\\u0625\\u0630\\u0627'", "'\\u0648\\u0625\\u0644\\u0627'", "'\\u0628\\u064A\\u0646\\u0645\\u0627'", 
			"'\\u0644\\u0643\\u0644'", "'\\u0645\\u0646'", "'\\u0625\\u0644\\u0649'", 
			"'\\u0641\\u064A'", "'\\u0628\\u062E\\u0637\\u0648\\u0629'", "'\\u062F\\u0627\\u0644\\u0629'", 
			"'\\u0625\\u0631\\u062C\\u0639'", "'\\u062A\\u0648\\u0642\\u0641'", "'\\u0627\\u0633\\u062A\\u0645\\u0631'", 
			"'\\u0635\\u062D'", "'\\u062E\\u0637\\u0623'", "'\\u0641\\u0627\\u0631\\u063A'", 
			"'\\u0631\\u0645\\u0632'", null, "'\\u0647\\u0640'", "'\\u0644\\u0627\\u0646\\u0647\\u0627\\u064A\\u0629'", 
			null, null, null, "'+='", "'-='", "'*='", "'/='", "'^='", "'%='", "'++='", 
			"'**'", "'++'", "'+'", "'-'", "'*'", "'/'", "'\\u00F7'", "'%'", "'^'", 
			"'=>'", "'=='", null, null, null, "'<'", "'>'", "'='", "'('", "')'", 
			"'['", "']'", "'{'", "'}'", null, null, "':'", "'.'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "IDHA", "WA_ILLA", "BAYNAMA", "LIKULL", "MIN", "ILA", "FI", "BKHUTWA", 
			"DALA", "IRJA", "AWQIF", "ISTAMIRR", "SAHIH", "KHATA", "FARIG", "RAMZ", 
			"PI_CONST", "E_CONST", "INF_CONST", "AND", "OR", "NOT", "PLUS_ASSIGN", 
			"MINUS_ASSIGN", "STAR_ASSIGN", "SLASH_ASSIGN", "CARET_ASSIGN", "PERCENT_ASSIGN", 
			"CONCAT_ASSIGN", "MAT_MUL", "STR_CONCAT", "PLUS", "MINUS", "STAR", "SLASH", 
			"INT_DIV", "PERCENT", "CARET", "ARROW", "EQ", "NEQ", "LTE", "GTE", "LT", 
			"GT", "ASSIGN", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", "LBRACE", 
			"RBRACE", "COMMA", "SEMI", "COLON", "DOT", "INTEGER_LIT", "FLOAT_LIT", 
			"STRING_LIT", "FSTRING_LIT", "IDENTIFIER", "LINE_COMMENT", "ARABIC_COMMENT", 
			"BLOCK_COMMENT", "WS"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "HassoobArabi.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public HassoobArabiParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(HassoobArabiParser.EOF, 0); }
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(75);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 4468274530683452954L) != 0)) {
				{
				{
				setState(72);
				statement();
				}
				}
				setState(77);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(78);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class StatementContext extends ParserRuleContext {
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
	 
		public StatementContext() { }
		public void copyFrom(StatementContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AugAssignStatementContext extends StatementContext {
		public AugAssignStmtContext augAssignStmt() {
			return getRuleContext(AugAssignStmtContext.class,0);
		}
		public AugAssignStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SymbolDeclStatementContext extends StatementContext {
		public SymbolDeclContext symbolDecl() {
			return getRuleContext(SymbolDeclContext.class,0);
		}
		public SymbolDeclStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IndexAssignStatementContext extends StatementContext {
		public IndexAssignStmtContext indexAssignStmt() {
			return getRuleContext(IndexAssignStmtContext.class,0);
		}
		public IndexAssignStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ForRangeStatementContext extends StatementContext {
		public ForRangeStmtContext forRangeStmt() {
			return getRuleContext(ForRangeStmtContext.class,0);
		}
		public ForRangeStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class WhileStatementContext extends StatementContext {
		public WhileStmtContext whileStmt() {
			return getRuleContext(WhileStmtContext.class,0);
		}
		public WhileStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AssignStatementContext extends StatementContext {
		public AssignStmtContext assignStmt() {
			return getRuleContext(AssignStmtContext.class,0);
		}
		public AssignStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class BreakStatementContext extends StatementContext {
		public BreakStmtContext breakStmt() {
			return getRuleContext(BreakStmtContext.class,0);
		}
		public BreakStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IfStatementContext extends StatementContext {
		public IfStmtContext ifStmt() {
			return getRuleContext(IfStmtContext.class,0);
		}
		public IfStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ReturnStatementContext extends StatementContext {
		public ReturnStmtContext returnStmt() {
			return getRuleContext(ReturnStmtContext.class,0);
		}
		public ReturnStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExprStatementContext extends StatementContext {
		public ExprStmtContext exprStmt() {
			return getRuleContext(ExprStmtContext.class,0);
		}
		public ExprStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FunctionDefStmtContext extends StatementContext {
		public FunctionDefContext functionDef() {
			return getRuleContext(FunctionDefContext.class,0);
		}
		public FunctionDefStmtContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ContinueStatementContext extends StatementContext {
		public ContinueStmtContext continueStmt() {
			return getRuleContext(ContinueStmtContext.class,0);
		}
		public ContinueStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ForEachStatementContext extends StatementContext {
		public ForEachStmtContext forEachStmt() {
			return getRuleContext(ForEachStmtContext.class,0);
		}
		public ForEachStatementContext(StatementContext ctx) { copyFrom(ctx); }
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_statement);
		try {
			setState(93);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
			case 1:
				_localctx = new FunctionDefStmtContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(80);
				functionDef();
				}
				break;
			case 2:
				_localctx = new IfStatementContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(81);
				ifStmt();
				}
				break;
			case 3:
				_localctx = new WhileStatementContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(82);
				whileStmt();
				}
				break;
			case 4:
				_localctx = new ForEachStatementContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(83);
				forEachStmt();
				}
				break;
			case 5:
				_localctx = new ForRangeStatementContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(84);
				forRangeStmt();
				}
				break;
			case 6:
				_localctx = new ReturnStatementContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(85);
				returnStmt();
				}
				break;
			case 7:
				_localctx = new BreakStatementContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(86);
				breakStmt();
				}
				break;
			case 8:
				_localctx = new ContinueStatementContext(_localctx);
				enterOuterAlt(_localctx, 8);
				{
				setState(87);
				continueStmt();
				}
				break;
			case 9:
				_localctx = new SymbolDeclStatementContext(_localctx);
				enterOuterAlt(_localctx, 9);
				{
				setState(88);
				symbolDecl();
				}
				break;
			case 10:
				_localctx = new AssignStatementContext(_localctx);
				enterOuterAlt(_localctx, 10);
				{
				setState(89);
				assignStmt();
				}
				break;
			case 11:
				_localctx = new AugAssignStatementContext(_localctx);
				enterOuterAlt(_localctx, 11);
				{
				setState(90);
				augAssignStmt();
				}
				break;
			case 12:
				_localctx = new IndexAssignStatementContext(_localctx);
				enterOuterAlt(_localctx, 12);
				{
				setState(91);
				indexAssignStmt();
				}
				break;
			case 13:
				_localctx = new ExprStatementContext(_localctx);
				enterOuterAlt(_localctx, 13);
				{
				setState(92);
				exprStmt();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FunctionDefContext extends ParserRuleContext {
		public TerminalNode DALA() { return getToken(HassoobArabiParser.DALA, 0); }
		public TerminalNode IDENTIFIER() { return getToken(HassoobArabiParser.IDENTIFIER, 0); }
		public TerminalNode LPAREN() { return getToken(HassoobArabiParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(HassoobArabiParser.RPAREN, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public ParamListContext paramList() {
			return getRuleContext(ParamListContext.class,0);
		}
		public FunctionDefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_functionDef; }
	}

	public final FunctionDefContext functionDef() throws RecognitionException {
		FunctionDefContext _localctx = new FunctionDefContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_functionDef);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(95);
			match(DALA);
			setState(96);
			match(IDENTIFIER);
			setState(97);
			match(LPAREN);
			setState(99);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==IDENTIFIER) {
				{
				setState(98);
				paramList();
				}
			}

			setState(101);
			match(RPAREN);
			setState(102);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ParamListContext extends ParserRuleContext {
		public List<TerminalNode> IDENTIFIER() { return getTokens(HassoobArabiParser.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(HassoobArabiParser.IDENTIFIER, i);
		}
		public List<TerminalNode> COMMA() { return getTokens(HassoobArabiParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(HassoobArabiParser.COMMA, i);
		}
		public ParamListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_paramList; }
	}

	public final ParamListContext paramList() throws RecognitionException {
		ParamListContext _localctx = new ParamListContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_paramList);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(104);
			match(IDENTIFIER);
			setState(109);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(105);
				match(COMMA);
				setState(106);
				match(IDENTIFIER);
				}
				}
				setState(111);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BlockContext extends ParserRuleContext {
		public TerminalNode LBRACE() { return getToken(HassoobArabiParser.LBRACE, 0); }
		public TerminalNode RBRACE() { return getToken(HassoobArabiParser.RBRACE, 0); }
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public BlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_block; }
	}

	public final BlockContext block() throws RecognitionException {
		BlockContext _localctx = new BlockContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_block);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(112);
			match(LBRACE);
			setState(116);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 4468274530683452954L) != 0)) {
				{
				{
				setState(113);
				statement();
				}
				}
				setState(118);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(119);
			match(RBRACE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class IfStmtContext extends ParserRuleContext {
		public TerminalNode IDHA() { return getToken(HassoobArabiParser.IDHA, 0); }
		public TerminalNode LPAREN() { return getToken(HassoobArabiParser.LPAREN, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(HassoobArabiParser.RPAREN, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public List<ElseIfClauseContext> elseIfClause() {
			return getRuleContexts(ElseIfClauseContext.class);
		}
		public ElseIfClauseContext elseIfClause(int i) {
			return getRuleContext(ElseIfClauseContext.class,i);
		}
		public ElseClauseContext elseClause() {
			return getRuleContext(ElseClauseContext.class,0);
		}
		public IfStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ifStmt; }
	}

	public final IfStmtContext ifStmt() throws RecognitionException {
		IfStmtContext _localctx = new IfStmtContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_ifStmt);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(121);
			match(IDHA);
			setState(122);
			match(LPAREN);
			setState(123);
			expression();
			setState(124);
			match(RPAREN);
			setState(125);
			block();
			setState(129);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(126);
					elseIfClause();
					}
					} 
				}
				setState(131);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
			}
			setState(133);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==WA_ILLA) {
				{
				setState(132);
				elseClause();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ElseIfClauseContext extends ParserRuleContext {
		public TerminalNode WA_ILLA() { return getToken(HassoobArabiParser.WA_ILLA, 0); }
		public TerminalNode IDHA() { return getToken(HassoobArabiParser.IDHA, 0); }
		public TerminalNode LPAREN() { return getToken(HassoobArabiParser.LPAREN, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(HassoobArabiParser.RPAREN, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public ElseIfClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_elseIfClause; }
	}

	public final ElseIfClauseContext elseIfClause() throws RecognitionException {
		ElseIfClauseContext _localctx = new ElseIfClauseContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_elseIfClause);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(135);
			match(WA_ILLA);
			setState(136);
			match(IDHA);
			setState(137);
			match(LPAREN);
			setState(138);
			expression();
			setState(139);
			match(RPAREN);
			setState(140);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ElseClauseContext extends ParserRuleContext {
		public TerminalNode WA_ILLA() { return getToken(HassoobArabiParser.WA_ILLA, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public ElseClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_elseClause; }
	}

	public final ElseClauseContext elseClause() throws RecognitionException {
		ElseClauseContext _localctx = new ElseClauseContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_elseClause);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(142);
			match(WA_ILLA);
			setState(143);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class WhileStmtContext extends ParserRuleContext {
		public TerminalNode BAYNAMA() { return getToken(HassoobArabiParser.BAYNAMA, 0); }
		public TerminalNode LPAREN() { return getToken(HassoobArabiParser.LPAREN, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(HassoobArabiParser.RPAREN, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public WhileStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_whileStmt; }
	}

	public final WhileStmtContext whileStmt() throws RecognitionException {
		WhileStmtContext _localctx = new WhileStmtContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_whileStmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(145);
			match(BAYNAMA);
			setState(146);
			match(LPAREN);
			setState(147);
			expression();
			setState(148);
			match(RPAREN);
			setState(149);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ForEachStmtContext extends ParserRuleContext {
		public TerminalNode LIKULL() { return getToken(HassoobArabiParser.LIKULL, 0); }
		public TerminalNode IDENTIFIER() { return getToken(HassoobArabiParser.IDENTIFIER, 0); }
		public TerminalNode FI() { return getToken(HassoobArabiParser.FI, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public ForEachStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_forEachStmt; }
	}

	public final ForEachStmtContext forEachStmt() throws RecognitionException {
		ForEachStmtContext _localctx = new ForEachStmtContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_forEachStmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(151);
			match(LIKULL);
			setState(152);
			match(IDENTIFIER);
			setState(153);
			match(FI);
			setState(154);
			expression();
			setState(155);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ForRangeStmtContext extends ParserRuleContext {
		public TerminalNode LIKULL() { return getToken(HassoobArabiParser.LIKULL, 0); }
		public TerminalNode IDENTIFIER() { return getToken(HassoobArabiParser.IDENTIFIER, 0); }
		public TerminalNode MIN() { return getToken(HassoobArabiParser.MIN, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode ILA() { return getToken(HassoobArabiParser.ILA, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public TerminalNode BKHUTWA() { return getToken(HassoobArabiParser.BKHUTWA, 0); }
		public ForRangeStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_forRangeStmt; }
	}

	public final ForRangeStmtContext forRangeStmt() throws RecognitionException {
		ForRangeStmtContext _localctx = new ForRangeStmtContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_forRangeStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(157);
			match(LIKULL);
			setState(158);
			match(IDENTIFIER);
			setState(159);
			match(MIN);
			setState(160);
			expression();
			setState(161);
			match(ILA);
			setState(162);
			expression();
			setState(165);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==BKHUTWA) {
				{
				setState(163);
				match(BKHUTWA);
				setState(164);
				expression();
				}
			}

			setState(167);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ReturnStmtContext extends ParserRuleContext {
		public TerminalNode IRJA() { return getToken(HassoobArabiParser.IRJA, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode SEMI() { return getToken(HassoobArabiParser.SEMI, 0); }
		public ReturnStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_returnStmt; }
	}

	public final ReturnStmtContext returnStmt() throws RecognitionException {
		ReturnStmtContext _localctx = new ReturnStmtContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_returnStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(169);
			match(IRJA);
			setState(171);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,8,_ctx) ) {
			case 1:
				{
				setState(170);
				expression();
				}
				break;
			}
			setState(174);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SEMI) {
				{
				setState(173);
				match(SEMI);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BreakStmtContext extends ParserRuleContext {
		public TerminalNode AWQIF() { return getToken(HassoobArabiParser.AWQIF, 0); }
		public TerminalNode SEMI() { return getToken(HassoobArabiParser.SEMI, 0); }
		public BreakStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_breakStmt; }
	}

	public final BreakStmtContext breakStmt() throws RecognitionException {
		BreakStmtContext _localctx = new BreakStmtContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_breakStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(176);
			match(AWQIF);
			setState(178);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SEMI) {
				{
				setState(177);
				match(SEMI);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ContinueStmtContext extends ParserRuleContext {
		public TerminalNode ISTAMIRR() { return getToken(HassoobArabiParser.ISTAMIRR, 0); }
		public TerminalNode SEMI() { return getToken(HassoobArabiParser.SEMI, 0); }
		public ContinueStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_continueStmt; }
	}

	public final ContinueStmtContext continueStmt() throws RecognitionException {
		ContinueStmtContext _localctx = new ContinueStmtContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_continueStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(180);
			match(ISTAMIRR);
			setState(182);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SEMI) {
				{
				setState(181);
				match(SEMI);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SymbolDeclContext extends ParserRuleContext {
		public TerminalNode RAMZ() { return getToken(HassoobArabiParser.RAMZ, 0); }
		public List<TerminalNode> IDENTIFIER() { return getTokens(HassoobArabiParser.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(HassoobArabiParser.IDENTIFIER, i);
		}
		public List<TerminalNode> COMMA() { return getTokens(HassoobArabiParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(HassoobArabiParser.COMMA, i);
		}
		public TerminalNode SEMI() { return getToken(HassoobArabiParser.SEMI, 0); }
		public SymbolDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_symbolDecl; }
	}

	public final SymbolDeclContext symbolDecl() throws RecognitionException {
		SymbolDeclContext _localctx = new SymbolDeclContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_symbolDecl);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(184);
			match(RAMZ);
			setState(185);
			match(IDENTIFIER);
			setState(190);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(186);
				match(COMMA);
				setState(187);
				match(IDENTIFIER);
				}
				}
				setState(192);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(194);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SEMI) {
				{
				setState(193);
				match(SEMI);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AssignStmtContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(HassoobArabiParser.IDENTIFIER, 0); }
		public TerminalNode ASSIGN() { return getToken(HassoobArabiParser.ASSIGN, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode SEMI() { return getToken(HassoobArabiParser.SEMI, 0); }
		public AssignStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assignStmt; }
	}

	public final AssignStmtContext assignStmt() throws RecognitionException {
		AssignStmtContext _localctx = new AssignStmtContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_assignStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(196);
			match(IDENTIFIER);
			setState(197);
			match(ASSIGN);
			setState(198);
			expression();
			setState(200);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SEMI) {
				{
				setState(199);
				match(SEMI);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AugAssignStmtContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(HassoobArabiParser.IDENTIFIER, 0); }
		public AugOpContext augOp() {
			return getRuleContext(AugOpContext.class,0);
		}
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode SEMI() { return getToken(HassoobArabiParser.SEMI, 0); }
		public AugAssignStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_augAssignStmt; }
	}

	public final AugAssignStmtContext augAssignStmt() throws RecognitionException {
		AugAssignStmtContext _localctx = new AugAssignStmtContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_augAssignStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(202);
			match(IDENTIFIER);
			setState(203);
			augOp();
			setState(204);
			expression();
			setState(206);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SEMI) {
				{
				setState(205);
				match(SEMI);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AugOpContext extends ParserRuleContext {
		public TerminalNode PLUS_ASSIGN() { return getToken(HassoobArabiParser.PLUS_ASSIGN, 0); }
		public TerminalNode MINUS_ASSIGN() { return getToken(HassoobArabiParser.MINUS_ASSIGN, 0); }
		public TerminalNode STAR_ASSIGN() { return getToken(HassoobArabiParser.STAR_ASSIGN, 0); }
		public TerminalNode SLASH_ASSIGN() { return getToken(HassoobArabiParser.SLASH_ASSIGN, 0); }
		public TerminalNode CARET_ASSIGN() { return getToken(HassoobArabiParser.CARET_ASSIGN, 0); }
		public TerminalNode PERCENT_ASSIGN() { return getToken(HassoobArabiParser.PERCENT_ASSIGN, 0); }
		public TerminalNode CONCAT_ASSIGN() { return getToken(HassoobArabiParser.CONCAT_ASSIGN, 0); }
		public AugOpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_augOp; }
	}

	public final AugOpContext augOp() throws RecognitionException {
		AugOpContext _localctx = new AugOpContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_augOp);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(208);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 1065353216L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class IndexAssignStmtContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(HassoobArabiParser.IDENTIFIER, 0); }
		public TerminalNode ASSIGN() { return getToken(HassoobArabiParser.ASSIGN, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public List<TerminalNode> LBRACKET() { return getTokens(HassoobArabiParser.LBRACKET); }
		public TerminalNode LBRACKET(int i) {
			return getToken(HassoobArabiParser.LBRACKET, i);
		}
		public List<IndexListContext> indexList() {
			return getRuleContexts(IndexListContext.class);
		}
		public IndexListContext indexList(int i) {
			return getRuleContext(IndexListContext.class,i);
		}
		public List<TerminalNode> RBRACKET() { return getTokens(HassoobArabiParser.RBRACKET); }
		public TerminalNode RBRACKET(int i) {
			return getToken(HassoobArabiParser.RBRACKET, i);
		}
		public TerminalNode SEMI() { return getToken(HassoobArabiParser.SEMI, 0); }
		public IndexAssignStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_indexAssignStmt; }
	}

	public final IndexAssignStmtContext indexAssignStmt() throws RecognitionException {
		IndexAssignStmtContext _localctx = new IndexAssignStmtContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_indexAssignStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(210);
			match(IDENTIFIER);
			setState(215); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(211);
				match(LBRACKET);
				setState(212);
				indexList();
				setState(213);
				match(RBRACKET);
				}
				}
				setState(217); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==LBRACKET );
			setState(219);
			match(ASSIGN);
			setState(220);
			expression();
			setState(222);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SEMI) {
				{
				setState(221);
				match(SEMI);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExprStmtContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode SEMI() { return getToken(HassoobArabiParser.SEMI, 0); }
		public ExprStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_exprStmt; }
	}

	public final ExprStmtContext exprStmt() throws RecognitionException {
		ExprStmtContext _localctx = new ExprStmtContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_exprStmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(224);
			expression();
			setState(226);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SEMI) {
				{
				setState(225);
				match(SEMI);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressionContext extends ParserRuleContext {
		public LambdaExprContext lambdaExpr() {
			return getRuleContext(LambdaExprContext.class,0);
		}
		public OrExprContext orExpr() {
			return getRuleContext(OrExprContext.class,0);
		}
		public ExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expression; }
	}

	public final ExpressionContext expression() throws RecognitionException {
		ExpressionContext _localctx = new ExpressionContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_expression);
		try {
			setState(230);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,19,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(228);
				lambdaExpr();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(229);
				orExpr();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LambdaExprContext extends ParserRuleContext {
		public LambdaExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_lambdaExpr; }
	 
		public LambdaExprContext() { }
		public void copyFrom(LambdaExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MultiParamLambdaContext extends LambdaExprContext {
		public TerminalNode LPAREN() { return getToken(HassoobArabiParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(HassoobArabiParser.RPAREN, 0); }
		public TerminalNode ARROW() { return getToken(HassoobArabiParser.ARROW, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public ParamListContext paramList() {
			return getRuleContext(ParamListContext.class,0);
		}
		public MultiParamLambdaContext(LambdaExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SingleParamLambdaContext extends LambdaExprContext {
		public TerminalNode IDENTIFIER() { return getToken(HassoobArabiParser.IDENTIFIER, 0); }
		public TerminalNode ARROW() { return getToken(HassoobArabiParser.ARROW, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public SingleParamLambdaContext(LambdaExprContext ctx) { copyFrom(ctx); }
	}

	public final LambdaExprContext lambdaExpr() throws RecognitionException {
		LambdaExprContext _localctx = new LambdaExprContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_lambdaExpr);
		int _la;
		try {
			setState(242);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case IDENTIFIER:
				_localctx = new SingleParamLambdaContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(232);
				match(IDENTIFIER);
				setState(233);
				match(ARROW);
				setState(234);
				expression();
				}
				break;
			case LPAREN:
				_localctx = new MultiParamLambdaContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(235);
				match(LPAREN);
				setState(237);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==IDENTIFIER) {
					{
					setState(236);
					paramList();
					}
				}

				setState(239);
				match(RPAREN);
				setState(240);
				match(ARROW);
				setState(241);
				expression();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class OrExprContext extends ParserRuleContext {
		public List<AndExprContext> andExpr() {
			return getRuleContexts(AndExprContext.class);
		}
		public AndExprContext andExpr(int i) {
			return getRuleContext(AndExprContext.class,i);
		}
		public List<TerminalNode> OR() { return getTokens(HassoobArabiParser.OR); }
		public TerminalNode OR(int i) {
			return getToken(HassoobArabiParser.OR, i);
		}
		public OrExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_orExpr; }
	}

	public final OrExprContext orExpr() throws RecognitionException {
		OrExprContext _localctx = new OrExprContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_orExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(244);
			andExpr();
			setState(249);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==OR) {
				{
				{
				setState(245);
				match(OR);
				setState(246);
				andExpr();
				}
				}
				setState(251);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AndExprContext extends ParserRuleContext {
		public List<NotExprContext> notExpr() {
			return getRuleContexts(NotExprContext.class);
		}
		public NotExprContext notExpr(int i) {
			return getRuleContext(NotExprContext.class,i);
		}
		public List<TerminalNode> AND() { return getTokens(HassoobArabiParser.AND); }
		public TerminalNode AND(int i) {
			return getToken(HassoobArabiParser.AND, i);
		}
		public AndExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_andExpr; }
	}

	public final AndExprContext andExpr() throws RecognitionException {
		AndExprContext _localctx = new AndExprContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_andExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(252);
			notExpr();
			setState(257);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==AND) {
				{
				{
				setState(253);
				match(AND);
				setState(254);
				notExpr();
				}
				}
				setState(259);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NotExprContext extends ParserRuleContext {
		public NotExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_notExpr; }
	 
		public NotExprContext() { }
		public void copyFrom(NotExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NotExpressionContext extends NotExprContext {
		public TerminalNode NOT() { return getToken(HassoobArabiParser.NOT, 0); }
		public NotExprContext notExpr() {
			return getRuleContext(NotExprContext.class,0);
		}
		public NotExpressionContext(NotExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PassThroughNotContext extends NotExprContext {
		public EqualityExprContext equalityExpr() {
			return getRuleContext(EqualityExprContext.class,0);
		}
		public PassThroughNotContext(NotExprContext ctx) { copyFrom(ctx); }
	}

	public final NotExprContext notExpr() throws RecognitionException {
		NotExprContext _localctx = new NotExprContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_notExpr);
		try {
			setState(263);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case NOT:
				_localctx = new NotExpressionContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(260);
				match(NOT);
				setState(261);
				notExpr();
				}
				break;
			case SAHIH:
			case KHATA:
			case FARIG:
			case PI_CONST:
			case E_CONST:
			case INF_CONST:
			case PLUS:
			case MINUS:
			case LPAREN:
			case LBRACKET:
			case INTEGER_LIT:
			case FLOAT_LIT:
			case STRING_LIT:
			case FSTRING_LIT:
			case IDENTIFIER:
				_localctx = new PassThroughNotContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(262);
				equalityExpr();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class EqualityExprContext extends ParserRuleContext {
		public List<RelationalExprContext> relationalExpr() {
			return getRuleContexts(RelationalExprContext.class);
		}
		public RelationalExprContext relationalExpr(int i) {
			return getRuleContext(RelationalExprContext.class,i);
		}
		public List<TerminalNode> EQ() { return getTokens(HassoobArabiParser.EQ); }
		public TerminalNode EQ(int i) {
			return getToken(HassoobArabiParser.EQ, i);
		}
		public List<TerminalNode> NEQ() { return getTokens(HassoobArabiParser.NEQ); }
		public TerminalNode NEQ(int i) {
			return getToken(HassoobArabiParser.NEQ, i);
		}
		public EqualityExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_equalityExpr; }
	}

	public final EqualityExprContext equalityExpr() throws RecognitionException {
		EqualityExprContext _localctx = new EqualityExprContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_equalityExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(265);
			relationalExpr();
			setState(270);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==EQ || _la==NEQ) {
				{
				{
				setState(266);
				_la = _input.LA(1);
				if ( !(_la==EQ || _la==NEQ) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(267);
				relationalExpr();
				}
				}
				setState(272);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RelationalExprContext extends ParserRuleContext {
		public List<AddExprContext> addExpr() {
			return getRuleContexts(AddExprContext.class);
		}
		public AddExprContext addExpr(int i) {
			return getRuleContext(AddExprContext.class,i);
		}
		public List<TerminalNode> LT() { return getTokens(HassoobArabiParser.LT); }
		public TerminalNode LT(int i) {
			return getToken(HassoobArabiParser.LT, i);
		}
		public List<TerminalNode> LTE() { return getTokens(HassoobArabiParser.LTE); }
		public TerminalNode LTE(int i) {
			return getToken(HassoobArabiParser.LTE, i);
		}
		public List<TerminalNode> GT() { return getTokens(HassoobArabiParser.GT); }
		public TerminalNode GT(int i) {
			return getToken(HassoobArabiParser.GT, i);
		}
		public List<TerminalNode> GTE() { return getTokens(HassoobArabiParser.GTE); }
		public TerminalNode GTE(int i) {
			return getToken(HassoobArabiParser.GTE, i);
		}
		public RelationalExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_relationalExpr; }
	}

	public final RelationalExprContext relationalExpr() throws RecognitionException {
		RelationalExprContext _localctx = new RelationalExprContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_relationalExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(273);
			addExpr();
			setState(278);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 65970697666560L) != 0)) {
				{
				{
				setState(274);
				_la = _input.LA(1);
				if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 65970697666560L) != 0)) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(275);
				addExpr();
				}
				}
				setState(280);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AddExprContext extends ParserRuleContext {
		public List<MulExprContext> mulExpr() {
			return getRuleContexts(MulExprContext.class);
		}
		public MulExprContext mulExpr(int i) {
			return getRuleContext(MulExprContext.class,i);
		}
		public List<TerminalNode> PLUS() { return getTokens(HassoobArabiParser.PLUS); }
		public TerminalNode PLUS(int i) {
			return getToken(HassoobArabiParser.PLUS, i);
		}
		public List<TerminalNode> MINUS() { return getTokens(HassoobArabiParser.MINUS); }
		public TerminalNode MINUS(int i) {
			return getToken(HassoobArabiParser.MINUS, i);
		}
		public List<TerminalNode> STR_CONCAT() { return getTokens(HassoobArabiParser.STR_CONCAT); }
		public TerminalNode STR_CONCAT(int i) {
			return getToken(HassoobArabiParser.STR_CONCAT, i);
		}
		public AddExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_addExpr; }
	}

	public final AddExprContext addExpr() throws RecognitionException {
		AddExprContext _localctx = new AddExprContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_addExpr);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(281);
			mulExpr();
			setState(286);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,27,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(282);
					_la = _input.LA(1);
					if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 15032385536L) != 0)) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					setState(283);
					mulExpr();
					}
					} 
				}
				setState(288);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,27,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class MulExprContext extends ParserRuleContext {
		public List<UnaryExprContext> unaryExpr() {
			return getRuleContexts(UnaryExprContext.class);
		}
		public UnaryExprContext unaryExpr(int i) {
			return getRuleContext(UnaryExprContext.class,i);
		}
		public List<TerminalNode> STAR() { return getTokens(HassoobArabiParser.STAR); }
		public TerminalNode STAR(int i) {
			return getToken(HassoobArabiParser.STAR, i);
		}
		public List<TerminalNode> SLASH() { return getTokens(HassoobArabiParser.SLASH); }
		public TerminalNode SLASH(int i) {
			return getToken(HassoobArabiParser.SLASH, i);
		}
		public List<TerminalNode> INT_DIV() { return getTokens(HassoobArabiParser.INT_DIV); }
		public TerminalNode INT_DIV(int i) {
			return getToken(HassoobArabiParser.INT_DIV, i);
		}
		public List<TerminalNode> PERCENT() { return getTokens(HassoobArabiParser.PERCENT); }
		public TerminalNode PERCENT(int i) {
			return getToken(HassoobArabiParser.PERCENT, i);
		}
		public List<TerminalNode> MAT_MUL() { return getTokens(HassoobArabiParser.MAT_MUL); }
		public TerminalNode MAT_MUL(int i) {
			return getToken(HassoobArabiParser.MAT_MUL, i);
		}
		public MulExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mulExpr; }
	}

	public final MulExprContext mulExpr() throws RecognitionException {
		MulExprContext _localctx = new MulExprContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_mulExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(289);
			unaryExpr();
			setState(294);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 258771779584L) != 0)) {
				{
				{
				setState(290);
				_la = _input.LA(1);
				if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 258771779584L) != 0)) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(291);
				unaryExpr();
				}
				}
				setState(296);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UnaryExprContext extends ParserRuleContext {
		public UnaryExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unaryExpr; }
	 
		public UnaryExprContext() { }
		public void copyFrom(UnaryExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PassThroughUnaryContext extends UnaryExprContext {
		public PowerExprContext powerExpr() {
			return getRuleContext(PowerExprContext.class,0);
		}
		public PassThroughUnaryContext(UnaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnaryPlusContext extends UnaryExprContext {
		public TerminalNode PLUS() { return getToken(HassoobArabiParser.PLUS, 0); }
		public UnaryExprContext unaryExpr() {
			return getRuleContext(UnaryExprContext.class,0);
		}
		public UnaryPlusContext(UnaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnaryMinusContext extends UnaryExprContext {
		public TerminalNode MINUS() { return getToken(HassoobArabiParser.MINUS, 0); }
		public UnaryExprContext unaryExpr() {
			return getRuleContext(UnaryExprContext.class,0);
		}
		public UnaryMinusContext(UnaryExprContext ctx) { copyFrom(ctx); }
	}

	public final UnaryExprContext unaryExpr() throws RecognitionException {
		UnaryExprContext _localctx = new UnaryExprContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_unaryExpr);
		try {
			setState(302);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case MINUS:
				_localctx = new UnaryMinusContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(297);
				match(MINUS);
				setState(298);
				unaryExpr();
				}
				break;
			case PLUS:
				_localctx = new UnaryPlusContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(299);
				match(PLUS);
				setState(300);
				unaryExpr();
				}
				break;
			case SAHIH:
			case KHATA:
			case FARIG:
			case PI_CONST:
			case E_CONST:
			case INF_CONST:
			case LPAREN:
			case LBRACKET:
			case INTEGER_LIT:
			case FLOAT_LIT:
			case STRING_LIT:
			case FSTRING_LIT:
			case IDENTIFIER:
				_localctx = new PassThroughUnaryContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(301);
				powerExpr();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PowerExprContext extends ParserRuleContext {
		public PostfixExprContext postfixExpr() {
			return getRuleContext(PostfixExprContext.class,0);
		}
		public TerminalNode CARET() { return getToken(HassoobArabiParser.CARET, 0); }
		public UnaryExprContext unaryExpr() {
			return getRuleContext(UnaryExprContext.class,0);
		}
		public PowerExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_powerExpr; }
	}

	public final PowerExprContext powerExpr() throws RecognitionException {
		PowerExprContext _localctx = new PowerExprContext(_ctx, getState());
		enterRule(_localctx, 60, RULE_powerExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(304);
			postfixExpr();
			setState(307);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==CARET) {
				{
				setState(305);
				match(CARET);
				setState(306);
				unaryExpr();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PostfixExprContext extends ParserRuleContext {
		public PrimaryContext primary() {
			return getRuleContext(PrimaryContext.class,0);
		}
		public List<TerminalNode> LPAREN() { return getTokens(HassoobArabiParser.LPAREN); }
		public TerminalNode LPAREN(int i) {
			return getToken(HassoobArabiParser.LPAREN, i);
		}
		public List<TerminalNode> RPAREN() { return getTokens(HassoobArabiParser.RPAREN); }
		public TerminalNode RPAREN(int i) {
			return getToken(HassoobArabiParser.RPAREN, i);
		}
		public List<TerminalNode> LBRACKET() { return getTokens(HassoobArabiParser.LBRACKET); }
		public TerminalNode LBRACKET(int i) {
			return getToken(HassoobArabiParser.LBRACKET, i);
		}
		public List<IndexListContext> indexList() {
			return getRuleContexts(IndexListContext.class);
		}
		public IndexListContext indexList(int i) {
			return getRuleContext(IndexListContext.class,i);
		}
		public List<TerminalNode> RBRACKET() { return getTokens(HassoobArabiParser.RBRACKET); }
		public TerminalNode RBRACKET(int i) {
			return getToken(HassoobArabiParser.RBRACKET, i);
		}
		public List<ArgListContext> argList() {
			return getRuleContexts(ArgListContext.class);
		}
		public ArgListContext argList(int i) {
			return getRuleContext(ArgListContext.class,i);
		}
		public PostfixExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_postfixExpr; }
	}

	public final PostfixExprContext postfixExpr() throws RecognitionException {
		PostfixExprContext _localctx = new PostfixExprContext(_ctx, getState());
		enterRule(_localctx, 62, RULE_postfixExpr);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(309);
			primary();
			setState(321);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,33,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					setState(319);
					_errHandler.sync(this);
					switch (_input.LA(1)) {
					case LPAREN:
						{
						setState(310);
						match(LPAREN);
						setState(312);
						_errHandler.sync(this);
						_la = _input.LA(1);
						if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 4468274530683379712L) != 0)) {
							{
							setState(311);
							argList();
							}
						}

						setState(314);
						match(RPAREN);
						}
						break;
					case LBRACKET:
						{
						setState(315);
						match(LBRACKET);
						setState(316);
						indexList();
						setState(317);
						match(RBRACKET);
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					} 
				}
				setState(323);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,33,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ArgListContext extends ParserRuleContext {
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public List<TerminalNode> IDENTIFIER() { return getTokens(HassoobArabiParser.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(HassoobArabiParser.IDENTIFIER, i);
		}
		public List<TerminalNode> ASSIGN() { return getTokens(HassoobArabiParser.ASSIGN); }
		public TerminalNode ASSIGN(int i) {
			return getToken(HassoobArabiParser.ASSIGN, i);
		}
		public List<TerminalNode> COMMA() { return getTokens(HassoobArabiParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(HassoobArabiParser.COMMA, i);
		}
		public ArgListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_argList; }
	}

	public final ArgListContext argList() throws RecognitionException {
		ArgListContext _localctx = new ArgListContext(_ctx, getState());
		enterRule(_localctx, 64, RULE_argList);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(326);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,34,_ctx) ) {
			case 1:
				{
				setState(324);
				match(IDENTIFIER);
				setState(325);
				match(ASSIGN);
				}
				break;
			}
			setState(328);
			expression();
			setState(337);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(329);
				match(COMMA);
				setState(332);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,35,_ctx) ) {
				case 1:
					{
					setState(330);
					match(IDENTIFIER);
					setState(331);
					match(ASSIGN);
					}
					break;
				}
				setState(334);
				expression();
				}
				}
				setState(339);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrimaryContext extends ParserRuleContext {
		public PrimaryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_primary; }
	 
		public PrimaryContext() { }
		public void copyFrom(PrimaryContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FloatLiteralContext extends PrimaryContext {
		public TerminalNode FLOAT_LIT() { return getToken(HassoobArabiParser.FLOAT_LIT, 0); }
		public FloatLiteralContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class InfinityConstantContext extends PrimaryContext {
		public TerminalNode INF_CONST() { return getToken(HassoobArabiParser.INF_CONST, 0); }
		public InfinityConstantContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FalseLiteralContext extends PrimaryContext {
		public TerminalNode KHATA() { return getToken(HassoobArabiParser.KHATA, 0); }
		public FalseLiteralContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StringLiteralContext extends PrimaryContext {
		public TerminalNode STRING_LIT() { return getToken(HassoobArabiParser.STRING_LIT, 0); }
		public StringLiteralContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TrueLiteralContext extends PrimaryContext {
		public TerminalNode SAHIH() { return getToken(HassoobArabiParser.SAHIH, 0); }
		public TrueLiteralContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IdentifierExprContext extends PrimaryContext {
		public TerminalNode IDENTIFIER() { return getToken(HassoobArabiParser.IDENTIFIER, 0); }
		public IdentifierExprContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FStringLiteralContext extends PrimaryContext {
		public TerminalNode FSTRING_LIT() { return getToken(HassoobArabiParser.FSTRING_LIT, 0); }
		public FStringLiteralContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TupleLiteralContext extends PrimaryContext {
		public TerminalNode LPAREN() { return getToken(HassoobArabiParser.LPAREN, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(HassoobArabiParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(HassoobArabiParser.COMMA, i);
		}
		public TerminalNode RPAREN() { return getToken(HassoobArabiParser.RPAREN, 0); }
		public TupleLiteralContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IntLiteralContext extends PrimaryContext {
		public TerminalNode INTEGER_LIT() { return getToken(HassoobArabiParser.INTEGER_LIT, 0); }
		public IntLiteralContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PiConstantContext extends PrimaryContext {
		public TerminalNode PI_CONST() { return getToken(HassoobArabiParser.PI_CONST, 0); }
		public PiConstantContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ListExprContext extends PrimaryContext {
		public ListLiteralContext listLiteral() {
			return getRuleContext(ListLiteralContext.class,0);
		}
		public ListExprContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParenExprContext extends PrimaryContext {
		public TerminalNode LPAREN() { return getToken(HassoobArabiParser.LPAREN, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(HassoobArabiParser.RPAREN, 0); }
		public ParenExprContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NullLiteralContext extends PrimaryContext {
		public TerminalNode FARIG() { return getToken(HassoobArabiParser.FARIG, 0); }
		public NullLiteralContext(PrimaryContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class EulerConstantContext extends PrimaryContext {
		public TerminalNode E_CONST() { return getToken(HassoobArabiParser.E_CONST, 0); }
		public EulerConstantContext(PrimaryContext ctx) { copyFrom(ctx); }
	}

	public final PrimaryContext primary() throws RecognitionException {
		PrimaryContext _localctx = new PrimaryContext(_ctx, getState());
		enterRule(_localctx, 66, RULE_primary);
		int _la;
		try {
			setState(369);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,38,_ctx) ) {
			case 1:
				_localctx = new IntLiteralContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(340);
				match(INTEGER_LIT);
				}
				break;
			case 2:
				_localctx = new FloatLiteralContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(341);
				match(FLOAT_LIT);
				}
				break;
			case 3:
				_localctx = new StringLiteralContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(342);
				match(STRING_LIT);
				}
				break;
			case 4:
				_localctx = new FStringLiteralContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(343);
				match(FSTRING_LIT);
				}
				break;
			case 5:
				_localctx = new PiConstantContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(344);
				match(PI_CONST);
				}
				break;
			case 6:
				_localctx = new EulerConstantContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(345);
				match(E_CONST);
				}
				break;
			case 7:
				_localctx = new InfinityConstantContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(346);
				match(INF_CONST);
				}
				break;
			case 8:
				_localctx = new TrueLiteralContext(_localctx);
				enterOuterAlt(_localctx, 8);
				{
				setState(347);
				match(SAHIH);
				}
				break;
			case 9:
				_localctx = new FalseLiteralContext(_localctx);
				enterOuterAlt(_localctx, 9);
				{
				setState(348);
				match(KHATA);
				}
				break;
			case 10:
				_localctx = new NullLiteralContext(_localctx);
				enterOuterAlt(_localctx, 10);
				{
				setState(349);
				match(FARIG);
				}
				break;
			case 11:
				_localctx = new IdentifierExprContext(_localctx);
				enterOuterAlt(_localctx, 11);
				{
				setState(350);
				match(IDENTIFIER);
				}
				break;
			case 12:
				_localctx = new ListExprContext(_localctx);
				enterOuterAlt(_localctx, 12);
				{
				setState(351);
				listLiteral();
				}
				break;
			case 13:
				_localctx = new ParenExprContext(_localctx);
				enterOuterAlt(_localctx, 13);
				{
				setState(352);
				match(LPAREN);
				setState(353);
				expression();
				setState(354);
				match(RPAREN);
				}
				break;
			case 14:
				_localctx = new TupleLiteralContext(_localctx);
				enterOuterAlt(_localctx, 14);
				{
				setState(356);
				match(LPAREN);
				setState(357);
				expression();
				setState(358);
				match(COMMA);
				setState(359);
				expression();
				setState(364);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==COMMA) {
					{
					{
					setState(360);
					match(COMMA);
					setState(361);
					expression();
					}
					}
					setState(366);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(367);
				match(RPAREN);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ListLiteralContext extends ParserRuleContext {
		public TerminalNode LBRACKET() { return getToken(HassoobArabiParser.LBRACKET, 0); }
		public TerminalNode RBRACKET() { return getToken(HassoobArabiParser.RBRACKET, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(HassoobArabiParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(HassoobArabiParser.COMMA, i);
		}
		public ListLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_listLiteral; }
	}

	public final ListLiteralContext listLiteral() throws RecognitionException {
		ListLiteralContext _localctx = new ListLiteralContext(_ctx, getState());
		enterRule(_localctx, 68, RULE_listLiteral);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(371);
			match(LBRACKET);
			setState(380);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 4468274530683379712L) != 0)) {
				{
				setState(372);
				expression();
				setState(377);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==COMMA) {
					{
					{
					setState(373);
					match(COMMA);
					setState(374);
					expression();
					}
					}
					setState(379);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(382);
			match(RBRACKET);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class IndexListContext extends ParserRuleContext {
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(HassoobArabiParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(HassoobArabiParser.COMMA, i);
		}
		public IndexListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_indexList; }
	}

	public final IndexListContext indexList() throws RecognitionException {
		IndexListContext _localctx = new IndexListContext(_ctx, getState());
		enterRule(_localctx, 70, RULE_indexList);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(384);
			expression();
			setState(389);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(385);
				match(COMMA);
				setState(386);
				expression();
				}
				}
				setState(391);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001A\u0189\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007\u0012"+
		"\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002\u0015\u0007\u0015"+
		"\u0002\u0016\u0007\u0016\u0002\u0017\u0007\u0017\u0002\u0018\u0007\u0018"+
		"\u0002\u0019\u0007\u0019\u0002\u001a\u0007\u001a\u0002\u001b\u0007\u001b"+
		"\u0002\u001c\u0007\u001c\u0002\u001d\u0007\u001d\u0002\u001e\u0007\u001e"+
		"\u0002\u001f\u0007\u001f\u0002 \u0007 \u0002!\u0007!\u0002\"\u0007\"\u0002"+
		"#\u0007#\u0001\u0000\u0005\u0000J\b\u0000\n\u0000\f\u0000M\t\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0003\u0001^\b\u0001\u0001\u0002\u0001"+
		"\u0002\u0001\u0002\u0001\u0002\u0003\u0002d\b\u0002\u0001\u0002\u0001"+
		"\u0002\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0005\u0003l\b"+
		"\u0003\n\u0003\f\u0003o\t\u0003\u0001\u0004\u0001\u0004\u0005\u0004s\b"+
		"\u0004\n\u0004\f\u0004v\t\u0004\u0001\u0004\u0001\u0004\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005\u0080"+
		"\b\u0005\n\u0005\f\u0005\u0083\t\u0005\u0001\u0005\u0003\u0005\u0086\b"+
		"\u0005\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001"+
		"\u0006\u0001\u0006\u0001\u0007\u0001\u0007\u0001\u0007\u0001\b\u0001\b"+
		"\u0001\b\u0001\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t\u0001\t\u0001"+
		"\t\u0001\t\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001"+
		"\n\u0003\n\u00a6\b\n\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0003\u000b"+
		"\u00ac\b\u000b\u0001\u000b\u0003\u000b\u00af\b\u000b\u0001\f\u0001\f\u0003"+
		"\f\u00b3\b\f\u0001\r\u0001\r\u0003\r\u00b7\b\r\u0001\u000e\u0001\u000e"+
		"\u0001\u000e\u0001\u000e\u0005\u000e\u00bd\b\u000e\n\u000e\f\u000e\u00c0"+
		"\t\u000e\u0001\u000e\u0003\u000e\u00c3\b\u000e\u0001\u000f\u0001\u000f"+
		"\u0001\u000f\u0001\u000f\u0003\u000f\u00c9\b\u000f\u0001\u0010\u0001\u0010"+
		"\u0001\u0010\u0001\u0010\u0003\u0010\u00cf\b\u0010\u0001\u0011\u0001\u0011"+
		"\u0001\u0012\u0001\u0012\u0001\u0012\u0001\u0012\u0001\u0012\u0004\u0012"+
		"\u00d8\b\u0012\u000b\u0012\f\u0012\u00d9\u0001\u0012\u0001\u0012\u0001"+
		"\u0012\u0003\u0012\u00df\b\u0012\u0001\u0013\u0001\u0013\u0003\u0013\u00e3"+
		"\b\u0013\u0001\u0014\u0001\u0014\u0003\u0014\u00e7\b\u0014\u0001\u0015"+
		"\u0001\u0015\u0001\u0015\u0001\u0015\u0001\u0015\u0003\u0015\u00ee\b\u0015"+
		"\u0001\u0015\u0001\u0015\u0001\u0015\u0003\u0015\u00f3\b\u0015\u0001\u0016"+
		"\u0001\u0016\u0001\u0016\u0005\u0016\u00f8\b\u0016\n\u0016\f\u0016\u00fb"+
		"\t\u0016\u0001\u0017\u0001\u0017\u0001\u0017\u0005\u0017\u0100\b\u0017"+
		"\n\u0017\f\u0017\u0103\t\u0017\u0001\u0018\u0001\u0018\u0001\u0018\u0003"+
		"\u0018\u0108\b\u0018\u0001\u0019\u0001\u0019\u0001\u0019\u0005\u0019\u010d"+
		"\b\u0019\n\u0019\f\u0019\u0110\t\u0019\u0001\u001a\u0001\u001a\u0001\u001a"+
		"\u0005\u001a\u0115\b\u001a\n\u001a\f\u001a\u0118\t\u001a\u0001\u001b\u0001"+
		"\u001b\u0001\u001b\u0005\u001b\u011d\b\u001b\n\u001b\f\u001b\u0120\t\u001b"+
		"\u0001\u001c\u0001\u001c\u0001\u001c\u0005\u001c\u0125\b\u001c\n\u001c"+
		"\f\u001c\u0128\t\u001c\u0001\u001d\u0001\u001d\u0001\u001d\u0001\u001d"+
		"\u0001\u001d\u0003\u001d\u012f\b\u001d\u0001\u001e\u0001\u001e\u0001\u001e"+
		"\u0003\u001e\u0134\b\u001e\u0001\u001f\u0001\u001f\u0001\u001f\u0003\u001f"+
		"\u0139\b\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f"+
		"\u0005\u001f\u0140\b\u001f\n\u001f\f\u001f\u0143\t\u001f\u0001 \u0001"+
		" \u0003 \u0147\b \u0001 \u0001 \u0001 \u0001 \u0003 \u014d\b \u0001 \u0005"+
		" \u0150\b \n \f \u0153\t \u0001!\u0001!\u0001!\u0001!\u0001!\u0001!\u0001"+
		"!\u0001!\u0001!\u0001!\u0001!\u0001!\u0001!\u0001!\u0001!\u0001!\u0001"+
		"!\u0001!\u0001!\u0001!\u0001!\u0001!\u0005!\u016b\b!\n!\f!\u016e\t!\u0001"+
		"!\u0001!\u0003!\u0172\b!\u0001\"\u0001\"\u0001\"\u0001\"\u0005\"\u0178"+
		"\b\"\n\"\f\"\u017b\t\"\u0003\"\u017d\b\"\u0001\"\u0001\"\u0001#\u0001"+
		"#\u0001#\u0005#\u0184\b#\n#\f#\u0187\t#\u0001#\u0000\u0000$\u0000\u0002"+
		"\u0004\u0006\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u001e"+
		" \"$&(*,.02468:<>@BDF\u0000\u0005\u0001\u0000\u0017\u001d\u0001\u0000"+
		"()\u0001\u0000*-\u0001\u0000\u001f!\u0002\u0000\u001e\u001e\"%\u01a6\u0000"+
		"K\u0001\u0000\u0000\u0000\u0002]\u0001\u0000\u0000\u0000\u0004_\u0001"+
		"\u0000\u0000\u0000\u0006h\u0001\u0000\u0000\u0000\bp\u0001\u0000\u0000"+
		"\u0000\ny\u0001\u0000\u0000\u0000\f\u0087\u0001\u0000\u0000\u0000\u000e"+
		"\u008e\u0001\u0000\u0000\u0000\u0010\u0091\u0001\u0000\u0000\u0000\u0012"+
		"\u0097\u0001\u0000\u0000\u0000\u0014\u009d\u0001\u0000\u0000\u0000\u0016"+
		"\u00a9\u0001\u0000\u0000\u0000\u0018\u00b0\u0001\u0000\u0000\u0000\u001a"+
		"\u00b4\u0001\u0000\u0000\u0000\u001c\u00b8\u0001\u0000\u0000\u0000\u001e"+
		"\u00c4\u0001\u0000\u0000\u0000 \u00ca\u0001\u0000\u0000\u0000\"\u00d0"+
		"\u0001\u0000\u0000\u0000$\u00d2\u0001\u0000\u0000\u0000&\u00e0\u0001\u0000"+
		"\u0000\u0000(\u00e6\u0001\u0000\u0000\u0000*\u00f2\u0001\u0000\u0000\u0000"+
		",\u00f4\u0001\u0000\u0000\u0000.\u00fc\u0001\u0000\u0000\u00000\u0107"+
		"\u0001\u0000\u0000\u00002\u0109\u0001\u0000\u0000\u00004\u0111\u0001\u0000"+
		"\u0000\u00006\u0119\u0001\u0000\u0000\u00008\u0121\u0001\u0000\u0000\u0000"+
		":\u012e\u0001\u0000\u0000\u0000<\u0130\u0001\u0000\u0000\u0000>\u0135"+
		"\u0001\u0000\u0000\u0000@\u0146\u0001\u0000\u0000\u0000B\u0171\u0001\u0000"+
		"\u0000\u0000D\u0173\u0001\u0000\u0000\u0000F\u0180\u0001\u0000\u0000\u0000"+
		"HJ\u0003\u0002\u0001\u0000IH\u0001\u0000\u0000\u0000JM\u0001\u0000\u0000"+
		"\u0000KI\u0001\u0000\u0000\u0000KL\u0001\u0000\u0000\u0000LN\u0001\u0000"+
		"\u0000\u0000MK\u0001\u0000\u0000\u0000NO\u0005\u0000\u0000\u0001O\u0001"+
		"\u0001\u0000\u0000\u0000P^\u0003\u0004\u0002\u0000Q^\u0003\n\u0005\u0000"+
		"R^\u0003\u0010\b\u0000S^\u0003\u0012\t\u0000T^\u0003\u0014\n\u0000U^\u0003"+
		"\u0016\u000b\u0000V^\u0003\u0018\f\u0000W^\u0003\u001a\r\u0000X^\u0003"+
		"\u001c\u000e\u0000Y^\u0003\u001e\u000f\u0000Z^\u0003 \u0010\u0000[^\u0003"+
		"$\u0012\u0000\\^\u0003&\u0013\u0000]P\u0001\u0000\u0000\u0000]Q\u0001"+
		"\u0000\u0000\u0000]R\u0001\u0000\u0000\u0000]S\u0001\u0000\u0000\u0000"+
		"]T\u0001\u0000\u0000\u0000]U\u0001\u0000\u0000\u0000]V\u0001\u0000\u0000"+
		"\u0000]W\u0001\u0000\u0000\u0000]X\u0001\u0000\u0000\u0000]Y\u0001\u0000"+
		"\u0000\u0000]Z\u0001\u0000\u0000\u0000][\u0001\u0000\u0000\u0000]\\\u0001"+
		"\u0000\u0000\u0000^\u0003\u0001\u0000\u0000\u0000_`\u0005\t\u0000\u0000"+
		"`a\u0005=\u0000\u0000ac\u0005/\u0000\u0000bd\u0003\u0006\u0003\u0000c"+
		"b\u0001\u0000\u0000\u0000cd\u0001\u0000\u0000\u0000de\u0001\u0000\u0000"+
		"\u0000ef\u00050\u0000\u0000fg\u0003\b\u0004\u0000g\u0005\u0001\u0000\u0000"+
		"\u0000hm\u0005=\u0000\u0000ij\u00055\u0000\u0000jl\u0005=\u0000\u0000"+
		"ki\u0001\u0000\u0000\u0000lo\u0001\u0000\u0000\u0000mk\u0001\u0000\u0000"+
		"\u0000mn\u0001\u0000\u0000\u0000n\u0007\u0001\u0000\u0000\u0000om\u0001"+
		"\u0000\u0000\u0000pt\u00053\u0000\u0000qs\u0003\u0002\u0001\u0000rq\u0001"+
		"\u0000\u0000\u0000sv\u0001\u0000\u0000\u0000tr\u0001\u0000\u0000\u0000"+
		"tu\u0001\u0000\u0000\u0000uw\u0001\u0000\u0000\u0000vt\u0001\u0000\u0000"+
		"\u0000wx\u00054\u0000\u0000x\t\u0001\u0000\u0000\u0000yz\u0005\u0001\u0000"+
		"\u0000z{\u0005/\u0000\u0000{|\u0003(\u0014\u0000|}\u00050\u0000\u0000"+
		"}\u0081\u0003\b\u0004\u0000~\u0080\u0003\f\u0006\u0000\u007f~\u0001\u0000"+
		"\u0000\u0000\u0080\u0083\u0001\u0000\u0000\u0000\u0081\u007f\u0001\u0000"+
		"\u0000\u0000\u0081\u0082\u0001\u0000\u0000\u0000\u0082\u0085\u0001\u0000"+
		"\u0000\u0000\u0083\u0081\u0001\u0000\u0000\u0000\u0084\u0086\u0003\u000e"+
		"\u0007\u0000\u0085\u0084\u0001\u0000\u0000\u0000\u0085\u0086\u0001\u0000"+
		"\u0000\u0000\u0086\u000b\u0001\u0000\u0000\u0000\u0087\u0088\u0005\u0002"+
		"\u0000\u0000\u0088\u0089\u0005\u0001\u0000\u0000\u0089\u008a\u0005/\u0000"+
		"\u0000\u008a\u008b\u0003(\u0014\u0000\u008b\u008c\u00050\u0000\u0000\u008c"+
		"\u008d\u0003\b\u0004\u0000\u008d\r\u0001\u0000\u0000\u0000\u008e\u008f"+
		"\u0005\u0002\u0000\u0000\u008f\u0090\u0003\b\u0004\u0000\u0090\u000f\u0001"+
		"\u0000\u0000\u0000\u0091\u0092\u0005\u0003\u0000\u0000\u0092\u0093\u0005"+
		"/\u0000\u0000\u0093\u0094\u0003(\u0014\u0000\u0094\u0095\u00050\u0000"+
		"\u0000\u0095\u0096\u0003\b\u0004\u0000\u0096\u0011\u0001\u0000\u0000\u0000"+
		"\u0097\u0098\u0005\u0004\u0000\u0000\u0098\u0099\u0005=\u0000\u0000\u0099"+
		"\u009a\u0005\u0007\u0000\u0000\u009a\u009b\u0003(\u0014\u0000\u009b\u009c"+
		"\u0003\b\u0004\u0000\u009c\u0013\u0001\u0000\u0000\u0000\u009d\u009e\u0005"+
		"\u0004\u0000\u0000\u009e\u009f\u0005=\u0000\u0000\u009f\u00a0\u0005\u0005"+
		"\u0000\u0000\u00a0\u00a1\u0003(\u0014\u0000\u00a1\u00a2\u0005\u0006\u0000"+
		"\u0000\u00a2\u00a5\u0003(\u0014\u0000\u00a3\u00a4\u0005\b\u0000\u0000"+
		"\u00a4\u00a6\u0003(\u0014\u0000\u00a5\u00a3\u0001\u0000\u0000\u0000\u00a5"+
		"\u00a6\u0001\u0000\u0000\u0000\u00a6\u00a7\u0001\u0000\u0000\u0000\u00a7"+
		"\u00a8\u0003\b\u0004\u0000\u00a8\u0015\u0001\u0000\u0000\u0000\u00a9\u00ab"+
		"\u0005\n\u0000\u0000\u00aa\u00ac\u0003(\u0014\u0000\u00ab\u00aa\u0001"+
		"\u0000\u0000\u0000\u00ab\u00ac\u0001\u0000\u0000\u0000\u00ac\u00ae\u0001"+
		"\u0000\u0000\u0000\u00ad\u00af\u00056\u0000\u0000\u00ae\u00ad\u0001\u0000"+
		"\u0000\u0000\u00ae\u00af\u0001\u0000\u0000\u0000\u00af\u0017\u0001\u0000"+
		"\u0000\u0000\u00b0\u00b2\u0005\u000b\u0000\u0000\u00b1\u00b3\u00056\u0000"+
		"\u0000\u00b2\u00b1\u0001\u0000\u0000\u0000\u00b2\u00b3\u0001\u0000\u0000"+
		"\u0000\u00b3\u0019\u0001\u0000\u0000\u0000\u00b4\u00b6\u0005\f\u0000\u0000"+
		"\u00b5\u00b7\u00056\u0000\u0000\u00b6\u00b5\u0001\u0000\u0000\u0000\u00b6"+
		"\u00b7\u0001\u0000\u0000\u0000\u00b7\u001b\u0001\u0000\u0000\u0000\u00b8"+
		"\u00b9\u0005\u0010\u0000\u0000\u00b9\u00be\u0005=\u0000\u0000\u00ba\u00bb"+
		"\u00055\u0000\u0000\u00bb\u00bd\u0005=\u0000\u0000\u00bc\u00ba\u0001\u0000"+
		"\u0000\u0000\u00bd\u00c0\u0001\u0000\u0000\u0000\u00be\u00bc\u0001\u0000"+
		"\u0000\u0000\u00be\u00bf\u0001\u0000\u0000\u0000\u00bf\u00c2\u0001\u0000"+
		"\u0000\u0000\u00c0\u00be\u0001\u0000\u0000\u0000\u00c1\u00c3\u00056\u0000"+
		"\u0000\u00c2\u00c1\u0001\u0000\u0000\u0000\u00c2\u00c3\u0001\u0000\u0000"+
		"\u0000\u00c3\u001d\u0001\u0000\u0000\u0000\u00c4\u00c5\u0005=\u0000\u0000"+
		"\u00c5\u00c6\u0005.\u0000\u0000\u00c6\u00c8\u0003(\u0014\u0000\u00c7\u00c9"+
		"\u00056\u0000\u0000\u00c8\u00c7\u0001\u0000\u0000\u0000\u00c8\u00c9\u0001"+
		"\u0000\u0000\u0000\u00c9\u001f\u0001\u0000\u0000\u0000\u00ca\u00cb\u0005"+
		"=\u0000\u0000\u00cb\u00cc\u0003\"\u0011\u0000\u00cc\u00ce\u0003(\u0014"+
		"\u0000\u00cd\u00cf\u00056\u0000\u0000\u00ce\u00cd\u0001\u0000\u0000\u0000"+
		"\u00ce\u00cf\u0001\u0000\u0000\u0000\u00cf!\u0001\u0000\u0000\u0000\u00d0"+
		"\u00d1\u0007\u0000\u0000\u0000\u00d1#\u0001\u0000\u0000\u0000\u00d2\u00d7"+
		"\u0005=\u0000\u0000\u00d3\u00d4\u00051\u0000\u0000\u00d4\u00d5\u0003F"+
		"#\u0000\u00d5\u00d6\u00052\u0000\u0000\u00d6\u00d8\u0001\u0000\u0000\u0000"+
		"\u00d7\u00d3\u0001\u0000\u0000\u0000\u00d8\u00d9\u0001\u0000\u0000\u0000"+
		"\u00d9\u00d7\u0001\u0000\u0000\u0000\u00d9\u00da\u0001\u0000\u0000\u0000"+
		"\u00da\u00db\u0001\u0000\u0000\u0000\u00db\u00dc\u0005.\u0000\u0000\u00dc"+
		"\u00de\u0003(\u0014\u0000\u00dd\u00df\u00056\u0000\u0000\u00de\u00dd\u0001"+
		"\u0000\u0000\u0000\u00de\u00df\u0001\u0000\u0000\u0000\u00df%\u0001\u0000"+
		"\u0000\u0000\u00e0\u00e2\u0003(\u0014\u0000\u00e1\u00e3\u00056\u0000\u0000"+
		"\u00e2\u00e1\u0001\u0000\u0000\u0000\u00e2\u00e3\u0001\u0000\u0000\u0000"+
		"\u00e3\'\u0001\u0000\u0000\u0000\u00e4\u00e7\u0003*\u0015\u0000\u00e5"+
		"\u00e7\u0003,\u0016\u0000\u00e6\u00e4\u0001\u0000\u0000\u0000\u00e6\u00e5"+
		"\u0001\u0000\u0000\u0000\u00e7)\u0001\u0000\u0000\u0000\u00e8\u00e9\u0005"+
		"=\u0000\u0000\u00e9\u00ea\u0005\'\u0000\u0000\u00ea\u00f3\u0003(\u0014"+
		"\u0000\u00eb\u00ed\u0005/\u0000\u0000\u00ec\u00ee\u0003\u0006\u0003\u0000"+
		"\u00ed\u00ec\u0001\u0000\u0000\u0000\u00ed\u00ee\u0001\u0000\u0000\u0000"+
		"\u00ee\u00ef\u0001\u0000\u0000\u0000\u00ef\u00f0\u00050\u0000\u0000\u00f0"+
		"\u00f1\u0005\'\u0000\u0000\u00f1\u00f3\u0003(\u0014\u0000\u00f2\u00e8"+
		"\u0001\u0000\u0000\u0000\u00f2\u00eb\u0001\u0000\u0000\u0000\u00f3+\u0001"+
		"\u0000\u0000\u0000\u00f4\u00f9\u0003.\u0017\u0000\u00f5\u00f6\u0005\u0015"+
		"\u0000\u0000\u00f6\u00f8\u0003.\u0017\u0000\u00f7\u00f5\u0001\u0000\u0000"+
		"\u0000\u00f8\u00fb\u0001\u0000\u0000\u0000\u00f9\u00f7\u0001\u0000\u0000"+
		"\u0000\u00f9\u00fa\u0001\u0000\u0000\u0000\u00fa-\u0001\u0000\u0000\u0000"+
		"\u00fb\u00f9\u0001\u0000\u0000\u0000\u00fc\u0101\u00030\u0018\u0000\u00fd"+
		"\u00fe\u0005\u0014\u0000\u0000\u00fe\u0100\u00030\u0018\u0000\u00ff\u00fd"+
		"\u0001\u0000\u0000\u0000\u0100\u0103\u0001\u0000\u0000\u0000\u0101\u00ff"+
		"\u0001\u0000\u0000\u0000\u0101\u0102\u0001\u0000\u0000\u0000\u0102/\u0001"+
		"\u0000\u0000\u0000\u0103\u0101\u0001\u0000\u0000\u0000\u0104\u0105\u0005"+
		"\u0016\u0000\u0000\u0105\u0108\u00030\u0018\u0000\u0106\u0108\u00032\u0019"+
		"\u0000\u0107\u0104\u0001\u0000\u0000\u0000\u0107\u0106\u0001\u0000\u0000"+
		"\u0000\u01081\u0001\u0000\u0000\u0000\u0109\u010e\u00034\u001a\u0000\u010a"+
		"\u010b\u0007\u0001\u0000\u0000\u010b\u010d\u00034\u001a\u0000\u010c\u010a"+
		"\u0001\u0000\u0000\u0000\u010d\u0110\u0001\u0000\u0000\u0000\u010e\u010c"+
		"\u0001\u0000\u0000\u0000\u010e\u010f\u0001\u0000\u0000\u0000\u010f3\u0001"+
		"\u0000\u0000\u0000\u0110\u010e\u0001\u0000\u0000\u0000\u0111\u0116\u0003"+
		"6\u001b\u0000\u0112\u0113\u0007\u0002\u0000\u0000\u0113\u0115\u00036\u001b"+
		"\u0000\u0114\u0112\u0001\u0000\u0000\u0000\u0115\u0118\u0001\u0000\u0000"+
		"\u0000\u0116\u0114\u0001\u0000\u0000\u0000\u0116\u0117\u0001\u0000\u0000"+
		"\u0000\u01175\u0001\u0000\u0000\u0000\u0118\u0116\u0001\u0000\u0000\u0000"+
		"\u0119\u011e\u00038\u001c\u0000\u011a\u011b\u0007\u0003\u0000\u0000\u011b"+
		"\u011d\u00038\u001c\u0000\u011c\u011a\u0001\u0000\u0000\u0000\u011d\u0120"+
		"\u0001\u0000\u0000\u0000\u011e\u011c\u0001\u0000\u0000\u0000\u011e\u011f"+
		"\u0001\u0000\u0000\u0000\u011f7\u0001\u0000\u0000\u0000\u0120\u011e\u0001"+
		"\u0000\u0000\u0000\u0121\u0126\u0003:\u001d\u0000\u0122\u0123\u0007\u0004"+
		"\u0000\u0000\u0123\u0125\u0003:\u001d\u0000\u0124\u0122\u0001\u0000\u0000"+
		"\u0000\u0125\u0128\u0001\u0000\u0000\u0000\u0126\u0124\u0001\u0000\u0000"+
		"\u0000\u0126\u0127\u0001\u0000\u0000\u0000\u01279\u0001\u0000\u0000\u0000"+
		"\u0128\u0126\u0001\u0000\u0000\u0000\u0129\u012a\u0005!\u0000\u0000\u012a"+
		"\u012f\u0003:\u001d\u0000\u012b\u012c\u0005 \u0000\u0000\u012c\u012f\u0003"+
		":\u001d\u0000\u012d\u012f\u0003<\u001e\u0000\u012e\u0129\u0001\u0000\u0000"+
		"\u0000\u012e\u012b\u0001\u0000\u0000\u0000\u012e\u012d\u0001\u0000\u0000"+
		"\u0000\u012f;\u0001\u0000\u0000\u0000\u0130\u0133\u0003>\u001f\u0000\u0131"+
		"\u0132\u0005&\u0000\u0000\u0132\u0134\u0003:\u001d\u0000\u0133\u0131\u0001"+
		"\u0000\u0000\u0000\u0133\u0134\u0001\u0000\u0000\u0000\u0134=\u0001\u0000"+
		"\u0000\u0000\u0135\u0141\u0003B!\u0000\u0136\u0138\u0005/\u0000\u0000"+
		"\u0137\u0139\u0003@ \u0000\u0138\u0137\u0001\u0000\u0000\u0000\u0138\u0139"+
		"\u0001\u0000\u0000\u0000\u0139\u013a\u0001\u0000\u0000\u0000\u013a\u0140"+
		"\u00050\u0000\u0000\u013b\u013c\u00051\u0000\u0000\u013c\u013d\u0003F"+
		"#\u0000\u013d\u013e\u00052\u0000\u0000\u013e\u0140\u0001\u0000\u0000\u0000"+
		"\u013f\u0136\u0001\u0000\u0000\u0000\u013f\u013b\u0001\u0000\u0000\u0000"+
		"\u0140\u0143\u0001\u0000\u0000\u0000\u0141\u013f\u0001\u0000\u0000\u0000"+
		"\u0141\u0142\u0001\u0000\u0000\u0000\u0142?\u0001\u0000\u0000\u0000\u0143"+
		"\u0141\u0001\u0000\u0000\u0000\u0144\u0145\u0005=\u0000\u0000\u0145\u0147"+
		"\u0005.\u0000\u0000\u0146\u0144\u0001\u0000\u0000\u0000\u0146\u0147\u0001"+
		"\u0000\u0000\u0000\u0147\u0148\u0001\u0000\u0000\u0000\u0148\u0151\u0003"+
		"(\u0014\u0000\u0149\u014c\u00055\u0000\u0000\u014a\u014b\u0005=\u0000"+
		"\u0000\u014b\u014d\u0005.\u0000\u0000\u014c\u014a\u0001\u0000\u0000\u0000"+
		"\u014c\u014d\u0001\u0000\u0000\u0000\u014d\u014e\u0001\u0000\u0000\u0000"+
		"\u014e\u0150\u0003(\u0014\u0000\u014f\u0149\u0001\u0000\u0000\u0000\u0150"+
		"\u0153\u0001\u0000\u0000\u0000\u0151\u014f\u0001\u0000\u0000\u0000\u0151"+
		"\u0152\u0001\u0000\u0000\u0000\u0152A\u0001\u0000\u0000\u0000\u0153\u0151"+
		"\u0001\u0000\u0000\u0000\u0154\u0172\u00059\u0000\u0000\u0155\u0172\u0005"+
		":\u0000\u0000\u0156\u0172\u0005;\u0000\u0000\u0157\u0172\u0005<\u0000"+
		"\u0000\u0158\u0172\u0005\u0011\u0000\u0000\u0159\u0172\u0005\u0012\u0000"+
		"\u0000\u015a\u0172\u0005\u0013\u0000\u0000\u015b\u0172\u0005\r\u0000\u0000"+
		"\u015c\u0172\u0005\u000e\u0000\u0000\u015d\u0172\u0005\u000f\u0000\u0000"+
		"\u015e\u0172\u0005=\u0000\u0000\u015f\u0172\u0003D\"\u0000\u0160\u0161"+
		"\u0005/\u0000\u0000\u0161\u0162\u0003(\u0014\u0000\u0162\u0163\u00050"+
		"\u0000\u0000\u0163\u0172\u0001\u0000\u0000\u0000\u0164\u0165\u0005/\u0000"+
		"\u0000\u0165\u0166\u0003(\u0014\u0000\u0166\u0167\u00055\u0000\u0000\u0167"+
		"\u016c\u0003(\u0014\u0000\u0168\u0169\u00055\u0000\u0000\u0169\u016b\u0003"+
		"(\u0014\u0000\u016a\u0168\u0001\u0000\u0000\u0000\u016b\u016e\u0001\u0000"+
		"\u0000\u0000\u016c\u016a\u0001\u0000\u0000\u0000\u016c\u016d\u0001\u0000"+
		"\u0000\u0000\u016d\u016f\u0001\u0000\u0000\u0000\u016e\u016c\u0001\u0000"+
		"\u0000\u0000\u016f\u0170\u00050\u0000\u0000\u0170\u0172\u0001\u0000\u0000"+
		"\u0000\u0171\u0154\u0001\u0000\u0000\u0000\u0171\u0155\u0001\u0000\u0000"+
		"\u0000\u0171\u0156\u0001\u0000\u0000\u0000\u0171\u0157\u0001\u0000\u0000"+
		"\u0000\u0171\u0158\u0001\u0000\u0000\u0000\u0171\u0159\u0001\u0000\u0000"+
		"\u0000\u0171\u015a\u0001\u0000\u0000\u0000\u0171\u015b\u0001\u0000\u0000"+
		"\u0000\u0171\u015c\u0001\u0000\u0000\u0000\u0171\u015d\u0001\u0000\u0000"+
		"\u0000\u0171\u015e\u0001\u0000\u0000\u0000\u0171\u015f\u0001\u0000\u0000"+
		"\u0000\u0171\u0160\u0001\u0000\u0000\u0000\u0171\u0164\u0001\u0000\u0000"+
		"\u0000\u0172C\u0001\u0000\u0000\u0000\u0173\u017c\u00051\u0000\u0000\u0174"+
		"\u0179\u0003(\u0014\u0000\u0175\u0176\u00055\u0000\u0000\u0176\u0178\u0003"+
		"(\u0014\u0000\u0177\u0175\u0001\u0000\u0000\u0000\u0178\u017b\u0001\u0000"+
		"\u0000\u0000\u0179\u0177\u0001\u0000\u0000\u0000\u0179\u017a\u0001\u0000"+
		"\u0000\u0000\u017a\u017d\u0001\u0000\u0000\u0000\u017b\u0179\u0001\u0000"+
		"\u0000\u0000\u017c\u0174\u0001\u0000\u0000\u0000\u017c\u017d\u0001\u0000"+
		"\u0000\u0000\u017d\u017e\u0001\u0000\u0000\u0000\u017e\u017f\u00052\u0000"+
		"\u0000\u017fE\u0001\u0000\u0000\u0000\u0180\u0185\u0003(\u0014\u0000\u0181"+
		"\u0182\u00055\u0000\u0000\u0182\u0184\u0003(\u0014\u0000\u0183\u0181\u0001"+
		"\u0000\u0000\u0000\u0184\u0187\u0001\u0000\u0000\u0000\u0185\u0183\u0001"+
		"\u0000\u0000\u0000\u0185\u0186\u0001\u0000\u0000\u0000\u0186G\u0001\u0000"+
		"\u0000\u0000\u0187\u0185\u0001\u0000\u0000\u0000*K]cmt\u0081\u0085\u00a5"+
		"\u00ab\u00ae\u00b2\u00b6\u00be\u00c2\u00c8\u00ce\u00d9\u00de\u00e2\u00e6"+
		"\u00ed\u00f2\u00f9\u0101\u0107\u010e\u0116\u011e\u0126\u012e\u0133\u0138"+
		"\u013f\u0141\u0146\u014c\u0151\u016c\u0171\u0179\u017c\u0185";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}