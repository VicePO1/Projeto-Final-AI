import tkinter as tk
import os

user=os.getlogin()
with open(fr"Assets/shark.txt", "r") as file:
    sharkart=file.read()

def create_titulo():
    titulo=tk.Label(text="Assistente Sharkcoders",bg="light Blue",font=("Georgia",18))
    titulo.place(x=85,y=30)

def shark_art():
    shark_label=tk.Label(text=sharkart,bg="light Blue",font=("Courier",2))
    shark_label.place(x=275,y=280)

def label_entry_screenshot_size():
    label_screenshot_size=tk.Label(text="Escreva aqui:",bg="light Blue")
    label_screenshot_size.place(x=50,y=275)

def create_label_resultado(texto_imagem):
    global label_resultado

    label_resultado=tk.Label(text=texto_imagem,bg="light Blue")
    if texto_imagem!="":
       label_resultado.place(x=50,y=280)

def delete_label_resultado():
    label_resultado.pack_forget()