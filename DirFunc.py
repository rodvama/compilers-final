# Jose Arturo Villalobos A00818214
# Rodrigo Valencia A00818256
# Diseno de compiladores
# Directorio de Funciones

import sys
from TablaVars import *

'''
El Directorio de Funciones sera representado por un Diccionario, el cual incluira los atributos semanticos de: 
- nombre : nombre de la funcion 
- tipo : tipo de la funcion 
- cantParametros : Cantidad de parametros 
- variables : link hacia la tabla de variables
- cantQuads : cantidad actual de cuadruplos
'''

class DirFunc:
    '''
    Constructor que inicializa el diccionario directorio_funciones con sus atributos, empezando con la seccion de globales.
    '''
    def __init__(self):
        self.directorio_funciones = {'global': {'nombre' : 'global', 'tipo' : 'void', 'cantParametros' : 0, 'variables': TablaVars(), 'cantQuads' : 0}}
        print("Funcion creada exitosamente: Global de tipo void")


    '''
    Funcion que checa si ya existe una funcion en el directorio_funciones
    '''
    def func_existe(self, nombre):
        return nombre in self.directorio_funciones.keys()

    '''
    Funcion para agregar una funcion nueva al diccionario de directorio_funciones
    '''
    def func_add(self, nombre, tipo, cantParametros, cantQuads):
        if self.func_existe(nombre):
            print ("Error: Declaracion multiple de funcion: ", str(nombre), "\n")
        else:
            self.directorio_funciones[nombre] = {
                'nombre': nombre,
                'tipo': tipo,
                'cantParametros': cantParametros,
                'variables': TablaVars(),
                'cantQuads': cantQuads
            }
            print ("NUEVA Funcion creada en el Directorio de Funciones: ", nombre, " de tipo: ", tipo, "\n")

    '''
    Funcion que regresa todos los datos de la funcion dada. Si no existe no regresa nada.
    '''
    def func_search(self, nombre):
        if self.func_existe(nombre):
            return self.directorio_funciones[nombre]
        else:
            return None

    '''
    Funcion que agrega una variable a la tabla de variables linkeada a la funcion dada.
    '''
    def func_addVar(self, nombre, nombreVar, tipoVar, renglonesVar, columnasVar, memPos):

        if self.directorio_funciones[nombre]['variables'].var_add(nombreVar, tipoVar, renglonesVar, columnasVar, memPos):
            print ("Variable: ", nombreVar, " creada exitosamente, dentro de la funcion:  ", nombre)
        else:
            print ("Error: No es posible crear la variable: ", nombreVar, " dentro de  la funcion: ", nombre)
    
    
    '''
    Funcion para actualizar indicar que una variable es dimensionada
    '''
    def func_updateDim(self, nombre, nombreVar, renglones, columnas):
        if self.directorio_funciones[nombre]['variables'].var_exist(nombreVar):
            if columnas > 0:
                return self.directorio_funciones[nombre]['variables'].var_upadateDims(nombreVar, renglones, columnas)
            else:
                return self.directorio_funciones[nombre]['variables'].var_upadateDims(nombreVar, renglones, -1)
        else:
            print("Error: Variable ", nombreVar, "no existe en este contexto ", nombre)
            return None
    

    '''
    Funcion que dice si una variable dada es dimensionada en el contexto dado
    '''
    def func_isVarDimensionada(self, nombre, nombreVar):
        if self.directorio_funciones[nombre]['variables'].var_exist(nombreVar):
            print("DIRECTORIO FUNC DE ", nombreVar, "col: ", self.directorio_funciones[nombre]['variables'].tabla_variables[nombreVar]['columnas'])

            if self.directorio_funciones[nombre]['variables'].tabla_variables[nombreVar]['columnas'] > 0 or self.directorio_funciones[nombre]['variables'].tabla_variables[nombreVar]['renglones'] > 0:
                return 1
            else:
                return 0
        else:
            return -1 #No existe esa variable en este contexto
    

    '''
    Funcion que regresa las dimensiones de una variable dimensionada en forma de lista
    '''
    def func_getDims(self, nombre, nombreVar):
        if self.directorio_funciones[nombre]['variables'].var_exist(nombreVar):
            dim = [self.directorio_funciones[nombre]['variables'].tabla_variables[nombreVar]['columnas'], self.directorio_funciones[nombre]['variables'].tabla_variables[nombreVar]['renglones']]
            return dim
        else:
            return -1 #No existe esa variable en este contexto

    
    '''
    Funcion que regresa el string del tipo de una variable previamente creada en las funciones
    '''
    def func_searchVarType(self, nombre, nombreVar):
        if self.directorio_funciones[nombre]['variables'].var_exist(nombreVar):
            return self.directorio_funciones[nombre]['variables'].var_searchType(nombreVar)
        else:
            print("Error: Variable: ", nombreVar ," no existe en este contexto: ", nombre)
            return None
    
    '''
    Funcion que regresa si existe una variable en la tabla de variables de la funcion dada
    '''
    def var_exist(self, nombre, nombreVar):
        if self.directorio_funciones[nombre]['variables'].var_exist(nombreVar):
            return True
        else:
            return False

    '''
    Funcion para cambiar la cantidad de parametros de una funcion dada.
    '''
    def func_UpdateParametros(self, nombre, cantParametros):
        if self.func_existe(nombre):
            self.directorio_funciones[nombre]['cantParametros'] = cantParametros
        else:
            print("Error: NO existe la funcion: ", nombre)

    

    '''
    
    '''
    def listaTipos(self, funcion):
        return [self.directorio_funciones[funcion]['variables'].tabla_variables[x]['tipo'] for x in self.directorio_funciones[funcion]['variables'].tabla_variables]

    '''
    Funcion que regresa la posicion de memoria virtual de la variable dada
    '''
    def func_memoria(self, nombre, nombreVar):
        if self.directorio_funciones[nombre]['variables'].var_exist(nombreVar):
            return  self.directorio_funciones[nombre]['variables'].var_searchMemPos(nombreVar)
        else:
            print("Error: Variable: ", nombreVar, "no existe en este contexto: ", nombre)

    '''
    Funcion que imprime el directorio de funciones actual
    '''
    def func_print(self):
        print (self.directorio_funciones[nombre]['variables'].tabla_variables)
        print("\n")

    '''
    Funcion que borra el directorio de funciones
    '''
    def func_deleteDic(self):
        self.directorio_funciones.clear()