#!/usr/bin/env python3
"""
SharkCoders Assistant - Widgets Personalizados
Widgets customizados para a interface gráfica.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from .styles import (
    COLORS, FONTS, STYLES, DIMENSIONS,
    FONT_NORMAL, FONT_SMALL, FONT_LARGE, FONT_MONO,
    get_status_color,
)


class ModernButton(tk.Button):
    """
    Botão moderno com efeitos de hover.
    """
    
    def __init__(self, master, text: str = "", command: Callable = None,
                 style: str = "primary", **kwargs):
        """
        Inicializa o botão moderno.
        
        Args:
            master: Widget pai
            text: Texto do botão
            command: Função a executar no clique
            style: Estilo ('primary', 'secondary', 'success', 'danger')
            **kwargs: Argumentos adicionais para tk.Button
        """
        # Cores baseadas no estilo
        self.style = style
        self.colors = self._get_style_colors(style)
        
        # Configurações padrão
        config = {
            "text": text,
            "command": command,
            "bg": self.colors["bg"],
            "fg": self.colors["fg"],
            "activebackground": self.colors["hover"],
            "activeforeground": self.colors["fg"],
            "font": FONT_NORMAL,
            "relief": "flat",
            "cursor": "hand2",
            "padx": 15,
            "pady": 8,
            "bd": 0,
        }
        config.update(kwargs)
        
        super().__init__(master, **config)
        
        # Bind de eventos de hover
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _get_style_colors(self, style: str) -> dict:
        """Retorna cores baseadas no estilo."""
        styles = {
            "primary": {
                "bg": COLORS["PRIMARY"],
                "fg": COLORS["TEXT"],
                "hover": COLORS["BUTTON_HOVER"],
            },
            "secondary": {
                "bg": COLORS["SURFACE_LIGHT"],
                "fg": COLORS["TEXT"],
                "hover": COLORS["SURFACE"],
            },
            "success": {
                "bg": COLORS["SUCCESS"],
                "fg": COLORS["TEXT"],
                "hover": "#66BB6A",
            },
            "danger": {
                "bg": COLORS["ERROR"],
                "fg": COLORS["TEXT"],
                "hover": "#EF5350",
            },
            "warning": {
                "bg": COLORS["WARNING"],
                "fg": COLORS["BACKGROUND"],
                "hover": "#FFCA28",
            },
            "info": {
                "bg": COLORS["INFO"],
                "fg": COLORS["TEXT"],
                "hover": "#42A5F5",
            },
        }
        return styles.get(style, styles["primary"])
    
    def _on_enter(self, event):
        """Efeito ao entrar com o rato."""
        self.config(bg=self.colors["hover"])
    
    def _on_leave(self, event):
        """Efeito ao sair com o rato."""
        self.config(bg=self.colors["bg"])


class IconButton(tk.Button):
    """
    Botão com emoji/ícone.
    """
    
    def __init__(self, master, icon: str = "⚙️", command: Callable = None,
                 tooltip: str = "", size: int = 16, **kwargs):
        """
        Inicializa o botão de ícone.
        
        Args:
            master: Widget pai
            icon: Emoji ou texto do ícone
            command: Função a executar no clique
            tooltip: Texto de dica
            size: Tamanho da fonte do ícone
            **kwargs: Argumentos adicionais
        """
        config = {
            "text": icon,
            "command": command,
            "bg": COLORS["SURFACE"],
            "fg": COLORS["TEXT"],
            "activebackground": COLORS["PRIMARY"],
            "activeforeground": COLORS["TEXT"],
            "font": (FONTS["FAMILY"], size),
            "relief": "flat",
            "cursor": "hand2",
            "width": 3,
            "height": 1,
            "bd": 0,
        }
        config.update(kwargs)
        
        super().__init__(master, **config)
        
        self.tooltip_text = tooltip
        self._tooltip = None
        
        # Efeitos de hover
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        """Efeito ao entrar com o rato."""
        self.config(bg=COLORS["PRIMARY"])
        self._show_tooltip()
    
    def _on_leave(self, event):
        """Efeito ao sair com o rato."""
        self.config(bg=COLORS["SURFACE"])
        self._hide_tooltip()
    
    def _show_tooltip(self):
        """Mostra tooltip."""
        if self.tooltip_text and not self._tooltip:
            x = self.winfo_rootx() + self.winfo_width() // 2
            y = self.winfo_rooty() + self.winfo_height() + 5
            
            self._tooltip = tk.Toplevel(self)
            self._tooltip.wm_overrideredirect(True)
            self._tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(
                self._tooltip,
                text=self.tooltip_text,
                bg=COLORS["SURFACE_LIGHT"],
                fg=COLORS["TEXT"],
                font=FONT_SMALL,
                padx=5,
                pady=2,
            )
            label.pack()
    
    def _hide_tooltip(self):
        """Esconde tooltip."""
        if self._tooltip:
            self._tooltip.destroy()
            self._tooltip = None


class StatusLabel(tk.Label):
    """
    Label com cores dinâmicas baseadas no estado.
    """
    
    def __init__(self, master, text: str = "", status: str = "normal", **kwargs):
        """
        Inicializa o label de estado.
        
        Args:
            master: Widget pai
            text: Texto inicial
            status: Estado inicial ('success', 'error', 'warning', 'info', 'normal')
            **kwargs: Argumentos adicionais
        """
        config = {
            "text": text,
            "bg": COLORS["BACKGROUND"],
            "fg": get_status_color(status),
            "font": FONT_NORMAL,
        }
        config.update(kwargs)
        
        super().__init__(master, **config)
        self._status = status
    
    def set_status(self, status: str, text: Optional[str] = None):
        """
        Actualiza o estado e opcionalmente o texto.
        
        Args:
            status: Novo estado
            text: Novo texto (opcional)
        """
        self._status = status
        self.config(fg=get_status_color(status))
        if text is not None:
            self.config(text=text)
    
    def set_success(self, text: str = None):
        """Define estado de sucesso."""
        self.set_status("success", text)
    
    def set_error(self, text: str = None):
        """Define estado de erro."""
        self.set_status("error", text)
    
    def set_warning(self, text: str = None):
        """Define estado de aviso."""
        self.set_status("warning", text)
    
    def set_info(self, text: str = None):
        """Define estado de informação."""
        self.set_status("info", text)


class ScrolledText(tk.Frame):
    """
    Área de texto com scrollbar integrada.
    """
    
    def __init__(self, master, width: int = 60, height: int = 10, **kwargs):
        """
        Inicializa a área de texto com scroll.
        
        Args:
            master: Widget pai
            width: Largura em caracteres
            height: Altura em linhas
            **kwargs: Argumentos adicionais para o Text
        """
        super().__init__(master, bg=COLORS["BACKGROUND"])
        
        # Área de texto
        text_config = {
            "width": width,
            "height": height,
            "bg": COLORS["SURFACE_DARK"],
            "fg": COLORS["TEXT"],
            "insertbackground": COLORS["TEXT"],
            "font": FONT_MONO,
            "relief": "flat",
            "highlightbackground": COLORS["BORDER"],
            "highlightcolor": COLORS["PRIMARY"],
            "highlightthickness": 1,
            "padx": 10,
            "pady": 10,
            "wrap": tk.WORD,
        }
        text_config.update(kwargs)
        
        self.text = tk.Text(self, **text_config)
        
        # Scrollbar
        self.scrollbar = tk.Scrollbar(
            self,
            command=self.text.yview,
            bg=COLORS["SURFACE"],
            troughcolor=COLORS["BACKGROUND"],
            activebackground=COLORS["PRIMARY"],
            highlightthickness=0,
            bd=0,
        )
        self.text.config(yscrollcommand=self.scrollbar.set)
        
        # Layout
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def insert(self, index, text: str, *tags):
        """Insere texto."""
        self.text.insert(index, text, *tags)
    
    def delete(self, start, end=None):
        """Remove texto."""
        self.text.delete(start, end)
    
    def get(self, start, end=None) -> str:
        """Obtém texto."""
        return self.text.get(start, end)
    
    def clear(self):
        """Limpa todo o texto."""
        self.text.delete("1.0", tk.END)
    
    def append(self, text: str, newline: bool = True):
        """
        Adiciona texto no final.
        
        Args:
            text: Texto a adicionar
            newline: Se deve adicionar nova linha antes
        """
        if newline and self.get("1.0", tk.END).strip():
            self.text.insert(tk.END, "\n")
        self.text.insert(tk.END, text)
        self.text.see(tk.END)
    
    def set_text(self, text: str):
        """Define todo o texto."""
        self.clear()
        self.text.insert("1.0", text)
    
    def config_text(self, **kwargs):
        """Configura o widget de texto."""
        self.text.config(**kwargs)


class LabeledFrame(tk.LabelFrame):
    """
    Frame com título estilizado.
    """
    
    def __init__(self, master, text: str = "", **kwargs):
        """
        Inicializa o frame com título.
        
        Args:
            master: Widget pai
            text: Título do frame
            **kwargs: Argumentos adicionais
        """
        config = {
            "text": f" {text} ",
            "bg": COLORS["SURFACE"],
            "fg": COLORS["PRIMARY"],
            "font": FONT_LARGE,
            "labelanchor": "nw",
            "padx": 10,
            "pady": 10,
        }
        config.update(kwargs)
        
        super().__init__(master, **config)


class ModernEntry(tk.Frame):
    """
    Entry moderno com placeholder.
    """
    
    def __init__(self, master, placeholder: str = "", width: int = 30, **kwargs):
        """
        Inicializa o entry moderno.
        
        Args:
            master: Widget pai
            placeholder: Texto de placeholder
            width: Largura em caracteres
            **kwargs: Argumentos adicionais
        """
        super().__init__(master, bg=COLORS["BACKGROUND"])
        
        self.placeholder = placeholder
        self._has_placeholder = False
        
        # Entry
        entry_config = {
            "width": width,
            "bg": COLORS["SURFACE"],
            "fg": COLORS["TEXT"],
            "insertbackground": COLORS["TEXT"],
            "font": FONT_NORMAL,
            "relief": "flat",
            "highlightbackground": COLORS["BORDER"],
            "highlightcolor": COLORS["PRIMARY"],
            "highlightthickness": 1,
        }
        entry_config.update(kwargs)
        
        self.entry = tk.Entry(self, **entry_config)
        self.entry.pack(fill=tk.X, padx=2, pady=2)
        
        # Eventos para placeholder
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        
        # Mostrar placeholder inicial
        self._show_placeholder()
    
    def _show_placeholder(self):
        """Mostra o placeholder."""
        if self.placeholder and not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=COLORS["TEXT_MUTED"])
            self._has_placeholder = True
    
    def _hide_placeholder(self):
        """Esconde o placeholder."""
        if self._has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=COLORS["TEXT"])
            self._has_placeholder = False
    
    def _on_focus_in(self, event):
        """Evento ao ganhar foco."""
        self._hide_placeholder()
    
    def _on_focus_out(self, event):
        """Evento ao perder foco."""
        if not self.entry.get():
            self._show_placeholder()
    
    def get(self) -> str:
        """Obtém o valor (excluindo placeholder)."""
        if self._has_placeholder:
            return ""
        return self.entry.get()
    
    def set(self, value: str):
        """Define o valor."""
        self._hide_placeholder()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def clear(self):
        """Limpa o entry."""
        self.entry.delete(0, tk.END)
        self._show_placeholder()


class ProgressIndicator(tk.Frame):
    """
    Indicador de progresso/loading.
    """
    
    def __init__(self, master, size: int = 100, **kwargs):
        """
        Inicializa o indicador.
        
        Args:
            master: Widget pai
            size: Tamanho em pixels
        """
        super().__init__(master, bg=COLORS["BACKGROUND"], **kwargs)
        
        self.label = tk.Label(
            self,
            text="⏳",
            font=(FONTS["FAMILY"], size // 4),
            bg=COLORS["BACKGROUND"],
            fg=COLORS["PRIMARY"],
        )
        self.label.pack(expand=True)
        
        self._running = False
        self._symbols = ["⏳", "⌛"]
        self._index = 0
    
    def start(self):
        """Inicia a animação."""
        self._running = True
        self._animate()
    
    def stop(self):
        """Para a animação."""
        self._running = False
    
    def _animate(self):
        """Actualiza a animação."""
        if self._running:
            self._index = (self._index + 1) % len(self._symbols)
            self.label.config(text=self._symbols[self._index])
            self.after(500, self._animate)


if __name__ == "__main__":
    # Teste dos widgets
    root = tk.Tk()
    root.title("Teste de Widgets SharkCoders")
    root.geometry("600x500")
    root.configure(bg=COLORS["BACKGROUND"])
    
    # Frame principal
    main_frame = tk.Frame(root, bg=COLORS["BACKGROUND"], padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    tk.Label(
        main_frame,
        text="🦈 Widgets SharkCoders",
        bg=COLORS["BACKGROUND"],
        fg=COLORS["PRIMARY"],
        font=(FONTS["FAMILY"], 18, "bold"),
    ).pack(pady=10)
    
    # Botões
    btn_frame = tk.Frame(main_frame, bg=COLORS["BACKGROUND"])
    btn_frame.pack(pady=10)
    
    ModernButton(btn_frame, text="Primary", style="primary").pack(side=tk.LEFT, padx=5)
    ModernButton(btn_frame, text="Secondary", style="secondary").pack(side=tk.LEFT, padx=5)
    ModernButton(btn_frame, text="Success", style="success").pack(side=tk.LEFT, padx=5)
    ModernButton(btn_frame, text="Danger", style="danger").pack(side=tk.LEFT, padx=5)
    
    # Botões de ícone
    icon_frame = tk.Frame(main_frame, bg=COLORS["BACKGROUND"])
    icon_frame.pack(pady=10)
    
    IconButton(icon_frame, icon="🎤", tooltip="Microfone").pack(side=tk.LEFT, padx=5)
    IconButton(icon_frame, icon="📷", tooltip="Câmara").pack(side=tk.LEFT, padx=5)
    IconButton(icon_frame, icon="📤", tooltip="Enviar").pack(side=tk.LEFT, padx=5)
    IconButton(icon_frame, icon="⚙️", tooltip="Definições").pack(side=tk.LEFT, padx=5)
    
    # Status label
    status = StatusLabel(main_frame, text="Estado: Pronto")
    status.pack(pady=10)
    
    # Entry com placeholder
    entry = ModernEntry(main_frame, placeholder="Escreve aqui...", width=40)
    entry.pack(pady=10)
    
    # Labeled frame com texto
    lf = LabeledFrame(main_frame, text="Área de Texto")
    lf.pack(pady=10, fill=tk.X)
    
    scroll_text = ScrolledText(lf, width=50, height=5)
    scroll_text.pack(padx=5, pady=5)
    scroll_text.append("🦈 Bem-vindo ao SharkCoders Assistant!")
    scroll_text.append("Este é um teste dos widgets personalizados.")
    
    root.mainloop()
