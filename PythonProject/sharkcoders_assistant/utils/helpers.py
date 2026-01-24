#!/usr/bin/env python3
"""
SharkCoders Assistant - Funções Auxiliares
Utilitários gerais usados em todo o projeto.
"""

import os
import re
import sys
import time
import threading
from datetime import datetime
from pathlib import Path
from functools import wraps
from typing import Callable, Optional, Any


def get_timestamp() -> str:
    """
    Retorna timestamp actual no formato YYYYMMDD_HHMMSS.
    Útil para nomear ficheiros.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_datetime_string(format_str: str = "%d/%m/%Y %H:%M:%S") -> str:
    """
    Retorna data/hora actual formatada.
    
    Args:
        format_str: Formato da string (padrão: DD/MM/YYYY HH:MM:SS)
    
    Returns:
        String com data/hora formatada
    """
    return datetime.now().strftime(format_str)


def ensure_dir(path: Path | str) -> Path:
    """
    Garante que um diretório existe, criando-o se necessário.
    
    Args:
        path: Caminho do diretório
    
    Returns:
        Path do diretório
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_unique_filename(base_path: Path | str, prefix: str = "file", 
                        extension: str = ".png") -> Path:
    """
    Gera um nome de ficheiro único com timestamp.
    
    Args:
        base_path: Diretório base
        prefix: Prefixo do nome
        extension: Extensão do ficheiro
    
    Returns:
        Path completo do ficheiro único
    """
    base_path = Path(base_path)
    ensure_dir(base_path)
    
    timestamp = get_timestamp()
    filename = f"{prefix}_{timestamp}{extension}"
    
    return base_path / filename


def sanitize_filename(filename: str) -> str:
    """
    Remove caracteres inválidos de um nome de ficheiro.
    
    Args:
        filename: Nome original
    
    Returns:
        Nome sanitizado
    """
    # Caracteres inválidos em Windows
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, "_", filename)
    
    # Remover espaços extras
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    # Limitar tamanho
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    return sanitized


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Trunca texto se exceder o tamanho máximo.
    
    Args:
        text: Texto original
        max_length: Tamanho máximo
        suffix: Sufixo a adicionar se truncado
    
    Returns:
        Texto truncado ou original
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_phone_number(number: str) -> str:
    """
    Formata número de telefone removendo caracteres especiais.
    
    Args:
        number: Número original
    
    Returns:
        Número formatado (apenas dígitos e +)
    """
    # Manter apenas dígitos e +
    formatted = re.sub(r'[^\d+]', '', number)
    
    # Adicionar código de país se não tiver
    if not formatted.startswith('+'):
        if formatted.startswith('351'):
            formatted = '+' + formatted
        else:
            formatted = '+351' + formatted
    
    return formatted


def get_platform() -> str:
    """
    Retorna o sistema operativo actual.
    
    Returns:
        'windows', 'linux', 'darwin' (macOS) ou 'unknown'
    """
    platform = sys.platform.lower()
    
    if platform.startswith('win'):
        return 'windows'
    elif platform.startswith('linux'):
        return 'linux'
    elif platform.startswith('darwin'):
        return 'darwin'
    else:
        return 'unknown'


def run_in_thread(func: Callable) -> Callable:
    """
    Decorador que executa uma função numa thread separada.
    Útil para operações demoradas que não devem bloquear a GUI.
    
    Uso:
        @run_in_thread
        def operacao_demorada():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread
    
    return wrapper


class Timer:
    """
    Context manager para medir tempo de execução.
    
    Uso:
        with Timer("Operação"):
            # código a medir
    """
    
    def __init__(self, name: str = "Operação", logger_func: Optional[Callable] = None):
        """
        Inicializa o Timer.
        
        Args:
            name: Nome da operação (para log)
            logger_func: Função de logging (opcional)
        """
        self.name = name
        self.logger_func = logger_func or print
        self.start_time: float = 0
        self.end_time: float = 0
        self.elapsed: float = 0
    
    def __enter__(self):
        """Inicia a contagem."""
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Termina a contagem e mostra resultado."""
        self.end_time = time.perf_counter()
        self.elapsed = self.end_time - self.start_time
        self.logger_func(f"⏱️ {self.name}: {self.elapsed:.3f}s")
        return False


class Logger:
    """
    Classe de logging simples com cores e emojis.
    """
    
    # Cores ANSI
    COLORS = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }
    
    # Emojis por tipo
    EMOJIS = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "debug": "🔍",
    }
    
    def __init__(self, name: str = "SharkCoders", use_colors: bool = True):
        """
        Inicializa o Logger.
        
        Args:
            name: Nome do logger
            use_colors: Se deve usar cores ANSI
        """
        self.name = name
        self.use_colors = use_colors and self._supports_color()
    
    def _supports_color(self) -> bool:
        """Verifica se o terminal suporta cores."""
        if get_platform() == 'windows':
            # Tentar habilitar cores no Windows
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                return True
            except:
                return False
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    def _colorize(self, text: str, color: str) -> str:
        """Aplica cor ao texto."""
        if self.use_colors and color in self.COLORS:
            return f"{self.COLORS[color]}{text}{self.COLORS['reset']}"
        return text
    
    def _format_message(self, level: str, message: str, color: str) -> str:
        """Formata uma mensagem de log."""
        timestamp = get_datetime_string("%H:%M:%S")
        emoji = self.EMOJIS.get(level, "")
        
        formatted = f"[{timestamp}] {emoji} [{self.name}] {message}"
        return self._colorize(formatted, color)
    
    def info(self, message: str):
        """Log de informação."""
        print(self._format_message("info", message, "blue"))
    
    def success(self, message: str):
        """Log de sucesso."""
        print(self._format_message("success", message, "green"))
    
    def warning(self, message: str):
        """Log de aviso."""
        print(self._format_message("warning", message, "yellow"))
    
    def error(self, message: str):
        """Log de erro."""
        print(self._format_message("error", message, "red"))
    
    def debug(self, message: str):
        """Log de debug."""
        print(self._format_message("debug", message, "magenta"))


# Instância global do logger
logger = Logger("SharkCoders")


if __name__ == "__main__":
    # Testes dos utilitários
    print("=" * 50)
    print("Testes do módulo helpers")
    print("=" * 50)
    
    # Testar timestamp
    print(f"\n📅 Timestamp: {get_timestamp()}")
    print(f"📅 Data/Hora: {get_datetime_string()}")
    
    # Testar plataforma
    print(f"\n💻 Plataforma: {get_platform()}")
    
    # Testar sanitização
    filename = 'Ficheiro <teste>: "exemplo".txt'
    print(f"\n📁 Original: {filename}")
    print(f"📁 Sanitizado: {sanitize_filename(filename)}")
    
    # Testar truncamento
    texto_longo = "Este é um texto muito longo que precisa de ser truncado para caber no ecrã."
    print(f"\n📝 Truncado: {truncate_text(texto_longo, 30)}")
    
    # Testar telefone
    print(f"\n📱 Telefone formatado: {format_phone_number('912 345 678')}")
    
    # Testar logger
    print("\n" + "=" * 50)
    logger.info("Isto é uma mensagem de informação")
    logger.success("Isto é uma mensagem de sucesso")
    logger.warning("Isto é uma mensagem de aviso")
    logger.error("Isto é uma mensagem de erro")
    logger.debug("Isto é uma mensagem de debug")
    
    # Testar Timer
    print("\n" + "=" * 50)
    with Timer("Teste de sleep"):
        time.sleep(0.5)
    
    print("\n✅ Todos os testes concluídos!")
