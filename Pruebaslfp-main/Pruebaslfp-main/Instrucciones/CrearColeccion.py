from Error.Errores import *
from Abstract.Abstract import Expression

class FuncionCrearColeccion(Expression):
    def __init__ (self, crearcol, nombrecole, igual, nueva, crearcole2, nombree, fila, columna):
        self.crearcol = crearcol
        self.nombrecole = nombrecole
        self.igual = igual
        self.nueva = nueva
        self.crearcole2 = crearcole2
        self.nombree = nombree
        super().__init__(fila, columna)

    def operar(self, arbol):
        pass

    def ejecutarT(self):
        if self.crearcol == 'CrearColeccion':
            if self.nombrecole is not None:
                if self.igual == '=':
                    if self.nueva == 'nueva':
                        if self.crearcole2 == 'CrearColeccion(' + self.nombree + ')':
                            return 'db.createCollection("' + self.nombree + '");'
                        else:
                            return 'Error: falta la palabra reservada CrearColeccion()'
                    else:
                        return 'Error: Falta la palabra reservada nueva'
                else:
                    return 'Error: Falta el símbolo ='
            else:
                return 'Error: Falta el nombre de la colección'

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()
