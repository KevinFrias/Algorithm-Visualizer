import tkinter as tk
import helping_functions as hf

## Algoritmos a incluir : 
## > Flujo maximo
## > Prim or Kruskal

# Creamos la ventana de la aplicacion
window = tk.Tk()
window.title("Visualización")
window.geometry("800x600")
window.resizable(False, False)

opcion = 0

def limpiar_pantalla():
    # Limpiamos la pantalla
    for widgets in window.winfo_children():
        widgets.destroy()

def get_data(s, inicial, final):

    # En caso de que no haya ningun dato cuando se pide la matriz, cerramos completamente el programa
    if (len(s) == 0) :
        window.destroy()
        return ''

    # En caso  de que se haya seleccionado el algoritmo del flujo maximo y no se hayan proporcionado el
    # nodo inicial y final, cerramos completamente el programa
    if (opcion == 1) :
        if (len(inicial) == 0 or len(final) == 0) :
            indow.destroy()
            return ''


    limpiar_pantalla()
    # Usamos la funcion de ayuda para limpiar la entrada y crear la lista de adyacencia
    # En este caso se ocupa una tabla hash con multiples valores para cada llave
    adj = hf.crear_adjList(s)
    
    print(inicial)
    print(final)

    for k,v in adj.items():
        print(k , ' : ', v)

def pedir_grafo(numero):
    limpiar_pantalla()
    opcion = numero
    nodoInicial = 'x'
    nodoFinal = 'x'

    # Los algoritmos son 
    # BFS, lo cual necesitamos : Nodo inicial, Nodo final y matriz de adyacencia

    # En caso de que se haya seleccionado el algoritmo para el flujo maximo, se pediran el nodo inicial y el nodo final
    if (opcion == 1) :
        # Creamos un frame para poder poner en la misma linea la etiqueta y el input para el dato
        frame = tk.Frame(window)
        frame.pack()
        # Creamos la etiqueta y el input
        nodoInicial_label = tk.Label(frame, text="Nodo inicial :", font='helvetica 14')
        nodoInicial_dato = tk.Entry(frame)
        # Lo ponemos en pantalla
        nodoInicial_label.pack(side="left")
        nodoInicial_dato.pack(side="left")



        frame2 = tk.Frame(window)
        frame2.pack()
        # Creamos la etiqueta y el input
        nodoFinal_label = tk.Label(frame2, text="Nodo final :", font='helvetica 14')
        nodoFinal_dato = tk.Entry(frame2)
        # Lo ponemos en pantalla
        nodoFinal_label.pack(side="left")
        nodoFinal_dato.pack(side="left")




        # Obtenemos los valores del nodo inicial y final
        nodoInicial = nodoInicial_dato.get()
        nodoFinal = nodoFinal_dato.get()


    # Mostramos instrucciones para ingresar datos
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
    confirmar_boton = tk.Button(window, width=35, height=3, text="OK", command=lambda:get_data(input_grafo.get("1.0",'end-1c'), nodoInicial, nodoFinal))
    confirmar_boton.pack(side="top", expand=True)


    # Creamos un boton para volver al menu principal
    volver_boton = tk.Button(window, width=35, height=3, text="Volver", command=mostrar_menu)
    volver_boton.pack(side="bottom", expand=True)

def mostrar_menu():   
    limpiar_pantalla()
    opcion = 0
    
    # Create the first button and add it to the top of the frame
    arbolMinimo_boton = tk.Button(window, width=35, height=3, text="Árbol mínimo", command=lambda:pedir_grafo(1))
    arbolMinimo_boton.pack(side="top", expand=True)

    # Create the second button and add it below the first button
    flujoMaximo_boton = tk.Button(window, width=35, height=3, text="Flujo máximo", command=lambda:pedir_grafo(2))
    flujoMaximo_boton.pack(side="top", expand=True)

    # Create the third button and add it below the second button
    button3 = tk.Button(window, width=35, height=3, text="Extra 1")
    button3.pack(side="top", expand=True)

    # Create the fourth button and add it below the third button
    button4 = tk.Button(window, width=35, height=3, text="Extra 2")
    button4.pack(side="top", expand=True)


mostrar_menu()
# Run the main loop
window.mainloop()
