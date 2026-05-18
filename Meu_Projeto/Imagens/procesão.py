import pywhatkit
from Meu_Projeto.Utils.utils import tts_say


def convert_ascii(image):
   art=pywhatkit.image_to_ascii_art(image)
   tts_say("Texto convertido")
   return art

