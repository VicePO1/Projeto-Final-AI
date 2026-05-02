from tkinter import messagebox

def help_messagebox():
    texto = ("Para utilizar este programa, clica no botão Listen, espera e depois diz uma destas palavras-chave para fazer a função designada:"
             "\n\nKit - abre o kit de programação"
             "\nScreenshot - Tira um screenshot total ou parcial"
             "\nLer imagem - mostra o texto dentro de uma imagem"
             "\nLimpeza - Minimiza todas as janelas"
             "\nAbrir - Abre a aplicação que tu queres")

    messagebox.showinfo("Bem-vindo!",texto)