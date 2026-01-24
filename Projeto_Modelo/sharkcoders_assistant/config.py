#!/usr/bin/env python3
"""
SharkCoders Assistant - Configurações Globais
Ficheiro de configuração central do projeto.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente do ficheiro .env (se existir)
load_dotenv()

# =============================================================================
# CAMINHOS BASE
# =============================================================================
BASE_DIR = Path(__file__).parent.absolute()
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"

# Criar diretórios se não existirem
SCREENSHOTS_DIR.mkdir(exist_ok=True)
ICONS_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# CONFIGURAÇÕES DA APLICAÇÃO
# =============================================================================
APP_NAME = "SharkCoders Assistant"
APP_VERSION = "1.0.0"
APP_AUTHOR = "SharkCoders"

# Dimensões da janela principal
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600

# =============================================================================
# CONFIGURAÇÕES DE VOZ
# =============================================================================
VOICE_CONFIG = {
    "language": "pt-PT",  # Idioma português de Portugal
    "rate": 150,          # Velocidade da fala (palavras por minuto)
    "volume": 1.0,        # Volume (0.0 a 1.0)
    "timeout": 5,         # Timeout para reconhecimento (segundos)
    "phrase_timeout": 3,  # Timeout entre frases (segundos)
    "energy_threshold": 300,  # Limiar de energia para detecção
}

# =============================================================================
# CONFIGURAÇÕES DE OCR
# =============================================================================
OCR_CONFIG = {
    # Caminho do Tesseract (ajustar conforme instalação)
    "tesseract_path": r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    "language": "por",  # Português
    "config": "--oem 3 --psm 6",  # Modo OCR
}

# =============================================================================
# CONFIGURAÇÕES DA API LOCAL
# =============================================================================
API_CONFIG = {
    "host": "127.0.0.1",
    "port": 5000,
    "debug": False,
    "threaded": True,
}

# =============================================================================
# CONFIGURAÇÕES DO TELEGRAM
# =============================================================================
TELEGRAM_CONFIG = {
    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "api_url": "https://api.telegram.org/bot",
}

# =============================================================================
# URLs DE APIs EXTERNAS
# =============================================================================
EXTERNAL_APIS = {
    "quotes": "https://api.quotable.io/random",
    "jokes": "https://v2.jokeapi.dev/joke/Any?lang=pt&type=single",
    "facts": "https://uselessfacts.jsph.pl/random.json?language=en",
    "weather": "https://api.openweathermap.org/data/2.5/weather",
    "weather_api_key": os.getenv("OPENWEATHER_API_KEY", ""),
}

# =============================================================================
# CORES DO TEMA
# =============================================================================
COLORS = {
    "PRIMARY": "#FF6B35",      # Laranja SharkCoders
    "SECONDARY": "#1A1A2E",    # Azul escuro
    "BACKGROUND": "#0F0F1A",   # Fundo muito escuro
    "SURFACE": "#16213E",      # Superfície
    "SURFACE_LIGHT": "#1F3460", # Superfície clara
    "TEXT": "#FFFFFF",         # Texto branco
    "TEXT_SECONDARY": "#B0B0B0", # Texto secundário
    "SUCCESS": "#4CAF50",      # Verde sucesso
    "ERROR": "#F44336",        # Vermelho erro
    "WARNING": "#FFC107",      # Amarelo aviso
    "INFO": "#2196F3",         # Azul informação
    "ACCENT": "#00D9FF",       # Ciano destaque
}

# =============================================================================
# FONTES
# =============================================================================
FONTS = {
    "FAMILY": "Segoe UI",
    "FAMILY_MONO": "Consolas",
    "SIZE_SMALL": 10,
    "SIZE_NORMAL": 12,
    "SIZE_LARGE": 14,
    "SIZE_TITLE": 18,
    "SIZE_HEADER": 24,
}

# =============================================================================
# COMANDOS DE VOZ
# =============================================================================
VOICE_COMMANDS = {
    # Captura de ecrã
    "capturar ecrã": "capture_screen",
    "capturar ecra": "capture_screen",
    "tirar captura": "capture_screen",
    "screenshot": "capture_screen",
    "captura": "capture_screen",
    
    # OCR / Leitura de imagem
    "ler imagem": "read_image",
    "extrair texto": "read_image",
    "ocr": "read_image",
    "reconhecer texto": "read_image",
    
    # Envio de imagem
    "enviar imagem": "send_image",
    "enviar captura": "send_image",
    "mandar imagem": "send_image",
    
    # Tempo/Data
    "que horas são": "tell_time",
    "que horas sao": "tell_time",
    "horas": "tell_time",
    "que dia é hoje": "tell_date",
    "que dia e hoje": "tell_date",
    "data": "tell_date",
    
    # APIs externas
    "diz uma piada": "tell_joke",
    "conta uma piada": "tell_joke",
    "piada": "tell_joke",
    "uma citação": "get_quote",
    "uma citacao": "get_quote",
    "citação": "get_quote",
    "facto interessante": "get_fact",
    "facto": "get_fact",
    
    # Gestão de janelas
    "janela ativa": "active_window",
    "janela actual": "active_window",
    "listar janelas": "list_windows",
    "todas as janelas": "list_windows",
    
    # Sistema
    "informação do sistema": "system_info",
    "informacao do sistema": "system_info",
    "info sistema": "system_info",
    
    # Ajuda e controlo
    "ajuda": "help",
    "comandos": "help",
    "sair": "exit",
    "fechar": "exit",
    "terminar": "exit",
}

# =============================================================================
# MENSAGENS DO SISTEMA
# =============================================================================
MESSAGES = {
    "welcome": "Bem-vindo ao SharkCoders Assistant!",
    "listening": "Estou a ouvir...",
    "not_understood": "Desculpa, não entendi. Podes repetir?",
    "success": "Operação concluída com sucesso!",
    "error": "Ocorreu um erro. Por favor, tenta novamente.",
    "goodbye": "Até à próxima! Bom trabalho!",
    "processing": "A processar...",
    "capturing": "A capturar ecrã...",
    "sending": "A enviar...",
    "extracting": "A extrair texto...",
}

# =============================================================================
# CONFIGURAÇÕES DE AUTOMAÇÃO
# =============================================================================
AUTOMATION_CONFIG = {
    "failsafe": True,      # Mover rato para canto para abortar
    "pause": 0.1,          # Pausa entre ações (segundos)
    "screenshot_delay": 0.5,  # Delay antes de captura
}


if __name__ == "__main__":
    # Teste das configurações
    print(f"📁 Diretório base: {BASE_DIR}")
    print(f"📸 Diretório de capturas: {SCREENSHOTS_DIR}")
    print(f"🎨 Cor primária: {COLORS['PRIMARY']}")
    print(f"🎤 Idioma de voz: {VOICE_CONFIG['language']}")
    print(f"🔤 Idioma OCR: {OCR_CONFIG['language']}")
    print(f"🌐 API local: http://{API_CONFIG['host']}:{API_CONFIG['port']}")
