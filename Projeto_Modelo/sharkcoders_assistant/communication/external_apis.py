#!/usr/bin/env python3
"""
SharkCoders Assistant - APIs Externas
Módulo para consumo de APIs públicas.
"""

import sys
from pathlib import Path
from typing import Optional, Dict
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ requests não instalado. Instale: pip install requests")

from config import EXTERNAL_APIS
from utils import logger


class WeatherAPI:
    """
    API para obter informação meteorológica.
    Usa OpenWeatherMap.
    """
    
    def __init__(self, api_key: str = None):
        """
        Inicializa a API de tempo.
        
        Args:
            api_key: Chave da API (opcional, usa config se não fornecida)
        """
        self.api_key = api_key or EXTERNAL_APIS.get("weather_api_key", "")
        self.base_url = EXTERNAL_APIS.get("weather", "https://api.openweathermap.org/data/2.5/weather")
        self.available = REQUESTS_AVAILABLE and bool(self.api_key)
    
    def get_weather(self, city: str, country: str = "PT") -> Optional[Dict]:
        """
        Obtém informação meteorológica de uma cidade.
        
        Args:
            city: Nome da cidade
            country: Código do país (padrão: PT)
        
        Returns:
            Dicionário com informação ou None
        """
        if not self.available:
            logger.warning("API de tempo não disponível. Configure OPENWEATHER_API_KEY.")
            return None
        
        try:
            params = {
                "q": f"{city},{country}",
                "appid": self.api_key,
                "units": "metric",
                "lang": "pt",
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data.get("name"),
                    "country": data.get("sys", {}).get("country"),
                    "temperature": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "description": data.get("weather", [{}])[0].get("description", ""),
                    "wind_speed": data.get("wind", {}).get("speed"),
                }
            else:
                logger.warning(f"Erro na API de tempo: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao obter tempo: {e}")
            return None
    
    def get_weather_text(self, city: str, country: str = "PT") -> str:
        """
        Obtém informação meteorológica formatada em texto.
        
        Args:
            city: Nome da cidade
            country: Código do país
        
        Returns:
            Texto formatado
        """
        data = self.get_weather(city, country)
        
        if not data:
            return f"Não foi possível obter o tempo para {city}."
        
        return (
            f"🌡️ Tempo em {data['city']}, {data['country']}:\n"
            f"   Temperatura: {data['temperature']}°C (sensação: {data['feels_like']}°C)\n"
            f"   Condição: {data['description'].capitalize()}\n"
            f"   Humidade: {data['humidity']}%\n"
            f"   Vento: {data['wind_speed']} m/s"
        )


class QuotesAPI:
    """
    API para obter citações inspiradoras.
    Usa quotable.io (gratuita, sem chave).
    """
    
    def __init__(self):
        """Inicializa a API de citações."""
        self.base_url = EXTERNAL_APIS.get("quotes", "https://api.quotable.io/random")
        self.available = REQUESTS_AVAILABLE
    
    def get_quote(self) -> Optional[Dict]:
        """
        Obtém uma citação aleatória.
        
        Returns:
            Dicionário com citação ou None
        """
        if not self.available:
            return None
        
        try:
            response = requests.get(self.base_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "content": data.get("content", ""),
                    "author": data.get("author", "Desconhecido"),
                    "tags": data.get("tags", []),
                }
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter citação: {e}")
            return None
    
    def get_quote_text(self) -> str:
        """
        Obtém uma citação formatada em texto.
        
        Returns:
            Texto formatado
        """
        data = self.get_quote()
        
        if not data:
            return "Não foi possível obter uma citação."
        
        return f'"{data["content"]}"\n   — {data["author"]}'


class JokesAPI:
    """
    API para obter piadas.
    Usa jokeapi.dev (gratuita, suporta português).
    """
    
    def __init__(self):
        """Inicializa a API de piadas."""
        self.base_url = EXTERNAL_APIS.get("jokes", "https://v2.jokeapi.dev/joke/Any")
        self.available = REQUESTS_AVAILABLE
    
    def get_joke(self, language: str = "pt") -> Optional[Dict]:
        """
        Obtém uma piada aleatória.
        
        Args:
            language: Idioma ('pt', 'en', etc.)
        
        Returns:
            Dicionário com piada ou None
        """
        if not self.available:
            return None
        
        try:
            params = {
                "lang": language,
                "type": "single",  # Piadas de uma linha
                "safe-mode": "",   # Modo seguro
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("error"):
                    # Tentar em inglês se falhar em português
                    if language != "en":
                        return self.get_joke("en")
                    return None
                
                if data.get("type") == "single":
                    return {
                        "joke": data.get("joke", ""),
                        "type": "single",
                        "category": data.get("category", ""),
                    }
                else:
                    return {
                        "setup": data.get("setup", ""),
                        "delivery": data.get("delivery", ""),
                        "type": "twopart",
                        "category": data.get("category", ""),
                    }
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter piada: {e}")
            return None
    
    def get_joke_text(self) -> str:
        """
        Obtém uma piada formatada em texto.
        
        Returns:
            Texto da piada
        """
        data = self.get_joke()
        
        if not data:
            # Piada de fallback
            return "Porque é que o programador foi ao médico? Porque tinha um vírus! 😄"
        
        if data["type"] == "single":
            return data["joke"]
        else:
            return f"{data['setup']}\n{data['delivery']}"


class FactsAPI:
    """
    API para obter factos interessantes.
    Usa uselessfacts.jsph.pl (gratuita).
    """
    
    def __init__(self):
        """Inicializa a API de factos."""
        self.base_url = EXTERNAL_APIS.get("facts", "https://uselessfacts.jsph.pl/random.json")
        self.available = REQUESTS_AVAILABLE
    
    def get_fact(self, language: str = "en") -> Optional[Dict]:
        """
        Obtém um facto aleatório.
        
        Args:
            language: Idioma ('en' ou 'de')
        
        Returns:
            Dicionário com facto ou None
        """
        if not self.available:
            return None
        
        try:
            params = {"language": language}
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "text": data.get("text", ""),
                    "source": data.get("source", ""),
                    "source_url": data.get("source_url", ""),
                }
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter facto: {e}")
            return None
    
    def get_fact_text(self) -> str:
        """
        Obtém um facto formatado em texto.
        
        Returns:
            Texto do facto
        """
        data = self.get_fact()
        
        if not data:
            return "Sabias que o polvo tem três corações? 🐙"
        
        # O facto vem em inglês, podemos adicionar tradução se necessário
        return f"🎲 Facto: {data['text']}"


class ExternalAPIs:
    """
    Classe agregadora de todas as APIs externas.
    """
    
    def __init__(self):
        """Inicializa todas as APIs."""
        self.weather = WeatherAPI()
        self.quotes = QuotesAPI()
        self.jokes = JokesAPI()
        self.facts = FactsAPI()
    
    def get_quote(self) -> str:
        """Obtém uma citação."""
        return self.quotes.get_quote_text()
    
    def get_joke(self) -> str:
        """Obtém uma piada."""
        return self.jokes.get_joke_text()
    
    def get_fact(self) -> str:
        """Obtém um facto."""
        return self.facts.get_fact_text()
    
    def get_weather(self, city: str, country: str = "PT") -> str:
        """Obtém informação do tempo."""
        return self.weather.get_weather_text(city, country)


# Instâncias globais
weather_api = WeatherAPI()
quotes_api = QuotesAPI()
jokes_api = JokesAPI()
facts_api = FactsAPI()
external_apis = ExternalAPIs()

# Funções de conveniência
def get_quote() -> str:
    """Obtém uma citação."""
    return quotes_api.get_quote_text()

def get_joke() -> str:
    """Obtém uma piada."""
    return jokes_api.get_joke_text()

def get_fact() -> str:
    """Obtém um facto."""
    return facts_api.get_fact_text()

def get_weather(city: str, country: str = "PT") -> str:
    """Obtém informação do tempo."""
    return weather_api.get_weather_text(city, country)


if __name__ == "__main__":
    # Teste das APIs externas
    print("=" * 50)
    print("🌐 Teste de APIs Externas")
    print("=" * 50)
    
    print(f"\n📦 requests disponível: {REQUESTS_AVAILABLE}")
    
    if REQUESTS_AVAILABLE:
        # Testar citação
        print("\n💭 Citação:")
        print(f"   {get_quote()}")
        
        # Testar piada
        print("\n😂 Piada:")
        print(f"   {get_joke()}")
        
        # Testar facto
        print("\n🎲 Facto:")
        print(f"   {get_fact()}")
        
        # Testar tempo (só funciona com API key)
        if weather_api.available:
            print("\n🌡️ Tempo:")
            print(f"   {get_weather('Lisboa')}")
        else:
            print("\n⚠️ API de tempo não configurada")
            print("   Configure OPENWEATHER_API_KEY para usar")
    
    print("\n✅ Teste concluído!")
