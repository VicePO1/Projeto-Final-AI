#!/usr/bin/env python3
"""
SharkCoders Assistant - Módulo Communication
Comunicação externa via Telegram e APIs.
"""

from .message_sender import TelegramSender, MessageSender, telegram_sender, message_sender
from .external_apis import (
    WeatherAPI, QuotesAPI, JokesAPI, FactsAPI, ExternalAPIs,
    weather_api, quotes_api, jokes_api, facts_api, external_apis,
    get_quote, get_joke, get_fact, get_weather,
)

__all__ = [
    "TelegramSender",
    "MessageSender",
    "telegram_sender",
    "message_sender",
    "WeatherAPI",
    "QuotesAPI",
    "JokesAPI",
    "FactsAPI",
    "ExternalAPIs",
    "weather_api",
    "quotes_api",
    "jokes_api",
    "facts_api",
    "external_apis",
    "get_quote",
    "get_joke",
    "get_fact",
    "get_weather",
]
