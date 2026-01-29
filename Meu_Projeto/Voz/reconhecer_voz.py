from tkinter.filedialog import askopenfilename
from Meu_Projeto.Automation.files_open import kit
from Meu_Projeto.Imagens.extração import ler_imagem
from Meu_Projeto.Automation.screenshots import *
from Meu_Projeto.Voz.tts import tts_say
from Meu_Projeto.Utils.utils import listen


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
        case _ :
            tts_say("Não percebi")















