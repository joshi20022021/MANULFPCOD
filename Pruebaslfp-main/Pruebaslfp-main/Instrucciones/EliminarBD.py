from Error.Errores import *
from Abstract.Abstract import Expression

class FuncionEliminarBD(Expression):
    def __init__(self, eliminar, nombre, igual, nueva, eliminar2, fila, columna):
        self.eliminar = eliminar
        self.nombre = nombre
        self.igual = igual
        self.nueva = nueva
        self.eliminar2 = eliminar2
        super().__init__(fila, columna)

    def operar(self, arbol):
        pass

    def ejecutarT(self):
        if self.eliminar == 'EliminarBD':
            if self.nombre != None:
                if self.igual == '=':
                    if self.nueva == 'nueva':
                        if self.eliminar2 == 'EliminarBD()':
                            return 'db.dropDatabase();'
                        else:
                            return 'Error: falta la palabra reservada EliminarBD()'
                    else:
                        return 'Error: Falta la palabra reservada nueva'
                else:
                    return 'Error: Falta el simbolo ='
            else:
                return 'Error: Falta el nombre de la base de datos a eliminar'
        else:
            return 'Error: Falta la palabra reservada EliminarDB'
        
    def getFila(self):
        return super().getFila()
    
    def getColumna(self):
        return super().getColumna()