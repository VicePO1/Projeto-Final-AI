from tkinter.filedialog import askopenfilename
from Funcões.Automation.files_open import kit
from Funcões.Imagens.extração import ler_imagem
from Funcões.Automation.screenshots import *
from Funcões.Voz.tts import tts_say
from Utils.utils import listen


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














