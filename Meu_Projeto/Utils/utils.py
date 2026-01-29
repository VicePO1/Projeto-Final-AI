import speech_recognition as sr
from speech_recognition import UnknownValueError
from Meu_Projeto.Voz.tts import tts_say


def listen():
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
       rec.adjust_for_ambient_noise(mic)
       tts_say('Fale algo e aguarde ...')
       audio = rec.listen(mic)
       try:
           rec.adjust_for_ambient_noise(mic,duration=1)
           texto = rec.recognize_google(audio, language="pt-BR")
       except UnknownValueError:
           texto="google is dumb"
       print(texto)
       return texto