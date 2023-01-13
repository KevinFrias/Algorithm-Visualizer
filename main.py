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

    for n in G.nodes:
        G.nodes[n]["visible"] = True

    for u,v in G.edges: 
        G[u][v]["visible"] = True


    position_graph = nx.spring_layout(G)

    nx.draw(G, position_graph, with_labels=True, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, position_graph, edge_labels=labels)

    # create a FigureCanvasTkAgg widget to display the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    return G,canvas, position_graph



def modificar_grafo(G, canvas, position_graph):

    '''
    ax.clear()  
    fig.clear()

    # Set the node's visibility to False
    G.nodes[2]["visible"] = False
    # Set the edges' visibility to False
    for u, v in G.edges(2):
        G[u][v]["visible"] = False

    node_list = []
    edge_list = []

    for i in G.nodes :
        if G.nodes[i]["visible"] == True :
            node_list.append(i)

    for u,v in G.edges :
        if G[u][v]["visible"] == True :
            edge_list.append((u,v))



    # Draw the graph, skipping invisible nodes and edges
    nx.draw(G, position_graph,  with_labels=True, font_weight='bold', nodelist=node_list)
    nx.draw_networkx_edges(G,position_graph, edgelist=edge_list)
    labels = nx.get_edge_attributes(G, 'weight')

    for i in labels:
        for j in i :
            if (j == 2):
                del[i]
                break

    

    print(labels)

    nx.draw_networkx_edge_labels(G,position_graph, edge_labels=labels)
    '''

    '''
    G.remove_node(6)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    canvas.draw()
    canvas.get_tk_widget().update()
    '''



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

    for i in range (0, len(caminos)):
        actual = caminos[i]
        camino_actual = actual[0]
        valor_minimo = actual[1]

        print ('Valor minimo : ', valor_minimo, '   Camino a seguir : ', camino_actual)



    # Create the first button and add it to the top of the frame
    Siguiente_boton = tk.Button(window, width=35, height=3, text="Anterior", command= lambda: modificar_grafo(graph, canvas, position_graph))
    #Siguiente_boton.place(x=10, y=525)
    Siguiente_boton.pack(side=tk.LEFT, expand=True)

    # Mostramos instrucciones para ingresar la matriz
    Resultado = tk.Label(text = "00000", font='helvetica 14')
    #Resultado.place(x=380, y=545)
    Resultado.pack(side=tk.LEFT, expand=True)

    # Create the first button and add it to the top of the frame
    Anterior_boton = tk.Button(window, width=35, height=3, text="Siguiente")
    #Anterior_boton.place(x=480, y=525)
    Anterior_boton.pack(side=tk.LEFT, expand=True)

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
