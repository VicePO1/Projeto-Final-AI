import pywhatkit

def convert_ascii(image):
   art=pywhatkit.image_to_ascii_art(image)
   return art