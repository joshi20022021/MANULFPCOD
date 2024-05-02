import pandas as pd
from Abstract.Lexema import *
from Error.Errores import *

reserved = {
    'RCREARBD':             'CrearBD',
    'ELIMINARBD':           'EliminarBD',
    'RCREARCOLECCION':      'CrearColeccion',
    'ELIMINARCOLECCION':    'EliminarColeccion',
    'RINSERTARUNICO':       'InsertarUnico',
    'RACTUALIZARUNICO':     'ActualizarUnico',
    'RELIMINARUNICO':       'EliminarUnico',
    'RBUSCARTODO':          'BuscarTodo',
    'RBUSCARUNICO':         'BuscarUnico',
    'PUNTOYCOMA':           ';',
    'COMILLAIZQ':           '"',
    'COMILLADER':           '"',
    'DOSPUNTOS':            ':',
    'LLAVEIZQ':             '{',
    'LLAVEDER':             '}',
    'COMA':                 ',',
    'CORCHETEIZQ':          '[',
    'CORCHETEDER':          ']',
    'IGUAL':                '=',
    'PARIZQ':               '(',
    'PARDER':               ')',
}

palabras_reservadas = list(reserved.values())
global n_lineas
global n_columnas
global lista_lexemas
global lista_errores
global instrucciones

n_lineas = 1
n_columnas = 1
lista_lexemas = []
lista_errores = []
instrucciones = []


def analizador_lexico(cadena):
    lista_lexemas = []
    lista_errores = []
    n_lineas = 1
    n_columnas = 1
    lexema = ''
    puntero = 0
    entre_comillas = False

    while puntero < len(cadena):
        char = cadena[puntero]
        if char == '\n':
            n_lineas += 1
            n_columnas = 1
            puntero += 1
        elif char == ' ':
            if entre_comillas:
                lexema += char
            else:
                if lexema:
                    lista_lexemas.append(Lexema(lexema, n_lineas, n_columnas - len(lexema)))
                    lexema = ''
                else:
                    lista_errores.append(Errores(char, "error", n_lineas, n_columnas))
                n_columnas += 1
            puntero += 1
        elif char == '\"':
            lexema += char
            entre_comillas = not entre_comillas
            lista_lexemas.append(Lexema(lexema, n_lineas, n_columnas - len(lexema)))
            puntero += 1
        elif char in reserved.values():
            if lexema:
                lista_lexemas.append(Lexema(lexema, n_lineas, n_columnas - len(lexema)))
                lexema = ''
            lista_lexemas.append(Lexema(char, n_lineas, n_columnas))
            n_columnas += 1
            puntero += 1
        else:
            if entre_comillas:
                if not char.isalpha():
                    lista_errores.append(Errores(char, "error", n_lineas, n_columnas))
            if char != '\r':  # No agregue el carácter '\r' al lexema
                lexema += char
            n_columnas += 1
            puntero += 1

    # Agregar el último lexema que quedó en el buffer
    if lexema:
        lista_lexemas.append(Lexema(lexema, n_lineas, n_columnas - len(lexema)))

    return lista_lexemas, lista_errores

def generar_tabla_tokens_html(lista_lexemas):
    data_lexemas = {
        "Token": [lexema.lexema for lexema in lista_lexemas],
        "Tipo": [get_token_type(lexema.lexema) for lexema in lista_lexemas],
        "Fila": [lexema.fila for lexema in lista_lexemas],
        "Columna": [lexema.columna for lexema in lista_lexemas]
    }
    df_lexemas = pd.DataFrame(data_lexemas)

    styles = """
    <style>
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th {
        background-color: #4CAF50;
        color: white;
    }
    th, td {
        text-align: left;
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }
    tr:hover {background-color: #f5f5f5;}
    </style>
    """

    with open("tabla_lexemas.html", "w") as file:
        file.write(styles)
        file.write("<h1>Lexemas</h1>")
        file.write(df_lexemas.to_html(index=False))

def generar_tabla_errores_html(lista_errores):
    lista_errores_cleaned = []
    for error in lista_errores:
        if '\r' in error.lexema:
            error.lexema = error.lexema.replace('\r', '')
        lista_errores_cleaned.append(error)

    data_errores_cleaned = {
        "Caracter": [error.lexema for error in lista_errores_cleaned],
        "Tipo": [get_token_type(error.lexema) for error in lista_errores_cleaned],
        "Fila": [error.fila for error in lista_errores_cleaned],
        "Columna": [error.columna for error in lista_errores_cleaned]
    }
    df_errores_cleaned = pd.DataFrame(data_errores_cleaned)

    styles = """
    <style>
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th {
        background-color: #4CAF50;
        color: white;
    }
    th, td {
        text-align: left;
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }
    tr:hover {background-color: #f5f5f5;}
    </style>
    """

    with open("tabla_errores.html", "w") as file:
        file.write(styles)
        file.write("<h1>Errores</h1>")
        file.write(df_errores_cleaned.to_html(index=False))

def get_token_type(token):
    if token in ['CrearDB', 'EliminarDB', 'CrearColeccion', 'EliminarColeccion', 'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']:
        return "Palabra reservada"
    elif token in [';', '"', ':', '{', '}', ',', '[', ']', '=', '(', ')']:
        return "Simbolo"
    else:
        return "Identificador"