import tkinter as tk
from Meu_Projeto.GUI.labels import *
from Meu_Projeto.Utils.button_janela_mensagem import create_button_grab_imagem
from Meu_Projeto.Utils.button_janela_mensagem import create_button_enviar
from Meu_Projeto.GUI.entries import create_entry_cont
from Meu_Projeto.GUI.entries import create_entry_cap

def criar_janela_mensagem():
    janela_mensagem = tk.Tk()
    janela_mensagem.configure(bg='lightblue')
    janela_mensagem.wm_resizable(False, False)
    janela_mensagem.wm_geometry("700x700")

    create_button_grab_imagem(janela_mensagem)
    create_entry_cont(janela_mensagem)
    create_label_cont(janela_mensagem)
    create_entry_cap(janela_mensagem)
    create_label_cap(janela_mensagem)
    create_label_imagem(janela_mensagem)
    create_button_enviar(janela_mensagem)