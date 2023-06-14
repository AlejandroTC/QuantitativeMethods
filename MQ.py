import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def generar_espacios():
    # Creamos la ventana
    ventana = tk.Tk()
    ventana.title("Generador de espacios")

    # Creamos el campo de entrada para "n"
    label_n = tk.Label(ventana, text="Ingrese el número de restricciones:")
    label_n.pack()

    input_n = tk.Entry(ventana)
    input_n.pack()

    # Función para destruir la ventana y mostrar la siguiente
    def destruir_ventana():
        n = int(input_n.get())
        # Destruimos la ventana actual
        ventana.destroy()
        # Mostramos la siguiente ventana con los campos de entrada
        mostrar_campos(n)

    def delete_window():
        close = tk.messagebox.askyesno(
            message="¿Está seguro de que quiere cerrar la aplicación?",
            title="Confirmar cierre"
        )
        if close:
            ventana.destroy()

    # Creamos el botón para generar los espacios
    boton_generar = tk.Button(ventana, text="Generar espacios", command=destruir_ventana)
    boton_salir = tk.Button(ventana, text="Salir", command=delete_window)
    boton_generar.pack(side=tk.LEFT)
    boton_salir.pack(side=tk.RIGHT)

    # Mostramos la ventana
    ventana.mainloop()


def mostrar_campos(n):
    # Creamos la ventana
    ventana = tk.Tk()
    ventana.title("Campos de entrada")

    # Crear listas para almacenar los coeficientes de cada restricción
    a_list = []
    b_list = []
    c_list = []

    # Generamos los espacios
    j = 1
    while True:
        def marcocrear():
            # Creamos un marco para los 3 espacios
            marco = tk.Frame(ventana)
            marco.pack()

            contadorlabel = tk.Label(marco, text=f"Datos {j}/{n}")
            contadorlabel.grid(row=0,column=1)
            # Creamos los campos de entrada
            labelEsp1 = tk.Label(marco, text=f"Ingrese el valor para 'x{j}':")
            labelEsp1.grid(row=1, column=0)
            espacio1 = tk.Entry(marco)
            espacio1.grid(row=2, column=0)

            labelEsp2 = tk.Label(marco, text=f"Ingrese el valor para 'y'{j}:")
            labelEsp2.grid(row=1, column=1)
            espacio2 = tk.Entry(marco)
            espacio2.grid(row=2, column=1)

            labelEsp3 = tk.Label(marco, text=f"Ingrese el valor para el valor independiente{j}:")
            labelEsp3.grid(row=1, column=2)
            espacio3 = tk.Entry(marco)
            espacio3.grid(row=2, column=2)

            # Guardamos los campos de entrada en una lista
            campos_entrada = [espacio1, espacio2, espacio3]
    
            # Función para obtener los valores de los campos de entrada
            def obtener_valores():
                a = int(campos_entrada[0].get())
                b = int(campos_entrada[1].get())
                c = int(campos_entrada[2].get())
                a_list.append(a)
                b_list.append(b)
                c_list.append(c)

            # Función para avanzar al siguiente espacio
            detener = False
            def siguiente():
                nonlocal j
                nonlocal detener
                obtener_valores()
                j += 1
                if detener or j > n:
                    ventana.destroy()
                    graficar()
                    generar_espacios()
                else:
                    marco.destroy()
                    marcocrear()

            def graficar():
                # Activar el modo interactivo de matplotlib
                plt.ion()

                # Crear una lista de puntos para graficar las restricciones
                points = []
                for z in range(n):
                    if b_list[z] != 0:
                        x = [c_list[z] / a_list[z], 0]
                        y = [0, c_list[z] / b_list[z]]
                    else:
                        x = [c_list[z] / a_list[z], c_list[z] / a_list[z]]
                        y = [0, 10]
                    points.append((x, y))

                # Graficar las restricciones
                fig, ax = plt.subplots()
                for p in points:
                    ax.plot(p[0], p[1], 'r')

                # Desactivar el modo interactivo de matplotlib y mostrar la gráfica
                plt.ioff()

                # Crear una ventana de tkinter
                root = tk.Tk()
                root.title('Gráfico')

                # Convertir el gráfico en una imagen tkinter
                canvas = FigureCanvasTkAgg(fig, master=root)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

                # Agregar la imagen al widget de etiqueta en la ventana
                graph_widget = tk.Label(root)
                graph_widget.pack(side=tk.TOP, pady=10)
                graph_widget.configure(image=canvas.get_tk_widget().image)
                # Mostrar la ventana tkinter
                root.mainloop()

            # Creamos los botones
            boton_siguiente = tk.Button(marco, text="Siguiente", command=siguiente)

            # Añadimos los botones al marco
            boton_siguiente.grid(row=3, column=1)

        marcocrear()
        # Mostramos la ventana
        ventana.mainloop()

#ejemplo de uso
generar_espacios()