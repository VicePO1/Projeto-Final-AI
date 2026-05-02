import tkinter as tk

from Meu_Projeto.GUI.labels import *
from Meu_Projeto.GUI.buttons import create_button_listen
from Meu_Projeto.GUI.buttons import create_button_ajuda


def janela_inicial():
   root=tk.Tk()
   root.configure(bg='lightblue')
   root.wm_resizable(False, False)
   root.wm_geometry("500x500")

   shark_art()
   create_titulo()
   create_button_listen(root)
   create_button_ajuda(root)

   root.mainloop()




