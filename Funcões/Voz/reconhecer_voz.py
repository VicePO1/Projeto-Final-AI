import speech_recognition as sr
from tts import tts_say

def listen_inicial():
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
       rec.adjust_for_ambient_noise(mic)
       print('Fale algo e aguarde ...')
       audio = rec.listen(mic)
       texto = rec.recognize_google(audio, language="pt-BR")

    match texto:
        case "kit":
            tts_say("A abrir kit de programação")
        case ""


listen_inicial()