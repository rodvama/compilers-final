# Jose Arturo Villalobos A00818214
# Rodrigo Valencia A00818256
# Diseno de compiladores
# Maquina Virtual

# TODO: ARREGLOS VERIFICAR - declarados en parse
# TODO: Correlacion - Cambiarlo como todos los demas funciones especiales, sacar el arreglo de memoria 
# y guardarlo en un arreglo local, hacer calculos y guardar respuesta en la direccio que se pida
# Por esto, pedirle que las funciones especiales se guarden en un temporal si no es que ya lo hace
# TODO: CARGAR ARCHIVOS - Convertir archivo en un arreglo y guardarlo en la memoria, con su direccion de dataframe
# TODO: dataframe # Ver que tipo de valor regresa cada funcion



import sys
from memVirtual import *
import numpy as np
import statistics as stats
import matplotlib.pyplot as plt

GBL = 'globales'
LCL = 'locales'
CONST_TEMPORAL = 'temporal'
CONST_EJECUCION = 'ejecucion'
CONST_RETORNO_VALOR = 'retorno'
CONST_FUNCION_RETORNO = 'funcion'
ESPACIO_MEMORIA = 1000

mem_GLOBAL = memVirtual('global')
mem_PRINCIPAL = memVirtual('principal')

constLista = []
cuaLista = []
cuaIndice = 0
cuadruplo = ()
pilaRetorno = []
pilaFuncion = []
sigCuaIndice = -1

pilaTemporal = []
pilaEjecucion = []
pilaCorriendo = ''

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

def push(pilaNom, mem):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        pilaTemporal.append(mem)
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        pilaEjecucion.append(mem)
    elif pilaNom == CONST_RETORNO_VALOR:
        global pilaRetorno
        pilaRetorno.append(mem)
    elif pilaNom == CONST_FUNCION_RETORNO:
        global pilaFuncion
        pilaFuncion.append(mem)

def pop(pilaNom):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        return pilaTemporal.pop()
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        return pilaEjecucion.pop()
    elif pilaNom == CONST_RETORNO_VALOR:
        global pilaRetorno
        return pilaRetorno.pop()
    elif pilaNom == CONST_FUNCION_RETORNO:
        global pilaFuncion
        return pilaFuncion.pop()

def top(pilaNom):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        aux = len(pilaTemporal) - 1
        if (aux < 0):
            return 'vacia'
        return pilaTemporal[aux]
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        aux = len(pilaEjecucion) - 1
        if (aux < 0):
            return 'vacia'
        return pilaEjecucion[aux]

push(CONST_EJECUCION, mem_PRINCIPAL)

def getValor(memVirtual, memDireccion, memTipo):
    global mem_GLOBAL
    # XXX: BORRAR
    # print ("Valor: ", memVirtual, memDireccion, memTipo)
    # memVirtual.imprimirDir()
    # mem_GLOBAL.imprimirDir()
    try:
        if memDireccion[-1] == '!':
            memDireccion = getValor(memVirtual, memDireccion[0:-1], getTipo(memDireccion[0:-1]))
            memTipo = getTipo(memDireccion)
    except:
        pass
    seccion = getSeccion(memDireccion)
    try:
        if seccion == GBL:
            valor = mem_GLOBAL.obtenerValorDeDireccion(memDireccion, memTipo)
        elif seccion == LCL:
            valor = memVirtual.obtenerValorDeDireccion(memDireccion, memTipo)
        else:
            print("Error Maquina Virtual: No se encontró sección {} de memoria".format(seccion))
            sys.exit()
    except:
        print("Error Maquina Virtual: ", sys.exc_info()[0], " en seccion {}, en direccion {}, en indice {}.".format(seccion, memDireccion, cuaIndice))
        sys.exit()
    return valor

def llenarValor(memVirtual, memDireccion, memTipo, valor):
    global mem_GLOBAL
    # XXX: BORRAR
    # print("LLENAR VALOR ANTES", memDireccion)
    # memVirtual.imprimirDir()
    try:
        if memDireccion[-1] == '!':
            # print("LLENAR VALOR ANTES", memDireccion)
            memDireccion = getValor(memVirtual, memDireccion[0:-1], getTipo(memDireccion[0:-1]))
            # print("LLENAR VALOR DESPUES", memDireccion)
            memTipo = getTipo(memDireccion)
            # print("error aqui")
    except:
        pass
    seccion = getSeccion(memDireccion)

    if seccion == GBL:
        mem_GLOBAL.guardarValor(memDireccion, memTipo, valor)
    elif seccion == LCL:
        memVirtual.guardarValor(memDireccion, memTipo, valor)
    else:
        print("Error Maquina Virtual: No se encontró sección de memoria")
        sys.exit()
        return

def getSeccion(mem):
    global pilaCorriendo
    try:
        if mem[-1] == '!':
            mem = getValor(pilaCorriendo, mem[0:-1], getTipo(mem[0:-1]))
    except:
        pass
    mem = int(mem)
    # GLOBALES y CONSTANTES se guardan donde mismo
    if ((mem >= 0 and mem < limite_dfGlobales) or (mem >= limite_boolTemporales and mem <= limite_dfConstantes)):
        return GBL
    # LOCALES y TEMPORALES se guardan donde mismo
    if ((mem >= limite_dfGlobales and mem < limite_dfLocales) or (mem >= limite_dfLocales and mem < limite_boolTemporales)):
        return LCL
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro de ninguna seccion".format(mem))
        sys.exit()
        return

def getTipo(mem):
    global pilaCorriendo
    # XXX: BORRAR
    # print ("TIPO: ", mem[0])
    try: 
        if mem[-1] == '!':
            mem = getValor(pilaCorriendo, mem[0:-1], getTipo(mem[0:-1]))
            # XXX: BORRAR
            # print("tipo entre: ", mem)
    except:
        pass
    mem = int(mem)
    if ((mem >= 0 and mem < limite_intGlobales) or (mem >= limite_dfGlobales and mem < limite_intLocales) or (mem >= limite_dfLocales and mem < limite_intTemporales) or (mem >= limite_boolTemporales and mem < limite_intConstantes)):
        return 'int'
    if ((mem >= limite_intGlobales and mem < limite_floatGlobales) or (mem >= limite_intLocales and mem < limite_floatLocales) or (mem >= limite_intTemporales and mem < limite_floatTemporales) or (mem >= limite_intConstantes and mem < limite_floatConstantes)):
        return 'float'
    if ((mem >= limite_floatGlobales and mem < limite_stringsGlobales) or (mem >= limite_floatLocales and  mem < limite_stringsLocales) or (mem >= limite_floatTemporales and mem < limite_stringsTemporales) or (mem >= limite_floatConstantes and mem < limite_stringsConstantes)):
        return 'string'
    if ((mem >= limite_stringsGlobales and mem < limite_charGlobales) or (mem >= limite_stringsLocales and mem <limite_charLocales) or (mem >= limite_stringsTemporales and mem < limite_charTemporales) or (mem >= limite_stringsConstantes and mem < limite_charConstantes)):
        return 'char'
    if ((mem >= limite_charGlobales and mem < limite_dfGlobales) or (mem >= limite_charLocales and mem < limite_dfLocales) or (mem >= limite_charTemporales and mem < limite_dfTemporales) or (mem >= limite_charConstantes and mem < limite_dfConstantes)):
        return 'string'
    if (mem >= limite_dfTemporales and mem < limite_boolTemporales):
        return 'bool'
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro del rango de ningun tipo de variable".format(mem))
        sys.exit()
        return
    

def operadores(signo):
    global cuadruplo
    global pilaCorriendo
    if signo != 'CONS':
        if signo == '+':
            if cuadruplo[1][0] == '{' and cuadruplo[1][-1] == '}': 
                valor1 = int(cuadruplo[1][1:-1])
                valor2 = getValor(pilaCorriendo, cuadruplo[2], getTipo(cuadruplo[2]))
                valor2 = int(valor2)
            else:
                # XXX:BORRAR
                # pilaCorriendo.imprimirDir()
                tipo1 = getTipo(cuadruplo[1])
                # XXX:BORRAR
                # print("tipo1: ", tipo1)
                tipo2 = getTipo(cuadruplo[2])
                # XXX:BORRAR
                # print("tipo2: ", tipo2)
                valor1 = getValor(pilaCorriendo, cuadruplo[1], tipo1)
                # XXX:BORRAR
                # print("valor1: ", valor1)
                valor2 = getValor(pilaCorriendo, cuadruplo[2], tipo2)
                # XXX:BORRAR
                # print("valor2: ", valor2)

                if tipo1 == 'int':
                    valor1 = int(valor1)
                elif tipo1 == 'float':
                    valor1 = float(valor1);

                if tipo2 == 'int':
                    valor2 = int (valor2)
                elif tipo2 == 'float':
                    valor2 = float(valor2) 
                pass
            res = valor1 + valor2
        else:   
            tipo1 = getTipo(cuadruplo[1])
            tipo2 = getTipo(cuadruplo[2])
            valor1 = getValor(pilaCorriendo, cuadruplo[1], tipo1)
            valor2 = getValor(pilaCorriendo, cuadruplo[2], tipo2)

            if tipo1 == 'int':
                valor1 = int(valor1)
            elif tipo1 == 'float':
                valor1 = float(valor1)

            if tipo2 == 'int':
                valor2 = int(valor2)
            elif tipo2 == 'float':
                valor2 = float(valor2) 

            if signo == '-':
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
        # XXX:BORRAR
        # print(cuadruplo[3], getTipo(cuadruplo[3]), res)
        llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), res)

def correr():
    global constLista
    global cuaLista
    global cuaIndice
    global cuadruplo
    global mem_GLOBAL
    global pilaRetorno
    global sigCuaIndice
    global pilaCorriendo

    for cons in constLista:
        llenarValor(mem_GLOBAL, cons[3], cons[1], cons[2])
    
    #XXX: BORRAR\
    # mem_GLOBAL.imprimirDir()

    terminado = False
    while not terminado:
        sigCuaIndice = -1
        pilaCorriendo = top(CONST_EJECUCION)
        # XXX: BORRAR
        # print("Indice: ", cuaIndice)
        # print("Lista size: ",len(cuaLista))
        cuadruplo = cuaLista[cuaIndice]

        # XXX: BORRAR
        # print(cuadruplo)
        # mem_GLOBAL.imprimirDir()
        # pilaCorriendo.imprimirDir()

        # ASIGNACION
        if cuadruplo[0] == '=':
            # XXX:BORRAR
            # pilaCorriendo.imprimirDir()
            # print(cuadruplo[3])
            try:
                # XXX: BORRAR
                # print (cuadruplo[1])
                # print(cuadruplo[1])
                valor = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            except:
                valor = pop(CONST_RETORNO_VALOR)
                # XXX: BORRAR
                # print("= : ",valor)
                
            llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), valor)
        # COMANDOS        
        # CONS
        # Se saltará porque ya se agregarón con antelación
        # GOTO
        elif cuadruplo[0] == 'GOTO':
            sigCuaIndice = int(cuadruplo[3])
        # GOTOF
        elif cuadruplo[0] == 'GOTOF':
            auxValor = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
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
            # XXX: BORRAR
            # print(top(CONST_TEMPORAL))
        # PARAMETER
        elif cuadruplo[0] == 'PARAMETER':
            tipo = getTipo(cuadruplo[1])
            valor = getValor(pilaCorriendo, cuadruplo[1], tipo)
            auxMem = top(CONST_TEMPORAL)
            direccion = auxMem.sigDireccionDisponible(tipo, limite_dfGlobales, ESPACIO_MEMORIA)
            # XXX: BORRAR
            # print("Tipo: ", tipo, " Valor: ", valor, " auxMem: ", auxMem, " direccion: ", direccion)
            llenarValor(auxMem, direccion, getTipo(direccion), valor)
        # ENDFUNC
        elif cuadruplo[0] == 'ENDFUNC':
            pop(CONST_EJECUCION)
            sigCuaIndice = int(pop(CONST_FUNCION_RETORNO))
        # regresa
        elif cuadruplo[0] == 'regresa':
            # TODO: VERIFICAR
            try:
                valor = getValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]))
                push(CONST_RETORNO_VALOR, str(valor))
            except:
                push(CONST_RETORNO_VALOR, str(cuadruplo[3]))
                pass
            pop(CONST_EJECUCION) #Sacar funcion de la pila, porque se termino de ejecutar
            sigCuaIndice = int(pop(CONST_FUNCION_RETORNO));
        # lee
        elif cuadruplo[0] == 'lee':
            texto = input("<- ")
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
                        print("Error Maquina Virtual: {}".format(sys.exc_info()[0], cuaIndice))
            auxTipo = getTipo(cuadruplo[1])
            if tipo == auxTipo:
                llenarValor(pilaCorriendo, cuadruplo[1], auxTipo, texto)
            else:
                print("Error Maquina Virtual: {} es diferente a {}".format(tipo, auxTipo))
                sys.exit()
                return
        # escribe
        elif cuadruplo[0] == 'escribe':
            texto = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            print("->",str(texto))
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
                print("Error Maquina Virtual: El arreglo no tiene una moda definida, se regresa el ultimo valor.")
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
        # correlation
        elif cuadruplo[0] == 'correlation':
            #HACK: TERMINAR
            pass
        # plothist
        elif cuadruplo[0] == 'histograma':
            #HACK: TERMINAR

            pass
        # plotline
        elif cuadruplo[0] == 'plotline':
            #HACK: TERMINAR
            pass
        #ARREGLO
        #VER
        elif cuadruplo[0] == 'VER':
            # XXX:BORRAR
            # print("Entre aqui primero")
            valor = int(getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1])))
            if valor != 0: #HACK: Se aceptan indices negativos?
                valor = valor - 1 # Para que se vuelva índice y se prueba.
            if valor > int(cuadruplo[3]) or valor < int(cuadruplo[2]):
                print("Error Maquina Virtual: El valor {} no pertence a los indices.".format(valor+1))
                sys.exit()
                return
            # XXX: BORRAR
            # pilaCorriendo.imprimirDir()
        #FINPROGRAMA
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

cuadruplos = getArchivo()
for linea in cuadruplos:
    linea = linea.replace('(','')
    linea = linea.replace(')','')
    linea = linea.replace('\n','')
    linea = linea.replace('\'','')
    linea = linea.replace(' ','')
    cuadruplo = tuple(linea.split(','))
    if (cuadruplo[0] == 'CONS'):
        cuadroCONST = (cuadruplo[0], cuadruplo[1], cuadruplo[2], cuadruplo[3])
        constLista.append(cuadroCONST)
    cuadruplo = (cuadruplo[0], cuadruplo[1], cuadruplo[2], cuadruplo[3])
    cuaLista.append(cuadruplo)

correr()
