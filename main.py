import tkinter as tk
from tkinter import ttk
import pandas as pd

import helping_functions as hf
import arbolMinimo as am
import flujo

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
window.resizable(False, False)

# Declaramos la varaibles necesarias para poder dibujar el grafo
fig, ax = plt.subplots()

def limpiar_pantalla():
    # Limpiamos la pantalla
    for widgets in window.winfo_children():
        widgets.destroy()



def iniciar_grafo_arbol(adj):
    G = nx.Graph()
    
    for k,v in adj.items() :
        for i in v :
            G.add_edge(k,i[0], weight=i[1])

    # La siguiente linea nos ayuda a medir la distancia entre nodo y nodo, esto nos ayuda posteriormente a mantener en su lugar geometrico
    # la posicion de toda la información del grafo y poder modificarlo
    position_graph = nx.spring_layout(G)

    widths = [2 for u,v in G.edges()]
    node_colors = ['#A4A4A4' for n in G.nodes()]
    node_sizes = [800 for n in G.nodes()]
    labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, position_graph, with_labels=True, font_weight='bold', width=widths, node_size=node_sizes, node_color=node_colors)
    nx.draw_networkx_edge_labels(G, position_graph, edge_labels=labels, font_size=11)

    # create a FigureCanvasTkAgg widget para poder mostrar correctamente el grafo
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    return G,canvas, position_graph

def mostar_arbol_minimo(adj, G, canvas, position_graph, nodos_visited, edges_visited):

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

def iniciar_arbol_minimo(adj):
    limpiar_pantalla()
    graph,canvas,position_graph = iniciar_grafo_arbol(adj)

    path, pesos = am.conseguir_camino(adj)

    # Etiqueta donde mostraremos el resultado conforme vayamos tomando cada nodo
    Resultado_arbol = tk.Label(height = 3, text = "Resultado : 0", font='helvetica 14')
    Resultado_arbol.pack(side=tk.LEFT, expand=True)

    nodos_visited = []
    edges_visited = []

    indice = 0
    resultado_algoritmo_arbol = 0

    for arista in path :
        edges_visited.append(arista)

        if (arista[0] not in nodos_visited):
            nodos_visited.append(arista[0])

        if (arista[1] not in nodos_visited):
            nodos_visited.append(arista[1])

        mostar_arbol_minimo(adj, graph, canvas, position_graph, nodos_visited, edges_visited)

        resultado_algoritmo_arbol += pesos[indice]
        
        Resultado_arbol.config(text = "Resultado : " + str(resultado_algoritmo_arbol))
        Resultado_arbol.update()
        indice += 1

        time.sleep(1.5)





def iniciar_grafo_flujo(adj, inicial, final):
    G = nx.Graph()
    
    for k,v in adj.items() :
        for i in v :
            G.add_edge(k,i[0], weight=i[1])

    # La siguiente linea nos ayuda a medir la distancia entre nodo y nodo, esto nos ayuda posteriormente a mantener en su lugar geometrico
    # la posicion de toda la información del grafo y poder modificarlo
    position_graph = nx.spring_layout(G)

    widths = [2 for u,v in G.edges()]
    node_colors = ['blue' if n == inicial or n == final else '#E9E9E9' for n in G.nodes()]
    node_sizes = [800 for n in G.nodes()]
    labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, position_graph, with_labels=True, font_weight='bold', width=widths, node_size=node_sizes, node_color=node_colors)
    nx.draw_networkx_edge_labels(G, position_graph, edge_labels=labels, font_size=11)

    # create a FigureCanvasTkAgg widget para poder mostrar correctamente el grafo
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    return G,canvas, position_graph

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


def iniciar_flujo(graph, canvas, position_graph, adj, inicial, final):

    # Mostramos el grafo
    mostrar_camino_flujo(graph, canvas,  0, [(final, final)], inicial, final, position_graph)

    # Obtenemos todos lo caminos que tenemos que seguir
    caminos = flujo.completo(adj, inicial, final)

    # Etiqueta que nos ayudara para mostrar el valor minimo del camino que se tomó
    Info = tk.Label(height = 3, text = "", font='helvetica 14')
    Info.pack(side=tk.LEFT, expand=True)

    # Etiqueta donde mostraremos el resultado del algoritmo camino por camino
    Resultado_flujo = tk.Label(height = 3, text = "Resultado : 0", font='helvetica 14')
    Resultado_flujo.pack(side=tk.LEFT, expand=True)

    # La siguiente variable nos ayudara a mostrar el resultado 
    resultado_algoritmo = 0

    for i in range (0, len(caminos)):
        Info.config(text= "")

        actual = caminos[i]

        camino_actual = actual[0]
        valor_minimo = actual[1]

        graph = mostrar_camino_flujo(graph, canvas, valor_minimo, camino_actual,inicial, final, position_graph)

        resultado_algoritmo += valor_minimo

        # Mostramos la informacion relevante al camino que se tomó
        Info.config(text = "Valor minimo : " + str(valor_minimo))
        Resultado_flujo.config(text = "Resultado : " + str(resultado_algoritmo))

        Info.update()
        Resultado_flujo.update()

        time.sleep(1)

    #### -------------------------------------------------------------------- ###


    mostrar_camino_flujo(graph, canvas,  0, [(inicial, inicial)], inicial, final, position_graph)
    Info.config(text = "")
    Resultado_flujo.config(text = "Resultado : " + str(resultado_algoritmo), foreground="red",  font='helvetica 20')


def mostar_grafo_flujo(adj, inicial, final):
    # En caso de que no haya ningun dato cuando se pide el nodo inicial y final, cerramos completamente el programa
    if (len(inicial) == 0 or len(final) == 0) :
        window.destroy()
        return ''

    inicial = int(inicial)
    final = int(final)

    # Limpiamos la pantalla para poder mostrar toda la información necesaria (El grafo, botones para mostar los pasos del algoritmo y la respuesta)
    limpiar_pantalla()

    graph, canvas, position_graph = iniciar_grafo_flujo(adj, inicial, final)

    # Create the third button and add it below the second button
    button3 = tk.Button(window, width=35, height=3, text="Iniciar", command=lambda: (button3.pack_forget(), iniciar_flujo(graph, canvas, position_graph, adj, inicial, final)))
    button3.pack(side=tk.LEFT, expand=True)



def iniciar_tabla(input, opcion):
    limpiar_pantalla()

    data = hf.limpiar_tabla(input)

    hf.imprimir_tabla(data)

    # Creating a dataframe
    df = pd.DataFrame(data)
    
    tree = ttk.Treeview(window, show='')

    # Creating the columns
    tree["columns"] = list(range(len(df.columns)))

    # Setting the column headings
    for col, col_name in enumerate(df.columns):
        tree.heading(col, text=col_name)

    # Adding the data to the treeview
    for i, row in df.iterrows():
        tree.insert("", "end", iid=i, values=list(row))
        
    style = ttk.Style()
    style.configure("Treeview", font=('Helvetica', 14), fieldbackground="", padding=5)
    tree.configure(style="Treeview")

    # Packaging the treeview
    tree.pack(pady=(100,0)) 

def iniciar_pert(graph, inicial, final, opcion) :
     # En caso de que no haya ningun dato cuando se pide el nodo inicial y final, cerramos completamente el programa
    if (len(inicial) == 0 or len(final) == 0) :
        window.destroy()
        return ''

    inicial = int(inicial)
    final = int(final)

    # Limpiamos la pantalla para poder mostrar toda la información necesaria (El grafo, botones para mostar los pasos del algoritmo y la respuesta)
    limpiar_pantalla()
    
    graph, canvas, position_graph = iniciar_grafo_flujo(graph, inicial, final)



def obtener_grafo(s, opcion):
    # En caso de que no haya ningun dato cuando se pide la matriz, cerramos completamente el programa
    if (len(s) == 0) :
        window.destroy()
        return ''

    # Limpiamos la entrada que fue proporcionada por el usuario, esto con una funcion de ayuda en otro archivo, para
    # su posterior asignacion a una variable
    adj = hf.limpiar_entrada(s)

    # En caso de que se haya seleccionado el algoritmo para el flujo maximo, se pediran el nodo inicial y el nodo final
    if (opcion == 1 or opcion == 3) :
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

        if (opcion == 1) :
            # Creamos el boton para iniciar con el algoritmo, el cual mandara a llamar una funcion con los parametros de entrada del usuario
            confirmar_boton = tk.Button(window, width=35, height=3, text="OK", command=lambda:mostar_grafo_flujo(adj, nodoInicial_entry.get(), nodoFinal_entry.get()))
            confirmar_boton.pack(pady = (25,25))

        if (opcion == 3) :

            var = tk.IntVar()

            # Ponemos la opcion para saber la opcion que se Eliga
            R1 = tk.Radiobutton(window, text="Maximizar", font=('Georgia 20'), variable=var, value=1)
            R1.pack()

            R2 = tk.Radiobutton(window, text="Minimizar", font=('Georgia 20'), variable=var, value=2)
            R2.pack()

            # Creamos el boton para iniciar con el algoritmo, el cual mandara a llamar una funcion con los parametros de entrada del usuario
            confirmar_boton = tk.Button(window, width=35, height=3, text="Iniciar", command=lambda:iniciar_pert(adj, nodoInicial_entry.get(), nodoFinal_entry.get(), var.get()))
            confirmar_boton.pack(pady = (25,25))



        # Creamos un boton para volver al menu principal
        volver_boton = tk.Button(window, width=35, height=3, text="Volver", command=mostrar_menu)
        volver_boton.pack(pady = (25,25))

    elif (opcion == 2) :
        iniciar_arbol_minimo(adj)

def pedir_datos(opcion):
    limpiar_pantalla()

    # La siguiente condicional es para saber si fue seleccionado un algoritmo en el que se ocupe un grafo
    if opcion == 1 or opcion == 2 or opcion == 3:
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

        # Creamos el boton para iniciar con el algoritmo
        confirmar_boton = tk.Button(window, width=35, height=3, text="OK", command=lambda:iniciar_tabla(input_tabla.get("1.0",'end-1c'), opcion))
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
    button3 = tk.Button(window, width=35, height=3, text="PERT probabilistico")
    button3.pack(side="top", expand=True)

    # Create the fourth button and add it below the third button
    button4 = tk.Button(window, width=35, height=3, text="Extra 1")
    button4.pack(side="top", expand=True)


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
