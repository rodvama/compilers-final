# Jose Arturo Villalobos A00818214
# Rodrigo Valencia
# Diseno de compiladores
# Directorio de Funciones

import sys

#Importa la Tabla de Variables
from TablaVars import *

class DirFunc:
    def __init__(self):
        '''
        Diccionario de directorio de Funciones
        diccionario = {nombre: nombre, tipo, cantParametros, variables}
        nombre : nombre de la funcion que se va a guardar
        tipo : tipo de la funcion que se va a guardar
        cantParametros : Cantidad de parametros para la funcion definida
        variables : objeto de tipo Jubilo_TablaVars para guardar las variables
        '''
        #Inicializacion del diccionario
        self.diccionario = {'global': {'nombre' : 'globals', 'tipo' : 'void', 'cantParametros' : 0, 'variables': TablaVars()}}
        print("Funcion creada : Globals de tipo void")


    '''
    Funcion para saber si ya existe una funcion en el diccionario
    '''
    def func_exist(self, nombre):
        return nombre in self.diccionario.keys()

    '''
    Funcion para agregar una funcion al diccionario
    '''
    def func_add(self, nombre, tipo, cantParametros):
        if self.func_exist(nombre):
            #Error Multiple declaration
            print "Error: Funcion ", str(nombre), " ya existe", "\n"
        else:
            self.diccionario[nombre] = {
                'nombre': nombre,
                'tipo': tipo,
                'cantParametros': cantParametros,
                'variables': TablaVars()
            }
            print "Funcion creada en el diccionario: ", nombre, " de tipo: ", tipo, "\n"

    '''
    Funcion que busca y regresa una funcion y sus datos
    '''
    def func_search(self, nombre):
        if self.func_exist(nombre):
            return self.diccionario[nombre]
        else:
            return None

    '''
    Funcion que intenta agregar una variable a la funcion nombre
    '''
    def func_addVar(self, nombre, nombreVar, tipoVar, renglonesVar, columnasVar):
        '''
        Dentro de mi diccionario de funciones, ir a la funcion nombre
        En su atributo variables e intentar agregar la nueva variable.
        Si regresa verdadero se pudo crear, si regresa falso ya existia esa variable.
        '''
        if self.diccionario[nombre]['variables'].var_add(nombreVar, tipoVar, renglonesVar, columnasVar):
            print "Variable: ", nombreVar, " creada en la funcion ", nombre
        else:
            print "Error: No se pudo crear la variable: ", nombreVar, " en la funcion: ", nombre
        
        print self.diccionario[nombre]['variables'].diccionario, "\n"
    
    
    # '''
    # Funcion que llama a la funcion en TablaVars para actualizar renglones y columnas de una variable
    # '''
    # def update_dimensions(self, nombre, nombreVar, renglones, columnas):
    #     if self.diccionario[nombre]['variables'].var_exist(nombreVar):
    #         if columnas > 0: #Se manda columnas > 0 cuando se van a actualizar columnas
    #             return self.diccionario[nombre]['variables'].update_varDimensions(nombreVar, renglones, columnas)
    #         else: #Se manda columnas -1 cuando se actualizan rengloens
    #             return self.diccionario[nombre]['variables'].update_varDimensions(nombreVar, renglones, -1)
    #     else:
    #         print("Warning: Variable ", nombreVar, "no existe en este contexto ", nombre)
    #         return None
    
    
    '''
    Funcion que regresa el string del tipo de una variable previamente creada en las funciones
    '''
    def func_searchVarType(self, nombre, nombreVar):
        if self.diccionario[nombre]['variables'].var_exist(nombreVar):
            return self.diccionario[nombre]['variables'].var_searchType(nombreVar)
        else:
            print("Advertencia: Variable: ", nombreVar ," no existe en este contexto: ", nombre)
            return None
    
    '''
    Funcion que regresa si existe una variable en la tabla de variables de la funcion dada
    '''
    def var_exist(self, nombre, nombreVar):
        if self.diccionario[nombre]['variables'].var_exist(nombreVar):
            return True
        else:
            return False

    '''
    Funcion para actualizar el numero de parametros de una funcion previamente creada
    '''
    def func_UpdateParams(self, nombre, cantParametros):
        #Si ya existe la funcion actualizar su cantidad  de parametros directamente
        if self.func_exist(nombre):
            self.diccionario[nombre]['cantParametros'] = cantParametros

        #Si no existe desplegar error
        else:
            print("Error: Imposible actualizar parametros de una funcion no existente: ", nombre)

        #print("Funcion creada: ", nombre, " de tipo: ", self.diccionario[nombre]['tipo'], " con cantParametros: ", cantParametros)

    def func_deleteDic(self):
        self.diccionario.clear()