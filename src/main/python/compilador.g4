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

// Operadores compuestos de asignación
MASIG : '+=' ;
RESIG : '-=' ;
MULASIG : '*=' ;
DIVASIG : '/=' ;
MODASIG : '%=' ;

// Operadores LOGICOS
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

// s : ID     {print("ID ->" + $ID.text + "<--") }         s
//   | NUMERO {print("NUMERO ->" + $NUMERO.text + "<--") } s
//   | OTRO   {print("Otro ->" + $OTRO.text + "<--") }     s
//   | EOF
//   ;

// s : PA s PC s
//   |
//   ;

programa : instrucciones EOF ;

instrucciones : instruccion instrucciones
              |
              ;

instruccion : asignacion
            | declaracion
            | iif
            | iwhile
            | ifor
            | funcion
            | bloque
            | opal PYC
            ;
            
bloque : LLA instrucciones LLC ;

iwhile : WHILE PA opal PC instruccion ;

iif : IF PA opal PC instruccion ielse ;

ielse : ELSE instruccion
           |
           ;

ifor : FOR PA (asignacionFor | declaracionFor) PYC (opal) PYC (asignacionFor) PC bloque ;

asignacionFor : ID (ASIG | MASIG | RESIG | MULASIG | DIVASIG | MODASIG) opal
              | ID INCREMENTO
              | ID DECREMENTO
          ;

declaracionFor: tipo ID inic listavar ;

declaracion : tipo ID inic listavar PYC ;

listavar: COMA ID inic listavar
        |
        ;

inic : ASIG opal
     |
     ;

tipo : INT
     | DOUBLE
     ;

asignacion : ID (ASIG | MASIG | RESIG | MULASIG | DIVASIG | MODASIG) opal PYC
          | ID (INCREMENTO | DECREMENTO) PYC
          ;

INCREMENTO : '++' ;

DECREMENTO : '--' ;

opal : exp
     ;

exp : term e ;

e : SUMA term e
  | RESTA term e
  |
  ;

term : factor t
     | factor l
     ;

t : MULT factor t
  | DIV factor t
  | MOD factor t
  |
  ;

l : MENOR factor l
  | MAYOR factor l
  | MENOREQ factor l
  | MAYOREQ factor l
  | EQUAL factor l
  | NEQUAL factor l
  ;

funcion : tipo ID PA parametros PC bloque ;

parametros : tipo ID lista_param
           |
           ;

lista_param : COMA ID lista_param
            |
            ;

factor : PA exp PC
       | NUMERO
       | ID
       | ID PA argumentos? PC ;

argumentos : opal (COMA opal)* ;

// Prototipo (declaración sin cuerpo)
prototipo : tipo ID PA parametrosTipados? PC PYC ;

// Parámetros tipados
parametrosTipados : tipo ID (COMA tipo ID)* ;
