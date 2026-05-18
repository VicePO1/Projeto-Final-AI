from Meu_Projeto.Voz.tts import tts_say
import pyautogui
from Meu_Projeto.Utils.listen import listen
from Meu_Projeto.GUI.entries import *
from Meu_Projeto.GUI.labels import label_entry_screenshot_size
#from Meu_Projeto.GUI.buttons import create_button_submit

def tirar_screenshot():
    scr=pyautogui.screenshot()
    scr.save(f"{identificar_screenshot_name()}.jpg")

def identificar_screenshot_name():
    tts_say("Como se chama este screenshot?")
    nome_scr = listen()
    print(nome_scr)
    return nome_scr




