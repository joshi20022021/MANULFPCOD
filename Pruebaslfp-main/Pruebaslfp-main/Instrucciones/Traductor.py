def traducir_a_mongodb(texto):
    lineas = texto.split('\n')
    resultado = []

    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith('---'):
            continue
        
        if linea.startswith('CrearBD'):
            nombre = linea.split()[1]
            resultado.append(f'db = use("{nombre}");')
        elif linea.startswith('EliminarBD'):
            nombre = linea.split()[1]
            resultado.append(f'db.dropDatabase("{nombre}");')
        elif linea.startswith('CrearColeccion'):
            nombre = linea.split('"')[1]
            resultado.append(f'db.createCollection("{nombre}");')
        elif linea.startswith('EliminarColeccion'):
            nombre = linea.split('"')[1]
            resultado.append(f'db.{nombre}.drop();')
        elif linea.startswith('InsertarUnico'):
            partes = linea.split('(', 1)[1].split(')', 1)[0].split(',', 1)
            nombre_coleccion = partes[0].strip().strip('"')
            datos_json = partes[1].strip() if len(partes) > 1 else ''
            resultado.append(f'db.{nombre_coleccion}.insertOne({datos_json});')
        elif linea.startswith('ActualizarUnico'):
            partes = linea.split('(', 1)[1].split(')', 1)[0].split(',', 1)
            nombre_coleccion = partes[0].strip().strip('"')
            filtro = partes[1].strip().split(',')[0].strip() if len(partes) > 1 else ''
            cambio = partes[1].strip().split(',')[1].strip() if len(partes) > 1 and len(partes[1].strip().split(',')) > 1 else ''
            resultado.append(f'db.{nombre_coleccion}.updateOne({filtro}, {cambio});')
        elif linea.startswith('EliminarUnico'):
            partes = linea.split('(', 1)[1].split(')', 1)[0].split(',', 1)
            nombre_coleccion = partes[0].strip().strip('"')
            filtro = partes[1].strip() if len(partes) > 1 else ''
            resultado.append(f'db.{nombre_coleccion}.deleteOne({filtro});')
        elif linea.startswith('BuscarTodo'):
            nombre_coleccion = linea.split('"')[1]
            resultado.append(f'db.{nombre_coleccion}.find();')
        elif linea.startswith('BuscarUnico'):
            nombre_coleccion = linea.split('"')[1]
            resultado.append(f'db.{nombre_coleccion}.findOne();')

    return '\n'.join(resultado)
