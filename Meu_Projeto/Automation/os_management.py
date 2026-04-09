import pyautogui
import os
from Meu_Projeto.Utils.utils import listen

def minimize_all():
    pyautogui.hotkey("win","d")

def minimize():
    pyautogui.hotkey("win","down")