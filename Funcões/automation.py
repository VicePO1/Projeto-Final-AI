from Voz.tts import tts_say
from Voz.reconhecer_voz import identificar_screenshot_name
import os
import pyautogui


def kit():
    try:
        os.system(r"C\:Program Files\JetBrains\PyCharm 2025.2.2\bin\pycharm64.exe")
    except FileNotFoundError:
        tts_say("Não foi encontrado o Pycharm")
    try:
        user=os.getlogin()
        os.system(fr"C\Users\{user}\AppData\Local\GitHubDesktop\GitHubDesktop.exe")
    except FileNotFoundError:
        tts_say("Não foi encontrado o GithubDesktop")

def screenshot_total():
    scr=pyautogui.screenshot()
    scr.save(identificar_screenshot_name())

def screenshot_parcial(x1,x2,y1,y2):
    scr=pyautogui.screenshot(region=(x1,y1,x2,y2))
    scr.save(identificar_screenshot_name())






