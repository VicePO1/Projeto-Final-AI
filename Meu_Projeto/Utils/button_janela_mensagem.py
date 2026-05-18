import tkinter as tk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
from Meu_Projeto.GUI.labels import change_label_imagem
from pywhatkit.core.exceptions import CountryCodeException
from Meu_Projeto.Imagens.whatsapp import *
from Meu_Projeto.GUI.entries import *
from tkinter import messagebox

image_selec=None
image_path=None

def create_button_grab_imagem(jan):
    button_grab_imagem = tk.Button(jan, width=15, height=3, text="Escolher imagem", font=("Georgia", 12),
                              command=lambda: get_imagem())
    button_grab_imagem.place(x=95, y=400)

def get_imagem():
    global image_selec, image_path
    image_path = askopenfilename()
    image_selec = ImageTk.PhotoImage(Image.open(image_path))
    change_label_imagem(image_selec)

def create_button_enviar(jan):
    global image_path
    button_enviar = tk.Button(jan, width=15, height=3, text="Enviar", font=("Georgia", 12),command=lambda: funcao_button_enviar(get_entry_cont(),image_path,get_entry_cap()))
    button_enviar.place(x=400, y=500)


def funcao_button_enviar(cont,image,caption):
    try:
        if caption!="":
            enviar_imagem_caption(f"+{cont}",image,caption)
        else:
            enviar_imagem(f"+{cont}",image)
    except CountryCodeException:
        messagebox.showerror("Erro",f"Erro ao enviar imagem")