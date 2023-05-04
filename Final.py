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

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.materia = customtkinter.CTkLabel(self, text="Métodos Cuantitativos para la Toma de Decisiones")
        self.materia.pack(padx=20, pady=20)
        self.alumnos = customtkinter.CTkLabel(self, text="Alumnos: ")
        self.alumnos.pack(padx=20, pady=20)
        self.name1 = customtkinter.CTkLabel(self, text="Daniel Michelle Tovar Ponce")
        self.name1.pack(padx=20, pady=5)
        self.name2 = customtkinter.CTkLabel(self, text="Arnold Torres Maldonado")
        self.name2.pack(padx=20, pady=5)
        self.name3 = customtkinter.CTkLabel(self, text="Alejandro Tamayo Castro")
        self.name3.pack(padx=20, pady=5)
        self.wm_attributes("-topmost", True)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Método Gráfico")

        #Definir el modo del switch
        def cambiar_modos():
            if switch_var.get() == "on":
                switch_text.set("Maximización")
                # Funcion a maximizar
            else:
                switch_text.set("Minimización")
                # Funcion a minimizar
        
        # Crear los marcos
        self.frame1 = customtkinter.CTkFrame(self, border_width=2, width=500, height=700)
        self.frame1.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.frame1.grid_propagate(False) # desactiva el cambio de tamaño automático
        self.frame2 = customtkinter.CTkFrame(self, border_width=2, width=500, height=500)
        self.frame2.grid(row=0, column=1, sticky="nsew")
        self.frame2.grid_propagate(False) # desactiva el cambio de tamaño automático
        self.frame3 = customtkinter.CTkFrame(self, border_width=2, width=500, height=200)
        self.frame3.grid(row=1, column=1, columnspan="2", sticky="nsew")
        self.frame3.grid_propagate(False) # desactiva el cambio de tamaño automático
        
        #Crear el switch para cambiar entre los metodos de maximizacion y minimizacion
        switch_var = customtkinter.StringVar(value="on")
        switch_text = customtkinter.StringVar(value="Maximización")
        switch = customtkinter.CTkSwitch(master=self.frame1, textvariable=switch_text, variable=switch_var, onvalue="on", offvalue="off", command=cambiar_modos)
        switch.grid(row=0, column=0, padx=10, pady=10)
        self.frame1.columnconfigure(0, weight=1)    #Configura que la colunma 0 tenga un weight especifico
        
        #Boton para una ventana con nuestra info
        self.toplevel_window = None
        def open_toplevel():
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow()  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()  # if window exists focus it
        
        ruta_icono = os.path.join(CTkMessagebox.__path__[0], 'icons', 'info.png')
        # cargar la imagen
        img = Image.open(ruta_icono)
        img_resized = img.resize((15, 15))
        photo = customtkinter.CTkImage(img_resized)
        self.info = customtkinter.CTkButton(self.frame1, image=photo, fg_color="transparent", text='', width=20, height=20, command=open_toplevel)
        self.info.grid(row=0, column=0, padx=2, pady=5, sticky='w')
        
        
        #Label para funcion objetivo
        self.label = customtkinter.CTkLabel(self.frame1, text="Función Objetivo")
        self.label.grid(row=1, column=0, columnspan=5, padx=10, pady=10)
        
        # Crear un sub-frame para la funcion Z
        z_frame = customtkinter.CTkFrame(self.frame1, fg_color="transparent")
        z_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

        #Label Z
        z_label = customtkinter.CTkLabel(z_frame, text="Z =")
        z_label.grid(row=0, column=0)
        #Entry para x1
        x1_entry = customtkinter.CTkEntry(z_frame, width=40, placeholder_text="X1")
        x1_entry.grid(row=0, column=1, padx=5)
        #Label X1 y +
        mas_label = customtkinter.CTkLabel(z_frame, text="X1 +")
        mas_label.grid(row=0, column=2, padx=5)
        #Entry para x2
        x2_entry = customtkinter.CTkEntry(z_frame, width=40, placeholder_text="X2")
        x2_entry.grid(row=0, column=3, padx=5)
        #Label para x2
        mas_label2 = customtkinter.CTkLabel(z_frame, text="X2")
        mas_label2.grid(row=0, column=4, padx=10)
        # Crear un sub-frame para las restricciones
        restr_frame = customtkinter.CTkFrame(self.frame1, fg_color="transparent")
        restr_frame.grid(row=3, column=0, columnspan=5, padx=10, pady=10)
        #numero de restricciones
        self.num_restr_label = customtkinter.CTkLabel(restr_frame, text="Cantidad de Restricciones")
        self.num_restr_label.grid(row=0, column=0, padx=2, pady=5, sticky='ns')
        #n restricciones
        self.num_restr_entry = customtkinter.CTkEntry(restr_frame, placeholder_text="n", width=70)
        self.num_restr_entry.grid(row=0, column=1, padx=2, pady=5, sticky='ns')

        # Graficar Maximizacion
        def graficar_maximizacion():
            limpiar()
            obtener_valores()

            # Obtener los valores de la funcion objetivo
            n = int(self.num_restr_entry.get())  # Guardar el valor de n
            x1_valor = x1_entry.get()
            x1 = int(x1_valor)
            x2_valor = x2_entry.get()
            x2 = int(x2_valor)

            def solve_lp(c, A, b):
                resmax = linprog(-c, A_ub=A, b_ub=b, bounds=(0, None), method='highs')
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
            for p in points:
                ax.plot(p[0], p[1], 'r')

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
            n = int(self.num_restr_entry.get())  # Guardar el valor de n

            # Obtener los valores de la funcion objetivo
            n = int(self.num_restr_entry.get())  # Guardar el valor de n
            x1_valor = x1_entry.get()
            x1 = int(x1_valor)
            x2_valor = x2_entry.get()
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
            res = linprog(c, A_ub=-A, b_ub=-b, bounds=(0, None), method='highs')

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

            # Graficar las restricciones
            fig, ax = plt.subplots()

            for p in points:
                ax.plot(p[0], p[1], 'r')

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
            concluir_minimizacion(min_x, min_y,x1_valor, x2_valor)

        # Concluir minimizacion
        def concluir_minimizacion(min_x=float, min_y=float, x1_valor=float, x2_valor=float):
            conclusiones = f"El punto que resuelve la funcion objetivo 'Z= {x1_valor}x_1 + {x2_valor}x_2'" \
                           f" esta dado en el punto ({round(min_x, 2)}, {round(min_y, 2)}), el cual es mostrado en la gráfica" \
                           f" y resuelve el problema de minimización."
            self.text_area.delete('1.0', customtkinter.END)
            self.text_area.insert(customtkinter.END, conclusiones)
        
        #Restricciones y todo lo que tenga que ver con ello
        # Crear un sub-frame para las entrys de restricciones
        restrentry_frame = customtkinter.CTkScrollableFrame(self.frame1, fg_color="transparent", width=400, height=300)
        restrentry_frame.grid(row=5, column=0, columnspan=5, padx=10, pady=10)
        # Crear un sub-frame para las entrys de restricciones
        do_frame = customtkinter.CTkFrame(self.frame1, fg_color="transparent", width=400)
        do_frame.grid(row=6, column=0, columnspan=5, padx=10, pady=10)
        #Funcion para generar las restricciones
        restrs = [] #Guardar las label para eliminarlas
        restr_entrys = []   #Guardar las entradas para eliminarlas o leerlas
        def generar_restricciones():
            n_str = self.num_restr_entry.get()  #Obtener el valor de n
            eliminar_etiquetas()    #Limpiar todas las restricciones
            if n_str.isdigit(): #Si el valor de n es un digito
                n = int(n_str)  #Guardar el valor de n
                for i in range(n):  #Generar todas las entradas de las restricciones
                    restr = customtkinter.CTkLabel(restrentry_frame, text=f"Restricción {i+1}")
                    restr.grid(row=0+i, column=0, padx=10, pady=5, sticky="ns")
                    restr_x1 = customtkinter.CTkEntry(restrentry_frame, placeholder_text="X1", width=50)
                    restr_x1.grid(row=0+i, column=2, padx=2, pady=5, sticky="ns")
                    masr_label = customtkinter.CTkLabel(restrentry_frame, text="X1 +")
                    masr_label.grid(row=0+i, column=3, padx=5)
                    restr_x2 = customtkinter.CTkEntry(restrentry_frame, placeholder_text="X2", width=50)
                    restr_x2.grid(row=0+i, column=4, padx=2, pady=5, sticky="ns")
                    if switch_var.get() == "on":
                        equalr_label = customtkinter.CTkLabel(restrentry_frame, text="X2 <=")
                        equalr_label.grid(row=0+i, column=5, padx=5)
                    else:
                        equalr_label = customtkinter.CTkLabel(restrentry_frame, text="X2 >=")
                        equalr_label.grid(row=0+i, column=5, padx=5)
                    restr_ind = customtkinter.CTkEntry(restrentry_frame, placeholder_text="Ind", width=50)
                    restr_ind.grid(row=0+i, column=6, padx=2, pady=5, sticky="ns")
                    restrs.append(restr)
                    restr_entrys.append((restr_x1, restr_x2, restr_ind, masr_label, equalr_label))  # agregar una tupla con las tres entradas de la restricción
                if switch_var.get() == "on":
                    #Generar el boton para graficar maximizacion
                    generar_restr = customtkinter.CTkButton(do_frame, text="Maximizar", command=graficar_maximizacion)
                    generar_restr.grid(row=0, column=0, padx=10, pady=5, sticky="ns")
                    restrs.append(generar_restr)
                else:
                    #Generar el boton para graficar minimizacion
                    generar_restr = customtkinter.CTkButton(do_frame, text="Minimizar", command=graficar_minimizacion)
                    generar_restr.grid(row=0, column=0, padx=10, pady=5, sticky="ns")
                    restrs.append(generar_restr)
            else:
                CtkMessagebox(title="Error", message="El número de restricciones no es un numero valido", icon="cancel")
        #Eliminar 
        def eliminar_etiquetas():
            for restr in restrs:
                restr.destroy()
            for restr_entry in restr_entrys:
                for entry in restr_entry:
                    entry.destroy()
            restr_entrys.clear()
            restrs.clear()
        #Obtener los valores de las restricciones
        a_list = []
        b_list = []
        c_list = []
        #Limpiar los valores de las restricciones para reutilizar
        def limpiar():
            a_list.clear()
            b_list.clear()
            c_list.clear()
        #Funcion para obtener los valores
        def obtener_valores():
            for restr_entry in restr_entrys:
                if restr_entry[0].get().isdigit() and restr_entry[0].get().isdigit() and restr_entry[0].get().isdigit() : 
                    a = int(restr_entry[0].get())
                    b = int(restr_entry[1].get())
                    c = int(restr_entry[2].get())
                    a_list.append(a)
                    b_list.append(b)
                    c_list.append(c)
                else:
                    CtkMessagebox(title="Error", message="Asegurese de ingresar numeros positivos", icon="cancel")
                    
        # Crear un sub-frame para las restricciones
        restrbutton_frame = customtkinter.CTkFrame(self.frame1, fg_color="transparent")
        restrbutton_frame.grid(row=4, column=0, columnspan=5, padx=10, pady=10)
        #botones para agregar restricciones
        self.button_restr = customtkinter.CTkButton(restrbutton_frame, text="Agregar", command=generar_restricciones)
        self.button_restr.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='ns')
        self.button_eliminar = customtkinter.CTkButton(restrbutton_frame, text="Eliminar", command=eliminar_etiquetas)
        self.button_eliminar.grid(row=0, column=2, columnspan=3, padx=2, pady=5, sticky='ns')
        
        # Crear los widgets de la columna 3
        self.text_area = customtkinter.CTkTextbox(self.frame3, height=200, width=500, font=("Arial", 20))
        self.text_area.pack(side=customtkinter.TOP, pady=5)
        
if __name__ == "__main__":
    app = App()
    #Cerrar la ventana completamente
    def cerrar_ventana():
        app.destroy()
    # Agregar un botón de cerrar a la ventana
    app.protocol("WM_DELETE_WINDOW", cerrar_ventana)
    app.mainloop()
