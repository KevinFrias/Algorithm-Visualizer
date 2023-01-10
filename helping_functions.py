infinito = 1000000000

# Con la ayuda de la siguiente funcion creamos la lista de adyacencia de nuestro grafo
# Los parametros es la matrix de adyacencia que se pidio al usuario
# Para la lista de adyacencia se esta ocupando una tabla hash, en python se ocupa un diccionario
def crear_adjList(entrada):
    temp = entrada.split('\n')
    adj = {}

    for i in temp : 
        a = i.split('|')
        a[1] = a[1].split(' ')
        b = []

        for j in range (0, len(a[1])):
            if  a[1][j] == 'x' or a[1][j] == '-' : 
                b.append(infinito)
            else :
                b.append(int(a[1][j]))

        adj[a[0]] = b

    return adj 