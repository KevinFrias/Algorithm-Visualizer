import tkinter as tk
import helping_functions as hf
import flujo

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

import sys
import atexit
import threading
import time

infinito = 10000000000

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

def iniciar_grafo(adj):
    G = nx.Graph()
    
    for k,v in adj.items() :
        for i in v :
            G.add_edge(k,i[0], weight=i[1])

    position_graph = nx.spring_layout(G)

    widths = [2 for u,v in G.edges()]
    node_sizes = [800 for n in G.nodes()]
    labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, position_graph, with_labels=True, font_weight='bold', width=widths, node_size=node_sizes)
    nx.draw_networkx_edge_labels(G, position_graph, edge_labels=labels)

    # create a FigureCanvasTkAgg widget to display the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    return G,canvas, position_graph



def mostrar_camino(G, canvas, camino_actual, inicial, final, position_graph):

    pasados  = []
    arista_pasada = []

    for i in camino_actual :
        ax.clear()
        fig.clear()
        pasados.append(i[0])
        pasados.append(i[1])

        arista_pasada.append((i))

        node_colors = ['blue' if n == inicial or n == final else 'red' if n in pasados else 'white' for n in G.nodes()]
        edge_colors = ['red' if (u,v) in arista_pasada or (v,u) in arista_pasada else 'black' for u,v in G.edges()]

        node_sizes = [800 for n in G.nodes()]
        widths = [3 if (u,v) == i or (v,u) == i else 2 for u,v in G.edges()]
        labels = nx.get_edge_attributes(G, 'weight')


        nx.draw(G, position_graph, with_labels=True, font_weight='bold', edge_color=edge_colors, node_color=node_colors, width= widths, node_size=node_sizes)
        nx.draw_networkx_edge_labels(G, position_graph, edge_labels=labels)

        canvas.draw()
        canvas.get_tk_widget().update()

        time.sleep(1.5)


def iniciar_flujo(adj, inicial, final):
    # En caso de que no haya ningun dato cuando se pide el nodo inicial y final, cerramos completamente el programa
    if (len(inicial) == 0 or len(final) == 0) :
        window.destroy()
        return ''

    inicial = int(inicial)
    final = int(final)

    # Limpiamos la pantalla para poder mostrar toda la información necesaria (El grafo, botones para mostar los pasos del algoritmo y la respuesta)
    limpiar_pantalla()
    graph,canvas,position_graph = iniciar_grafo(adj)



    #### -------------------------------------------------------------------- ###

    caminos = flujo.completo(adj, inicial, final)

    ## Para hacer update al grafo, primero hay que hacer de color diferente la arista. de cado de el camino
    ## Despues de que hacemos todo el camino, regresamos al color original
    ## Poner el peso actualizado
    ## Si alguno de esos pesos ya no lo podemos ocupar, entonces marcamos de color diferente esa arista

    for i in range (0, len(caminos)):
        actual = caminos[i]

        camino_actual = actual[0]
        valor_minimo = actual[1]

        #print ('Valor minimo : ', valor_minimo, '   Camino a seguir : ', camino_actual)
        #print()

        mostrar_camino(graph, canvas, camino_actual,inicial, final, position_graph)
        time.sleep(2)



    #### -------------------------------------------------------------------- ###

    '''
    # Create the first button and add it to the top of the frame
    Anterior_boton = tk.Button(window, width=35, height=3, text="Siguiente", command=lambda : modificar_grafo())
    #Anterior_boton.place(x=480, y=525)
    Anterior_boton.pack(side=tk.LEFT, expand=True)
    '''

    # Mostramos instrucciones para ingresar la matriz
    Resultado = tk.Label(text = "00000", font='helvetica 14')
    #Resultado.place(x=380, y=545)
    Resultado.pack(side=tk.LEFT, expand=True)

def obtener_grafo(s, opcion):
    # En caso de que no haya ningun dato cuando se pide la matriz, cerramos completamente el programa
    if (len(s) == 0) :
        window.destroy()
        return ''

    # En caso de que se haya seleccionado el algoritmo para el flujo maximo, se pediran el nodo inicial y el nodo final
    if (opcion == 1) :
        # Limpiamos la entrada que fue proporcionada por el usuario, esto con una funcion de ayuda en otro archivo, para
        # su posterior asignacion a una variable
        adj = hf.limpiar_entrada(s)

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
        confirmar_boton = tk.Button(window, width=35, height=3, text="Iniciar", command=lambda:iniciar_flujo(adj, nodoInicial_entry.get(), nodoFinal_entry.get()))
        confirmar_boton.pack(pady = (25,25))


        # Creamos un boton para volver al menu principal
        volver_boton = tk.Button(window, width=35, height=3, text="Volver", command=mostrar_menu)
        volver_boton.pack(pady = (25,25))

def pedir_grafo(opcion):
    limpiar_pantalla()

    # Mostramos instrucciones para ingresar la matriz
    label1 = tk.Label(text = "Ingresar la matriz de adyacencia de manera :", font='helvetica 14')
    label1.pack()

    label2 = tk.Label(text = "NODO ORIGEN" + "  |  NODO(S) DESTINO", font='Helvetica 12 bold' )
    label2.pack()
    
    label3 = tk.Label(text = "*Usar espacio entre cada nodo destino, se ignorarán los lazos y marcar con una x si no hay vertice", font = 'Helvetica 11')
    label3.pack()

    #Pedimos la lista de adyacencia
    input_grafo = tk.Text(window, height = 18, width = 68, bg = "white")
    input_grafo.pack()

    # Creamos el boton para iniciar con el algoritmo
    confirmar_boton = tk.Button(window, width=35, height=3, text="OK", command=lambda:obtener_grafo(input_grafo.get("1.0",'end-1c'), opcion))
    confirmar_boton.pack(side="top", expand=True)


    # Creamos un boton para volver al menu principal
    volver_boton = tk.Button(window, width=35, height=3, text="Volver", command=mostrar_menu)
    volver_boton.pack(side="bottom", expand=True)

def mostrar_menu():   
    limpiar_pantalla()
    
    # Create the first button and add it to the top of the frame
    arbolMinimo_boton = tk.Button(window, width=35, height=3, text="Flujo máximo", command=lambda:pedir_grafo(1))
    arbolMinimo_boton.pack(side="top", expand=True)

    # Create the second button and add it below the first button
    flujoMaximo_boton = tk.Button(window, width=35, height=3, text="Árbol mínimo", command=lambda:pedir_grafo(2))
    flujoMaximo_boton.pack(side="top", expand=True)

    # Create the third button and add it below the second button
    button3 = tk.Button(window, width=35, height=3, text="Extra 1")
    button3.pack(side="top", expand=True)

    # Create the fourth button and add it below the third button
    button4 = tk.Button(window, width=35, height=3, text="Extra 2")
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
