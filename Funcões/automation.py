from Voz.tts import tts_say
import os
import pyautogui


def kit():
    try:
        os.system(r"C\:Program Files\JetBrains\PyCharm 2025.2.2\bin\pycharm64.exe")
    except FileNotFoundError:
        tts_say("Não foi encontrado o Pycharm")

    try:
        os.system(r"C\Users\Vicente Faria\AppData\Local\GitHubDesktop\GitHubDesktop.exe")
    except FileNotFoundError:
        tts_say("Não foi encontrado o GithubDesktop")

def screenshot_total():
    scr=pyautogui.screenshot()
    return scr

def screenshot_parcial(x1,x2,y1,y2):
    scr=pyautogui.screenshot(region=(x1,y1,x2,y2))




