#!/usr/bin/env python3
"""
SharkCoders Assistant - Reconhecimento de Voz
Módulo para captura e reconhecimento de fala.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️ SpeechRecognition não instalado. Instale: pip install SpeechRecognition PyAudio")

from config import VOICE_CONFIG
from utils import logger


class SpeechRecognizer:
    """
    Classe para reconhecimento de voz.
    Usa a biblioteca SpeechRecognition com Google Speech-to-Text.
    """
    
    def __init__(self):
        """Inicializa o reconhecedor de voz."""
        self.recognizer = None
        self.microphone = None
        self.language = VOICE_CONFIG.get("language", "pt-PT")
        self.timeout = VOICE_CONFIG.get("timeout", 5)
        self.phrase_timeout = VOICE_CONFIG.get("phrase_timeout", 3)
        self.energy_threshold = VOICE_CONFIG.get("energy_threshold", 300)
        self._is_listening = False
        self._stop_listening = None
        
        if SPEECH_AVAILABLE:
            self._initialize()
    
    def _initialize(self):
        """Inicializa os componentes de reconhecimento."""
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = self.energy_threshold
            self.recognizer.dynamic_energy_threshold = True
            self.microphone = sr.Microphone()
            logger.success("Reconhecedor de voz inicializado")
        except Exception as e:
            logger.error(f"Erro ao inicializar reconhecedor: {e}")
            self.recognizer = None
    
    def calibrate(self, duration: float = 1.0) -> bool:
        """
        Calibra o reconhecedor para o ruído ambiente.
        
        Args:
            duration: Duração da calibração em segundos
        
        Returns:
            True se calibração bem sucedida
        """
        if not self.recognizer or not self.microphone:
            return False
        
        try:
            logger.info(f"A calibrar microfone ({duration}s)...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
            logger.success(f"Calibração concluída. Limiar de energia: {self.recognizer.energy_threshold}")
            return True
        except Exception as e:
            logger.error(f"Erro na calibração: {e}")
            return False
    
    def listen_once(self) -> str | None:
        """
        Captura uma única frase do microfone.
        
        Returns:
            Texto reconhecido ou None se falhar
        """
        if not SPEECH_AVAILABLE:
            logger.error("SpeechRecognition não disponível")
            return None
        
        if not self.recognizer or not self.microphone:
            self._initialize()
            if not self.recognizer:
                return None
        
        try:
            logger.info("A ouvir...")
            with self.microphone as source:
                # Ajuste rápido para ruído
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Capturar áudio
                audio = self.recognizer.listen(
                    source,
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_timeout,
                )
            
            # Reconhecer com Google
            logger.info("A processar...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.success(f"Reconhecido: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            logger.warning("Tempo esgotado - nenhuma fala detectada")
            return None
        except sr.UnknownValueError:
            logger.warning("Não foi possível entender o áudio")
            return None
        except sr.RequestError as e:
            logger.error(f"Erro no serviço de reconhecimento: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro no reconhecimento: {e}")
            return None
    
    def start_continuous_listening(self, callback) -> bool:
        """
        Inicia escuta contínua em background.
        
        Args:
            callback: Função a chamar quando reconhecer texto
                     callback(text: str)
        
        Returns:
            True se iniciado com sucesso
        """
        if not SPEECH_AVAILABLE or not self.recognizer or not self.microphone:
            return False
        
        if self._is_listening:
            logger.warning("Já está a ouvir")
            return False
        
        def audio_callback(recognizer, audio):
            """Callback interno para processar áudio."""
            try:
                text = recognizer.recognize_google(audio, language=self.language)
                if text:
                    callback(text.lower())
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                logger.error(f"Erro no reconhecimento contínuo: {e}")
        
        try:
            # Calibrar primeiro
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Iniciar escuta em background
            self._stop_listening = self.recognizer.listen_in_background(
                self.microphone,
                audio_callback,
                phrase_time_limit=self.phrase_timeout,
            )
            self._is_listening = True
            logger.success("Escuta contínua iniciada")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao iniciar escuta contínua: {e}")
            return False
    
    def stop_continuous_listening(self):
        """Para a escuta contínua."""
        if self._stop_listening:
            self._stop_listening(wait_for_stop=False)
            self._stop_listening = None
        self._is_listening = False
        logger.info("Escuta contínua parada")
    
    @property
    def is_listening(self) -> bool:
        """Retorna se está a ouvir."""
        return self._is_listening
    
    def is_available(self) -> bool:
        """Verifica se o reconhecimento está disponível."""
        return SPEECH_AVAILABLE and self.recognizer is not None


# Instância global
speech_recognizer = SpeechRecognizer()


if __name__ == "__main__":
    # Teste do reconhecimento de voz
    print("=" * 50)
    print("🎤 Teste de Reconhecimento de Voz")
    print("=" * 50)
    
    if not speech_recognizer.is_available():
        print("❌ Reconhecimento não disponível")
        print("   Instale: pip install SpeechRecognition PyAudio")
        sys.exit(1)
    
    # Calibrar
    print("\n📊 A calibrar microfone...")
    speech_recognizer.calibrate(2)
    
    # Teste de reconhecimento único
    print("\n🎤 Diga algo...")
    text = speech_recognizer.listen_once()
    
    if text:
        print(f"\n✅ Reconhecido: {text}")
    else:
        print("\n❌ Nenhum texto reconhecido")
