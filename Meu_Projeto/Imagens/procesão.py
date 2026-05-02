import pywhatkit
import cv2

def convert_ascii(image):
   art=pywhatkit.image_to_ascii_art(image)
   return art

def monochrome(imageI):
    imageF=cv2.imread(imageI, 0)
    return imageF