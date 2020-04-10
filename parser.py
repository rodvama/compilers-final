import ply.yacc as yacc
import os
import codecs
import re
from lex import tokens
from sys import stdin

#Se define la precedencia
precedence = (
    ('right', 'ASSIGN'),
    ('left', 'NOT_EQUAL'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL','DIV'),
    ('left', 'LPAREN', 'RPAREN')
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
         | STRING
    '''
    print("TYPE")

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
def p_lista_ids(p)
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

def p_est(p):
    '''
    est : estatutos est
        | empty
    '''

def p_estatutos(p):
    '''
    estatutos : asignacion
              | llamada_func
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


