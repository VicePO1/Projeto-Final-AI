import pywhatkit as what

def enviar_imagem(cont,image):
    what.sendwhats_image(cont,image)

def enviar_imagen_caption(cont,imagen,caption):
    what.sendwhats_image(cont,imagen,caption)