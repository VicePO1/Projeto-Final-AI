#!/usr/bin/env python3
"""
SharkCoders Assistant - Controlo de Rato e Teclado
Módulo para automação de inputs.
"""

import sys
import time
from pathlib import Path
from typing import Tuple, List, Optional
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    # Configurações de segurança
    pyautogui.FAILSAFE = True  # Mover rato para canto aborta
    pyautogui.PAUSE = 0.1  # Pausa entre ações
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️ PyAutoGUI não instalado. Instale: pip install PyAutoGUI")

from config import AUTOMATION_CONFIG
from utils import logger


class MouseController:
    """
    Controlador de rato.
    Permite mover, clicar e arrastar o rato.
    """
    
    def __init__(self):
        """Inicializa o controlador de rato."""
        self.available = PYAUTOGUI_AVAILABLE
        
        if self.available:
            # Obter tamanho do ecrã
            self.screen_width, self.screen_height = pyautogui.size()
            logger.debug(f"Ecrã detectado: {self.screen_width}x{self.screen_height}")
    
    def get_position(self) -> Tuple[int, int]:
        """
        Obtém a posição actual do rato.
        
        Returns:
            Tupla (x, y) com coordenadas
        """
        if not self.available:
            return (0, 0)
        
        return pyautogui.position()
    
    def move_to(self, x: int, y: int, duration: float = 0.5):
        """
        Move o rato para uma posição.
        
        Args:
            x: Coordenada X
            y: Coordenada Y
            duration: Duração do movimento em segundos
        """
        if not self.available:
            logger.error("PyAutoGUI não disponível")
            return
        
        try:
            pyautogui.moveTo(x, y, duration=duration)
            logger.debug(f"Rato movido para ({x}, {y})")
        except Exception as e:
            logger.error(f"Erro ao mover rato: {e}")
    
    def move_relative(self, dx: int, dy: int, duration: float = 0.25):
        """
        Move o rato relativamente à posição actual.
        
        Args:
            dx: Deslocamento em X
            dy: Deslocamento em Y
            duration: Duração do movimento
        """
        if not self.available:
            return
        
        try:
            pyautogui.moveRel(dx, dy, duration=duration)
            logger.debug(f"Rato movido +({dx}, {dy})")
        except Exception as e:
            logger.error(f"Erro ao mover rato: {e}")
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = "left", clicks: int = 1):
        """
        Clica com o rato.
        
        Args:
            x: Coordenada X (None para posição actual)
            y: Coordenada Y (None para posição actual)
            button: 'left', 'right' ou 'middle'
            clicks: Número de cliques
        """
        if not self.available:
            return
        
        try:
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
            pos = f"({x}, {y})" if x and y else "posição actual"
            logger.debug(f"Clique {button} em {pos}")
        except Exception as e:
            logger.error(f"Erro ao clicar: {e}")
    
    def double_click(self, x: Optional[int] = None, y: Optional[int] = None):
        """
        Faz duplo clique.
        
        Args:
            x: Coordenada X
            y: Coordenada Y
        """
        self.click(x, y, clicks=2)
    
    def right_click(self, x: Optional[int] = None, y: Optional[int] = None):
        """
        Faz clique com botão direito.
        
        Args:
            x: Coordenada X
            y: Coordenada Y
        """
        self.click(x, y, button="right")
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
             duration: float = 0.5, button: str = "left"):
        """
        Arrasta o rato de uma posição para outra.
        
        Args:
            start_x, start_y: Posição inicial
            end_x, end_y: Posição final
            duration: Duração do arrasto
            button: Botão a usar
        """
        if not self.available:
            return
        
        try:
            self.move_to(start_x, start_y, duration=0.2)
            pyautogui.drag(end_x - start_x, end_y - start_y, 
                          duration=duration, button=button)
            logger.debug(f"Arrastado de ({start_x}, {start_y}) para ({end_x}, {end_y})")
        except Exception as e:
            logger.error(f"Erro ao arrastar: {e}")
    
    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None):
        """
        Faz scroll com a roda do rato.
        
        Args:
            clicks: Número de 'cliques' (positivo = cima, negativo = baixo)
            x, y: Posição onde fazer scroll
        """
        if not self.available:
            return
        
        try:
            if x and y:
                pyautogui.scroll(clicks, x=x, y=y)
            else:
                pyautogui.scroll(clicks)
            direction = "cima" if clicks > 0 else "baixo"
            logger.debug(f"Scroll {direction} ({abs(clicks)} clicks)")
        except Exception as e:
            logger.error(f"Erro ao fazer scroll: {e}")
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Obtém o tamanho do ecrã.
        
        Returns:
            Tupla (largura, altura)
        """
        if not self.available:
            return (1920, 1080)  # Valor padrão
        
        return pyautogui.size()


class KeyboardController:
    """
    Controlador de teclado.
    Permite escrever texto e pressionar teclas.
    """
    
    def __init__(self):
        """Inicializa o controlador de teclado."""
        self.available = PYAUTOGUI_AVAILABLE
    
    def write(self, text: str, interval: float = 0.05):
        """
        Escreve texto (simula digitação).
        
        Args:
            text: Texto a escrever
            interval: Intervalo entre teclas
        """
        if not self.available:
            logger.error("PyAutoGUI não disponível")
            return
        
        try:
            # pyautogui.write não suporta caracteres especiais portugueses
            # Usar pyperclip para colar texto com caracteres especiais
            pyautogui.write(text, interval=interval)
            logger.debug(f"Texto escrito: {text[:30]}...")
        except Exception as e:
            logger.error(f"Erro ao escrever: {e}")
    
    def type_text(self, text: str):
        """
        Escreve texto usando clipboard (suporta caracteres especiais).
        
        Args:
            text: Texto a escrever
        """
        if not self.available:
            return
        
        try:
            import pyperclip
            pyperclip.copy(text)
            self.paste()
            logger.debug(f"Texto colado: {text[:30]}...")
        except ImportError:
            # Fallback para write normal
            self.write(text)
        except Exception as e:
            logger.error(f"Erro ao escrever: {e}")
    
    def press(self, key: str):
        """
        Pressiona uma tecla.
        
        Args:
            key: Nome da tecla ('enter', 'tab', 'escape', etc.)
        """
        if not self.available:
            return
        
        try:
            pyautogui.press(key)
            logger.debug(f"Tecla pressionada: {key}")
        except Exception as e:
            logger.error(f"Erro ao pressionar tecla: {e}")
    
    def hotkey(self, *keys: str):
        """
        Pressiona combinação de teclas.
        
        Args:
            *keys: Teclas da combinação (ex: 'ctrl', 'c')
        """
        if not self.available:
            return
        
        try:
            pyautogui.hotkey(*keys)
            combo = "+".join(keys)
            logger.debug(f"Atalho pressionado: {combo}")
        except Exception as e:
            logger.error(f"Erro no atalho: {e}")
    
    def copy(self):
        """Executa Ctrl+C (copiar)."""
        self.hotkey('ctrl', 'c')
    
    def paste(self):
        """Executa Ctrl+V (colar)."""
        self.hotkey('ctrl', 'v')
    
    def cut(self):
        """Executa Ctrl+X (cortar)."""
        self.hotkey('ctrl', 'x')
    
    def select_all(self):
        """Executa Ctrl+A (selecionar tudo)."""
        self.hotkey('ctrl', 'a')
    
    def undo(self):
        """Executa Ctrl+Z (desfazer)."""
        self.hotkey('ctrl', 'z')
    
    def redo(self):
        """Executa Ctrl+Y (refazer)."""
        self.hotkey('ctrl', 'y')
    
    def save(self):
        """Executa Ctrl+S (guardar)."""
        self.hotkey('ctrl', 's')
    
    def new_tab(self):
        """Executa Ctrl+T (novo separador)."""
        self.hotkey('ctrl', 't')
    
    def close_tab(self):
        """Executa Ctrl+W (fechar separador)."""
        self.hotkey('ctrl', 'w')
    
    def alt_tab(self):
        """Executa Alt+Tab (alternar janelas)."""
        self.hotkey('alt', 'tab')
    
    def hold_key(self, key: str, duration: float = 1.0):
        """
        Mantém uma tecla pressionada.
        
        Args:
            key: Tecla a manter
            duration: Duração em segundos
        """
        if not self.available:
            return
        
        try:
            pyautogui.keyDown(key)
            time.sleep(duration)
            pyautogui.keyUp(key)
            logger.debug(f"Tecla {key} mantida por {duration}s")
        except Exception as e:
            logger.error(f"Erro ao manter tecla: {e}")


# Instâncias globais
mouse_controller = MouseController()
keyboard_controller = KeyboardController()


if __name__ == "__main__":
    # Teste dos controladores
    print("=" * 50)
    print("🖱️ Teste de Controladores de Rato e Teclado")
    print("=" * 50)
    
    if not PYAUTOGUI_AVAILABLE:
        print("❌ PyAutoGUI não disponível")
        print("   Instale: pip install PyAutoGUI")
        sys.exit(1)
    
    # Testar rato
    print("\n🖱️ Posição actual do rato:", mouse_controller.get_position())
    print("🖥️ Tamanho do ecrã:", mouse_controller.get_screen_size())
    
    # Demonstração (comentada para segurança)
    print("\n📝 Demonstração de escrita (em 3 segundos)...")
    print("   Coloca o cursor num campo de texto!")
    time.sleep(3)
    
    keyboard_controller.write("Ola SharkCoders!", interval=0.1)
    keyboard_controller.press('enter')
    
    print("\n✅ Teste concluído!")
