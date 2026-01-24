#!/usr/bin/env python3
"""
SharkCoders Assistant - Módulo API
API REST com Flask.
"""

from .server import AssistantAPI, assistant_api
from .routes import register_routes

__all__ = [
    "AssistantAPI",
    "assistant_api",
    "register_routes",
]
