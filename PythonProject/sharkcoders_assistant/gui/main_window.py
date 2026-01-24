#!/usr/bin/env python3
"""
SharkCoders Assistant - Janela Principal
Interface gráfica principal da aplicação.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import queue
from pathlib import Path
from typing import Callable, Optional
from PIL import Image, ImageTk

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    APP_NAME, APP_VERSION, 
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    MESSAGES, VOICE_COMMANDS,
)
from .styles import COLORS, FONTS, FONT_NORMAL, FONT_LARGE, FONT_TITLE, FONT_MONO
from .widgets import (
    ModernButton, IconButton, StatusLabel, ScrolledText, 
    LabeledFrame, ModernEntry, ProgressIndicator,
)


class MainWindow:
    """
    Janela principal do SharkCoders Assistant.
    """
    
    def __init__(self):
        """Inicializa a janela principal."""
        # Janela principal
        self.root = tk.Tk()
        self.root.title(f"🦈 {APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.root.configure(bg=COLORS["BACKGROUND"])
        
        # Tentar definir ícone
        try:
            # Usar ícone se existir
            pass
        except:
            pass
        
        # Fila de mensagens para comunicação thread-safe
        self.message_queue = queue.Queue()
        
        # Estado da aplicação
        self.is_listening = False
        self.current_image = None
        self.current_image_path = None
        self.last_ocr_text = ""
        
        # Handlers de comandos
        self.command_handlers = {}
        
        # Criar interface
        self._create_layout()
        self._create_header()
        self._create_main_content()
        self._create_footer()
        
        # Iniciar processamento da fila de mensagens
        self._process_message_queue()
        
        # Mensagem de boas-vindas
        self.log_message(MESSAGES["welcome"], "info")
        self.log_message("✨ Pronto para ajudar!", "success")
    
    def _create_layout(self):
        """Cria o layout base."""
        # Container principal
        self.main_container = tk.Frame(self.root, bg=COLORS["BACKGROUND"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.header_frame = tk.Frame(self.main_container, bg=COLORS["SURFACE"], height=60)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        self.header_frame.pack_propagate(False)
        
        # Content (duas colunas)
        self.content_frame = tk.Frame(self.main_container, bg=COLORS["BACKGROUND"])
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna esquerda (controlos)
        self.left_column = tk.Frame(self.content_frame, bg=COLORS["BACKGROUND"], width=350)
        self.left_column.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.left_column.pack_propagate(False)
        
        # Coluna direita (output)
        self.right_column = tk.Frame(self.content_frame, bg=COLORS["BACKGROUND"])
        self.right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Footer
        self.footer_frame = tk.Frame(self.main_container, bg=COLORS["SURFACE"], height=30)
        self.footer_frame.pack(fill=tk.X, pady=(10, 0))
        self.footer_frame.pack_propagate(False)
    
    def _create_header(self):
        """Cria o header."""
        # Logo/Título
        title_frame = tk.Frame(self.header_frame, bg=COLORS["SURFACE"])
        title_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            title_frame,
            text="🦈",
            font=(FONTS["FAMILY"], 24),
            bg=COLORS["SURFACE"],
            fg=COLORS["PRIMARY"],
        ).pack(side=tk.LEFT)
        
        tk.Label(
            title_frame,
            text=APP_NAME,
            font=FONT_TITLE,
            bg=COLORS["SURFACE"],
            fg=COLORS["TEXT"],
        ).pack(side=tk.LEFT, padx=10)
        
        # Botões de ação rápida (direita do header)
        quick_frame = tk.Frame(self.header_frame, bg=COLORS["SURFACE"])
        quick_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        IconButton(
            quick_frame, 
            icon="❓", 
            tooltip="Ajuda",
            command=self._show_help,
        ).pack(side=tk.LEFT, padx=2)
        
        IconButton(
            quick_frame, 
            icon="⚙️", 
            tooltip="Definições",
            command=self._show_settings,
        ).pack(side=tk.LEFT, padx=2)
    
    def _create_main_content(self):
        """Cria o conteúdo principal."""
        self._create_control_panels()
        self._create_output_area()
    
    def _create_control_panels(self):
        """Cria os painéis de controlo na coluna esquerda."""
        # Secção de Voz
        voice_frame = LabeledFrame(self.left_column, text="🎤 Voz")
        voice_frame.pack(fill=tk.X, pady=5)
        
        voice_btns = tk.Frame(voice_frame, bg=COLORS["SURFACE"])
        voice_btns.pack(fill=tk.X, pady=5)
        
        self.btn_listen = ModernButton(
            voice_btns,
            text="🎤 Ouvir",
            command=self._on_listen,
            style="primary",
        )
        self.btn_listen.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_speak = ModernButton(
            voice_btns,
            text="🔊 Falar",
            command=self._on_speak,
            style="secondary",
        )
        self.btn_speak.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.voice_status = StatusLabel(
            voice_frame,
            text="Pronto",
            status="info",
            bg=COLORS["SURFACE"],
        )
        self.voice_status.pack(pady=5)
        
        # Secção de Captura/OCR
        capture_frame = LabeledFrame(self.left_column, text="📷 Captura / OCR")
        capture_frame.pack(fill=tk.X, pady=5)
        
        capture_btns = tk.Frame(capture_frame, bg=COLORS["SURFACE"])
        capture_btns.pack(fill=tk.X, pady=5)
        
        ModernButton(
            capture_btns,
            text="📸 Capturar Ecrã",
            command=self._on_capture_screen,
            style="primary",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ModernButton(
            capture_btns,
            text="📁 Abrir Imagem",
            command=self._on_open_image,
            style="secondary",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ocr_btns = tk.Frame(capture_frame, bg=COLORS["SURFACE"])
        ocr_btns.pack(fill=tk.X, pady=5)
        
        ModernButton(
            ocr_btns,
            text="🔤 Extrair Texto",
            command=self._on_extract_text,
            style="info",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ModernButton(
            ocr_btns,
            text="🔊 Ler Texto",
            command=self._on_read_text,
            style="secondary",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Secção de Envio
        send_frame = LabeledFrame(self.left_column, text="📤 Envio")
        send_frame.pack(fill=tk.X, pady=5)
        
        # Entry para chat ID
        chat_entry_frame = tk.Frame(send_frame, bg=COLORS["SURFACE"])
        chat_entry_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            chat_entry_frame,
            text="Chat ID:",
            bg=COLORS["SURFACE"],
            fg=COLORS["TEXT"],
            font=FONT_NORMAL,
        ).pack(side=tk.LEFT, padx=5)
        
        self.chat_id_entry = ModernEntry(
            chat_entry_frame,
            placeholder="ID do Telegram",
            width=20,
        )
        self.chat_id_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        send_btns = tk.Frame(send_frame, bg=COLORS["SURFACE"])
        send_btns.pack(fill=tk.X, pady=5)
        
        ModernButton(
            send_btns,
            text="📱 Enviar Imagem",
            command=self._on_send_image,
            style="success",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ModernButton(
            send_btns,
            text="💬 Enviar Texto",
            command=self._on_send_text,
            style="secondary",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Secção de APIs/Sistema
        api_frame = LabeledFrame(self.left_column, text="🌐 APIs / Sistema")
        api_frame.pack(fill=tk.X, pady=5)
        
        api_btns1 = tk.Frame(api_frame, bg=COLORS["SURFACE"])
        api_btns1.pack(fill=tk.X, pady=5)
        
        ModernButton(
            api_btns1,
            text="😂 Piada",
            command=self._on_get_joke,
            style="warning",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ModernButton(
            api_btns1,
            text="💭 Citação",
            command=self._on_get_quote,
            style="warning",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ModernButton(
            api_btns1,
            text="🎲 Facto",
            command=self._on_get_fact,
            style="warning",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        api_btns2 = tk.Frame(api_frame, bg=COLORS["SURFACE"])
        api_btns2.pack(fill=tk.X, pady=5)
        
        ModernButton(
            api_btns2,
            text="💻 Info Sistema",
            command=self._on_system_info,
            style="info",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ModernButton(
            api_btns2,
            text="🪟 Janelas",
            command=self._on_list_windows,
            style="info",
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ModernButton(
            api_btns2,
            text="🕐 Hora",
            command=self._on_tell_time,
            style="info",
        ).pack(side=tk.LEFT, padx=5, pady=5)
    
    def _create_output_area(self):
        """Cria a área de output na coluna direita."""
        # Frame de imagem
        image_frame = LabeledFrame(self.right_column, text="🖼️ Imagem")
        image_frame.pack(fill=tk.X, pady=5)
        
        self.image_label = tk.Label(
            image_frame,
            text="Nenhuma imagem carregada",
            bg=COLORS["SURFACE_DARK"],
            fg=COLORS["TEXT_SECONDARY"],
            font=FONT_NORMAL,
            width=50,
            height=10,
        )
        self.image_label.pack(padx=10, pady=10, fill=tk.X)
        
        # Frame de log
        log_frame = LabeledFrame(self.right_column, text="📋 Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = ScrolledText(log_frame, width=60, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botão de limpar log
        log_btns = tk.Frame(log_frame, bg=COLORS["SURFACE"])
        log_btns.pack(fill=tk.X, pady=5)
        
        ModernButton(
            log_btns,
            text="🗑️ Limpar Log",
            command=self._clear_log,
            style="secondary",
        ).pack(side=tk.RIGHT, padx=5)
        
        ModernButton(
            log_btns,
            text="💾 Guardar Log",
            command=self._save_log,
            style="secondary",
        ).pack(side=tk.RIGHT, padx=5)
    
    def _create_footer(self):
        """Cria o footer."""
        # Status geral
        self.status_label = StatusLabel(
            self.footer_frame,
            text="🟢 Pronto",
            status="success",
            bg=COLORS["SURFACE"],
        )
        self.status_label.pack(side=tk.LEFT, padx=20, pady=5)
        
        # Versão
        tk.Label(
            self.footer_frame,
            text=f"v{APP_VERSION}",
            bg=COLORS["SURFACE"],
            fg=COLORS["TEXT_SECONDARY"],
            font=(FONTS["FAMILY"], 9),
        ).pack(side=tk.RIGHT, padx=20, pady=5)
        
        # API Status
        self.api_status = tk.Label(
            self.footer_frame,
            text="🌐 API: Inactiva",
            bg=COLORS["SURFACE"],
            fg=COLORS["TEXT_SECONDARY"],
            font=(FONTS["FAMILY"], 9),
        )
        self.api_status.pack(side=tk.RIGHT, padx=20, pady=5)
    
    # =========================================================================
    # MÉTODOS DE AÇÃO
    # =========================================================================
    
    def _on_listen(self):
        """Inicia o reconhecimento de voz."""
        self.voice_status.set_info("A ouvir...")
        self.log_message(MESSAGES["listening"], "info")
        self._run_in_thread(self._listen_voice)
    
    def _listen_voice(self):
        """Executa reconhecimento de voz em thread."""
        try:
            from voice import speech_recognizer, voice_processor
            
            text = speech_recognizer.listen_once()
            if text:
                self._queue_message(f"🎤 Ouvido: {text}", "success")
                # Processar comando
                result = voice_processor.process(text)
                if result:
                    self._queue_message(f"✅ Comando executado: {result}", "success")
            else:
                self._queue_message(MESSAGES["not_understood"], "warning")
        except ImportError:
            self._queue_message("⚠️ Módulo de voz não disponível. Instale: pip install SpeechRecognition PyAudio", "warning")
        except Exception as e:
            self._queue_message(f"❌ Erro no reconhecimento: {e}", "error")
        finally:
            self._queue_status_update("Pronto", "info")
    
    def _on_speak(self):
        """Abre diálogo para texto a falar."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Falar")
        dialog.geometry("400x150")
        dialog.configure(bg=COLORS["BACKGROUND"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Texto para falar:",
            bg=COLORS["BACKGROUND"],
            fg=COLORS["TEXT"],
            font=FONT_NORMAL,
        ).pack(pady=10)
        
        entry = ModernEntry(dialog, placeholder="Escreve o texto aqui...", width=40)
        entry.pack(pady=10, padx=20, fill=tk.X)
        
        def speak():
            text = entry.get()
            if text:
                self._run_in_thread(lambda: self._speak_text(text))
                dialog.destroy()
        
        ModernButton(dialog, text="🔊 Falar", command=speak).pack(pady=10)
    
    def _speak_text(self, text: str):
        """Fala o texto usando TTS."""
        try:
            from voice import text_to_speech
            text_to_speech.speak(text)
            self._queue_message(f"🔊 Falado: {text}", "success")
        except ImportError:
            self._queue_message("⚠️ Módulo TTS não disponível. Instale: pip install pyttsx3", "warning")
        except Exception as e:
            self._queue_message(f"❌ Erro ao falar: {e}", "error")
    
    def _on_capture_screen(self):
        """Captura o ecrã."""
        self.log_message(MESSAGES["screenshot"], "info")
        self._run_in_thread(self._capture_screen)
    
    def _capture_screen(self):
        """Executa captura de ecrã em thread."""
        try:
            from automation import screen_capture
            
            # Minimizar janela antes de capturar
            self.root.iconify()
            import time
            time.sleep(0.5)
            
            image, path = screen_capture.capture_full_screen()
            
            # Restaurar janela
            self.root.deiconify()
            
            if image and path:
                self.current_image = image
                self.current_image_path = path
                self._queue_message(f"📸 Captura guardada: {path}", "success")
                self._queue_image_update(image)
            else:
                self._queue_message("❌ Falha ao capturar ecrã", "error")
        except ImportError:
            self.root.deiconify()
            self._queue_message("⚠️ Módulo de captura não disponível. Instale: pip install PyAutoGUI Pillow", "warning")
        except Exception as e:
            self.root.deiconify()
            self._queue_message(f"❌ Erro na captura: {e}", "error")
    
    def _on_open_image(self):
        """Abre uma imagem do sistema de ficheiros."""
        filetypes = [
            ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("Todos", "*.*"),
        ]
        filepath = filedialog.askopenfilename(
            title="Abrir Imagem",
            filetypes=filetypes,
        )
        
        if filepath:
            try:
                image = Image.open(filepath)
                self.current_image = image
                self.current_image_path = filepath
                self._update_image_display(image)
                self.log_message(f"📁 Imagem carregada: {filepath}", "success")
            except Exception as e:
                self.log_message(f"❌ Erro ao abrir imagem: {e}", "error")
    
    def _on_extract_text(self):
        """Extrai texto da imagem actual."""
        if not self.current_image:
            self.log_message("⚠️ Nenhuma imagem carregada", "warning")
            return
        
        self.log_message(MESSAGES["ocr"], "info")
        self._run_in_thread(self._extract_text)
    
    def _extract_text(self):
        """Executa OCR em thread."""
        try:
            from vision import ocr_engine, image_processor
            
            # Pré-processar imagem
            processed = image_processor.prepare_for_ocr(self.current_image)
            
            # Extrair texto
            text = ocr_engine.extract_text(processed)
            
            if text.strip():
                self.last_ocr_text = text
                self._queue_message(f"📝 Texto extraído:\n{text}", "success")
            else:
                self._queue_message("⚠️ Nenhum texto encontrado na imagem", "warning")
        except ImportError:
            self._queue_message("⚠️ Módulo OCR não disponível. Instale: pip install pytesseract opencv-python", "warning")
        except Exception as e:
            self._queue_message(f"❌ Erro no OCR: {e}", "error")
    
    def _on_read_text(self):
        """Lê o texto extraído em voz alta."""
        if not self.last_ocr_text:
            self.log_message("⚠️ Nenhum texto para ler. Extrai primeiro.", "warning")
            return
        
        self._run_in_thread(lambda: self._speak_text(self.last_ocr_text))
    
    def _on_send_image(self):
        """Envia imagem via Telegram."""
        if not self.current_image_path:
            self.log_message("⚠️ Nenhuma imagem para enviar", "warning")
            return
        
        chat_id = self.chat_id_entry.get()
        if not chat_id:
            self.log_message("⚠️ Introduz o Chat ID do Telegram", "warning")
            return
        
        self.log_message(MESSAGES["telegram"], "info")
        self._run_in_thread(lambda: self._send_telegram_image(chat_id))
    
    def _send_telegram_image(self, chat_id: str):
        """Envia imagem para Telegram em thread."""
        try:
            from communication import telegram_sender
            
            caption = self.last_ocr_text[:200] if self.last_ocr_text else "📸 Captura do SharkCoders Assistant"
            success, message = telegram_sender.send_image(
                chat_id, 
                self.current_image_path,
                caption=caption,
            )
            
            if success:
                self._queue_message(f"📤 Imagem enviada com sucesso!", "success")
            else:
                self._queue_message(f"❌ Erro ao enviar: {message}", "error")
        except ImportError:
            self._queue_message("⚠️ Módulo Telegram não disponível. Instale: pip install requests", "warning")
        except Exception as e:
            self._queue_message(f"❌ Erro no envio: {e}", "error")
    
    def _on_send_text(self):
        """Envia texto via Telegram."""
        if not self.last_ocr_text:
            self.log_message("⚠️ Nenhum texto para enviar", "warning")
            return
        
        chat_id = self.chat_id_entry.get()
        if not chat_id:
            self.log_message("⚠️ Introduz o Chat ID do Telegram", "warning")
            return
        
        self._run_in_thread(lambda: self._send_telegram_text(chat_id))
    
    def _send_telegram_text(self, chat_id: str):
        """Envia texto para Telegram em thread."""
        try:
            from communication import telegram_sender
            
            success, message = telegram_sender.send_message(chat_id, self.last_ocr_text)
            
            if success:
                self._queue_message(f"📤 Texto enviado com sucesso!", "success")
            else:
                self._queue_message(f"❌ Erro ao enviar: {message}", "error")
        except Exception as e:
            self._queue_message(f"❌ Erro no envio: {e}", "error")
    
    def _on_get_joke(self):
        """Obtém uma piada."""
        self._run_in_thread(self._fetch_joke)
    
    def _fetch_joke(self):
        """Obtém piada em thread."""
        try:
            from communication import external_apis
            
            joke = external_apis.get_joke()
            self._queue_message(f"😂 Piada:\n{joke}", "info")
            self._run_in_thread(lambda: self._speak_text(joke))
        except Exception as e:
            self._queue_message(f"❌ Erro ao obter piada: {e}", "error")
    
    def _on_get_quote(self):
        """Obtém uma citação."""
        self._run_in_thread(self._fetch_quote)
    
    def _fetch_quote(self):
        """Obtém citação em thread."""
        try:
            from communication import external_apis
            
            quote = external_apis.get_quote()
            self._queue_message(f"💭 Citação:\n{quote}", "info")
        except Exception as e:
            self._queue_message(f"❌ Erro ao obter citação: {e}", "error")
    
    def _on_get_fact(self):
        """Obtém um facto."""
        self._run_in_thread(self._fetch_fact)
    
    def _fetch_fact(self):
        """Obtém facto em thread."""
        try:
            from communication import external_apis
            
            fact = external_apis.get_fact()
            self._queue_message(f"🎲 Facto:\n{fact}", "info")
        except Exception as e:
            self._queue_message(f"❌ Erro ao obter facto: {e}", "error")
    
    def _on_system_info(self):
        """Mostra informação do sistema."""
        try:
            from system import os_interaction
            
            info = os_interaction.get_system_info()
            formatted = "\n".join([f"  {k}: {v}" for k, v in info.items()])
            self.log_message(f"💻 Informação do Sistema:\n{formatted}", "info")
        except Exception as e:
            self.log_message(f"❌ Erro ao obter info: {e}", "error")
    
    def _on_list_windows(self):
        """Lista janelas abertas."""
        try:
            from automation import window_manager
            
            windows = window_manager.get_all_windows()
            if windows:
                formatted = "\n".join([f"  • {w}" for w in windows[:10]])
                self.log_message(f"🪟 Janelas abertas:\n{formatted}", "info")
            else:
                self.log_message("⚠️ Não foi possível listar janelas", "warning")
        except Exception as e:
            self.log_message(f"❌ Erro ao listar janelas: {e}", "error")
    
    def _on_tell_time(self):
        """Diz a hora actual."""
        try:
            from system import os_interaction
            
            time_info = os_interaction.get_datetime_info()
            message = f"🕐 {time_info['time']} - {time_info['date']}"
            self.log_message(message, "info")
            self._run_in_thread(lambda: self._speak_text(f"São {time_info['time']}"))
        except Exception as e:
            self.log_message(f"❌ Erro: {e}", "error")
    
    def _show_help(self):
        """Mostra janela de ajuda."""
        help_window = tk.Toplevel(self.root)
        help_window.title("Ajuda - SharkCoders Assistant")
        help_window.geometry("500x400")
        help_window.configure(bg=COLORS["BACKGROUND"])
        
        tk.Label(
            help_window,
            text="🦈 Comandos de Voz Disponíveis",
            font=FONT_TITLE,
            bg=COLORS["BACKGROUND"],
            fg=COLORS["PRIMARY"],
        ).pack(pady=20)
        
        help_text = ScrolledText(help_window, width=50, height=15)
        help_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        commands_text = "\n".join([f"• \"{cmd}\" → {action}" for cmd, action in VOICE_COMMANDS.items()])
        help_text.set_text(commands_text)
        
        ModernButton(
            help_window,
            text="Fechar",
            command=help_window.destroy,
        ).pack(pady=10)
    
    def _show_settings(self):
        """Mostra janela de definições."""
        messagebox.showinfo("Definições", "⚙️ Definições em desenvolvimento...")
    
    def _clear_log(self):
        """Limpa o log."""
        self.log_text.clear()
    
    def _save_log(self):
        """Guarda o log num ficheiro."""
        filepath = filedialog.asksaveasfilename(
            title="Guardar Log",
            defaultextension=".txt",
            filetypes=[("Ficheiro de Texto", "*.txt")],
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get("1.0", tk.END))
                self.log_message(f"💾 Log guardado: {filepath}", "success")
            except Exception as e:
                self.log_message(f"❌ Erro ao guardar: {e}", "error")
    
    # =========================================================================
    # MÉTODOS DE UTILIDADE
    # =========================================================================
    
    def log_message(self, message: str, status: str = "info"):
        """
        Adiciona mensagem ao log.
        
        Args:
            message: Mensagem a adicionar
            status: Tipo de mensagem ('info', 'success', 'warning', 'error')
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        self.log_text.append(formatted)
    
    def _update_image_display(self, image: Image.Image):
        """Actualiza a exibição da imagem."""
        # Redimensionar para caber no label
        max_size = (400, 200)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo  # Manter referência
    
    def _run_in_thread(self, func: Callable):
        """Executa função em thread separada."""
        thread = threading.Thread(target=func, daemon=True)
        thread.start()
    
    def _queue_message(self, message: str, status: str = "info"):
        """Adiciona mensagem à fila (thread-safe)."""
        self.message_queue.put(("message", message, status))
    
    def _queue_status_update(self, text: str, status: str):
        """Adiciona actualização de status à fila."""
        self.message_queue.put(("status", text, status))
    
    def _queue_image_update(self, image: Image.Image):
        """Adiciona actualização de imagem à fila."""
        self.message_queue.put(("image", image, None))
    
    def _process_message_queue(self):
        """Processa mensagens da fila periodicamente."""
        try:
            while True:
                msg_type, data, extra = self.message_queue.get_nowait()
                
                if msg_type == "message":
                    self.log_message(data, extra)
                elif msg_type == "status":
                    self.voice_status.set_status(extra, data)
                elif msg_type == "image":
                    self._update_image_display(data)
        except queue.Empty:
            pass
        
        # Agendar próxima verificação
        self.root.after(100, self._process_message_queue)
    
    def register_command_handler(self, command: str, handler: Callable):
        """Regista um handler para um comando."""
        self.command_handlers[command] = handler
    
    def run(self):
        """Inicia a aplicação."""
        # Tentar iniciar a API em background
        try:
            from api import assistant_api
            assistant_api.start(threaded=True)
            self.api_status.config(text="🌐 API: http://localhost:5000")
        except Exception as e:
            print(f"API não iniciada: {e}")
        
        # Iniciar loop principal
        self.root.mainloop()


def create_main_window() -> MainWindow:
    """
    Cria e retorna a janela principal.
    
    Returns:
        Instância de MainWindow
    """
    return MainWindow()


if __name__ == "__main__":
    # Teste da janela principal
    app = create_main_window()
    app.run()
