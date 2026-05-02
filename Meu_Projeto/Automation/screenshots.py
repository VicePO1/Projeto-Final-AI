from Meu_Projeto.Voz.tts import tts_say
import pyautogui
from Meu_Projeto.Utils.utils import listen
from Meu_Projeto.GUI.entries import *
from Meu_Projeto.GUI.labels import label_entry_screenshot_size
#from Meu_Projeto.GUI.buttons import create_button_submit

def screenshot_total():
    scr=pyautogui.screenshot()
    scr.save(f"{identificar_screenshot_name()}.jpg")

def screenshot_parcial():
    x1,y1,x2,y2=create_entry_screenshot_size().get().split()
    scr=pyautogui.screenshot(region=(x1,y1,x2,y2))
    scr.save(f"{identificar_screenshot_name()}.jpg")

def identificar_screenshot_name():
    tts_say("Como se chama este screenshot?")
    nome_scr = listen()
    print(nome_scr)
    return nome_scr

def identificar_screenshot_size():
    tts_say("Screenshot total ou parcial")
    t_ou_p = listen()
    print(t_ou_p)
    if t_ou_p =="parcial":
       create_entry_screenshot_size()
       label_entry_screenshot_size()
    elif t_ou_p =="total":
        screenshot_total()
    else:
        tts_say("Não percebi")


