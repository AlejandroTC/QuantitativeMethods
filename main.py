import tkinter
import tkinter.messagebox
import customtkinter
import CTkMessagebox
from CTkMessagebox import CTkMessagebox as CtkMessagebox
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import linprog
import os

# Para la ventana de informacion
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Info")
        self.geometry("400x300")
        self.materia = customtkinter.CTkLabel(
            self, text="Métodos Cuantitativos para la Toma de Decisiones")
        self.materia.pack(padx=20, pady=20)
        self.alumnos = customtkinter.CTkLabel(self, text="Alumnos: ")
        self.alumnos.pack(padx=20, pady=20)
        self.name1 = customtkinter.CTkLabel(
            self, text="Daniel Michelle Tovar Ponce")
        self.name1.pack(padx=20, pady=5)
        self.name2 = customtkinter.CTkLabel(
            self, text="Arnold Torres Maldonado")
        self.name2.pack(padx=20, pady=5)
        self.name3 = customtkinter.CTkLabel(
            self, text="Alejandro Tamayo Castro")
        self.name3.pack(padx=20, pady=5)
        self.wm_attributes("-topmost", True)

#Main
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dual por método gráfico")

        # Definir el modo del switch
        def cambiar_modos():
            if switch_var.get() == "on":
                switch_text.set("Maximización")
                # Funcion a maximizar
            else:
                switch_text.set("Minimización")
                # Funcion a minimizar

        #Colores
        colors = ['red', 'green', 'blue', 'orange', 'purple', 'gray', 'brown', 'pink', 'yellow', 'cyan',
          'magenta', 'teal', 'navy', 'olive', 'maroon', 'lime', 'aqua', 'silver', 'black', 'white',
          'indigo', 'violet', 'turquoise', 'coral', 'gold', 'salmon', 'orchid', 'khaki', 'peru',
          'slategray', 'chartreuse', 'steelblue', 'tomato', 'plum', 'dodgerblue', 'sienna', 'seagreen',
          'sandybrown', 'rosybrown', 'mediumvioletred', 'mediumturquoise', 'mediumslateblue', 'mediumpurple',
          'mediumaquamarine', 'lightsteelblue', 'lightsalmon', 'lightseagreen', 'lightgray', 'lightcyan']
        # Cambiar el modo en cualquier momento
        def on_switch_change(*args):
            iniciar()
        # Crear los marcos
        self.frame2 = customtkinter.CTkFrame(
            self, border_width=2, width=500, height=700)
        self.frame2.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # desactiva el cambio de tamaño automático
        self.frame2.grid_propagate(False)
        self.frame1 = customtkinter.CTkFrame(
            self, border_width=2, width=500, height=500)
        self.frame1.grid(row=0, column=1, sticky="nsew")
        # desactiva el cambio de tamaño automático
        self.frame1.grid_propagate(False)
        self.frame3 = customtkinter.CTkFrame(
            self, border_width=2, width=500, height=200)
        self.frame3.grid(row=1, column=1, columnspan="2", sticky="nsew")
        # desactiva el cambio de tamaño automático
        self.frame3.grid_propagate(False)

        # Crear el switch para cambiar entre los metodos de maximizacion y minimizacion
        switch_var = customtkinter.StringVar(value="on")
        switch_var.trace_add('write', on_switch_change)
        switch_text = customtkinter.StringVar(value="Maximización")
        switch = customtkinter.CTkSwitch(master=self.frame1, textvariable=switch_text,
                                         variable=switch_var, onvalue="on", offvalue="off", command=cambiar_modos)
        switch.grid(row=0, column=0, padx=10, pady=10)
        # Configura que la colunma 0 tenga un weight especifico
        self.frame1.columnconfigure(0, weight=1)

        # Boton para una ventana con nuestra info
        self.toplevel_window = None

        def open_toplevel():
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                # create window if its None or destroyed
                self.toplevel_window = ToplevelWindow()
            else:
                self.toplevel_window.focus()  # if window exists focus it

        ruta_icono = os.path.join(CTkMessagebox.__path__[
                                  0], 'icons', 'info.png')
        # cargar la imagen
        img = Image.open(ruta_icono)
        img_resized = img.resize((15, 15))
        photo = customtkinter.CTkImage(img_resized)
        self.info = customtkinter.CTkButton(
            self.frame1, image=photo, fg_color="transparent", text='', width=20, height=20, command=open_toplevel)
        self.info.grid(row=0, column=0, padx=2, pady=5, sticky='w')

        # Label para funcion objetivo
        self.label = customtkinter.CTkLabel(
            self.frame1, text="Función Objetivo")
        self.label.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        # Crear un sub-frame para la funcion Z
        z_frame = customtkinter.CTkFrame(self.frame1, fg_color="transparent")
        z_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10)
        # Label Z
        z_label = customtkinter.CTkLabel(z_frame, text="Z =")
        z_label.grid(row=0, column=0)
        # Entry para x1
        x1_entry = customtkinter.CTkEntry(
            z_frame, width=40, placeholder_text="X1")
        x1_entry.grid(row=0, column=1, padx=5)

        # Label X1 y +
        mas_label = customtkinter.CTkLabel(z_frame, text="X1 +")
        mas_label.grid(row=0, column=2, padx=5)
        # Entry para x2
        x2_entry = customtkinter.CTkEntry(
            z_frame, width=40, placeholder_text="X2")
        x2_entry.grid(row=0, column=3, padx=5)
        # Label para x2
        mas_label2 = customtkinter.CTkLabel(z_frame, text="X2 + ")
        mas_label2.grid(row=0, column=4, padx=10)
        # Entry para x3
        x3_entry = customtkinter.CTkEntry(
            z_frame, width=40, placeholder_text="X3")
        x3_entry.grid(row=0, column=5, padx=5)
        # Label para x2
        mas_label3 = customtkinter.CTkLabel(z_frame, text="X3")
        mas_label3.grid(row=0, column=6, padx=10)

        # Graficar Maximizacion

        def graficar_maximizacion():
            limpiar()
            obtener_valores()
            x1_valor = int(x_valor[0])
            x2_valor = int(x_valor[1])
            # Obtener los valores de la funcion objetivo
            # n = int(self.num_restr_entry.get())  # Guardar el valor de n
            n = int(3)  # Guardar el valor de n
            x1 = int(x1_valor)
            x2 = int(x2_valor)

            def solve_lp(c, A, b):
                resmax = linprog(-c, A_ub=A, b_ub=b,
                                 bounds=(0, None), method='highs')
                return resmax

            # Crear una figura de matplotlib
            fig = plt.Figure(figsize=(5, 5), dpi=100)
            ax = fig.add_subplot(111)

            # Crear la matriz de coeficientes para el método Simplex
            A = np.array([a_list, b_list]).T
            b = np.array(c_list)

            # Definir la función objetivo a maximizar
            c = np.array([x1, x2])

            # Resolver el problema de programación lineal con el método Simplex
            res = solve_lp(c, A, b)

            # Obtener el punto máximo
            max_x, max_y = res.x

            # Crear una lista de puntos para graficar las restricciones
            points = []
            for i in range(n):
                if b_list[i] != 0:
                    x = [c_list[i] / a_list[i], 0]
                    y = [0, c_list[i] / b_list[i]]
                else:
                    x = [c_list[i] / a_list[i], c_list[i] / a_list[i]]
                    y = [0, 10]
                points.append((x, y))

            # Graficar las restricciones
            for i, p in enumerate(points):
                ax.plot(p[0], p[1], color=colors[i])

            # Graficar el puntos
            ax.scatter(max_x, max_y, color='blue')
            # Agregar una etiqueta con el valor de min_x y min_y a la gráfica
            ax.annotate(f"({round(max_x,2)}, {round(max_y,2)})", xy=(max_x, max_y), xytext=(max_x + 0.2, max_y + 0.2), fontsize=8,
                        color='blue')

            # Destruir la figura anterior, si existe
            for widget in self.frame2.winfo_children():
                widget.destroy()

            # Agregar la figura al widget de la gráfica
            canvas = FigureCanvasTkAgg(fig, master=self.frame2)
            canvas.draw()
            canvas.get_tk_widget().pack(side=customtkinter.TOP, fill=customtkinter.BOTH)
            concluir_maximizacion(max_x, max_y, x1_valor, x2_valor)

        # Concluir minimizacion
        def concluir_maximizacion(max_x=float, max_y=float, x1_valor=float, x2_valor=float):
            conclusiones = f"El punto que resuelve la funcion objetivo 'Z= {x1_valor}x_1 + {x2_valor}x_2'" \
                           f" esta dado en el punto ({round(max_x, 2)}, {round(max_y, 2)}), el cual es mostrado en la gráfica" \
                           f" y resuelve el problema de maximización"
            self.text_area.delete('1.0', customtkinter.END)
            self.text_area.insert(customtkinter.END, conclusiones)

        # Graficar Minimizacion - Hay que modificar esto para que haga la minimizacion
        def graficar_minimizacion():
            limpiar()
            obtener_valores()
            x1_valor = int(x_valor[0])
            x2_valor = int(x_valor[1])
            # n = int(self.num_restr_entry.get())  # Guardar el valor de n

            # Obtener los valores de la funcion objetivo
            # n = int(self.num_restr_entry.get())  # Guardar el valor de n
            n = int(3)  # Guardar el valor de n
            x1 = int(x1_valor)
            x2 = int(x2_valor)

            # Crear una figura de matplotlib
            fig = plt.Figure(figsize=(5, 5), dpi=100)
            ax = fig.add_subplot(111)

            # Crear la matriz de coeficientes para el método Simplex
            A = np.array([a_list, b_list]).T
            b = np.array(c_list)

            # Definir la función objetivo a minimizar
            c = np.array([x1, x2])

            # Resolver el problema de programación lineal con el método Simplex
            res = linprog(c, A_ub=-A, b_ub=-b,
                          bounds=(0, None), method='highs')

            # Obtener el punto mínimo
            min_x, min_y = res.x

            # Crear una lista de puntos para graficar las restricciones
            points = []
            for i in range(n):
                if b_list[i] != 0:
                    x = [c_list[i] / a_list[i], 0]
                    y = [0, c_list[i] / b_list[i]]
                else:
                    x = [c_list[i] / a_list[i], c_list[i] / a_list[i]]
                    y = [0, 10]
                points.append((x, y))

            # Colores para las restricciones

            # Graficar las restricciones
            fig, ax = plt.subplots()

            for i, p in enumerate(points):
                ax.plot(p[0], p[1], color=colors[i])

            # Graficar el puntos
            ax.scatter(min_x, min_y, color='blue')
            # Agregar una etiqueta con el valor de min_x y min_y a la gráfica
            ax.annotate(f"({round(min_x,2)}, {round(min_y,2)})", xy=(min_x, min_y), xytext=(min_x + 0.2, min_y + 0.2), fontsize=8,
                        color='blue')

            # Destruir la figura anterior, si existe
            for widget in self.frame2.winfo_children():
                widget.destroy()

            # Agregar la figura al widget de la gráfica
            canvas = FigureCanvasTkAgg(fig, master=self.frame2)
            canvas.draw()
            canvas.get_tk_widget().pack(side=customtkinter.TOP, fill=customtkinter.BOTH)
            concluir_minimizacion(min_x, min_y, x1_valor, x2_valor)

        # Concluir minimizacion
        def concluir_minimizacion(min_x=float, min_y=float, x1_valor=float, x2_valor=float):
            conclusiones = f"El punto que resuelve la funcion objetivo 'Z= {x1_valor}x_1 + {x2_valor}x_2'" \
                           f" esta dado en el punto ({round(min_x, 2)}, {round(min_y, 2)}), el cual es mostrado en la gráfica" \
                           f" y resuelve el problema de minimización."
            self.text_area.delete('1.0', customtkinter.END)
            self.text_area.insert(customtkinter.END, conclusiones)

           # Restricciones y todo lo que tenga que ver con ello

        # Crear un sub-frame para las entrys de restricciones
        restrentry_frame = customtkinter.CTkFrame(
            self.frame1, fg_color="transparent", width=400, height=150)
        restrentry_frame.grid(row=3, column=0, columnspan=5, padx=10, pady=10)
        # Crear un sub-frame para las entrys de restricciones
        do_frame = customtkinter.CTkFrame(
            self.frame1, fg_color="transparent", width=400, height=150)
        do_frame.grid(row=4, column=0, columnspan=5, padx=10, pady=10)
        # Funcion para generar las restricciones
        restrs = []  # Guardar las label para eliminarlas
        restr_entrys = []  # Guardar las entradas para eliminarlas o leerlas

        def iniciar():
            def generar_restricciones():

                def res1():
                    restr = customtkinter.CTkLabel(
                        restrentry_frame, text="Restricción 1", text_color=colors[1])
                    restr.grid(row=0, column=0, columnspan=7,
                               padx=10, pady=5, sticky="ns")

                    restr_x1 = customtkinter.CTkEntry(
                        restrentry_frame, placeholder_text="X1", width=50)
                    restr_x1.grid(row=1, column=0, padx=2, pady=5, sticky="ns")

                    masr_label = customtkinter.CTkLabel(
                        restrentry_frame, text="X1 +", text_color=colors[1])
                    masr_label.grid(row=1, column=1, padx=5)

                    restr_x2 = customtkinter.CTkEntry(
                        restrentry_frame, placeholder_text="X2", width=50)
                    restr_x2.grid(row=1, column=2, padx=2, pady=5, sticky="ns")

                    masr_label2 = customtkinter.CTkLabel(
                        restrentry_frame, text="X2 +", text_color=colors[1])
                    masr_label2.grid(row=1, column=3, padx=5)

                    restr_x3 = customtkinter.CTkEntry(
                        restrentry_frame, placeholder_text="X2", width=50)
                    restr_x3.grid(row=1, column=4, padx=2, pady=5, sticky="ns")

                    if switch_var.get() == "on":
                        equalr_label = customtkinter.CTkLabel(
                            restrentry_frame, text="X3 <=", text_color=colors[1])
                    else:
                        equalr_label = customtkinter.CTkLabel(
                            restrentry_frame, text="X3 >=", text_color=colors[1])
                    equalr_label.grid(row=1, column=5, padx=5)

                    restr_ind = customtkinter.CTkEntry(
                        restrentry_frame, placeholder_text="Ind", width=50)
                    restr_ind.grid(row=1, column=6, padx=2,
                                   pady=5, sticky="ns")

                    restrs.append(restr)
                    restr_entrys.append(
                        (restr_x1, restr_x2, restr_x3, restr_ind, masr_label, equalr_label, masr_label2))

                def res2():
                    restr = customtkinter.CTkLabel(
                        restrentry_frame, text="Restricción 2", text_color=colors[2])
                    restr.grid(row=2, column=0, columnspan=7,
                               padx=10, pady=5, sticky="ns")

                    restr_x1 = customtkinter.CTkEntry(
                        restrentry_frame, placeholder_text="X1", width=50)
                    restr_x1.grid(row=3, column=0, padx=2, pady=5, sticky="ns")

                    masr_label = customtkinter.CTkLabel(
                        restrentry_frame, text="X1 +", text_color=colors[2])
                    masr_label.grid(row=3, column=1, padx=5)

                    restr_x2 = customtkinter.CTkEntry(
                        restrentry_frame, placeholder_text="X2", width=50)
                    restr_x2.grid(row=3, column=2, padx=2, pady=5, sticky="ns")

                    masr_label2 = customtkinter.CTkLabel(
                        restrentry_frame, text="X2 +", text_color=colors[2])
                    masr_label2.grid(row=3, column=3, padx=5)

                    restr_x3 = customtkinter.CTkEntry(
                        restrentry_frame, placeholder_text="X2", width=50)
                    restr_x3.grid(row=3, column=4, padx=2, pady=5, sticky="ns")

                    if switch_var.get() == "on":
                        equalr_label = customtkinter.CTkLabel(
                            restrentry_frame, text="X3 <=", text_color=colors[2])
                    else:
                        equalr_label = customtkinter.CTkLabel(
                            restrentry_frame, text="X3 >=", text_color=colors[2])
                    equalr_label.grid(row=3, column=5, padx=5)

                    restr_ind = customtkinter.CTkEntry(
                        restrentry_frame, placeholder_text="Ind", width=50)
                    restr_ind.grid(row=3, column=6, padx=2,
                                   pady=5, sticky="ns")

                    restrs.append(restr)
                    restr_entrys.append(
                        (restr_x1, restr_x2, restr_x3, restr_ind, masr_label, equalr_label, masr_label2))

                res1()
                res2()

                if switch_var.get() == "on":
                    # Generar el boton para graficar maximizacion
                    generar_restr = customtkinter.CTkButton(
                        do_frame, text="Maximizar", command=graficar_minimizacion)
                    generar_restr.grid(row=0, column=0, padx=10,
                                       pady=5, sticky="ns")
                    restrs.append(generar_restr)
                else:
                    # Generar el boton para graficar minimizacion
                    generar_restr = customtkinter.CTkButton(
                        do_frame, text="Minimizar", command=graficar_maximizacion)
                    generar_restr.grid(row=0, column=0, padx=10,
                                       pady=5, sticky="ns")
                    restrs.append(generar_restr)

            generar_restricciones()
        iniciar()

        # Eliminar
        def eliminar_etiquetas():
            for restr in restrs:
                restr.destroy()
            for restr_entry in restr_entrys:
                for entry in restr_entry:
                    entry.destroy()
            restr_entrys.clear()
            restrs.clear()
            iniciar()

        self.button_eliminar_dual = customtkinter.CTkButton(do_frame, text="Reiniciar", command=eliminar_etiquetas)
        self.button_eliminar_dual.grid(row=1, column=0, padx=10, pady=5, sticky='ns')

        # Obtener los valores de las restricciones
        a_list_dual = []  # Valor de X1
        b_list_dual = []  # Valor de X2
        c_list_dual = []  # Valor de Ind
        # Para obtener la funcion objetivo y mandar los valores a graficar_...
        z_list_dual = []  # Valor de Z
        x_valor_dual = []  # Para valor de x

        # Limpiar los valores de las restricciones para reutilizar

        def limpiar_dual():
            a_list_dual.clear()
            b_list_dual.clear()
            c_list_dual.clear()
            z_list_dual.clear()
            x_valor_dual.clear()
        # Funcion para obtener los valores

        def obtener_valores_dual():
            for restr_entry in restr_entrys:
                x = int(restr_entry[3].get())  # Valor de funcion objetivo Z
                x_valor.append(x)

            # Acceder al primer elemento de restr_entrys
            restr_entry_dual = restr_entrys_dual[0]
            a = int(restr_entry_dual[0].get())   # Valor de x1 en restricciones
            a_list_dual.append(a)
            a = int(restr_entry_dual[1].get())   # Valor de x2 en restricciones
            a_list_dual.append(a)
            a = int(restr_entry_dual[2].get())   # Valor de ind en restricciones
            a_list_dual.append(a)
            # Acceder al primer elemento de restr_entrys
            restr_entry_dual = restr_entrys_dual[1]
            # Valor de x1 en el segundo restr_entry
            b = int(restr_entry_dual[0].get())
            b_list_dual.append(b)
            # Valor de x2 en el segundo restr_entry
            b = int(restr_entry_dual[1].get())
            b_list_dual.append(b)
            # Valor de ind en el segundo restr_entry
            b = int(restr_entry_dual[2].get())
            b_list_dual.append(b)

            if x1_entry_dual.get().isdigit():  # Verificar si el valor de x1_entry es un dígito
                # Agregar el valor a la lista
                c_list_dual.append(int(x1_entry.get()))

            if x2_entry_dual.get().isdigit():  # Verificar si el valor de x2_entry es un dígito
                # Agregar el valor a la lista
                c_list_dual.append(int(x2_entry.get()))

            if x3_entry_dual.get().isdigit():  # Verificar si el valor de x3_entry es un dígito
                # Agregar el valor a la lista
                c_list_dual.append(int(x3_entry.get()))

        # Crear los widgets de la columna 3
        self.text_area = customtkinter.CTkTextbox(self.frame3, height=200, width=500, font=("Arial", 20))
        self.text_area.pack(side=customtkinter.TOP, pady=5)


if __name__ == "__main__":
    app = App()
    # Cerrar la ventana completamente

    def cerrar_ventana():
        app.destroy()
    # Agregar un botón de cerrar a la ventana
    app.protocol("WM_DELETE_WINDOW", cerrar_ventana)
    app.mainloop()
