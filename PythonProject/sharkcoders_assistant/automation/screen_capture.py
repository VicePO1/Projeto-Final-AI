#!/usr/bin/env python3
"""
SharkCoders Assistant - Captura de Ecrã
Módulo para tirar screenshots.
"""

import sys
import time
from pathlib import Path
from typing import Tuple, Optional, List
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pyautogui
    from PIL import Image
    CAPTURE_AVAILABLE = True
except ImportError:
    CAPTURE_AVAILABLE = False
    print("⚠️ Dependências não instaladas. Instale: pip install PyAutoGUI Pillow")

from config import SCREENSHOTS_DIR, AUTOMATION_CONFIG
from utils import logger, get_timestamp, ensure_dir


class ScreenCapture:
    """
    Classe para captura de ecrã.
    Permite tirar screenshots completos ou de regiões específicas.
    """
    
    def __init__(self):
        """Inicializa o capturador de ecrã."""
        self.available = CAPTURE_AVAILABLE
        self.screenshots_dir = ensure_dir(SCREENSHOTS_DIR)
        self.last_capture_path: Optional[Path] = None
        self.last_capture_image: Optional[Image.Image] = None
    
    def capture_full_screen(self, save: bool = True) -> Tuple[Optional[Image.Image], Optional[Path]]:
        """
        Captura o ecrã completo.
        
        Args:
            save: Se deve guardar o ficheiro
        
        Returns:
            Tupla (imagem PIL, caminho do ficheiro) ou (None, None) se falhar
        """
        if not self.available:
            logger.error("Captura não disponível. Instale: pip install PyAutoGUI Pillow")
            return None, None
        
        try:
            # Pequeno delay para permitir esconder janelas
            delay = AUTOMATION_CONFIG.get("screenshot_delay", 0.5)
            time.sleep(delay)
            
            # Capturar
            logger.info("A capturar ecrã completo...")
            screenshot = pyautogui.screenshot()
            
            self.last_capture_image = screenshot
            
            if save:
                # Guardar com timestamp
                filename = f"screenshot_{get_timestamp()}.png"
                filepath = self.screenshots_dir / filename
                screenshot.save(filepath)
                self.last_capture_path = filepath
                logger.success(f"Captura guardada: {filepath}")
                return screenshot, filepath
            
            return screenshot, None
            
        except Exception as e:
            logger.error(f"Erro na captura: {e}")
            return None, None
    
    def capture_region(self, x: int, y: int, width: int, height: int, 
                       save: bool = True) -> Tuple[Optional[Image.Image], Optional[Path]]:
        """
        Captura uma região específica do ecrã.
        
        Args:
            x: Coordenada X do canto superior esquerdo
            y: Coordenada Y do canto superior esquerdo
            width: Largura da região
            height: Altura da região
            save: Se deve guardar o ficheiro
        
        Returns:
            Tupla (imagem PIL, caminho do ficheiro)
        """
        if not self.available:
            logger.error("Captura não disponível")
            return None, None
        
        try:
            logger.info(f"A capturar região: ({x}, {y}) {width}x{height}")
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            self.last_capture_image = screenshot
            
            if save:
                filename = f"screenshot_region_{get_timestamp()}.png"
                filepath = self.screenshots_dir / filename
                screenshot.save(filepath)
                self.last_capture_path = filepath
                logger.success(f"Captura de região guardada: {filepath}")
                return screenshot, filepath
            
            return screenshot, None
            
        except Exception as e:
            logger.error(f"Erro na captura de região: {e}")
            return None, None
    
    def capture_window(self, title: str = None, save: bool = True) -> Tuple[Optional[Image.Image], Optional[Path]]:
        """
        Captura uma janela específica (por título).
        Nota: Funcionalidade limitada em algumas plataformas.
        
        Args:
            title: Título parcial da janela
            save: Se deve guardar o ficheiro
        
        Returns:
            Tupla (imagem PIL, caminho do ficheiro)
        """
        if not self.available:
            return None, None
        
        try:
            # Tentar encontrar janela
            windows = pyautogui.getWindowsWithTitle(title) if title else []
            
            if windows:
                window = windows[0]
                # Capturar região da janela
                return self.capture_region(
                    window.left, window.top,
                    window.width, window.height,
                    save=save
                )
            else:
                logger.warning(f"Janela não encontrada: {title}")
                # Capturar ecrã completo como fallback
                return self.capture_full_screen(save=save)
                
        except Exception as e:
            logger.error(f"Erro na captura de janela: {e}")
            return self.capture_full_screen(save=save)
    
    def list_captures(self, limit: int = 10) -> List[Path]:
        """
        Lista as últimas capturas guardadas.
        
        Args:
            limit: Número máximo de ficheiros a retornar
        
        Returns:
            Lista de caminhos ordenados por data (mais recente primeiro)
        """
        try:
            captures = list(self.screenshots_dir.glob("screenshot_*.png"))
            captures.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return captures[:limit]
        except Exception as e:
            logger.error(f"Erro ao listar capturas: {e}")
            return []
    
    def get_last_capture(self) -> Tuple[Optional[Image.Image], Optional[Path]]:
        """
        Retorna a última captura feita.
        
        Returns:
            Tupla (imagem PIL, caminho do ficheiro)
        """
        return self.last_capture_image, self.last_capture_path
    
    def delete_capture(self, filepath: Path) -> bool:
        """
        Remove uma captura.
        
        Args:
            filepath: Caminho do ficheiro a remover
        
        Returns:
            True se removido com sucesso
        """
        try:
            if filepath.exists():
                filepath.unlink()
                logger.info(f"Captura removida: {filepath}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover captura: {e}")
            return False
    
    def clear_old_captures(self, days: int = 7) -> int:
        """
        Remove capturas antigas.
        
        Args:
            days: Remover capturas mais antigas que X dias
        
        Returns:
            Número de ficheiros removidos
        """
        try:
            import time
            threshold = time.time() - (days * 24 * 60 * 60)
            removed = 0
            
            for capture in self.screenshots_dir.glob("screenshot_*.png"):
                if capture.stat().st_mtime < threshold:
                    capture.unlink()
                    removed += 1
            
            if removed:
                logger.info(f"Removidas {removed} capturas antigas")
            
            return removed
        except Exception as e:
            logger.error(f"Erro ao limpar capturas: {e}")
            return 0
    
    def get_capture_info(self, filepath: Path) -> dict:
        """
        Obtém informação sobre uma captura.
        
        Args:
            filepath: Caminho do ficheiro
        
        Returns:
            Dicionário com informação
        """
        try:
            if not filepath.exists():
                return {}
            
            stat = filepath.stat()
            
            # Abrir para obter dimensões
            with Image.open(filepath) as img:
                width, height = img.size
            
            return {
                "path": str(filepath),
                "name": filepath.name,
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "width": width,
                "height": height,
                "created": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            }
        except Exception as e:
            logger.error(f"Erro ao obter info: {e}")
            return {}


# Instância global
screen_capture = ScreenCapture()


if __name__ == "__main__":
    # Teste de captura de ecrã
    print("=" * 50)
    print("📸 Teste de Captura de Ecrã")
    print("=" * 50)
    
    if not CAPTURE_AVAILABLE:
        print("❌ Captura não disponível")
        print("   Instale: pip install PyAutoGUI Pillow")
        sys.exit(1)
    
    # Capturar ecrã completo
    print("\n📸 A capturar ecrã em 2 segundos...")
    time.sleep(2)
    
    image, path = screen_capture.capture_full_screen()
    
    if image and path:
        print(f"✅ Captura guardada: {path}")
        
        # Mostrar info
        info = screen_capture.get_capture_info(path)
        print(f"   Dimensões: {info.get('width')}x{info.get('height')}")
        print(f"   Tamanho: {info.get('size_kb')} KB")
    else:
        print("❌ Falha na captura")
    
    # Listar capturas
    print("\n📋 Últimas capturas:")
    for capture in screen_capture.list_captures(5):
        print(f"   • {capture.name}")
    
    print("\n✅ Teste concluído!")
