from Meu_Projeto.Voz.tts import tts_say
import os

def kit():
    user=os.getlogin()

    pycharm=r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\JetBrains\PyCharm Community Edition 2024.3.1.1.lnk"
    github=fr"C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\GitHub, Inc\GitHub Desktop.lnk"
    vscode=fr"C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"

    if os.path.exists(pycharm):
        os.startfile(pycharm)
    else:
        tts_say("Não foi encontrado o PyCharm")

    if os.path.exists(github):
        os.startfile(github)
    else:
        tts_say("Não foi encontrado o Github")

    if os.path.exists(vscode):
        os.startfile(vscode)
    else:
        tts_say("Não foi encontrado o Visual Studio Code")
