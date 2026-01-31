from Meu_Projeto.Voz.tts import tts_say
import pyautogui
from Meu_Projeto.Utils.utils import listen
from Meu_Projeto.GUI.entries import *
from Meu_Projeto.GUI.labels import label_entry_screenshot_size

def screenshot_total():
    scr=pyautogui.screenshot()
    scr.save(f"{identificar_screenshot_name()}.jpg")

def screenshot_parcial(x1,x2,y1,y2):
    scr=pyautogui.screenshot(region=(x1,y1,x2,y2))
    scr.save(identificar_screenshot_name())

def identificar_screenshot_name():
    tts_say("Como se chama este screenshot?")
    nome_scr=listen()
    return nome_scr

def identificar_screenshot_size():
    tts_say("Screenshot total ou parcial")
    t_ou_p=listen()
    if t_ou_p=="parcial":
       create_entry_screenshot_size()
       label_entry_screenshot_size()

       x1,x2,y1,y2=get_entry_screenshot_size().split(",",3)
       print(x1,x2,y1,y2)
       screenshot_parcial(x1,x2,y1,y2)
    elif t_ou_p=="total":
        screenshot_total()
    else:
        tts_say("Não percebi")

