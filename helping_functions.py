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
            if  a[1][j] != 'x' and a[1][j] != '-' : 
                b.append((j+1, int(a[1][j])))

        indice = int(a[0])
        adj[indice] = b

    return adj 