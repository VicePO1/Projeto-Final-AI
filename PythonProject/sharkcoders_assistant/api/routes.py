#!/usr/bin/env python3
"""
SharkCoders Assistant - Rotas da API
Definição dos endpoints da API REST.
"""

import sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from flask import Flask, jsonify, request, send_file
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from config import APP_NAME, APP_VERSION


def register_routes(app: 'Flask', api_server):
    """
    Regista todas as rotas da API.
    
    Args:
        app: Aplicação Flask
        api_server: Instância do AssistantAPI
    """
    
    @app.route('/')
    def index():
        """Página inicial com informação da API."""
        return jsonify({
            "name": APP_NAME,
            "version": APP_VERSION,
            "description": "API REST do SharkCoders Assistant",
            "endpoints": {
                "GET /": "Esta página",
                "GET /api/status": "Estado do assistente",
                "GET /api/text": "Último texto extraído (OCR/voz)",
                "GET /api/screenshot": "Última captura de ecrã",
                "POST /api/command": "Executar comando",
                "GET /api/info": "Informação do sistema",
                "GET /api/commands": "Lista de comandos disponíveis",
            },
            "timestamp": datetime.now().isoformat(),
        })
    
    @app.route('/api/status')
    def get_status():
        """Retorna o estado actual do assistente."""
        state = api_server.get_state()
        
        return jsonify({
            "status": state.get("status", "unknown"),
            "last_ocr_text_length": len(state.get("last_ocr_text", "")),
            "last_voice_text_length": len(state.get("last_voice_text", "")),
            "has_screenshot": bool(state.get("last_screenshot_path")),
            "api_running": api_server.is_running,
            "timestamp": datetime.now().isoformat(),
        })
    
    @app.route('/api/text')
    def get_text():
        """Retorna o último texto extraído."""
        state = api_server.get_state()
        
        return jsonify({
            "ocr_text": state.get("last_ocr_text", ""),
            "voice_text": state.get("last_voice_text", ""),
            "timestamp": datetime.now().isoformat(),
        })
    
    @app.route('/api/screenshot')
    def get_screenshot():
        """Retorna a última captura de ecrã."""
        screenshot_path = api_server.get_state("last_screenshot_path")
        
        if screenshot_path and Path(screenshot_path).exists():
            return send_file(
                screenshot_path,
                mimetype='image/png',
                as_attachment=False,
            )
        else:
            return jsonify({
                "error": "Nenhuma captura disponível",
                "screenshot_path": screenshot_path,
            }), 404
    
    @app.route('/api/screenshot/info')
    def get_screenshot_info():
        """Retorna informação sobre a última captura."""
        screenshot_path = api_server.get_state("last_screenshot_path")
        
        if screenshot_path and Path(screenshot_path).exists():
            path = Path(screenshot_path)
            stat = path.stat()
            
            return jsonify({
                "available": True,
                "path": str(path),
                "filename": path.name,
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
        else:
            return jsonify({
                "available": False,
                "path": screenshot_path,
            })
    
    @app.route('/api/command', methods=['POST'])
    def execute_command():
        """Executa um comando no assistente."""
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Corpo da requisição vazio ou inválido",
            }), 400
        
        command = data.get("command")
        params = data.get("params", {})
        
        if not command:
            return jsonify({
                "success": False,
                "error": "Campo 'command' obrigatório",
            }), 400
        
        result = api_server.execute_command(command, params)
        
        return jsonify({
            **result,
            "command": command,
            "timestamp": datetime.now().isoformat(),
        })
    
    @app.route('/api/commands')
    def list_commands():
        """Lista os comandos disponíveis."""
        commands = list(api_server.command_handlers.keys())
        
        return jsonify({
            "commands": commands,
            "count": len(commands),
            "timestamp": datetime.now().isoformat(),
        })
    
    @app.route('/api/info')
    def get_info():
        """Retorna informação do sistema."""
        try:
            from system import os_interaction
            info = os_interaction.get_system_info()
        except ImportError:
            info = {"error": "Módulo system não disponível"}
        
        return jsonify({
            "app": {
                "name": APP_NAME,
                "version": APP_VERSION,
            },
            "system": info,
            "timestamp": datetime.now().isoformat(),
        })
    
    @app.route('/api/state')
    def get_full_state():
        """Retorna o estado completo (debug)."""
        return jsonify({
            "state": api_server.get_state(),
            "timestamp": datetime.now().isoformat(),
        })
    
    @app.route('/api/state', methods=['POST'])
    def update_state():
        """Actualiza o estado (debug)."""
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "Dados inválidos"}), 400
        
        for key, value in data.items():
            api_server.update_state(key, value)
        
        return jsonify({
            "success": True,
            "updated_keys": list(data.keys()),
            "timestamp": datetime.now().isoformat(),
        })
    
    # =========================================================================
    # ENDPOINTS DE ACÇÕES
    # =========================================================================
    
    @app.route('/api/capture', methods=['POST'])
    def capture_screen():
        """Endpoint para capturar ecrã."""
        try:
            from automation import screen_capture
            
            image, path = screen_capture.capture_full_screen()
            
            if path:
                api_server.update_state("last_screenshot_path", str(path))
                return jsonify({
                    "success": True,
                    "path": str(path),
                    "timestamp": datetime.now().isoformat(),
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Falha na captura",
                }), 500
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e),
            }), 500
    
    @app.route('/api/ocr', methods=['POST'])
    def extract_text():
        """Endpoint para extrair texto da última imagem."""
        try:
            screenshot_path = api_server.get_state("last_screenshot_path")
            
            if not screenshot_path or not Path(screenshot_path).exists():
                return jsonify({
                    "success": False,
                    "error": "Nenhuma imagem disponível",
                }), 400
            
            from vision import ocr_engine, image_processor
            from PIL import Image
            
            # Carregar e processar imagem
            image = Image.open(screenshot_path)
            processed = image_processor.prepare_for_ocr(image)
            
            # Extrair texto
            text = ocr_engine.extract_text(processed)
            
            api_server.update_state("last_ocr_text", text)
            
            return jsonify({
                "success": True,
                "text": text,
                "length": len(text),
                "timestamp": datetime.now().isoformat(),
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e),
            }), 500
    
    @app.route('/api/speak', methods=['POST'])
    def speak_text():
        """Endpoint para falar texto."""
        data = request.get_json()
        text = data.get("text", "") if data else ""
        
        if not text:
            return jsonify({
                "success": False,
                "error": "Campo 'text' obrigatório",
            }), 400
        
        try:
            from voice import text_to_speech
            text_to_speech.speak_async(text)
            
            return jsonify({
                "success": True,
                "text": text,
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e),
            }), 500
    
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    print("Este módulo define as rotas da API.")
    print("Execute server.py para testar o servidor.")
