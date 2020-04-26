# Jose Arturo Villalobos A00818214
# Rodrigo Valencia
# Diseno de compiladores
# Directorio de Funciones
import ply.yacc as yacc
import os
import codecs
import re
from lex import tokens
from sys import stdin
from DirFunc import *
from CuboSemantico import *

directorioFunciones = DirFunc()
cubo = CuboSemantico()

pOperandos = [] #Pila de operandos
pOperadores = [] #Pila de operadores

currentFunc = "global"
currentType = "void"
varName = ""
currentContParams = 0
numRenglones = 0
numColumnas = 0

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
    'programa : PROGRAMA ID SEMICOLON var1 func1 principal pn_6_end'
    # print("PROGRAMA")

def p_var1(p):
    '''
    var1 : var
         | empty
    '''
    # print("VAR1")

def p_func1(p):
    '''
    func1 : funcion func1
          | empty
    '''
    # print("FUNC'")

def p_principal(p):
    'principal : PRINCIPAL LPAREN RPAREN bloque'
    # print("PRINCIPAL")

#DECLARACION DE VARIABLES
def p_var(p):
    'var : VAR var2'
    # print("VAR")

def p_var2(p):
    'var2 : type TWO_DOTS lista_ids var3'
    # print("VAR2")

def p_var3(p):
    '''
    var3 : var2
         | empty
    '''
    # print("VAR3")

def p_type(p):
    '''
    type : tipo_simple
         | tipo_compuesto
    '''

#DECLARACION DE FUNCIONES
def p_funcion(p):
    'funcion : FUNCION tipo_fun ID pn_3_addFunction LPAREN parametros RPAREN pn_5_updateContParams var1 bloque'
    # print("FUNCION")

def p_tipo_fun(p):
    '''
    tipo_fun : VOID pn_1_setCurrentType
             | tipo_simple
    '''
    # print("TIPO_FUN")

def p_parametros(p):
    '''
    parametros : param
               | empty
    '''
    # print("PARAMETROS")

def p_param(p):
    'param : tipo_simple ID pn_4_params param1'
    # print("PARAM")

def p_param1(p):
    '''
    param1 : COMMA param
           | empty
    '''

#TIPOS
def p_tipo_simple(p):
    '''
    tipo_simple : INT pn_1_setCurrentType
                | FLOAT pn_1_setCurrentType
                | CHAR pn_1_setCurrentType
    '''

def p_tipo_compuesto(p):
    '''
    tipo_compuesto : DATAFRAME pn_1_setCurrentType
                   | STRING pn_1_setCurrentType
    '''

#Lista de IDS
def p_lista_ids(p):
    'lista_ids : lista SEMICOLON'

def p_lista(p):
    'lista : ID dd pn_2_addVariable lista1'

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
    'dim_dec : LBRACK CTE_INT RBRACK pn_7_decRenglones dim_dec1'

def p_dim_dec1(p):
    '''
    dim_dec1 : LBRACK CTE_INT RBRACK pn_8_decColumnas
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
    # print("BLOQUE")

def p_est(p):
    '''
    est : estatutos est
        | empty
    '''
    # print("EST")

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
    'lectura : LEE LPAREN variable RPAREN SEMICOLON'

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
            | CTE_CH
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
    # print("nulo")

def p_error(p):
    if p:
        print("Error de sintaxis ",p.type, p.value)
        print("Error en la linea "+str(p.lineno))
        parser.errok()
    else:
        print("Syntax error at EOF")



################ PUNTOS NEURALGICOS ###################
def p_pn_1_setCurrentType(p):
    '''
    pn_1_setCurrentType :
    '''
    global currentType
    currentType = p[-1]

def p_pn_2_addVariable(p):
    '''
    pn_2_addVariable : 
    '''
    global currentFunc
    global varName
    global currentType
    global numColumnas
    global numRenglones

    varName = p[-2]
    
    directorioFunciones.func_addVar(currentFunc, varName, currentType, numRenglones, numColumnas)
    numColumnas = 0
    numRenglones = 0

def p_pn_3_addFunction(p):
    '''
    pn_3_addFunction : 
    '''
    global currentFunc
    global currentType
    global currentContParams

    currentContParams = 0

    currentFunc = p[-1]
    directorioFunciones.func_add(currentFunc, currentType, currentContParams)

def p_pn_4_params(p):
    '''
    pn_4_params :
    '''
    global currentFunc
    global currentType
    global currentContParams
    global varName

    varName = p[-1]
    directorioFunciones.func_addVar(currentFunc, varName, currentType, 0, 0)
    currentContParams += 1

def p_pn_5_updateContParams(p):
    '''
    pn_5_updateContParams :  
    '''
    global currentFunc
    global currentContParams

    directorioFunciones.func_UpdateParams(currentFunc, currentContParams)

def p_pn_6_end(p):
    '''
    pn_6_end :
    '''
    #directorioFunciones.func_deleteDic()

def p_pn_7_decRenglones(p):
    '''
    pn_7_decRenglones :
    '''

    global numRenglones
    numRenglones = p[-2]

def p_pn_8_decColumnas(p):
    '''
    pn_8_decColumnas : 
    '''
    global numColumnas
    numColumnas = p[-2]


# parser = yacc.yacc()

# Put all test inside prueba folder
def main():
    name = input('File name: ')
    name = "pruebas/" + name
    print(name)
    try:
        f = open(name,'r', encoding='utf-8')
        parser.parse(f.read())
        f.close()
    except EOFError:
        print (EOFError)

#main()

#Test it out
data =''' 
programa COVID19;

var 
int : i[3], k[4][6];

funcion int sumar (int x, int y, float z)
var
float : j, i;
{

}

principal()
{

}
'''

parser = yacc.yacc()
result = parser.parse(data)

print(result)
# print(directorioFunciones.func_search("global"))