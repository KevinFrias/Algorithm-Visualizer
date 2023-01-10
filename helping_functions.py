infinito = 1000000000

# Con la ayuda de la siguiente funcion limpiamos la entrada del usuario para la construcción del grafo
# Primero separamos renglon por renglon
# Luego identificamos el nodo origen en cada renglon y las conexiones que tiene con cada otro nodo

def limpiar_entrada(entrada):
    temp = entrada.split('\n')
    adj = {}

    for i in temp : 
        a = i.split('|')
        a[1] = a[1].split(' ')
        b = []

        for j in range (0, len(a[1])):
            # Si no hay camino o algun lazo, usamos una varible la cual no tomaremos en cuenta
            if  a[1][j] == 'x' or a[1][j] == '-' : 
                b.append(infinito)
            else :
                b.append(int(a[1][j]))


        # Para poder tener multiples valores dentro de una llave hacemos uso de una lista
        adj[int(a[0])] = b

    return adj 