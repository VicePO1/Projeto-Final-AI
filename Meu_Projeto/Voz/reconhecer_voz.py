from tkinter.filedialog import askopenfilename
from Meu_Projeto.Automation.files_open import *
from Meu_Projeto.Imagens.extração import ler_imagem
from Meu_Projeto.Automation.screenshots import identificar_screenshot_size
from Meu_Projeto.Voz.tts import tts_say
from Meu_Projeto.GUI.labels import create_label_resultado
from Meu_Projeto.Automation.os_management import *
from Meu_Projeto.GUI.labels import delete_label_resultado
from time import sleep


def identificar_inicial(texto):
    match texto:
        case "kit":
            create_label_resultado(texto)
            tts_say("A abrir kit de programação")
            kit()
        case "captura":
            create_label_resultado(texto)
            tts_say("A preparar o screenshot")
            identificar_screenshot_size()
        case "ler imagem":
            create_label_resultado(texto)
            tts_say("Qual é a imagem")
            filename=askopenfilename()
            tts_say("Onde está o tesseract")
            tesseract= askopenfilename()
            create_label_resultado(ler_imagem(filename,tesseract))
        case "limpeza":
            create_label_resultado(texto)
            tts_say("Minimizing all windows")
            minimize_all()
        case "minimizar":
            create_label_resultado(texto)
            tts_say("Minimizar esta janela")
            minimize_all()
        case "abrir":
            create_label_resultado(texto)
            tts_say("Que app queres abrir")
            app=listen()
            open_app(app)
        case "":
            tts_say("Não ouvi o que disseste")
        case _ :
            create_label_resultado(texto)
            tts_say("Não percebi")













