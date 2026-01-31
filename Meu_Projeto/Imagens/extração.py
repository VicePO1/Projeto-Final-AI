import pytesseract
import cv2
from Meu_Projeto.Voz.tts import tts_say

def ler_imagem(imagem_sub,caminho_tesseract):
    imagem = cv2.imread(imagem_sub)
    caminho = caminho_tesseract
    pytesseract.pytesseract.tesseract_cmd = caminho
    texto = pytesseract.image_to_string(imagem)
    if texto=="":
        tts_say("Não há texto na imagem")
        return texto
    else:
        tts_say("Texto identificado")
        return texto

