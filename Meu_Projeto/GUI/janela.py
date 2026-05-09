import tkinter as tk

from Meu_Projeto.GUI.labels import *
from Meu_Projeto.GUI.buttons import *
from Meu_Projeto.GUI.entries import create_entry_cont
from Meu_Projeto.GUI.entries import create_entry_cap



def janela_inicial():
   root=tk.Tk()
   root.configure(bg='lightblue')
   root.wm_resizable(False, False)
   root.wm_geometry("500x500")

   shark_art(root)
   create_titulo(root)
   create_button_listen(root)
   create_button_ajuda(root)

   root.mainloop()

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








