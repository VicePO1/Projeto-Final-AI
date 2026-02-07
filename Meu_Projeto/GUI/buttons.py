import tkinter as tk
from Meu_Projeto.Voz.reconhecer_voz import identificar_inicial
from Meu_Projeto.Utils.utils import listen

def create_button_listen(jan):
    button_listen=tk.Button(jan,width=18,height=4,text="Listen",font=("Georgia",12),command=lambda:identificar_inicial(listen()))
    button_listen.place(x=115,y=100)

def create_button_ajuda(jan):
    button_ajuda=tk.Button(jan,width=6,height=2,text="Ajuda",font=("Georgia",5),bg="light blue",)
    button_ajuda.place(x=15,y=10)