import tkinter as tk


def criar_janela_definicoes():
    global janela_definicoes
    janela_definicoes = tk.Toplevel()
    janela_definicoes.configure(bg='lightblue')
    janela_definicoes.wm_resizable(False, False)
    janela_definicoes.wm_geometry("400x400")

    criar_label_account(janela_definicoes)
    criar_entry_account(janela_definicoes)
    criar_button_confirm(janela_definicoes)


def criar_label_account(jan):
    label_account = tk.Label(jan, text="Account Github:",bg='lightblue')
    label_account.place(x=20, y=100)

def criar_entry_account(jan):
    global entry_account
    entry_account = tk.Entry(jan,width=30)
    entry_account.place(x=20, y=150)

def criar_button_confirm(jan):
    button_confirm=tk.Button(jan,text="Confirmar",command=lambda:funcao_button_confirm(),font=("Georgia",12))
    button_confirm.place(x=250, y=300)

def funcao_button_confirm():
    global janela_definicoes
    global entry_account
    with open("Assets/account_github.txt","w") as file:
        file.write(entry_account.get())
    janela_definicoes.destroy()
