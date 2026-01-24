import speech_recognition as sr
from speech_recognition import UnknownValueError


def listen():

    rec = sr.Recognizer()
    with sr.Microphone() as mic:
       rec.adjust_for_ambient_noise(mic)
       print('Fale algo e aguarde ...')
       audio = rec.listen(mic)
       try:
           rec.adjust_for_ambient_noise(mic,duration=1)
           texto = rec.recognize_google(audio, language="pt-BR")
       except UnknownValueError:
           texto="google is dumb"
       print(texto)
       return texto

listen()

