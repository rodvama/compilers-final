# Jose Arturo Villalobos A00818214
# Rodrigo Valencia A00818256
# Diseno de compiladores
#Creacion: 25 de Abril 2020
#Ultima modificacion: 8 de Mayo 2020

############################### CUBO SEMANTICO #####################################

'''
Para representar el cubo semantico vamos a utilizar un Diccionario que contiene todas las combinaciones posibles entre dos operandos, utilizando todos los tipos que existen en el lenguaje COVID. 
        
Los tipos de datos que contiene COVID son:
    - Int
    - Float
    - Char
    - String
    - Dataframe

Tambien incluye los resultados cuando se utilizan los estatutos de lectura (lee) y escritura (escribe). 

La estructura que va a manejar el cubo semantico es la siguiente:
        
    (operando1, operando2, operador) : tipo de operando resultante

    Error: Type Mismatch
        
'''
class CuboSemantico:

    ''' 
    Conctructor
    '''
    def __init__(self):

        self.CuboSem = {
            #Int 
            ('int' , 'int' , '+' ) : 'int',
            ('int' , 'int' , '-' ) : 'int',
            ('int' , 'int' , '*' ) : 'int',
            ('int' , 'int' , '/' ) : 'float',
            ('int' , 'int' , '=' ) : 'int',
            ('int' , 'int' , '==' ) : 'bool',
            ('int' , 'int' , '<' ) : 'bool',
            ('int' , 'int' , '>' ) : 'bool',
            ('int' , 'int' , '<=' ) : 'bool',
            ('int' , 'int' , '>=' ) : 'bool',
            ('int' , 'int' , '!=' ) : 'bool',
            ('int' , 'int' , '|' ) : 'error',
            ('int' , 'int' , '&' ) : 'error',

            ('int' , 'float' , '+' ) : 'float',
            ('int' , 'float' , '-' ) : 'float',
            ('int' , 'float' , '*' ) : 'float',
            ('int' , 'float' , '/' ) : 'float',
            ('int' , 'float' , '=' ) : 'int', 
            ('int' , 'float' , '==' ) : 'bool',
            ('int' , 'float' , '<' ) : 'bool',
            ('int' , 'float' , '>' ) : 'bool',
            ('int' , 'float' , '<=' ) : 'bool',
            ('int' , 'float' , '>=' ) : 'bool',
            ('int' , 'float' , '!=' ) : 'bool',
            ('int' , 'float' , '|' ) : 'error',
            ('int' , 'float' , '&' ) : 'error',

            ('int' , 'char' , '+' ) : 'error',
            ('int' , 'char' , '-' ) : 'error',
            ('int' , 'char' , '*' ) : 'error',
            ('int' , 'char' , '/' ) : 'error',
            ('int' , 'char' , '=' ) : 'error', 
            ('int' , 'char' , '==' ) : 'error',
            ('int' , 'char' , '<' ) : 'error',
            ('int' , 'char' , '>' ) : 'error',
            ('int' , 'char' , '<=' ) : 'error',
            ('int' , 'char' , '>=' ) : 'error',
            ('int' , 'char' , '!=' ) : 'error',
            ('int' , 'char' , '|' ) : 'error',
            ('int' , 'char' , '&' ) : 'error',
 
            ('int' , 'string' , '+' ) : 'error',
            ('int' , 'string' , '-' ) : 'error',
            ('int' , 'string' , '*' ) : 'error',
            ('int' , 'string' , '/' ) : 'error',
            ('int' , 'string' , '=' ) : 'error', 
            ('int' , 'string' , '==' ) : 'error',
            ('int' , 'string' , '<' ) : 'error',
            ('int' , 'string' , '>' ) : 'error',
            ('int' , 'string' , '<=' ) : 'error',
            ('int' , 'string' , '>=' ) : 'error',
            ('int' , 'string' , '!=' ) : 'error',
            ('int' , 'string' , '|' ) : 'error',
            ('int' , 'string' , '&' ) : 'error',

            ('int' , 'dataframe' , '+' ) : 'error',
            ('int' , 'dataframe' , '-' ) : 'error',
            ('int' , 'dataframe' , '*' ) : 'error',
            ('int' , 'dataframe' , '/' ) : 'error',
            ('int' , 'dataframe' , '=' ) : 'error', 
            ('int' , 'dataframe' , '==' ) : 'error',
            ('int' , 'dataframe' , '<' ) : 'error',
            ('int' , 'dataframe' , '>' ) : 'error',
            ('int' , 'dataframe' , '<=' ) : 'error',
            ('int' , 'dataframe' , '>=' ) : 'error',
            ('int' , 'dataframe' , '!=' ) : 'error',
            ('int' , 'dataframe' , '|' ) : 'error',
            ('int' , 'dataframe' , '&' ) : 'error',
            
            #Float 
            ('float' , 'int' , '+' ) : 'float',
            ('float' , 'int' , '-' ) : 'float',
            ('float' , 'int' , '*' ) : 'float',
            ('float' , 'int' , '/' ) : 'float',
            ('float' , 'int' , '=' ) : 'float', 
            ('float' , 'int' , '==' ) : 'bool',
            ('float' , 'int' , '<' ) : 'bool',
            ('float' , 'int' , '>' ) : 'bool',
            ('float' , 'int' , '<=' ) : 'bool',
            ('float' , 'int' , '>=' ) : 'bool',
            ('float' , 'int' , '!=' ) : 'bool',
            ('float' , 'int' , '|' ) : 'error',
            ('float' , 'int' , '&' ) : 'error',

            ('float' , 'float' , '+' ) : 'float',
            ('float' , 'float' , '-' ) : 'float',
            ('float' , 'float' , '*' ) : 'float',
            ('float' , 'float' , '/' ) : 'float',
            ('float' , 'float' , '=' ) : 'float', 
            ('float' , 'float' , '==' ) : 'bool',
            ('float' , 'float' , '<' ) : 'bool',
            ('float' , 'float' , '>' ) : 'bool',
            ('float' , 'float' , '<=' ) : 'bool',
            ('float' , 'float' , '>=' ) : 'bool',
            ('float' , 'float' , '!=' ) : 'bool',
            ('float' , 'float' , '|' ) : 'error',
            ('float' , 'float' , '&' ) : 'error',

            ('float' , 'char' , '+' ) : 'error',
            ('float' , 'char' , '-' ) : 'error',
            ('float' , 'char' , '*' ) : 'error',
            ('float' , 'char' , '/' ) : 'error',
            ('float' , 'char' , '=' ) : 'error', 
            ('float' , 'char' , '==' ) : 'error',
            ('float' , 'char' , '<' ) : 'error',
            ('float' , 'char' , '>' ) : 'error',
            ('float' , 'char' , '<=' ) : 'error',
            ('float' , 'char' , '>=' ) : 'error',
            ('float' , 'char' , '!=' ) : 'error',
            ('float' , 'char' , '|' ) : 'error',
            ('float' , 'char' , '&' ) : 'error',

            ('float' , 'string' , '+' ) : 'error',
            ('float' , 'string' , '-' ) : 'error',
            ('float' , 'string' , '*' ) : 'error',
            ('float' , 'string' , '/' ) : 'error',
            ('float' , 'string' , '=' ) : 'error', 
            ('float' , 'string' , '==' ) : 'error',
            ('float' , 'string' , '<' ) : 'error',
            ('float' , 'string' , '>' ) : 'error',
            ('float' , 'string' , '<=' ) : 'error',
            ('float' , 'string' , '>=' ) : 'error',
            ('float' , 'string' , '!=' ) : 'error',
            ('float' , 'string' , '|' ) : 'error',
            ('float' , 'string' , '&' ) : 'error',

            ('float' , 'dataframe' , '+' ) : 'error',
            ('float' , 'dataframe' , '-' ) : 'error',
            ('float' , 'dataframe' , '*' ) : 'error',
            ('float' , 'dataframe' , '/' ) : 'error',
            ('float' , 'dataframe' , '=' ) : 'error', 
            ('float' , 'dataframe' , '==' ) : 'error',
            ('float' , 'dataframe' , '<' ) : 'error',
            ('float' , 'dataframe' , '>' ) : 'error',
            ('float' , 'dataframe' , '<=' ) : 'error',
            ('float' , 'dataframe' , '>=' ) : 'error',
            ('float' , 'dataframe' , '!=' ) : 'error',
            ('float' , 'dataframe' , '|' ) : 'error',
            ('float' , 'dataframe' , '&' ) : 'error',

            #Char
            ('char' , 'int' , '+' ) : 'error',
            ('char' , 'int' , '-' ) : 'error',
            ('char' , 'int' , '*' ) : 'error',
            ('char' , 'int' , '/' ) : 'error',
            ('char' , 'int' , '=' ) : 'error', 
            ('char' , 'int' , '==' ) : 'error',
            ('char' , 'int' , '<' ) : 'error',
            ('char' , 'int' , '>' ) : 'error',
            ('char' , 'int' , '<=' ) : 'error',
            ('char' , 'int' , '>=' ) : 'error',
            ('char' , 'int' , '!=' ) : 'error',
            ('char' , 'int' , '|' ) : 'error',
            ('char' , 'int' , '&' ) : 'error',

            ('char' , 'float' , '+' ) : 'error',
            ('char' , 'float' , '-' ) : 'error',
            ('char' , 'float' , '*' ) : 'error',
            ('char' , 'float' , '/' ) : 'error',
            ('char' , 'float' , '=' ) : 'error', 
            ('char' , 'float' , '==' ) : 'error',
            ('char' , 'float' , '<' ) : 'error',
            ('char' , 'float' , '>' ) : 'error',
            ('char' , 'float' , '<=' ) : 'error',
            ('char' , 'float' , '>=' ) : 'error',
            ('char' , 'float' , '!=' ) : 'error',
            ('char' , 'float' , '|' ) : 'error',
            ('char' , 'float' , '&' ) : 'error',

            ('char' , 'char' , '+' ) : 'error',
            ('char' , 'char' , '-' ) : 'error',
            ('char' , 'char' , '*' ) : 'error',
            ('char' , 'char' , '/' ) : 'error',
            ('char' , 'char' , '=' ) : 'char', 
            ('char' , 'char' , '==' ) : 'bool',
            ('char' , 'char' , '<' ) : 'error',
            ('char' , 'char' , '>' ) : 'error',
            ('char' , 'char' , '<=' ) : 'error',
            ('char' , 'char' , '>=' ) : 'error',
            ('char' , 'char' , '!=' ) : 'bool',
            ('char' , 'char' , '|' ) : 'error',
            ('char' , 'char' , '&' ) : 'error',

            ('char' , 'string' , '+' ) : 'string',
            ('char' , 'string' , '-' ) : 'error',
            ('char' , 'string' , '*' ) : 'error',
            ('char' , 'string' , '/' ) : 'error',
            ('char' , 'string' , '=' ) : 'error', 
            ('char' , 'string' , '==' ) : 'bool',
            ('char' , 'string' , '<' ) : 'error',
            ('char' , 'string' , '>' ) : 'error',
            ('char' , 'string' , '<=' ) : 'error',
            ('char' , 'string' , '>=' ) : 'error',
            ('char' , 'string' , '!=' ) : 'bool',
            ('char' , 'string' , '|' ) : 'error',
            ('char' , 'string' , '&' ) : 'error',

            ('char' , 'dataframe' , '+' ) : 'error',
            ('char' , 'dataframe' , '-' ) : 'error',
            ('char' , 'dataframe' , '*' ) : 'error',
            ('char' , 'dataframe' , '/' ) : 'error',
            ('char' , 'dataframe' , '=' ) : 'error', 
            ('char' , 'dataframe' , '==' ) : 'error',
            ('char' , 'dataframe' , '<' ) : 'error',
            ('char' , 'dataframe' , '>' ) : 'error',
            ('char' , 'dataframe' , '<=' ) : 'error',
            ('char' , 'dataframe' , '>=' ) : 'error',
            ('char' , 'dataframe' , '!=' ) : 'error',
            ('char' , 'dataframe' , '|' ) : 'error',
            ('char' , 'dataframe' , '&' ) : 'error',

            #String
            ('string' , 'int' , '+' ) : 'error',
            ('string' , 'int' , '-' ) : 'error',
            ('string' , 'int' , '*' ) : 'error',
            ('string' , 'int' , '/' ) : 'error',
            ('string' , 'int' , '=' ) : 'error', 
            ('string' , 'int' , '==' ) : 'error',
            ('string' , 'int' , '<' ) : 'error',
            ('string' , 'int' , '>' ) : 'error',
            ('string' , 'int' , '<=' ) : 'error',
            ('string' , 'int' , '>=' ) : 'error',
            ('string' , 'int' , '!=' ) : 'error',
            ('string' , 'int' , '|' ) : 'error',
            ('string' , 'int' , '&' ) : 'error',

            ('string' , 'float' , '+' ) : 'error',
            ('string' , 'float' , '-' ) : 'error',
            ('string' , 'float' , '*' ) : 'error',
            ('string' , 'float' , '/' ) : 'error',
            ('string' , 'float' , '=' ) : 'error', 
            ('string' , 'float' , '==' ) : 'error',
            ('string' , 'float' , '<' ) : 'error',
            ('string' , 'float' , '>' ) : 'error',
            ('string' , 'float' , '<=' ) : 'error',
            ('string' , 'float' , '>=' ) : 'error',
            ('string' , 'float' , '!=' ) : 'error',
            ('string' , 'float' , '|' ) : 'error',
            ('string' , 'float' , '&' ) : 'error',

            ('string' , 'char' , '+' ) : 'string',
            ('string' , 'char' , '-' ) : 'error',
            ('string' , 'char' , '*' ) : 'error',
            ('string' , 'char' , '/' ) : 'error',
            ('string' , 'char' , '=' ) : 'char', 
            ('string' , 'char' , '==' ) : 'bool',
            ('string' , 'char' , '<' ) : 'error',
            ('string' , 'char' , '>' ) : 'error',
            ('string' , 'char' , '<=' ) : 'error',
            ('string' , 'char' , '>=' ) : 'error',
            ('string' , 'char' , '!=' ) : 'bool',
            ('string' , 'char' , '|' ) : 'error',
            ('string' , 'char' , '&' ) : 'error',

            ('string' , 'string' , '+' ) : 'string',
            ('string' , 'string' , '-' ) : 'error',
            ('string' , 'string' , '*' ) : 'error',
            ('string' , 'string' , '/' ) : 'error',
            ('string' , 'string' , '=' ) : 'string', 
            ('string' , 'string' , '==' ) : 'bool',
            ('string' , 'string' , '<' ) : 'error',
            ('string' , 'string' , '>' ) : 'error',
            ('string' , 'string' , '<=' ) : 'error',
            ('string' , 'string' , '>=' ) : 'error',
            ('string' , 'string' , '!=' ) : 'bool',
            ('string' , 'string' , '|' ) : 'error',
            ('string' , 'string' , '&' ) : 'error',

            ('string' , 'dataframe' , '+' ) : 'error',
            ('string' , 'dataframe' , '-' ) : 'error',
            ('string' , 'dataframe' , '*' ) : 'error',
            ('string' , 'dataframe' , '/' ) : 'error',
            ('string' , 'dataframe' , '=' ) : 'error', 
            ('string' , 'dataframe' , '==' ) : 'error',
            ('string' , 'dataframe' , '<' ) : 'error',
            ('string' , 'dataframe' , '>' ) : 'error',
            ('string' , 'dataframe' , '<=' ) : 'error',
            ('string' , 'dataframe' , '>=' ) : 'error',
            ('string' , 'dataframe' , '!=' ) : 'error',
            ('string' , 'dataframe' , '|' ) : 'error',
            ('string' , 'dataframe' , '&' ) : 'error',

            #Dataframe
            ('dataframe' , 'int' , '+' ) : 'error',
            ('dataframe' , 'int' , '-' ) : 'error',
            ('dataframe' , 'int' , '*' ) : 'error',
            ('dataframe' , 'int' , '/' ) : 'error',
            ('dataframe' , 'int' , '=' ) : 'error', 
            ('dataframe' , 'int' , '==' ) : 'error',
            ('dataframe' , 'int' , '<' ) : 'error',
            ('dataframe' , 'int' , '>' ) : 'error',
            ('dataframe' , 'int' , '<=' ) : 'error',
            ('dataframe' , 'int' , '>=' ) : 'error',
            ('dataframe' , 'int' , '!=' ) : 'error',
            ('dataframe' , 'int' , '|' ) : 'error',
            ('dataframe' , 'int' , '&' ) : 'error',

            ('dataframe' , 'float' , '+' ) : 'error',
            ('dataframe' , 'float' , '-' ) : 'error',
            ('dataframe' , 'float' , '*' ) : 'error',
            ('dataframe' , 'float' , '/' ) : 'error',
            ('dataframe' , 'float' , '=' ) : 'error', 
            ('dataframe' , 'float' , '==' ) : 'error',
            ('dataframe' , 'float' , '<' ) : 'error',
            ('dataframe' , 'float' , '>' ) : 'error',
            ('dataframe' , 'float' , '<=' ) : 'error',
            ('dataframe' , 'float' , '>=' ) : 'error',
            ('dataframe' , 'float' , '!=' ) : 'error',
            ('dataframe' , 'float' , '|' ) : 'error',
            ('dataframe' , 'float' , '&' ) : 'error',

            ('dataframe' , 'char' , '+' ) : 'error',
            ('dataframe' , 'char' , '-' ) : 'error',
            ('dataframe' , 'char' , '*' ) : 'error',
            ('dataframe' , 'char' , '/' ) : 'error',
            ('dataframe' , 'char' , '=' ) : 'error', 
            ('dataframe' , 'char' , '==' ) : 'error',
            ('dataframe' , 'char' , '<' ) : 'error',
            ('dataframe' , 'char' , '>' ) : 'error',
            ('dataframe' , 'char' , '<=' ) : 'error',
            ('dataframe' , 'char' , '>=' ) : 'error',
            ('dataframe' , 'char' , '!=' ) : 'error',
            ('dataframe' , 'char' , '|' ) : 'error',
            ('dataframe' , 'char' , '&' ) : 'error',

            ('dataframe' , 'string' , '+' ) : 'error',
            ('dataframe' , 'string' , '-' ) : 'error',
            ('dataframe' , 'string' , '*' ) : 'error',
            ('dataframe' , 'string' , '/' ) : 'error',
            ('dataframe' , 'string' , '=' ) : 'error', 
            ('dataframe' , 'string' , '==' ) : 'error',
            ('dataframe' , 'string' , '<' ) : 'error',
            ('dataframe' , 'string' , '>' ) : 'error',
            ('dataframe' , 'string' , '<=' ) : 'error',
            ('dataframe' , 'string' , '>=' ) : 'error',
            ('dataframe' , 'string' , '!=' ) : 'error',
            ('dataframe' , 'string' , '|' ) : 'error',
            ('dataframe' , 'string' , '&' ) : 'error',

            ('dataframe' , 'dataframe' , '+' ) : 'error',
            ('dataframe' , 'dataframe' , '-' ) : 'error',
            ('dataframe' , 'dataframe' , '*' ) : 'error',
            ('dataframe' , 'dataframe' , '/' ) : 'error',
            ('dataframe' , 'dataframe' , '=' ) : 'dataframe', 
            ('dataframe' , 'dataframe' , '==' ) : 'error',
            ('dataframe' , 'dataframe' , '<' ) : 'error',
            ('dataframe' , 'dataframe' , '>' ) : 'error',
            ('dataframe' , 'dataframe' , '<=' ) : 'error',
            ('dataframe' , 'dataframe' , '>=' ) : 'error',
            ('dataframe' , 'dataframe' , '!=' ) : 'error',
            ('dataframe' , 'dataframe' , '|' ) : 'error',
            ('dataframe' , 'dataframe' , '&' ) : 'error',

            #Lectura
            ('lee', 'int', '') : 'int',
            ('lee', 'float', '') : 'float',
            ('lee', 'char', '') : 'error',
            ('lee', 'string', '') : 'error',
            ('lee', 'dataframe', '') : 'char', #?????

            #Escritura
            ('escribe', 'int', '') : 'string',
            ('escribe', 'float', '') : 'string',
            ('escribe', 'char', '') : 'string',
            ('escribe', 'string', '') : 'string',
            ('escribe', 'dataframe', '') : 'error',

            #Retorno
            ('regresa', 'int', '') : 'int',
            ('regresa', 'float', '') : 'float',
            ('regresa', 'char', '') : 'char',
            ('regresa', 'string', '') : 'string',
            ('regresa', 'dataframe', '') : 'dataframe'
        }

    '''
    Funcion para obtener el TIPO DE RESULTADO de la operacion con el operador entre dos operandos
    '''
    def getType(self, operando1, operando2, operador):
        return self.CuboSem[operando1, operando2, operador]

    