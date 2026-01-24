#Imports
import pyttsx3 as tts

#Usa o tts para falar, text é o que vai dizer
def tts_say(text):
   engine = tts.init()
   voices = engine.getProperty('voices')
   engine.setProperty('voice', voices[0].id)
   engine.say(text)
   engine.runAndWait()

