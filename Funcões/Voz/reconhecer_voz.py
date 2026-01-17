from tkinter.filedialog import askopenfilename
from Funcões.Automation.files_open import kit
from Funcões.Imagens.extração import ler_imagem
from Funcões.Automation.screenshots import *
from Funcões.Voz.tts import tts_say
from utils import listen


def identificar_inicial(texto):
    match texto:
        case "kit":
            tts_say("A abrir kit de programação")
            kit()
        case "screenshot":
            identificar_screenshot_size()
        case "ler imagem":
            tts_say("Qual é a imagem")
            filename=askopenfilename()
            tts_say("Onde está o tesseract")
            tesseract= askopenfilename()
            ler_imagem(filename,tesseract)

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













