# Jose Arturo Villalobos A00818214
# Rodrigo Valencia
# Diseno de compiladores
# Cubo Semantico de Funciones especiales
#Creacion: 27 de Abril 2020
#Ultima modificacion: 27 Abril 2020

class CuboSemantico_FuncEsp:
    '''
    Combinaciones entre funciones especiales y sus posibles operandos de parametro para todos los tipos de datos manejados por el lenguaje de COVID 

    (funcion_especial, operando1, operando2) : tipo de operando resultado

    Funciones especiales: Media, Mediana, Moda, Varianza, Correlaciona
    '''

    def __init__(self):
        self.diccionario = {
            ('Media', 'int', '') : 'float',
            ('Media', 'float', '') : 'float',

            ('Mediana', 'int', '') : 'float',
            ('Mediana', 'float', '') : 'float',

            ('Moda', 'int', '') : 'int',
            ('Moda', 'float', '') : 'float',

            ('Varianza', 'int', '') : 'float',
            ('Varianza', 'float', '') : 'float',

            ('Correlaciona', 'int', '') : 'float',
            ('Correlaciona', 'float', '') : 'float',

            ('plothist', 'int', '') : 'histogram',
            ('plothist', 'float', '') : 'histogram',

            ('plotline', 'int', 'int') : 'line',
            ('plotline', 'int', 'float') : 'line',
            ('plotline', 'float', 'int') : 'line',
            ('plotline', 'float', 'float') : 'line'
        }

    '''
    Funcion para obtener el tipo de valor resultado de la funcion especial con los tipos de valor pasados como parametro
    '''
    def getType(self, funcion_especial, operando1, operando2):
        try:
            resultado = self.diccionario[funcion_especial, operando1, operando2]
        except:
            resultado = 'error'
        
        return resultado