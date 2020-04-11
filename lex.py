#Jose Arturo Villalobos A00818214
#Rodrigo Valencia 
#Scanner del proyecto de Compiladores
import ply.lex as lex
import re
import codecs
import os
import sys

#Lista de Tokens
tokens = [
    # OPERATOR
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'OR',
    'AND',
    'LT',
    'LE',
    'GT',
    'GE',
    'EQUAL',
    'ASSIGN',
    'NOT_EQUAL',
    # COMMENT AND WHITESPACE
    'COMMENT',
    #'WS',
    # SEPARATORS
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACK',
    'RBRACK',
    'SEMICOLON',
    'COMMA',
    #'DOT',
    'TWO_DOTS',
    # LITERALS
    'ID',
    'CTE_INT',
    'CTE_FLOAT',
    'CTE_STR',
    'CTE_CH'
]

#Palabras reservadas
keywords = {
    # MAIN 
    'programa' : 'PROGRAMA',
    'principal' : 'PRINCIPAL',
    # DECLARATIONS
    'var' : 'VAR',
    'int' : 'INT',
    'void' : 'VOID',
    'char' : 'CHAR',
    'float' : 'FLOAT',
    'string' : 'STRING',
    'regresa' : 'REGRESA',
    'funcion' : 'FUNCION',
    'dataframe' : 'DATAFRAME',
    # UPLOAD
    'lee' : 'LEE',
    'cargaArchivo' : 'CARGA', 
    'escribe' : 'ESCRIBE',
    # CONDITIONS
    'si' : 'SI',
    'haz' : 'HAZ',
    'sino' : 'SINO',
    'mientras' : 'MIENTRAS',
    'entonces' : 'ENTONCES',
    # LOOPS
    'desde' : 'DESDE',
    'hasta' : 'HASTA',
    'hacer' : 'HACER',
    #FUNCIONES ESPECIALES
    'Variables' : 'VARIABLES',
    'Distribucion' : 'DISTRIBUCION',
    'Tendencia' : 'TENDENCIA',
    'Media' : 'MEDIA',
    'Mediana' : 'MEDIANA',
    'Moda' : 'MODA',
    'Varianza' : 'VARIANZA',
    'Correlaciona' : 'CORRELACIONA'
}


tokens = tokens + list(keywords.values())

#Definir los Tokens
t_ADD           = r'\+'
t_SUB           = r'\-'
t_MUL           = r'\*'
t_DIV           = r'/'
t_OR            = r'\|'
t_AND           = r'&'
t_LT            = r'<'
t_LE            = r'<='
t_GT            = r'>'
t_GE            = r'>='
t_EQUAL         = r'=='
t_NOT_EQUAL     = r'!='
t_ASSIGN        = r'='
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACE        = r'\{'
t_RBRACE        = r'\}'
t_LBRACK        = r'\['
t_RBRACK        = r'\]'
t_SEMICOLON     = r';'
t_COMMA         = r','
#t_DOT           = r'\.'
t_TWO_DOTS      = r':'
t_ignore        = ' \t'

#Definicion de funciones necesarias
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTE_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_CTE_STR(t):
    r''
    t.value = str(t.value)
    return t

def t_CTE_CH(t):
    r''
    t.value = chr(t.value)
    return t

def t_COMMENT(t):
    r'\%\%.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    if t:
        print("Illegal character '{}' at: {}".format(t.value[0], t.lexer.lineno))
        t.lexer.skip(1)
    else:
        print ("Error from lex")



analizador = lex.lex()
analizador.input("hola  'T'")
while True:
    tok = analizador.token()
    if not tok : break
    print(tok)