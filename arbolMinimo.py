import helping_functions as hf

def find_parent(parent, node):
    if parent[node] == node:
        return node

    parent[node] = find_parent(parent, parent[node])

    return parent[node]

def conseguir_camino(graph):

    ordenado = hf.ordenar_grafo_increasing(graph)
    nodos = set()

    for k, v in ordenado.items():
        for arista in v :
            nodos.add(arista[0])
            nodos.add(arista[1])

    cantidad_nodos = len(nodos)

    # Para cada nodo decimos que su padre es el mismo al iniciar, es su propia componente
    parents = {}
    for node in nodos :
        parents [node] = node

    cantidad_aristas = 0
    resultado = []
    pesos = []


    # Entonces para tener el árbol mínimo de expansión sabemos que debe tener n-1 cantidad de aristas que de nodos
    # es por eso que ponemos esa condición dentro del while

    while cantidad_aristas < cantidad_nodos - 1 :
        # Recorremos item por item dentro de nuestro dictionario
        for weight, aristas in ordenado.items() :
            for arista in aristas :
                origen = arista[0]
                destino = arista[1]
                peso = weight

                # Para cada arista, buscamos cual es el padre de ese nodo, 
                padre_destino = find_parent(parents, destino)
                padre_origen = find_parent(parents, origen)

            # Si el padre para ambos nodos no es el mismo, entonces agregamos esa arista a nuestra
            # respuesta, en caso contrario, si es el mismo tendriamos un ciclo por lo que no formaría parte de la respuesta
            if (padre_destino != padre_origen) :
                cantidad_aristas += 1
                resultado.append(arista)
                pesos.append(weight)

                # Actualizamos el padre del nodo origen que acabamos de checar
                parents[padre_origen] = padre_destino

    return resultado,pesos