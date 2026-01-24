#!/usr/bin/env python3
"""
SharkCoders Assistant - ASCII Art
Arte ASCII original do SharkCoders.
"""

# =============================================================================
# LOGO SHARKCODERS EM ASCII ART
# =============================================================================
SHARK_LOGO = r"""
   _____ _                _     _____          _               
  / ____| |              | |   / ____|        | |              
 | (___ | |__   __ _ _ __| | _| |     ___   __| | ___ _ __ ___ 
  \___ \| '_ \ / _` | '__| |/ / |    / _ \ / _` |/ _ \ '__/ __|
  ____) | | | | (_| | |  |   <| |___| (_) | (_| |  __/ |  \__ \
 |_____/|_| |_|\__,_|_|  |_|\_\\_____\___/ \__,_|\___|_|  |___/
                                                                
"""

# =============================================================================
# MASCOTE TUBARÃO EM ASCII
# =============================================================================
SHARK_MASCOT = r"""
                          ,-
                         ,'::|
                        /::::|
                      ,'::::o\                                      _..
                   __.:-:::::;'\                                  ,:' /
                .-':::::::::'\ `.                               ,' ,'
              .':::::::::::::::\ `-._                         ,'  /
             /:::::::::::::::::::::`-.`-._          ___..--'--,'_.'
            /-;::::::::::::::::::::::::::: `.   _.-':::::::::'.-'
           /   `;::::::::::::::::::::::::::.:| ,':::::::::::-'
          /      `,-. :::::::::::::::::::,.::' ::::::::'
         |         \ `:;_:::::::_,.-'  ,' _',-'::::::,'
          \          `--`-`   '   _,' '.:::::::::,'
           |                      / _.:'::::::_,'
           \                 _.-.-'  `::::::,'
            `._     __..--'   _...::::::::,'
               `---'   __..--':::::::::_,'
                  _.--'  :::::::::::_,'
               ,-'   _::::::::::_,-'
              / _,.-' ::::::_,-'
             /,'      ::::,'
            |'       _.::'
            `.__..--'
"""

# =============================================================================
# TUBARÃO PEQUENO PARA LOGO
# =============================================================================
SHARK_SMALL = r"""
        /\
       /  \  🦈
      / /\ \
     / /  \ \____
    / /    \___  \
    \/ SharkCoders\
"""

# =============================================================================
# BANNER DE BOAS-VINDAS
# =============================================================================
WELCOME_BANNER = r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗ ██████╗ ██████╗ ██████╗ ███████╗ ║
║   ██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██╔═══██╗██╔══██╗██╔════╝ ║
║   ███████╗███████║███████║██████╔╝█████╔╝ ██║     ██║   ██║██║  ██║█████╗   ║
║   ╚════██║██╔══██║██╔══██║██╔══██╗██╔═██╗ ██║     ██║   ██║██║  ██║██╔══╝   ║
║   ███████║██║  ██║██║  ██║██║  ██║██║  ██╗╚██████╗╚██████╔╝██████╔╝███████╗ ║
║   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝ ║
║                                                                              ║
║                    🦈 ASSISTANT - Python for AI 🦈                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# =============================================================================
# SEPARADORES
# =============================================================================
SEPARATOR = "─" * 78
SEPARATOR_THICK = "═" * 78
SEPARATOR_WAVE = "〰" * 39
SEPARATOR_SHARK = "🦈" + "─" * 36 + "🦈" + "─" * 36 + "🦈"

# =============================================================================
# MENSAGENS COM EMOJIS
# =============================================================================
MESSAGES = {
    # Estados
    "welcome": "🦈 Bem-vindo ao SharkCoders Assistant!",
    "goodbye": "👋 Até à próxima! Bom trabalho!",
    "ready": "✨ Pronto para ajudar!",
    "listening": "🎤 Estou a ouvir...",
    "processing": "⏳ A processar...",
    "thinking": "🤔 A pensar...",
    
    # Sucesso
    "success": "✅ Operação concluída com sucesso!",
    "captured": "📸 Captura de ecrã guardada!",
    "sent": "📤 Mensagem enviada!",
    "extracted": "📝 Texto extraído!",
    
    # Erros
    "error": "❌ Ocorreu um erro.",
    "not_found": "🔍 Não encontrado.",
    "not_understood": "🤷 Desculpa, não entendi.",
    "timeout": "⏰ Tempo esgotado.",
    "cancelled": "🚫 Operação cancelada.",
    
    # Ações
    "screenshot": "📷 A capturar ecrã...",
    "ocr": "🔤 A extrair texto...",
    "voice": "🗣️ A falar...",
    "api": "🌐 A consultar API...",
    "telegram": "📱 A enviar para Telegram...",
    
    # Sistema
    "system_info": "💻 Informação do Sistema",
    "time": "🕐 Hora actual",
    "date": "📅 Data actual",
    "window": "🪟 Janela activa",
    
    # Ajuda
    "help": "❓ Ajuda",
    "commands": "📋 Comandos disponíveis",
    "tip": "💡 Dica",
}

# =============================================================================
# EMOJIS POR ESTADO
# =============================================================================
STATUS_EMOJIS = {
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "loading": "⏳",
    "ready": "🟢",
    "busy": "🟡",
    "offline": "🔴",
    "listening": "🎤",
    "speaking": "🔊",
    "camera": "📷",
    "text": "📝",
    "send": "📤",
    "receive": "📥",
}


def get_status_emoji(status: str) -> str:
    """
    Retorna o emoji correspondente a um estado.
    
    Args:
        status: Nome do estado
    
    Returns:
        Emoji correspondente ou emoji genérico
    """
    return STATUS_EMOJIS.get(status.lower(), "🔵")


def print_welcome():
    """Imprime o banner de boas-vindas completo."""
    print("\n" + WELCOME_BANNER)
    print(f"\n{SEPARATOR_SHARK}\n")
    print(MESSAGES["welcome"])
    print(MESSAGES["ready"])
    print(f"\n{SEPARATOR}\n")


def print_shark():
    """Imprime o mascote tubarão."""
    print(SHARK_MASCOT)


def print_separator(style: str = "normal"):
    """
    Imprime um separador.
    
    Args:
        style: 'normal', 'thick', 'wave' ou 'shark'
    """
    separators = {
        "normal": SEPARATOR,
        "thick": SEPARATOR_THICK,
        "wave": SEPARATOR_WAVE,
        "shark": SEPARATOR_SHARK,
    }
    print(separators.get(style, SEPARATOR))


def print_goodbye():
    """Imprime mensagem de despedida."""
    print(f"\n{SEPARATOR_SHARK}\n")
    print(MESSAGES["goodbye"])
    print("""
    🦈 Obrigado por usar o SharkCoders Assistant! 🦈
    
        Aprende a programar como um tubarão! 🌊
    """)
    print(f"\n{SEPARATOR}\n")


def print_logo():
    """Imprime o logo SharkCoders."""
    print(SHARK_LOGO)


def print_help():
    """Imprime ajuda com comandos disponíveis."""
    help_text = f"""
{SEPARATOR}
{MESSAGES["help"]} - {MESSAGES["commands"]}
{SEPARATOR}

🎤 COMANDOS DE VOZ:
    • "capturar ecrã"    → Tira screenshot
    • "ler imagem"       → Extrai texto (OCR)
    • "enviar imagem"    → Envia via Telegram
    • "que horas são"    → Diz as horas
    • "que dia é hoje"   → Diz a data
    • "diz uma piada"    → Conta uma piada
    • "uma citação"      → Diz uma citação
    • "janela ativa"     → Mostra janela actual
    • "listar janelas"   → Lista todas as janelas
    • "ajuda"            → Mostra esta ajuda
    • "sair"             → Fecha a aplicação

{SEPARATOR}
"""
    print(help_text)


if __name__ == "__main__":
    # Demonstração da arte ASCII
    print_welcome()
    print_shark()
    print_separator("shark")
    print_logo()
    print_help()
    print_goodbye()
