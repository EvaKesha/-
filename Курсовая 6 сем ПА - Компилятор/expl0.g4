grammar expl0;

program : main_const=const? main_var=var? procedure* block '.' ;  // без const var procedure не работает

const : CONST ID '=' (NUMBER? float_number?) (',' ID '=' (NUMBER? float_number?))* ';';

var : VAR (ID (',' ID)* ':' 'integer' ';')?  (ID (',' ID)* ':' 'real' ';')? ;

procedure : PROCEDURE procedure_id=ID ';' proc_const=const? proc_var=var? block ';';

block : BEGIN (statement ';')* statement END;  // было BEGIN statement* (BEGIN statement* END)* statement* END

statement : assign | call | ifthen | ifthenelse | whiledo | write;

assign : ID ':=' expression;

expression : ID
             |(NUMBER? float_number?)
             |left = expression op=('*'|'/'|'+'|'-') right = expression;

call : CALL ID ;

write : WRITE (ID|(NUMBER? float_number?));

ifthen : IF condition THEN (if_body=block | statement) ;

ifthenelse : IF condition THEN (if_body=block | if_st=statement) ELSE (else_body=block | else_st=statement);

whiledo : WHILE condition DO (while_body=block | statement);

condition : left=expression op=('='|'<>'|'>'|'<') right=expression;

float_number : NUMBER '.' NUMBER;

LPAREN: '(';
RPAREN: ')';
WS : [ \t\r\n]+ -> skip;
ID : [a-z]+;
NUMBER : '0'..'9'+;
CONST : 'const'|'CONST';
VAR : 'var'|'VAR';
PROCEDURE : 'procedure'|'PROCEDURE';
CALL : 'call'|'CALL';
BEGIN : 'begin'|'BEGIN';
END : 'end'|'END';
IF : 'if'|'IF';
THEN : 'then'|'THEN';
ELSE : 'ELSE'| 'else';
WHILE : 'while'|'WHILE';
DO : 'do'|'DO';
ODD : 'odd'|'ODD';
WRITE : 'write'|'WRITE';