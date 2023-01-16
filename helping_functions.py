# Con la ayuda de la siguiente funcion limpiamos la entrada del usuario para la construcción del grafo
# Primero separamos renglon por renglon
# Luego identificamos el nodo origen en cada renglon y las conexiones que tiene con cada otro nodo
# Para poder pasarlo dentro de una tabla hash, que esta en la llave tiene las conexiones entre los nodos, y su valor es el peso de estas

def limpiar_entrada(entrada):
    temp = entrada.split('\n')
    adj = {}

    for i in temp : 
        a = i.split('|')
        a[1] = a[1].split(' ')
        b = []

        for j in range (0, len(a[1])):
            # Si no hay camino o algun lazo, usamos una varible la cual no tomaremos en cuenta
            if  len(a[1][j]) and a[1][j].isnumeric() : 
                b.append((j+1, int(a[1][j])))

        indice = int(a[0])
        adj[indice] = b

    return adj 

def ordenar_grafo_increasing(graph) :
    # Primero creamos un diccionario para poder acomodar los datos de manera que
    # la llave sea el peso y los valores, las aristas
    resultado = {}

    for u,value in graph.items():
        for v, w in value :
            if w in resultado.keys():
                temp = resultado[w]
                if ((u,v) not in temp and (v, u) not in temp) :
                    temp.append((u,v))
                resultado[w] = temp
            else :
                temp = []
                temp.append((u,v))
                resultado[w] = temp

    # Creo una lista con los pesos del grafo y la ordeno
    # despues se recorre el diccionario por los indices ordenados y se autoasigna
    myKeys = list(resultado.keys())
    myKeys.sort()
    resultado = {i: resultado[i] for i in myKeys}

    return resultado


def limpiar_tabla(entrada):
    temp = entrada.split('\n')
    respuesta = []

    for i in temp :
        a = i.split(' ')
        b = []
        for j in a :
            b.append(int(j))

        respuesta.append(b)

    return respuesta


def limpiar_tabla_coste(entrada):
    temp = entrada.split('\n')
    respuesta = []

    for i in range (len(temp) -1):
        a = temp[i].split(' ')
        for j in range (len(a) - 1) :
            respuesta.append( (int(a[j]),i, j))

    respuesta  = sorted(respuesta, key=lambda x: x[0], reverse=False)

    return respuesta