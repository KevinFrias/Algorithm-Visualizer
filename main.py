import tkinter as tk
from tkinter import ttk

import helping_functions as hf
import arbolMinimo
import flujo
import esquinaNoroeste
import costoMinimo

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

import sys
import atexit
import threading
import time

## Algoritmos a incluir : 
## > Flujo maximo
## > Prim or Kruskal

# Creamos la ventana de la aplicacion
window = tk.Tk()
window.title("Visualización")
window.geometry("800x600")
#window.resizable(False, False)

# Declaramos la varaibles necesarias para poder dibujar el grafo
fig, ax = plt.subplots()

def limpiar_pantalla():
    # Limpiamos la pantalla
    for widgets in window.winfo_children():
        widgets.destroy()
    
     # Limpiamos la figura en pantalla
    ax.clear()
    fig.clear()

def dibujar_grafo(adj, inicial, final):
    G = nx.Graph()
    
    for k,v in adj.items() :
        for i in v :
            G.add_edge(k,i[0], weight=i[1])

    # La siguiente linea nos ayuda a medir la distancia entre nodo y nodo, esto nos ayuda posteriormente a mantener en su lugar geometrico
    # la posicion de toda la información del grafo y poder modificarlo
    position_graph = nx.spring_layout(G)

    widths = [2 for u,v in G.edges()]
    node_colors = ['blue' if n == inicial or n == final else '#C7C7C7' for n in G.nodes()]
    node_sizes = [800 for n in G.nodes()]
    labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, position_graph, with_labels=True, font_weight='bold', width=widths, node_size=node_sizes, node_color=node_colors)
    nx.draw_networkx_edge_labels(G, position_graph, edge_labels=labels, font_size=11)

    # create a FigureCanvasTkAgg widget para poder mostrar correctamente el grafo
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    return G,canvas, position_graph

def mostar_grafo(adj, inicial, final, opcion):
    # En caso de que no haya ningun dato cuando se pide el nodo inicial y final, cerramos completamente el programa
    if (len(inicial) == 0 or len(final) == 0) :
        window.destroy()
        return ''

    inicial = int(inicial)
    final = int(final)

    # Limpiamos la pantalla para poder mostrar toda la información necesaria (El grafo, botones para mostar los pasos del algoritmo y la respuesta)
    limpiar_pantalla()

    graph, canvas, position_graph = dibujar_grafo(adj, inicial, final)

    # Creamos un boton para volver al menu principal
    volver_boton = tk.Button(window, width=30, height=3, text="Volver", command=mostrar_menu)
    volver_boton.pack(side=tk.LEFT, expand=True)

    # Al momento de presionar cualquiera de los botones los quitamos e iniciamos con el algoritmo
    if opcion == 1 :
        button3 = tk.Button(window, width=30, height=3, text="Iniciar", command=lambda: (volver_boton.pack_forget(), button3.pack_forget(), iniciar_flujo_maximo(graph, canvas, position_graph, adj, inicial, final)))
        button3.pack(side=tk.LEFT, expand=True)
    else :
        button3 = tk.Button(window, width=30, height=3, text="Iniciar", command=lambda: (volver_boton.pack_forget(), button3.pack_forget(), iniciar_arbol_minimo(graph, canvas, position_graph, adj, inicial, final)))
        button3.pack(side=tk.LEFT, expand=True)




def mostrar_componente_arbol(adj, G, canvas, position_graph, nodos_visited, edges_visited):

    # Limpiamos la figura en pantalla
    ax.clear()
    fig.clear()

    # En la siguiente para de lineas cambiamos el color de los nodos y aristas dependiendo de varias condiciones
    node_colors = ['#7e6cff' if (n in nodos_visited) else  '#8D8D8D' for n in G.nodes()]
    edge_colors = ['#7e6cff' if (u,v) in edges_visited or (v,u) in edges_visited else '#8D8D8D' for u,v in G.edges()]

    # Asignamos un tamaño para los nodos
    node_sizes = [800 for n in G.nodes()]

    # Asignamos un tañano para las aristas
    widths = [3 if (u,v) in edges_visited or (v,u) in edges_visited else 2 for u,v in G.edges()]
    labels = nx.get_edge_attributes(G, 'weight')

    # Dibujamos el grafo y pasando como parametro toda la información necesaria para su representacion
    nx.draw(G, position_graph, with_labels=True, font_weight='bold', edge_color=edge_colors, node_color=node_colors, width= widths, node_size=node_sizes)
    nx.draw_networkx_edge_labels(G, position_graph, edge_labels=labels, font_size=11)

    canvas.draw()
    canvas.get_tk_widget().update()

def iniciar_arbol_minimo(graph, canvas, position_graph, adj, inicial, final) :

    path, pesos = arbolMinimo.conseguir_camino(adj)

    # Etiqueta donde mostraremos el resultado conforme vayamos tomando cada nodo
    Resultado_arbol = tk.Label(height = 3, text = "Resultado : 0 ", font='helvetica 14')
    Resultado_arbol.pack(side=tk.RIGHT, expand=True)

    nodos_visited = []
    edges_visited = []

    indice = 0
    resultado_algoritmo = 0

    for arista in path :
        edges_visited.append(arista)

        if (arista[0] not in nodos_visited):
            nodos_visited.append(arista[0])

        if (arista[1] not in nodos_visited):
            nodos_visited.append(arista[1])

        mostrar_componente_arbol(adj, graph, canvas, position_graph, nodos_visited, edges_visited)

        resultado_algoritmo += pesos[indice]
        
        Resultado_arbol.config(text = "Resultado : " + str(resultado_algoritmo))
        Resultado_arbol.update()
        indice += 1

        time.sleep(1.5)


    # Creamos y ponemos en pantalla un boton para volver al menu principal
    volver_boton = tk.Button(window, width=35, height=3, text="Volver", command=mostrar_menu)
    volver_boton.pack(side=tk.LEFT, expand=True)

    # Mostramos el resultado final en color rojo y una fuente más grande
    Resultado_arbol.config(text = "Resultado : " + str(resultado_algoritmo), foreground="red",  font='helvetica 20')



def mostrar_camino_flujo(G, canvas, valor_minimo, camino_actual, inicial, final, position_graph):

    # Creamos un par de listas que nos ayudaran a saber por que aristas y nodos hemos pasado para poder cambiar su color correctamente
    pasados  = []
    arista_pasada = []

    for i in camino_actual :
        # Limpiamos la figura en pantalla
        ax.clear()
        fig.clear()

        # Agregamos los nodos que estamos ocuando 
        pasados.append(i[0])
        pasados.append(i[1])

        # Agregamos la arista que ocupamos
        arista_pasada.append((i))

        # En la siguiente para de lineas cambiamos el color de los nodos y aristas dependiendo de varias condiciones
        node_colors = ['blue' if n == inicial or n == final else 'red' if n in pasados else '#E9E9E9' for n in G.nodes()]
        edge_colors = ['red' if (u,v) in arista_pasada or (v,u) in arista_pasada else '#F3F3F3' if G[u][v]['weight'] == 0 else 'black'   for u,v in G.edges()]

        # Asignamos un tamaño para los nodos
        node_sizes = [800 for n in G.nodes()]

        # Asignamos un tañano para las aristas
        widths = [3 if (u,v) == i or (v,u) == i else 2 for u,v in G.edges()]
        labels = nx.get_edge_attributes(G, 'weight')

        # Dibujamos el grafo y pasando como parametro toda la información necesaria para su representacion
        nx.draw(G, position_graph, with_labels=True, font_weight='bold', edge_color=edge_colors, node_color=node_colors, width= widths, node_size=node_sizes)
        nx.draw_networkx_edge_labels(G, position_graph, edge_labels=labels, font_size=11)

        canvas.draw()
        canvas.get_tk_widget().update()

        time.sleep(1.7)

    # Despues que mostramos el camino se tiene que cambiar el peso de las aristas del camino recorrido
    weights = nx.get_edge_attributes(G,'weight')
    for u,v in weights:
        if (u,v) in camino_actual or (v,u) in camino_actual :
            weights[(u,v)] -= valor_minimo
    
    nx.set_edge_attributes(G, weights, 'weight')

    return G

def iniciar_flujo_maximo (graph, canvas, position_graph, adj, inicial, final) :
    # Obtenemos todos lo caminos que tenemos que seguir
    caminos = flujo.completo(adj, inicial, final)

    # Etiqueta que nos ayudara para mostrar el valor minimo del camino que se tomó
    Info = tk.Label(height = 3, text = "", font='helvetica 14')
    Info.pack(side=tk.LEFT, expand=True)

    # Etiqueta donde mostraremos el resultado del algoritmo camino por camino
    Resultado_flujo = tk.Label(height = 3, text = "Resultado : 0", font='helvetica 14')
    Resultado_flujo.pack(side=tk.RIGHT, expand=True)

    # La siguiente variable nos ayudara a mostrar el resultado 
    resultado_algoritmo = 0

    # Mostramos todos los caminos del algoritmo
    for i in range (0, len(caminos)):
        Info.config(text= "")

        actual = caminos[i]

        # Obtenemos el camino actual y el valor minimo de este
        camino_actual = actual[0]
        valor_minimo = actual[1]

        # Mostramos el camino seguido en pantalla
        graph = mostrar_camino_flujo(graph, canvas, valor_minimo, camino_actual,inicial, final, position_graph)

        # Agregamos el valor mínimo del camino a la respuesta final
        resultado_algoritmo += valor_minimo

        # Mostramos la informacion relevante al camino que se tomó
        Info.config(text = "Valor minimo : " + str(valor_minimo))
        Resultado_flujo.config(text = "Resultado : " + str(resultado_algoritmo))

        # Hacemos una actualizacion de los datos 
        Info.update()
        Resultado_flujo.update()

        # Ponemos un pequeño delay entre camino y camino
        time.sleep(1)


    # Mostramos el camino final del algoritmo
    mostrar_camino_flujo(graph, canvas,  0, [(inicial, inicial)], inicial, final, position_graph) 

    # Al ya no mostrar el valor mínimo del camino se quita la etiqueta
    Info.destroy()

    # Creamos y ponemos en pantalla un boton para volver al menu principal
    volver_boton = tk.Button(window, width=35, height=3, text="Volver", command=mostrar_menu)
    volver_boton.pack(side=tk.LEFT, expand=True)

    # Mostramos el resultado final en color rojo y una fuente más grande
    Resultado_flujo.config(text = "Resultado : " + str(resultado_algoritmo), foreground="red",  font='helvetica 20')


def dibuja_tabla(data, a , b, ancho) :

    for x in range(len(data)):
        for y in range(len(data[x])):
            frameGrid = tk.Frame(window, relief=tk.RIDGE, borderwidth=3)
            frameGrid.grid(row=x, column=y, padx=(10,10), pady=(10,20))

            if (x == a and b == y) :
                labelGrid = tk.Label(master=frameGrid, text=f"{data[x][y]}", width=ancho, height=1, bg= "#FF3C3C", font='helvetica 14')
            else :
                if (data[x][y] == 0) :
                    labelGrid = tk.Label(master=frameGrid, text=f"{data[x][y]}", width=ancho, height=1, bg= "#323434", font='helvetica 14')
                else :
                    if (x == len(data) - 1) :
                        labelGrid = tk.Label(master=frameGrid, text=f"{data[x][y]}", width=ancho, height=1, bg= "#A0C0D0", font='helvetica 14')
                    else :
                        if (y == len(data[x]) - 1) :
                            labelGrid = tk.Label(master=frameGrid, text=f"{data[x][y]}", width=ancho, height=1, bg= "#A0C0D0", font='helvetica 14')
                        else :
                            labelGrid = tk.Label(master=frameGrid, text=f"{data[x][y]}", width=ancho, height=1, font='helvetica 14')

            labelGrid.pack()

def iniciar_esquina_noroeste(input):
    # Limpiamos pantalla para poder mostrar todos lo datos de la tabla
    limpiar_pantalla()

    # Hacemos formato de los datos ingresados del usuario para un mejor manejo
    data = hf.limpiar_tabla(input)
    
    # Establecemos el tamaño que va a tomar cada celda de la tabla
    ancho = (800//len(data[0]))//16

    a, b = 0, 0
    respuesta = 0

    # El algoritimo se ejecuta hasta que se tenga un siguiente paso
    while (a != -1 and b != -1) :
        limpiar_pantalla()

        # Ocupamos una funcion auxiliar para poder mostrar la tabla
        dibuja_tabla(data, a, b, ancho)

        # Etiqueta donde mostraremos el resultado del algoritmo paso por paso
        Resultado = tk.Label(height = 3, text = "Resultado : " + str(respuesta), font='helvetica 14')
        Resultado.grid(columnspan=3, column=1, row=5, padx=50, sticky='ew')

        # Obtenemos los datos del siguiente paso en el algoritmo
        b, a, data, respuesta_paso = esquinaNoroeste.obtener_tabla(a, b, data)

        # Agregamos la respuesta del paso actual a la respuesta total
        respuesta += respuesta_paso

        # Hacemos una actualizacion a la pantalla para poder mostrar el siguiente paso, en caso contrario solo muestra el último paso seguido
        window.update()

        # Ponemos un pequeño delay para poder visualizar el paso actual
        time.sleep(2)

    
    # Al final el algoritmo mostramos el resultado final en color rojo y un tamaño de letra mayor
    Resultado.config(text = "Resultado : " + str(respuesta), foreground="red",  font='helvetica 20')

    # Creamos y ponemos en pantalla un boton para volver al menu principal
    volver_boton = tk.Button(window, height=3, text="Volver", command=mostrar_menu)
    volver_boton.grid(columnspan=3, column=1, row=7, padx=50, sticky='ew')

def iniciar_costo_minimo(input):
    limpiar_pantalla()

    # Limpiamos los datos de entrada de usuario
    data = hf.limpiar_tabla(input)

    # De los datos de usurio los ordenamos de menor a mayor dependiendo el valor de la celda
    # esto para el correcto funcionamiento del algoritmo
    elementos = hf.limpiar_tabla_coste(input)

    # Establecemos el tamaño que va a tomar cada celda de la tabla
    ancho = (800//len(data[0]))//16

    # Declaramos una variable donde se guardara el resultado total de algoritmo
    respuesta = 0

    # El algoritmo se ejecuta hasta que tengamos celdas disponibles
    while (len(elementos) > 0) :
        limpiar_pantalla()

        # Obtenemos los datos actuales de la celda a ocupar, solamente necesitamos las coordenadas
        trash, a, b = elementos[0]
        
        # Ocupamos una funcion auxiliar para poder mostrar la tabla
        dibuja_tabla(data, a, b, ancho)

        # Etiqueta donde mostraremos el resultado del algoritmo paso por paso
        Resultado = tk.Label(height = 3, text = "Resultado : " + str(respuesta), font='helvetica 14')
        Resultado.grid(columnspan=3, column=1, row=5, padx=50, sticky='ew')

        # Obtenemos el siguiente paso del algoritmo
        data, elementos, respuesta_paso = costoMinimo.paso_siguiente(a, b,  data, elementos)

        # Agregamos la respuesta del siguiente paso del algoritmo y lo sumamos al resultado final
        respuesta += respuesta_paso

        # Hacemos una actualizacion a la pantalla para poder mostrar el siguiente paso, en caso contrario solo muestra el último paso seguido
        window.update()
        
        # Ponemos un pequeño delay para poder visualizar el paso actual
        time.sleep(2)


    # Para que no se tenga ninguna confusion se muestra la tabla final 
    dibuja_tabla(data, -1, -1, ancho)

     # Al final el algoritmo mostramos el resultado final en color rojo y un tamaño de letra mayor
    Resultado.config(text = "Resultado : " + str(respuesta), foreground="red",  font='helvetica 20')

    # Creamos y ponemos en pantalla un boton para volver al menu principal
    volver_boton = tk.Button(window, height=3, text="Volver", command=mostrar_menu)
    volver_boton.grid(columnspan=3, column=1, row=7, padx=50, sticky='ew')




def obtener_grafo(s, opcion):
    # En caso de que no haya ningun dato cuando se pide la matriz, cerramos completamente el programa
    if (len(s) == 0) :
        window.destroy()
        return ''

    # Limpiamos la entrada que fue proporcionada por el usuario, esto con una funcion de ayuda en otro archivo, para
    # su posterior asignacion a una variable
    adj = hf.limpiar_entrada(s)

    # En caso de que se haya seleccionado el algoritmo para el flujo maximo, se pediran el nodo inicial y el nodo final
    if opcion == 1 :
        # Limpiamos la pnatalla para poder pedir los datos restantes para el algoritmo
        limpiar_pantalla()

        # Creamos la entiqueta y el campo de entrada para el nodo inicial
        nodoInicial_label = tk.Label(window, text="Nodo inicial :", font='helvetica 20')
        nodoInicial_entry = tk.Entry(window, font=('Georgia 20'))

        # -> padx(left, right)
        # -> pady(top, bottom)

        # Los agregamos a pantalla
        nodoInicial_label.pack(pady=(50,0)) 
        nodoInicial_entry.pack(padx=(100,100), pady=(10,50))


        # Creamos la entiqueta y el campo de entrada para el nodo final
        nodoFinal_label = tk.Label(window, text="Nodo final :", font='helvetica 20')
        nodoFinal_entry = tk.Entry(window, font=('Georgia 20'))

        # Los agregamos a pantalla
        nodoFinal_label.pack()
        nodoFinal_entry.pack(padx=(100,100), pady=(10,50))

        # Creamos el boton para iniciar con el algoritmo, el cual mandara a llamar una funcion con los parametros de entrada del usuario
        confirmar_boton = tk.Button(window, width=35, height=3, text="OK", command=lambda:mostar_grafo(adj, nodoInicial_entry.get(), nodoFinal_entry.get(), 1))
        confirmar_boton.pack(pady = (25,25))

        # Creamos un boton para volver al menu principal
        volver_boton = tk.Button(window, width=35, height=3, text="Volver", command=mostrar_menu)
        volver_boton.pack(pady = (25,25))

    # En caso contrario solamente mostramos la previsualización grafo del árbol mínimo
    else :
        mostar_grafo(adj, "-1", "-1", 2)

def pedir_datos(opcion):
    limpiar_pantalla()

    # La siguiente condicional es para saber si fue seleccionado un algoritmo en el que se ocupe un grafo
    if opcion == 1 or opcion == 2 :
        # Mostramos instrucciones para ingresar la matriz
        label1 = tk.Label(text = "Ingresar la matriz de adyacencia de manera :", font='helvetica 14')
        label1.pack()

        label2 = tk.Label(text = "NODO ORIGEN" + "|NODO(S) DESTINO", font='Helvetica 12 bold' )
        label2.pack()
        
        label3 = tk.Label(text = "*Usar espacio entre cada nodo destino, se ignorarán los lazos y marcar con una x si no hay vertice", font = 'Helvetica 11')
        label3.pack()

        #Pedimos la lista de adyacencia
        input_grafo = tk.Text(window, height = 12, width = 45, bg = "white", font=('Georgia 18') )
        input_grafo.pack()

        # Creamos el boton para iniciar con el algoritmo
        confirmar_boton = tk.Button(window, width=35, height=3, text="OK", command=lambda:obtener_grafo(input_grafo.get("1.0",'end-1c'), opcion))
        confirmar_boton.pack(side="top", expand=True)

        # Creamos un boton para volver al menu principal
        volver_boton = tk.Button(window, width=35, height=3, text="Volver", command=mostrar_menu)
        volver_boton.pack(side="bottom", expand=True)

    else :
        # Mostramos instrucciones para ingresar la matriz
        label1 = tk.Label(text = "Ingresar los datos de la tabla:", font='helvetica 14')
        label1.pack()

        label2 = tk.Label(text = "*Usar espacio entre cada uno de los datos", font = 'Helvetica 11')
        label2.pack()

        #Pedimos la lista de adyacencia
        input_tabla = tk.Text(window, height = 12, width = 45, bg = "white", font=('Georgia 18') )
        input_tabla.pack()

        if opcion == 3 :
            # Creamos el boton para iniciar con el algoritmo
            confirmar_boton = tk.Button(window, width=35, height=3, text="OK", command=lambda:iniciar_esquina_noroeste(input_tabla.get("1.0",'end-1c')))
            confirmar_boton.pack(side="top", expand=True)
        else :
            # Creamos el boton para iniciar con el algoritmo
            confirmar_boton = tk.Button(window, width=35, height=3, text="OK", command=lambda:iniciar_costo_minimo(input_tabla.get("1.0",'end-1c')))
            confirmar_boton.pack(side="top", expand=True)


        # Creamos un boton para volver al menu principal
        volver_boton = tk.Button(window, width=35, height=3, text="Volver", command=mostrar_menu)
        volver_boton.pack(side="bottom", expand=True)

def mostrar_menu():   
    limpiar_pantalla()
    
    # Create the first button and add it to the top of the frame
    flujoMaximo_boton = tk.Button(window, width=35, height=3, text="Flujo máximo", command=lambda:pedir_datos(1))
    flujoMaximo_boton.pack(side="top", expand=True)

    # Create the second button and add it below the first button
    arbolMinimo_boton = tk.Button(window, width=35, height=3, text="Árbol mínimo", command=lambda:pedir_datos(2))
    arbolMinimo_boton.pack(side="top", expand=True)

    # Create the third button and add it below the second button
    esquinaNoroeste_boton = tk.Button(window, width=35, height=3, text="Esquina noroeste", command=lambda:pedir_datos(3))
    esquinaNoroeste_boton.pack(side="top", expand=True)

    # Create the fourth button and add it below the third button
    costeMinimo_botn = tk.Button(window, width=35, height=3, text="Coste Mínimo", command=lambda:pedir_datos(4))
    costeMinimo_botn.pack(side="top", expand=True)


# El siguiente par de funciones son de ayuda para manejar el cierre de la ventana del programa
# Ya que al usar el graficador de networkx, usa diferentes hilos para su ejecución

def on_closing():
    sys.exit()
window.protocol("WM_DELETE_WINDOW", on_closing)

def exit_handler():
    for thread in threading.enumerate():
        if thread is not threading.main_thread():
            thread.join()
atexit.register(exit_handler)


mostrar_menu()

# Iniciamos el programa
window.mainloop()
