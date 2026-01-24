import pywhatkit

def convert(image):
   art=pywhatkit.image_to_ascii_art(image)
   return art