from Abstract.Abstract import Expression

class Numero(Expression):
    def __init__(self, valor, fila, columna) -> None:
        self.valor = valor
        super().__init__(fila, columna)

    def getValor(self):
        return self.valor
    
    def getFila(self):
        return super().getfila()
    
    def getColumna(self):
        return super().getColumna()
    
    def operar(self, arbol):
        return super().operar(arbol)