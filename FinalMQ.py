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
                
        # Crear los widgets de la columna 3
        self.text_area_dual = customtkinter.CTkTextbox(self.frame6, height=200, width=500, font=("Arial", 20))
        self.text_area_dual.pack(side=customtkinter.TOP)
        
app = App()
app.mainloop()
