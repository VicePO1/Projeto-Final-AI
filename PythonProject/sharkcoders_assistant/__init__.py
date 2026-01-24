# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════╗
║           🦈 SHARKCODERS ASSISTANT 🦈                         ║
║         Assistente Multimodal Inteligente                     ║
╚═══════════════════════════════════════════════════════════════╝

Pacote principal do SharkCoders Assistant.

Módulos disponíveis:
    - config: Configurações globais
    - utils: Utilitários e helpers
    - assets: Arte ASCII e recursos visuais
    - gui: Interface gráfica (tkinter)
    - voice: Reconhecimento e síntese de voz
    - automation: Automação de rato, teclado e captura de ecrã
    - vision: Processamento de imagem e OCR
    - communication: Envio de mensagens e APIs externas
    - api: Servidor REST API
    - system: Interação com o sistema operativo

Uso:
    python main.py          # Modo GUI (padrão)
    python main.py --cli    # Modo linha de comandos
    python main.py --api-only  # Apenas servidor API
    python main.py --check  # Verificar dependências
"""

__version__ = '1.0.0'
__author__ = 'SharkCoders Team'
__app_name__ = 'SharkCoders Assistant'

# Importações principais para facilitar o uso
try:
    from .config import APP_NAME, VERSION, DEBUG
except ImportError:
    pass

__all__ = [
    '__version__',
    '__author__',
    '__app_name__',
]
