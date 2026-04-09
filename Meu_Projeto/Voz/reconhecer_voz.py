from tkinter.filedialog import askopenfilename
from Meu_Projeto.Automation.files_open import *
from Meu_Projeto.Imagens.extração import ler_imagem
from Meu_Projeto.Automation.screenshots import identificar_screenshot_size
from Meu_Projeto.Voz.tts import tts_say
from Meu_Projeto.GUI.labels import create_label_resultado
from Meu_Projeto.Automation.os_management import *
from Meu_Projeto.GUI.labels import delete_label_resultado


def identificar_inicial(texto):
    create_label_resultado(texto)
    match texto:
        case "kit":
            tts_say("A abrir kit de programação")
            delete_label_resultado()
            kit()
        case "captura":
            tts_say("A preparar o screenshot")
            delete_label_resultado()
            identificar_screenshot_size()
        case "ler imagem":
            tts_say("Qual é a imagem")
            delete_label_resultado()
            filename=askopenfilename()
            tts_say("Onde está o tesseract")
            tesseract= askopenfilename()
            create_label_resultado(ler_imagem(filename,tesseract))
        case "limpeza":
            tts_say("Minimizing all windows")
            delete_label_resultado()
            minimize_all()
        case "minimizar":
            tts_say("Minimizar esta janela")
            delete_label_resultado()
            minimize_all()
        case "abrir":
            tts_say("Que app queres abrir")
            app=listen()
            delete_label_resultado()
            open_app(app)
        case "":
            tts_say("Não ouvi o que disseste")
            delete_label_resultado()
        case _ :
            tts_say("Não percebi")
            delete_label_resultado()













