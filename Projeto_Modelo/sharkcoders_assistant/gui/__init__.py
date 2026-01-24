#!/usr/bin/env python3
"""
SharkCoders Assistant - Módulo GUI
Interface gráfica com tkinter.
"""

from .styles import COLORS, FONTS, STYLES
from .widgets import (
    ModernButton,
    IconButton,
    StatusLabel,
    ScrolledText,
    LabeledFrame,
    ModernEntry,
)
from .main_window import MainWindow, create_main_window

__all__ = [
    "COLORS",
    "FONTS",
    "STYLES",
    "ModernButton",
    "IconButton",
    "StatusLabel",
    "ScrolledText",
    "LabeledFrame",
    "ModernEntry",
    "MainWindow",
    "create_main_window",
]
