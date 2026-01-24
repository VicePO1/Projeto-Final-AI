#!/usr/bin/env python3
"""
SharkCoders Assistant - Processamento de Comandos de Voz
Módulo para processar e executar comandos de voz.
"""

import sys
from pathlib import Path
from typing import Callable, Optional, Any
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import VOICE_COMMANDS
from utils import logger


class VoiceCommandProcessor:
    """
    Processador de comandos de voz.
    Mapeia texto falado para ações.
    """
    
    def __init__(self):
        """Inicializa o processador de comandos."""
        # Mapa de comandos de texto → identificador de ação
        self.commands = dict(VOICE_COMMANDS)
        
        # Mapa de identificador de ação → função handler
        self.handlers: dict[str, Callable] = {}
        
        # Registar handlers padrão
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Regista handlers padrão para comandos."""
        # Os handlers serão registados pela aplicação principal
        # Aqui só definimos placeholders
        
        self.handlers = {
            "capture_screen": self._default_handler,
            "read_image": self._default_handler,
            "send_image": self._default_handler,
            "tell_time": self._tell_time,
            "tell_date": self._tell_date,
            "tell_joke": self._default_handler,
            "get_quote": self._default_handler,
            "get_fact": self._default_handler,
            "active_window": self._default_handler,
            "list_windows": self._default_handler,
            "system_info": self._default_handler,
            "help": self._show_help,
            "exit": self._exit_app,
        }
    
    def _default_handler(self, *args, **kwargs) -> str:
        """Handler padrão que não faz nada."""
        return "Comando reconhecido mas handler não implementado"
    
    def _tell_time(self) -> str:
        """Handler para dizer a hora."""
        try:
            from system import os_interaction
            from voice import text_to_speech
            
            info = os_interaction.get_datetime_info()
            time_str = info['time']
            text_to_speech.say_time(time_str)
            return f"São {time_str}"
        except Exception as e:
            return f"Erro ao obter hora: {e}"
    
    def _tell_date(self) -> str:
        """Handler para dizer a data."""
        try:
            from system import os_interaction
            from voice import text_to_speech
            
            info = os_interaction.get_datetime_info()
            date_str = info['date']
            text_to_speech.say_date(date_str)
            return f"Hoje é {date_str}"
        except Exception as e:
            return f"Erro ao obter data: {e}"
    
    def _show_help(self) -> str:
        """Handler para mostrar ajuda."""
        help_text = self.get_help_text()
        logger.info(help_text)
        return help_text
    
    def _exit_app(self) -> str:
        """Handler para sair da aplicação."""
        try:
            from voice import text_to_speech
            text_to_speech.say_goodbye()
        except:
            pass
        return "exit"
    
    def register_handler(self, action: str, handler: Callable):
        """
        Regista um handler para uma ação.
        
        Args:
            action: Identificador da ação (ex: 'capture_screen')
            handler: Função a executar
        """
        self.handlers[action] = handler
        logger.debug(f"Handler registado para: {action}")
    
    def register_command(self, command: str, action: str):
        """
        Regista um novo comando de voz.
        
        Args:
            command: Texto do comando (ex: 'tirar foto')
            action: Identificador da ação associada
        """
        self.commands[command.lower()] = action
        logger.debug(f"Comando registado: '{command}' → {action}")
    
    def process(self, text: str) -> Optional[str]:
        """
        Processa texto e executa comando correspondente.
        
        Args:
            text: Texto reconhecido da voz
        
        Returns:
            Resultado da execução ou None se comando não reconhecido
        """
        if not text:
            return None
        
        text = text.lower().strip()
        logger.info(f"A processar: '{text}'")
        
        # Procurar comando exacto
        action = self.commands.get(text)
        
        # Se não encontrar exacto, procurar parcial
        if not action:
            action = self._find_partial_match(text)
        
        if not action:
            logger.warning(f"Comando não reconhecido: '{text}'")
            try:
                from voice import text_to_speech
                text_to_speech.say_not_understood()
            except:
                pass
            return None
        
        # Executar handler
        handler = self.handlers.get(action)
        if handler:
            try:
                logger.info(f"A executar: {action}")
                result = handler()
                return result
            except Exception as e:
                logger.error(f"Erro ao executar {action}: {e}")
                return f"Erro: {e}"
        else:
            logger.warning(f"Handler não encontrado para: {action}")
            return None
    
    def _find_partial_match(self, text: str) -> Optional[str]:
        """
        Procura correspondência parcial no texto.
        
        Args:
            text: Texto a procurar
        
        Returns:
            Ação correspondente ou None
        """
        # Procurar se algum comando está contido no texto
        for command, action in self.commands.items():
            if command in text:
                return action
        
        # Procurar se o texto está contido em algum comando
        for command, action in self.commands.items():
            if text in command:
                return action
        
        # Procurar por palavras-chave
        keywords = {
            "captura": "capture_screen",
            "screenshot": "capture_screen",
            "ecrã": "capture_screen",
            "ler": "read_image",
            "texto": "read_image",
            "ocr": "read_image",
            "enviar": "send_image",
            "telegram": "send_image",
            "hora": "tell_time",
            "horas": "tell_time",
            "data": "tell_date",
            "dia": "tell_date",
            "piada": "tell_joke",
            "citação": "get_quote",
            "facto": "get_fact",
            "janela": "active_window",
            "janelas": "list_windows",
            "sistema": "system_info",
            "ajuda": "help",
            "sair": "exit",
            "fechar": "exit",
        }
        
        for keyword, action in keywords.items():
            if keyword in text:
                return action
        
        return None
    
    def get_action_for_text(self, text: str) -> Optional[str]:
        """
        Retorna a ação correspondente a um texto sem executar.
        
        Args:
            text: Texto a verificar
        
        Returns:
            Identificador da ação ou None
        """
        text = text.lower().strip()
        action = self.commands.get(text)
        if not action:
            action = self._find_partial_match(text)
        return action
    
    def get_commands(self) -> dict:
        """
        Retorna todos os comandos registados.
        
        Returns:
            Dicionário de comandos → ações
        """
        return dict(self.commands)
    
    def get_help_text(self) -> str:
        """
        Retorna texto de ajuda com comandos disponíveis.
        
        Returns:
            Texto formatado com lista de comandos
        """
        # Agrupar comandos por ação
        actions = {}
        for cmd, action in self.commands.items():
            if action not in actions:
                actions[action] = []
            actions[action].append(cmd)
        
        # Descrições das ações
        descriptions = {
            "capture_screen": "Capturar ecrã",
            "read_image": "Extrair texto (OCR)",
            "send_image": "Enviar imagem",
            "tell_time": "Dizer as horas",
            "tell_date": "Dizer a data",
            "tell_joke": "Contar uma piada",
            "get_quote": "Dizer uma citação",
            "get_fact": "Dizer um facto",
            "active_window": "Mostrar janela activa",
            "list_windows": "Listar janelas",
            "system_info": "Info do sistema",
            "help": "Mostrar ajuda",
            "exit": "Sair da aplicação",
        }
        
        # Formatar texto
        lines = ["📋 Comandos de Voz Disponíveis:", ""]
        
        for action, commands in sorted(actions.items()):
            desc = descriptions.get(action, action)
            cmds = ", ".join([f'"{c}"' for c in commands[:3]])
            lines.append(f"  • {desc}:")
            lines.append(f"      {cmds}")
        
        return "\n".join(lines)


# Instância global
voice_processor = VoiceCommandProcessor()


if __name__ == "__main__":
    # Teste do processador de comandos
    print("=" * 50)
    print("🎤 Teste do Processador de Comandos de Voz")
    print("=" * 50)
    
    # Mostrar ajuda
    print("\n" + voice_processor.get_help_text())
    
    # Testar alguns comandos
    test_commands = [
        "capturar ecrã",
        "que horas são",
        "diz uma piada",
        "comando desconhecido",
        "quero tirar uma captura",
        "ajuda",
    ]
    
    print("\n" + "=" * 50)
    print("📝 Testes de Reconhecimento:")
    print("=" * 50)
    
    for cmd in test_commands:
        action = voice_processor.get_action_for_text(cmd)
        status = "✅" if action else "❌"
        result = action or "não reconhecido"
        print(f"  {status} '{cmd}' → {result}")
    
    print("\n✅ Teste concluído!")
