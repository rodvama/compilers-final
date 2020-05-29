# Jose Arturo Villalobos A00818214
# Rodrigo Valencia A00818256
# Diseno de compiladores
# Parser
#Ultima modificacion: 23 Mayo 2020
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
tablaVariables = TablaVars()
cuboSem = CuboSemantico()
cuboSemEsp = CuboSemantico_FuncEsp()


### Pilas para generacion de cuadruplos ####
pOperandos = [] #Pila de operandos pendientes (PilaO)
pOper = [] #Pila de operadores pendientes (POper)
pTipos = [] #Pila de tipos
pSaltos = [] #Pila de saltos para condiciones y ciclos
pFunciones = [] #Pila de funciones
pArgumentos = [] #Pila de agumentos de una funcion
pMemorias = [] # Pila de direcciones de memoria
pDim = [] #Pila de Arreglos

#Arreglo donde se almacenaran todos los cuadruplos que se vayan generando
cuadruplos = []

#Diccionarios de constantes que cuardan la direccion de memoria de constantes
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
OP_SECUENCIALES = ['lee', 'escribe', 'regresa']
ESPACIO_MEMORIA = 1000 #Tamano del espacio de memoria

##Variables globales
currentFunc = GBL
currentType = "void"
varName = ""
currentVarName = ""
currentCantParams = 0
currentCantVars = 0
avail = 0
constanteNegativa = False
forBool = False
varFor = ''
negativo = False
returnBool = False #sirve para saber si una funcion debe regresar algun valor (si es void o no)


#Variables para Arreglos y matrices
isArray = False
isMatrix = False
numRenglones = 0
numColumnas = 0
R = 1 #m0
dirBase = 0 #Direccion base
currentConstArrays = []

'''
Espacios de memoria:
+++++++++++++++++++++++
+globales enteras     + ESPACIO MEMORIA
+---------------------+
+globales flotantes   + ESPACIO MEMORIA
+---------------------+
+globales strings     + ESPACIO MEMORIA
+---------------------+
+globales char       + ESPACIO MEMORIA
+---------------------+
+globales dataframes  + ESPACIO MEMORIA
+++++++++++++++++++++++
+locales enteras      + ESPACIO MEMORIA
+---------------------+
+locales flotantes    + ESPACIO MEMORIA
+---------------------+
+locales strings      + ESPACIO MEMORIA
+---------------------+
+locales char         + ESPACIO MEMORIA
+---------------------+
+locales dataframes   + ESPACIO MEMORIA
+++++++++++++++++++++++
+temp enteras         + ESPACIO MEMORIA
+---------------------+
+temp flotantes       + ESPACIO MEMORIA
+---------------------+
+temp strings         + ESPACIO MEMORIA
+---------------------+
+temp char            + ESPACIO MEMORIA
+---------------------+
+temp dataframes      + ESPACIO MEMORIA
+---------------------+
+temp booleanas       + ESPACIO MEMORIA
+++++++++++++++++++++++
+constantes enteras   + ESPACIO MEMORIA
+---------------------+
+constantes flotantes + ESPACIO MEMORIA
+---------------------+
+constantes strings   + ESPACIO MEMORIA
+---------------------+
+constantes char      + ESPACIO MEMORIA
+---------------------+
+constantes dataframe    + ESPACIO MEMORIA
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


#Inicio de memoria para Globales
cont_IntGlobales = 0
cont_FloatGlobales = limite_intGlobales
cont_StringGlobales = limite_floatGlobales
cont_CharGlobales = limite_stringsGlobales
cont_dfGlobales = limite_charGlobales

#Inicio de memoria para Locales
cont_IntLocales = limite_dfGlobales
cont_FloatLocales = limite_intLocales
cont_StringLocales = limite_floatLocales
cont_CharLocales = limite_stringsLocales
cont_dfLocales = limite_charLocales

#Inicio de memoria para Temporales
cont_IntTemporales = limite_dfLocales
cont_FloatTemporales = limite_intTemporales
cont_StringTemporales = limite_floatTemporales
cont_CharTemporales = limite_stringsTemporales
cont_dfTemporales = limite_charTemporales
cont_BoolTemporales = limite_dfTemporales


#Inicio de memoria para Constatnes
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
    'programa : PROGRAMA ID SEMICOLON var1 pnGOTOprincipal func1 principal'
    print("PROGRAMA \"", p[2], "\" terminado.")
    QuadGenerateList()
    print("Poper : ", pOper)
    print("pOperandos: ", pOperandos)
    print("pTipos: ", pTipos)
    
    
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
    'principal : PRINCIPAL pnPrincipal2 LPAREN RPAREN bloque'
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
    'funcion : FUNCION tipo_fun ID pnFunDec1 LPAREN parametros RPAREN pnFunDec4 var1 bloque pnFunDec7'
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
    'param : tipo_simple ID pnFunDec_2_3 param1'
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
    'lista : ID pn_2_addVariable dd lista1'

def p_dd(p):
    '''
    dd : dim_dec pnDimDec8
       | empty
    '''

def p_lista1(p):
    '''
    lista1 : COMMA lista
           | empty
    '''

#Dimensiones
def p_dim_dec(p):
    'dim_dec : LBRACK pnDimDec2_3 CTE_INT pnDimDec5 RBRACK pn_7_decRenglones dim_dec1'

def p_dim_dec1(p):
    '''
    dim_dec1 : LBRACK CTE_INT pnDimDec6 RBRACK pn_8_decColumnas
             | empty
    '''

def p_dim_index(p):
    'dim_index : LBRACK pnDimAccess2 pnExp6 exp pnActivaArray pnArregloAcc RBRACK pnExp7 dim_index1'

def p_dim_index1(p):
    '''
    dim_index1 : LBRACK pnExp6 exp pnActivaArray RBRACK pnExp7 pnMatrizAcc
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
    'asignacion : variable ASSIGN pnSec1 exp SEMICOLON pnSec2'

# def p_asig(p):
#     '''
#     asig : llamada 
#          | exp SEMICOLON pnSec2
#     '''
def p_variable(p):
    'variable : ID pnExp1 di'

def p_di(p):
    '''
    di : dim_index
       | empty
    '''

def p_llamada(p):
    'llamada :  ID pnFunCall_1_2 LPAREN llamada1 RPAREN pnFunCall_5_6_llamada'
    p[0] = 'llamada'
    

def p_llamada1(p):
    '''
    llamada1 : exp pnFunCall_3 llamada2
             | empty
    '''
    

def p_llamada2(p):
    '''
    llamada2 : COMMA llamada1
             | empty
    '''
    

def p_retorno(p):
    'retorno : REGRESA pnSec3 LPAREN exp RPAREN pnRetorno SEMICOLON'

def p_lectura(p):
    'lectura : LEE pnSec3 LPAREN variable RPAREN SEMICOLON pnSec4 pnSec5'

def p_escritura(p):
    'escritura : ESCRIBE pnSec3 LPAREN esc RPAREN SEMICOLON pnSec5 '

def p_esc(p):
    'esc : esc1 esc2'

def p_esc1(p):
    '''
    esc1 : exp pnSec4 
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
    funciones_especiales_void : VARIABLES pnFunEsp1 LPAREN ID COMMA ID COMMA ID RPAREN SEMICOLON
                              | fev LPAREN ID COMMA v_exp RPAREN SEMICOLON
    '''
def p_fev(p):
    '''
    fev : PLOTHIST pnFunEsp1
        | PLOTLINE pnFunEsp1
    '''

def p_funciones_especiales(p):
    '''
    funciones_especiales : fe LPAREN ID COMMA v_exp RPAREN
                         | CORRELACIONA pnFunEsp1 LPAREN ID COMMA v_exp COMMA v_exp RPAREN
    '''
def p_fe(p):
    '''
    fe : MEDIA pnFunEsp1
       | MEDIANA pnFunEsp1
       | MODA pnFunEsp1
       | VARIANZA pnFunEsp1
    '''
def p_v_exp(p):
    'v_exp : VARIABLES  LBRACK exp RBRACK'




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
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>FACTOOR")

def p_empty(p):
    '''empty :'''
    pass
    # print("nulo")

def p_error(p):
    if p:
        print("Error de sintaxis ",p.type, p.value)
        print("Error en la linea "+str(p.lineno))
        print()
        parser.errok()
    else:
        print("Syntax error at EOF")

############## FUNCIONES DE LAS PILAS ################

#Te regresa el ultimo elemento de la pila de operandos
def popOperandos():
    global pOperandos
    pop = pOperandos.pop()
    print("--------------------> POP Operandos")
    print("Pop Operandos= ", pop)
    return pop

#Te regresa el ultimo elemento de la pila de operadores
def popOperadores():
    global pOper
    pop = pOper.pop()
    print("--------------------> POP POper")
    print("Pop Poper= ", pop)
    return pop

#Te regresa el ultimo elemento de la pila de tipos
def popTipos():
    global pTipos
    pop = pTipos.pop()
    print("--------------------> POP Tipos")
    print("Pop Tipos = ", pop)
    return pop

#Mete a la pila operandos el nuevo operando
def pushOperando(operando):
    global pOperandos
    pOperandos.append(operando)
    print("------> pushOperando : ", operando)
    print("POperandos : ", pOperandos)

#Mete a la pila operador el nuevo operador
def pushOperador(operador):
    global pOper
    pOper.append(operador)
    print("------> pushOperador : ", operador)
    print("POper : ", pOper)
    

#Mete a la pila tipos el nuevo tipo
def pushTipo(tipo):
    global pTipos
    pTipos.append(tipo)
    print("------>pushTipo : ", tipo)
    print("pTipos : ", pTipos)

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
    #print("PUSH SALTO: ", salto)
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
                QuadGenerate('CONS', 'int', constante, d_ints[constante])
            else:
                print(cont_IntConstantes, limite_intConstantes)
                errorOutOfBounds('Constantes', 'Enteras')
        pushOperando(constante)
        pushMemoria(d_ints[constante])
        pushTipo('int')
    
    elif type(constante) == float:
        if constante not in d_floats:
            if cont_FloatConstantes < limite_floatConstantes:
                d_floats[constante] = cont_FloatConstantes
                cont_FloatConstantes = cont_FloatConstantes + 1
                QuadGenerate('CONS', 'float', constante, d_floats[constante])
            else:
                errorOutOfBounds('Constantes', 'Flotantes')
        pushOperando(constante)
        pushMemoria(d_floats[constante])
        pushTipo('float')
    
    elif type(constante) == str:
        if len(constante) > 3: #String
            if constante not in d_strs:
                if cont_StringConstantes < limite_stringConstantes:
                    d_strs[constante] = cont_StringConstantes
                    cont_StringConstantes += 1
                    print("LENG",len(constante), constante)
                    QuadGenerate('CONS', 'string', constante, d_strs[constante])
                else:
                    errorOutOfBounds('constantes', 'Strings')
            pushOperando(constante)
            pushMemoria(d_strs[constante])
            pushTipo('string')
        else: #Char
            if constante not in d_ch:
                if cont_CharConstantes < limite_charConstantes:
                    d_ch[constante] = cont_CharConstantes
                    cont_CharConstantes += 1
                    QuadGenerate('CONS', 'char', constante, d_ch[constante])
                else:
                    errorOutOfBounds('constantes', 'Chars')
            pushOperando(constante)
            pushMemoria(d_ch[constante])
            pushTipo('char')
    else:
        sys.exit("Error: Tipo de Variable desconocida")


'''
Regresa la direccion de memoria de una constante, y si no está declarada la agrega.
''' 

def getAddConst(constante):

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
                cont_IntConstantes += 1
                QuadGenerate('CONS', 'int', constante, d_ints[constante])
            
            else:
                errorOutOfBounds('constantes', 'Enteras')
        return d_ints[constante]
    
    elif type(constante) == float:
        if constante not in d_floats:
            if cont_FloatConstantes < limite_floatConstantes:
                d_floats[constante] = cont_FloatConstantes
                cont_FloatConstantes += 1
                QuadGenerate('CONS', 'float', constante, d_floats[constante])
            
            else:
                errorOutOfBounds('constantes', 'Flotantes')
        return d_floats[constante]
    
    elif type(constante) == str:
        if len(constante) > 1: #String
            if constante not in d_strs:
                if cont_StringConstantes < limite_stringConstantes:
                    d_strs[constante] = cont_StringConstantes
                    cont_StringConstantes += 1
                    QuadGenerate('CONS', 'string', constante, d_strs[constante])
                else:
                    errorOutOfBounds('constantes', 'Strings')
            
            return d_strs[constante]

        else: #Char
            if constante not in d_ch:
                if cont_CharConstantes < limite_charConstantes:
                    d_ch[constante] = cont_CharConstantes
                    cont_CharConstantes += 1
                    QuadGenerate('CONS', 'char', constante, d_ch[constante])
                else:
                    errorOutOfBounds('constantes', 'Chars')
        
            return d_ch[constante]

    else: 
        sys.exit("Error en getAddConst")






################ Funciones de impresion y Errores #####################

#Impresion de nuevo cuadruplo
def QuadGenerate(operator, leftOperand, rightOperand, result):
    QuadTemporal = (operator, leftOperand, rightOperand, result)
    pushQuad(QuadTemporal)
    NumQuad = nextQuad() - 1
    print(">> Quad {}: ('{}','{}','{}','{}')".format(NumQuad, operator, leftOperand, rightOperand, result))
    
    print("\n")

#Impresion de lista de cuadruplos
def QuadGenerateList():
    
    print(directorioFunciones.func_print(GBL))
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

def errorReturnTipo():
    print("Error: el tipo que intenta retornar no es correcto")

################ Funciones de manejo de memoria##############

'''
Regresa el siguiente temporal disponible, dependiendo el tipo
'''
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

'''
Regresa el siguiente espacio de memoria disponible
'''
def nextAvailMemory(contexto, tipo):
    global cont_IntGlobales
    global cont_IntLocales
    global cont_FloatGlobales
    global cont_FloatLocales
    global cont_StringGlobales
    global cont_StringLocales
    global cont_CharGlobales
    global cont_CharLocales
    global cont_dfGlobales
    global cont_dfLocales

    posMem = -1
    
    #Global
    if contexto == GBL:

        if tipo == 'int':
            if cont_IntGlobales < limite_intGlobales:
                posMem = cont_IntGlobales
                cont_IntGlobales += 1
            else:
                errorOutOfBounds(GBL, 'Enteras')
        

        elif tipo == 'float':
            if cont_FloatGlobales < limite_floatGlobales:
                posMem = cont_FloatGlobales
                cont_FloatGlobales += 1
            else:
                errorOutOfBounds(GBL, 'Floats')

        elif tipo == 'string':
            if cont_StringGlobales < limite_stringsGlobales:
                posMem = cont_StringGlobales
                cont_StringGlobales += 1
            else:
                errorOutOfBounds(GBL, 'Strings')

        elif tipo == 'char':
            if cont_CharGlobales < limite_charGlobales:
                posMem = cont_CharGlobales
                cont_CharGlobales += 1
            else:
                errorOutOfBounds(GBL, 'Chars')

        elif tipo == 'dataframe':
            if cont_dfGlobales < limite_dfGlobales:
                posMem = cont_dfGlobales
                cont_dfGlobales += 1
            else:
                errorOutOfBounds(GBL, 'Dataframes')
    #Locales
    else:
        if tipo == 'int':
            if cont_IntLocales < limite_intLocales:
                posMem = cont_IntLocales
                cont_IntLocales += 1
            else:
                errorOutOfBounds('Locales', 'Enteras')
        

        elif tipo == 'float':
            if cont_FloatLocales < limite_floatLocales:
                posMem = cont_FloatLocales
                cont_FloatLocales += 1
            else:
                errorOutOfBounds('Locales', 'Floats')

        elif tipo == 'string':
            if cont_StringLocales < limite_stringsLocales:
                posMem = cont_StringLocales
                cont_StringLocales += 1
            else:
                errorOutOfBounds('Locales', 'Strings')

        elif tipo == 'char':
            if cont_CharLocales < limite_charLocales:
                posMem = cont_CharLocales
                cont_CharLocales += 1
            else:
                errorOutOfBounds('Locales', 'Chars')

        elif tipo == 'dataframe':
            if cont_dfLocales < limite_dfLocales:
                posMem = cont_dfLocales
                cont_dfLocales += 1
            else:
                errorOutOfBounds('Locales', 'Dataframes')
    return posMem



'''
Modificador de memoria
'''
def update_pointer(contexto, tipo, cont):
    global cont_IntGlobales
    global cont_IntLocales
    global cont_FloatGlobales
    global cont_FloatLocales
    global cont_StringGlobales
    global cont_StringLocales
    global cont_CharGlobales
    global cont_CharLocales
    global cont_dfGlobales
    global cont_dfLocales

    if contexto == GBL:

        if tipo == 'int':
            cont_IntGlobales += cont
            if cont_IntGlobales > limite_intGlobales:
                print('Error: Overflow Enteras Globales')
        
        if tipo == 'float':
            cont_FloatGlobales += cont
            if cont_FloatGlobales > limite_floatGlobales:
                print('Error: Overflow Flotantes Globales')
        
        if tipo == 'string':
            cont_StringGlobales += cont
            if cont_StringGlobales > limite_stringsGlobales:
                print('Error: Overflow Strings Globales')
        
        if tipo == 'char':
            cont_CharGlobales += cont
            if cont_CharGlobales > limite_charGlobales:
                print('Error: Overflow Chars Globales')

        if tipo == 'dataframe':
            cont_dfGlobales += cont
            if cont_dfGlobales > limite_dfGlobales:
                print('Error: Overflow DF Globales')
    else:
        if tipo == 'int':
            cont_IntLocales += cont
            if cont_IntLocales > limite_intLocales:
                print('Error: Overflow Enteras Locales')
        
        if tipo == 'float':
            cont_FloatLocales += cont
            if cont_FloatLocales > limite_floatLocales:
                print('Error: Overflow Flotantes Locales')
        
        if tipo == 'string':
            cont_StringLocales += cont
            if cont_StringLocales > limite_stringsLocales:
                print('Error: Overflow Strings Locales')
        
        if tipo == 'char':
            cont_CharLocales += cont
            if cont_CharLocales > limite_charLocales:
                print('Error: Overflow Chars Locales')

        if tipo == 'dataframe':
            cont_dfLocales += cont
            if cont_dfLocales > limite_dfLocales:
                print('Error: Overflow DF Locales')

        
def popMemoria():
    global pMemorias
    pop = pMemorias.pop()
    print("--------------------> POP Memorias")
    print("Pop Memoria = ", pop)
    return pop

def pushMemoria(memoria):
    global pMemorias
    pMemorias.append(memoria)
    print("------>pushMemoria : ", memoria)
    print("pMemoria : ", pMemorias)

################ PUNTOS NEURALGICOS ###################
'''
Generador del cuadruplo GOTO Main al inicio del programa
'''
def p_pnGOTOprincipal(p):
    '''
    pnGOTOprincipal : 
    '''
    QuadGenerate('GOTO', '', '', '')
    pushSaltos(nextQuad() - 1)

def p_pnPrincipal2(p):
    '''
    pnPrincipal2 :
    '''
    global currentFunc
    global cuadruplos

    currentFunc = GBL
    cuadruplos[popSaltos()] = ('GOTO', '', '', nextQuad())
    
    



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
    global currentVarName
    global currentCantVars

    varName = p[-1]
    currentVarName = varName
    
    PosMem = nextAvailMemory(currentFunc, currentType)
    
    directorioFunciones.func_addVar(currentFunc, varName, currentType, 0, 0, PosMem)
    
    currentCantVars += 1
  

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




################################## Generacion de cuadruplos #############################################

########### Funciones ################


#### FUNCTION DECLARATION####
'''
Agega nueva funcion al Directorio de Funciones
'''
def p_pnFunDec1(p):
    '''
    pnFunDec1 : 
    '''
    global currentFunc
    global currentType
    global currentCantParams
    global currentCantVars
    global returnBool

    currentCantVars = 0
    currentCantParams = 0
    currentFunc = p[-1]
    print("CAMBIO de CONTEXTO currentFunc = ", currentFunc)
    print("\n")
    directorioFunciones.func_add(currentFunc, currentType, currentCantParams, nextQuad())

    if directorioFunciones.directorio_funciones[currentFunc]['tipo'] == 'void':
        returnBool = False
    else:
        returnBool = True
    
    print("Return Bool : ", returnBool)
    print("\n")
    
    

'''
Cuenta la cantidad de parametros que tiene una funcion y agrega dichos parametros como variables locales de la funcion actual
'''
def p_pnFunDec_2_3(p):
    '''
    pnFunDec_2_3 :
    '''
    global currentFunc
    global currentType
    global currentCantParams
    global currentCantVars
    global varName

    varName = p[-1]
    PosMem = nextAvailMemory(currentFunc, currentType)
    directorioFunciones.func_addVar(currentFunc, varName, currentType, 0, 0, PosMem)

    currentCantParams += 1
    currentCantVars += 1


'''
Modifica la cantidad de parametros de una funcion en el directorio de funciones
'''
def p_pnFunDec4(p):
    '''
    pnFunDec4 :  
    '''
    global currentFunc
    global currentCantParams

    directorioFunciones.func_UpdateParametros(currentFunc, currentCantParams)

'''
Elimina el directorio de funciones
'''
def p_pnFunDec7(p):
    '''
    pnFunDec7 :
    '''
    
    global returnBool
    #global returnDone

    global cont_IntLocales  
    global cont_FloatLocales
    global cont_StringLocales
    global cont_CharLocales   
    global cont_dfLocales

    global cont_IntTemporales  
    global cont_FloatTemporales
    global cont_StringTemporales
    global cont_CharTemporales   
    global cont_dfTemporales
    
    #Reinicio de apuntadores de meomria Locales y Temporales

    cont_IntLocales = limite_dfGlobales
    cont_FloatLocales = limite_intLocales
    cont_StringLocales = limite_floatLocales
    cont_CharLocales = limite_stringsLocales
    cont_dfLocales = limite_charLocales

   
    cont_IntTemporales = limite_dfLocales
    cont_FloatTemporales = limite_intTemporales
    cont_StringTemporales = limite_floatTemporales
    cont_CharTemporales = limite_stringsTemporales
    cont_dfTemporales = limite_charTemporales
    cont_BoolTemporales = limite_dfTemporales

    
    QuadGenerate('ENDFUNC', '', '', '')
    returnBool = False

    #directorioFunciones.func_deleteDic()

  




########## Function Call ##############
'''
Verifica que la funcion exista en el directorio de funciones

Cuadruplos 1 y 2 de las hojas de Elda
'''
def p_pnFunCall_1_2(p):
    '''
    pnFunCall_1_2 : 
    '''
    global pFunciones
    global pArgumentos
    funcId = p[-1]

    if funcId in directorioFunciones.directorio_funciones:
        pFunciones.append(funcId)

        QuadGenerate('ERA', funcId, '', '')
        pArgumentos.append(0)
    
    else:
        print("Error: la funcion no existe")
        sys.exit()
        return

'''

Cuadruplo 3 de la hoja de Elda
'''
def p_pnFunCall_3(p):
    '''
    pnFunCall_3 :
    '''
    global pArgumentos
    global pFunciones
    global currentFunc

    argument = popOperandos()
    argumentType = popTipos()
    argumentMem = popMemoria()
    function = pFunciones.pop()
    args = pArgumentos.pop() + 1

    pArgumentos.append(args)
    parametro = 'param' + str(args)

    Func_Parameters = directorioFunciones.directorio_funciones[function]['cantParametros']

    lista = directorioFunciones.listaTipos(function) ######PENDIENTE

    if Func_Parameters >= args:
        if lista[args-1] == argumentType:
            QuadGenerate('PARAMETER', argumentMem, '', parametro)
        else:
            print("Error: Parametros incorrectos")
    else:
        print("Error, muchos argumentos")
        sys.exit()
    
    pFunciones.append(function)

'''
Cuadruplos 5 y 6 de hojas de Elda
'''
def p_pnFunCall_5_6_llamada(p):
    '''
    pnFunCall_5_6_llamada : 
    '''
    global returnBool
    global pFunciones
    global pArgumentos

    args = pArgumentos.pop()
    funcion = pFunciones.pop()
    
    #Verify that the last parameter points to null
    if args == directorioFunciones.directorio_funciones[funcion]['cantParametros']:
        quadStartFunc = directorioFunciones.directorio_funciones[funcion]['cantQuads']

        #Generate action GOSUB, procedure-name, '', initial address
        QuadGenerate('GOSUB', funcion, nextQuad() + 1, quadStartFunc )
        
    else:
        print("Error: Mismatch de Argumentos")
        sys.exit()
        resultE
    
    tipo =  directorioFunciones.directorio_funciones[funcion]['tipo']
    if tipo != 'void':
        quad_resultIndex = nextAvailTemp(tipo)
        QuadGenerate('=', funcion,'', quad_resultIndex)
        pushOperando(quad_resultIndex)
        pushMemoria(quad_resultIndex)
        pushTipo(tipo)

###### FUNCIONES ESPECIALES #######
def p_pnFunEsp1(p):
    '''
    pnFunEsp1 :
    '''
    nombreFun = str(p[-1])
    pushOperador(nombreFun)

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
    print("p-1 : ", p[-1])
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
    global isArray
    global currentVarName


    idName = p[-1]
    idType = directorioFunciones.func_searchVarType(currentFunc, idName)
    if not idType: #Si no la encuentra en el contexto actual, cambia de contexto a Tipos
        idType = directorioFunciones.func_searchVarType(GBL, idName)
        print("Ahora busca la variable en el contexto Global ")
    
    if not idType:
        print("Error: Variable ", idName, " no declarada")
        return
    
    varPosMem = directorioFunciones.func_memoria(currentFunc, idName)
    if not varPosMem:
        varPosMem = directorioFunciones.func_memoria(GBL, idName)
    
    if varPosMem < 0:
        print("Error: Variable ", idName, " no declarada")
        return
    

    if forBool:
        varFor = idName

    isDim = directorioFunciones.func_isVarDimensionada(currentFunc, idName)

    print("Exp1, DIMENSIONADA: ", isDim)

    if isDim == -1: #sigfinica que no esta en este contexto
        isDim = directorioFunciones.func_isVarDimensionada(GBL, idName)
    
    if isDim == 1:
        isArray = True
        currentVarName = idName
    elif isDim == 0:
        isArray = False
    else:
        isArray = False
        sys.exit("Error. No se ha declarado la variable : ", idName)
        return

    pushOperando(idName)
    pushMemoria(varPosMem)
    pushTipo(idType)
    
    
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

'''Checa si el top del POper es un + o - para generar el cuadruplo de esa operacion'''
def p_pnExp4(p):
    '''
    pnExp4 : 
    '''
    if topOperador() in OP_SUMARESTA:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_leftOperand = popOperandos()
        quad_leftMem = popMemoria()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            errorTypeMismatch()
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            QuadGenerate(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
            pushTipo(quad_resultType)


'''Checa si el top de la pila de operadores es un * o / para generar el cuadruplo  '''
def p_pnExp5(p):
    '''
    pnExp5 : 
    '''
    if topOperador() in OP_MULTDIV:
        
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_leftOperand = popOperandos()
        quad_leftMem = popMemoria()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            QuadGenerate(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
            pushTipo(quad_resultType)

'''Agrega fondo falso '''
def p_pnExp6(p):
    '''
    pnExp6 : 
    '''
    global pOper
    pushOperador('(')
    print("pushOperador: '('")
    

'''Quita fondo falso '''
def p_pnExp7(p):
    '''
    pnExp7 : 
    '''
    tipo = popOperadores()
    print("Quita fondo Falso ')'")

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

'''Verifica si el top de la pila de operadores es un operador relacional para generar el cuadruplo de operacion'''
def p_pnExp9(p):
    '''
    pnExp9 : 
    '''
    if topOperador() in OP_REL:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_leftOperand = popOperandos()
        quad_leftMem = popMemoria()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            QuadGenerate(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
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
        

'''Checa si el top de la pila de operadores es un operador logico  '''
def p_pnExp11(p):
    '''
    pnExp11 : 
    '''
    if topOperador() in OP_LOGICOS:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_leftOperand = popOperandos()
        quad_leftMem = popMemoria()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            QuadGenerate(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
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
        

'''Checa si en el top de la pila de operadores hay una asignacion (=) '''
def p_pnSec2(p):
    '''
    pnSec2 : 
    '''
    if topOperador() in OP_ASIG:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_leftOperand = popOperandos()
        quad_leftMem = popMemoria()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global cuboSem
        global directorioFunciones

        quad_resultType = cuboSem.getType(quad_leftType, quad_rightType, quad_operator)

        if directorioFunciones.var_exist(currentFunc, quad_leftOperand) or directorioFunciones.var_exist(GBL, quad_leftOperand):
            if quad_resultType == 'error':
                print("Error: Operacion invalida")
            else:
                QuadGenerate(quad_operator, quad_rightMem, '', quad_leftMem)
        else:
            print("Error al intentar asignar una variable")



'''
Meter escribir o leer o regresa a la pila
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
        

'''Checa si el top de la pila de operadores es lectura o escritura o retorno'''
def p_pnSec4(p):
    '''
    pnSec4 : 
    '''

    global cuboSem
    if topOperador() in OP_SECUENCIALES:
        print("Voy a ejecutar pnSEc4")
        quad_Operando = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_operator = popOperadores()

        quad_resultType = cuboSem.getType(quad_operator, quad_rightType, '')

        if quad_resultType == 'error':
            print("Error: Operacion invalida")
        else:
            print("HEEEY AQUII")
            QuadGenerate(quad_operator, quad_rightMem, '', quad_operator)
            pushOperador(quad_operator)
            #pushOperando(quad_Operando) #Posible BORRAR
            #pushMemoria(quad_Operando) #Posible BORRAR
            #pushTipo(quad_resultType) #Possible BORRAR

def p_pnSec5(p):
    '''
    pnSec5 : 
    ''' 
    popOperadores()


# GENERACION DE CODIGO PARA ESTATUTOS NO LINEALES (CONDICIONALES)
'''
Genera el cuadruplo GOTOF en la condicion SI (if) depues de recibir el booleano generado por la expresion
'''
def p_pnCond1(p): #IF
    '''
    pnCond1 :
    '''
    global cuadruplos
    memPos = popMemoria()
    exp_type = popTipos()
    
    if(exp_type != 'error'):
        result = popOperandos()
        QuadGenerate('GOTOF', result,'', '')
        pushSaltos(nextQuad() - 1)

    else:
        errorTypeMismatch()

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
    QuadGenerate('GOTO', '', '', '')
    falso = popSaltos()
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
    memPos = popMemoria()
    if exp_type != 'error':
        result = popOperandos()
        QuadGenerate('GOTOF', result, '', '')
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
    QuadGenerate('GOTO', '', '', retorno) #Genetare quad: GOTO

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
            if quad_resultType == 'error':
                print("Error: Operacion invalida")
            else:
                QuadGenerate(quad_operator, quad_rightOperand, '', quad_leftOperand)
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
            QuadGenerate(quad_operator, quad_leftOperand, quad_rightOperand, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)
            
        exp_type = popTipos()
        if (exp_type != 'bool' or exp_type == 'error'):
            errorTypeMismatch()
        else:
            result = popOperandos()
            QuadGenerate('GOTOF', result, '', '')
            pushSaltos(nextQuad() - 1)

'''

'''
def p_pnCiclos8(p):
    '''
    pnCiclos8 :
    '''
    end = popSaltos()
    retorno = popSaltos()
    QuadGenerate('GOTO', '', '', retorno) #Genetare quad: GOTO

    QuadTemporal = (cuadruplos[end][0], cuadruplos[end][1], cuadruplos[end][2], nextQuad())
    cuadruplos[end] = QuadTemporal #FILL (end, cont) 

#################### ESTATUTOS ###############
'''Punto neuralgico en returno'''
def p_pnRetorno(p):
    '''
    pnRetorno :
    '''
    global currentFunc
    global returnBool
    print("return Bool: ", returnBool)
    if returnBool:
        print(pOperandos)
        print(pTipos)
        operador = popOperadores()
        operandoRetorno = popOperandos()
        tipoRetorno = popTipos()
        memRetorno = popMemoria()

        if directorioFunciones.directorio_funciones[currentFunc]['tipo'] == tipoRetorno:
            QuadGenerate(operador, '', '', memRetorno)
        else:
            errorReturnTipo()
    else:
        print ("Error: Esta funcion no debe regresar nada")
    
######## ARREGLOS ###############


'''
Punto neuralgico 2 y 3
Set id as an Array (isArray = true)
'''
def p_pnDimDec2_3(p):
    '''
    pnDimDec2_3 : 
    '''
    global isArray
    isArray = True

    # t = popTipos()
    # t = popOperandos()
    # t = popMemoria()



'''
Punto neuralgico 5 de Elda
Guardar limite de Columnas
'''
def p_pnDimDec5(p):
    '''
    pnDimDec5 : 
    '''
    global R
    global numColumnas
    global directorioFunciones
    global currentFunc
    global currentVarName

    columnas = p[-1]
    if columnas > 0:
        R = R * columnas # R = (LimSup - LimInf + 1) * R
        print("PN5Arreglos.  R = ", R)
        numColumnas = columnas

        directorioFunciones.func_updateDim(currentFunc, currentVarName, 0, columnas)
    else:
        sys.exit("Error: Index de arreglo invalido: ", columnas)

'''
Guarda la cantidad de renglones (Significa que es matriz)
'''
def p_pnDimDec6(p):
    '''
    pnDimDec6 :
    '''
    # global isMatrix
    global R
    global numRenglones
    global directorioFunciones
    global currentFunc
    global currentVarName

    isMatrix = True
    renglones = p[-1]
    if renglones > 0:
        R = R * renglones 
        print("PN6Matriz.  R = ", R)
        numRenglones = renglones

        directorioFunciones.func_updateDim(currentFunc, currentVarName, renglones, -1)
    else: 
        sys.exit("Error. Index menor o igual a cero no es valido")
        return

'''
Actualiza el pointer de memoria tomando los espacios necesarios para el arreglo
'''
def p_pnDimDec8(p):
    '''
    pnDimDec8 : 
    '''
    global R
    global directorioFunciones
    global currentFunc
    global currentVarName
    global isArray
    # global isMatrix
    global currentConstArrays
    NumEspacios = R - 1
    
    currentType = directorioFunciones.func_searchVarType(currentFunc, currentVarName)

    update_pointer(currentFunc, currentType, NumEspacios) #Separa los espacios que va a usar para el arreglo o matriz
    
    
    #Reseteo
    R = 1
    isArray = False
    currentConstArrays = []

'''
Punto neuralgico 2 de Elda para acceder a Arreglos

'''
def p_pnDimAccess2(p):
    '''
    pnDimAccess2 : 
    '''
    global isArray
    global pDim
    isArray = True
    
    varid = popOperandos()
    varmem = popMemoria()
    vartipo = popTipos()
    pDim.append(varid)

'''
Acceder al indice del arreglo
'''
def p_pnArregloAcc(p):
    '''
    pnArregloAcc : 
    '''
    global isArray
    global currentFunc
    global currentVarName

    auxID = popOperandos()
    auxMem = popMemoria()
    auxTipo = popTipos()

    auxDIM = pDim.pop()
    if isArray:
        if auxTipo != 'int':
            sys.exit("Error. Es necesario que el tipo sea un entero para acceder al arreglo")
            return
        
        varDimensiones = directorioFunciones.func_getDims(currentFunc, auxDIM)

        if varDimensiones == -1:
            varDimensiones = directorioFunciones.func_getDims(GBL, auxDIM)

            if varDimensiones == -1:
                sys.exit("Error. No existe variable dimensionada")
                return
            
        #Cuadruplo verifica
        QuadGenerate('VER', auxMem, 0, varDimensiones[0]) #DUDA tamaño -1
        
        

        #Si es Matriz...
        if varDimensiones[1] == 0:
            #Memoria Base
            PosicionMemoria = directorioFunciones.func_memoria(currentFunc, auxDIM)
            if not PosicionMemoria:
                PosicionMemoria = directorioFunciones.func_memoria(GBL, auxDIM)
                
            if PosicionMemoria < 0:
                sys.exit("Error. Variable no declarada: ", auxDIM)
                return
                

            TipoActual = directorioFunciones.func_searchVarType(currentFunc, auxDIM)
            if not TipoActual:
                TipoActual = directorioFunciones.func_searchVarType(GBL, auxDIM)
                
            if not TipoActual:
                sys.exit("Error. Variable no declarada: ", auxDIM)
                return
                

            tMem = nextAvailTemp('int')
            QuadGenerate('+', PosicionMemoria, auxMem, tMem)

            valorTMem = '(' + str(tMem) + ')'
                
            pushOperando(auxDIM)
            pushMemoria(valorTMem)
            pushTipo(TipoActual)
            isArray = False
            currentVarName = ''
        else: #Si es matriz, hay que generar el cuadruplo de *
            print("\n")
            print("Si es matriz...")
            print("\n")
            print("\n")
            print("\n")
            print("\n")
            print("pOperandos: ", pOperandos)
            
            tMem = nextAvailTemp('int')
            QuadGenerate('*', auxMem, getAddConst(varDimensiones[0]), tMem)
            pushOperando(tMem)
            pushMemoria(tMem)
            pushTipo('int')
            pDim.append(auxDIM)

            
            


    else: 
        sys.exit("Error. No se puede acceder al index porque la variable no es dimensionada")
        return

'''
Acceder indice de matrixz
'''
def p_pnMatrizAcc(p):
    '''
    pnMatrizAcc : 
    '''

    print("MATRIZZZZZZZZZZZ")
    global isArray
    global currentVarName
    global currentFunc
    global pDim
    print("pOperandos: ", pOperandos)

    auxID = popOperandos()
    auxMem = popMemoria()
    auxTipo = popTipos() 

    auxDIM = pDim.pop()

    if isArray:
        if auxTipo != 'int':
            sys.exit("Error. Es necesario que el tipo sea un entero para acceder al arreglo")
            return
        
        #Checa las dimensiones
        varDimensiones = directorioFunciones.func_getDims(currentFunc, auxDIM)
        print("MAT: ", auxDIM)
        if varDimensiones == -1:
            varDimensiones = directorioFunciones.func_getDims(GBL, auxDIM) #Busca en global
            if varDimensiones == -1: # si no hay en global...
                sys.exit("Error. La variable no es matriz...")
                return
        
        #Si obtiene las dimensiones correctamente.....
        #Genera los cuadruplos
        QuadGenerate('VER', auxMem, 0, varDimensiones[1]-1)
       

        #Memoria Base
        PosicionMemoria = directorioFunciones.func_memoria(currentFunc, auxDIM)
        if not PosicionMemoria:
            PosicionMemoria = directorioFunciones.func_memoria(GBL, auxDIM)
        if PosicionMemoria < 0:
            sys.exit("Error. La variable no ha sido declarada: ", auxDIM)
            return
        
        #AHORA checamos los tipos
        TipoActual = directorioFunciones.func_searchVarType(currentFunc, auxDIM)
        if not TipoActual:
            TipoActual = directorioFunciones.func_searchVarType(GBL, auxDIM)
        
        if not TipoActual: #Si no está en globales
            sys.exit("Error. La variable no ha sido declarada: ", auxDIM)
            return
        
        auxID2 = popOperandos()
        auxMem2 = popMemoria()
        auxTipo2 = popTipos()

        tMem2 = nextAvailTemp('int')
        QuadGenerate('+', auxMem2, auxMem, tMem2)
        pushOperando(tMem2)
        pushMemoria(tMem2)
        pushTipo('int')

        tMem3 = nextAvailTemp('int')
        base = str(PosicionMemoria) # ESta es la base
        QuadGenerate('+', base, tMem2, tMem3)

        valorTMem = '(' + str(tMem3) + ')'

        pushOperando(auxDIM)
        pushMemoria(valorTMem)
        pushTipo(TipoActual)

        isArray = False
        currentVarName = ''

    else:
        sys.exit("Error. La variable no es dimensionada y no se puede acceder al indice")
        return





def p_pnActivaArray(p):
    '''
    pnActivaArray :    
    '''
    global isArray
    isArray = True


parser = yacc.yacc()

# Put all test inside prueba folder
def main():
    #name = input('File name: ')
    name = "pruebas/" + "test5" + ".txt" #Para probar, cambia el nombre del archivo
    print(name)
    try:
        f = open(name,'r', encoding='utf-8')
        QuadTemporal = ('0', '0', '0', '0')
        pushQuad(QuadTemporal)
        result = parser.parse(f.read())
        print(result)
        f.close()
    except EOFError:
        print (EOFError)

main()

