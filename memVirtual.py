# Jose Arturo Villalobos A00818214
# Rodrigo Valencia A00818256
# Diseno de compiladores
# Clase Memoria Virtual
import sys

"""
Esta clase permitirá manejar la memoria de la maquina virtual,
mediante instancias, que seran generadas para cada funcion recibida,
empezando por la global. 
"""

class memVirtual:
    def __init__(self, fun):
        # Guardamos el nombre de funcion al que pertenece la tabla
        self.funNombre = fun
        # Declaramos diccionario para las direcciones de la tabla de variable
        self.direcciones = {
            #tipo       #direcciones
            'int'       : {},
            'float'     : {},
            'char'      : {},
            'string'    : {},
            'DataFrame' : {}
        }

    """
    Guardar el valor, en una direccion específica
    """
    def guardarValor(self, direccion, tipo, valor):
        print("entre")
        self.direcciones[str(tipo)][str(direccion)] = valor
        print(direccion, " ", tipo, " ", valor)

    """
    Obtener el valor de una direccion en específico
    """
    def obtenerValorDeDireccion(self, direccion, tipo):
        try:
            valor = self.direcciones[str(tipo)][str(direccion)]
            return valor
        except:
            print("Error: ", sys.exc_info()[0], " en memoria {}, tipo {}, nombre de la funcion {}.".format(direccion, tipo, self.funNombre))
            raise

    """
    Obtener la siguiente dirreccion disponible
    """
    def sigDireccionDisponible(self, tipo, direccion_inicial, tam):
        if tipo == 'int':
            aux = 0
        elif tipo == 'float':
            aux = tam
        elif tipo == 'char':
            aux = tam * 2
        elif tipo == 'string':
            aux = tam * 3
        elif tipo == 'bool':
            aux = tam * 4

        return direccion_inicial + aux + len(self.direcciones[tipo])

    """
    Imprimir diccionario de la memoria
    """
    def imprimirDir(self):
        print("Nombre de memoria {}: \n".format(self.funNombre))
        print(self.direcciones)