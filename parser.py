import ply.yacc as yacc
import os
import codecs
import re
from lex import tokens
from sys import stdin

#Se define la precedencia
precedence = (
    ('nonassoc', 'SEMICOLON'),
    ('right', 'ASSIGN'),
    ('left', 'NOT_EQUAL'),
    ('nonassoc', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL','DIV'),
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'LBRACK', 'RBRACK'),
    ('left', 'LBRACE', 'RBRACE')
)

#INICIO
def p_programa(p):
    'programa : PROGRAMA ID SEMICOLON var1 func1 principal'
    print("PROGRAMA")

def p_var1(p):
    '''
    var1 : var
         | empty
    '''
    print("VAR1")

def p_func1(p):
    '''
    func1 : funcion
          | empty
    '''
    print("FUNC'")

def p_principal(p):
    'principal : PRINCIPAL LPAREN RPAREN bloque'
    print("PRINCIPAL")

#DECLARACION DE VARIABLES
def p_var(p):
    'var : VAR var2'
    print("VAR")

def p_var2(p):
    'var2 : type TWO_DOTS lista_ids var3'
    print("VAR2")

def p_var3(p):
    '''
    var3 : var2
         | empty
    '''
    print("VAR3")

def p_type(p):
    '''
    type : tipo_simple
         | tipo_compuesto
    '''

#DECLARACION DE FUNCIONES
def p_funcion(p):
    'funcion : FUNCION tipo_fun ID LPAREN parametros RPAREN var1 bloque'
    print("FUNCION")

def p_tipo_fun(p):
    '''
    tipo_fun : VOID
             | tipo_simple
    '''
    print("TIPO_FUN")

def p_parametros(p):
    '''
    parametros : param
               | empty
    '''
    print("PARAMETROS")

def p_param(p):
    'param : tipo_simple ID param1'
    print("PARAM")

def p_param1(p):
    '''
    param1 : COMMA param
           | empty
    '''

#TIPOS
def p_tipo_simple(p):
    '''
    tipo_simple : INT
                | FLOAT
                | CHAR
    '''

def p_tipo_compuesto(p):
    '''
    tipo_compuesto : DATAFRAME
                   | STRING
    '''

#Lista de IDS
def p_lista_ids(p):
    'lista_ids : lista SEMICOLON'

def p_lista(p):
    'lista : ID dd lista1'

def p_dd(p):
    '''
    dd : dim_dec
       | empty
    '''

def p_lista1(p):
    '''
    lista1 : COMMA lista
           | empty
    '''

#Dimensiones
def p_dim_dec(p):
    'dim_dec : LBRACK CTE_INT RBRACK dim_dec1'

def p_dim_dec1(p):
    '''
    dim_dec1 : LBRACK CTE_INT RBRACK
             | empty
    '''

def p_dim_index(p):
    'dim_index : LBRACK exp RBRACK dim_index1'

def p_dim_index1(p):
    '''
    dim_index1 : LBRACK exp RBRACK
               | empty
    '''


#Bloque
def p_bloque(p):
    'bloque : LBRACE est RBRACE'
    print("BLOQUE")

def p_est(p):
    '''
    est : estatutos est
        | empty
    '''
    print("EST")

def p_estatutos(p):
    '''
    estatutos : asignacion
              | llamada
              | retorno
              | lectura
              | escritura
              | carga_datos
              | decision
              | condicional
              | no_condicional
              | funciones_especiales_void
    '''

#ESTATUTOS

    #Asig
def p_asignacion(p):
    'asignacion : variable ASSIGN asig'

def p_asig(p):
    '''
    asig : llamada
         | exp SEMICOLON
    '''
def p_variable(p):
    'variable : ID di'

def p_di(p):
    '''
    di : dim_index
       | empty
    '''

def p_llamada(p):
    'llamada :  ID LPAREN llamada1 RPAREN SEMICOLON'

def p_llamada1(p):
    '''
    llamada1 : exp llamada2
             | empty
    '''

def p_llamada2(p):
    '''
    llamada2 : COMMA llamada1
             | empty
    '''

def p_retorno(p):
    'retorno : REGRESA LPAREN exp RPAREN SEMICOLON'

def p_lectura(p):
    'lectura : LEE LPAREN lista_ids RPAREN SEMICOLON'

def p_escritura(p):
    'escritura : ESCRIBE LPAREN esc RPAREN SEMICOLON'

def p_esc(p):
    'esc : esc1 esc2'

def p_esc1(p):
    '''
    esc1 : exp
         | CTE_STR
    '''
def p_esc2(p):
    '''
    esc2 : COMMA esc
         | empty
    '''

def p_carga_datos(p):
    'carga_datos : CARGA LPAREN ID COMMA CTE_STR COMMA ca COMMA ca RPAREN SEMICOLON'

def p_ca(pa):
    '''
    ca : ID
       | CTE_INT
    '''


def p_decision(p):
    'decision : SI LPAREN expresion RPAREN ENTONCES bloque sino'

def p_sino(p):
    '''
    sino : SINO bloque
         | empty
    '''

def p_condicional(p):
    'condicional : MIENTRAS LPAREN expresion RPAREN HAZ bloque'

def p_no_condicional(p):
    'no_condicional : DESDE variable ASSIGN exp HASTA exp HACER bloque'


def p_funciones_especiales_void(p):
    '''
    funciones_especiales_void : VARIABLES LPAREN ID COMMA ID COMMA ID RPAREN SEMICOLON
                              | fev LPAREN ID COMMA v_exp RPAREN SEMICOLON
    '''
def p_fev(p):
    '''
    fev : DISTRIBUCION
        | TENDENCIA
    '''

def p_funciones_especiales(p):
    '''
    funciones_especiales : fe LPAREN ID COMMA v_exp RPAREN
                         | CORRELACIONA LPAREN ID COMMA v_exp COMMA v_exp RPAREN
    '''
def p_fe(p):
    '''
    fe : MEDIA
       | MEDIANA
       | MODA
       | VARIANZA
    '''
def p_v_exp(p):
    'v_exp : VARIABLES LBRACK exp RBRACK'




def p_var_cte(p):
    '''
    var_cte : CTE_INT
            | CTE_FLOAT
    '''

#EXPRESIONES

def p_expresion(p):
    'expresion : mega_exp expresion1'

def p_expresion1(p):
    '''
    expresion1 : ASSIGN expresion
               | empty
    '''

def p_mega_exp(p):
    'mega_exp : super_exp meg'

def p_meg(p):
    '''
    meg : op_l mega_exp
        | empty
    '''
def p_op_l(p):
    '''
    op_l : AND
         | OR
    '''

def p_super_exp(p):
    'super_exp : exp sp'

def p_sp(p):
    '''
    sp : op_r exp
       | empty
    '''
def p_op_r(p):
    '''
    op_r : LT
         | GT
         | LE
         | GE
         | NOT_EQUAL
         | EQUAL
    '''

def p_exp(p):
    'exp : termino exp1'

def p_exp1(p):
    '''
    exp1 : op_a exp
         | empty
    '''
def p_op_a(p):
    '''
    op_a : ADD
         | SUB
    '''

def p_termino(p):
    'termino : factor term'

def p_term(p):
    '''
    term : op_a1 termino
         | empty
    '''
def p_op_a1(p):
    '''
    op_a1 : MUL
          | DIV
    '''

def p_factor(p):
    '''
    factor : var_cte
           | LPAREN exp RPAREN
           | variable
           | llamada
           | funciones_especiales
    '''


def p_empty(p):
    '''empty :'''
    pass
    print("nulo")

def p_error(p):
    if p:
        print("Error de sintaxis ",p.type)
        print("Error en la linea "+str(p.lineno))
        parser.errok()
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
result = parser.parse("programa Covid19 ;  principal () { }")

print(result)