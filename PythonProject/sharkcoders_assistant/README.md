# 🦈 SharkCoders Assistant

Um **Assistente Multimodal** completo desenvolvido em Python, criado como projeto final do curso "Python for AI - Módulo 1" da SharkCoders.

## 📋 Descrição

O SharkCoders Assistant é um centro de operações digital que integra múltiplas funcionalidades:

- 🖥️ **Interface Gráfica** - GUI moderna com tkinter
- 🎤 **Comandos de Voz** - Reconhecimento e síntese de fala em português
- 📸 **Captura de Ecrã** - Screenshots completos ou parciais
- 🔤 **OCR** - Reconhecimento de texto em imagens
- 🤖 **Automação** - Controlo de rato e teclado
- 📱 **Telegram** - Envio de imagens e mensagens
- 🌐 **APIs Externas** - Citações, piadas, tempo, factos
- 🔌 **API Própria** - Servidor HTTP Flask para controlo remoto
- 💻 **Sistema** - Interação com o sistema operativo

## 🚀 Instalação

### Pré-requisitos

1. **Python 3.8+** instalado
2. **Tesseract OCR** (para reconhecimento de texto)

### Instalar Tesseract OCR (Windows)

Descarregar e instalar de: https://github.com/UB-Mannheim/tesseract/wiki

### Instalar Dependências Python

```bash
cd sharkcoders_assistant
pip install -r requirements.txt
```

### Configurar Variáveis de Ambiente (Opcional)

Criar ficheiro `.env` na raiz do projeto:

```env
TELEGRAM_BOT_TOKEN=seu_token_do_bot_telegram
OPENWEATHER_API_KEY=sua_chave_openweathermap
```

## 🎮 Como Usar

### Iniciar a Aplicação

```bash
python main.py
```

### Comandos de Voz Disponíveis

| Comando | Ação |
|---------|------|
| "capturar ecrã" | Tira screenshot do ecrã |
| "ler imagem" | Extrai texto da última imagem |
| "enviar imagem" | Envia imagem via Telegram |
| "que horas são" | Diz as horas actuais |
| "que dia é hoje" | Diz a data actual |
| "diz uma piada" | Conta uma piada |
| "uma citação" | Diz uma citação inspiradora |
| "janela ativa" | Identifica a janela actual |
| "listar janelas" | Lista todas as janelas abertas |
| "ajuda" | Lista todos os comandos |
| "sair" | Fecha a aplicação |

### Interface Gráfica

A GUI está dividida em secções:

1. **Voz** - Botões para ouvir e falar
2. **Captura/OCR** - Capturar ecrã e extrair texto
3. **Envio** - Enviar imagens via Telegram
4. **APIs/Sistema** - Consultar APIs e info do sistema

## 🔌 API HTTP

O assistente disponibiliza uma API REST local:

### Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informação da API |
| GET | `/api/status` | Estado do assistente |
| GET | `/api/text` | Último texto extraído |
| GET | `/api/screenshot` | Última captura de ecrã |
| POST | `/api/command` | Enviar comando |
| GET | `/api/info` | Informação do sistema |

### Exemplo de Uso

```bash
# Obter estado
curl http://localhost:5000/api/status

# Enviar comando
curl -X POST http://localhost:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "capture_screen"}'
```

## 📁 Estrutura do Projeto

```
sharkcoders_assistant/
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências
├── config.py              # Configurações
├── README.md              # Documentação
│
├── gui/                   # Interface Gráfica
├── voice/                 # Interação por Voz
├── automation/            # Automação
├── vision/                # Processamento de Imagem e OCR
├── communication/         # Telegram e APIs externas
├── api/                   # API Flask
├── system/                # Interação com SO
├── assets/                # ASCII Art e recursos
└── utils/                 # Utilitários
```

## 🛠️ Tecnologias Utilizadas

- **tkinter** - Interface gráfica
- **SpeechRecognition** - Reconhecimento de voz
- **pyttsx3** - Síntese de voz
- **PyAutoGUI** - Automação
- **OpenCV** - Processamento de imagem
- **pytesseract** - OCR
- **Flask** - API HTTP
- **requests** - Chamadas HTTP
- **python-telegram-bot** - Integração Telegram

## 📝 Notas

- O Tesseract OCR deve estar instalado e configurado no `config.py`
- Para funcionalidades do Telegram, configurar o token do bot
- A API de tempo requer chave da OpenWeatherMap
- Testado principalmente em Windows, com suporte para Linux/macOS

## 👥 Autores

Desenvolvido pelos alunos da **SharkCoders** - Escola de Programação

## 📄 Licença

Este projeto é para fins educativos.

---

🦈 **SharkCoders** - Aprende a programar como um tubarão! 🌊
