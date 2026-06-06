from tkinter.filedialog import askopenfilename
from Meu_Projeto.Automation.files_open import *
from Meu_Projeto.Imagens.extração import ler_imagem
from Meu_Projeto.Imagens.procesão import convert_ascii
from Meu_Projeto.Automation.screenshots import tirar_screenshot
from Meu_Projeto.Voz.tts import tts_say
from Meu_Projeto.GUI.labels import create_label_resultado
from Meu_Projeto.Automation.os_management import *
from Meu_Projeto.Utils.janela_mensagem import criar_janela_mensagem
from Meu_Projeto.Utils.listen import listen
from Meu_Projeto.API.github import info_perfil

def identificar_inicial(texto):
    match texto:
        case "kit":
            create_label_resultado(texto)
            tts_say("A abrir kit de programação")
            kit()

        case "captura":
            create_label_resultado(texto)
            tts_say("A preparar o screenshot")
            tirar_screenshot()

        case "ler":
            create_label_resultado(texto)
            tts_say("Qual é a imagem")
            try:
                filename=askopenfilename()
                tts_say("Onde está o tesseract")
                tesseract = askopenfilename()  # C:\Program Files\Tesseract-OCR\tesseract
                create_label_resultado(ler_imagem(filename, tesseract))
            except AttributeError:
                tts_say("Erro ao ler imagem")

        case "limpeza":
            create_label_resultado(texto)
            tts_say("Minimizing all windows")
            minimize_all()

        case "minimizar":
            create_label_resultado(texto)
            tts_say("Minimizar esta janela")
            minimize()

        case "abrir":
            create_label_resultado(texto)
            tts_say("Que app queres abrir")
            app=listen()
            if app!="":
                open_app(app)
            else:
                tts_say("Não ouvi o que disseste")

        case "desenhar":
            create_label_resultado(texto)
            tts_say("Qual é a imagem")
            try:
                filename = askopenfilename()
                art=convert_ascii(filename)
                with open(f"{filename}.ascii.txt","w") as file:
                    file.write(art)
            except AttributeError:
                tts_say("Erro ao ler imagem")

        case "enviar":
            create_label_resultado(texto)
            criar_janela_mensagem()

        case "perfil":
            create_label_resultado(texto)
            tts_say("A mostrar perfil")
            create_label_resultado(info_perfil())

        case "fechar":
            create_label_resultado(texto)
            tts_say("Bye-Bye")
            quit()

        case "":
            tts_say("Não ouvi o que disseste")

        case _ :
            create_label_resultado(texto)
            tts_say("Não percebi")