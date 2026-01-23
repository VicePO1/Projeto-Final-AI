from Funcões.Voz.tts import tts_say
import pyautogui
from Utils.utils import listen

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
