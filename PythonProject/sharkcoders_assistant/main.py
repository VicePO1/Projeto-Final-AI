# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════╗
║           🦈 SHARKCODERS ASSISTANT - MAIN 🦈                  ║
║         Assistente Multimodal Inteligente                     ║
║                                                               ║
║  Desenvolvido pela equipa SharkCoders                         ║
║  Versão: 1.0.0                                                ║
╚═══════════════════════════════════════════════════════════════╝

Ponto de entrada principal do SharkCoders Assistant.
Este ficheiro inicializa todos os módulos e lança a aplicação.
"""

import sys
import os

# Adiciona o diretório pai ao path para importações
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def print_welcome():
    """Imprime a mensagem de boas-vindas"""
    try:
        from assets import print_banner
        print_banner()
    except ImportError:
        print("\n" + "="*60)
        print("🦈 SHARKCODERS ASSISTANT 🦈")
        print("="*60 + "\n")


def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    missing = []
    
    dependencies = [
        ('tkinter', 'tkinter (incluído no Python)'),
        ('PIL', 'Pillow'),
        ('cv2', 'opencv-python'),
        ('speech_recognition', 'SpeechRecognition'),
        ('pyttsx3', 'pyttsx3'),
        ('pyautogui', 'PyAutoGUI'),
        ('requests', 'requests'),
        ('flask', 'Flask'),
    ]
    
    optional = [
        ('pytesseract', 'pytesseract'),
        ('pyaudio', 'PyAudio'),
        ('psutil', 'psutil'),
    ]
    
    print("🔍 A verificar dependências...")
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NÃO INSTALADO")
            missing.append(name)
    
    print("\n📦 Dependências opcionais:")
    for module, name in optional:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ⚠️  {name} - não instalado (opcional)")
    
    if missing:
        print("\n" + "="*60)
        print("⚠️  ATENÇÃO: Algumas dependências não estão instaladas!")
        print("Execute: pip install -r requirements.txt")
        print("="*60 + "\n")
        return False
    
    print("\n✅ Todas as dependências obrigatórias estão instaladas!\n")
    return True


def initialize_modules():
    """Inicializa os módulos do assistente"""
    print("🔧 A inicializar módulos...")
    
    modules_status = {}
    
    # Config
    try:
        from config import APP_NAME, VERSION
        modules_status['config'] = True
        print(f"  ✅ Config carregado ({APP_NAME} v{VERSION})")
    except Exception as e:
        modules_status['config'] = False
        print(f"  ❌ Config: {e}")
    
    # Utils
    try:
        from utils import Logger
        modules_status['utils'] = True
        print("  ✅ Utils")
    except Exception as e:
        modules_status['utils'] = False
        print(f"  ❌ Utils: {e}")
    
    # Assets
    try:
        from assets import SHARK_LOGO
        modules_status['assets'] = True
        print("  ✅ Assets")
    except Exception as e:
        modules_status['assets'] = False
        print(f"  ⚠️  Assets: {e}")
    
    # GUI
    try:
        from gui import MainWindow
        modules_status['gui'] = True
        print("  ✅ GUI")
    except Exception as e:
        modules_status['gui'] = False
        print(f"  ❌ GUI: {e}")
    
    # Voice
    try:
        from voice import speech_recognizer, text_to_speech
        modules_status['voice'] = True
        print("  ✅ Voice")
    except Exception as e:
        modules_status['voice'] = False
        print(f"  ⚠️  Voice: {e}")
    
    # Automation
    try:
        from automation import mouse_controller, keyboard_controller, screen_capture
        modules_status['automation'] = True
        print("  ✅ Automation")
    except Exception as e:
        modules_status['automation'] = False
        print(f"  ⚠️  Automation: {e}")
    
    # Vision
    try:
        from vision import image_processor, ocr_engine
        modules_status['vision'] = True
        print("  ✅ Vision")
    except Exception as e:
        modules_status['vision'] = False
        print(f"  ⚠️  Vision: {e}")
    
    # Communication
    try:
        from communication import telegram_sender
        modules_status['communication'] = True
        print("  ✅ Communication")
    except Exception as e:
        modules_status['communication'] = False
        print(f"  ⚠️  Communication: {e}")
    
    # API
    try:
        from api import AssistantAPI
        modules_status['api'] = True
        print("  ✅ API")
    except Exception as e:
        modules_status['api'] = False
        print(f"  ⚠️  API: {e}")
    
    # System
    try:
        from system import os_interaction
        modules_status['system'] = True
        print("  ✅ System")
    except Exception as e:
        modules_status['system'] = False
        print(f"  ⚠️  System: {e}")
    
    # Verifica se os módulos essenciais estão OK
    essential = ['config', 'utils', 'gui']
    essential_ok = all(modules_status.get(m, False) for m in essential)
    
    if essential_ok:
        print("\n✅ Módulos essenciais inicializados com sucesso!\n")
    else:
        print("\n❌ Erro ao inicializar módulos essenciais!\n")
    
    return modules_status, essential_ok


def create_main_window():
    """Cria e configura a janela principal"""
    from gui import MainWindow
    from utils import Logger
    
    logger = Logger("MainWindow")
    logger.info("A criar janela principal...")
    
    # Cria a janela
    window = MainWindow()
    
    return window


def start_api_server():
    """Inicia o servidor API em segundo plano"""
    try:
        from api import AssistantAPI
        from config import API_HOST, API_PORT
        
        api = AssistantAPI()
        api.start()
        print(f"🌐 API Server iniciado em http://{API_HOST}:{API_PORT}")
        return api
    except Exception as e:
        print(f"⚠️  Não foi possível iniciar o servidor API: {e}")
        return None


def run_cli_mode():
    """Executa o assistente em modo CLI (sem interface gráfica)"""
    from utils import Logger
    from system import os_interaction
    
    logger = Logger("CLI")
    
    print("\n" + "="*60)
    print("🖥️  MODO CLI - SharkCoders Assistant")
    print("="*60)
    print("Digite 'help' para ver os comandos disponíveis")
    print("Digite 'exit' para sair\n")
    
    commands = {
        'help': 'Mostra esta ajuda',
        'info': 'Mostra informações do sistema',
        'time': 'Mostra a hora atual',
        'date': 'Mostra a data atual',
        'disk': 'Mostra uso do disco',
        'screenshot': 'Captura o ecrã',
        'say [texto]': 'Fala o texto especificado',
        'quote': 'Obtém uma citação aleatória',
        'joke': 'Obtém uma piada aleatória',
        'fact': 'Obtém um facto interessante',
        'weather [cidade]': 'Obtém meteorologia',
        'api start': 'Inicia o servidor API',
        'exit': 'Sai do programa',
    }
    
    api_server = None
    
    while True:
        try:
            user_input = input("🦈 > ").strip()
            
            if not user_input:
                continue
            
            cmd = user_input.lower()
            parts = user_input.split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ''
            
            if cmd == 'exit' or cmd == 'quit':
                print("👋 Adeus! Obrigado por usar o SharkCoders Assistant!")
                if api_server:
                    api_server.stop()
                break
            
            elif cmd == 'help':
                print("\n📖 Comandos disponíveis:")
                for c, desc in commands.items():
                    print(f"  {c:20} - {desc}")
                print()
            
            elif cmd == 'info':
                info = os_interaction.get_system_info()
                print("\n📊 Informações do Sistema:")
                for key, value in info.items():
                    print(f"  {key}: {value}")
                print()
            
            elif cmd == 'time':
                print(f"🕐 Hora atual: {os_interaction.get_current_time()}")
            
            elif cmd == 'date':
                print(f"📅 Data atual: {os_interaction.get_current_date()}")
            
            elif cmd == 'disk':
                disk = os_interaction.get_disk_usage()
                print(f"\n💾 Uso do Disco:")
                print(f"  Total: {disk.get('total_gb', 'N/A')} GB")
                print(f"  Usado: {disk.get('usado_gb', 'N/A')} GB ({disk.get('percentagem_usado', 'N/A')}%)")
                print(f"  Livre: {disk.get('livre_gb', 'N/A')} GB")
                print()
            
            elif cmd == 'screenshot':
                try:
                    from automation import screen_capture
                    filepath = screen_capture.capture_full_screen()
                    if filepath:
                        print(f"📸 Screenshot guardado: {filepath}")
                    else:
                        print("❌ Erro ao capturar ecrã")
                except Exception as e:
                    print(f"❌ Erro: {e}")
            
            elif command == 'say':
                if args:
                    try:
                        from voice import text_to_speech
                        text_to_speech.speak(args)
                        print(f"🔊 A dizer: {args}")
                    except Exception as e:
                        print(f"❌ Erro ao falar: {e}")
                else:
                    print("⚠️  Uso: say [texto]")
            
            elif cmd == 'quote':
                try:
                    from communication import get_quote
                    quote = get_quote()
                    if quote:
                        print(f"\n💬 \"{quote['quote']}\"")
                        print(f"   - {quote['author']}\n")
                    else:
                        print("❌ Não foi possível obter citação")
                except Exception as e:
                    print(f"❌ Erro: {e}")
            
            elif cmd == 'joke':
                try:
                    from communication import get_joke
                    joke = get_joke()
                    if joke:
                        print(f"\n😂 {joke}\n")
                    else:
                        print("❌ Não foi possível obter piada")
                except Exception as e:
                    print(f"❌ Erro: {e}")
            
            elif cmd == 'fact':
                try:
                    from communication import get_fact
                    fact = get_fact()
                    if fact:
                        print(f"\n🧠 {fact}\n")
                    else:
                        print("❌ Não foi possível obter facto")
                except Exception as e:
                    print(f"❌ Erro: {e}")
            
            elif command == 'weather':
                if args:
                    try:
                        from communication import get_weather
                        weather = get_weather(args)
                        if weather and 'erro' not in weather:
                            print(f"\n🌤️  Meteorologia para {weather.get('cidade', args)}:")
                            print(f"  Temperatura: {weather.get('temperatura', 'N/A')}°C")
                            print(f"  Descrição: {weather.get('descricao', 'N/A')}")
                            print(f"  Humidade: {weather.get('humidade', 'N/A')}%")
                            print()
                        else:
                            print(f"❌ {weather.get('erro', 'Erro desconhecido')}")
                    except Exception as e:
                        print(f"❌ Erro: {e}")
                else:
                    print("⚠️  Uso: weather [cidade]")
            
            elif cmd == 'api start':
                if not api_server:
                    api_server = start_api_server()
                else:
                    print("⚠️  Servidor API já está a correr")
            
            else:
                print(f"❌ Comando não reconhecido: {command}")
                print("   Digite 'help' para ver os comandos disponíveis")
        
        except KeyboardInterrupt:
            print("\n👋 Interrompido pelo utilizador")
            if api_server:
                api_server.stop()
            break
        except Exception as e:
            logger.error(f"Erro no CLI: {e}")
            print(f"❌ Erro: {e}")


def main():
    """Função principal"""
    import argparse
    
    # Parser de argumentos
    parser = argparse.ArgumentParser(
        description='SharkCoders Assistant - Assistente Multimodal Inteligente'
    )
    parser.add_argument(
        '--cli', 
        action='store_true',
        help='Executar em modo CLI (sem interface gráfica)'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Verificar dependências e sair'
    )
    parser.add_argument(
        '--api-only',
        action='store_true',
        help='Iniciar apenas o servidor API'
    )
    parser.add_argument(
        '--no-api',
        action='store_true',
        help='Não iniciar o servidor API'
    )
    
    args = parser.parse_args()
    
    # Imprime banner de boas-vindas
    print_welcome()
    
    # Verifica dependências
    deps_ok = check_dependencies()
    
    if args.check:
        sys.exit(0 if deps_ok else 1)
    
    # Inicializa módulos
    modules_status, essential_ok = initialize_modules()
    
    if not essential_ok:
        print("❌ Não foi possível inicializar os módulos essenciais.")
        print("   Por favor, verifique a instalação das dependências.")
        sys.exit(1)
    
    # Modo API only
    if args.api_only:
        print("\n🌐 Modo API Only")
        api = start_api_server()
        if api:
            print("Pressione Ctrl+C para terminar...")
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 A terminar servidor API...")
                api.stop()
        sys.exit(0)
    
    # Modo CLI
    if args.cli:
        run_cli_mode()
        sys.exit(0)
    
    # Modo GUI (padrão)
    print("🖼️  A iniciar interface gráfica...")
    
    # Inicia API em segundo plano (se não desativado)
    api_server = None
    if not args.no_api:
        api_server = start_api_server()
    
    try:
        # Cria e executa a janela principal
        window = create_main_window()
        
        print("✅ SharkCoders Assistant iniciado com sucesso!")
        print("   Pode agora utilizar a interface gráfica.\n")
        
        # Inicia o loop da GUI
        window.run()
        
    except Exception as e:
        print(f"❌ Erro ao iniciar a interface gráfica: {e}")
        print("   Tente executar em modo CLI: python main.py --cli")
        
        # Tenta modo CLI como fallback
        response = input("\nDeseja executar em modo CLI? (s/n): ").strip().lower()
        if response == 's':
            run_cli_mode()
    
    finally:
        # Para o servidor API se estiver a correr
        if api_server:
            api_server.stop()
        
        print("\n👋 SharkCoders Assistant encerrado. Até à próxima!")


if __name__ == '__main__':
    main()
