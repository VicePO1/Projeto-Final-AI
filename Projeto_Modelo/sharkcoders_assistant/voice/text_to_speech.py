#!/usr/bin/env python3
"""
SharkCoders Assistant - Síntese de Voz (TTS)
Módulo para conversão de texto em fala.
"""

import sys
import threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ pyttsx3 não instalado. Instale: pip install pyttsx3")

from config import VOICE_CONFIG, MESSAGES
from utils import logger


class TextToSpeech:
    """
    Classe para síntese de voz (Text-to-Speech).
    Usa a biblioteca pyttsx3 para conversão offline.
    """
    
    def __init__(self):
        """Inicializa o motor de síntese de voz."""
        self.engine = None
        self.rate = VOICE_CONFIG.get("rate", 150)
        self.volume = VOICE_CONFIG.get("volume", 1.0)
        self.language = VOICE_CONFIG.get("language", "pt-PT")
        self._is_speaking = False
        self._lock = threading.Lock()
        
        if TTS_AVAILABLE:
            self._initialize()
    
    def _initialize(self):
        """Inicializa o motor TTS."""
        try:
            self.engine = pyttsx3.init()
            
            # Configurar propriedades
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            
            # Tentar encontrar voz portuguesa
            self._set_portuguese_voice()
            
            logger.success("Motor TTS inicializado")
        except Exception as e:
            logger.error(f"Erro ao inicializar TTS: {e}")
            self.engine = None
    
    def _set_portuguese_voice(self):
        """Tenta definir uma voz em português."""
        if not self.engine:
            return
        
        try:
            voices = self.engine.getProperty('voices')
            
            # Procurar voz portuguesa
            for voice in voices:
                voice_id = voice.id.lower()
                voice_name = voice.name.lower() if voice.name else ""
                
                # Verificar se é voz portuguesa
                if any(lang in voice_id or lang in voice_name 
                       for lang in ['portuguese', 'pt-pt', 'pt_pt', 'pt-br', 'brazil', 'portugal']):
                    self.engine.setProperty('voice', voice.id)
                    logger.info(f"Voz portuguesa encontrada: {voice.name}")
                    return
            
            # Se não encontrar portuguesa, usar a primeira disponível
            if voices:
                logger.warning("Voz portuguesa não encontrada, usando voz padrão")
        except Exception as e:
            logger.warning(f"Erro ao configurar voz: {e}")
    
    def speak(self, text: str, wait: bool = True):
        """
        Converte texto em fala.
        
        Args:
            text: Texto a falar
            wait: Se deve esperar pela conclusão
        """
        if not TTS_AVAILABLE:
            logger.error("TTS não disponível")
            return
        
        if not self.engine:
            self._initialize()
            if not self.engine:
                return
        
        with self._lock:
            try:
                self._is_speaking = True
                logger.info(f"A falar: {text[:50]}...")
                
                self.engine.say(text)
                
                if wait:
                    self.engine.runAndWait()
                
            except Exception as e:
                logger.error(f"Erro ao falar: {e}")
            finally:
                self._is_speaking = False
    
    def speak_async(self, text: str):
        """
        Fala de forma assíncrona (não bloqueante).
        
        Args:
            text: Texto a falar
        """
        thread = threading.Thread(
            target=self.speak,
            args=(text, True),
            daemon=True,
        )
        thread.start()
        return thread
    
    def stop(self):
        """Para a fala actual."""
        if self.engine and self._is_speaking:
            try:
                self.engine.stop()
                self._is_speaking = False
                logger.info("Fala interrompida")
            except Exception as e:
                logger.error(f"Erro ao parar: {e}")
    
    def set_rate(self, rate: int):
        """
        Define a velocidade da fala.
        
        Args:
            rate: Palavras por minuto (100-200 recomendado)
        """
        if self.engine:
            self.rate = rate
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """
        Define o volume da fala.
        
        Args:
            volume: Volume entre 0.0 e 1.0
        """
        if self.engine:
            self.volume = max(0.0, min(1.0, volume))
            self.engine.setProperty('volume', self.volume)
    
    def get_voices(self) -> list:
        """
        Lista as vozes disponíveis.
        
        Returns:
            Lista de vozes disponíveis
        """
        if not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [{"id": v.id, "name": v.name, "languages": v.languages} for v in voices]
        except:
            return []
    
    # =========================================================================
    # MÉTODOS PREDEFINIDOS
    # =========================================================================
    
    def say_welcome(self):
        """Diz mensagem de boas-vindas."""
        self.speak_async("Bem-vindo ao SharkCoders Assistant!")
    
    def say_listening(self):
        """Indica que está a ouvir."""
        self.speak_async("Estou a ouvir.")
    
    def say_not_understood(self):
        """Indica que não entendeu."""
        self.speak_async("Desculpa, não entendi. Podes repetir?")
    
    def say_success(self, action: str = ""):
        """Indica sucesso na operação."""
        if action:
            self.speak_async(f"{action} concluído com sucesso!")
        else:
            self.speak_async("Operação concluída com sucesso!")
    
    def say_error(self, message: str = ""):
        """Indica um erro."""
        if message:
            self.speak_async(f"Ocorreu um erro: {message}")
        else:
            self.speak_async("Ocorreu um erro. Por favor, tenta novamente.")
    
    def say_goodbye(self):
        """Diz adeus."""
        self.speak("Até à próxima! Bom trabalho!", wait=True)
    
    def say_time(self, time_str: str):
        """Diz a hora."""
        self.speak_async(f"São {time_str}")
    
    def say_date(self, date_str: str):
        """Diz a data."""
        self.speak_async(f"Hoje é {date_str}")
    
    @property
    def is_speaking(self) -> bool:
        """Retorna se está a falar."""
        return self._is_speaking
    
    def is_available(self) -> bool:
        """Verifica se o TTS está disponível."""
        return TTS_AVAILABLE and self.engine is not None


# Instância global
text_to_speech = TextToSpeech()


if __name__ == "__main__":
    # Teste do TTS
    print("=" * 50)
    print("🔊 Teste de Síntese de Voz (TTS)")
    print("=" * 50)
    
    if not text_to_speech.is_available():
        print("❌ TTS não disponível")
        print("   Instale: pip install pyttsx3")
        sys.exit(1)
    
    # Mostrar vozes disponíveis
    print("\n📋 Vozes disponíveis:")
    voices = text_to_speech.get_voices()
    for i, voice in enumerate(voices[:5]):
        print(f"   {i+1}. {voice['name']}")
    
    # Testar fala
    print("\n🔊 A testar fala...")
    text_to_speech.speak("Olá! Eu sou o assistente SharkCoders. Estou pronto para ajudar!")
    
    print("\n✅ Teste concluído!")
