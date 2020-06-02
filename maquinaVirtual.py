# Jose Arturo Villalobos A00818214
# Rodrigo Valencia A00818256
# Diseno de compiladores
# Maquina Virtual

import sys
from memVirtual import *
import numpy as np
import statistics as statistics
import matplotlib.pyplot as plt


# TODO: COMENTARIOS
# TODO: FUNCIONES PA GRAFICAR

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
    try:
        if memDireccion[-1] == '!':
            memDireccion = getValor(memVirtual, memDireccion[0:-1], getTipo(memDireccion[0:-1]))
            memTipo = getTipo(memDireccion)
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
    try: 
        if mem[-1] == '!':
            mem = getValor(pilaCorriendo, mem[0:-1], getTipo(mem[0:-1]))
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
        return 'dataframe'
    if (mem >= limite_dfTemporales and mem < limite_boolTemporales):
        return 'bool'
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro del rango de ningun tipo de variable".format(mem))
        sys.exit()
        return
# Funcion operadores, para sacar el signo
def operadores(signo):
    global cuadruplo
    global pilaCorriendo
    if signo == '+':
        if cuadruplo[1][0] == '{' and cuadruplo[1][-1] == '}': 
            valor1 = int(cuadruplo[1][1:-1])
            valor2 = getValor(pilaCorriendo, cuadruplo[2], getTipo(cuadruplo[2]))
            valor2 = int(valor2)
        else:
            tipo1 = getTipo(cuadruplo[1])
            tipo2 = getTipo(cuadruplo[2])
            valor1 = getValor(pilaCorriendo, cuadruplo[1], tipo1)
            valor2 = getValor(pilaCorriendo, cuadruplo[2], tipo2)

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

    llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), res)

# Verifica que los indices esten dentro del dataframe
def verificar(arr, de, a):
    l = len(arr) - 1
    if de < 0 or de > l:
        print("Error Maquina Virtual: el inidice {} no esta dentro del rango del dataframe 0 a {} ".format(de,l))
        sys.exit()
        return False
    if  a < 0 or a > l:
        print("Error Maquina Virtual: el inidice {} no esta dentro del rango del dataframe 0 a {} ".format(a,l))
        sys.exit()
        return False
    return True


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
        # PARAMETER
        elif cuadruplo[0] == 'PARAMETER':
            tipo = getTipo(cuadruplo[1])
            valor = getValor(pilaCorriendo, cuadruplo[1], tipo)
            auxMem = top(CONST_TEMPORAL)
            direccion = auxMem.sigDireccionDisponible(tipo, limite_dfGlobales, ESPACIO_MEMORIA)
            llenarValor(auxMem, direccion, getTipo(direccion), valor)
        # ENDFUNC
        elif cuadruplo[0] == 'ENDFUNC':
            pop(CONST_EJECUCION)
            sigCuaIndice = int(pop(CONST_FUNCION_RETORNO))
        # regresa
        elif cuadruplo[0] == 'regresa':
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
        # Mediana
        elif cuadruplo[0] == 'mediana':
            subArreglo = []
            tipo = getTipo(cuadruplo[3])
            arreglo = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            aux = cuadruplo[2].split('#')
            if (aux[0] != '0' and aux[1] != '0'): #Si vienen 0 significa que es todo el arreglo
                de = int(aux[0][1:]) 
                a = int(aux[1][:])
                # Si es -1, significa que es 0
                if (aux[0] == -1):
                    de = 0
                if (aux[1] == -1):
                    a = 0
                if verificar(arreglo, de, a): # Verificar con cualquier arreglo, ya que deben de ser del mismo tamaño
                    for r in range(de,a+1): subArreglo.append(arreglo[r])
                    try:
                        llenarValor(pilaCorriendo, cuadruplo[3], tipo, statistics.median(subArreglo))
                    except:
                        print("Error Maquina Virtual: El arreglo no tiene mediana, en el rango de {} a {}".format(de, a))
                        sys.exit()
                        return
            else:
                try:
                    llenarValor(pilaCorriendo, cuadruplo[3], tipo, statistics.median(arreglo))
                except:
                    print("Error Maquina Virtual: El arreglo no tiene mediana en todo el archivo")
                    sys.exit()
                    return
        # Media
        elif cuadruplo[0] == 'media':
            subArreglo = []
            tipo = getTipo(cuadruplo[3])
            arreglo = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            aux = cuadruplo[2].split('#')
            if (aux[0] != '0' and aux[1] != '0'): #Si vienen 0 significa que es todo el arreglo
                de = int(aux[0][1:]) 
                a = int(aux[1][:])
                # Si es -1, significa que es 0
                if (aux[0] == -1):
                    de = 0
                if (aux[1] == -1):
                    a = 0
                if verificar(arreglo, de, a): # Verificar con cualquier arreglo, ya que deben de ser del mismo tamaño
                    for r in range(de,a+1): subArreglo.append(arreglo[r])
                    try:
                        llenarValor(pilaCorriendo, cuadruplo[3], tipo, statistics.mean(subArreglo))
                    except:
                        print("Error Maquina Virtual: El arreglo no tiene mediana, en el rango de {} a {}".format(de, a))
                        sys.exit()
                        return
            else:
                try:
                    llenarValor(pilaCorriendo, cuadruplo[3], tipo, statistics.mean(arreglo))
                except:
                    print("Error Maquina Virtual: El arreglo no tiene mediana en todo el archivo")
                    sys.exit()
                    return
        # moda
        elif cuadruplo[0] == 'moda':
            subArreglo = []
            tipo = getTipo(cuadruplo[3])
            arreglo = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            aux = cuadruplo[2].split('#')
            if (aux[0] != '0' and aux[1] != '0'): #Si vienen 0 significa que es todo el arreglo
                de = int(aux[0][1:]) 
                a = int(aux[1][:])
                # Si es -1, significa que es 0
                if (aux[0] == -1):
                    de = 0
                if (aux[1] == -1):
                    a = 0
                if verificar(arreglo, de, a): # Verificar con cualquier arreglo, ya que deben de ser del mismo tamaño
                    for r in range(de,a+1): subArreglo.append(arreglo[r])
                    try:
                        llenarValor(pilaCorriendo, cuadruplo[3], tipo, statistics.mode(subArreglo))
                    except:
                        print("Error Maquina Virtual: El arreglo no tiene moda o tiene mas de una, en el rango de {} a {}".format(de, a))
                        sys.exit()
                        return
            else:
                try:
                    llenarValor(pilaCorriendo, cuadruplo[3], tipo, statistics.mode(arreglo))
                except:
                    print("Error Maquina Virtual: El arreglo no tiene moda o tiene mas de una, en todo el archivo")
                    sys.exit()
                    return
        # varianza
        elif cuadruplo[0] == 'varianza':
            subArreglo = []
            tipo = getTipo(cuadruplo[3])
            arreglo = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            aux = cuadruplo[2].split('#')
            if (aux[0] != '0' and aux[1] != '0'): #Si vienen 0 significa que es todo el arreglo
                de = int(aux[0][1:]) 
                a = int(aux[1][:])
                # Si es -1, significa que es 0
                if (aux[0] == -1):
                    de = 0
                if (aux[1] == -1):
                    a = 0
                if verificar(arreglo, de, a): # Verificar con cualquier arreglo, ya que deben de ser del mismo tamaño
                    for r in range(de,a+1): subArreglo.append(arreglo[r])
                    try:
                        llenarValor(pilaCorriendo, cuadruplo[3], tipo, statistics.variance(subArreglo))
                    except:
                        print("Error Maquina Virtual: Error al calcular la varianza, del rango de {} a {}".format(de, a))
                        sys.exit()
                        return
            else:
                try:
                    llenarValor(pilaCorriendo, cuadruplo[3], tipo, statistics.variance(arreglo))
                except:
                    print("Error Maquina Virtual: Error al calcular la varianza, en todo el archivo")
                    sys.exit()
                    return
        # correlation
        elif cuadruplo[0] == 'correlacion':
            subArreglo1 = []
            subArreglo2 = []
            cuadAUX = cuadruplo[1].split('#')
            tipo1 = getTipo(cuadAUX[0][1:])
            tipo2 = getTipo(cuadAUX[1][:])
            arr1 = getValor(pilaCorriendo, cuadAUX[0][1:],tipo1)
            arr2 = getValor(pilaCorriendo, cuadAUX[1][:],tipo2)
            if (len(arr1) == len(arr2)):
                aux = cuadruplo[2].split("#")
                if (aux[0] != '0' and aux[1] != '0'): #Si vienen 0 significa que es todo el arreglo
                    de = int(aux[0][1:]) 
                    a = int(aux[1][:])
                    # Si es -1, significa que es 0
                    if (aux[0] == -1):
                        de = 0
                    if (aux[1] == -1):
                        a = 0
                    if verificar(arr1, de, a): # Verificar con cualquier arreglo, ya que deben de ser del mismo tamaño
                        for r in range(de,a+1): 
                            subArreglo1.append(arr1[r])
                            subArreglo2.append(arr2[r])
                        try:
                            i = np.corrcoef(subArreglo1,subArreglo2)
                        except:
                            print("Error Maquina Virtual: Error al calcular la varianza, del rango de {} a {}".format(de, a))
                            sys.exit()
                            return
                else:
                    try:
                        i = np.corrcoef(arr1, arr2)
                    except:
                        print("Error Maquina Virtual: Error al calcular la correlacion")
                        sys.exit()
                        return
                llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), i[0][1])

            else: 
                print("Error Maquina Virtual: Los dataframes para el coeficiente de correlacion no son del mismo tamaño")
        # plothist
        elif cuadruplo[0] == 'histograma':
            subArreglo = []
            arr = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            if (cuadruplo[2] != '0' and cuadruplo[3] != '0'): #Si vienen 0 significa que es todo el arreglo
                de = int(cuadruplo[2])
                a = int(cuadruplo[3])
                # Si es -1, significa que es 0
                if (cuadruplo[2] == -1):
                    de = 0
                if (cuadruplo[3] == -1):
                    a = 0
                if verificar(arr, de, a): # Verificar con cualquier arreglo, ya que deben de ser del mismo tamaño
                    for r in range(de,a+1): 
                        subArreglo.append(arr[r])
                    try:
                        a = np.histogram(subArreglo)
                        plt.hist(a)
                        plt.savefig("histograma.png")
                        plt.show()
                        print("WARNING Maquina Virtual: En caso de que no se vea la imagen, se guardo como histograma.png")
                        plt.close()                    
                    except:
                        print("Error no se logro graficar el histograma")
                        sys.exit()
            else:
                try:
                    a = np.histogram(arr)
                    plt.hist(a)
                    plt.savefig("histograma.png")
                    plt.show()
                    print("WARNING Maquina Virtual: En caso de que no se vea la imagen, se guardo como histograma.png")
                    plt.close()
                except:
                    print("Error no se logro graficar el histograma")
                    sys.exit()
        # plotline
        elif cuadruplo[0] == 'plotline':
            subArreglo1 = []
            subArreglo2 = []
            arr1 = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            arr2 = getValor(pilaCorriendo, cuadruplo[2], getTipo(cuadruplo[2]))
            axisX = [] # Para tener donde comporar los arreglos
            if (len(arr1) == len(arr2)): # Dataframes deben ser del mismo tamaño
                if (cuadruplo[2] != '0' and cuadruplo[3] != '0'): #Si vienen 0 significa que es todo el arreglo
                    de = 0 # Siempre sera de 0 en adelante
                    a = int(getValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3])))
                    if (a == -1):
                        a = 0
                    if verificar(arr1, de, a): # Verificar con cualquier arreglo, ya que deben de ser del mismo tamaño
                        for r in range(de,a+1): 
                            subArreglo1.append(arr1[r])
                            subArreglo2.append(arr2[r])
                            axisX.append(r)
                        try:
                            plt.plot(axisX,subArreglo1, label='Dataframe 1')
                            plt.plot(axisX,subArreglo2, label='Dataframe 2')
                            plt.legend()
                            plt.savefig("plotline.png")
                            plt.show()
                            print("WARNING Maquina Virtual: En caso de que no se vea la imagen, se guardo como plotline.png")
                            plt.close()
                        except:
                            print("Error no se logro graficar")
                            sys.exit()
                else:
                    #Create x Axis
                    for r in range(0, len(arr1) - 1):axisX.append(r)
                    try:
                        plt.plot(axisX,arr1, label='Dataframe 1')
                        plt.plot(axisX,arr2, label='Dataframe 2')
                        plt.legend()
                        plt.savefig("plotline.png")
                        plt.show()
                        print("WARNING Maquina Virtual: En caso de que no se vea la imagen, se guardo como plotline.png")
                        plt.close()
                    except:
                        print("Error no se logro graficar")
                        sys.exit()
            else:
                print("Error Maquina Virtual: Los dataframes en plotline no son del mismo tamaño")
        #Carga de Archivos
        elif cuadruplo[0] == 'carga':
            nombreArchivo = cuadruplo[2]
            nombreArchivo = nombreArchivo.replace('"','')
            nombreArchivo = nombreArchivo.replace('"','')
            archivo = getArchivo(nombreArchivo)
            arreglo = []
            for val in archivo:
                try:
                    int(val)
                    val = int(val)
                except:
                    try:
                        float(val)
                        val = float(val)
                    except:
                        pass
                arreglo.append(val)
            llenarValor(mem_GLOBAL, cuadruplo[1], getTipo(cuadruplo[1]), arreglo)
        #ARREGLO
        #VER
        elif cuadruplo[0] == 'VER':
            valor = int(getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1])))
            if valor != 0:
                valor = valor - 1 # Para que se vuelva índice y se prueba.
            if valor > int(cuadruplo[3]) or valor < int(cuadruplo[2]):
                print("Error Maquina Virtual: El valor {} no pertence a los indices.".format(valor+1))
                sys.exit()
                return
        #FINPROGRAMA
        elif cuadruplo[0] == 'FINPROGRAMA':
            terminado = True
        # OPERADORES 
        elif cuadruplo[0] != 'CONS':
            operadores(cuadruplo[0])

        if sigCuaIndice != -1:
            cuaIndice = sigCuaIndice
        else: #Solo se ejecuta el siguiente quad
            cuaIndice = cuaIndice + 1

# Put all test inside prueba folder
def getArchivo(name):
    try:
        f = open(name,'r', encoding='utf-8')
        return f
        f.close()
    except EOFError:
        print ("Error Maquina Virtual:", EOFError, " no se encuentra el archivo {}".format(name))

cuadruplos = getArchivo('obj.txt')
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
