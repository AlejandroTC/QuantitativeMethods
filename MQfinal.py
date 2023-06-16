import tkinter
import sys
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
from PIL import ImageGrab

# Para la ventana de informacion
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Info")
        self.geometry("400x300")
        self.materia = customtkinter.CTkLabel(
            self, text="Métodos Cuantitativos para la Toma de Decisiones")
        self.materia.pack(padx=20, pady=5)
        self.grupo = customtkinter.CTkLabel(
            self, text="6CM1")
        self.grupo.pack(padx=20, pady=5)
        self.alumnos = customtkinter.CTkLabel(self, text="Alumnos: ")
        self.alumnos.pack(padx=20, pady=5)
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

# Main
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Programación Lineal - Métodos Cuantitativos")
        
        # Función para verificar el cambio de pestaña
        def inicio():
            active_tab = tabview.get()
            if active_tab != "Método Dual":
                print("Grafico")
                mgrafico()
            else:
                print("Dual")
                mdual()
        def captura_pantalla():
            counter = 1  # Contador de capturas
            x = self.winfo_rootx()
            y = self.winfo_rooty()
            width = self.winfo_width()
            height = self.winfo_height()
            active_tab = tabview.get()
            if active_tab != "Método Dual":
                filename = f"Grafico_{counter}.png"
            else:
                filename = f"Dual_{counter}.png"
            while os.path.exists(filename):
                # Si existe, incrementar el contador y generar un nuevo nombre de archivo
                counter += 1
                active_tab = tabview.get()
                if active_tab != "Método Dual":
                    filename = f"Grafico_{counter}.png"
                else:
                    filename = f"Dual_{counter}.png"
            CtkMessagebox(title="Captura", message="Se ha guardado la captura", icon="check")
            sc = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            counter += 1
            sc.save(filename)
        
        tabview = customtkinter.CTkTabview(master=self)
        tabview.pack(padx=20, pady=20)
        tabview.configure(command=inicio)
        #Variables para ventanas
        mg = tabview.add("Método Gráfico")
        dual = tabview.add("Método Dual")    
        
    #Colores
        colors = ['red', 'green', 'blue', 'orange', 'purple', 'gray', 'brown', 'pink', 'yellow', 'cyan',
          'magenta', 'teal', 'navy', 'olive', 'maroon', 'lime', 'aqua', 'silver', 'black', 'white',
          'indigo', 'violet', 'turquoise', 'coral', 'gold', 'salmon', 'orchid', 'khaki', 'peru',
          'slategray', 'chartreuse', 'steelblue', 'tomato', 'plum', 'dodgerblue', 'sienna', 'seagreen',
          'sandybrown', 'rosybrown', 'mediumvioletred', 'mediumturquoise', 'mediumslateblue', 'mediumpurple',
          'mediumaquamarine', 'lightsteelblue', 'lightsalmon', 'lightseagreen', 'lightgray', 'lightcyan']
    
    #Funciones para graficar y concluir
        # Graficar Maximizacion
        def graficar_maximizacion(a_list, b_list, c_list, x1, x2, n):
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


            active_tab = tabview.get()
            if active_tab == "Método Dual":
                start_index = 1
            else:
                start_index = 0

            for i, p in enumerate(points[start_index:], start=start_index):
                ax.plot(p[0], p[1], color=colors[i])
                ax.fill_between(p[0], p[1], np.max(y)*4, color=colors[i], alpha=0.3)
            ax.set_ylim(bottom=0, top=np.max(y))
            ax.set_xlim(left=0, right=np.max(x))
            # Graficar el puntos
            ax.scatter(max_x, max_y, color='black')
            # Agregar una etiqueta con el valor de min_x y min_y a la gráfica
            ax.annotate(f"({round(max_x,2)}, {round(max_y,2)})", xy=(max_x, max_y), xytext=(max_x - 1, max_y - 1), fontsize=10,color='black')
            
            # Destruir la figura anterior, si existe
            active_tab = tabview.get()
            if(active_tab == "Método Dual"):
                for widget in self.frame5.winfo_children():
                    widget.destroy()
            else:
                for widget in self.frame2.winfo_children():
                    widget.destroy()

            # Agregar la figura al widget de la gráfica
            active_tab = tabview.get()
            if(active_tab == "Método Dual"):
                canvas = FigureCanvasTkAgg(fig, master=self.frame5)
            else:
                canvas = FigureCanvasTkAgg(fig, master=self.frame2)
            canvas.draw()
            canvas.get_tk_widget().pack(side=customtkinter.TOP, fill=customtkinter.BOTH)
            concluir_maximizacion(max_x, max_y, x1, x2)
        # Concluir minimizacion
        def concluir_maximizacion(max_x=float, max_y=float, x1_valor=float, x2_valor=float):
            conclusiones = f"El punto que resuelve la funcion objetivo 'Z= {x1_valor}x_1 + {x2_valor}x_2'" \
                           f" esta dado en el punto ({round(max_x, 2)}, {round(max_y, 2)}), el cual es mostrado en la gráfica" \
                           f" y resuelve el problema de maximización"
            # active_tab = tabview.get()
            # if(active_tab == "Método Dual"):
            #     self.text_area_dual.delete('1.0', customtkinter.END)
            #     self.text_area_dual.insert(customtkinter.END, conclusiones)
            # else:
            self.text_area.delete('1.0', customtkinter.END)
            self.text_area.insert(customtkinter.END, conclusiones)
        # Graficar Minimizacion
        def graficar_minimizacion(a_list, b_list, c_list, x1, x2, n):
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

            active_tab = tabview.get()
            if active_tab == "Método Dual":
                start_index = 1
            else:
                start_index = 0

            for i, p in enumerate(points[start_index:], start=start_index):
                ax.plot(p[0], p[1], color=colors[i])
                ax.fill_between(p[0], p[1], color=colors[i], alpha=0.3)

            ax.set_ylim(bottom=0, top=np.max(y))
            ax.set_xlim(left=0, right=np.max(x))
            # Graficar el puntos
            ax.scatter(min_x, min_y, color='black')
            # Agregar una etiqueta con el valor de min_x y min_y a la gráfica
            ax.annotate(f"({round(min_x,2)}, {round(min_y,2)})", xy=(min_x, min_y), xytext=(min_x + 0.2, min_y + 0.2), fontsize=10,color='black')

            # Destruir la figura anterior, si existe
            active_tab = tabview.get()
            if(active_tab == "Método Dual"):
                for widget in self.frame5.winfo_children():
                    widget.destroy()
            else:
                for widget in self.frame2.winfo_children():
                    widget.destroy()

            # Agregar la figura al widget de la gráfica}
            active_tab = tabview.get()
            if(active_tab == "Método Dual"):
                canvas = FigureCanvasTkAgg(fig, master=self.frame5)
            else:
                canvas = FigureCanvasTkAgg(fig, master=self.frame2)
            canvas.draw()
            canvas.get_tk_widget().pack(side=customtkinter.TOP, fill=customtkinter.BOTH)
            concluir_minimizacion(min_x, min_y,x1, x2)
        # Concluir minimizacion
        def concluir_minimizacion(min_x=float, min_y=float, x1_valor=float, x2_valor=float):
            conclusiones = f"El punto que resuelve la funcion objetivo 'Z= {x1_valor}x_1 + {x2_valor}x_2'" \
                           f" esta dado en el punto ({round(min_x, 2)}, {round(min_y, 2)}), el cual es mostrado en la gráfica" \
                           f" y resuelve el problema de minimización."
            # active_tab = tabview.get()
            # if(active_tab == "Método Dual"):
            #     self.text_area_dual.delete('1.0', customtkinter.END)
            #     self.text_area_dual.insert(customtkinter.END, conclusiones)
            # else:
            self.text_area.delete('1.0', customtkinter.END)
            self.text_area.insert(customtkinter.END, conclusiones)
            
    #Metodos
        #Método gráfico
        def mgrafico():
            def cambiar_modos():
                if switch_var.get() == "on":
                    switch_text.set("Maximización")
                    # Funcion a maximizar
                else:
                    switch_text.set("Minimización")
                    # Funcion a minimizar
            # Crear los marcos para Metodo grafico
            self.frame1 = customtkinter.CTkFrame(mg, border_width=2, width=500, height=700)
            self.frame1.grid(row=0, column=0, rowspan=2, sticky="nsew")
            self.frame1.grid_propagate(False) # desactiva el cambio de tamaño automático
            self.frame2 = customtkinter.CTkFrame(mg, border_width=2, width=500, height=500)
            self.frame2.grid(row=0, column=1, sticky="nsew")
            self.frame2.grid_propagate(False) # desactiva el cambio de tamaño automático
            self.frame3 = customtkinter.CTkFrame(mg, border_width=2, width=500, height=200)
            self.frame3.grid(row=1, column=1, columnspan="2", sticky="nsew")
            self.frame3.grid_propagate(False) # desactiva el cambio de tamaño automático
            #Crear el switch de modos para el Metodo Grafico
            switch_var = customtkinter.StringVar(value="on")
            switch_text = customtkinter.StringVar(value="Maximización")
            switch = customtkinter.CTkSwitch(master=self.frame1, textvariable=switch_text,variable=switch_var, onvalue="on", offvalue="off", command=cambiar_modos)
            switch.grid(row=0, column=0, padx=10, pady=10)
            # Configura que la colunma 0 tenga un weight especifico
            self.frame1.columnconfigure(0, weight=1)
            # Boton para una ventana con nuestra info
            self.toplevel_window = None
            def open_toplevel():
                if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                    self.toplevel_window = ToplevelWindow()  # create window if its None or destroyed
                else:
                    self.toplevel_window.focus()  # if window exists focus it
            # Info page
            ruta_icono = os.path.join(CTkMessagebox.__path__[0], 'icons', 'info.png')
            img = Image.open(ruta_icono)
            img_resized = img.resize((15, 15))
            photo = customtkinter.CTkImage(img_resized)
            self.info = customtkinter.CTkButton(self.frame1, image=photo, fg_color="transparent", text='', width=20, height=20, command=open_toplevel)
            self.info.grid(row=0, column=0, padx=2, pady=5, sticky='w')
            #Screenshot
            ruta_icono = os.path.join(CTkMessagebox.__path__[0], 'icons', 'check.png')
            img = Image.open(ruta_icono)
            img_resized = img.resize((15, 15))
            photo = customtkinter.CTkImage(img_resized)
            self.screenshot = customtkinter.CTkButton(self.frame1, image=photo, fg_color="transparent", text='', width=20, height=20, command=captura_pantalla)
            self.screenshot.grid(row=0, column=1, padx=2, pady=5, sticky='w')
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
                #colors = ['red', 'green', 'blue', 'orange', 'purple', 'gray', 'brown']
                n_str = self.num_restr_entry.get()  #Obtener el valor de n
                eliminar_etiquetas()    #Limpiar todas las restricciones
                if n_str.isdigit() and int(n_str) != 0: #Si el valor de n es un digito
                    n = int(n_str)  #Guardar el valor de n
                    for i in range(n):  #Generar todas las entradas de las restricciones
                        restr = customtkinter.CTkLabel(restrentry_frame, text=f"Restricción {i+1}", text_color=colors[i])
                        restr.grid(row=0+i, column=0, padx=10, pady=5, sticky="ns")
                        restr_x1 = customtkinter.CTkEntry(restrentry_frame, placeholder_text="X1", width=50)
                        restr_x1.grid(row=0+i, column=2, padx=2, pady=5, sticky="ns")
                        masr_label = customtkinter.CTkLabel(restrentry_frame, text="X1 +", text_color=colors[i])
                        masr_label.grid(row=0+i, column=3, padx=5)
                        restr_x2 = customtkinter.CTkEntry(restrentry_frame, placeholder_text="X2", width=50)
                        restr_x2.grid(row=0+i, column=4, padx=2, pady=5, sticky="ns")
                        if switch_var.get() == "on":
                            equalr_label = customtkinter.CTkLabel(restrentry_frame, text="X2 <=", text_color=colors[i])
                            equalr_label.grid(row=0+i, column=5, padx=5)
                        else:
                            equalr_label = customtkinter.CTkLabel(restrentry_frame, text="X2 >=", text_color=colors[i])
                            equalr_label.grid(row=0+i, column=5, padx=5)
                        restr_ind = customtkinter.CTkEntry(restrentry_frame, placeholder_text="Ind", width=50)
                        restr_ind.grid(row=0+i, column=6, padx=2, pady=5, sticky="ns")
                        restrs.append(restr)
                        restr_entrys.append((restr_x1, restr_x2, restr_ind, masr_label, equalr_label))  # agregar una tupla con las tres entradas de la restricción
                    if switch_var.get() == "on":
                        #Generar el boton para graficar maximizacion
                        generar_restr = customtkinter.CTkButton(do_frame, text="Maximizar", command=lambda: graficar_maximizacion(obtener_valores(1), obtener_valores(2), obtener_valores(3), obtener_valores(4), obtener_valores(5), obtener_valores(6)))
                        generar_restr.grid(row=0, column=0, padx=10, pady=5, sticky="ns")
                        restrs.append(generar_restr)
                    else:
                        #Generar el boton para graficar minimizacion
                        generar_restr = customtkinter.CTkButton(do_frame, text="Minimizar", command=lambda: graficar_minimizacion(obtener_valores(1), obtener_valores(2), obtener_valores(3), obtener_valores(4), obtener_valores(5), obtener_valores(6)))
                        generar_restr.grid(row=0, column=0, padx=10, pady=5, sticky="ns")
                        restrs.append(generar_restr)
                else:
                    CtkMessagebox(title="Error", message="El número de restricciones no es un numero valido", icon="cancel")
                    raise ValueError("El número de restricciones no es un numero valido")
            #Eliminar 
            def eliminar_etiquetas():
                for restr in restrs:
                    restr.destroy()
                for restr_entry in restr_entrys:
                    for entry in restr_entry:
                        entry.destroy()
                restr_entrys.clear()
                restrs.clear()
            #Funcion para obtener los valores
            def obtener_valores(opcion):
                # Obtener los valores de la funcion objetivo
                n = int(self.num_restr_entry.get())  # Guardar el valor de n
                x1_valor = x1_entry.get()
                x2_valor = x2_entry.get()
                if x2_valor.isdigit() and x1_valor.isdigit() and int(x2_valor) != 0 and int(x1_valor) != 0:
                    x1 = int(x1_valor)
                    x2 = int(x2_valor)
                else:
                    CtkMessagebox(title="Error", message="La función objetivo no son números enteros válidos", icon="cancel")
                    raise ValueError("La función objetivo no contiene números enteros válidos")
                #Obtener los valores de las restricciones
                a_list = []
                b_list = []
                c_list = []
                for restr_entry in restr_entrys:
                    if restr_entry[0].get().isdigit() and restr_entry[1].get().isdigit() and restr_entry[2].get().isdigit() and int(restr_entry[0].get()) and int(restr_entry[1].get()) and int(restr_entry[2].get()):
                        x1 = int(x1_valor)
                        x2 = int(x2_valor)
                    else:
                        CtkMessagebox(title="Error", message="Las restricciones no contienen números enteros válidos", icon="cancel")
                        raise ValueError("Las restricciones no contienen números enteros válidos")
                    a = int(restr_entry[0].get())
                    b = int(restr_entry[1].get())
                    c = int(restr_entry[2].get())
                    a_list.append(a)
                    b_list.append(b)
                    c_list.append(c)
                if opcion == 1:
                    return a_list
                elif opcion == 2:
                    return b_list
                elif opcion == 3:
                    return c_list
                elif opcion == 4:
                    return x1
                elif opcion == 5:
                    return x2
                else:
                    return n
                    
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
            
        #Método dual
        def mdual():
            def cambiar_modos():
                if switch_var.get() == "on":
                    switch_text.set("Maximización")
                    # Funcion a maximizar
                else:
                    switch_text.set("Minimización")
                    # Funcion a minimizar
                # Cambiar el modo en cualquier momento
            def on_switch_change(*args):
                generar_restricciones()
            #Crear los marcos para Metodo Dual
            self.frame4 = customtkinter.CTkFrame(dual, border_width=2, width=500, height=500)
            self.frame4.grid(row=0, column=1, sticky="nsew")
            # desactiva el cambio de tamaño automático
            self.frame4.grid_propagate(False)
            self.frame5 = customtkinter.CTkFrame(dual, border_width=2, width=500, height=500)
            self.frame5.grid(row=0, column=0, rowspan=2, sticky="nsew")
            # desactiva el cambio de tamaño automático
            self.frame5.grid_propagate(False)
            self.frame6 = customtkinter.CTkFrame(dual, border_width=2, width=500, height=200)
            self.frame6.grid(row=1, column=0,  sticky="nsew")
            # desactiva el cambio de tamaño automático
            self.frame6.grid_propagate(False)
            self.frame7 = customtkinter.CTkFrame(dual, border_width=2, width=500, height=200)
            self.frame7.grid(row=1, column=1, columnspan="2", sticky="nsew")
            # desactiva el cambio de tamaño automático
            self.frame7.grid_propagate(False)
            self.text_area = customtkinter.CTkTextbox(self.frame6, height=200, width=500, font=("Arial", 20))
            self.text_area.pack(side=customtkinter.TOP, pady=5)
            #Aviso dual 
            # Crear los widgets de la columna 3
            self.aviso = customtkinter.CTkTextbox(self.frame7, height=200, width=500, font=("Arial", 20), text_color=colors[5], fg_color="transparent")
            self.aviso.pack(side=customtkinter.TOP)
            duala = "El método dual se resuelve mediante el método" \
                    f" gráfico, utilizando las variables de las dos restricciones para " \
                    f" formar las restricciones 1, 2 y 3 en el método gráfico." \
                    f" La solución se obtiene de la función objetivo del" \
                    f" dual, mientras que la función objetivo en el gráfico" \
                    f" se genera utilizando los resultados de las restricciones en el dual."
            self.aviso.delete('1.0', customtkinter.END)
            self.aviso.insert(customtkinter.END, duala)
            self.aviso.configure(state="disabled")
            #Crear el switch de modos para el Dual
            switch_var = customtkinter.StringVar(value="on")
            switch_var.trace_add('write', on_switch_change)
            switch_text = customtkinter.StringVar(value="Maximización")
            switch = customtkinter.CTkSwitch(master=self.frame4, textvariable=switch_text, variable=switch_var, onvalue="on", offvalue="off", command=cambiar_modos)
            switch.grid(row=0, column=0, padx=10, pady=10)
            # Configura que la colunma 0 tenga un weight especifico
            self.frame4.columnconfigure(0, weight=1)
            # Boton para una ventana con nuestra info
            self.toplevel_window = None
            def open_toplevel():
                if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                    self.toplevel_window = ToplevelWindow()  # create window if its None or destroyed
                else:
                    self.toplevel_window.focus()  # if window exists focus it
            # Info
            ruta_icono = os.path.join(CTkMessagebox.__path__[0], 'icons', 'info.png')
            img = Image.open(ruta_icono)
            img_resized = img.resize((15, 15))
            photo = customtkinter.CTkImage(img_resized)
            self.info = customtkinter.CTkButton(
                self.frame4, image=photo, fg_color="transparent", text='', width=20, height=20, command=open_toplevel)
            self.info.grid(row=0, column=0, padx=2, pady=5, sticky='w')
            #Screenshot
            ruta_icono = os.path.join(CTkMessagebox.__path__[0], 'icons', 'check.png')
            img = Image.open(ruta_icono)
            img_resized = img.resize((15, 15))
            photo = customtkinter.CTkImage(img_resized)
            self.screenshot = customtkinter.CTkButton(self.frame4, image=photo, fg_color="transparent", text='', width=20, height=20, command=captura_pantalla)
            self.screenshot.grid(row=0, column=1, padx=2, pady=5, sticky='w')
            # Crear un sub-frame para la funcion Z
            z_frame = customtkinter.CTkFrame(self.frame4, fg_color="transparent")
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
            # Crear un sub-frame para las entrys de restricciones
            restrentry_frame = customtkinter.CTkFrame(self.frame4, fg_color="transparent", width=400, height=150)
            restrentry_frame.grid(row=3, column=0, columnspan=5, padx=10, pady=10)
            # Crear un sub-frame para las entrys de restricciones
            do_frame = customtkinter.CTkFrame(self.frame4, fg_color="transparent", width=400, height=150)
            do_frame.grid(row=4, column=0, columnspan=5, padx=10, pady=10)
            # Funcion para generar las restricciones
            restrs = []  # Guardar las label para eliminarlas
            restr_entrys = []  # Guardar las entradas para eliminarlas o leerlas
            def generar_restricciones():
                def res1():
                    restr = customtkinter.CTkLabel(restrentry_frame, text="Restricción 1", text_color=colors[0])
                    restr.grid(row=0, column=0, columnspan=7,padx=10, pady=5, sticky="ns")

                    restr_x1 = customtkinter.CTkEntry(restrentry_frame, placeholder_text="X1", width=50)
                    restr_x1.grid(row=1, column=0, padx=2, pady=5, sticky="ns")

                    masr_label = customtkinter.CTkLabel(restrentry_frame, text="X1 +", text_color=colors[0])
                    masr_label.grid(row=1, column=1, padx=5)

                    restr_x2 = customtkinter.CTkEntry(restrentry_frame, placeholder_text="X2", width=50)
                    restr_x2.grid(row=1, column=2, padx=2, pady=5, sticky="ns")

                    masr_label2 = customtkinter.CTkLabel(restrentry_frame, text="X2 +", text_color=colors[0])
                    masr_label2.grid(row=1, column=3, padx=5)

                    restr_x3 = customtkinter.CTkEntry(restrentry_frame, placeholder_text="X2", width=50)
                    restr_x3.grid(row=1, column=4, padx=2, pady=5, sticky="ns")

                    if switch_var.get() == "on":
                        equalr_label = customtkinter.CTkLabel(restrentry_frame, text="X3 <=", text_color=colors[0])
                    else:
                        equalr_label = customtkinter.CTkLabel(restrentry_frame, text="X3 >=", text_color=colors[0])
                    equalr_label.grid(row=1, column=5, padx=5)

                    restr_ind = customtkinter.CTkEntry(restrentry_frame, placeholder_text="Ind", width=50)
                    restr_ind.grid(row=1, column=6, padx=2,pady=5, sticky="ns")

                    restrs.append(restr)
                    restr_entrys.append((restr_x1, restr_x2, restr_x3, restr_ind, masr_label, equalr_label, masr_label2))

                def res2():
                    restr = customtkinter.CTkLabel(restrentry_frame, text="Restricción 2", text_color=colors[1])
                    restr.grid(row=2, column=0, columnspan=7,padx=10, pady=5, sticky="ns")

                    restr_x1 = customtkinter.CTkEntry(restrentry_frame, placeholder_text="X1", width=50)
                    restr_x1.grid(row=3, column=0, padx=2, pady=5, sticky="ns")

                    masr_label = customtkinter.CTkLabel(restrentry_frame, text="X1 +", text_color=colors[1])
                    masr_label.grid(row=3, column=1, padx=5)

                    restr_x2 = customtkinter.CTkEntry(restrentry_frame, placeholder_text="X2", width=50)
                    restr_x2.grid(row=3, column=2, padx=2, pady=5, sticky="ns")

                    masr_label2 = customtkinter.CTkLabel(restrentry_frame, text="X2 +", text_color=colors[1])
                    masr_label2.grid(row=3, column=3, padx=5)

                    restr_x3 = customtkinter.CTkEntry(restrentry_frame, placeholder_text="X2", width=50)
                    restr_x3.grid(row=3, column=4, padx=2, pady=5, sticky="ns")

                    if switch_var.get() == "on":
                        equalr_label = customtkinter.CTkLabel(restrentry_frame, text="X3 <=", text_color=colors[1])
                    else:
                        equalr_label = customtkinter.CTkLabel(restrentry_frame, text="X3 >=", text_color=colors[1])
                    equalr_label.grid(row=3, column=5, padx=5)

                    restr_ind = customtkinter.CTkEntry(restrentry_frame, placeholder_text="Ind", width=50)
                    restr_ind.grid(row=3, column=6, padx=2,pady=5, sticky="ns")

                    restrs.append(restr)
                    restr_entrys.append((restr_x1, restr_x2, restr_x3, restr_ind, masr_label, equalr_label, masr_label2))

                res1()
                res2()

                if switch_var.get() == "on":
                    # Generar el boton para graficar maximizacion
                    generar_restr = customtkinter.CTkButton(do_frame, text="Maximizar", command=lambda: graficar_minimizacion(obtener_valores(1), obtener_valores(2), obtener_valores(3), obtener_valores(4), obtener_valores(5), obtener_valores(6)))
                    generar_restr.grid(row=0, column=0, padx=10,pady=5, sticky="ns")
                    restrs.append(generar_restr)
                else:
                    # Generar el boton para graficar minimizacion
                    generar_restr = customtkinter.CTkButton(do_frame, text="Minimizar", command=lambda: graficar_maximizacion(obtener_valores(1), obtener_valores(2), obtener_valores(3), obtener_valores(4), obtener_valores(5), obtener_valores(6)))
                    generar_restr.grid(row=0, column=0, padx=10,pady=5, sticky="ns")
                    restrs.append(generar_restr)
            generar_restricciones()
            # Eliminar
            def eliminar_etiquetas():
                for restr in restrs:
                    restr.destroy()
                for restr_entry in restr_entrys:
                    for entry in restr_entry:
                        entry.destroy()
                restr_entrys.clear()
                restrs.clear()
                generar_restricciones()
            
            self.button_eliminar = customtkinter.CTkButton(do_frame, text="Reiniciar", command=eliminar_etiquetas)
            self.button_eliminar.grid(row=1, column=0, padx=10, pady=5, sticky='ns')   
            # Obtener los valores de las restricciones
        
            def obtener_valores(opcion):
                a_list = []  # Valor de X1
                b_list = []  # Valor de X2
                c_list = []  # Valor de Ind
                # Para obtener la funcion objetivo y mandar los valores a graficar_...
                x_valor = []  # Para valor de x
                for restr_entry in restr_entrys:
                    if restr_entry[3].get().isdigit() and int(restr_entry[3].get()):
                        x = int(restr_entry[3].get())  # Valor de funcion objetivo Z
                        x_valor.append(x)
                    else:
                        CtkMessagebox(title="Error", message="Las restricciones no contienen números enteros válidos", icon="cancel")
                        raise ValueError("Las restricciones no contienen números enteros válidos")
                # Acceder al primer elemento de restr_entrys
                restr_entry = restr_entrys[0]
                if restr_entry[0].get().isdigit() and restr_entry[1].get().isdigit() and restr_entry[2].get().isdigit() and int(restr_entry[0].get()) and int(restr_entry[1].get()) and int(restr_entry[2].get()):
                    a = int(restr_entry[0].get())   # Valor de x1 en restricciones
                    a_list.append(a)
                    a = int(restr_entry[1].get())   # Valor de x2 en restricciones
                    a_list.append(a)
                    a = int(restr_entry[2].get())   # Valor de ind en restricciones
                    a_list.append(a)
                else:
                    CtkMessagebox(title="Error", message="Las restricciones no contienen números enteros válidos", icon="cancel")
                    raise ValueError("Las restricciones no contienen números enteros válidos")
                
                # Acceder al primer elemento de restr_entrys
                restr_entry = restr_entrys[1]
                if restr_entry[0].get().isdigit() and restr_entry[1].get().isdigit() and restr_entry[2].get().isdigit() and int(restr_entry[0].get()) and int(restr_entry[1].get()) and int(restr_entry[2].get()):
                    # Valor de x1 en el segundo restr_entry
                    b = int(restr_entry[0].get())
                    b_list.append(b)
                    # Valor de x2 en el segundo restr_entry
                    b = int(restr_entry[1].get())
                    b_list.append(b)
                    # Valor de ind en el segundo restr_entry
                    b = int(restr_entry[2].get())
                    b_list.append(b)
                else:
                    CtkMessagebox(title="Error", message="Las restricciones no contienen números enteros válidos", icon="cancel")
                    raise ValueError("Las restricciones no contienen números enteros válidos")
                
                if x1_entry.get().isdigit() and x2_entry.get().isdigit() and x3_entry.get().isdigit() and int(x1_entry.get()) != 0 and int(x2_entry.get()) != 0 and int(x3_entry.get()) != 0:
                    c_list.append(int(x1_entry.get()))
                    c_list.append(int(x2_entry.get()))
                    c_list.append(int(x3_entry.get()))
                else:
                    CtkMessagebox(title="Error", message="La función objetivo no son números enteros válidos", icon="cancel")
                    raise ValueError("La función objetivo no contiene números enteros válidos")
                print(a_list)
                print(b_list)
                print(c_list)
                print(x_valor[0])
                print(x_valor[1])
                if opcion == 1:
                    return a_list
                elif opcion == 2:
                    return b_list
                elif opcion == 3:
                    return c_list
                elif opcion == 4:
                    return x_valor[0]
                elif opcion == 5:
                    return x_valor[1]
                else:
                    return 3
            
        # Iniciar la verificación del cambio de pestaña
        inicio()
        
if __name__ == "__main__":
    app = App()
    # Cerrar la ventana completamente

    def cerrar_ventana():
        app.destroy()
    # Agregar un botón de cerrar a la ventana
    app.protocol("WM_DELETE_WINDOW", cerrar_ventana)
    app.mainloop()