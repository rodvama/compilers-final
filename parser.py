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

#Objetos
directorioFunciones = DirFunc()
cuboSem = CuboSemantico()
cuboSemEsp = CuboSemantico_FuncEsp()


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
GBL = 'global'
OP_SUMARESTA = ['+', '-']
OP_MULTDIV = ['*', '/']
OP_REL = ['>', '<', '<=', '>=', '==', '!=']
OP_LOGICOS = ['&', '|']
OP_ASIG = ['=']
OP_SECUENCIALES = ['lee', 'escribe']
ESPACIO_MEMORIA = 100 #Tamano del espacio de memoria

##Variables globales
currentFunc = GBL
currentType = "void"
varName = ""
currentCantParams = 0
currentCantVars = 0
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
limite_intGlobales = ESPACIO_MEMORIA
limite_floatGlobales = limite_intGlobales + ESPACIO_MEMORIA
limite_stringsGlobales = limite_floatGlobales + ESPACIO_MEMORIA
limite_charGlobales = limite_stringsGlobales + ESPACIO_MEMORIA
limite_dfGlobales = limite_charGlobales + ESPACIO_MEMORIA

limite_intLocales = limite_dfGlobales + ESPACIO_MEMORIA
limite_floatLocales = limite_intLocales + ESPACIO_MEMORIA
limite_stringsLocales = limite_floatLocales + ESPACIO_MEMORIA
limite_charLocales = limite_stringsLocales + ESPACIO_MEMORIA
limite_dfLocales = limite_charLocales + ESPACIO_MEMORIA

limite_intTemporales = limite_dfLocales + ESPACIO_MEMORIA
limite_floatTemporales = limite_intTemporales + ESPACIO_MEMORIA
limite_stringsTemporales = limite_floatTemporales + ESPACIO_MEMORIA
limite_charTemporales = limite_stringsTemporales + ESPACIO_MEMORIA
limite_dfTemporales = limite_charTemporales + ESPACIO_MEMORIA
limite_boolTemporales = limite_dfTemporales + ESPACIO_MEMORIA

limite_intConstantes = limite_boolTemporales + ESPACIO_MEMORIA
limite_floatConstantes = limite_intConstantes + ESPACIO_MEMORIA
limite_stringConstantes = limite_floatConstantes + ESPACIO_MEMORIA
limite_charConstantes = limite_stringConstantes + ESPACIO_MEMORIA
limite_dfConstantes = limite_charConstantes + ESPACIO_MEMORIA


#Declaracion de inicio de index de memoria para temporales
cont_IntTemporales = limite_dfLocales
cont_FloatTemporales = limite_intTemporales
cont_StringTemporales = limite_floatTemporales
cont_CharTemporales = limite_stringsTemporales
cont_dfTemporales = limite_charTemporales
cont_BoolTemporales = limite_dfTemporales


#Declaracion de inicio de los inde de memoria para constantes 
cont_IntConstantes = limite_boolTemporales
cont_FloatConstantes = limite_intConstantes
cont_StringConstantes = limite_floatConstantes
cont_CharConstantes = limite_stringConstantes
cont_dfConstantes = limite_charConstantes


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
    'asignacion : variable ASSIGN pnSec1 asig'

def p_asig(p):
    '''
    asig : llamada
         | exp SEMICOLON pnSec2
    '''
def p_variable(p):
    'variable : ID pnExp1 di'

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
    'lectura : LEE pnSec3 LPAREN variable RPAREN SEMICOLON pnSec4'

def p_escritura(p):
    'escritura : ESCRIBE pnSec3 LPAREN esc RPAREN SEMICOLON pnSec4'

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
    'decision : SI LPAREN expresion RPAREN pnCond1 ENTONCES bloque sino pnCond2'

def p_sino(p): #ELSE
    '''
    sino : SINO pnCond3 bloque
         | empty
    '''


def p_condicional(p): #While
    'condicional : MIENTRAS pnCiclos1 LPAREN expresion RPAREN pnCiclos2 HAZ bloque pnCiclos3'

def p_no_condicional(p): #For
    'no_condicional : DESDE pnCiclos4 variable ASSIGN pnSec1 exp pnCiclos5 HASTA pnCiclos6 exp pnCiclos7 HACER bloque pnCiclos8'


def p_funciones_especiales_void(p):
    '''
    funciones_especiales_void : VARIABLES LPAREN ID COMMA ID COMMA ID RPAREN SEMICOLON
                              | fev LPAREN ID COMMA v_exp RPAREN SEMICOLON
    '''
def p_fev(p):
    '''
    fev : PLOTHIST
        | PLOTLINE
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
    var_cte : CTE_CH pnCteChar
            | CTE_STR pnCteStr
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
    var_num : CTE_INT pnCteInt
            | CTE_FLOAT pnCteFloat
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
    meg : op_l pnExp10 mega_exp pnExp11
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
    sp : op_r  exp pnExp9
       | empty
    '''
def p_op_r(p):
    '''
    op_r : LT pnExp8
         | GT pnExp8
         | LE pnExp8
         | GE pnExp8
         | NOT_EQUAL pnExp8
         | EQUAL pnExp8
    '''

def p_exp(p):
    'exp : termino pnExp4 exp1'

def p_exp1(p):
    '''
    exp1 : op_a exp
         | empty
    '''
def p_op_a(p):
    '''
    op_a : ADD pnExp2
         | SUB pnExp2
    '''

def p_termino(p):
    'termino : factor pnExp5 term'

def p_term(p):
    '''
    term : op_a1 termino
         | empty
    '''
def p_op_a1(p):
    '''
    op_a1 : MUL pnExp3
          | DIV pnExp3
    '''

def p_factor(p):
    '''
    factor : var_cte
           | LPAREN pnExp6 exp RPAREN pnExp7
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

#Agrega las constantes a la pila de Operandos y Tipos
def pushConstante(constante):
    global d_ints
    global d_floats
    global d_strs
    global d_ch
    global d_df
    
    global cont_IntConstantes
    global cont_FloatConstantes
    global cont_StringConstantes
    global cont_CharConstantes
    global cont_dfConstantes

    if type(constante) == int:
        if constante not in d_ints:
            if cont_IntConstantes < limite_intConstantes:
                d_ints[constante] = cont_IntConstantes
                cont_IntConstantes = cont_IntConstantes + 1
                printQuad('addConstante', 'int', constante, d_ints[constante])
            else:
                print(cont_IntConstantes, limite_intConstantes)
                errorOutOfBounds('Constantes', 'Enteras')
        pushOperando(d_ints[constante])
        pushTipo('int')
    
    elif type(constante) == float:
        if constante not in d_floats:
            if cont_FloatConstantes < limite_floatConstantes:
                d_floats[constante] = cont_FloatConstantes
                cont_FloatConstantes = cont_FloatConstantes + 1
                printQuad('addConstante', 'float', constante, d_floats[constante])
            else:
                errorOutOfBounds('Constantes', 'Flotantes')
        pushOperando(d_floats[constante])
        pushTipo('float')
    
    elif type(constante) == str:
        if constante not in d_strs:
            if cont_StringConstantes < limite_stringConstantes:
                d_strs[constante] = cont_StringsConst
                cont_StringsConst = cont_StringsConst + 1
                printQuad('addConstante', 'string', constante, d_strs[constante])
            else:
                errorOutOfBounds('Constantes', 'Strings')
        pushOperando(d_strs[constante])
        pushTipo('string')
    
    elif type(constante) == chr:
        if constante not in d_ch:
            if cont_CharConstantes < limite_charConstantes:
                d_chars[constante] = cont_CharConstantes
                cont_CharConstantes = cont_CharConstantes + 1
                printQuad('addConstante', 'char', constante, d_chars[constante])
            else:
                errorOutOfBounds('Constantes', 'Chars')
        pushOperando(d_chars[constante])
        pushTipo('char')
    else:
        sys.exit("Error: Tipo de Variable desconocida")

    

################ Funciones de impresion y Errores #####################

#Impresion de nuevo cuadruplo
def printQuad(operator, leftOperand, rightOperand, result):
    QuadTemporal = (operator, leftOperand, rightOperand, result)
    pushQuad(QuadTemporal)
    print(">> Quad: ('{}','{}','{}','{}')".format(operator, leftOperand, rightOperand, result))
    print("Contador = ", nextQuad() - 1)
    print("\n")

#Impresion de lista de cuadruplos
def printQuadList():
    print("-------Lista de Cuadruplos: ")

    contador = 0
    for quad in cuadruplos:
        print("{}.\t{},\t{},\t{},\t{}".format(contador,quad[0],quad[1],quad[2],quad[3]))
        contador = contador + 1

#Funcion que muestra menssaje de error cuando los tipos no coinciden
def errorTypeMismatch():
    print('Error: Type Mismatch')
    sys.exit()

#Funcion para mostrar un mensaje de error cuando se llena los maximos posibles valores temporales
def errorOutOfBounds(tipoMemoria,tipoDato):
    print("Error: Memoria llena; Muchas {} de tipo {}.".format(tipoMemoria,tipoDato))
    sys.exit()

################ Funciones de manejo de memoria##############

#Regresa el siguiente temporal disponible, dependiendo el tipo
def nextAvailTemp(tipo):
    global cont_IntTemporales
    global cont_FloatTemporales
    global cont_BoolTemporales
    global avail
    
    if tipo == 'int':
        if cont_IntTemporales < limite_intTemporales:
            avail = cont_IntTemporales
            cont_IntTemporales += 1
        else:
            errorOutOfBounds('temporales','Enteras')
    elif tipo == 'float':
        
        if cont_FloatTemporales < limite_floatTemporales:
            avail = cont_FloatTemporales
            cont_FloatTemporales += 1
        else:
            errorOutOfBounds('temporales','Flotantes')

    elif tipo == 'bool':
        if cont_BoolTemporales < limite_boolTemporales:
            avail = cont_BoolTemporales
            cont_BoolTemporales = cont_BoolTemporales + 1
        else:
           errorOutOfBounds('temporales','Boleanas')
    else:
        avail = -1
        print("Error: Tipo de variable no existente")
    return avail
        


################ PUNTOS NEURALGICOS ###################


##########DIRECTORIO DE FUNCIONES Y TABLA DE VARIABLES#############

'''
Establece el currentType
'''
def p_pn_1_setCurrentType(p):
    '''
    pn_1_setCurrentType :
    '''
    global currentType
    currentType = p[-1]

'''
Agrega la nueva variable a la tabla de variables
'''
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

'''
Agega nueva funcion al Directorio de Funciones
'''
def p_pn_3_addFunction(p):
    '''
    pn_3_addFunction : 
    '''
    global currentFunc
    global currentType
    global currentCantParams

    currentCantParams = 0

    currentFunc = p[-1]
    directorioFunciones.func_add(currentFunc, currentType, currentCantParams)

'''
Cuenta la cantidad de parametros que tiene una funcion
'''
def p_pn_4_params(p):
    '''
    pn_4_params :
    '''
    global currentFunc
    global currentType
    global currentCantParams
    global varName

    varName = p[-1]
    directorioFunciones.func_addVar(currentFunc, varName, currentType, 0, 0)
    currentCantParams += 1

'''
Modifica la cantidad de parametros de una funcion en el directorio de funciones
'''
def p_pn_5_updateContParams(p):
    '''
    pn_5_updateContParams :  
    '''
    global currentFunc
    global currentCantParams

    directorioFunciones.func_UpdateParametros(currentFunc, currentCantParams)

'''
Elimina el directorio de funciones
'''
def p_pn_6_end(p):
    '''
    pn_6_end :
    '''
    #directorioFunciones.func_deleteDic()

'''
Guarda la cantidad de Renglones que tiene la variable
'''
def p_pn_7_decRenglones(p):
    '''
    pn_7_decRenglones :
    '''

    global numRenglones
    numRenglones = p[-2]

'''
Guarda la cantidad de columnas que tiene la variable
'''
def p_pn_8_decColumnas(p):
    '''
    pn_8_decColumnas : 
    '''
    global numColumnas
    numColumnas = p[-2]

'''
Establece que la funcion actual es la Global
'''
def p_pn_9_setCurrentFuncGl(p):
    '''
    pn_9_setCurrentFuncGl :
    '''
    global currentFunc
    currentFunc = GBL


################################## Generacion de cuadruplos #############################################

###### CONSTANTES ###########
'''
Si hay un negativo, activa el booleano para indicar que es negativo
'''
def p_pnNeg(p):
    '''
    pnNeg :
    '''
    global negativo
    negativo = True

'''
Agrega la constante Entera a la pila de Constantes
'''
def p_pnCteInt(p):
    '''
    pnCteInt :
    '''
    if negativo:
        pushConstante(-1 * p[-1])
    else:
        pushConstante(p[-1])

'''
Agrega la constante Flotante a la pila de Constantes
'''
def p_pnCteFloat(p):
    '''
    pnCteFloat :
    '''
    if negativo:
        pushConstante(-1 * p[-1])
    else:
        pushConstante(p[-1])

'''
Agrega la constante Char a la pila de Constantes
'''
def p_pnCteChar(p):
    '''
    pnCteChar :
    '''
    pushConstante(p[-1])

'''
Agrega la constante String a la pila de Constantes
'''
def p_pnCteStr(p):
    '''
    pnCteStr :
    '''
    pushConstante(p[-1])


###### EXPRESIONES #########

'''Anade id y Tipo a poper y pTipo respectivamente'''
def p_pnExp1(p):
    '''
    pnExp1 : 
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
        idType = directorioFunciones.func_searchVarType(GBL, idName)
    
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

'''Anade  + o - al POper'''
def p_pnExp2(p):
    '''
    pnExp2 : 
    '''

    global pOper

    if p[-1] not in OP_SUMARESTA:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("POper: ", pOper)

'''Anade * o / al POper'''
def p_pnExp3(p):
    '''
    pnExp3 : 
    '''

    global pOper

    if p[-1] not in OP_MULTDIV:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("POper: ", pOper)

'''Checa si el top del POper es un + o - para generar el cuadruplo de esa operacion'''
def p_pnExp4(p):
    '''
    pnExp4 : 
    '''
    if topOperador() in OP_SUMARESTA:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            errorTypeMismatch()
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            printQuad(quad_operator, quad_leftOperand, quad_rightOperand, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)


'''Checa si el top de la pila de operadores es un * o / para generar el cuadruplo  '''
def p_pnExp5(p):
    '''
    pnExp5 : 
    '''
    if topOperador() in OP_MULTDIV:
        
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            printQuad(quad_operator, quad_leftOperand, quad_rightOperand, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)

'''Agrega fondo falso '''
def p_pnExp6(p):
    '''
    pnExp6 : 
    '''
    pushOperador('(')

'''Quita fondo falso '''
def p_pnExp7(p):
    '''
    pnExp7 : 
    '''
    tipo = popOperadores()

'''Mete un operador relacional a la pila de operadores'''
def p_pnExp8(p):
    '''
    pnExp8 : 
    '''
    global popOperadores
    if p[-1] not in OP_REL:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("POper : ", pOper)

'''Verifica si el top de la pila de operadores es un operador relacional para generar el cuadruplo de operacion'''
def p_pnExp9(p):
    '''
    pnExp9 : 
    '''
    if topOperador() in OP_REL:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

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
def p_pnExp10(p):
    '''
    pnExp10 : 
    '''
    global pOper
    if p[-1] not in OP_LOGICOS:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("pOper : ", pOper)

'''Checa si el top de la pila de operadores es un operador logico  '''
def p_pnExp11(p):
    '''
    pnExp11 : 
    '''
    if topOperador() in OP_LOGICOS:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            printQuad(quad_operator, quad_leftOperand, quad_rightOperand, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)


'''
Mete '=' a la pila operadores
'''
def p_pnSec1(p):
    '''
    pnSec1 : 
    '''
    global pOper
    if p[-1] not in OP_ASIG:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("pOper : ", pOper)

'''Checa si en el top de la pila de operadores hay una asignacion (=) '''
def p_pnSec2(p):
    '''
    pnSec2 : 
    '''
    if topOperador() in OP_ASIG:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        global directorioFunciones

        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

        if directorioFunciones.var_exist(currentFunc, quad_leftOperand) or directorioFunciones.var_exist(GBL, quad_leftOperand):
            if quad_leftType == 'error':
                print("Error: Operacion invalida")
            else:
                printQuad(quad_operator, quad_rightOperand, '', quad_leftOperand)
        else:
            print("Error")



'''
Meter escribir o leer a la pila
'''
def p_pnSec3(p):
    '''
    pnSec3 : 
    '''
    global pOper
    if p[-1] not in OP_SECUENCIALES:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
        print("pOper : ", pOper)

'''Checa si el top de la pila de operadores es lectura o escritura '''
def p_pnSec4(p):
    '''
    pnSec4 : 
    '''
    if topOperador() in OP_SECUENCIALES:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_operator = popOperadores()

        global cuboSem

        quad_resultType = cuboSem.getType(quad_operator, quad_rightType, '')

    
        if quad_resultType == 'error':
            print("Error: Operacion invalida")
        else:
            printQuad(quad_operator, quad_rightOperand, '', quad_operator)
            pushOperando(quad_rightOperand)
            pushTipo(quad_resultType)
        

# GENERACION DE CODIGO PARA ESTATUTOS NO LINEALES (CONDICIONALES)
'''
Genera el cuadruplo GOTOF en la condicion SI (if) depues de recibir el booleano generado por la expresion
'''
def p_pnCond1(p): #IF
    '''
    pnCond1 :
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

'''
Rellena el cuadruplo para saber cuando terminar la condicion
'''   
def p_pnCond2(p): #IF
    '''
    pnCond2 :
    '''
    global cuadruplos
    
    end = popSaltos()
    
    QuadTemporal = (cuadruplos[end][0], cuadruplos[end][1], cuadruplos[end][2], nextQuad())
    cuadruplos[end] = QuadTemporal

'''
Genera el cuadruplo GOTO para SINO (else) y completa el cuadruplo
'''
def p_pnCond3(p): #IF
    '''
    pnCond3 :
    '''
    global cuadruplos
    printQuad('GOTO', '', '', '')
    falso = popSaltos()
    print("cond3: ", nextQuad())
    pushSaltos(nextQuad() - 1)
    QuadTemporal = (cuadruplos[falso][0], cuadruplos[falso][1], cuadruplos[falso][2], nextQuad())
    cuadruplos[falso] = QuadTemporal

'''
Mete el siguiente cuadruplo a pSaltos. Que representa la ubicacion a donde regresara al final del ciclo para volver a evaluar la condicion
'''
def p_pnCiclos1(p):
    '''
    pnCiclos1 :  
    '''
    
    pushSaltos(nextQuad())

'''
Genera el cuadruplo de GOTOF
'''
def p_pnCiclos2(p):
    '''
    pnCiclos2 : 
    '''
    exp_type = popTipos()
    if exp_type != 'error':
        result = popOperandos()
        printQuad('GOTOF', result, '', '')
        pushSaltos(nextQuad() - 1)
    else:
        errorTypeMismatch()

'''
Genera el cuadruplo GOTO para regresar al inicio del ciclo y volver evaluar la nueva condicion. Aqui tambien se rellena el GOTOF anterior
'''
def p_pnCiclos3(p):
    '''
    pnCiclos3 : 
    '''
    end = popSaltos()
    retorno = popSaltos()
    printQuad('GOTO', '', '', retorno) #Genetare quad: GOTO

    QuadTemporal = (cuadruplos[end][0], cuadruplos[end][1], cuadruplos[end][2], nextQuad())
    cuadruplos[end] = QuadTemporal #FILL (end, cont)

'''
Activa la variable bool de ForBool para indicar que esta entrando a un For
'''
def p_pnCiclos4(p):
    '''
    pnCiclos4 : 
    '''
    global forBool
    forBool = True
    
'''
Hace verificaciones si existen las variables y si los tipos son compatibles
'''
def p_pnCiclos5(p):
    '''
    pnCiclos5 : 
    '''
    if topOperador() in OP_ASIG:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        global directorioFunciones

        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

        if directorioFunciones.var_exist(currentFunc, quad_leftOperand) or directorioFunciones.var_exist(GBL, quad_leftOperand):
            if quad_leftType == 'error':
                print("Error: Operacion invalida")
            else:
                printQuad(quad_operator, quad_rightOperand, '', quad_leftOperand)
        else:
            print("Error")

'''

'''
def p_pnCiclos6(p):
    '''
    pnCiclos6 :
    '''
    pushOperando(varFor)

    idType = directorioFunciones.func_searchVarType(currentFunc, varFor)
    if not idType: #Si no la encuentra en el contexto actual, cambia de contexto a Tipos
        idType = directorioFunciones.func_searchVarType(GBL, varFor)
    
    if not idType:
        print("Error: Variable ", idName, " no declarada")
        return

    pushTipo(idType)
    pushOperador('<=')
    pushSaltos(nextQuad())
    
'''

'''
def p_pnCiclos7(p):
    '''
    pnCiclos7 :
    '''
    if topOperador() in OP_REL:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()
        
        global cuboSem
        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)
        
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

'''

'''
def p_pnCiclos8(p):
    '''
    pnCiclos8 :
    '''
    end = popSaltos()
    retorno = popSaltos()
    printQuad('GOTO', '', '', retorno) #Genetare quad: GOTO

    QuadTemporal = (cuadruplos[end][0], cuadruplos[end][1], cuadruplos[end][2], nextQuad())
    cuadruplos[end] = QuadTemporal #FILL (end, cont) 


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
QuadTemporal = ('0', '0', '0', '0')
pushQuad(QuadTemporal)

parser = yacc.yacc()
result = parser.parse(data)

print(result)
# print(directorioFunciones.func_search(GBL))