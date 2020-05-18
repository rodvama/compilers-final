# Jose Arturo Villalobos A00818214
# Rodrigo Valencia A00818256
# Diseno de compiladores
# Cubo Semantico de Funciones especiales
#Creacion: 27 de Abril 2020
#Ultima modificacion: 8 de Mayo 2020

''' 
Cubo Semantico representado por un Diccionario, que contiene el Tipo Resultante de hacer operaciones entre todas las combinaciones entre funciones especiales que manejara nuestro lenguaje COVID y sus operandos.

Las funciones especiales que contiene COVID son:
    - Media
    - Moda
    - Mediana
    - Varianza
    - plothist
    - plotline

Tambien incluye los resultados cuando se utilizan los estatutos de lectura (lee) y escritura (escribe). 

La estructura que va a manejar el cubo semantico es la siguiente:
        
    (operando1, operando2, operador) : tipo de operando resultante

    Error: Type Mismatch
'''

class CuboSemantico_FuncEsp:
    def __init__(self):
        self.CS_FEsp = {
            ('Media', 'int', '') : 'float',
            ('Media', 'float', '') : 'float',

            ('Mediana', 'int', '') : 'float',
            ('Mediana', 'float', '') : 'float',

            ('Moda', 'int', '') : 'int',
            ('Moda', 'float', '') : 'float',

            ('Varianza', 'int', '') : 'float',
            ('Varianza', 'float', '') : 'float',

            ('Correlaciona', 'int', 'int') : 'float',
            ('Correlaciona', 'float', 'int') : 'float',
            ('Correlaciona', 'int', 'float') : 'float',
            ('Correlaciona', 'float', 'float') : 'float',

            ('plothist', 'int', 'int') : 'histogram',
            ('plothist', 'float', 'int') : 'histogram',

            ('plotline', 'int', 'int') : 'line',
            ('plotline', 'int', 'float') : 'line',
            ('plotline', 'float', 'int') : 'line',
            ('plotline', 'float', 'float') : 'line'
        }

    '''
    Funcion que obtiene el tipo resultante al ejecutar funciones especiales con otros tipos de operandos.
    '''
    def getType(self, funcion_especial, operando1, operando2):
        try:
            TypeResult = self.CS_FEsp[funcion_especial, operando1, operando2]
        except:
            TypeResult = 'error'
        
        return TypeResult