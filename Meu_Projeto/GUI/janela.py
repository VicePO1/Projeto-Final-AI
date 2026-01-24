import tkinter as tk

from Meu_Projeto.GUI.entries import create_entry_screenshot_size
from Meu_Projeto.GUI.labels import *
from Meu_Projeto.GUI.buttons import *


def janela_inicial():
   root=tk.Tk()
   root.configure(bg='lightblue')
   root.wm_resizable(False, False)
   root.wm_geometry("400x400")

   shark_art()
   título()
   create_button_listen()

   root.mainloop()


janela_inicial()




