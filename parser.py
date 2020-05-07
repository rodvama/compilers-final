# Jose Arturo Villalobos A00818214
# Rodrigo Valencia
# Diseno de compiladores
# Parser
#Ultima modificacion: 2 Mayo 2020
import ply.yacc as yacc
import os
import codecs
import re
from lex import tokens
from sys import stdin
from DirFunc import *
from CuboSemantico import *
from CuboSemantico_FuncEsp import *

directorioFunciones = DirFunc()
validaCubo = CuboSemantico()
validaCuboEsp = CuboSemantico_FuncEsp()


### Pilas para generacion de cuadruplos ####
pOperandos = [] #Pila de operandos pendientes (PilaO)
pOper = [] #Pila de operadores pendientes (POper)
pTipos = [] #Pila de tipos
pSaltos = [] #Pila de saltos para condiciones y ciclos

#Arreglo donde se almacenaran todos los cuadruplos que se vayan generando
cuadruplos = []

#Diccionarios de constantes
d_ints = {}
d_floats = {}
d_strs = {}
d_ch = {}
d_df = {}

##Constantes
CONTEXT_GLOBAL = 'global'
OPERADORES_SUMARESTA = ['+', '-']
OPERADORES_MULTDIV = ['*', '/']
OPERADORES_REL = ['>', '<', '<=', '>=', '==', '!=']
OPERADORES_LOGICOS = ['&', '|']
OP_ASIG = ['=']
OP_SECUENCIALES = ['lee', 'escribe']
BATCH_SIZE = 100 #Tamano del espacio de memoria

##Variables globales
currentFunc = CONTEXT_GLOBAL
currentType = "void"
varName = ""
currentContParams = 0
numRenglones = 0
numColumnas = 0
avail = 0
constanteNegativa = False
forBool = False
varFor = ''
negativo = False

'''
Espacios de memoria:
+++++++++++++++++++++++
+globales enteras     + batch_size
+---------------------+
+globales flotantes   + batch_size
+---------------------+
+globales strings     + batch_size
+---------------------+
+globales char       + batch_size
+---------------------+
+globales dataframes  + batch_size
+++++++++++++++++++++++
+locales enteras      + batch_size
+---------------------+
+locales flotantes    + batch_size
+---------------------+
+locales strings      + batch_size
+---------------------+
+locales char         + batch_size
+---------------------+
+locales dataframes   + batch_size
+++++++++++++++++++++++
+temp enteras         + batch_size
+---------------------+
+temp flotantes       + batch_size
+---------------------+
+temp strings         + batch_size
+---------------------+
+temp char            + batch_size
+---------------------+
+temp dataframes      + batch_size
+---------------------+
+temp booleanas       + batch_size
+++++++++++++++++++++++
+constantes enteras   + batch_size
+---------------------+
+constantes flotantes + batch_size
+---------------------+
+constantes strings   + batch_size
+---------------------+
+constantes char      + batch_size
+---------------------+
+constantes dataframe    + batch_size
+++++++++++++++++++++++
'''
#Declaracion de espacio de memoria por tipo de memoria
index_intGlobales = BATCH_SIZE
index_floatGlobales = index_intGlobales + BATCH_SIZE
index_stringsGlobales = index_floatGlobales + BATCH_SIZE
index_charGlobales = index_stringsGlobales + BATCH_SIZE
index_dfGlobales = index_charGlobales + BATCH_SIZE

index_intLocales = index_dfGlobales + BATCH_SIZE
index_floatLocales = index_intLocales + BATCH_SIZE
index_stringsLocales = index_floatLocales + BATCH_SIZE
index_charLocales = index_stringsLocales + BATCH_SIZE
index_dfLocales = index_charLocales + BATCH_SIZE

index_intTemporales = index_dfLocales + BATCH_SIZE
index_floatTemporales = index_intTemporales + BATCH_SIZE
index_stringsTemporales = index_floatTemporales + BATCH_SIZE
index_charTemporales = index_stringsTemporales + BATCH_SIZE
index_dfTemporales = index_charTemporales + BATCH_SIZE
index_boolTemporales = index_dfTemporales + BATCH_SIZE

index_intConstantes = index_boolTemporales + BATCH_SIZE
index_floatConstantes = index_intConstantes + BATCH_SIZE
index_stringConstantes = index_floatConstantes + BATCH_SIZE
index_charConstantes = index_stringConstantes + BATCH_SIZE
index_dfConstantes = index_charConstantes + BATCH_SIZE


#Declaracion de inicio de index de memoria para temporales
cont_IntTemp = index_dfLocales
cont_FloatTemp = index_intTemporales
cont_StringTemp = index_floatTemporales
cont_CharTemp = index_stringsTemporales
cont_dfTemp = index_charTemporales
cont_BoolTemp = index_dfTemporales


#Declaracion de inicio de los inde de memoria para constantes 
cont_IntConst = index_boolTemporales
cont_FloatConst = index_intConstantes
cont_StringConst = index_floatConstantes
cont_CharConst = index_stringConstantes
cont_dfConst = index_charConstantes


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
    print("PROGRAMA \"", p[2], "\" terminado.")
    printQuadList()
    
    

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
    'principal : PRINCIPAL pn_9_setCurrentFuncGl LPAREN RPAREN bloque'
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
    'asignacion : variable ASSIGN pnQuadGenSec1 asig'

def p_asig(p):
    '''
    asig : llamada
         | exp SEMICOLON pnQuadGenSec2
    '''
def p_variable(p):
    'variable : ID pnQuadGenExp1 di'

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
    'lectura : LEE pnQuadGenSec3 LPAREN variable RPAREN SEMICOLON pnQuadGenSec4'

def p_escritura(p):
    'escritura : ESCRIBE pnQuadGenSec3 LPAREN esc RPAREN SEMICOLON pnQuadGenSec4'

def p_esc(p):
    'esc : esc1 esc2'

def p_esc1(p):
    '''
    esc1 : exp
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

#Condicionales y Ciclos
def p_decision(p): #IF
    'decision : SI LPAREN expresion RPAREN pnQuadGenCond1 ENTONCES bloque sino pnQuadGenCond2'

def p_sino(p): #ELSE
    '''
    sino : SINO pnQuadGenCond3 bloque
         | empty
    '''


def p_condicional(p): #While
    'condicional : MIENTRAS pnQuadGenCiclos1 LPAREN expresion RPAREN pnQuadGenCiclos2 HAZ bloque pnQuadGenCiclos3'

def p_no_condicional(p): #For
    'no_condicional : DESDE pnQuadGenCiclos4 variable ASSIGN pnQuadGenSec1 exp pnQuadGenCiclos5 HASTA pnQuadGenCiclos6 exp pnQuadGenCiclos7 HACER bloque pnQuadGenCiclos8'


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




def p_var_cte(p):#Se modificaran los PN
    '''
    var_cte : CTE_CH pnQuadGenCteChar
            | CTE_STR pnQuadGenCteStr
            | SUB pnNeg var_num
            | var_num
    '''
    
    if p[1] == '-':
        p[0] = -1 * p[3]
    else:
        p[0] = p[1]
    
    global negativo
    negativo = False

def p_var_num(p): 
    '''
    var_num : CTE_INT pnQuadGenCteInt
            | CTE_FLOAT pnQuadGenCteFloat
    '''
    p[0] = p[1]

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
    meg : op_l pnQuadGenExp10 mega_exp pnQuadGenExp11
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
    sp : op_r  exp pnQuadGenExp9
       | empty
    '''
def p_op_r(p):
    '''
    op_r : LT pnQuadGenExp8
         | GT pnQuadGenExp8
         | LE pnQuadGenExp8
         | GE pnQuadGenExp8
         | NOT_EQUAL pnQuadGenExp8
         | EQUAL pnQuadGenExp8
    '''

def p_exp(p):
    'exp : termino pnQuadGenExp4 exp1'

def p_exp1(p):
    '''
    exp1 : op_a exp
         | empty
    '''
def p_op_a(p):
    '''
    op_a : ADD pnQuadGenExp2
         | SUB pnQuadGenExp2
    '''

def p_termino(p):
    'termino : factor pnQuadGenExp5 term'

def p_term(p):
    '''
    term : op_a1 termino
         | empty
    '''
def p_op_a1(p):
    '''
    op_a1 : MUL pnQuadGenExp3
          | DIV pnQuadGenExp3
    '''

def p_factor(p):
    '''
    factor : var_cte
           | LPAREN pnQuadGenExp6 exp RPAREN pnQuadGenExp7
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

############## FUNCIONES DE LAS PILAS ################

#Te regresa el ultimo elemento de la pila de operandos
def popOperandos():
    global pOperandos
    return pOperandos.pop()

#Te regresa el ultimo elemento de la pila de operadores
def popOperadores():
    global pOper
    return pOper.pop()

#Te regresa el ultimo elemento de la pila de tipos
def popTipos():
    global pTipos
    return pTipos.pop()

#Mete a la pila operandos el nuevo operando
def pushOperando(operando):
    global pOperandos
    pOperandos.append(operando)

#Mete a la pila operador el nuevo operador
def pushOperador(operador):
    global pOper
    pOper.append(operador)

#Mete a la pila tipos el nuevo tipo
def pushTipo(tipo):
    global pTipos
    pTipos.append(tipo)

#obtiene el ultimo operando ingresado a la pila de operandos
def topOperador():
    global pOper
    last = len(pOper) - 1
    if (last < 0):
        return 'empty'
    return pOper[last]

#Ultimo tipo ingresado a la pila de tipos
def topTipo():
    global pTipos
    last = len(pTipos) - 1
    if(last < 0):
        return 'empty'
    return pTipos[last]

#Regresa el ultimo elemento de la pila de Saltos
def popSaltos():
    global pSaltos

    return pSaltos.pop()

#Agrega el nuevo salto a la pila de Saltos.
def pushSaltos(salto):
    global pSaltos
    print("PUSH SALTO: ", salto)
    pSaltos.append(salto)

#Obtiene el indice del siguiente cuadruplo del arreglo de cuadruplos
def nextQuad():
    global cuadruplos
    return len(cuadruplos)

#Regresa el ultimo cuadruplo
def popQuad():
    global cuadruplos
    return cuadruplos.pop()

#Agrega un nuevo cuadruplo al arreglo de cuadruplos
def pushQuad(quad):
    global cuadruplos
    cuadruplos.append(quad)

def pushConstante(constante):
    global d_ints
    global d_floats
    global d_strs
    global d_ch
    global d_df
    
    global cont_IntConst
    global cont_FloatConst
    global cont_StringConst
    global cont_CharConst
    global cont_dfConst

    if type(constante) == int:
        if constante not in d_ints:
            if cont_IntConst < index_intConstantes:
                d_ints[constante] = cont_IntConst
                cont_IntConst = cont_IntConst + 1
                printQuad('addConstante', 'int', constante, d_ints[constante])
            else:
                print(cont_IntConst, index_intConstantes)
                errorOutOfBounds('Constantes', 'Enteras')
        pushOperando(d_ints[constante])
        pushTipo('int')
    
    elif type(constante) == float:
        if constante not in d_floats:
            if cont_FloatConst < index_floatConstantes:
                d_floats[constante] = cont_FloatConst
                cont_FloatConst = cont_FloatConst + 1
                printQuad('addConstante', 'float', constante, d_floats[constante])
            else:
                errorOutOfBounds('Constantes', 'Flotantes')
        pushOperando(d_floats[constante])
        pushTipo('float')
    
    elif type(constante) == str:
        if constante not in d_strs:
            if cont_StringConst < index_stringConstantes:
                d_strs[constante] = cont_StringsConst
                cont_StringsConst = cont_StringsConst + 1
                printQuad('addConstante', 'string', constante, d_strs[constante])
            else:
                errorOutOfBounds('Constantes', 'Strings')
        pushOperando(d_strs[constante])
        pushTipo('string')
    
    elif type(constante) == chr:
        if constante not in d_ch:
            if cont_CharConst < index_charConstantes:
                d_chars[constante] = cont_CharConst
                cont_CharConst = cont_CharConst + 1
                printQuad('addConstante', 'char', constante, d_chars[constante])
            else:
                errorOutOfBounds('Constantes', 'Chars')
        pushOperando(d_chars[constante])
        pushTipo('char')
    else:
        sys.exit("Error: Tipo de Variable desconocida")

    

################ Funciones de impresion y Errores #####################

#Impresion de cuadruplo agregado
def printQuad(operator, leftOperand, rightOperand, result):
    tempQuad = (operator, leftOperand, rightOperand, result)
    pushQuad(tempQuad)
    print(">> Quad: ('{}','{}','{}','{}')".format(operator, leftOperand, rightOperand, result))
    print("Contador = ", nextQuad() - 1)
    print("\n")

#Impresion de lista de cuadruplos
def printQuadList():
    print("-------Cuadruplos al momento: ")

    count = 0
    for quad in cuadruplos:
        print("{}.\t{},\t{},\t{},\t{}".format(count,quad[0],quad[1],quad[2],quad[3]))
        count = count + 1


def errorTypeMismatch():
    print('Error: Type Mismatch')
    sys.exit()

#Funcion para mostrar un mensaje de error cuando se llena los maximos posibles valores temporales
def errorOutOfBounds(tipoMemoria,tipoDato):
    print("Error: Memoria llena; Muchas {} de tipo {}.".format(tipoMemoria,tipoDato))
    sys.exit()

################ Funciones de manejo de memoria##############
def nextAvailTemp(tipo):
    global cont_IntTemp
    global cont_FloatTemp
    global cont_BoolTemp
    global avail
    
    if tipo == 'int':
        if cont_IntTemp < index_intTemporales:
            avail = cont_IntTemp
            cont_IntTemp += 1
        else:
            errorOutOfBounds('temporales','Enteras')
    elif tipo == 'float':
        
        if cont_FloatTemp < index_floatTemporales:
            avail = cont_FloatTemp
            cont_FloatTemp += 1
        else:
            errorOutOfBounds('temporales','Flotantes')

    elif tipo == 'bool':
        if cont_BoolTemp < index_boolTemporales:
            avail = cont_BoolTemp
            cont_BoolTemp = cont_BoolTemp + 1
        else:
           errorOutOfBounds('temporales','Boleanas')
    else:
        avail = -1
        print("Error: Tipo de variable no existente")
    return avail
        


################ PUNTOS NEURALGICOS ###################


##########DIRECTORIO DE FUNCIONES Y TABLA DE VARIABLESpnQuadGenExp1#############
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

#Modifica la cantidad de parametros de una funcion en el directorio de funciones
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

def p_pn_9_setCurrentFuncGl(p):
    '''
    pn_9_setCurrentFuncGl :
    '''
    global currentFunc
    currentFunc = CONTEXT_GLOBAL


##### Generacion de cuadruplos #######

###### CONSTANTES ###########
def p_pnNeg(p):
    '''
    pnNeg :
    '''
    global negativo
    negativo = True

def p_pnQuadGenCteInt(p):
    '''
    pnQuadGenCteInt :
    '''
    if negativo:
        pushConstante(-1 * p[-1])
    else:
        pushConstante(p[-1])

def p_pnQuadGenCteFloat(p):
    '''
    pnQuadGenCteFloat :
    '''
    if negativo:
        pushConstante(-1 * p[-1])
    else:
        pushConstante(p[-1])

def p_pnQuadGenCteChar(p):
    '''
    pnQuadGenCteChar :
    '''
    pushConstante(p[-1])

def p_pnQuadGenCteStr(p):
    '''
    pnQuadGenCteStr :
    '''
    pushConstante(p[-1])


###### EXPRESIONES #########

'''Anadir id a poper y pTipo'''
def p_pnQuadGenExp1(p):
    '''
    pnQuadGenExp1 : 
    '''
    global currentFunc
    global directorioFunciones
    global pOperandos
    global pTipos
    global forBool
    global varFor

    idName = p[-1]
    print("ID : ", p[-1])
    print("CurrentFunc: " , currentFunc)
    idType = directorioFunciones.func_searchVarType(currentFunc, idName)
    if not idType: #Si no la encuentra en el contexto actual, cambia de contexto a Tipos
        idType = directorioFunciones.func_searchVarType(CONTEXT_GLOBAL, idName)
    
    if not idType:
        print("Error: Variable ", idName, " no declarada")
        return
    
    if forBool:
        varFor = idName

    pushOperando(idName)
    pushTipo(idType)
    print("POperandos : ", pOperandos)
    print("pTipos : ", pTipos)
    print("\n")

'''Anadir un + o - al POper'''
def p_pnQuadGenExp2(p):
    '''
    pnQuadGenExp2 : 
    '''

    global pOper

    if p[-1] not in OPERADORES_SUMARESTA:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("POper: ", pOper)

'''Anadir un * o / al POper'''
def p_pnQuadGenExp3(p):
    '''
    pnQuadGenExp3 : 
    '''

    global pOper

    if p[-1] not in OPERADORES_MULTDIV:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("POper: ", pOper)

'''Checa si el top del POper es un + o - para crear el cuadruplo de esa operacion'''
def p_pnQuadGenExp4(p):
    '''
    pnQuadGenExp4 : 
    '''
    if topOperador() in OPERADORES_SUMARESTA:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global validaCubo
        quad_resultType = validaCubo.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            errorTypeMismatch()
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            printQuad(quad_operator, quad_leftOperand, quad_rightOperand, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)


'''Checa si el top de la pila de operadores es un * o / para crear el cuadruplo  '''
def p_pnQuadGenExp5(p):
    '''
    pnQuadGenExp5 : 
    '''
    if topOperador() in OPERADORES_MULTDIV:
        
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global validaCubo
        quad_resultType = validaCubo.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            printQuad(quad_operator, quad_leftOperand, quad_rightOperand, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)

'''Agrega fondo falso '''
def p_pnQuadGenExp6(p):
    '''
    pnQuadGenExp6 : 
    '''
    pushOperador('(')

'''Quita fondo falso '''
def p_pnQuadGenExp7(p):
    '''
    pnQuadGenExp7 : 
    '''
    tipo = popOperadores()

'''Meter un operador relacional a la pila de operadores'''
def p_pnQuadGenExp8(p):
    '''
    pnQuadGenExp8 : 
    '''
    global popOperadores
    if p[-1] not in OPERADORES_REL:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("POper : ", pOper)

'''Checa si el top de la pila de operadores es un operador relacional para crear el cuadruplo de operacion'''
def p_pnQuadGenExp9(p):
    '''
    pnQuadGenExp9 : 
    '''
    if topOperador() in OPERADORES_REL:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global validaCubo
        quad_resultType = validaCubo.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            printQuad(quad_operator, quad_leftOperand, quad_rightOperand, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)

'''
Meter un operador logico a pila de operadores
'''
def p_pnQuadGenExp10(p):
    '''
    pnQuadGenExp10 : 
    '''
    global pOper
    if p[-1] not in OPERADORES_LOGICOS:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("pOper : ", pOper)

'''Checa si el top de la pila de operadores es un operador logico  '''
def p_pnQuadGenExp11(p):
    '''
    pnQuadGenExp11 : 
    '''
    if topOperador() in OPERADORES_LOGICOS:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global validaCubo
        quad_resultType = validaCubo.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            printQuad(quad_operator, quad_leftOperand, quad_rightOperand, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)


'''
Meter = a la pila operadores
'''
def p_pnQuadGenSec1(p):
    '''
    pnQuadGenSec1 : 
    '''
    global pOper
    if p[-1] not in OP_ASIG:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("pOper : ", pOper)

'''Checa si el top de la pila de operadores es una asignacion '''
def p_pnQuadGenSec2(p):
    '''
    pnQuadGenSec2 : 
    '''
    if topOperador() in OP_ASIG:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global validaCubo
        global directorioFunciones

        quad_resultType = validaCubo.getType(quad_leftType, quad_rightType, quad_operator)

        if directorioFunciones.var_exist(currentFunc, quad_leftOperand) or directorioFunciones.var_exist(CONTEXT_GLOBAL, quad_leftOperand):
            if quad_leftType == 'error':
                print("Error: Operacion invalida")
            else:
                printQuad(quad_operator, quad_rightOperand, '', quad_leftOperand)
        else:
            print("Error")



'''
Meter escribir o leer a la pila
'''
def p_pnQuadGenSec3(p):
    '''
    pnQuadGenSec3 : 
    '''
    global pOper
    if p[-1] not in OP_SECUENCIALES:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("pOper : ", pOper)

'''Checa si el top de la pila de operadores es lectura o escritura '''
def p_pnQuadGenSec4(p):
    '''
    pnQuadGenSec4 : 
    '''
    if topOperador() in OP_SECUENCIALES:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_operator = popOperadores()

        global validaCubo

        quad_resultType = validaCubo.getType(quad_operator, quad_rightType, '')

    
        if quad_resultType == 'error':
            print("Error: Operacion invalida")
        else:
            printQuad(quad_operator, quad_rightOperand, '', quad_operator)
            pushOperando(quad_rightOperand)
            pushTipo(quad_resultType)
        

# GENERACION DE CODIGO PARA ESTATUTOS NO LINEALES (CONDICIONALES)

#Genera el cuadruplo GOTOF en la condicion SI (if) depues de recibir el booleano generado por la expresion
def p_pnQuadGenCond1(p): #IF
    '''
    pnQuadGenCond1 :
    '''
    global cuadruplos
    exp_type = popTipos()
    
    if(exp_type != 'error'):
        result = popOperandos()
        printQuad('GOTOF', result,'', '')
        print("cond1: ", nextQuad())
        pushSaltos(nextQuad() - 1)

    else:
        errorTypeMismatch

    
#Rellena el cuadruplo para saber cuando terminar la condicion
def p_pnQuadGenCond2(p): #IF
    '''
    pnQuadGenCond2 :
    '''
    global cuadruplos
    
    end = popSaltos()
    
    tempQuad = (cuadruplos[end][0], cuadruplos[end][1], cuadruplos[end][2], nextQuad())
    cuadruplos[end] = tempQuad

#Genera el cuadruplo GOTO para SINO (else) y completa el cuadruplo
def p_pnQuadGenCond3(p): #IF
    '''
    pnQuadGenCond3 :
    '''
    global cuadruplos
    printQuad('GOTO', '', '', '')
    falso = popSaltos()
    print("cond3: ", nextQuad())
    pushSaltos(nextQuad() - 1)
    tempQuad = (cuadruplos[falso][0], cuadruplos[falso][1], cuadruplos[falso][2], nextQuad())
    cuadruplos[falso] = tempQuad


#Mete el siguiente cuadruplo a pSaltos. Que representa la ubicacion a donde regresara al final del ciclo para volver a evaluar la condicion
def p_pnQuadGenCiclos1(p):
    '''
    pnQuadGenCiclos1 :  
    '''
    
    pushSaltos(nextQuad())


def p_pnQuadGenCiclos2(p):
    '''
    pnQuadGenCiclos2 : 
    '''
    exp_type = popTipos()
    if exp_type != 'error':
        result = popOperandos()
        printQuad('GOTOF', result, '', '')
        pushSaltos(nextQuad() - 1)
    else:
        errorTypeMismatch()


#Genera el cuadruplo GOTO para regresar al inicio del ciclo y volver evaluar la nueva condicion. Aqui tambien se rellena el GOTOF anterior
def p_pnQuadGenCiclos3(p):
    '''
    pnQuadGenCiclos3 : 
    '''
    end = popSaltos()
    retorno = popSaltos()
    printQuad('GOTO', '', '', retorno) #Genetare quad: GOTO

    tempQuad = (cuadruplos[end][0], cuadruplos[end][1], cuadruplos[end][2], nextQuad())
    cuadruplos[end] = tempQuad #FILL (end, cont)

#Activa la variable bool de ForBool para indicar que esta entrando a un For
def p_pnQuadGenCiclos4(p):
    '''
    pnQuadGenCiclos4 : 
    '''
    global forBool
    forBool = True
    

def p_pnQuadGenCiclos5(p):
    '''
    pnQuadGenCiclos5 : 
    '''
    if topOperador() in OP_ASIG:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global validaCubo
        global directorioFunciones

        quad_resultType = validaCubo.getType(quad_leftType, quad_rightType, quad_operator)

        if directorioFunciones.var_exist(currentFunc, quad_leftOperand) or directorioFunciones.var_exist(CONTEXT_GLOBAL, quad_leftOperand):
            if quad_leftType == 'error':
                print("Error: Operacion invalida")
            else:
                printQuad(quad_operator, quad_rightOperand, '', quad_leftOperand)
        else:
            print("Error")
    
def p_pnQuadGenCiclos6(p):
    '''
    pnQuadGenCiclos6 :
    '''
    pushOperando(varFor)

    idType = directorioFunciones.func_searchVarType(currentFunc, varFor)
    if not idType: #Si no la encuentra en el contexto actual, cambia de contexto a Tipos
        idType = directorioFunciones.func_searchVarType(CONTEXT_GLOBAL, varFor)
    
    if not idType:
        print("Error: Variable ", idName, " no declarada")
        return

    pushTipo(idType)
    pushOperador('<=')
    pushSaltos(nextQuad())
    

def p_pnQuadGenCiclos7(p):
    '''
    pnQuadGenCiclos7 :
    '''
    if topOperador() in OPERADORES_REL:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()
        
        global validaCubo
        quad_resultType = validaCubo.getType(quad_leftType, quad_rightType, quad_operator)
        
        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            printQuad(quad_operator, quad_leftOperand, quad_rightOperand, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)
            
        exp_type = popTipos()
        if (exp_type != 'bool' or exp_type == 'error'):
            errorTypeMismatch()
        else:
            result = popOperandos()
            printQuad('GOTOF', result, '', '')
            pushSaltos(nextQuad() - 1)

def p_pnQuadGenCiclos8(p):
    '''
    pnQuadGenCiclos8 :
    '''
    end = popSaltos()
    retorno = popSaltos()
    printQuad('GOTO', '', '', retorno) #Genetare quad: GOTO

    tempQuad = (cuadruplos[end][0], cuadruplos[end][1], cuadruplos[end][2], nextQuad())
    cuadruplos[end] = tempQuad #FILL (end, cont) 


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
int : A, B, C, D;

principal()
{

A = -5.6 +  C;

}
'''
tempQuad = ('0', '0', '0', '0')
pushQuad(tempQuad)

parser = yacc.yacc()
result = parser.parse(data)

print(result)
# print(directorioFunciones.func_search(CONTEXT_GLOBAL))