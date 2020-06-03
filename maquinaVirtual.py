# Jose Arturo Villalobos A00818214
# Rodrigo Valencia A00818256
# Diseno de compiladores
# Maquina Virtual

import sys
from memVirtual import *
import numpy as np
import statistics as statistics
import matplotlib.pyplot as plt

'''
Declaracion de constantes
'''
GBL = 'globales'
LCL = 'locales'
CONST_TEMPORAL = 'temporal'
CONST_EJECUCION = 'ejecucion'
CONST_RETORNO_VALOR = 'retorno'
CONST_FUNCION_RETORNO = 'funcion'
ESPACIO_MEMORIA = 1000

'''
Inicializamos las instancias de memoria de defaul
Globla y funcion principal
'''
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

'''
Funciones de control de las pilas
'''
# Funcion para hacer push a las diferenes pilas y poder manear las diferentes instancias de memmoria
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
# Funcion para hacer pop a las diferenes pilas y poder manear las diferentes instancias de memmoria
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
# Funcion para sacar pop de las principales pilas a las diferenes pilas y poder manear las diferentes instancias de memmoria
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

# Declaramos la primera instancia de la memoria principal
push(CONST_EJECUCION, mem_PRINCIPAL)

'''
Funcion que permite sacar los valores de la clase memoria, mandando la instacnia de memoria, la direccion y el tipo
'''
def getValor(memVirtual, memDireccion, memTipo):
    global mem_GLOBAL
    try: # En caso de que sea un apuntador
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
'''
Funcion que permite meter los valores a la clase memoria, mandando la instacnia de memoria, la direccion y el tipo
'''
def llenarValor(memVirtual, memDireccion, memTipo, valor):
    global mem_GLOBAL
    try: # En caso de que sea un apuntador
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

'''
Esta funcion ayuda a sacar la seccion de la memoria, mediante el numero
'''
def getSeccion(direccion):
    global pilaCorriendo
    try:
        if direccion[-1] == '!':
            direccion = getValor(pilaCorriendo, direccion[0:-1], getTipo(direccion[0:-1]))
    except:
        pass
    direccion = int(direccion)
    # GLOBALES y CONSTANTES se guardan donde mismo
    if ((direccion >= 0 and direccion < limite_dfGlobales) or (direccion >= limite_boolTemporales and direccion <= limite_dfConstantes)):
        return GBL
    # LOCALES y TEMPORALES se guardan donde mismo
    if ((direccion >= limite_dfGlobales and direccion < limite_dfLocales) or (direccion >= limite_dfLocales and direccion < limite_boolTemporales)):
        return LCL
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro de ninguna seccion".format(direccion))
        sys.exit()
        return

'''
Esta funcion permite sacar el tipo, al que pertenece la direccion que se le envia
'''
def getTipo(direccion):
    global pilaCorriendo
    try: 
        if direccion[-1] == '!':
            direccion = getValor(pilaCorriendo, direccion[0:-1], getTipo(direccion[0:-1]))
    except:
        pass
    direccion = int(direccion)
    if ((direccion >= 0 and direccion < limite_intGlobales) or (direccion >= limite_dfGlobales and direccion < limite_intLocales) or (direccion >= limite_dfLocales and direccion < limite_intTemporales) or (direccion >= limite_boolTemporales and direccion < limite_intConstantes)):
        return 'int'
    if ((direccion >= limite_intGlobales and direccion < limite_floatGlobales) or (direccion >= limite_intLocales and direccion < limite_floatLocales) or (direccion >= limite_intTemporales and direccion < limite_floatTemporales) or (direccion >= limite_intConstantes and direccion < limite_floatConstantes)):
        return 'float'
    if ((direccion >= limite_floatGlobales and direccion < limite_stringsGlobales) or (direccion >= limite_floatLocales and  direccion < limite_stringsLocales) or (direccion >= limite_floatTemporales and direccion < limite_stringsTemporales) or (direccion >= limite_floatConstantes and direccion < limite_stringsConstantes)):
        return 'string'
    if ((direccion >= limite_stringsGlobales and direccion < limite_charGlobales) or (direccion >= limite_stringsLocales and direccion <limite_charLocales) or (direccion >= limite_stringsTemporales and direccion < limite_charTemporales) or (direccion >= limite_stringsConstantes and direccion < limite_charConstantes)):
        return 'char'
    if ((direccion >= limite_charGlobales and direccion < limite_dfGlobales) or (direccion >= limite_charLocales and direccion < limite_dfLocales) or (direccion >= limite_charTemporales and direccion < limite_dfTemporales) or (direccion >= limite_charConstantes and direccion < limite_dfConstantes)):
        return 'dataframe'
    if (direccion >= limite_dfTemporales and direccion < limite_boolTemporales):
        return 'bool'
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro del rango de ningun tipo de variable".format(direccion))
        sys.exit()
        return
'''
Funcion operadores, para sacar el signo
'''
def operadores(signo):
    global cuadruplo
    global pilaCorriendo
    if signo == '+':
        if cuadruplo[1][0] == '{' and cuadruplo[1][-1] == '}':  # En caso de que se refiera a la suma de la direccion de vector
            valor1 = int(cuadruplo[1][1:-1])
            valor2 = getValor(pilaCorriendo, cuadruplo[2], getTipo(cuadruplo[2]))
            valor2 = int(valor2)
        else: # Suma normal de dos valores
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
'''
 Verifica que los indices esten dentro del dataframe o arreglo
'''
def verificar(arr, de, a):
    l = len(arr) - 1
    if de < 0 or de > l:
        print("Error Maquina Virtual: el inidice {} no esta dentro del rango del dataframe o arreglo 0 a {} ".format(de,l))
        sys.exit()
        return False
    if  a < 0 or a > l:
        print("Error Maquina Virtual: el inidice {} no esta dentro del rango del dataframe o arreglo 0 a {} ".format(a,l))
        sys.exit()
        return False
    return True

'''
    FUNCION PRINCIPAL
    Usa los cuádruplos para detectar que debe de ejecutar.
'''

def correr():
    # Se declaran las variables globales a utilizar
    global constLista
    global cuaLista
    global cuaIndice
    global cuadruplo
    global mem_GLOBAL
    global pilaRetorno
    global sigCuaIndice
    global pilaCorriendo

    # Ciclo que permite guardar todos los constantes antes de correr los demas cuadruplo
    for cons in constLista:
        llenarValor(mem_GLOBAL, cons[3], cons[1], cons[2])

    terminado = False # nos avisas cuando salir del programa
    while not terminado:
        sigCuaIndice = -1 # nos permite llevar control, de que cuadro ejecutar
        pilaCorriendo = top(CONST_EJECUCION) # Saca la instancia de memoria que se este ejecutando
        cuadruplo = cuaLista[cuaIndice] # Saca el cuadruplo a ejecutar

        # ASIGNACION
        if cuadruplo[0] == '=':
            try: # Sino encuentra el valor, checa que este en la pila de valores de retorno 
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
            if not auxValor: #Confirma si es falso el valor
                sigCuaIndice = int(cuadruplo[3])
        # GOSUB
        elif cuadruplo[0] == 'GOSUB':
            pilaCorriendo = pop(CONST_TEMPORAL) # Sacamos la instancia de memoria temporal
            push(CONST_EJECUCION, pilaCorriendo) # Metemos la instancia a ejecucion
            push(CONST_FUNCION_RETORNO, cuadruplo[2]) # Guardamos el retorno
            sigCuaIndice = int(cuadruplo[3])
        # ERA
        elif cuadruplo[0] == 'ERA':
            #Declara nueva funcion de memoria virtual
            memNueva = memVirtual(str(cuadruplo[1]))
            push(CONST_TEMPORAL, memNueva)
        # PARAMETER
        elif cuadruplo[0] == 'PARAMETER':
            tipo = getTipo(cuadruplo[1])
            valor = getValor(pilaCorriendo, cuadruplo[1], tipo)
            auxMem = top(CONST_TEMPORAL)
            # Nos permite saber que direccion sigue
            # Donde empiezan las variables globales 
            direccion = auxMem.sigDireccionDisponible(tipo, 5000, ESPACIO_MEMORIA)
            llenarValor(auxMem, direccion, getTipo(direccion), valor)
        # ENDFUNC
        elif cuadruplo[0] == 'ENDFUNC':
            pop(CONST_EJECUCION)
            sigCuaIndice = int(pop(CONST_FUNCION_RETORNO))
        # regresa
        elif cuadruplo[0] == 'regresa':
            valor = getValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]))
            push(CONST_RETORNO_VALOR, str(valor)) #Guarda el valor para despues
            pop(CONST_EJECUCION) #Sacar funcion de la pila, porque se termino de ejecutar
            sigCuaIndice = int(pop(CONST_FUNCION_RETORNO));
        # lee
        elif cuadruplo[0] == 'lee':
            texto = input("<- ")
            #Verifica que tipo de valor es el que recibe, para guardarlo donde corresponde
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
            #Trae el valor y lo imprime
            texto = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            print("->",str(texto))
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
        elif cuadruplo[0] == 'ordena':
            inicio = int(cuadruplo[1])
            tam = int(cuadruplo[2])
            tipo = getTipo(cuadruplo[1])
            arr = []
            #Crea arreglo a partir de los datos de memoria
            for i in range (0, tam-1):
                valor = getValor(pilaCorriendo, inicio + i, tipo)
                # Verifca que valor utilizar
                try:
                    int(valor)
                    valor = int(valor)
                except:
                    try:
                        float(valor)
                        valor = float(valor)
                    except:
                        try:
                            str(valor)
                            tipo = 'char' if len(valor) == 1 else 'string'
                        except:
                            print("Error Maquina Virtual: {}".format(sys.exc_info()[0], cuaIndice))
                arr.append(valor)
            arr.sort()
            for i in range (0, tam-1): llenarValor(pilaCorriendo, inicio + i, tipo, arr[i])
        elif cuadruplo[0] == 'encontrar':
            inicio = int(cuadruplo[1])
            tipo = getTipo(cuadruplo[1])
            aux = cuadruplo[2].split('#')
            tam = int(aux[0][1:])
            buscado = int(aux[1][:])
            arr = []
            #Crea arreglo a partir de los datos de memoria
            for i in range (0, tam-1):
                valor = getValor(pilaCorriendo, inicio + i, tipo)
                # Verifca que valor utilizar
                try:
                    int(valor)
                    valor = int(valor)
                except:
                    try:
                        float(valor)
                        valor = float(valor)
                    except:
                        try:
                            str(valor)
                            valor = 'char' if len(valor) == 1 else 'string'
                        except:
                            print("Error Maquina Virtual: {}".format(sys.exc_info()[0], cuaIndice))
                arr.append(valor)
            llenarValor(pilaCorriendo, cuadruplo[3], tipo, arr.index(buscado))
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
                    for r in range(de,a+1): subArreglo.append(arreglo[r]) #Crea arreglo a partir de los datos sacados
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
                    for r in range(de,a+1): subArreglo.append(arreglo[r])#Crea arreglo a partir de los datos sacados
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
                    for r in range(de,a+1): subArreglo.append(arreglo[r])#Crea arreglo a partir de los datos sacados
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
                    for r in range(de,a+1): subArreglo.append(arreglo[r])#Crea arreglo a partir de los datos sacados
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
                        for r in range(de,a+1): #Crea arreglos a partir de los datos sacados
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
                        subArreglo.append(arr[r])#Crea arreglo a partir de los datos sacados
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
                        for r in range(de,a+1): #Crea arreglos a partir de los datos sacados
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
            #FINPROGRAMA
        elif cuadruplo[0] == 'FINPROGRAMA':
            terminado = True
        # OPERADORES 
        elif cuadruplo[0] != 'CONS':
            operadores(cuadruplo[0])

        # Controla el indice para saber que cuadroplo ejecutar
        if sigCuaIndice != -1:
            cuaIndice = sigCuaIndice
        else: 
            cuaIndice = cuaIndice + 1

# Funcion para abrir archivo
def getArchivo(name):
    try:
        f = open(name,'r', encoding='utf-8')
        return f
        f.close()
    except EOFError:
        print ("Error Maquina Virtual:", EOFError, " no se encuentra el archivo {}".format(name))

cuadruplos = getArchivo('obj.txt') # saca el archivo de cuadruplos

# GUarda los cuadruplos en una lista
for linea in cuadruplos:
    linea = linea.replace('(','')
    linea = linea.replace(')','')
    linea = linea.replace('\n','')
    linea = linea.replace('\'','')
    linea = linea.replace(' ','')
    cuadruplo = tuple(linea.split(','))
    if (cuadruplo[0] == 'CONS'): # Lista de constntes, para guardarlos desde un principio en memoria
        cuadroCONST = (cuadruplo[0], cuadruplo[1], cuadruplo[2], cuadruplo[3])
        constLista.append(cuadroCONST)
    cuadruplo = (cuadruplo[0], cuadruplo[1], cuadruplo[2], cuadruplo[3])
    cuaLista.append(cuadruplo)

correr()
