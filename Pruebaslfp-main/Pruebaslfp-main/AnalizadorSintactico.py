from Abstract.Lexema import *
from Error.Errores import *
from Instrucciones.Funcion import *
from Instrucciones.EliminarBD import FuncionEliminarBD
from Instrucciones.CrearColeccion import FuncionCrearColeccion

global n_lineas
global n_columnas
global instrucciones
global lista_lexemas
global lista_errores

n_lineas = 1
n_columnas = 1
lista_lexemas = []
instrucciones = []
lista_errores = []

def instruccion(cadena):
    global n_lineas
    global n_columnas
    global lista_lexemas
    lexema = ''
    puntero = 0 

    while cadena:
        char = cadena[puntero]
        puntero += 1

        if char.isupper() or char.islower():
            lexema, cadena = armar_lexema(cadena)
            if lexema and cadena:
                n_columnas += 1
                l = Lexema(lexema, n_lineas, n_columnas)
                lista_lexemas.append(l)
                n_columnas += len(lexema) + 1
                puntero = 0

        elif char == '=':
            c = Lexema(char, n_lineas, n_columnas)
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0
            n_columnas += 1

        elif char == '\t':
            n_columnas += 4
            cadena = cadena[4:]
            puntero = 0

        elif char == '\n':
            cadena = cadena[1:]
            puntero = 0
            n_lineas += 1
            n_columnas = 1

        elif char == ' ' or char == '\r':
            n_columnas += 1
            cadena = cadena[1:]
            puntero = 0

        else: 
            lista_errores.append(Errores(char, "Lexico", n_lineas, n_columnas))
            cadena = cadena[1:]
            puntero = 0
            n_columnas += 1

    return lista_lexemas 

def armar_lexema(cadena):
    global n_lineas
    global n_columnas
    global lista_lexemas
    lexema = ''
    puntero = ''

    for char in cadena:
        puntero += char
        if char == ' ' or char == ';':
            return lexema, cadena[len(puntero):]
        else:
            lexema += char
    return None, None

def operar():
    global lista_lexemas
    global instrucciones

    while lista_lexemas:
        lexema = lista_lexemas.pop(0)
        if lexema.operar(None) == 'CrearBD':
            nombredb = lista_lexemas.pop(0)
            igualdb = lista_lexemas.pop(0)
            nuevadb = lista_lexemas.pop(0)
            crearbd2 = lista_lexemas.pop(0)
            func = Funcion(lexema.lexema, nombredb.lexema, igualdb.lexema, nuevadb.lexema, crearbd2.lexema, lexema.getFila(), lexema.getColumna())
            return func
        
        elif lexema.operar(None) == 'EliminarBD':
            nombreel = lista_lexemas.pop(0)
            igualel = lista_lexemas.pop(0)
            nuevael = lista_lexemas.pop(0)
            eliminarel = lista_lexemas.pop(0)
            func = FuncionEliminarBD(lexema.lexema, nombreel.lexema, igualel.lexema, nuevael.lexema, eliminarel.lexema, lexema.getFila(), lexema.getColumna())
            return func
        
        elif lexema.operar(None) == 'CrearColeccion':
            nombrecol = lista_lexemas.pop(0)
            igualcol = lista_lexemas.pop(0)
            nuevacol = lista_lexemas.pop(0)
            crearcol2 = lista_lexemas.pop(0)
            nombree = lista_lexemas.pop(0)
            func = FuncionCrearColeccion(lexema.lexema, nombrecol.lexema, igualcol.lexema, nuevacol.lexema, crearcol2.lexema, nombree.lexema, lexema.getFila(), lexema.getColumna())
            return func
        
    return None

def operar_():
    global instrucciones
    temp_instrucciones = []
    while True:
        operacion = operar()
        if operacion:
            temp_instrucciones.append(operacion)
        else:
            break
    instrucciones = temp_instrucciones
    return instrucciones

def getErrores():
    global lista_errores
    return lista_errores
