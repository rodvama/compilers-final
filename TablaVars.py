# Jose Arturo Villalobos A00818214
# Rodrigo Valencia
# Diseno de compiladores
# Tabla de variables

class TablaVars:
    
    def __init__(self):
        '''
        Tabla de Variables
        diccionario = {nombre: nombre, tipo, renglones, columnas}
        nombre: nombre de la variable a guardar
        tipo : tipo de la variable a guardar
        renglones : Numero de renglones si es un arreglo
        columnas : Numero de columnas si es un arreglo
        '''
        self.diccionario = {} #Inicializa la tabla de variables
        
    
    '''
    Funcion para ver si la variable ya ha sido creada
    '''
    def var_exist(self, nombre):
        return nombre in self.diccionario.keys()

    '''
    Funcion para agregar una variable
    '''
    def var_add(self, nombre, tipo, renglones, columnas):
        #Verifica que el nombre de la variable no exista
        if self.var_exist(nombre):
            print("Error : Variable ", str(nombre), " duplicada")
            return False
        else:
            self.diccionario[nombre] = {
                'nombre' : nombre,
                'tipo': tipo,
                'renglones': renglones,
                'columnas' : columnas
            }
            return True

    '''
    Funcion que busca una variable en el diccionario y regresa su nombre y sus datos
    '''
    def var_search(self, nombre):
        if self.var_exist(nombre):
            return self.diccionario[nombre]
        else:
            return None

    '''
    Funcion que regresa el tipo de una variable del diccionario
    '''
    def var_searchType(self, nombre):
        if self.var_exist(nombre):
            return self.diccionario[nombre]['tipo']
        else:
            return None

    
    # '''
    # Funcion para actualizar renglones y columnas de una variable que es arreglo y ya esta creada
    # '''
    # def var_upadateDims(self, nombre, renglones, columnas):

    #     if self.var_exist(nombre):
    #         if columnas < 0: #Se actualizan solo renglones
    #             self.diccionario[nombre]['renglones'] = renglones
    #         else:
    #             self.diccionario[nombre]['columnas'] = columnas
    #             self.diccionario[nombre]['renglones']= renglones #?
            
    #         print("Dimensiones actualizadas de la variable: ", nombre)
    #         print("Renglones: ", self.diccionario[nombre]['renglones'], "Columnas: ", self.diccionario[nombre]['columnas'])

    #     else:
    #         print("Error. No es posible actializar las dimensaiones de una variable que no existe: ", nombre)

    
    # '''
    # Funcion que busca y regresa la posicion de memoria de una variables
    # '''
    # def var_searchMemPos(self, nombre):
    #     if self.var_exist(nombre):
    #         return self.diccionario[nombre]['posMem']
    #     else:
    #         return None
