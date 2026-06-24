// ═════════════════════════════════════════════════════════════════
// HassoobArabi.g4 — grammar for حاسوب عربي
//
// GRAMMAR REVIEW NOTES
// --------------------
// The provided grammar was reviewed end-to-end against src/ast_builder.py and
// the interpreter pipeline. No FUNCTIONAL changes were required; it parses the
// full language (control flow, lambdas, postfix call/index chains, symbolic
// constants, Arabic-Indic numerals, f-strings) correctly. Specifically:
//
//   * Lexer keyword ordering is correct: ANTLR resolves overlaps by (1) longest
//     match then (2) declaration order, so multi-char operators ('**', '++',
//     '++=', '&&', '||', '==', '!=', '<=', '>=') win over their single-char
//     prefixes, and keyword tokens are declared before IDENTIFIER so reserved
//     words are not swallowed as identifiers.
//   * postfixExpr uses label-free alternatives; ast_builder walks ctx.children
//     directly (handling '(' argList? ')' and '[' expression ']'), so no
//     per-alternative labels are needed.
//   * The single-token NOT ('!') vs NEQ ('!=') overlap is resolved by maximal
//     munch, so '!=' is never mis-lexed as NOT followed by ASSIGN.
//
// Any future change MUST be annotated inline with: // CHANGED: <reason>
// ═════════════════════════════════════════════════════════════════
grammar HassoobArabi;

program : statement* EOF ;

statement
    : functionDef       # FunctionDefStmt
    | ifStmt            # IfStatement
    | whileStmt         # WhileStatement
    | forEachStmt       # ForEachStatement
    | forRangeStmt      # ForRangeStatement
    | returnStmt        # ReturnStatement
    | breakStmt         # BreakStatement
    | continueStmt      # ContinueStatement
    | symbolDecl        # SymbolDeclStatement
    | assignStmt        # AssignStatement
    | augAssignStmt     # AugAssignStatement
    | indexAssignStmt   # IndexAssignStatement
    | exprStmt          # ExprStatement
    ;

functionDef : DALA IDENTIFIER LPAREN paramList? RPAREN block ;
paramList   : IDENTIFIER (COMMA IDENTIFIER)* ;
block       : LBRACE statement* RBRACE ;

ifStmt       : IDHA LPAREN expression RPAREN block elseIfClause* elseClause? ;
elseIfClause : WA_ILLA IDHA LPAREN expression RPAREN block ;
elseClause   : WA_ILLA block ;

whileStmt    : BAYNAMA LPAREN expression RPAREN block ;
forEachStmt  : LIKULL IDENTIFIER FI expression block ;
forRangeStmt : LIKULL IDENTIFIER MIN expression ILA expression (BKHUTWA expression)? block ;

returnStmt   : IRJA expression? SEMI? ;
breakStmt    : AWQIF SEMI? ;
continueStmt : ISTAMIRR SEMI? ;

symbolDecl    : RAMZ IDENTIFIER (COMMA IDENTIFIER)* SEMI? ;
assignStmt    : IDENTIFIER ASSIGN expression SEMI? ;
augAssignStmt : IDENTIFIER augOp expression SEMI? ;
augOp         : PLUS_ASSIGN | MINUS_ASSIGN | STAR_ASSIGN | SLASH_ASSIGN
              | CARET_ASSIGN | PERCENT_ASSIGN | CONCAT_ASSIGN ;
indexAssignStmt : IDENTIFIER (LBRACKET indexList RBRACKET)+ ASSIGN expression SEMI? ; // CHANGED (#8/#9): chained/N-D index targets a[i][j] and a[i, j] at any rank
exprStmt      : expression SEMI? ;

expression  : lambdaExpr | orExpr ;
lambdaExpr  : IDENTIFIER ARROW expression                       # SingleParamLambda
            | LPAREN paramList? RPAREN ARROW expression         # MultiParamLambda
            ;
orExpr      : andExpr (OR andExpr)* ;
andExpr     : notExpr (AND notExpr)* ;
notExpr     : NOT notExpr     # NotExpression
            | equalityExpr    # PassThroughNot
            ;
equalityExpr   : relationalExpr ((EQ | NEQ) relationalExpr)* ;
relationalExpr : addExpr ((LT | LTE | GT | GTE) addExpr)* ;
addExpr        : mulExpr ((PLUS | MINUS | STR_CONCAT) mulExpr)* ;
mulExpr        : unaryExpr ((STAR | SLASH | INT_DIV | PERCENT | MAT_MUL) unaryExpr)* ;
unaryExpr      : MINUS unaryExpr  # UnaryMinus
               | PLUS  unaryExpr  # UnaryPlus
               | powerExpr        # PassThroughUnary
               ;
powerExpr   : postfixExpr (CARET unaryExpr)? ;
postfixExpr : primary ( LPAREN argList? RPAREN | LBRACKET indexList RBRACKET )* ; // CHANGED (#8): index now uses indexList so N-D reads a[i, j] parse
argList     : (IDENTIFIER ASSIGN)? expression (COMMA (IDENTIFIER ASSIGN)? expression)* ; // CHANGED: support named call arguments such as title="..."

primary     : INTEGER_LIT    # IntLiteral
    | FLOAT_LIT      # FloatLiteral
    | STRING_LIT     # StringLiteral
    | FSTRING_LIT    # FStringLiteral
    | PI_CONST       # PiConstant
    | E_CONST        # EulerConstant
    | INF_CONST      # InfinityConstant
    | SAHIH          # TrueLiteral
    | KHATA          # FalseLiteral
    | FARIG          # NullLiteral
    | IDENTIFIER     # IdentifierExpr
    | listLiteral    # ListExpr
    | LPAREN expression RPAREN                              # ParenExpr
    | LPAREN expression COMMA expression (COMMA expression)* RPAREN  # TupleLiteral
    ;

listLiteral : LBRACKET (expression (COMMA expression)*)? RBRACKET ;
indexList   : expression (COMMA expression)* ; // CHANGED (#8): comma-separated indices for N-D access a[i, j, k]

// ── Keywords ──────────────────────────────────────────────
IDHA     : 'إذا'    ;
WA_ILLA  : 'وإلا'   ;
BAYNAMA  : 'بينما'  ;
LIKULL   : 'لكل'    ;
MIN      : 'من'     ;
ILA      : 'إلى'    ;
FI       : 'في'     ;
BKHUTWA  : 'بخطوة'  ;
DALA     : 'دالة'   ;
IRJA     : 'إرجع'   ;
AWQIF    : 'اوقف'   ;
ISTAMIRR : 'استمر'  ;
SAHIH    : 'صح'   ;
KHATA    : 'خطأ'    ;
FARIG    : 'فارغ'   ;
RAMZ     : 'رمز'    ;
PI_CONST  : 'π' | 'باي'  ;
E_CONST   : 'هـ'          ;
INF_CONST : 'لانهاية'     ;

AND : 'و' | '&&' ;
OR  : 'أو' | '||' ;
NOT : 'ليس' | '!' ;

PLUS_ASSIGN : '+=' ;
MINUS_ASSIGN : '-=' ;
STAR_ASSIGN  : '*=' ;
SLASH_ASSIGN : '/=';
CARET_ASSIGN : '^=';
PERCENT_ASSIGN: '%=';
CONCAT_ASSIGN : '++=';

MAT_MUL    : '**' ;
STR_CONCAT : '++' ;
PLUS  : '+' ;
MINUS : '-' ;
STAR  : '*' ;
SLASH : '/' ;
INT_DIV : '÷' ;
PERCENT : '%' ;
CARET : '^' ;
ARROW : '=>' ;

EQ : '==' ;
NEQ : '!=' | '≠' ;
LTE : '<=' | '≤' ;
GTE : '>=' | '≥' ;
LT : '<'  ;
GT  : '>'  ;
ASSIGN : '=' ;

LPAREN : '(' ;
RPAREN : ')' ;
LBRACKET : '[' ;
RBRACKET : ']' ;
LBRACE : '{' ;
RBRACE : '}' ;
COMMA : ',' | '\u060C' ;
SEMI : ';' | '\u061B' ; // CHANGED: also accept the Arabic semicolon '؛' as a statement terminator
COLON : ':' ;
DOT : '.' ;

fragment ARABIC_DIGIT  : [\u0660-\u0669] ;
fragment WESTERN_DIGIT : [0-9] ;
fragment DIGIT         : ARABIC_DIGIT | WESTERN_DIGIT ;
fragment DIGITS        : DIGIT (DIGIT | '_')* ;

INTEGER_LIT : DIGITS ;
FLOAT_LIT   : DIGITS '.' DIGITS? ([eE] [+\-]? DIGITS)?
            | '.' DIGITS          ([eE] [+\-]? DIGITS)?
            | DIGITS               [eE] [+\-]? DIGITS ;

STRING_LIT  : '"' (~["\\\r\n] | ESCAPE_SEQ)* '"'
            | '\'' (~['\\\r\n] | ESCAPE_SEQ)* '\'' ;
FSTRING_LIT : ('ف'|'f'|'F') '"' (~["\\\r\n] | ESCAPE_SEQ)* '"'
            | ('ف'|'f'|'F') '\'' (~['\\\r\n] | ESCAPE_SEQ)* '\'' ;

fragment ESCAPE_SEQ
    : '\\' [\\'"nrtbf0]
    | '\\u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT ;
fragment HEX_DIGIT : [0-9a-fA-F] ;

// CHANGED: range now starts at \u0620 (not \u0600) so Arabic punctuation in
// \u0600-\u061F — e.g. the Arabic semicolon '؛', comma '،' and question mark
// '؟' — is NOT swallowed into identifiers; those are handled as their own tokens.
fragment ARABIC_LETTER : [\u0620-\u06FF] | [\u0750-\u077F] | [\u08A0-\u08FF]
                       | [\uFB50-\uFDFF] | [\uFE70-\uFEFF] ;
fragment ID_START    : [a-zA-Z_] | ARABIC_LETTER ;
fragment ID_CONTINUE : ID_START | DIGIT ;
IDENTIFIER : ID_START ID_CONTINUE* ;

LINE_COMMENT   : '#' ~[\r\n]* -> skip ;
ARABIC_COMMENT : 'ملاحظة' ~[\r\n]* -> skip ;
BLOCK_COMMENT  : '/*' .*? '*/' -> skip ;
WS : [ \t\r\n\u00A0\u200C\u200D\u200E\u200F\uFEFF]+ -> skip ;
