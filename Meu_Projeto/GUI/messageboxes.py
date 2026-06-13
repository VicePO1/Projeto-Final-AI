from tkinter import messagebox

def help_messagebox():
    texto = ("Para utilizar este programa, clica no botão Listen, espera e depois diz uma destas palavras-chave para fazer a função designada:"
             "\n\nKit - abre o kit de programação"
             "\nCaptura - Tira um screenshot"
             "\nLer - Mostra o texto dentro de uma imagem"
             "\nLimpeza - Minimiza todas as janelas"
             "\nAbrir - Abre a aplicação que tu queres"
             "\nEnviar - Enviar uma imagem no Whatsapp, pode ter caption"
             "\nPerfil - Mostra alguma informação da tua conta (pode ser cofigurado pelo botão Definições)"
             "\nDesenhar - Converter uma imagem em ASCII"
             "\nMinimizar- Minimiza o programa"
             "\nFechar- Fecha o programa")

    messagebox.showinfo("Bem-vindo!",texto)