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



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        tabview = customtkinter.CTkTabview(master=self)
        tabview.pack(padx=20, pady=20)

        # Crear pestañas en el CTkTabview
        tab1 = tabview.add("Tab 1")
        tab2 = tabview.add("Tab 2")
        # Función para obtener la pestaña activa
        def get_active_tab():
            active_tab = tabview.get()
            print("Pestaña activa:", active_tab)

        # Botón para obtener la pestaña activa
        button = customtkinter.CTkButton(self, text="Obtener pestaña activa", command=get_active_tab)
        button.pack(pady=10)

app = App()
app.mainloop()