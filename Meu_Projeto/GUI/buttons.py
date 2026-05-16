import tkinter as tk
from Meu_Projeto.Voz.reconhecer_voz import identificar_inicial
from Meu_Projeto.Utils.utils import listen
from Meu_Projeto.GUI.messageboxes import *
from Meu_Projeto.GUI.labels import *
from Meu_Projeto.Imagens.whatsapp import *
from Meu_Projeto.GUI.entries import *
#from Meu_Projeto.Automation.screenshots import screenshot_parcial
from pywhatkit.core.exceptions import CountryCodeException
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

image_selec=None
image_path=None

def create_button_listen(jan):
    button_listen = tk.Button(jan,width=18,height=4,text="Listen",font=("Georgia",12),command=lambda:identificar_inicial(listen()))
    button_listen.place(x=115,y=100)

def create_button_ajuda(jan):
    button_ajuda = tk.Button(jan,width=6,height=2,text="Ajuda",font=("Georgia",5),bg="light blue",command=lambda:help_messagebox())
    button_ajuda.place(x=15,y=10)

#def create_button_submit():
    #button_submit = tk.Button(width=6, height=2, text="Submit", font=("Georgia", 5), bg="light blue",command=lambda:screenshot_parcial())
    #button_submit.place(x=15, y=10)

def create_button_grab_imagem(jan):
    button_grab_imagem = tk.Button(jan, width=15, height=3, text="Escolher imagem", font=("Georgia", 12),
                              command=lambda: get_imagem())
    button_grab_imagem.place(x=95, y=400)


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

def get_imagem():
    global image_selec, image_path
    image_path = askopenfilename()
    image_selec = ImageTk.PhotoImage(Image.open(image_path))
    change_label_imagem(image_selec)