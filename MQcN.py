import tkinter
import tkinter.messagebox
import customtkinter
import CTkMessagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Definir el modo del switch
        def cambiar_modos():
            if switch_var.get() == "on":
                switch_text.set("Maximización")
                # Funcion a maximizar
            else:
                switch_text.set("Minimización")
                # Funcion a minimizar
        #Graficar Maximizacion
        def graficar_maximizacion():
            limpiar()
            obtener_valores()
            n = int(self.num_restr_entry.get())  #Guardar el valor de n
            
            # Crear una figura de matplotlib
            fig = plt.Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)

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
            for p in points:
                ax.plot(p[0], p[1], 'r')
                
            # Destruir la figura anterior, si existe
            for widget in self.frame2.winfo_children():
                widget.destroy()
                
            # Agregar la figura al widget de la gráfica
            canvas = FigureCanvasTkAgg(fig, master=self.frame2)
            canvas.draw()
            canvas.get_tk_widget().pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True)
            concluir_maximizacion()
            
        #Concluir minimizacion
        def concluir_maximizacion():
            conclusiones = "Las conclusiones de la gráfica en maximizacion son ..."
            self.text_area.delete('1.0', customtkinter.END)
            self.text_area.insert(customtkinter.END, conclusiones)
            
        #Graficar Minimizacion - Hay que modificar esto para que haga la minimizacion
        def graficar_minimizacion():
            limpiar()
            obtener_valores()
            n = int(self.num_restr_entry.get())  #Guardar el valor de n
            
            # Crear una figura de matplotlib
            fig = plt.Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)

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
            for p in points:
                ax.plot(p[0], p[1], 'r')
                
            # Destruir la figura anterior, si existe
            for widget in self.frame2.winfo_children():
                widget.destroy()
                
            # Agregar la figura al widget de la gráfica
            canvas = FigureCanvasTkAgg(fig, master=self.frame2)
            canvas.draw()
            canvas.get_tk_widget().pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True)    
            concluir_minimizacion()
        #Concluir minimizacion
        def concluir_minimizacion():
            conclusiones = "Las conclusiones de la gráfica en minimizacion son ..."
            self.text_area.delete('1.0', customtkinter.END)
            self.text_area.insert(customtkinter.END, conclusiones)
        
        #Ventana
        self.title("Método Gráfico")
        self.geometry("1500x400")
        # Crear los marcos
        self.frame1 = customtkinter.CTkFrame(self, border_width=2)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame2 = customtkinter.CTkFrame(self, border_width=2)
        self.frame2.grid(row=0, column=1, sticky="nsew")
        self.frame3 = customtkinter.CTkFrame(self, border_width=2)
        self.frame3.grid(row=0, column=2, sticky="nsew")
        
        #Switch para cambiar entre el modo Maximizacion y Minimizacion
        switch_var = customtkinter.StringVar(value="on")
        switch_text = customtkinter.StringVar(value="Maximización")
        switch = customtkinter.CTkSwitch(master=self.frame1, textvariable=switch_text, command=cambiar_modos, variable=switch_var, onvalue="on", offvalue="off")
        switch.grid(row=0, column=0, columnspan=4, padx=10, pady=5)
        
        
        #Label para saber el modo
        cambiar_modos()
        self.label = customtkinter.CTkLabel(self.frame1, text="Función")
        self.label.grid(row=1,  column=0, columnspan=4, padx=10, pady=1)
        #Ingresar la funcion en Z
        self.z_label = customtkinter.CTkLabel(self.frame1, text="Z = ")
        self.z_label.grid(row=2, column=0, padx=10, pady=10)
        #ingresar la funcion en x1
        self.x1_entry = customtkinter.CTkEntry(self.frame1, width=50, placeholder_text="X1")
        self.x1_entry.grid(row=2, column=1, padx=10, pady=10)
        #Mas
        self.mas_label = customtkinter.CTkLabel(self.frame1, text="X1 +")
        self.mas_label.grid(row=2, column=2, padx=10, pady=10)
        #ingresar la funcion en x2
        self.x2_entry = customtkinter.CTkEntry(self.frame1, width=50, placeholder_text="X2")
        self.x2_entry.grid(row=2, column=3, padx=10, pady=10)
        
        #numero de restricciones
        self.num_restr_label = customtkinter.CTkLabel(self.frame1, text="Cantidad de Restricciones")
        self.num_restr_label.grid(row=3, column=0, columnspan=4, padx=2, pady=5)
        #n restricciones
        self.num_restr_entry = customtkinter.CTkEntry(self.frame1, placeholder_text="n")
        self.num_restr_entry.grid(row=4, column=0, columnspan=4, padx=2, pady=5)
        
        #Funcion para generar las restricciones
        restrs = [] #Guardar las label para eliminarlas
        restr_entrys = []   #Guardar las entradas para eliminarlas o leerlas
        def generar_restricciones():
            n_str = self.num_restr_entry.get()  #Obtener el valor de n
            eliminar_etiquetas()    #Limpiar todas las restricciones
            if n_str.isdigit(): #Si el valor de n es un digito
                n = int(n_str)  #Guardar el valor de n
                for i in range(n):  #Generar todas las entradas de las restricciones
                    restr = customtkinter.CTkLabel(self.frame1, text=f"Restricción {i+1}")
                    restr.grid(row=6+i, column=0, padx=10, pady=5)
                    restr_x1 = customtkinter.CTkEntry(self.frame1, placeholder_text="X1", width=50)
                    restr_x1.grid(row=6+i, column=2, padx=2, pady=5)
                    restr_x2 = customtkinter.CTkEntry(self.frame1, placeholder_text="X2", width=50)
                    restr_x2.grid(row=6+i, column=3, padx=2, pady=5)
                    restr_ind = customtkinter.CTkEntry(self.frame1, placeholder_text="Ind", width=50)
                    restr_ind.grid(row=6+i, column=4, padx=2, pady=5)
                    restrs.append(restr)
                    restr_entrys.append((restr_x1, restr_x2, restr_ind))  # agregar una tupla con las tres entradas de la restricción
                    if switch_var.get() == "on":
                        #Generar el boton para graficar maximizacion
                        generar_restr = customtkinter.CTkButton(self.frame1, text="Maximizar", command=graficar_maximizacion)
                        generar_restr.grid(row=6+n, column=0, columnspan=5, padx=10, pady=5)
                        restrs.append(generar_restr)
                    else:
                        #Generar el boton para graficar minimizacion
                        generar_restr = customtkinter.CTkButton(self.frame1, text="Minimizar", command=graficar_minimizacion)
                        generar_restr.grid(row=6+n, column=0, columnspan=5, padx=10, pady=5)
                        restrs.append(generar_restr)
                
                
            else:
                CTkMessagebox(title="Error", message="El número de restricciones no es un numero valido", icon="cancel")

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
        
        # Crear el botón de restricciones
        self.button_restr = customtkinter.CTkButton(self.frame1, text="Agregar", command=generar_restricciones)
        self.button_restr.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        self.button_eliminar = customtkinter.CTkButton(self.frame1, text="Eliminar", command=eliminar_etiquetas)
        self.button_eliminar.grid(row=5, column=2, columnspan=3, padx=2, pady=5)
        
        # Crear los widgets de la columna 3
        self.text_area = customtkinter.CTkTextbox(self.frame3, height=300, width=500)
        self.text_area.pack(side=customtkinter.TOP, pady=5)
            
if __name__ == "__main__":
    app = App()
    app.mainloop()
