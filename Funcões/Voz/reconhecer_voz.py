import speech_recognition as sr
from tts import tts_say
from Funcões.automation import *

def listen():
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
       rec.adjust_for_ambient_noise(mic)
       print('Fale algo e aguarde ...')
       audio = rec.listen(mic)
       texto = rec.recognize_google(audio, language="pt-BR")
       return texto

def identificar_inicial(texto):
    match texto:
        case "kit":
            tts_say("A abrir kit de programação")
            kit()
        case "screenshot":
            identificar_screenshot_size()

def identificar_screenshot_size():
    tts_say("O screenshot é parcial ou total?")
    p_ou_t=listen()
    match p_ou_t:
        case "total":
            screenshot_total()
        case "parcial":
            tts_say("Quantos pixels tem horizontalmente?")
            pixh=listen()
            tts_say("Quantos pixels tem verticalmente?")
            pixv=listen()
            tts_say("Onde é horizontalmente o pixel do canto superior esquerdo do screenshot?")
            pixoh = listen()
            tts_say("Onde é vertocalmente o pixel do canto superior esquerdo do screenshot?")
            pixov = listen()

            screenshot_parcial(pixh,pixv,pixoh,pixov)

def identificar_screenshot_name():
    tts_say("Como se chama este screenshot?")
    nome_scr=listen()
    return nome_scr











