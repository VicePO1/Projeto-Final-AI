#!/usr/bin/env python3
"""
SharkCoders Assistant - Motor OCR
Módulo para reconhecimento óptico de caracteres.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, List, Union
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("⚠️ pytesseract não instalado. Instale: pip install pytesseract")

from config import OCR_CONFIG
from utils import logger


class OCREngine:
    """
    Motor de OCR usando Tesseract.
    Extrai texto de imagens.
    """
    
    def __init__(self):
        """Inicializa o motor OCR."""
        self.available = TESSERACT_AVAILABLE and PIL_AVAILABLE
        self.language = OCR_CONFIG.get("language", "por")
        self.config = OCR_CONFIG.get("config", "--oem 3 --psm 6")
        
        # Configurar caminho do Tesseract no Windows
        tesseract_path = OCR_CONFIG.get("tesseract_path")
        if tesseract_path and TESSERACT_AVAILABLE:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        if self.available:
            self._verify_installation()
    
    def _verify_installation(self) -> bool:
        """Verifica se o Tesseract está instalado correctamente."""
        try:
            version = pytesseract.get_tesseract_version()
            logger.info(f"Tesseract versão: {version}")
            return True
        except Exception as e:
            logger.error(f"Tesseract não encontrado: {e}")
            logger.info("Instale o Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
            self.available = False
            return False
    
    def extract_text(self, image: Union[Image.Image, str, Path], 
                     preprocess: bool = False) -> str:
        """
        Extrai texto de uma imagem.
        
        Args:
            image: Imagem PIL ou caminho do ficheiro
            preprocess: Se deve pré-processar a imagem
        
        Returns:
            Texto extraído
        """
        if not self.available:
            logger.error("OCR não disponível. Instale Tesseract e pytesseract.")
            return ""
        
        try:
            # Carregar imagem se for caminho
            if isinstance(image, (str, Path)):
                image = Image.open(image)
            
            # Pré-processar se pedido
            if preprocess:
                from .image_processor import image_processor
                image = image_processor.prepare_for_ocr(image)
            
            # Extrair texto
            logger.info("A extrair texto...")
            text = pytesseract.image_to_string(
                image,
                lang=self.language,
                config=self.config,
            )
            
            # Limpar texto
            text = text.strip()
            
            if text:
                logger.success(f"Texto extraído: {len(text)} caracteres")
            else:
                logger.warning("Nenhum texto encontrado")
            
            return text
            
        except Exception as e:
            logger.error(f"Erro no OCR: {e}")
            return ""
    
    def extract_text_with_details(self, image: Union[Image.Image, str, Path],
                                   preprocess: bool = False) -> Dict:
        """
        Extrai texto com informação detalhada (confiança, posições).
        
        Args:
            image: Imagem PIL ou caminho
            preprocess: Se deve pré-processar
        
        Returns:
            Dicionário com texto e detalhes
        """
        if not self.available:
            return {"text": "", "words": [], "confidence": 0}
        
        try:
            # Carregar imagem se necessário
            if isinstance(image, (str, Path)):
                image = Image.open(image)
            
            if preprocess:
                from .image_processor import image_processor
                image = image_processor.prepare_for_ocr(image)
            
            # Extrair dados detalhados
            data = pytesseract.image_to_data(
                image,
                lang=self.language,
                config=self.config,
                output_type=pytesseract.Output.DICT,
            )
            
            # Processar resultados
            words = []
            confidences = []
            
            for i in range(len(data['text'])):
                text = data['text'][i].strip()
                conf = int(data['conf'][i])
                
                if text and conf > 0:
                    words.append({
                        "text": text,
                        "confidence": conf,
                        "left": data['left'][i],
                        "top": data['top'][i],
                        "width": data['width'][i],
                        "height": data['height'][i],
                    })
                    confidences.append(conf)
            
            # Calcular confiança média
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Extrair texto completo
            full_text = pytesseract.image_to_string(image, lang=self.language, config=self.config)
            
            return {
                "text": full_text.strip(),
                "words": words,
                "word_count": len(words),
                "confidence": round(avg_confidence, 2),
            }
            
        except Exception as e:
            logger.error(f"Erro no OCR detalhado: {e}")
            return {"text": "", "words": [], "confidence": 0}
    
    def extract_text_from_regions(self, image: Union[Image.Image, str, Path],
                                   regions: List[tuple]) -> List[Dict]:
        """
        Extrai texto de regiões específicas da imagem.
        
        Args:
            image: Imagem PIL ou caminho
            regions: Lista de tuplas (left, top, right, bottom)
        
        Returns:
            Lista de dicionários com texto de cada região
        """
        if not self.available:
            return []
        
        try:
            if isinstance(image, (str, Path)):
                image = Image.open(image)
            
            results = []
            for i, (left, top, right, bottom) in enumerate(regions):
                # Recortar região
                region = image.crop((left, top, right, bottom))
                
                # Extrair texto
                text = self.extract_text(region)
                
                results.append({
                    "region_index": i,
                    "bounds": (left, top, right, bottom),
                    "text": text,
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Erro ao extrair regiões: {e}")
            return []
    
    def get_text_boxes(self, image: Union[Image.Image, str, Path]) -> List[Dict]:
        """
        Obtém as caixas delimitadoras do texto detectado.
        
        Args:
            image: Imagem PIL ou caminho
        
        Returns:
            Lista de caixas com texto
        """
        if not self.available:
            return []
        
        try:
            if isinstance(image, (str, Path)):
                image = Image.open(image)
            
            # Obter caixas
            boxes = pytesseract.image_to_boxes(image, lang=self.language)
            
            result = []
            for box in boxes.splitlines():
                parts = box.split()
                if len(parts) >= 5:
                    result.append({
                        "char": parts[0],
                        "left": int(parts[1]),
                        "bottom": int(parts[2]),
                        "right": int(parts[3]),
                        "top": int(parts[4]),
                    })
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao obter caixas: {e}")
            return []
    
    def set_language(self, language: str):
        """
        Define o idioma do OCR.
        
        Args:
            language: Código do idioma (ex: 'por', 'eng', 'por+eng')
        """
        self.language = language
        logger.info(f"Idioma OCR definido: {language}")
    
    def get_available_languages(self) -> List[str]:
        """
        Lista os idiomas disponíveis no Tesseract.
        
        Returns:
            Lista de códigos de idioma
        """
        if not self.available:
            return []
        
        try:
            languages = pytesseract.get_languages()
            return languages
        except Exception as e:
            logger.error(f"Erro ao obter idiomas: {e}")
            return []
    
    def is_available(self) -> bool:
        """Verifica se o OCR está disponível."""
        return self.available


# Instância global
ocr_engine = OCREngine()


if __name__ == "__main__":
    # Teste do motor OCR
    print("=" * 50)
    print("🔤 Teste do Motor OCR")
    print("=" * 50)
    
    print(f"\n📦 pytesseract disponível: {TESSERACT_AVAILABLE}")
    print(f"📦 Pillow disponível: {PIL_AVAILABLE}")
    print(f"✅ OCR disponível: {ocr_engine.is_available()}")
    
    if ocr_engine.is_available():
        # Listar idiomas
        print("\n🌍 Idiomas disponíveis:")
        languages = ocr_engine.get_available_languages()
        for lang in languages[:10]:
            print(f"   • {lang}")
        
        # Criar imagem de teste com texto
        if PIL_AVAILABLE:
            from PIL import Image, ImageDraw, ImageFont
            
            # Criar imagem simples
            test_image = Image.new('RGB', (400, 100), color='white')
            draw = ImageDraw.Draw(test_image)
            
            try:
                # Tentar usar fonte do sistema
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            draw.text((20, 30), "SharkCoders Assistant", fill='black', font=font)
            
            print("\n🔍 A testar extração de texto...")
            text = ocr_engine.extract_text(test_image)
            
            if text:
                print(f"   Texto extraído: '{text}'")
            else:
                print("   ⚠️ Nenhum texto extraído (pode ser problema de fonte)")
    else:
        print("\n❌ OCR não disponível")
        print("   1. Instale pytesseract: pip install pytesseract")
        print("   2. Instale Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   3. Configure o caminho no config.py")
    
    print("\n✅ Teste concluído!")
