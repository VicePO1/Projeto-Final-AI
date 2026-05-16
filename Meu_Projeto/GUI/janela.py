import tkinter as tk

from Meu_Projeto.GUI.labels import *
from Meu_Projeto.GUI.buttons import *



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










