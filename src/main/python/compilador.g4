grammar compilador;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

// Agrupadores
PA : '(' ;
PC : ')' ;
LLA : '{' ;
LLC : '}' ;
CA : '[' ;
CC : ']' ;
PYC : ';' ;
COMA : ',' ;

// Operadores Aritmeticos
ASIG : '=' ;
SUMA : '+' ;
RESTA : '-' ;
MULT : '*' ;
DIV : '/' ;
MOD : '%' ;

// Operadores Logicos
MENOR : '<' ;
MAYOR : '>' ;
MENOREQ : '<=' ;
MAYOREQ : '>=' ;
EQUAL : '==' ;
NEQUAL : '!=' ;
NUMERO : DIGITO+ ;

// Palabras reservadas
INT : 'int' ;
DOUBLE : 'double' ;
IF : 'if' ;
ELSE : 'else' ;
FOR : 'for' ;
WHILE : 'while' ;
RETURN : 'return' ;
ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;
// Ignorar espacios en blanco
WS : [ \n\r\t] -> skip ;
OTRO : . ;

programa : instrucciones EOF ;

instrucciones : instruccion* ;

instruccion : asignacion
            | declaracion
            | iif
            | iwhile
            | bloque
            | returnstmt
            | ifor
            | funcion
            ;

bloque : LLA instrucciones LLC ;
iwhile : WHILE PA opal PC instruccion ;

iif : IF PA opal PC instruccion ielse? ; // '?' para opcional
ielse : ELSE instruccion;

ifor : FOR PA (asignacionFor | declaracionFor) PYC (opal) PYC (asignacionFor) PC bloque ;
asignacionFor : ID ( ASIG opal | INCREMENTO | DECREMENTO ) ;

declaracionFor: tipo ID inic listavar ;
declaracion : tipo ID inic listavar PYC ;

listavar: (COMA ID inic)* ;

inic : ASIG opal
     |
     ;

tipo : INT
     | DOUBLE
     ;

asignacion : ID ( ASIG opal | INCREMENTO | DECREMENTO ) PYC ;

INCREMENTO : '++' ;
DECREMENTO : '--' ;

opal : exp ;

exp : term ( (SUMA | RESTA) term )* ;

term : factor ( (MULT | DIV | MOD) factor )* (l)? ;

funcion : tipo ID PA parametros? PC bloque ;

parametros : tipo ID (COMA tipo ID)* ;

factor : PA exp PC
       | NUMERO
       | ID
       ;

l : (EQUAL | NEQUAL | MENOR | MENOREQ | MAYOR | MAYOREQ) factor ;

returnstmt : RETURN opal PYC ;