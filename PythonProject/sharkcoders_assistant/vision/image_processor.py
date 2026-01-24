#!/usr/bin/env python3
"""
SharkCoders Assistant - Processador de Imagens
Módulo para processamento e manipulação de imagens.
"""

import sys
from pathlib import Path
from typing import Tuple, Optional, Union
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from PIL import Image, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ Pillow não instalado. Instale: pip install Pillow")

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️ OpenCV não instalado. Instale: pip install opencv-python")

from utils import logger


class ImageProcessor:
    """
    Processador de imagens.
    Usa Pillow e OpenCV para manipulação de imagens.
    """
    
    def __init__(self):
        """Inicializa o processador de imagens."""
        self.pil_available = PIL_AVAILABLE
        self.cv2_available = CV2_AVAILABLE
        
        if not PIL_AVAILABLE and not CV2_AVAILABLE:
            logger.warning("Nenhuma biblioteca de imagem disponível")
    
    def load_image(self, path: Union[str, Path]) -> Optional[Image.Image]:
        """
        Carrega uma imagem de um ficheiro.
        
        Args:
            path: Caminho do ficheiro
        
        Returns:
            Imagem PIL ou None se falhar
        """
        if not PIL_AVAILABLE:
            logger.error("Pillow não disponível")
            return None
        
        try:
            path = Path(path)
            if not path.exists():
                logger.error(f"Ficheiro não encontrado: {path}")
                return None
            
            image = Image.open(path)
            logger.debug(f"Imagem carregada: {path} ({image.size})")
            return image
        except Exception as e:
            logger.error(f"Erro ao carregar imagem: {e}")
            return None
    
    def save_image(self, image: Image.Image, path: Union[str, Path], 
                   quality: int = 95) -> bool:
        """
        Guarda uma imagem num ficheiro.
        
        Args:
            image: Imagem PIL
            path: Caminho de destino
            quality: Qualidade (para JPEG)
        
        Returns:
            True se guardado com sucesso
        """
        try:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            if path.suffix.lower() in ['.jpg', '.jpeg']:
                image.save(path, quality=quality)
            else:
                image.save(path)
            
            logger.debug(f"Imagem guardada: {path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao guardar imagem: {e}")
            return False
    
    def to_grayscale(self, image: Image.Image) -> Image.Image:
        """
        Converte imagem para escala de cinzentos.
        
        Args:
            image: Imagem PIL
        
        Returns:
            Imagem em escala de cinzentos
        """
        return image.convert('L')
    
    def to_rgb(self, image: Image.Image) -> Image.Image:
        """
        Converte imagem para RGB.
        
        Args:
            image: Imagem PIL
        
        Returns:
            Imagem em RGB
        """
        return image.convert('RGB')
    
    def binarize(self, image: Image.Image, threshold: int = 128) -> Image.Image:
        """
        Binariza a imagem (preto e branco).
        
        Args:
            image: Imagem PIL
            threshold: Limiar de binarização (0-255)
        
        Returns:
            Imagem binarizada
        """
        # Converter para cinzento primeiro
        gray = self.to_grayscale(image)
        
        # Aplicar threshold
        return gray.point(lambda x: 255 if x > threshold else 0, mode='1')
    
    def adaptive_binarize(self, image: Image.Image) -> Optional[Image.Image]:
        """
        Binarização adaptativa usando OpenCV.
        Melhor para documentos com iluminação irregular.
        
        Args:
            image: Imagem PIL
        
        Returns:
            Imagem binarizada ou None se OpenCV não disponível
        """
        if not CV2_AVAILABLE:
            logger.warning("OpenCV não disponível, usando binarização simples")
            return self.binarize(image)
        
        try:
            # Converter para numpy/OpenCV
            cv_image = self.pil_to_cv2(image)
            
            # Converter para cinzento
            if len(cv_image.shape) == 3:
                gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
            else:
                gray = cv_image
            
            # Binarização adaptativa
            binary = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )
            
            # Converter de volta para PIL
            return self.cv2_to_pil(binary)
        except Exception as e:
            logger.error(f"Erro na binarização adaptativa: {e}")
            return self.binarize(image)
    
    def denoise(self, image: Image.Image, strength: int = 10) -> Optional[Image.Image]:
        """
        Remove ruído da imagem.
        
        Args:
            image: Imagem PIL
            strength: Força da remoção de ruído
        
        Returns:
            Imagem sem ruído
        """
        if CV2_AVAILABLE:
            try:
                cv_image = self.pil_to_cv2(image)
                
                if len(cv_image.shape) == 3:
                    denoised = cv2.fastNlMeansDenoisingColored(cv_image, None, strength, strength, 7, 21)
                else:
                    denoised = cv2.fastNlMeansDenoising(cv_image, None, strength, 7, 21)
                
                return self.cv2_to_pil(denoised)
            except Exception as e:
                logger.warning(f"Erro no denoise OpenCV: {e}")
        
        # Fallback com Pillow
        return image.filter(ImageFilter.MedianFilter(size=3))
    
    def adjust_contrast(self, image: Image.Image, factor: float = 1.5) -> Image.Image:
        """
        Ajusta o contraste da imagem.
        
        Args:
            image: Imagem PIL
            factor: Factor de contraste (1.0 = sem alteração)
        
        Returns:
            Imagem com contraste ajustado
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    def adjust_brightness(self, image: Image.Image, factor: float = 1.2) -> Image.Image:
        """
        Ajusta o brilho da imagem.
        
        Args:
            image: Imagem PIL
            factor: Factor de brilho (1.0 = sem alteração)
        
        Returns:
            Imagem com brilho ajustado
        """
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    def adjust_sharpness(self, image: Image.Image, factor: float = 2.0) -> Image.Image:
        """
        Ajusta a nitidez da imagem.
        
        Args:
            image: Imagem PIL
            factor: Factor de nitidez
        
        Returns:
            Imagem mais nítida
        """
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    def resize(self, image: Image.Image, width: int = None, height: int = None,
               maintain_aspect: bool = True) -> Image.Image:
        """
        Redimensiona a imagem.
        
        Args:
            image: Imagem PIL
            width: Nova largura (opcional)
            height: Nova altura (opcional)
            maintain_aspect: Manter proporções
        
        Returns:
            Imagem redimensionada
        """
        original_width, original_height = image.size
        
        if width and height and not maintain_aspect:
            new_size = (width, height)
        elif width:
            ratio = width / original_width
            new_size = (width, int(original_height * ratio))
        elif height:
            ratio = height / original_height
            new_size = (int(original_width * ratio), height)
        else:
            return image
        
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    def crop(self, image: Image.Image, left: int, top: int, 
             right: int, bottom: int) -> Image.Image:
        """
        Recorta uma região da imagem.
        
        Args:
            image: Imagem PIL
            left, top: Canto superior esquerdo
            right, bottom: Canto inferior direito
        
        Returns:
            Imagem recortada
        """
        return image.crop((left, top, right, bottom))
    
    def rotate(self, image: Image.Image, angle: float, 
               expand: bool = True) -> Image.Image:
        """
        Roda a imagem.
        
        Args:
            image: Imagem PIL
            angle: Ângulo em graus (positivo = anti-horário)
            expand: Expandir para não cortar
        
        Returns:
            Imagem rodada
        """
        return image.rotate(angle, expand=expand, resample=Image.Resampling.BICUBIC)
    
    def deskew(self, image: Image.Image) -> Optional[Image.Image]:
        """
        Corrige inclinação da imagem (para documentos).
        
        Args:
            image: Imagem PIL
        
        Returns:
            Imagem corrigida
        """
        if not CV2_AVAILABLE:
            logger.warning("OpenCV necessário para deskew")
            return image
        
        try:
            cv_image = self.pil_to_cv2(image)
            
            # Converter para cinzento
            if len(cv_image.shape) == 3:
                gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
            else:
                gray = cv_image
            
            # Binarizar
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Encontrar ângulo
            coords = np.column_stack(np.where(binary > 0))
            angle = cv2.minAreaRect(coords)[-1]
            
            # Corrigir ângulo
            if angle < -45:
                angle = 90 + angle
            elif angle > 45:
                angle = angle - 90
            
            # Rodar se necessário
            if abs(angle) > 0.5:
                (h, w) = cv_image.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                rotated = cv2.warpAffine(cv_image, M, (w, h),
                    flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                return self.cv2_to_pil(rotated)
            
            return image
        except Exception as e:
            logger.error(f"Erro no deskew: {e}")
            return image
    
    def prepare_for_ocr(self, image: Image.Image) -> Image.Image:
        """
        Prepara imagem para OCR aplicando sequência de processamento otimizada.
        
        Args:
            image: Imagem PIL original
        
        Returns:
            Imagem processada e pronta para OCR
        """
        logger.info("A preparar imagem para OCR...")
        
        # 1. Converter para RGB se necessário
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 2. Redimensionar se muito pequena
        width, height = image.size
        if width < 300 or height < 300:
            scale = max(300 / width, 300 / height)
            image = self.resize(image, width=int(width * scale))
        
        # 3. Converter para escala de cinzentos
        image = self.to_grayscale(image)
        
        # 4. Remover ruído (se OpenCV disponível)
        if CV2_AVAILABLE:
            image = self.denoise(image, strength=5)
        
        # 5. Ajustar contraste
        image = self.adjust_contrast(image, factor=1.5)
        
        # 6. Binarização adaptativa (se OpenCV disponível)
        if CV2_AVAILABLE:
            image = self.adaptive_binarize(image)
        else:
            image = self.binarize(image, threshold=150)
        
        logger.debug("Imagem preparada para OCR")
        return image
    
    def pil_to_cv2(self, pil_image: Image.Image) -> 'np.ndarray':
        """
        Converte imagem PIL para formato OpenCV (numpy array).
        
        Args:
            pil_image: Imagem PIL
        
        Returns:
            Array numpy (BGR para OpenCV)
        """
        if not CV2_AVAILABLE:
            raise ImportError("OpenCV não disponível")
        
        # Converter para RGB se necessário
        if pil_image.mode == 'L':
            return np.array(pil_image)
        
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        return np.array(pil_image)
    
    def cv2_to_pil(self, cv_image: 'np.ndarray') -> Image.Image:
        """
        Converte imagem OpenCV para PIL.
        
        Args:
            cv_image: Array numpy
        
        Returns:
            Imagem PIL
        """
        if not PIL_AVAILABLE:
            raise ImportError("Pillow não disponível")
        
        if len(cv_image.shape) == 2:
            # Escala de cinzentos
            return Image.fromarray(cv_image)
        else:
            # Cor - OpenCV usa BGR, PIL usa RGB
            return Image.fromarray(cv_image)
    
    def get_image_info(self, image: Image.Image) -> dict:
        """
        Obtém informação sobre uma imagem.
        
        Args:
            image: Imagem PIL
        
        Returns:
            Dicionário com informação
        """
        return {
            "width": image.size[0],
            "height": image.size[1],
            "mode": image.mode,
            "format": image.format,
        }


# Instância global
image_processor = ImageProcessor()


if __name__ == "__main__":
    # Teste do processador de imagens
    print("=" * 50)
    print("🖼️ Teste do Processador de Imagens")
    print("=" * 50)
    
    print(f"\n📦 Pillow disponível: {PIL_AVAILABLE}")
    print(f"📦 OpenCV disponível: {CV2_AVAILABLE}")
    
    if PIL_AVAILABLE:
        # Criar imagem de teste
        test_image = Image.new('RGB', (200, 100), color='white')
        
        print(f"\n📊 Info da imagem de teste:")
        info = image_processor.get_image_info(test_image)
        for k, v in info.items():
            print(f"   {k}: {v}")
        
        # Testar operações
        print("\n🔧 A testar operações:")
        
        gray = image_processor.to_grayscale(test_image)
        print(f"   ✅ Escala de cinzentos: {gray.mode}")
        
        resized = image_processor.resize(test_image, width=100)
        print(f"   ✅ Redimensionado: {resized.size}")
        
        contrast = image_processor.adjust_contrast(test_image, 1.5)
        print(f"   ✅ Contraste ajustado")
        
        prepared = image_processor.prepare_for_ocr(test_image)
        print(f"   ✅ Preparado para OCR: {prepared.mode}")
    
    print("\n✅ Teste concluído!")
