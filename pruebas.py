import customtkinter as ctk

def switch_callback():
    if switch_var.get() == "on":
        switch_text.set("Switch: ON")
    else:
        switch_text.set("Switch: OFF")

app = ctk.CTk()

switch_var = ctk.StringVar(value="on")
switch_text = ctk.StringVar(value="Switch: ON")
switch = ctk.CTkSwitch(app, textvariable=switch_text, command=switch_callback, variable=switch_var, onvalue="on", offvalue="off")
switch.pack(pady=10)

app.mainloop()
