# Para el conseguir la respuesta que se requiere lo que se hace es correr el algoritmo de busqueda en
# profundidad (DFS) para conseguir todos los caminos de

def obtener_camino(graph, start, end, path = [], weight = 1000000, visited=set()):
    if start == end:
        return path, weight

    visited.add(start)

    for neighbor, w in graph[start]:
        
        print(graph[start])

        if neighbor not in visited:
            visited.add(neighbor)
            new_path, min_weight = obtener_camino(graph, neighbor, end, path + [(start, neighbor)], min(weight, w), visited)

            if (new_path) :
                return new_path, min_weight

    return [], -1


def completo(graph, inicio, final):

    caminos = []

    while (True) :

        print('asjdbajksb')
        camino, peso_minimo = obtener_camino(graph, inicio, final)

        if (peso_minimo == -1) :
            break
        else:
            print(camino, ' - ', peso_minimo)
            print()

            caminos.append((camino, peso_minimo))

            for u,v in camino :
                temp = graph[u]
                new_data = []

                for dest, w in temp :
                    if (dest == v) :

                        w = w - peso_minimo
                        if (w) : 
                            new_data.append((dest, w))
                    else :
                        new_data.append((dest,w))

                graph[u] = new_data


            for k,v in graph.items() :
                print (k, ' : ', v)



    return caminos
