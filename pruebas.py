import tkinter as tk

class ColorBox(tk.Canvas):
  
  def __init__(self, parent, *args, **kwargs):
    tk.Canvas.__init__(self, parent, *args, **kwargs)
    self.configure(width=100, height=100) # ajusta el tamaño del cuadro
    self.red = 0
    self.green = 0
    self.blue = 0
    self.draw()
  
  def draw(self):
    self.delete("all") # borra el contenido anterior
    color = f"#{self.red:02x}{self.green:02x}{self.blue:02x}" # convierte RGB a un formato de color de cadena
    self.create_rectangle(0, 0, self.winfo_width(), self.winfo_height(), fill=color)
  
  def set_color(self, red, green, blue):
    self.red = red
    self.green = green
    self.blue = blue
    self.draw()

class ColorPicker(tk.Frame):
  
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.red_var = tk.StringVar()
    self.green_var = tk.StringVar()
    self.blue_var = tk.StringVar()
    self.color_box = ColorBox(self, bd=2, relief="sunken")
    self.red_entry = tk.Entry(self, textvariable=self.red_var, width=5)
    self.green_entry = tk.Entry(self, textvariable=self.green_var, width=5)
    self.blue_entry = tk.Entry(self, textvariable=self.blue_var, width=5)
    self.red_label = tk.Label(self, text="Red")
    self.green_label = tk.Label(self, text="Green")
    self.blue_label = tk.Label(self, text="Blue")
    self.red_entry.bind("<Return>", self.update_color)
    self.green_entry.bind("<Return>", self.update_color)
    self.blue_entry.bind("<Return>", self.update_color)
    self.color_box.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
    self.red_label.grid(row=0, column=1, sticky="e")
    self.green_label.grid(row=1, column=1, sticky="e")
    self.blue_label.grid(row=2, column=1, sticky="e")
    self.red_entry.grid(row=0, column=2, padx=5, pady=5)
    self.green_entry.grid(row=1, column=2, padx=5, pady=5)
    self.blue_entry.grid(row=2, column=2, padx=5, pady=5)
    self.pack()
  
  def update_color(self, event):
    red = int(self.red_var.get())
    green = int(self.green_var.get())
    blue = int(self.blue_var.get())
    self.color_box.set_color(red, green, blue)

if __name__ == "__main__":
  root = tk.Tk()
  root.title("Color Picker")
  picker = ColorPicker(root)
  root.mainloop()
