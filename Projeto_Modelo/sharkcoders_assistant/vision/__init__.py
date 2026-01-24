#!/usr/bin/env python3
"""
SharkCoders Assistant - Módulo Vision
Processamento de imagens e OCR.
"""

from .image_processor import ImageProcessor, image_processor
from .ocr_engine import OCREngine, ocr_engine

__all__ = [
    "ImageProcessor",
    "image_processor",
    "OCREngine",
    "ocr_engine",
]
