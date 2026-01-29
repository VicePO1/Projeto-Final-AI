import tkinter as tk
import os

user=os.getlogin()
with open(fr"Assets/shark.txt", "r") as file:
    sharkart=file.read()

def título():
    titulo=tk.Label(text="Assistente Sharkcoders",bg="light Blue",font=("Georgia",18))
    titulo.place(x=85,y=30)

def shark_art():
    shark_label=tk.Label(text=sharkart,bg="light Blue",font=("Courier",2))
    shark_label.place(x=225,y=230)

def label_entry_screenshot_size():
    label_screenshot_size=tk.Label(text="Escreva aqui:",bg="light Blue")
    label_screenshot_size.place(x=50,y=270)



