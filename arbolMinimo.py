import helping_functions as hf

def conseguir_camino(graph):

    ordenado = hf.ordenar_grafo_increasing(graph)

    nodos = set()
    camino = []
    pesos = []

    for k, v in ordenado.items():
        for arista in v :
            # Para poder agregar una arista a nuestro árbol mínimo sin que se teng algún ciclo
            # necesitamos hacer un nand con ambos nodos de la arista y si existen ambos no lo agregamos
            if  (not (arista[0] in nodos and arista[1] in nodos)) :
                # Agregamos a nuestro set de nodos, los nodos que vamos a ocupar en nuestro árbol
                nodos.add(arista[0])
                nodos.add(arista[1])
                camino.append(arista)

                pesos.append(k)


    return camino,pesos