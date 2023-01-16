def obtener_tabla(x, y, last_x, last_y, tabla):
    respuesta = 0

    if (last_x == len(tabla[0]) - 1 and last_y == len(tabla) - 1 ):
        return -1,-1,-1,-1, tabla, 0


    min1 = min(tabla[last_x][len(tabla) - 1], tabla[len(tabla[0]) - 1][last_y])

    respuesta = tabla[x][y] * min1

    tabla[last_x][len(tabla) - 1] -= min1
    tabla[len(tabla[0]) - 1][last_y] -= min1

    if (tabla[len(tabla[0]) - 1][last_y] == 0):
        for i in range(0, len(tabla[0])) :
            tabla[i][last_y] = 0

        y += 1
        last_y += 1

    if (tabla[last_x][len(tabla) - 1] == 0):
        for i in range(0, len(tabla)) :
            tabla[last_x][i] = 0

        x += 1
        last_x += 1

    return x, y, last_x, last_y, tabla, respuesta

