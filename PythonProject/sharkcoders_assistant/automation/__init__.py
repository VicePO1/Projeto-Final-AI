#!/usr/bin/env python3
"""
SharkCoders Assistant - Módulo Automation
Automação de rato, teclado e captura de ecrã.
"""

from .mouse_keyboard import MouseController, KeyboardController, mouse_controller, keyboard_controller
from .screen_capture import ScreenCapture, screen_capture
from .window_manager import WindowManager, window_manager

__all__ = [
    "MouseController",
    "KeyboardController",
    "mouse_controller",
    "keyboard_controller",
    "ScreenCapture",
    "screen_capture",
    "WindowManager",
    "window_manager",
]
