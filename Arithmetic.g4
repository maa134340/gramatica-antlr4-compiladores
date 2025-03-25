grammar Arithmetic;

// Regra principal do REPL (Read-Eval-Print Loop)
repl: (stmt NEWLINE)* stmt? ;

// Declarações podem ser expressões, atribuições, condicionais, loops, definições de funções ou blocos
stmt
    : assignment                    
    | ifStmt                        
    | whileStmt                     
    | funcDef                       
    | block                         
    | comparison                    
    | expr                          
    ;

// Declaração de atribuição
assignment: VAR ASSIGN expr ;

// Declaração condicional (if/else)
ifStmt
    : IF LPAREN comparison RPAREN stmt (ELSE stmt)?
    ;

// Declaração de loop while
whileStmt
    : WHILE LPAREN comparison RPAREN block
    ;

// Definição de função; o corpo da função é uma declaração (geralmente um bloco)
funcDef
    : FUN VAR LPAREN paramList? RPAREN stmt
    ;

// Lista de parâmetros para funções
paramList
    : VAR (COMMA VAR)*
    ;

// Regras de expressão para operações binárias
expr
    : expr (PLUS | MINUS) term       
    | term                          
    ;

term
    : term (MUL | DIV) factor       
    | factor                        
    ;

// Fator lida com chamadas de função e átomos
factor
    : functionCall                  
    | atom                          
    ;

// Chamada de função: variável seguida por lista de argumentos entre parênteses
functionCall
    : VAR LPAREN argList? RPAREN
    ;

// Lista de argumentos para chamadas de função
argList
    : expr (COMMA expr)*
    ;

// Um átomo pode ser um inteiro, uma variável ou uma expressão entre parênteses
atom
    : INT                           
    | VAR                          
    | LPAREN expr RPAREN            
    ;

// Bloco de declarações delimitado por chaves
block
    : LBRACE stmt* RBRACE
    ;

// Comparações entre expressões
comparison
    : expr (LT | LE | GT | GE | EQ | NE) expr
    ;

// Regras do lexer
PLUS: '+' ;
MINUS: '-' ;
MUL: '*' ;
DIV: '/' ;
ASSIGN: '=' ;
LPAREN: '(' ;
RPAREN: ')' ;
LBRACE: '{' ;
RBRACE: '}' ;
COMMA: ',' ;
IF: 'if' ;
ELSE: 'else' ;
WHILE: 'while' ;
FUN: 'fun' ;
INT: [0-9]+ ;
VAR: [a-zA-Z]+ ;
NEWLINE: ('\r'? '\n')+ ;
WS: [ \t]+ -> skip ;

LT  : '<' ;
LE  : '<=' ;
GT  : '>' ;
GE  : '>=' ;
EQ  : '==' ;
NE  : '!=' ;