#!/usr/bin/env python3
"""
SharkCoders Assistant - Servidor API Flask
Servidor HTTP para controlo remoto do assistente.
"""

import sys
import threading
from pathlib import Path
from typing import Callable, Optional, Dict, Any
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from flask import Flask, jsonify, request, send_file
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("⚠️ Flask não instalado. Instale: pip install Flask")

from config import API_CONFIG, APP_NAME, APP_VERSION
from utils import logger


class AssistantAPI:
    """
    Servidor API REST para o SharkCoders Assistant.
    Permite controlo remoto via HTTP.
    """
    
    def __init__(self):
        """Inicializa o servidor API."""
        self.available = FLASK_AVAILABLE
        self.app = None
        self.host = API_CONFIG.get("host", "127.0.0.1")
        self.port = API_CONFIG.get("port", 5000)
        self.debug = API_CONFIG.get("debug", False)
        self._server_thread = None
        self._running = False
        
        # Estado partilhado
        self.state = {
            "last_ocr_text": "",
            "last_voice_text": "",
            "last_screenshot_path": "",
            "status": "ready",
        }
        
        # Handlers de comandos
        self.command_handlers: Dict[str, Callable] = {}
        
        if self.available:
            self._create_app()
    
    def _create_app(self):
        """Cria a aplicação Flask."""
        self.app = Flask(__name__)
        
        # Desactivar logs do Flask em produção
        if not self.debug:
            import logging
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
        
        # Registar rotas
        self._register_routes()
    
    def _register_routes(self):
        """Regista as rotas da API."""
        from .routes import register_routes
        register_routes(self.app, self)
    
    def start(self, threaded: bool = True) -> bool:
        """
        Inicia o servidor API.
        
        Args:
            threaded: Se deve correr em thread separada
        
        Returns:
            True se iniciado com sucesso
        """
        if not self.available:
            logger.error("Flask não disponível")
            return False
        
        if self._running:
            logger.warning("API já está a correr")
            return True
        
        try:
            if threaded:
                self._server_thread = threading.Thread(
                    target=self._run_server,
                    daemon=True,
                )
                self._server_thread.start()
                self._running = True
                logger.success(f"API iniciada em http://{self.host}:{self.port}")
            else:
                self._run_server()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao iniciar API: {e}")
            return False
    
    def _run_server(self):
        """Executa o servidor Flask."""
        try:
            self.app.run(
                host=self.host,
                port=self.port,
                debug=self.debug,
                use_reloader=False,
                threaded=True,
            )
        except Exception as e:
            logger.error(f"Erro no servidor: {e}")
            self._running = False
    
    def stop(self):
        """Para o servidor (nota: Flask não suporta stop gracioso facilmente)."""
        self._running = False
        logger.info("API a parar...")
    
    def register_command(self, command: str, handler: Callable):
        """
        Regista um handler para um comando.
        
        Args:
            command: Nome do comando
            handler: Função a executar
        """
        self.command_handlers[command] = handler
        logger.debug(f"Comando API registado: {command}")
    
    def execute_command(self, command: str, params: dict = None) -> Dict[str, Any]:
        """
        Executa um comando registado.
        
        Args:
            command: Nome do comando
            params: Parâmetros do comando
        
        Returns:
            Resultado da execução
        """
        handler = self.command_handlers.get(command)
        
        if handler:
            try:
                result = handler(params) if params else handler()
                return {"success": True, "result": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {"success": False, "error": f"Comando desconhecido: {command}"}
    
    def update_state(self, key: str, value: Any):
        """
        Actualiza o estado partilhado.
        
        Args:
            key: Chave do estado
            value: Novo valor
        """
        self.state[key] = value
    
    def get_state(self, key: str = None) -> Any:
        """
        Obtém valor do estado.
        
        Args:
            key: Chave (None para todo o estado)
        
        Returns:
            Valor do estado
        """
        if key:
            return self.state.get(key)
        return dict(self.state)
    
    @property
    def is_running(self) -> bool:
        """Verifica se o servidor está a correr."""
        return self._running
    
    def get_url(self) -> str:
        """Retorna URL do servidor."""
        return f"http://{self.host}:{self.port}"


# Instância global
assistant_api = AssistantAPI()


if __name__ == "__main__":
    # Teste do servidor
    print("=" * 50)
    print("🌐 Teste do Servidor API")
    print("=" * 50)
    
    print(f"\n📦 Flask disponível: {FLASK_AVAILABLE}")
    
    if FLASK_AVAILABLE:
        # Registar comando de teste
        def test_command(params=None):
            return "Comando executado com sucesso!"
        
        assistant_api.register_command("test", test_command)
        
        print(f"\n🚀 A iniciar servidor em http://{assistant_api.host}:{assistant_api.port}")
        print("   Prima Ctrl+C para parar")
        
        # Iniciar em modo não-threaded para teste
        assistant_api.start(threaded=False)
    else:
        print("\n❌ Flask não disponível")
        print("   Instale: pip install Flask")
