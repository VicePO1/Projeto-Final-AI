from tkinter import messagebox

def help_messagebox():
    texto="Para utilizar este programa, clica no botão Listen e diz uma destas palavras-chave para fazer a função designada:\n\nKit - abre o kit de programação\nScreenshot - Tira um screenshot total ou parcial\nLer imagem - mostra o texto dentro de uma imagem"
    messagebox.showinfo("Bem-vindo!",texto)