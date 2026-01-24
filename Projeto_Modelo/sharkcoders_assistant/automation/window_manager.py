#!/usr/bin/env python3
"""
SharkCoders Assistant - Gestor de Janelas
Módulo para gestão de janelas do sistema operativo.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Optional, Dict
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import logger, get_platform

# Detectar plataforma e importar módulos específicos
PLATFORM = get_platform()

if PLATFORM == 'windows':
    try:
        import ctypes
        from ctypes import wintypes
        WINDOWS_AVAILABLE = True
    except ImportError:
        WINDOWS_AVAILABLE = False
else:
    WINDOWS_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


class WindowManager:
    """
    Gestor de janelas do sistema operativo.
    Suporta Windows, Linux e macOS.
    """
    
    def __init__(self):
        """Inicializa o gestor de janelas."""
        self.platform = PLATFORM
        logger.debug(f"WindowManager inicializado para: {self.platform}")
    
    def get_active_window_title(self) -> Optional[str]:
        """
        Obtém o título da janela activa.
        
        Returns:
            Título da janela ou None se falhar
        """
        try:
            if self.platform == 'windows':
                return self._get_active_window_windows()
            elif self.platform == 'linux':
                return self._get_active_window_linux()
            elif self.platform == 'darwin':
                return self._get_active_window_macos()
            else:
                return None
        except Exception as e:
            logger.error(f"Erro ao obter janela activa: {e}")
            return None
    
    def _get_active_window_windows(self) -> Optional[str]:
        """Obtém janela activa no Windows."""
        if not WINDOWS_AVAILABLE:
            return None
        
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            
            length = user32.GetWindowTextLengthW(hwnd)
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)
            
            return buffer.value if buffer.value else None
        except Exception as e:
            logger.error(f"Erro Windows: {e}")
            return None
    
    def _get_active_window_linux(self) -> Optional[str]:
        """Obtém janela activa no Linux."""
        try:
            # Usar xdotool se disponível
            result = subprocess.run(
                ['xdotool', 'getactivewindow', 'getwindowname'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except FileNotFoundError:
            logger.warning("xdotool não instalado. Instale: sudo apt install xdotool")
            return None
        except Exception as e:
            logger.error(f"Erro Linux: {e}")
            return None
    
    def _get_active_window_macos(self) -> Optional[str]:
        """Obtém janela activa no macOS."""
        try:
            script = '''
                tell application "System Events"
                    set frontApp to name of first application process whose frontmost is true
                end tell
                return frontApp
            '''
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception as e:
            logger.error(f"Erro macOS: {e}")
            return None
    
    def get_all_windows(self) -> List[str]:
        """
        Lista todas as janelas abertas.
        
        Returns:
            Lista de títulos de janelas
        """
        try:
            if self.platform == 'windows':
                return self._get_all_windows_windows()
            elif self.platform == 'linux':
                return self._get_all_windows_linux()
            elif self.platform == 'darwin':
                return self._get_all_windows_macos()
            else:
                return []
        except Exception as e:
            logger.error(f"Erro ao listar janelas: {e}")
            return []
    
    def _get_all_windows_windows(self) -> List[str]:
        """Lista janelas no Windows."""
        if not WINDOWS_AVAILABLE:
            return []
        
        windows = []
        
        try:
            user32 = ctypes.windll.user32
            
            def enum_callback(hwnd, _):
                if user32.IsWindowVisible(hwnd):
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buffer = ctypes.create_unicode_buffer(length + 1)
                        user32.GetWindowTextW(hwnd, buffer, length + 1)
                        if buffer.value:
                            windows.append(buffer.value)
                return True
            
            WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
            user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
            
        except Exception as e:
            logger.error(f"Erro ao enumerar janelas: {e}")
        
        return windows
    
    def _get_all_windows_linux(self) -> List[str]:
        """Lista janelas no Linux."""
        try:
            result = subprocess.run(
                ['wmctrl', '-l'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                windows = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        # Formato: <id> <desktop> <hostname> <title>
                        parts = line.split(None, 3)
                        if len(parts) >= 4:
                            windows.append(parts[3])
                return windows
            return []
        except FileNotFoundError:
            logger.warning("wmctrl não instalado. Instale: sudo apt install wmctrl")
            return []
        except Exception as e:
            logger.error(f"Erro Linux: {e}")
            return []
    
    def _get_all_windows_macos(self) -> List[str]:
        """Lista janelas no macOS."""
        try:
            script = '''
                tell application "System Events"
                    set windowList to {}
                    repeat with proc in (every process whose background only is false)
                        set end of windowList to name of proc
                    end repeat
                end tell
                return windowList
            '''
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # Parse da lista AppleScript
                output = result.stdout.strip()
                if output:
                    return [w.strip() for w in output.split(',')]
            return []
        except Exception as e:
            logger.error(f"Erro macOS: {e}")
            return []
    
    def minimize_window(self, title: str = None) -> bool:
        """
        Minimiza uma janela.
        
        Args:
            title: Título da janela (None para janela activa)
        
        Returns:
            True se bem sucedido
        """
        if PYAUTOGUI_AVAILABLE:
            try:
                if title:
                    windows = pyautogui.getWindowsWithTitle(title)
                    if windows:
                        windows[0].minimize()
                        return True
                else:
                    # Minimizar janela activa
                    active = pyautogui.getActiveWindow()
                    if active:
                        active.minimize()
                        return True
            except Exception as e:
                logger.error(f"Erro ao minimizar: {e}")
        
        return False
    
    def maximize_window(self, title: str = None) -> bool:
        """
        Maximiza uma janela.
        
        Args:
            title: Título da janela (None para janela activa)
        
        Returns:
            True se bem sucedido
        """
        if PYAUTOGUI_AVAILABLE:
            try:
                if title:
                    windows = pyautogui.getWindowsWithTitle(title)
                    if windows:
                        windows[0].maximize()
                        return True
                else:
                    active = pyautogui.getActiveWindow()
                    if active:
                        active.maximize()
                        return True
            except Exception as e:
                logger.error(f"Erro ao maximizar: {e}")
        
        return False
    
    def restore_window(self, title: str = None) -> bool:
        """
        Restaura uma janela minimizada.
        
        Args:
            title: Título da janela
        
        Returns:
            True se bem sucedido
        """
        if PYAUTOGUI_AVAILABLE:
            try:
                if title:
                    windows = pyautogui.getWindowsWithTitle(title)
                    if windows:
                        windows[0].restore()
                        return True
            except Exception as e:
                logger.error(f"Erro ao restaurar: {e}")
        
        return False
    
    def focus_window(self, title: str) -> bool:
        """
        Coloca uma janela em foco.
        
        Args:
            title: Título (parcial) da janela
        
        Returns:
            True se bem sucedido
        """
        if PYAUTOGUI_AVAILABLE:
            try:
                windows = pyautogui.getWindowsWithTitle(title)
                if windows:
                    windows[0].activate()
                    logger.info(f"Janela activada: {title}")
                    return True
            except Exception as e:
                logger.error(f"Erro ao focar janela: {e}")
        
        return False
    
    def close_window(self, title: str) -> bool:
        """
        Fecha uma janela.
        
        Args:
            title: Título da janela
        
        Returns:
            True se bem sucedido
        """
        if PYAUTOGUI_AVAILABLE:
            try:
                windows = pyautogui.getWindowsWithTitle(title)
                if windows:
                    windows[0].close()
                    logger.info(f"Janela fechada: {title}")
                    return True
            except Exception as e:
                logger.error(f"Erro ao fechar janela: {e}")
        
        return False
    
    def get_window_info(self, title: str = None) -> Optional[Dict]:
        """
        Obtém informação detalhada sobre uma janela.
        
        Args:
            title: Título da janela (None para janela activa)
        
        Returns:
            Dicionário com informação ou None
        """
        if PYAUTOGUI_AVAILABLE:
            try:
                if title:
                    windows = pyautogui.getWindowsWithTitle(title)
                    window = windows[0] if windows else None
                else:
                    window = pyautogui.getActiveWindow()
                
                if window:
                    return {
                        "title": window.title,
                        "left": window.left,
                        "top": window.top,
                        "width": window.width,
                        "height": window.height,
                        "visible": window.isActive,
                    }
            except Exception as e:
                logger.error(f"Erro ao obter info: {e}")
        
        return None


# Instância global
window_manager = WindowManager()


if __name__ == "__main__":
    # Teste do gestor de janelas
    print("=" * 50)
    print("🪟 Teste do Gestor de Janelas")
    print("=" * 50)
    
    print(f"\n💻 Plataforma: {window_manager.platform}")
    
    # Janela activa
    active = window_manager.get_active_window_title()
    print(f"\n🪟 Janela activa: {active}")
    
    # Listar janelas
    print("\n📋 Janelas abertas:")
    windows = window_manager.get_all_windows()
    for i, w in enumerate(windows[:10], 1):
        print(f"   {i}. {w}")
    
    if len(windows) > 10:
        print(f"   ... e mais {len(windows) - 10} janelas")
    
    print("\n✅ Teste concluído!")
