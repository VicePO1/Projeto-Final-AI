import pytesseract
import cv2
import pywhatkit

def ler(imagem,caminho_tesseract):
    imagem = cv2.imread(imagem)
    caminho = caminho_tesseract
    pytesseract.pytesseract.tesseract_cmd = caminho
    texto = pytesseract.image_to_string(imagem)
    print(texto)

def convert(image):
   art=pywhatkit.image_to_ascii_art(image)
   return art