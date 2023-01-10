import tkinter as tk
import helping_functions as hf

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

import sys
import atexit
import threading

## Algoritmos a incluir : 
## > Flujo maximo
## > Prim or Kruskal

infinito = 1000000000

# Creamos la ventana de la aplicacion
window = tk.Tk()
window.title("Visualización")
window.geometry("800x600")
window.resizable(False, False)

def limpiar_pantalla():
    # Limpiamos la pantalla
    for widgets in window.winfo_children():
        widgets.destroy()

def dibujar_grafo(adj):
    limpiar_pantalla()

    G = nx.Graph()

    # Recorremos la matrix de adyacencia

    for key in adj.keys():
        b = adj[key]
        i = 1

        for item in b :
            # Si hay un camino valido lo agregamos
            if item != infinito:
                G.add_edge(key, i, weight=item);
            i += 1


    # set up the figure and axes
    fig, ax = plt.subplots()

    # draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # create a FigureCanvasTkAgg widget to display the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create the first button and add it to the top of the frame
    arbolMinimo_boton = tk.Button(window, width=35, height=3, text="Flujo máximo")
    arbolMinimo_boton.pack(side="top", expand=True)





def iniciar_flujo(adj, inicial, final):
    # En caso de que no haya ningun dato cuando se pide el nodo inicial y final, cerramos completamente el programa
    if (len(inicial) == 0 or len(final) == 0) :
        window.destroy()
        return ''

    limpiar_pantalla()

    # Creamos el grafp
    dibujar_grafo(adj)
    




def obtener_grafo(s, opcion):
    # En caso de que no haya ningun dato cuando se pide la matriz, cerramos completamente el programa
    if (len(s) == 0) :
        window.destroy()
        return ''

    # En caso de que se haya seleccionado el algoritmo para el flujo maximo, se pediran el nodo inicial y el nodo final
    if (opcion == 1) :
        # Usamos la funcion de ayuda para limpiar la entrada y poder hacer uso de ella más fácil

        # En este caso se ocupa una tabla hash con multiples valores para cada llave
        adj = hf.limpiar_entrada(s)

        limpiar_pantalla()

        # Creamos la entiqueta y el campo de entrada para el nodo inicial
        nodoInicial_label = tk.Label(window, text="Nodo inicial :", font='helvetica 20')
        nodoInicial_entry = tk.Entry(window)

        # -> padx(left, right)
        # -> pady(top, bottom)

        # Los agregamos a pantalla
        nodoInicial_label.pack(pady=(50,0)) 
        nodoInicial_entry.pack(padx=(100,100), pady=(10,100))

        # Creamos la entiqueta y el campo de entrada para el nodo final
        nodoFinal_label = tk.Label(window, text="Nodo final :", font='helvetica 20')
        nodoFinal_entry = tk.Entry(window)

        # Los agregamos a pantalla
        nodoFinal_label.pack()
        nodoFinal_entry.pack(padx=(100,100), pady=(10,100))

        # Creamos el boton para iniciar con el algoritmo
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
