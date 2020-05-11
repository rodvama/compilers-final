# Jose Arturo Villalobos A00818214
# Rodrigo Valencia
# Diseno de compiladores

############################## Tabla de Variables ##############################
'''
La Tabla de Variables del Lenguaje COVID es reprsentado por un Diccionario.
Los atributos semanticos que contiene la tabla de variables son:
- nombre: nombre de la variable que se va a guardar
- tipo : tipo de la variable que se va a guardar
- renglones : Numero de renglones si es un arreglo
- columnas : Numero de columnas si es un arreglo
- memoria : Posicion de memoria

El formato sera: 
tabla_variables = {nombre: nombre, tipo, renglones, columnas}
'''

class TablaVars:
    
    '''
    Constructor para inicializar el diccionario tabla_variables
    '''
    def __init__(self):
        self.tabla_variables = {} 
        
    
    '''
    Funcion que verifica si una variable ya existe
    '''
    def var_exist(self, nombre):
        return nombre in self.tabla_variables.keys()

    '''
    Funcion para agregar una nueva variable a la tabla
    '''
    def var_add(self, nombre, tipo, renglones, columnas, memoria ):
        if self.var_exist(nombre):
            print("Error : Variable ", str(nombre), " duplicada")
            return False
        else:
            self.tabla_variables[nombre] = {
                'nombre' : nombre,
                'tipo': tipo,
                'renglones': renglones,
                'columnas' : columnas,
                'memoria' : memoria
            }
            return True

    '''
    Funcion que regresa todos los datos de una variable (si existe)
    '''
    def var_search(self, nombre):
        if self.var_exist(nombre):
            return self.tabla_variables[nombre]
        else:
            return None

    '''
    Funcion que regresa el el valor del atributo "Tipo" de la variable dada
    '''
    def var_searchType(self, nombre):
        if self.var_exist(nombre):
            return self.tabla_variables[nombre]['tipo']
        else:
            return None

    
    '''
    Funcion para indicar que una variable es dimensionada cambiando los valores de los atributos de renglones y columans
    '''
    def var_upadateDims(self, nombre, renglones, columnas):

        if self.var_exist(nombre):
            if columnas < 0: #Se actualizan solo renglones
                self.tabla_variables[nombre]['renglones'] = renglones
            else:
                self.tabla_variables[nombre]['columnas'] = columnas
                self.tabla_variables[nombre]['renglones']= renglones #?
            
            print("Dimensiones actualizadas de la variable: ", nombre)
            print("Renglones: ", self.tabla_variables[nombre]['renglones'], "Columnas: ", self.tabla_variables[nombre]['columnas'])

        else:
            print("Error. No es posible actializar las dimensaiones de una variable que no existe: ", nombre)

    
    '''
    Funcion que regresa la posicion de memoria virtual de la variable dada
    '''
    def var_searchMemPos(self, nombre):
        if self.var_exist(nombre):
            return self.tabla_variables[nombre]['memoria']
        else:
            return None
