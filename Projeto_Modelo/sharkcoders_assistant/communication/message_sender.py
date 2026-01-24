#!/usr/bin/env python3
"""
SharkCoders Assistant - Envio de Mensagens
Módulo para envio de mensagens via Telegram Bot API.
"""

import sys
from pathlib import Path
from typing import Tuple, Optional, List, Union
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ requests não instalado. Instale: pip install requests")

from config import TELEGRAM_CONFIG
from utils import logger


class TelegramSender:
    """
    Classe para envio de mensagens via Telegram Bot API.
    """
    
    def __init__(self, bot_token: str = None):
        """
        Inicializa o sender do Telegram.
        
        Args:
            bot_token: Token do bot (se não fornecido, usa config)
        """
        self.bot_token = bot_token or TELEGRAM_CONFIG.get("bot_token", "")
        self.base_url = TELEGRAM_CONFIG.get("api_url", "https://api.telegram.org/bot")
        self.available = REQUESTS_AVAILABLE and bool(self.bot_token)
        
        if not self.bot_token:
            logger.warning("Token do Telegram não configurado. "
                          "Defina TELEGRAM_BOT_TOKEN no ambiente.")
    
    def _get_url(self, method: str) -> str:
        """Constrói URL da API."""
        return f"{self.base_url}{self.bot_token}/{method}"
    
    def send_message(self, chat_id: Union[str, int], text: str, 
                     parse_mode: str = "HTML") -> Tuple[bool, str]:
        """
        Envia uma mensagem de texto.
        
        Args:
            chat_id: ID do chat/utilizador
            text: Texto da mensagem
            parse_mode: Modo de formatação ('HTML', 'Markdown', None)
        
        Returns:
            Tupla (sucesso, mensagem de resultado)
        """
        if not self.available:
            return False, "Telegram não configurado"
        
        try:
            url = self._get_url("sendMessage")
            data = {
                "chat_id": chat_id,
                "text": text,
            }
            if parse_mode:
                data["parse_mode"] = parse_mode
            
            response = requests.post(url, data=data, timeout=30)
            result = response.json()
            
            if result.get("ok"):
                logger.success(f"Mensagem enviada para {chat_id}")
                return True, "Mensagem enviada com sucesso"
            else:
                error = result.get("description", "Erro desconhecido")
                logger.error(f"Erro ao enviar mensagem: {error}")
                return False, error
                
        except requests.Timeout:
            return False, "Tempo limite excedido"
        except requests.RequestException as e:
            return False, f"Erro de rede: {e}"
        except Exception as e:
            return False, f"Erro: {e}"
    
    def send_image(self, chat_id: Union[str, int], image_path: Union[str, Path],
                   caption: str = "") -> Tuple[bool, str]:
        """
        Envia uma imagem.
        
        Args:
            chat_id: ID do chat/utilizador
            image_path: Caminho do ficheiro de imagem
            caption: Legenda opcional
        
        Returns:
            Tupla (sucesso, mensagem de resultado)
        """
        if not self.available:
            return False, "Telegram não configurado"
        
        image_path = Path(image_path)
        if not image_path.exists():
            return False, f"Ficheiro não encontrado: {image_path}"
        
        try:
            url = self._get_url("sendPhoto")
            
            with open(image_path, 'rb') as photo:
                files = {"photo": photo}
                data = {"chat_id": chat_id}
                if caption:
                    data["caption"] = caption[:1024]  # Limite do Telegram
                
                response = requests.post(url, data=data, files=files, timeout=60)
            
            result = response.json()
            
            if result.get("ok"):
                logger.success(f"Imagem enviada para {chat_id}")
                return True, "Imagem enviada com sucesso"
            else:
                error = result.get("description", "Erro desconhecido")
                logger.error(f"Erro ao enviar imagem: {error}")
                return False, error
                
        except requests.Timeout:
            return False, "Tempo limite excedido"
        except requests.RequestException as e:
            return False, f"Erro de rede: {e}"
        except Exception as e:
            return False, f"Erro: {e}"
    
    def send_document(self, chat_id: Union[str, int], document_path: Union[str, Path],
                      caption: str = "") -> Tuple[bool, str]:
        """
        Envia um documento/ficheiro.
        
        Args:
            chat_id: ID do chat/utilizador
            document_path: Caminho do ficheiro
            caption: Legenda opcional
        
        Returns:
            Tupla (sucesso, mensagem de resultado)
        """
        if not self.available:
            return False, "Telegram não configurado"
        
        document_path = Path(document_path)
        if not document_path.exists():
            return False, f"Ficheiro não encontrado: {document_path}"
        
        try:
            url = self._get_url("sendDocument")
            
            with open(document_path, 'rb') as doc:
                files = {"document": doc}
                data = {"chat_id": chat_id}
                if caption:
                    data["caption"] = caption[:1024]
                
                response = requests.post(url, data=data, files=files, timeout=60)
            
            result = response.json()
            
            if result.get("ok"):
                logger.success(f"Documento enviado para {chat_id}")
                return True, "Documento enviado com sucesso"
            else:
                error = result.get("description", "Erro desconhecido")
                return False, error
                
        except Exception as e:
            return False, f"Erro: {e}"
    
    def get_updates(self, offset: int = None, limit: int = 100) -> List[dict]:
        """
        Obtém actualizações (mensagens recebidas).
        
        Args:
            offset: ID da última actualização processada
            limit: Número máximo de actualizações
        
        Returns:
            Lista de actualizações
        """
        if not self.available:
            return []
        
        try:
            url = self._get_url("getUpdates")
            params = {"limit": limit}
            if offset:
                params["offset"] = offset
            
            response = requests.get(url, params=params, timeout=30)
            result = response.json()
            
            if result.get("ok"):
                return result.get("result", [])
            return []
            
        except Exception as e:
            logger.error(f"Erro ao obter actualizações: {e}")
            return []
    
    def get_chat_ids_from_updates(self) -> List[dict]:
        """
        Extrai IDs de chat das actualizações recentes.
        Útil para descobrir o chat_id quando se envia /start ao bot.
        
        Returns:
            Lista de dicionários com chat_id e username
        """
        updates = self.get_updates()
        chats = {}
        
        for update in updates:
            message = update.get("message", {})
            chat = message.get("chat", {})
            chat_id = chat.get("id")
            
            if chat_id and chat_id not in chats:
                chats[chat_id] = {
                    "chat_id": chat_id,
                    "type": chat.get("type"),
                    "username": chat.get("username"),
                    "first_name": chat.get("first_name"),
                }
        
        return list(chats.values())
    
    def get_me(self) -> Optional[dict]:
        """
        Obtém informação sobre o bot.
        
        Returns:
            Dicionário com informação do bot
        """
        if not self.available:
            return None
        
        try:
            url = self._get_url("getMe")
            response = requests.get(url, timeout=10)
            result = response.json()
            
            if result.get("ok"):
                return result.get("result")
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter info do bot: {e}")
            return None
    
    def set_token(self, token: str):
        """
        Define o token do bot.
        
        Args:
            token: Novo token
        """
        self.bot_token = token
        self.available = REQUESTS_AVAILABLE and bool(token)
    
    def is_available(self) -> bool:
        """Verifica se o Telegram está disponível."""
        return self.available


class MessageSender:
    """
    Interface unificada para envio de mensagens.
    Actualmente suporta Telegram, mas pode ser expandido.
    """
    
    def __init__(self):
        """Inicializa o sender."""
        self.telegram = TelegramSender()
    
    def send_message(self, destination: str, text: str, 
                     via: str = "telegram") -> Tuple[bool, str]:
        """
        Envia mensagem para um destino.
        
        Args:
            destination: Destino (chat_id para Telegram)
            text: Texto da mensagem
            via: Meio de envio ('telegram')
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        if via == "telegram":
            return self.telegram.send_message(destination, text)
        else:
            return False, f"Meio não suportado: {via}"
    
    def send_image(self, destination: str, image_path: str,
                   caption: str = "", via: str = "telegram") -> Tuple[bool, str]:
        """
        Envia imagem para um destino.
        
        Args:
            destination: Destino
            image_path: Caminho da imagem
            caption: Legenda
            via: Meio de envio
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        if via == "telegram":
            return self.telegram.send_image(destination, image_path, caption)
        else:
            return False, f"Meio não suportado: {via}"


# Instâncias globais
telegram_sender = TelegramSender()
message_sender = MessageSender()


if __name__ == "__main__":
    # Teste do sender
    print("=" * 50)
    print("📱 Teste do Telegram Sender")
    print("=" * 50)
    
    print(f"\n📦 requests disponível: {REQUESTS_AVAILABLE}")
    print(f"🔑 Token configurado: {'Sim' if telegram_sender.bot_token else 'Não'}")
    print(f"✅ Telegram disponível: {telegram_sender.is_available()}")
    
    if telegram_sender.is_available():
        # Obter info do bot
        print("\n🤖 Informação do bot:")
        bot_info = telegram_sender.get_me()
        if bot_info:
            print(f"   Nome: {bot_info.get('first_name')}")
            print(f"   Username: @{bot_info.get('username')}")
        
        # Listar chats conhecidos
        print("\n💬 Chats recentes:")
        chats = telegram_sender.get_chat_ids_from_updates()
        for chat in chats[:5]:
            print(f"   • {chat['chat_id']}: {chat.get('first_name', 'N/A')}")
        
        if not chats:
            print("   Nenhum chat encontrado. Envie /start ao bot.")
    else:
        print("\n⚠️ Para usar o Telegram:")
        print("   1. Crie um bot com @BotFather")
        print("   2. Defina TELEGRAM_BOT_TOKEN no ambiente")
        print("   3. Envie /start ao bot para obter o chat_id")
    
    print("\n✅ Teste concluído!")
