# Jose Arturo Villalobos A00818214
# Rodrigo Valencia A00818256
# Diseno de compiladores
# Maquina Virtual

import sys
from memVirtual import *


CONST_LOCALES = 'locales'
CONST_GLOBALES = 'globales'
CONST_TEMPORAL = 'temporal'
CONST_EJECUCION = 'ejecucion'
CONST_RETORNO_VALOR = 'retorno'
CONST_FUNCION_RETORNO = 'funcion'
ESPACIO_MEMORIA = 100

mem_GLOBAL = memVirtual('global')
mem_MAIN = memVirtual('main')

# obejota 
cuaLista = []
cuaIndice = 0
cuadruplo = ()
pilaRetorno = []
pilaFuncion = []
sigCuaIndice = -1

pilaTemporal = []
pilaEjecucion = []
pilaCorriendo = ''

def push(pilaNom, mem):
    if pilaNom == "temporal":
        global pilaTemporal
        pilaTemporal.append(mem)
    elif pilaNom == "ejecucion":
        global pilaEjecucion
        pilaEjecucion.append(mem)
    elif pilaNom == "retorno":
        global pilaRetorno
        pilaRetorno.append(mem)
    elif pilaNom == "funcion":
        global pilaFuncion
        pilaFuncion.append(mem)

def pop(pilaNom):
    if pilaNom == "temporal":
        global pilaTemporal
        pilaTemporal.pop()
    elif pilaNom == "ejecucion":
        global pilaEjecucion
        pilaEjecucion.pop()
    elif pilaNom == "retorno":
        global pilaRetorno
        pilaRetorno.pop()
    elif pilaNom == "funcion":
        global pilaFuncion
        pilaFuncion.pop()

def top(pilaNom):
    if pilaNom == "temporal":
        global pilaTemporal
        aux = len(pilaTemporal) - 1
        if (aux < 0):
            return 'vacia'
        return pilaTemporal[aux]
    elif pilaNom == "ejecucion":
        global pilaEjecucion
        aux = len(pilaEjecucion) - 1
        if (aux < 0):
            return 'vacia'
        return pilaEjecucion
    elif pilaNom == "retorno":
        global pilaRetorno
        aux = len(pilaRetorno) - 1
        if (aux < 0):
            return 'vacia'
        return pilaRetorno
    elif pilaNom == "funcion":
        global pilaFuncion
        aux = len(pilaFuncion) - 1
        if (aux < 0):
            return 'vacia'
        return pilaFuncion

push(CONST_EJECUCION, mem_MAIN)


'''
Espacios de memoria:
+++++++++++++++++++++++
+globales enteras     + batch_size
+---------------------+
+globales flotantes   + batch_size
+---------------------+
+globales strings     + batch_size
+---------------------+
+globales char        + batch_size
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
+constantes dataframe + batch_size
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
limite_stringsConstantes = limite_floatConstantes + ESPACIO_MEMORIA
limite_charConstantes = limite_stringsConstantes + ESPACIO_MEMORIA
limite_dfConstantes = limite_charConstantes + ESPACIO_MEMORIA


def getValor(memVirtual, memDireccion, memTipo):
    global mem_GLOBAL
    try:
        if memDireccion[0] == '{' and memDireccion[-1] == '}':
            memDireccion = getValor(memVirtual, memDireccion[1:-1], getTipo(memDireccion[1:-1]))
            memTipo = getTipo(memDireccion)
    except:
        pass
    
    valor = -1
    seccion = getSeccion(memDireccion)
    try:
        if seccion == CONST_GLOBALES:
            valor = mem_GLOBAL.obtenerValorDeDireccion(str(memDireccion), str(memTipo))
        elif seccion == CONST_LOCALES:
            valor = memVirtual.obtenerValorDeDireccion(str(memDireccion), str(memTipo))
        else:
            print("Error: No se encontró sección de memoria")
            sys.exit()
    except:
        print("Error: ", sys.exc_info()[0], " en seccion {}, en direccion {}, en indice {}.".format(seccion, memDireccion, cuaIndice))
        sys.exit()
    return valor

def llenarValor(memVirtual, memDireccion, memTipo, valor):
    global mem_GLOBAL
    try:
        if memDireccion[0] == '{' and memDireccion[-1] == '}':
            memDireccion = getValor(memVirtual, memDireccion[1:-1], getTipo(memDireccion[1:-1]))
            memTipo = getTipo(memDireccion)
    except:
        pass
    
    memTipo = str(memTipo)
    seccion = getSeccion(memDireccion)
    if seccion == CONST_GLOBALES:
        mem_GLOBAL.guardarValor(memDireccion, memTipo, valor)
    elif seccion == CONST_LOCALES:
        memVirtual.guardarValor(memVirtual, memTipo, valor)
    else:
        print("Error: No se encontró sección de memoria")
        sys.exit()

def getSeccion(mem):
    global pilaCorriendo
    try:
        if mem[0] == '{':
            mem = getValor(pilaCorriendo, mem[1:-1], getTipo(mem[1:-1]))
    except:
        pass
    mem = int(mem)
    # GLOBALES y CONSTANTES se guardan donde mismo
    if ((mem >= 0 and mem < limite_dfGlobales) or (mem >= limite_boolTemporales and mem <= limite_dfConstantes)):
        return CONST_GLOBALES
    # LOCALES y TEMPORALES se guardan donde mismo
    if ((mem >= limite_dfGlobales and mem < limite_dfLocales) or (mem >= limite_dfLocales and mem < limite_boolTemporales)):
        return CONST_LOCALES

def getTipo(mem):
    global pilaCorriendo
    try: 
        if mem[0] == '{':
            mem = getValor(pilaCorriendo, mem[1:-1], getTipo[1:-1])
    except:
        pass
    mem = int(mem)
    if ((mem >= 0 and mem < limite_intGlobales) or (mem >= limite_dfGlobales and limite_intLocales) or (mem >= limite_dfLocales and mem < limite_intTemporales) or (mem >= limite_boolTemporales and mem < limite_intConstantes)):
        return 'int'
    if ((mem >= limite_intGlobales and mem < limite_floatGlobales) or (mem >= limite_intLocales and limite_floatLocales) or (mem >= limite_intTemporales and mem < limite_floatTemporales) or (mem >= limite_intConstantes and mem < limite_floatConstantes)):
        return 'float'
    if ((mem >= limite_floatGlobales and mem < limite_stringsGlobales) or (mem >= limite_floatLocales and limite_stringsLocales) or (mem >= limite_floatTemporales and mem < limite_stringsTemporales) or (mem >= limite_floatConstantes and mem < limite_stringsConstantes)):
        return 'string'
    if ((mem >= limite_stringsGlobales and mem < limite_charGlobales) or (mem >= limite_stringsLocales and limite_charLocales) or (mem >= limite_stringsTemporales and mem < limite_charTemporales) or (mem >= limite_stringsConstantes and mem < limite_charConstantes)):
        return 'char'
    if ((mem >= limite_charGlobales and mem < limite_dfGlobales) or (mem >= limite_charLocales and limite_dfLocales) or (mem >= limite_charTemporales and mem < limite_dfTemporales) or (mem >= limite_charConstantes and mem < limite_dfConstantes)):
        return 'string'
    if (mem >= limite_dfTemporales and mem < limite_boolTemporales):
        return 'bool'
    

def res(signo):
    tipo1 = getTipo(cuadruplo[1])
    tipo2 = getTipo(cuadruplo[2])
    op1 = getValor(pilaCorriendo, cuadruplo[1], tipo1)
    op2 = getValor(pilaCorriendo, cuadruplo[2], tipo2)

    if tipo1 == 'int':
        op1 = int(op1)
    elif tipo1 == 'float':
        op1 == float(op1);

    if tipo2 == 'int':
        op2 = int (op2)
    elif tipo2 == 'float':
        op2 == float(op2) 
    
    if signo == '+':
        res = op1 + op2
    elif signo == '-':
        res = op1 - op2
    elif signo == '*':
        res = op1 * op2
    elif signo == '/':
        res = op1 / op2
    elif signo == '==':
        res = op1 == op2
    elif signo == '<':
        res = op1 < op2
    elif signo == '>':
        res = op1 > op2
    elif signo == '<=':
        res = op1 <= op2
    elif signo == '>=':
        res = op1 >= op2
    elif signo == '!=':
        res = op1 != op2
    elif signo == '|':
        res = True if op1 == op2 and op1 == False and op2 == False else False
    elif signo == '&':
        res = True if op1 == op2 and op1 == True else False

    llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), res)

    

def run():
    global cuaLista
    global cuaIndice
    global cuadruplo
    global mem_GLOBAL
    global pilaRetorno
    global sigCuaIndice
    global pilaCorriendo

    terminado = True
    while terminado != False:
        sigCuaIndice = -1
        pilaCorriendo = top(CONST_EJECUCION)
        cuadruplo = cuaLista[cuaIndice]
        
        if cuadruplo[0] == '=':
        # =
        # escribe
        # GOTO
        # GOTOF
        # ERA
        # PARAMETER
        # GOSUB
        # ENDFUNC
        # regresa
        # lee
        # Media
        # plothist
        # plotline
        # Mediana
        # moda


 