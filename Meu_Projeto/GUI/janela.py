import tkinter as tk

from Meu_Projeto.GUI.entries import create_entry_screenshot_size
from Meu_Projeto.GUI.labels import *
from Meu_Projeto.GUI.buttons import *


def janela_inicial():
   root=tk.Tk()
   root.configure(bg='lightblue')
   root.wm_resizable(False, False)
   root.wm_geometry("500x500")

   shark_art()
   create_titulo()
   create_button_listen(root)

   root.mainloop()




