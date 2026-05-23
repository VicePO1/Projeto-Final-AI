import tkinter as tk
from Meu_Projeto.GUI.messageboxes import *
from Meu_Projeto.Voz.reconhecer_voz import identificar_inicial
from Meu_Projeto.Utils.listen import listen
from Meu_Projeto.GUI.entries import *
from Meu_Projeto.Utils.janela_definicoes import *
#from Meu_Projeto.Automation.screenshots import screenshot_parcial

def create_button_listen(jan):
    button_listen = tk.Button(jan,width=18,height=4,text="Listen",font=("Georgia",12),command=lambda:identificar_inicial(listen()))
    button_listen.place(x=115,y=100)

def create_button_ajuda(jan):
    button_ajuda = tk.Button(jan,width=6,height=2,text="Ajuda",font=("Georgia",5),bg="light blue",command=lambda:help_messagebox())
    button_ajuda.place(x=15,y=10)

def create_button_defi(jan):
    button_defi = tk.Button(jan,width=8,height=2,text="Definições",font=("Georgia",5),bg="light blue",command=lambda:criar_janela_definicoes())
    button_defi.place(x=440,y=450)

#def create_button_submit():
    #button_submit = tk.Button(width=6, height=2, text="Submit", font=("Georgia", 5), bg="light blue",command=lambda:screenshot_parcial())
    #button_submit.place(x=15, y=10)




