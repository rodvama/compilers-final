# Jose Arturo Villalobos A00818214
# Rodrigo Valencia A00818256
# Diseno de compiladores
# Maquina Virtual

import sys
from memVirtual import *
import numpy as np
import statistics as stats
import matplotlib.pyplot as plt


CONST_LOCALES = 'locales'
CONST_GLOBALES = 'globales'
CONST_TEMPORAL = 'temporal'
CONST_EJECUCION = 'ejecucion'
CONST_RETORNO_VALOR = 'retorno'
CONST_FUNCION_RETORNO = 'funcion'
ESPACIO_MEMORIA = 100

mem_GLOBAL = memVirtual('global')
mem_MAIN = memVirtual('main')

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
        return pilaTemporal.pop()
    elif pilaNom == "ejecucion":
        global pilaEjecucion
        return pilaEjecucion.pop()
    elif pilaNom == "retorno":
        global pilaRetorno
        return pilaRetorno.pop()
    elif pilaNom == "funcion":
        global pilaFuncion
        return pilaFuncion.pop()

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
        return pilaEjecucion[aux]

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
    # try:
    #     if memDireccion[0] == '{' and memDireccion[-1] == '}':
    #         memDireccion = getValor(memVirtual, memDireccion[1:-1], getTipo(memDireccion[1:-1]))
    #         memTipo = getTipo(memDireccion)
    # except:
    #     pass
    
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
    # try:
    #     if memDireccion[0] == '{' and memDireccion[-1] == '}':
    #         memDireccion = getValor(memVirtual, memDireccion[1:-1], getTipo(memDireccion[1:-1]))
    #         memTipo = getTipo(memDireccion)
    # except:
    #     pass
    
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
    

def operadores(signo):
    tipo1 = getTipo(cuadruplo[1])
    tipo2 = getTipo(cuadruplo[2])
    valor1 = getValor(pilaCorriendo, cuadruplo[1], tipo1)
    valor2 = getValor(pilaCorriendo, cuadruplo[2], tipo2)

    if tipo1 == 'int':
        valor1 = int(valor1)
    elif tipo1 == 'float':
        valor1 == float(valor1);

    if tipo2 == 'int':
        valor2 = int (valor2)
    elif tipo2 == 'float':
        valor2 == float(valor2) 
    
    if signo == '+':
        res = valor1 + valor2
    elif signo == '-':
        res = valor1 - valor2
    elif signo == '*':
        res = valor1 * valor2
    elif signo == '/':
        res = valor1 / valor2
    elif signo == '==':
        res = valor1 == valor2
    elif signo == '<':
        res = valor1 < valor2
    elif signo == '>':
        res = valor1 > valor2
    elif signo == '<=':
        res = valor1 <= valor2
    elif signo == '>=':
        res = valor1 >= valor2
    elif signo == '!=':
        res = valor1 != valor2
    elif signo == '|':
        res = True if valor1 == valor2 and valor1 == False and valor2 == False else False
    elif signo == '&':
        res = True if valor1 == valor2 and valor1 == True else False

    llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), res)

def correr():
    global cuaLista
    global cuaIndice
    global cuadruplo
    global mem_GLOBAL
    global pilaRetorno
    global sigCuaIndice
    global pilaCorriendo

    terminado = False
    while not terminado:
        sigCuaIndice = -1
        pilaCorriendo = top(CONST_EJECUCION)
        cuadruplo = cuaLista[cuaIndice]

        # ASIGNACION
        if cuadruplo[0] == '=':
            try:
                valor = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            except:
                valor = pop(CONST_RETORNO_VALOR)
                print(valor)
            llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), valor)
        # COMANDOS        
        # GOTO
        elif cuadruplo[0] == 'GOTO':
            sigCuaIndice = int(cuadruplo[3])
        # GOTOF
        elif cuadruplo[0] == 'GOTOF':
            tipo = getTipo(cuadruplo[1])
            auxValor = getValor(pilaCorriendo, cuadruplo[1], tipo)
            if not auxValor:
                sigCuaIndice = int(cuadruplo[3])
        # GOSUB
        elif cuadruplo[0] == 'GOSUB':
            pilaCorriendo = pop(CONST_TEMPORAL)
            push(CONST_EJECUCION, pilaCorriendo)
            push(CONST_FUNCION_RETORNO, cuadruplo[2])
            sigCuaIndice = int(cuadruplo[3])
        # ERA
        elif cuadruplo[0] == 'ERA':
            memNueva = memVirtual(str(cuadruplo[1]))
            push(CONST_TEMPORAL, memNueva)
        # PARAMETER
        elif cuadruplo[0] == 'PARAMETER':
            tipo = getTipo(cuadruplo[1])
            valor = getValor(pilaCorriendo, cuadruplo[1], tipo)
            auxMem = top(CONST_TEMPORAL)
            mem = auxMem.sigDireccionDisponible(tipo, limite_dfGlobales, ESPACIO_MEMORIA)
            llenarValor(auxMem, mem, getTipo(mem), valor)
        # ENDFUNC
        elif cuadruplo[0] == 'ENDFUNC':
            pop(CONST_EJECUCION)
            sigCuaIndice = int(pop(CONST_FUNCION_RETORNO))
        # regresa
        elif cuadruplo[0] == 'regresa':
            if cuadruplo[3] != '':
                valor = getValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]))
                push(CONST_RETORNO_VALOR, valor)
            pop(CONST_EJECUCION)
            sigCuaIndice = int(pop(CONST_FUNCION_RETORNO));
        # lee
        elif cuadruplo[0] == 'lee':
        # TODO: Ver lo de los arreglos
            texto = input("> ")
            try:
                int(texto)
                tipo = 'int'
            except:
                try:
                    float(texto)
                    tipo = 'float'
                except:
                    try:
                        str(texto)
                        tipo = 'char' if len(texto) == 1 else 'string'
                    except:
                        print("Error: {}".format(sys.exc_info()[0], cuaIndice))
        # escribe
        elif cuadruplo[0] == 'escribe':
            texto = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            print(str(texto))
        # FUNCIONES ESPECIALES
        # Media
        elif cuadruplo[0] == 'media':
            arreglo = []
            base = int(cuadruplo[1])
            col = int(cuadruplo[2])
            for x in range(col):
                auxValor = getValor(pilaCorriendo, base+x, getTipo(base+x))
                arreglo.append(float(auxValor))
            auxTipo = getTipo(cuadruplo[3])
            llenarValor(pilaCorriendo, cuadruplo[3], auxTipo, np.mean(arreglo))
        # plothist
        elif cuadruplo[0] == 'plothist':
            base = int(cuadruplo[1])
            col = int(cuadruplo[2])
            auxBins = getValor(pilaCorriendo, int(cuadruplo[3]), getTipo(int(cuadruplo[3])))
            auxBins = int(auxBins)
            auxArray = []
            for x in range(col - 1):
                auxArray.append(getValor(pilaCorriendo, base+x, getTipo(base+x)))
            plt.hist(auxArray, bins=auxBins)
            plt.show()
            plt.close()
        # plotline
        elif cuadruplo[0] == 'plotline':
            col = int(cuadruplo[3])
            base1 = int(cuadruplo[1])
            base2 = int(cuadruplo[2])
            arreglo1 = []
            arreglo2 = []
            for x in range(col -1):
                arreglo1.append(getValor(pilaCorriendo, base1+x, getTipo(base1+x)))
                arreglo2.append(getValor(pilaCorriendo, base2+x, getTipo(base2+x)))
            plt.plot(arreglo1, arreglo2)
            plt.show()
            plt.close()
        # Mediana
        elif cuadruplo[0] == 'mediana':
            arreglo = []
            base = int(cuadruplo[1])
            col = int(cuadruplo[2])
            for x in range(col):
                auxValor = getValor(pilaCorriendo, base+x, getTipo(base+x))
                arreglo.append(float(auxValor))
            auxTipo = getTipo(cuadruplo[3])
            llenarValor(pilaCorriendo, cuadruplo[3], auxTipo, np.median(arreglo))
        # moda
        elif cuadruplo[0] == 'moda':
            arreglo = []
            base = int(cuadruplo[1])
            col = int(cuadruplo[2])
            for x in range(col):
                auxValor = getValor(pilaCorriendo, base+x, getTipo(base+x))
                arreglo.append(float(auxValor))
            auxTipo = getTipo(cuadruplo[3])
            try:
                res = stats.mode(arreglo)
                llenarValor(pilaCorriendo, cuadruplo[3], auxTipo, res)
            except:
                print("Error: El arreglo no tiene una moda definida, se regresa el ultimo valor.")
                llenarValor(pilaCorriendo, cuadruplo[3], auxTipo, auxValor)
        # varianza
        elif cuadruplo[0] == 'varianza':
            arreglo = []
            base = int(cuadruplo[1])
            col = int(cuadruplo[2])
            for x in range(col):
                auxValor = getValor(pilaEjecucion, base+x, getTipo(base+x))
                arreglo.append(float(auxValor))
            auxTipo = getTipo(cuadruplo[3])
            llenarValor(pilaEjecucion, cuadruplo[3], auxTipo, np.var(arreglo))
        elif cuadruplo[0] == 'FINPROGRAMA':
            terminado = True
        # OPERADORES 
        else:
            operadores(cuadruplo[0])

        if sigCuaIndice != -1:
            cuaIndice = sigCuaIndice
        else: #Solo se ejecuta el siguiente quad
            cuaIndice = cuaIndice + 1

# Put all test inside prueba folder
def getArchivo():
    #name = input('File name: ')
    name =  "obj"+ ".txt" #Para probar, cambia el nombre del archivo
    try:
        f = open(name,'r', encoding='utf-8')
        return f
        f.close()
    except EOFError:
        print (EOFError)

# TODO: lectura de archivos
cuadruplos = getArchivo()
for linea in cuadruplos:
    linea = linea.replace('(','')
    linea = linea.replace(')','')
    linea = linea.replace('\n','')
    linea = linea.replace('\'','')
    linea = linea.replace(' ','')
    cuadruplo = tuple(linea.split(','))
    cuadruplo = (cuadruplo[0], cuadruplo[1], cuadruplo[2], cuadruplo[3])
    cuaLista.append(cuadruplo)
correr()
