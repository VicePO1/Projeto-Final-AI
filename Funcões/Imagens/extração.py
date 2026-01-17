import pytesseract
import cv2

def ler_imagem(imagem,caminho_tesseract):
    imagem = cv2.imread(imagem)
    caminho = caminho_tesseract
    pytesseract.pytesseract.tesseract_cmd = caminho
    texto = pytesseract.image_to_string(imagem)
    print(texto)

