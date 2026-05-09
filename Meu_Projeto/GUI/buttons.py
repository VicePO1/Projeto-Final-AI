import tkinter as tk
from Meu_Projeto.Voz.reconhecer_voz import identificar_inicial
from Meu_Projeto.Utils.utils import listen
from Meu_Projeto.GUI.messageboxes import *
from Meu_Projeto.GUI.labels import *
from Meu_Projeto.Imagens.whatsapp import *
from Meu_Projeto.GUI.entries import *
#from Meu_Projeto.Automation.screenshots import screenshot_parcial

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
                              command=lambda: change_label_imagem())
    button_grab_imagem.place(x=95, y=400)

def create_button_enviar(jan):
    button_enviar = tk.Button(jan, width=15, height=3, text="Enviar", font=("Georgia", 12),)
    button_enviar.place(x=400, y=500)

def funcao_button_enviar(cont,image,caption):
    if caption!="":
        enviar_imagem_caption(cont,image,caption)
    else:
        enviar_imagem(cont,image)