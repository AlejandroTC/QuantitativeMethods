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

# Main
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        tabview = customtkinter.CTkTabview(master=self)
        tabview.pack(padx=20, pady=20)

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
    #Funciones para el cambio de modos
        # Definir el modo del switch
        def cambiar_modos():
            if switch_var.get() == "on":
                switch_text.set("Maximización")
                # Funcion a maximizar
            else:
                switch_text.set("Minimización")
                # Funcion a minimizar
                
        def cambiar_modos2():
            if switch_var2.get() == "on":
                switch_text2.set("Maximización")
                # Funcion a maximizar
            else:
                switch_text2.set("Minimización")
                # Funcion a minimizar
        # Cambiar el modo en cualquier momento
        def on_switch_change(*args):
            iniciar()
    #Funciones para graficar y concluir
    # Graficar Maximizacion
        def graficar_maximizacion():
            active_tab = tabview.get()
            if(active_tab == "Método Dual"):
                limpiar_dual()
                obtener_valores_dual()
                x1_valor = int(x_valor_dual[0])
                x2_valor = int(x_valor_dual[1])
                # Obtener los valores de la funcion objetivo
                # n = int(self.num_restr_entry.get())  # Guardar el valor de n
                n = int(3)  # Guardar el valor de n
                x1 = int(x1_valor)
                x2 = int(x2_valor)
                
            else:
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
            obtener_valores()
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
            concluir_maximizacion(max_x, max_y, x1_valor, x2_valor)

        # Concluir minimizacion
        def concluir_maximizacion(max_x=float, max_y=float, x1_valor=float, x2_valor=float):
            conclusiones = f"El punto que resuelve la funcion objetivo 'Z= {x1_valor}x_1 + {x2_valor}x_2'" \
                           f" esta dado en el punto ({round(max_x, 2)}, {round(max_y, 2)}), el cual es mostrado en la gráfica" \
                           f" y resuelve el problema de maximización"
            active_tab = tabview.get()
            if(active_tab == "Método Dual"):
                self.text_area_dual.delete('1.0', customtkinter.END)
                self.text_area_dual.insert(customtkinter.END, conclusiones)
            else:
                self.text_area.delete('1.0', customtkinter.END)
                self.text_area.insert(customtkinter.END, conclusiones)

        # Graficar Minimizacion
        def graficar_minimizacion():
            active_tab = tabview.get()
            if(active_tab == "Método Dual"):
                limpiar_dual()
                obtener_valores_dual()
                x1_valor = int(x_valor_dual[0])
                x2_valor = int(x_valor_dual[1])
                # Obtener los valores de la funcion objetivo
                # n = int(self.num_restr_entry.get())  # Guardar el valor de n
                n = int(3)  # Guardar el valor de n
                x1 = int(x1_valor)
                x2 = int(x2_valor)
                a_list = a_list_dual[:]
                b_list = b_list_dual[:]
                c_list = c_list_dual[:]
            else:
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

            for i, p in enumerate(points):
                ax.plot(p[0], p[1], color=colors[i])

            # Graficar el puntos
            ax.scatter(min_x, min_y, color='blue')
            # Agregar una etiqueta con el valor de min_x y min_y a la gráfica
            ax.annotate(f"({round(min_x,2)}, {round(min_y,2)})", xy=(min_x, min_y), xytext=(min_x + 0.2, min_y + 0.2), fontsize=8,color='blue')

            # Destruir la figura anterior, si existe
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
            concluir_minimizacion(min_x, min_y,x1_valor, x2_valor)

        # Concluir minimizacion
        def concluir_minimizacion(min_x=float, min_y=float, x1_valor=float, x2_valor=float):
            conclusiones = f"El punto que resuelve la funcion objetivo 'Z= {x1_valor}x_1 + {x2_valor}x_2'" \
                           f" esta dado en el punto ({round(min_x, 2)}, {round(min_y, 2)}), el cual es mostrado en la gráfica" \
                           f" y resuelve el problema de minimización."
            active_tab = tabview.get()
            if(active_tab == "Método Dual"):
                self.text_area_dual.delete('1.0', customtkinter.END)
                self.text_area_dual.insert(customtkinter.END, conclusiones)
            else:
                self.text_area.delete('1.0', customtkinter.END)
                self.text_area.insert(customtkinter.END, conclusiones)
            
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
        #Aviso dual 
        # Crear los widgets de la columna 3
        self.aviso = customtkinter.CTkTextbox(self.frame7, height=200, width=500, font=("Arial", 20))
        self.aviso.pack(side=customtkinter.TOP)
        dual = "El método dual se resuelve mediante el método" \
                f" gráfico, utilizando las variables de las dos restricciones para " \
                f" formar las restricciones 1, 2 y 3 en el método gráfico." \
                f" La solución se obtiene de la función objetivo del" \
                f" dual, mientras que la función objetivo en el gráfico" \
                f" se genera utilizando los resultados de las restricciones en el dual."
        self.aviso.delete('1.0', customtkinter.END)
        self.aviso.insert(customtkinter.END, dual)
            
        
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
        ruta_icono = os.path.join(CTkMessagebox.__path__[
                                  0], 'icons', 'info.png')
        # cargar la imagen
        img = Image.open(ruta_icono)
        img_resized = img.resize((15, 15))
        photo = customtkinter.CTkImage(img_resized)
        self.info = customtkinter.CTkButton(self.frame1, image=photo, fg_color="transparent", text='', width=20, height=20, command=open_toplevel)
        self.info.grid(row=0, column=0, padx=2, pady=5, sticky='w')
        
    #Crear el switch de modos para el Dual
        switch_var2 = customtkinter.StringVar(value="on")
        switch_var2.trace_add('write', on_switch_change)
        switch_text2 = customtkinter.StringVar(value="Maximización")
        switch2 = customtkinter.CTkSwitch(master=self.frame4, textvariable=switch_text2, variable=switch_var2, onvalue="on", offvalue="off", command=cambiar_modos2)
        switch2.grid(row=0, column=0, padx=10, pady=10)
        # Configura que la colunma 0 tenga un weight especifico
        self.frame4.columnconfigure(0, weight=1)
        # Boton para una ventana con nuestra info
        self.toplevel_window = None
        def open_toplevel():
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow()  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()  # if window exists focus it
        ruta_icono = os.path.join(CTkMessagebox.__path__[
                                  0], 'icons', 'info.png')
        # cargar la imagen
        img = Image.open(ruta_icono)
        img_resized = img.resize((15, 15))
        photo = customtkinter.CTkImage(img_resized)
        self.info = customtkinter.CTkButton(
            self.frame4, image=photo, fg_color="transparent", text='', width=20, height=20, command=open_toplevel)
        self.info.grid(row=0, column=0, padx=2, pady=5, sticky='w')
    
    #Widgets y funcionamiento del Metodo Grafico
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
            if n_str.isdigit(): #Si el valor de n es un digito
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
                a = int(restr_entry[0].get())
                b = int(restr_entry[1].get())
                c = int(restr_entry[2].get())
                a_list.append(a)
                b_list.append(b)
                c_list.append(c)
                
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
        
    #Widgets y funcionamiento del Metodo Grafico
        # Crear un sub-frame para la funcion Z
        z_frame_dual = customtkinter.CTkFrame(self.frame4, fg_color="transparent")
        z_frame_dual.grid(row=2, column=0, columnspan=5, padx=10, pady=10)
        # Label Z
        z_label = customtkinter.CTkLabel(z_frame_dual, text="Z =")
        z_label.grid(row=0, column=0)
        # Entry para x1
        x1_entry_dual = customtkinter.CTkEntry(z_frame_dual, width=40, placeholder_text="X1")
        x1_entry_dual.grid(row=0, column=1, padx=5)
        # Label X1 y +
        mas_label = customtkinter.CTkLabel(z_frame_dual, text="X1 +")
        mas_label.grid(row=0, column=2, padx=5)
        # Entry para x2
        x2_entry_dual = customtkinter.CTkEntry(z_frame_dual, width=40, placeholder_text="X2")
        x2_entry_dual.grid(row=0, column=3, padx=5)
        # Label para x2
        mas_label2 = customtkinter.CTkLabel(z_frame_dual, text="X2 + ")
        mas_label2.grid(row=0, column=4, padx=10)
        # Entry para x3
        x3_entry_dual = customtkinter.CTkEntry(z_frame_dual, width=40, placeholder_text="X3")
        x3_entry_dual.grid(row=0, column=5, padx=5)
        # Label para x2
        mas_label3 = customtkinter.CTkLabel(z_frame_dual, text="X3")
        mas_label3.grid(row=0, column=6, padx=10)
        
        # Crear un sub-frame para las entrys de restricciones
        restrentry_frame_dual = customtkinter.CTkFrame(self.frame4, fg_color="transparent", width=400, height=150)
        restrentry_frame_dual.grid(row=3, column=0, columnspan=5, padx=10, pady=10)
        # Crear un sub-frame para las entrys de restricciones
        do_frame_dual = customtkinter.CTkFrame(self.frame4, fg_color="transparent", width=400, height=150)
        do_frame_dual.grid(row=4, column=0, columnspan=5, padx=10, pady=10)
        
        # Funcion para generar las restricciones
        restrs_dual = []  # Guardar las label para eliminarlas
        restr_entrys_dual = []  # Guardar las entradas para eliminarlas o leerlas
        
        def iniciar():
            def generar_restricciones_dual():

                def res1():
                    restr_dual = customtkinter.CTkLabel(restrentry_frame_dual, text="Restricción 1", text_color=colors[1])
                    restr_dual.grid(row=0, column=0, columnspan=7,padx=10, pady=5, sticky="ns")

                    restr_x1_dual = customtkinter.CTkEntry(restrentry_frame_dual, placeholder_text="X1", width=50)
                    restr_x1_dual.grid(row=1, column=0, padx=2, pady=5, sticky="ns")

                    masr_label_dual = customtkinter.CTkLabel(restrentry_frame_dual, text="X1 +", text_color=colors[1])
                    masr_label_dual.grid(row=1, column=1, padx=5)

                    restr_x2_dual = customtkinter.CTkEntry(restrentry_frame_dual, placeholder_text="X2", width=50)
                    restr_x2_dual.grid(row=1, column=2, padx=2, pady=5, sticky="ns")

                    masr_label2_dual = customtkinter.CTkLabel(restrentry_frame_dual, text="X2 +", text_color=colors[1])
                    masr_label2_dual.grid(row=1, column=3, padx=5)

                    restr_x3_dual = customtkinter.CTkEntry(restrentry_frame_dual, placeholder_text="X2", width=50)
                    restr_x3_dual.grid(row=1, column=4, padx=2, pady=5, sticky="ns")

                    if switch_var.get() == "on":
                        equalr_label_dual = customtkinter.CTkLabel(restrentry_frame_dual, text="X3 <=", text_color=colors[1])
                    else:
                        equalr_label_dual = customtkinter.CTkLabel(restrentry_frame_dual, text="X3 >=", text_color=colors[1])
                    equalr_label_dual.grid(row=1, column=5, padx=5)

                    restr_ind_dual = customtkinter.CTkEntry(
                        restrentry_frame_dual, placeholder_text="Ind", width=50)
                    restr_ind_dual.grid(row=1, column=6, padx=2,pady=5, sticky="ns")

                    restrs_dual.append(restr_dual)
                    restr_entrys_dual.append((restr_x1_dual, restr_x2_dual, restr_x3_dual, restr_ind_dual, masr_label_dual, equalr_label_dual, masr_label2_dual))
                def res2():
                    restr_dual = customtkinter.CTkLabel(restrentry_frame_dual, text="Restricción 2", text_color=colors[2])
                    restr_dual.grid(row=2, column=0, columnspan=7, padx=10, pady=5, sticky="ns")

                    restr_x1_dual = customtkinter.CTkEntry(restrentry_frame_dual, placeholder_text="X1", width=50)
                    restr_x1_dual.grid(row=3, column=0, padx=2, pady=5, sticky="ns")

                    masr_label_dual = customtkinter.CTkLabel(restrentry_frame_dual, text="X1 +", text_color=colors[2])
                    masr_label_dual.grid(row=3, column=1, padx=5)

                    restr_x2_dual = customtkinter.CTkEntry(restrentry_frame_dual, placeholder_text="X2", width=50)
                    restr_x2_dual.grid(row=3, column=2, padx=2, pady=5, sticky="ns")

                    masr_label2_dual = customtkinter.CTkLabel(restrentry_frame_dual, text="X2 +", text_color=colors[2])
                    masr_label2_dual.grid(row=3, column=3, padx=5)

                    restr_x3_dual = customtkinter.CTkEntry(restrentry_frame_dual, placeholder_text="X2", width=50)
                    restr_x3_dual.grid(row=3, column=4, padx=2, pady=5, sticky="ns")

                    if switch_var.get() == "on":
                        equalr_label_dual = customtkinter.CTkLabel(restrentry_frame_dual, text="X3 <=", text_color=colors[2])
                    else:
                        equalr_label_dual = customtkinter.CTkLabel(restrentry_frame_dual, text="X3 >=", text_color=colors[2])
                    equalr_label_dual.grid(row=3, column=5, padx=5)

                    restr_ind_dual = customtkinter.CTkEntry(restrentry_frame_dual, placeholder_text="Ind", width=50)
                    restr_ind_dual.grid(row=3, column=6, padx=2,pady=5, sticky="ns")

                    restrs_dual.append(restr_dual)
                    restr_entrys_dual.append((restr_x1_dual, restr_x2_dual, restr_x3_dual, restr_ind_dual, masr_label_dual, equalr_label_dual, masr_label2_dual))

                res1()
                res2()

                if switch_var2.get() == "on":
                    # Generar el boton para graficar maximizacion
                    generar_restr_dual = customtkinter.CTkButton(do_frame_dual, text="Maximizar", command=graficar_minimizacion)
                    generar_restr_dual.grid(row=0, column=0, padx=10,pady=5, sticky="ns")
                    restrs_dual.append(generar_restr_dual)
                else:
                    # Generar el boton para graficar minimizacion
                    generar_restr_dual = customtkinter.CTkButton(do_frame_dual, text="Minimizar", command=graficar_maximizacion)
                    generar_restr_dual.grid(row=0, column=0, padx=10,pady=5, sticky="ns")
                    restrs_dual.append(generar_restr_dual)

            generar_restricciones_dual()
        iniciar()
        
        # Eliminar
        def eliminar_etiquetas_dual():
            for restr_dual in restrs_dual:
                restr_dual.destroy()
            for restr_entry_dual in restr_entrys_dual:
                for entry in restr_entry_dual:
                    entry.destroy()
            restr_entrys_dual.clear()
            restrs_dual.clear()
            iniciar()
        
        self.button_eliminar_dual = customtkinter.CTkButton(do_frame_dual, text="Reiniciar", command=eliminar_etiquetas_dual)
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
            for restr_entry_dual in restr_entrys_dual:
                x = int(restr_entry_dual[3].get())  # Valor de funcion objetivo Z
                x_valor_dual.append(x)

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
                c_list_dual.append(int(x1_entry_dual.get()))

            if x2_entry_dual.get().isdigit():  # Verificar si el valor de x2_entry es un dígito
                # Agregar el valor a la lista
                c_list_dual.append(int(x2_entry_dual.get()))

            if x3_entry_dual.get().isdigit():  # Verificar si el valor de x3_entry es un dígito
                # Agregar el valor a la lista
                c_list_dual.append(int(x3_entry_dual.get()))
                
            a_list = a_list_dual[:]
            b_list = b_list_dual[:]
            c_list = c_list_dual[:]
                
        # Crear los widgets de la columna 3
        self.text_area_dual = customtkinter.CTkTextbox(self.frame6, height=200, width=500, font=("Arial", 20))
        self.text_area_dual.pack(side=customtkinter.TOP)
        
app = App()
app.mainloop()
