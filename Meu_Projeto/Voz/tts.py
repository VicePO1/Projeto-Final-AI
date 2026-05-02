import pyttsx3 as tts

def tts_say(text):
   engine = tts.init()
   voices = engine.getProperty('voices')
   engine.setProperty('voice', voices[0].id)
   engine.say(text)
   engine.runAndWait()

