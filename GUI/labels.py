import tkinter as tk

with open("shark.txt","r") as file:
    sharkart=file.read()

def título():
    titulo=tk.Label(text="Assistente Sharkcoders",bg="light Blue",font=("Arial",15))
    titulo.place(x=85,y=30)

def shark_art():
    shark_label=tk.Label(text=sharkart,bg="light Blue",font=("Courier",2))
    shark_label.place(x=225,y=230)



