def obtener_tabla(y, x, tabla):
    respuesta = 0

    if (x == len(tabla[0]) - 1 and y == len(tabla) - 1 ):
        return -1,-1, tabla, 0

    # (0,0) | (0,1) | (0,2) | (0,3)
    # (1,0)
    # (2,0)

    min1 = min(tabla[len(tabla)-1][x], tabla[y][len(tabla[0]) -1])

    respuesta = tabla[y][x] * min1

    tabla[len(tabla)-1][x] -= min1
    tabla[y][len(tabla[0])-1] -= min1

    if (tabla[len(tabla)-1][x] == 0):
        for i in range(0, len(tabla)) :
            tabla[i][x] = 0
        x += 1


    if (tabla[y][len(tabla[0])-1] == 0):
        for i in range(0, len(tabla[0])) :
            tabla[y][i] = 0
        y += 1

    return x, y, tabla, respuesta

