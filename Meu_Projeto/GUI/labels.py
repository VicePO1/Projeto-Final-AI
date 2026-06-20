import tkinter as tk
import os

img=None
label_resultado=None

user = os.getlogin()
with open(fr"Assets/shark.txt", "r") as file:
    sharkart = file.read()

def create_titulo(jan):
    titulo = tk.Label(jan,text = "Assistente Sharkcoders",bg = "light Blue",font = ("Georgia",18))
    titulo.place(x=85,y=30)

def shark_art(jan):
    shark_label = tk.Label(jan,text = sharkart,bg = "light Blue",font = ("Courier",2))
    shark_label.place(x=275,y=280)

def label_entry_screenshot_size():
    label_screenshot_size = tk.Label(text = "Escreva aqui:",bg = "light Blue")
    label_screenshot_size.place(x=50,y=275)

def create_label_resultado(texto_imagem):
    global label_resultado

    label_resultado=tk.Label(text = texto_imagem,bg = "light Blue")
    if texto_imagem != "":
       label_resultado.place(x = 30,y = 280)

def delete_label_resultado():
    global label_resultado
    while label_resultado!=None:
        label_resultado.destroy()
        label_resultado=None

def create_label_cont(jan):
    label_cont = tk.Label(jan,text = "Contacto: ",bg = "light Blue")
    label_cont.place(x = 50,y = 580)

def create_label_cap(jan):
    label_cap = tk.Label(jan,text = "Caption: ",bg = "light Blue")
    label_cap.place(x = 500,y = 50)

def create_label_imagem(jan):
    global label_imagem
    label_imagem = tk.Label(jan,text = "Imagem não selecionada",bg = "light Blue")
    label_imagem.place(x = 100,y = 50)

def change_label_imagem(img):
    label_imagem.config(image = img,text = "")
    label_imagem.image = img

