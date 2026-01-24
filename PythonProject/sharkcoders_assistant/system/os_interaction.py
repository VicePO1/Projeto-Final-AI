# -*- coding: utf-8 -*-
"""
SharkCoders Assistant - OS Interaction
Funções de interação com o sistema operativo
"""

import os
import sys
import platform
import subprocess
import webbrowser
import shutil
from datetime import datetime
from typing import Dict, Any, Optional, Tuple


class OSInteraction:
    """Classe para interação com o sistema operativo"""
    
    def __init__(self):
        """Inicializa a classe de interação com o SO"""
        self.system = platform.system()
        self.is_windows = self.system == 'Windows'
        self.is_linux = self.system == 'Linux'
        self.is_mac = self.system == 'Darwin'
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Obtém informações completas do sistema
        
        Returns:
            Dict com informações do sistema
        """
        info = {
            'sistema': platform.system(),
            'versao_sistema': platform.version(),
            'release': platform.release(),
            'maquina': platform.machine(),
            'processador': platform.processor(),
            'arquitetura': platform.architecture()[0],
            'hostname': platform.node(),
            'python_versao': platform.python_version(),
            'python_implementacao': platform.python_implementation(),
            'usuario': self.get_username(),
            'diretorio_atual': os.getcwd(),
            'diretorio_home': os.path.expanduser('~'),
        }
        
        # Adiciona informações de memória se disponível
        try:
            import psutil
            mem = psutil.virtual_memory()
            info['memoria_total_gb'] = round(mem.total / (1024**3), 2)
            info['memoria_disponivel_gb'] = round(mem.available / (1024**3), 2)
            info['memoria_usada_percent'] = mem.percent
            
            cpu = psutil.cpu_percent(interval=0.1)
            info['cpu_uso_percent'] = cpu
            info['cpu_cores_fisicos'] = psutil.cpu_count(logical=False)
            info['cpu_cores_logicos'] = psutil.cpu_count(logical=True)
        except ImportError:
            pass
        
        return info
    
    def get_username(self) -> str:
        """
        Obtém o nome do utilizador atual
        
        Returns:
            Nome do utilizador
        """
        try:
            return os.getlogin()
        except OSError:
            # Fallback para ambientes sem terminal
            return os.environ.get('USERNAME', os.environ.get('USER', 'Utilizador'))
    
    def get_current_time(self) -> str:
        """
        Obtém a hora atual formatada
        
        Returns:
            Hora atual no formato HH:MM:SS
        """
        return datetime.now().strftime('%H:%M:%S')
    
    def get_current_date(self) -> str:
        """
        Obtém a data atual formatada
        
        Returns:
            Data atual no formato DD/MM/YYYY
        """
        return datetime.now().strftime('%d/%m/%Y')
    
    def get_datetime_info(self) -> Dict[str, Any]:
        """
        Obtém informações completas de data e hora
        
        Returns:
            Dict com informações de data/hora
        """
        now = datetime.now()
        
        dias_semana = [
            'Segunda-feira', 'Terça-feira', 'Quarta-feira',
            'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'
        ]
        
        meses = [
            '', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        
        return {
            'data': now.strftime('%d/%m/%Y'),
            'hora': now.strftime('%H:%M:%S'),
            'dia_semana': dias_semana[now.weekday()],
            'dia': now.day,
            'mes': now.month,
            'mes_nome': meses[now.month],
            'ano': now.year,
            'hora_int': now.hour,
            'minuto': now.minute,
            'segundo': now.second,
            'timestamp': now.timestamp(),
            'iso_format': now.isoformat(),
        }
    
    def get_disk_usage(self, path: str = '/') -> Dict[str, Any]:
        """
        Obtém informações de uso do disco
        
        Args:
            path: Caminho para verificar (default: raiz)
            
        Returns:
            Dict com informações do disco
        """
        if self.is_windows:
            path = 'C:\\'
        
        try:
            usage = shutil.disk_usage(path)
            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            free_gb = usage.free / (1024**3)
            percent_used = (usage.used / usage.total) * 100
            
            return {
                'caminho': path,
                'total_gb': round(total_gb, 2),
                'usado_gb': round(used_gb, 2),
                'livre_gb': round(free_gb, 2),
                'percentagem_usado': round(percent_used, 2),
                'total_bytes': usage.total,
                'usado_bytes': usage.used,
                'livre_bytes': usage.free,
            }
        except Exception as e:
            return {'erro': str(e)}
    
    def open_file(self, filepath: str) -> Tuple[bool, str]:
        """
        Abre um ficheiro com a aplicação padrão do sistema
        
        Args:
            filepath: Caminho do ficheiro a abrir
            
        Returns:
            Tuple (sucesso, mensagem)
        """
        if not os.path.exists(filepath):
            return False, f"Ficheiro não encontrado: {filepath}"
        
        try:
            if self.is_windows:
                os.startfile(filepath)
            elif self.is_mac:
                subprocess.run(['open', filepath], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', filepath], check=True)
            
            return True, f"Ficheiro aberto: {filepath}"
        except Exception as e:
            return False, f"Erro ao abrir ficheiro: {e}"
    
    def open_url(self, url: str) -> Tuple[bool, str]:
        """
        Abre uma URL no browser padrão
        
        Args:
            url: URL a abrir
            
        Returns:
            Tuple (sucesso, mensagem)
        """
        try:
            # Adiciona https:// se não tiver protocolo
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            return True, f"URL aberta: {url}"
        except Exception as e:
            return False, f"Erro ao abrir URL: {e}"
    
    def run_command(self, command: str, capture_output: bool = True,
                    timeout: int = 30) -> Dict[str, Any]:
        """
        Executa um comando no terminal
        
        Args:
            command: Comando a executar
            capture_output: Se deve capturar a saída
            timeout: Tempo limite em segundos
            
        Returns:
            Dict com resultado da execução
        """
        try:
            if self.is_windows:
                # No Windows, usa shell=True para comandos internos
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=capture_output,
                    text=True,
                    timeout=timeout
                )
            else:
                # No Linux/Mac, divide o comando
                result = subprocess.run(
                    command.split(),
                    capture_output=capture_output,
                    text=True,
                    timeout=timeout
                )
            
            return {
                'sucesso': result.returncode == 0,
                'codigo_retorno': result.returncode,
                'stdout': result.stdout if capture_output else None,
                'stderr': result.stderr if capture_output else None,
                'comando': command,
            }
        except subprocess.TimeoutExpired:
            return {
                'sucesso': False,
                'erro': f'Timeout após {timeout} segundos',
                'comando': command,
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e),
                'comando': command,
            }
    
    def list_directory(self, path: str = '.') -> Dict[str, Any]:
        """
        Lista o conteúdo de um diretório
        
        Args:
            path: Caminho do diretório
            
        Returns:
            Dict com lista de ficheiros e pastas
        """
        try:
            path = os.path.abspath(path)
            
            if not os.path.exists(path):
                return {'erro': f'Diretório não encontrado: {path}'}
            
            if not os.path.isdir(path):
                return {'erro': f'Não é um diretório: {path}'}
            
            items = os.listdir(path)
            ficheiros = []
            pastas = []
            
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    pastas.append(item)
                else:
                    ficheiros.append(item)
            
            return {
                'caminho': path,
                'total_items': len(items),
                'total_ficheiros': len(ficheiros),
                'total_pastas': len(pastas),
                'ficheiros': sorted(ficheiros),
                'pastas': sorted(pastas),
            }
        except Exception as e:
            return {'erro': str(e)}
    
    def get_environment_variable(self, name: str) -> Optional[str]:
        """
        Obtém o valor de uma variável de ambiente
        
        Args:
            name: Nome da variável
            
        Returns:
            Valor da variável ou None
        """
        return os.environ.get(name)
    
    def get_all_environment_variables(self) -> Dict[str, str]:
        """
        Obtém todas as variáveis de ambiente
        
        Returns:
            Dict com todas as variáveis
        """
        return dict(os.environ)
    
    def create_directory(self, path: str) -> Tuple[bool, str]:
        """
        Cria um diretório
        
        Args:
            path: Caminho do diretório a criar
            
        Returns:
            Tuple (sucesso, mensagem)
        """
        try:
            os.makedirs(path, exist_ok=True)
            return True, f"Diretório criado: {path}"
        except Exception as e:
            return False, f"Erro ao criar diretório: {e}"
    
    def delete_file(self, filepath: str) -> Tuple[bool, str]:
        """
        Elimina um ficheiro
        
        Args:
            filepath: Caminho do ficheiro
            
        Returns:
            Tuple (sucesso, mensagem)
        """
        try:
            if not os.path.exists(filepath):
                return False, f"Ficheiro não encontrado: {filepath}"
            
            os.remove(filepath)
            return True, f"Ficheiro eliminado: {filepath}"
        except Exception as e:
            return False, f"Erro ao eliminar ficheiro: {e}"
    
    def copy_file(self, source: str, destination: str) -> Tuple[bool, str]:
        """
        Copia um ficheiro
        
        Args:
            source: Caminho de origem
            destination: Caminho de destino
            
        Returns:
            Tuple (sucesso, mensagem)
        """
        try:
            if not os.path.exists(source):
                return False, f"Ficheiro de origem não encontrado: {source}"
            
            shutil.copy2(source, destination)
            return True, f"Ficheiro copiado de {source} para {destination}"
        except Exception as e:
            return False, f"Erro ao copiar ficheiro: {e}"
    
    def move_file(self, source: str, destination: str) -> Tuple[bool, str]:
        """
        Move um ficheiro
        
        Args:
            source: Caminho de origem
            destination: Caminho de destino
            
        Returns:
            Tuple (sucesso, mensagem)
        """
        try:
            if not os.path.exists(source):
                return False, f"Ficheiro de origem não encontrado: {source}"
            
            shutil.move(source, destination)
            return True, f"Ficheiro movido de {source} para {destination}"
        except Exception as e:
            return False, f"Erro ao mover ficheiro: {e}"
    
    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        """
        Obtém informações sobre um ficheiro
        
        Args:
            filepath: Caminho do ficheiro
            
        Returns:
            Dict com informações do ficheiro
        """
        try:
            if not os.path.exists(filepath):
                return {'erro': f'Ficheiro não encontrado: {filepath}'}
            
            stat = os.stat(filepath)
            
            return {
                'caminho': os.path.abspath(filepath),
                'nome': os.path.basename(filepath),
                'diretorio': os.path.dirname(os.path.abspath(filepath)),
                'extensao': os.path.splitext(filepath)[1],
                'tamanho_bytes': stat.st_size,
                'tamanho_kb': round(stat.st_size / 1024, 2),
                'tamanho_mb': round(stat.st_size / (1024**2), 2),
                'data_criacao': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'data_modificacao': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'data_acesso': datetime.fromtimestamp(stat.st_atime).isoformat(),
                'e_ficheiro': os.path.isfile(filepath),
                'e_diretorio': os.path.isdir(filepath),
                'e_link': os.path.islink(filepath),
            }
        except Exception as e:
            return {'erro': str(e)}
    
    def shutdown_system(self, delay: int = 60) -> Tuple[bool, str]:
        """
        Desliga o computador (com confirmação de delay)
        
        Args:
            delay: Tempo em segundos antes de desligar
            
        Returns:
            Tuple (sucesso, mensagem)
        """
        try:
            if self.is_windows:
                os.system(f'shutdown /s /t {delay}')
            elif self.is_linux:
                os.system(f'shutdown -h +{delay // 60}')
            elif self.is_mac:
                os.system(f'sudo shutdown -h +{delay // 60}')
            
            return True, f"Sistema será desligado em {delay} segundos"
        except Exception as e:
            return False, f"Erro ao agendar desligamento: {e}"
    
    def cancel_shutdown(self) -> Tuple[bool, str]:
        """
        Cancela o desligamento agendado
        
        Returns:
            Tuple (sucesso, mensagem)
        """
        try:
            if self.is_windows:
                os.system('shutdown /a')
            else:
                os.system('shutdown -c')
            
            return True, "Desligamento cancelado"
        except Exception as e:
            return False, f"Erro ao cancelar desligamento: {e}"
    
    def restart_system(self, delay: int = 60) -> Tuple[bool, str]:
        """
        Reinicia o computador
        
        Args:
            delay: Tempo em segundos antes de reiniciar
            
        Returns:
            Tuple (sucesso, mensagem)
        """
        try:
            if self.is_windows:
                os.system(f'shutdown /r /t {delay}')
            elif self.is_linux:
                os.system(f'shutdown -r +{delay // 60}')
            elif self.is_mac:
                os.system(f'sudo shutdown -r +{delay // 60}')
            
            return True, f"Sistema será reiniciado em {delay} segundos"
        except Exception as e:
            return False, f"Erro ao agendar reinício: {e}"


# Instância global
os_interaction = OSInteraction()
