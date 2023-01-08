import tkinter as tk
## Algoritmos a incluir : 
## > Flujo maximo
## > Prim or Kruskal

# Creamos la ventana de la aplicacion
window = tk.Tk()
window.title("Visualización")
window.geometry("800x600")
window.resizable(False, False)

def pedir_grafo():
    # Limpiamos la pantalla
    for widgets in window.winfo_children():
        widgets.destroy()
    
    # Mostramos instrucciones para ingresar datos
    label1 = tk.Label(text = "Ingresar la lista de adyacencia de manera :")
    label2 = tk.Label(text = "NODO ORIGEN" + "  |  NODO(S) DESTINO")
    label1.pack()
    label2.pack()
    label3 = tk.Label(text = "Con una coma de separacion entre cada nodo destino")
    label3.pack()

    #Pedimos la lista de adyacencia


    # Create the first button and add it to the top of the frame
    volver_boton = tk.Button(window, width=35, height=3, text="Volver", command=mostrar_menu)
    volver_boton.pack(side="bottom", expand=True)

def mostrar_menu():
    # Limpiamos la pantalla
    for widgets in window.winfo_children():
        widgets.destroy()
    
    # Create the first button and add it to the top of the frame
    arbolMinimo_boton = tk.Button(window, width=35, height=3, text="Árbol mínimo", command=pedir_grafo)
    arbolMinimo_boton.pack(side="top", expand=True)

    # Create the second button and add it below the first button
    flujoMaximo_boton = tk.Button(window, width=35, height=3, text="Flujo máximo", command=pedir_grafo)
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
