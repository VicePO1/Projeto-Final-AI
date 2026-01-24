#!/usr/bin/env python3
"""
SharkCoders Assistant - Estilos da GUI
Definição de cores, fontes e estilos para a interface.
"""

import sys
sys.path.insert(0, str(__file__).rsplit('\\', 2)[0])

try:
    from config import COLORS as CONFIG_COLORS, FONTS as CONFIG_FONTS
except ImportError:
    CONFIG_COLORS = {}
    CONFIG_FONTS = {}

# =============================================================================
# CORES DO TEMA
# =============================================================================
COLORS = {
    # Cores principais
    "PRIMARY": CONFIG_COLORS.get("PRIMARY", "#FF6B35"),      # Laranja SharkCoders
    "SECONDARY": CONFIG_COLORS.get("SECONDARY", "#1A1A2E"),  # Azul escuro
    
    # Fundos
    "BACKGROUND": CONFIG_COLORS.get("BACKGROUND", "#0F0F1A"),     # Fundo muito escuro
    "SURFACE": CONFIG_COLORS.get("SURFACE", "#16213E"),           # Superfície
    "SURFACE_LIGHT": CONFIG_COLORS.get("SURFACE_LIGHT", "#1F3460"), # Superfície clara
    "SURFACE_DARK": "#0A0A12",   # Superfície muito escura
    
    # Texto
    "TEXT": CONFIG_COLORS.get("TEXT", "#FFFFFF"),                 # Texto branco
    "TEXT_SECONDARY": CONFIG_COLORS.get("TEXT_SECONDARY", "#B0B0B0"), # Texto secundário
    "TEXT_MUTED": "#707070",     # Texto esmaecido
    
    # Estados
    "SUCCESS": CONFIG_COLORS.get("SUCCESS", "#4CAF50"),   # Verde sucesso
    "ERROR": CONFIG_COLORS.get("ERROR", "#F44336"),       # Vermelho erro
    "WARNING": CONFIG_COLORS.get("WARNING", "#FFC107"),   # Amarelo aviso
    "INFO": CONFIG_COLORS.get("INFO", "#2196F3"),         # Azul informação
    
    # Destaques
    "ACCENT": CONFIG_COLORS.get("ACCENT", "#00D9FF"),     # Ciano destaque
    "HIGHLIGHT": "#FF9500",      # Laranja destaque
    
    # Botões
    "BUTTON_BG": "#FF6B35",
    "BUTTON_HOVER": "#FF8C5A",
    "BUTTON_ACTIVE": "#E55A25",
    "BUTTON_DISABLED": "#555555",
    
    # Bordas
    "BORDER": "#2A2A4A",
    "BORDER_LIGHT": "#3A3A5A",
    "BORDER_FOCUS": "#FF6B35",
}

# =============================================================================
# FONTES
# =============================================================================
FONTS = {
    # Família de fontes
    "FAMILY": CONFIG_FONTS.get("FAMILY", "Segoe UI"),
    "FAMILY_MONO": CONFIG_FONTS.get("FAMILY_MONO", "Consolas"),
    
    # Tamanhos
    "SIZE_TINY": 8,
    "SIZE_SMALL": CONFIG_FONTS.get("SIZE_SMALL", 10),
    "SIZE_NORMAL": CONFIG_FONTS.get("SIZE_NORMAL", 12),
    "SIZE_LARGE": CONFIG_FONTS.get("SIZE_LARGE", 14),
    "SIZE_TITLE": CONFIG_FONTS.get("SIZE_TITLE", 18),
    "SIZE_HEADER": CONFIG_FONTS.get("SIZE_HEADER", 24),
    "SIZE_HUGE": 32,
}

# Fontes pré-definidas (tuplas para tkinter)
FONT_NORMAL = (FONTS["FAMILY"], FONTS["SIZE_NORMAL"])
FONT_SMALL = (FONTS["FAMILY"], FONTS["SIZE_SMALL"])
FONT_LARGE = (FONTS["FAMILY"], FONTS["SIZE_LARGE"])
FONT_TITLE = (FONTS["FAMILY"], FONTS["SIZE_TITLE"], "bold")
FONT_HEADER = (FONTS["FAMILY"], FONTS["SIZE_HEADER"], "bold")
FONT_MONO = (FONTS["FAMILY_MONO"], FONTS["SIZE_NORMAL"])
FONT_MONO_SMALL = (FONTS["FAMILY_MONO"], FONTS["SIZE_SMALL"])

# =============================================================================
# ESTILOS DE WIDGETS
# =============================================================================
STYLES = {
    # Estilo de botão padrão
    "button": {
        "bg": COLORS["BUTTON_BG"],
        "fg": COLORS["TEXT"],
        "activebackground": COLORS["BUTTON_HOVER"],
        "activeforeground": COLORS["TEXT"],
        "font": FONT_NORMAL,
        "relief": "flat",
        "cursor": "hand2",
        "padx": 15,
        "pady": 8,
        "bd": 0,
    },
    
    # Estilo de botão secundário
    "button_secondary": {
        "bg": COLORS["SURFACE_LIGHT"],
        "fg": COLORS["TEXT"],
        "activebackground": COLORS["SURFACE"],
        "activeforeground": COLORS["TEXT"],
        "font": FONT_NORMAL,
        "relief": "flat",
        "cursor": "hand2",
        "padx": 15,
        "pady": 8,
        "bd": 0,
    },
    
    # Estilo de botão de ícone
    "icon_button": {
        "bg": COLORS["SURFACE"],
        "fg": COLORS["TEXT"],
        "activebackground": COLORS["PRIMARY"],
        "activeforeground": COLORS["TEXT"],
        "font": (FONTS["FAMILY"], 16),
        "relief": "flat",
        "cursor": "hand2",
        "width": 3,
        "height": 1,
        "bd": 0,
    },
    
    # Estilo de frame
    "frame": {
        "bg": COLORS["BACKGROUND"],
        "highlightthickness": 0,
    },
    
    # Estilo de frame com borda
    "frame_bordered": {
        "bg": COLORS["SURFACE"],
        "highlightbackground": COLORS["BORDER"],
        "highlightthickness": 1,
    },
    
    # Estilo de label
    "label": {
        "bg": COLORS["BACKGROUND"],
        "fg": COLORS["TEXT"],
        "font": FONT_NORMAL,
    },
    
    # Estilo de label título
    "label_title": {
        "bg": COLORS["BACKGROUND"],
        "fg": COLORS["PRIMARY"],
        "font": FONT_TITLE,
    },
    
    # Estilo de label secundário
    "label_secondary": {
        "bg": COLORS["BACKGROUND"],
        "fg": COLORS["TEXT_SECONDARY"],
        "font": FONT_SMALL,
    },
    
    # Estilo de entry
    "entry": {
        "bg": COLORS["SURFACE"],
        "fg": COLORS["TEXT"],
        "insertbackground": COLORS["TEXT"],
        "font": FONT_NORMAL,
        "relief": "flat",
        "highlightbackground": COLORS["BORDER"],
        "highlightcolor": COLORS["PRIMARY"],
        "highlightthickness": 1,
    },
    
    # Estilo de text area
    "text": {
        "bg": COLORS["SURFACE_DARK"],
        "fg": COLORS["TEXT"],
        "insertbackground": COLORS["TEXT"],
        "font": FONT_MONO,
        "relief": "flat",
        "highlightbackground": COLORS["BORDER"],
        "highlightcolor": COLORS["PRIMARY"],
        "highlightthickness": 1,
        "padx": 10,
        "pady": 10,
    },
    
    # Estilo de scrollbar
    "scrollbar": {
        "bg": COLORS["SURFACE"],
        "troughcolor": COLORS["BACKGROUND"],
        "activebackground": COLORS["PRIMARY"],
        "highlightthickness": 0,
        "bd": 0,
    },
    
    # Estilo de labelframe
    "labelframe": {
        "bg": COLORS["SURFACE"],
        "fg": COLORS["PRIMARY"],
        "font": FONT_LARGE,
    },
}

# =============================================================================
# ESTILOS DE STATUS
# =============================================================================
STATUS_COLORS = {
    "success": COLORS["SUCCESS"],
    "error": COLORS["ERROR"],
    "warning": COLORS["WARNING"],
    "info": COLORS["INFO"],
    "normal": COLORS["TEXT"],
    "ready": COLORS["SUCCESS"],
    "busy": COLORS["WARNING"],
    "offline": COLORS["ERROR"],
}

# =============================================================================
# DIMENSÕES PADRÃO
# =============================================================================
DIMENSIONS = {
    "button_width": 15,
    "button_height": 2,
    "entry_width": 30,
    "text_width": 60,
    "text_height": 10,
    "padding_small": 5,
    "padding_normal": 10,
    "padding_large": 20,
    "border_radius": 5,
}


def get_button_style(style_name: str = "button") -> dict:
    """
    Retorna estilo de botão.
    
    Args:
        style_name: Nome do estilo ('button', 'button_secondary', 'icon_button')
    
    Returns:
        Dicionário com configurações do estilo
    """
    return STYLES.get(style_name, STYLES["button"]).copy()


def get_frame_style(bordered: bool = False) -> dict:
    """
    Retorna estilo de frame.
    
    Args:
        bordered: Se deve ter borda
    
    Returns:
        Dicionário com configurações do estilo
    """
    style_name = "frame_bordered" if bordered else "frame"
    return STYLES[style_name].copy()


def get_label_style(style_type: str = "normal") -> dict:
    """
    Retorna estilo de label.
    
    Args:
        style_type: Tipo ('normal', 'title', 'secondary')
    
    Returns:
        Dicionário com configurações do estilo
    """
    style_map = {
        "normal": "label",
        "title": "label_title",
        "secondary": "label_secondary",
    }
    style_name = style_map.get(style_type, "label")
    return STYLES[style_name].copy()


def get_status_color(status: str) -> str:
    """
    Retorna cor para um estado.
    
    Args:
        status: Nome do estado
    
    Returns:
        Código de cor hexadecimal
    """
    return STATUS_COLORS.get(status.lower(), COLORS["TEXT"])


if __name__ == "__main__":
    # Mostrar cores disponíveis
    print("=" * 50)
    print("Cores do Tema SharkCoders")
    print("=" * 50)
    for name, color in COLORS.items():
        print(f"  {name}: {color}")
    
    print("\n" + "=" * 50)
    print("Fontes")
    print("=" * 50)
    for name, value in FONTS.items():
        print(f"  {name}: {value}")
