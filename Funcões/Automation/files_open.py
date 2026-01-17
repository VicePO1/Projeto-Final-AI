from Funcões.Voz.tts import tts_say
import os

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