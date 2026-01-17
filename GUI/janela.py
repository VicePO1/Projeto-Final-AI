import tkinter as tk
from GUI.labels import *
from GUI.buttons import *

def janela_inicial():
   root=tk.Tk()
   root.configure(bg='lightblue')
   root.wm_resizable(False, False)
   root.wm_geometry("400x400")

   shark_art()
   título()
   button_listen()
   root.mainloop()


janela_inicial()




