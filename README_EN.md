# Gemini to OpenAI TTS Proxy

**English | [中文](README.md)**

🎯 **A high-performance text-to-speech proxy service that seamlessly integrates with Google Gemini TTS model (`gemini-2.5-flash-preview-tts`), fully compatible with OpenAI TTS API specifications.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## ✨ Features

- 🔄 **Fully Compatible with OpenAI TTS API** - Drop-in replacement, no code changes required
- 🚀 **High-Performance Async Architecture** - Built on FastAPI and uvicorn for high concurrency
- 🎙️ **Rich Voice Selection** - Support for 30 different Gemini voice styles
- 🎛️ **Flexible Voice Control** - Speed adjustment and natural language instructions
- 🎵 **Multiple Audio Formats** - Support for MP3, WAV, AAC, FLAC, OPUS output
- 🔒 **Secure Authentication** - API key authentication for protected access
- 📊 **Structured Logging** - Complete request tracking and error monitoring
- 🐳 **Containerized Deployment** - Out-of-the-box Docker support
- 🛠️ **Developer Friendly** - Comprehensive dev tools and code quality assurance

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/huangboming/gemini-to-openai-tts
   cd gemini-to-openai-tts
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file and fill in your API keys
   ```

3. **Build and run**
   ```bash
   make docker-build
   make docker-run
   ```

4. **Test the service**
   ```bash
   curl -X POST "http://localhost:8000/v1/audio/speech" \
     -H "Authorization: Bearer your_api_key" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gemini-2.5-flash-preview-tts",
       "input": "Hello, this is a test of the text-to-speech service.",
       "voice": "Zephyr",
       "response_format": "mp3"
     }' \
     --output speech.mp3
   ```

### Local Development

1. **Requirements**
   - Python 3.12+
   - FFmpeg
   - uv (recommended package manager)

2. **One-click development setup**
   ```bash
   git clone https://github.com/huangboming/gemini-to-openai-tts
   cd gemini-to-openai-tts
   make setup
   ```

3. **Start development server**
   ```bash
   make run
   ```

4. **Access API documentation**
   Open your browser and visit http://localhost:8000/docs

## 📋 Installation Guide

<details>
<summary><strong>📦 System Dependencies Installation Details</strong></summary>

### System Dependencies

#### macOS
```bash
# Install FFmpeg
brew install ffmpeg

# Install uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Ubuntu/Debian
```bash
# Install FFmpeg
sudo apt-get update && sudo apt-get install -y ffmpeg

# Install uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows
1. Download and install FFmpeg from [FFmpeg official website](https://ffmpeg.org/download.html)
2. Add FFmpeg to system PATH
3. Install [uv](https://github.com/astral-sh/uv#installation)

### Python Dependencies

#### Production Environment
```bash
uv pip sync
```

#### Development Environment
```bash
uv pip install -e ".[dev]"
```

</details>

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
# === Service Authentication Configuration ===
# API keys that clients need to provide when accessing this service (can be multiple, comma-separated)
API_KEYS="your_secret_api_key_1,your_secret_api_key_2"

# === Upstream API Configuration ===
# Your Google Gemini API key
# Get it from: https://ai.google.dev/
GEMINI_API_KEY="your_google_gemini_api_key_here"

# === Application Configuration ===
# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL="INFO"
```

### Getting Gemini API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Sign in to your Google account
3. Create a new API key
4. Copy the key to your `.env` file

## 📖 API Usage Guide

### Endpoints

```
POST /v1/audio/speech       # Text-to-speech conversion
GET  /v1/audio/models       # Get available models list
GET  /v1/audio/voices       # Get available voices list
```

### Get Models List

#### Endpoint
```
GET /v1/audio/models
```

#### Response Example
```json
{
  "data": [
    {
      "id": "gemini-2.5-flash-preview-tts",
      "name": "Gemini 2.5 Flash TTS"
    }
  ]
}
```

#### cURL Example
```bash
curl -X GET "http://localhost:8000/v1/audio/models"
```

### Get Voices List

#### Endpoint
```
GET /v1/audio/voices
```

#### Response Example
```json
{
  "voices": [
    "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus", "Aoede",
    "Callirrhoe", "Autonoe", "Enceladus", "Iapetus", "Umbriel", "Algieba",
    "Despina", "Erinome", "Algenib", "Rasalgethi", "Laomedeia", "Achernar",
    "Alnilam", "Schedar", "Gacrux", "Pulcherrima", "Achird", "Zubenelgenubi",
    "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat"
  ]
}
```

#### cURL Example
```bash
curl -X GET "http://localhost:8000/v1/audio/voices"
```

### Text-to-Speech Conversion

#### Endpoint
```
POST /v1/audio/speech
```

### Request Headers

```http
Authorization: Bearer your_api_key
Content-Type: application/json
```

### Request Body

```json
{
  "model": "gemini-2.5-flash-preview-tts",
  "input": "Text to convert to speech",
  "voice": "Zephyr",
  "response_format": "mp3",
  "speed": 1.0,
  "instructions": "Please read with a cheerful tone"
}
```

#### Parameter Description

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | ✅ | TTS model name, supports `gemini-2.5-flash-preview-tts` etc. |
| `input` | string | ✅ | Text content to convert |
| `voice` | string | ✅ | Voice name, see [Supported Voices](#supported-voices) |
| `response_format` | string | ❌ | Output format: `mp3`, `wav`, `aac`, `flac`, `opus` (default: `mp3`) |
| `speed` | float | ❌ | Speed multiplier: 0.25-4.0 (default: 1.0) |
| `instructions` | string | ❌ | Natural language instructions for voice style control |

### Supported Voices

<details>
<summary><strong>🎙️ View All 30 Available Voices</strong></summary>

| Voice Name | Style Description | Voice Name | Style Description |
|------------|-------------------|------------|-------------------|
| Zephyr | Bright | Puck | Upbeat |
| Charon | Informative | Kore | Firm |
| Fenrir | Excitable | Leda | Youthful |
| Orus | Firm | Aoede | Breezy |
| Callirrhoe | Easy-going | Autonoe | Bright |
| Enceladus | Breathy | Iapetus | Clear |
| Umbriel | Easy-going | Algieba | Smooth |
| Despina | Smooth | Erinome | Clear |
| Algenib | Gravelly | Rasalgethi | Informative |
| Laomedeia | Upbeat | Achernar | Soft |
| Alnilam | Firm | Schedar | Even |
| Gacrux | Mature | Pulcherrima | Forward |
| Achird | Friendly | Zubenelgenubi | Casual |
| Vindemiatrix | Gentle | Sadachbia | Lively |
| Sadaltager | Knowledgeable | Sulafat | Warm |

</details>

### Usage Examples

#### Python Example

```python
import requests

# Get available models list
models_response = requests.get("http://localhost:8000/v1/audio/models")
models = models_response.json()
print("Available models:", models)

# Get available voices list
voices_response = requests.get("http://localhost:8000/v1/audio/voices")
voices = voices_response.json()
print("Available voices:", voices)

# Text-to-speech request
response = requests.post(
    "http://localhost:8000/v1/audio/speech",
    headers={
        "Authorization": "Bearer your_api_key",
        "Content-Type": "application/json"
    },
    json={
        "model": "gemini-2.5-flash-preview-tts",
        "input": "Hello, world! This is a test of our TTS service.",
        "voice": "Zephyr",
        "response_format": "mp3"
    }
)

# Save audio file
with open("output.mp3", "wb") as f:
    f.write(response.content)
```

#### cURL Examples

```bash
# Basic text-to-speech request
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-preview-tts",
    "input": "Hello, this is a test message.",
    "voice": "Zephyr",
    "response_format": "mp3",
    "speed": 1.2,
    "instructions": "Please speak with enthusiasm"
  }' \
  --output speech.mp3
```

<details>
<summary><strong>📋 More API Usage Examples</strong></summary>

### Get Models and Voices List Examples

```bash
# Get available models list
curl -X GET "http://localhost:8000/v1/audio/models"

# Get available voices list
curl -X GET "http://localhost:8000/v1/audio/voices"
```

### Advanced Parameters Examples

```bash
# Request with speed and instructions
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-preview-tts",
    "input": "Welcome to our text-to-speech service!",
    "voice": "Zephyr",
    "response_format": "mp3",
    "speed": 1.2,
    "instructions": "Please read with a cheerful and energetic tone"
  }' \
  --output welcome.mp3
```

</details>

## 🐳 Deployment Guide

### Docker Deployment (Recommended)

#### Single Instance Deployment

```bash
# 1. Build image
docker build -t gemini-to-openai-tts .

# 2. Run container
docker run -d \
  --name gemini-tts \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  gemini-to-openai-tts
```

#### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  gemini-tts:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run:

```bash
docker-compose up -d
```

### Production Recommendations

1. **Security Configuration**
   - Use strong random API keys
   - Enable HTTPS
   - Configure firewall rules
   - Regular dependency updates

2. **Performance Optimization**
   - Use multiple worker processes
   - Configure appropriate resource limits
   - Enable gzip compression

3. **Monitoring and Logging**
   - Set up log rotation
   - Configure health checks
   - Monitor service status and performance

## 🛠️ Development Guide

### Development Environment Setup

```bash
# Clone repository
git clone https://github.com/huangboming/gemini-to-openai-tts
cd gemini-to-openai-tts

# One-click development environment setup
make setup
```

### Common Development Commands

```bash
# View all available commands
make help

# Start development server (with hot reload)
make run

# Code quality checks
make check          # Run lint and format checks
make lint           # Lint only
make format         # Format code

# Testing and cleanup
make test           # Run tests (to be implemented)
make clean          # Clean cache files

# Git hooks
make pre-commit     # Manually run pre-commit hooks
```

<details>
<summary><strong>📁 Project Structure Details</strong></summary>

### Project Structure

```
gemini-to-openai-tts/
├── app/                    # Main application code
│   ├── core/              # Core configuration and utilities
│   │   ├── config.py      # Configuration management
│   │   ├── logging.py     # Logging configuration
│   │   └── security.py    # Authentication logic
│   ├── models/            # Data models
│   │   └── schemas.py     # Pydantic models
│   ├── services/          # Business logic
│   │   ├── audio_processor.py  # Audio processing
│   │   └── gemini_client.py    # Gemini API client
│   ├── utils/             # Utility functions
│   │   └── error_handlers.py   # Exception handling
│   └── main.py            # FastAPI application entry point
├── scripts/               # Development scripts
│   └── dev-setup.sh      # Development environment setup
├── .env.example          # Environment variables template
├── Dockerfile            # Docker build file
├── Makefile             # Development commands
├── pyproject.toml       # Project configuration and dependencies
└── README.md            # Project documentation
```

</details>

<details>
<summary><strong>🔧 Code Quality and Contributing Guidelines</strong></summary>

### Code Quality

The project uses the following tools to ensure code quality:

- **Ruff**: Code linting and formatting
- **Pre-commit**: Automatic pre-commit checks
- **Type hints**: Type annotation support
- **Pydantic**: Data validation and serialization

### Contributing Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Create a Pull Request

</details>

## 🔧 Troubleshooting

<details>
<summary><strong>❓ Common Issues and Solutions</strong></summary>

### Common Issues

#### 1. FFmpeg Not Installed
```
Error: ModuleNotFoundError: No module named 'pydub'
Solution: Install FFmpeg (see installation guide)
```

#### 2. Invalid Gemini API Key
```
Error: Upstream API authentication failed
Solution: Check if GEMINI_API_KEY is correctly set
```

#### 3. Port Already in Use
```
Error: Port 8000 is already in use
Solution: Use a different port or stop the process using the port
```

#### 4. Unsupported Audio Format
```
Error: Invalid value for parameter 'response_format'
Solution: Use supported formats: mp3, wav, aac, flac, opus
```

### Debug Logging

Enable verbose logging:

```env
LOG_LEVEL="DEBUG"
```

View real-time logs:

```bash
# Docker
docker logs -f gemini-tts

# Local development
make run
```

### Health Checks

```bash
# Check service status
curl http://localhost:8000/health

# Check API documentation
curl http://localhost:8000/docs
```

</details>

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Google Gemini](https://ai.google.dev/) - Powerful AI speech synthesis
- [Pydub](https://pydub.com/) - Audio processing library
- [OpenAI](https://openai.com/) - API specification reference

---

⭐ If this project helps you, please consider giving it a star! 