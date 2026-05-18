import speech_recognition as sr
from speech_recognition import UnknownValueError
from Meu_Projeto.Voz.tts import tts_say
import tkinter as tk
from Meu_Projeto.GUI.labels import *
from Meu_Projeto.GUI.buttons import *
from Meu_Projeto.GUI.entries import create_entry_cont
from Meu_Projeto.GUI.entries import create_entry_cap

def listen():
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
       rec.adjust_for_ambient_noise(mic)
       tts_say('Fale algo e aguarde ...')
       audio = rec.listen(mic)
       try:
           rec.adjust_for_ambient_noise(mic,duration=1)
           texto = rec.recognize_google(audio,language="pt-BR")
       except UnknownValueError:
           texto=""
       return texto

def criar_janela_mensagem():
    janela_mensagem = tk.Tk()
    janela_mensagem.configure(bg='lightblue')
    janela_mensagem.wm_resizable(False, False)
    janela_mensagem.wm_geometry("700x700")

    create_button_grab_imagem(janela_mensagem)
    create_entry_cont(janela_mensagem)
    create_label_cont(janela_mensagem)
    create_entry_cap(janela_mensagem)
    create_label_cap(janela_mensagem)
    create_label_imagem(janela_mensagem)
    create_button_enviar(janela_mensagem)