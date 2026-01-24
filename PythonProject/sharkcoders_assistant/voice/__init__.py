#!/usr/bin/env python3
"""
SharkCoders Assistant - Módulo Voice
Reconhecimento e síntese de voz.
"""

from .speech_recognition import SpeechRecognizer, speech_recognizer
from .text_to_speech import TextToSpeech, text_to_speech
from .voice_commands import VoiceCommandProcessor, voice_processor

__all__ = [
    "SpeechRecognizer",
    "speech_recognizer",
    "TextToSpeech",
    "text_to_speech",
    "VoiceCommandProcessor",
    "voice_processor",
]
