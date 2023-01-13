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
        respuesta.append(i.split(' '))

    return respuesta

    respuesta_transverse = {}
    temp2 = []

    for i in range(0, len(respuesta[0])) :
        b = []
        for j in range (0, len(respuesta)) :
            b.append(respuesta[j][i])
        respuesta_transverse[i] = b
        temp2.append(b)

    return temp2

def imprimir_tabla (tabla):

    for i in range (0, len(tabla)):
        for j in range (0, len(tabla[i])):
                if (j == len(tabla[i]) - 1) :
                    print ('  | ', end = ' ')
                print (tabla[i][j], end = ' ')

        if (i == len(tabla[i]) - 2) :
            print()
            for x in range (0, len(tabla[i])):
                print ('-', end= '')

        print()



def esquina_noroeste(tabla):
    x, y = 0,0
    respuesta = 0

    imprimir_tabla(tabla)

    last_x = len(tabla[0]) - 1
    last_y = len(tabla) - 1


