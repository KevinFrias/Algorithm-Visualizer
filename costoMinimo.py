def paso_siguiente(y, x, tabla, elementos):

    respuesta = 0

    min1 = min(tabla[len(tabla)-1][x], tabla[y][len(tabla[0]) -1])

    if (len(elementos) == 0) :
        return -1, tabla, elementos

    respuesta = tabla[y][x] * min1

    tabla[len(tabla)-1][x] -= min1
    tabla[y][len(tabla[0])-1] -= min1

    # (0,0) | (0,1) | (0,2) | (0,3)
    # (1,0)
    # (2,0)


    if (tabla[y][len(tabla[0])-1] == 0) :
        for i in range(0, len(tabla[0])) :
            tabla[y][i] = 0
        
        temp = []
        for i in elementos :
            if (i[1] != y) :
                temp.append(i)

        elementos = temp



    if (tabla[len(tabla)-1][x] == 0) :
        for i in range(0, len(tabla)) :
            tabla[i][x] = 0

        temp = []
        for i in elementos :
            if (i[2] != x) :
                temp.append(i)

        elementos = temp

    return tabla, elementos, respuesta
        