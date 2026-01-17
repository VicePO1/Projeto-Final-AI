from Funcões.Voz.tts import tts_say
import pyautogui
from Funcões.Voz.reconhecer_voz import identificar_screenshot_name

def screenshot_total():
    tts_say("A tirar screenshot")
    scr=pyautogui.screenshot()
    scr.save(f"{identificar_screenshot_name()}.jpg")
    tts_say("Screenshot salvo")

def screenshot_parcial(x1,x2,y1,y2):
    tts_say("A tirar screenshot")
    scr=pyautogui.screenshot(region=(x1,y1,x2,y2))
    scr.save(identificar_screenshot_name())
    tts_say("Screenshot salvo")