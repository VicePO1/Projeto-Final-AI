import tkinter as tk
from Meu_Projeto.Voz.reconhecer_voz import identificar_inicial
from Meu_Projeto.Utils.utils import listen

def create_button_listen(jan):
    button_listen=tk.Button(jan,width=18,height=4,text="Listen",font=("Georgia",12),command=lambda:identificar_inicial(listen()))
    button_listen.place(x=115,y=100)