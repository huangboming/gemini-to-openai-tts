# Gemini to OpenAI TTS Proxy

**[English](README_EN.md) | 中文**

🎯 **一个高性能的文本转语音代理服务，无缝对接 Google Gemini TTS 模型（`gemini-2.5-flash-preview-tts`），完全兼容 OpenAI TTS API 接口规范。**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## ✨ 特性

- 🔄 **完全兼容 OpenAI TTS API** - 无需修改现有代码，直接替换 API 端点
- 🚀 **高性能异步架构** - 基于 FastAPI 和 uvicorn，支持高并发请求
- 🎙️ **丰富的语音选择** - 支持 30 种不同风格的 Gemini 语音
- 🎛️ **灵活的语音控制** - 支持语速调节和自然语言指令
- 🎵 **多种音频格式** - 支持 MP3、WAV、AAC、FLAC、OPUS 输出
- 🔒 **安全认证** - API 密钥认证，保护服务访问
- 📊 **结构化日志** - 完整的请求追踪和错误监控
- 🐳 **容器化部署** - 开箱即用的 Docker 支持
- 🛠️ **开发友好** - 完善的开发工具和代码质量保证

## 🚀 快速开始

### 使用 Docker（推荐）

1. **克隆项目**
   ```bash
   git clone https://github.com/huangboming/gemini-to-openai-tts
   cd gemini-to-openai-tts
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入你的 API 密钥
   ```

3. **构建并运行**
   ```bash
   make docker-build
   make docker-run
   ```

4. **测试服务**
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

### 本地开发

1. **环境要求**
   - Python 3.12+
   - FFmpeg
   - uv (推荐的包管理器)

2. **一键设置开发环境**
   ```bash
   git clone https://github.com/huangboming/gemini-to-openai-tts
   cd gemini-to-openai-tts
   make setup
   ```

3. **启动开发服务器**
   ```bash
   make run
   ```

4. **访问 API 文档**
   打开浏览器访问 http://localhost:8000/docs

## 📋 安装说明

### 系统依赖

#### macOS
```bash
# 安装 FFmpeg
brew install ffmpeg

# 安装 uv（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Ubuntu/Debian
```bash
# 安装 FFmpeg
sudo apt-get update && sudo apt-get install -y ffmpeg

# 安装 uv（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows
1. 从 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载并安装 FFmpeg
2. 将 FFmpeg 添加到系统 PATH
3. 安装 [uv](https://github.com/astral-sh/uv#installation)

### Python 依赖安装

#### 生产环境
```bash
uv pip sync
```

#### 开发环境
```bash
uv pip install -e ".[dev]"
```

## ⚙️ 配置说明

### 环境变量

创建 `.env` 文件（可以从 `.env.example` 复制）：

```env
# === 服务认证配置 ===
# 客户端访问此服务时需要提供的 API 密钥（可以是多个，用逗号分隔）
API_KEYS="your_secret_api_key_1,your_secret_api_key_2"

# === 上游 API 配置 ===
# 你的 Google Gemini API 密钥
# 获取方式：https://ai.google.dev/
GEMINI_API_KEY="your_google_gemini_api_key_here"

# === 应用配置 ===
# 日志级别：DEBUG, INFO, WARNING, ERROR
LOG_LEVEL="INFO"
```

### 获取 Gemini API 密钥

1. 访问 [Google AI Studio](https://ai.google.dev/)
2. 登录你的 Google 账户
3. 创建新的 API 密钥
4. 将密钥复制到 `.env` 文件中

## 📖 API 使用指南

### 端点

```
POST /v1/audio/speech       # 文本转语音
GET  /v1/audio/models       # 获取可用模型列表
GET  /v1/audio/voices       # 获取可用语音列表
```

### 获取模型列表

#### 端点
```
GET /v1/audio/models
```

#### 响应示例
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

#### cURL 示例
```bash
curl -X GET "http://localhost:8000/v1/audio/models"
```

### 获取语音列表

#### 端点
```
GET /v1/audio/voices
```

#### 响应示例
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

#### cURL 示例
```bash
curl -X GET "http://localhost:8000/v1/audio/voices"
```

### 文本转语音

#### 端点
```
POST /v1/audio/speech
```

### 请求头

```http
Authorization: Bearer your_api_key
Content-Type: application/json
```

### 请求体

```json
{
  "model": "gemini-2.5-flash-preview-tts",
  "input": "要转换为语音的文本",
  "voice": "Zephyr",
  "response_format": "mp3",
  "speed": 1.0,
  "instructions": "请用愉快的语调朗读"
}
```

#### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | TTS 模型名称，支持 `gemini-2.5-flash-preview-tts` 等 |
| `input` | string | ✅ | 要转换的文本内容 |
| `voice` | string | ✅ | 语音名称，见[支持的语音](#支持的语音) |
| `response_format` | string | ❌ | 输出格式：`mp3`、`wav`、`aac`、`flac`、`opus`（默认：`mp3`） |
| `speed` | float | ❌ | 语速倍率：0.25-4.0（默认：1.0） |
| `instructions` | string | ❌ | 自然语言指令，用于控制语音风格 |

### 支持的语音

| 语音名称 | 风格描述 | 语音名称 | 风格描述 |
|----------|----------|----------|----------|
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

### 使用示例

#### Python 示例

```python
import requests

# 获取可用模型列表
models_response = requests.get("http://localhost:8000/v1/audio/models")
models = models_response.json()
print("Available models:", models)

# 获取可用语音列表
voices_response = requests.get("http://localhost:8000/v1/audio/voices")
voices = voices_response.json()
print("Available voices:", voices)

# 文本转语音请求
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

# 保存音频文件
with open("output.mp3", "wb") as f:
    f.write(response.content)
```

#### cURL 示例

```bash
# 获取可用模型列表
curl -X GET "http://localhost:8000/v1/audio/models"

# 获取可用语音列表
curl -X GET "http://localhost:8000/v1/audio/voices"

# 基本文本转语音请求
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

# 使用不同语音和格式
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-preview-tts",
    "input": "This is a professional announcement.",
    "voice": "Charon",
    "response_format": "wav",
    "speed": 0.9
  }' \
  --output announcement.wav
```


## 🐳 部署指南

### Docker 部署（推荐）

#### 单机部署

```bash
# 1. 构建镜像
docker build -t gemini-to-openai-tts .

# 2. 运行容器
docker run -d \
  --name gemini-tts \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  gemini-to-openai-tts
```

#### Docker Compose

创建 `docker-compose.yml`：

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

运行：

```bash
docker-compose up -d
```

### 生产环境建议

1. **安全配置**
   - 使用强随机 API 密钥
   - 启用 HTTPS
   - 设置防火墙规则
   - 定期更新依赖

2. **性能优化**
   - 使用多个 worker 进程
   - 配置适当的资源限制
   - 启用 gzip 压缩

3. **监控和日志**
   - 设置日志轮转
   - 配置健康检查
   - 监控服务状态和性能

## 🛠️ 开发指南

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/huangboming/gemini-to-openai-tts
cd gemini-to-openai-tts

# 一键设置开发环境
make setup
```

### 常用开发命令

```bash
# 查看所有可用命令
make help

# 启动开发服务器（支持热重载）
make run

# 代码质量检查
make check          # 运行 lint 和格式检查
make lint           # 仅运行 lint
make format         # 格式化代码

# 测试和清理
make test           # 运行测试（待实现）
make clean          # 清理缓存文件

# Git hooks
make pre-commit     # 手动运行 pre-commit hooks
```

### 项目结构

```
gemini-to-openai-tts/
├── app/                    # 主要应用代码
│   ├── core/              # 核心配置和工具
│   │   ├── config.py      # 配置管理
│   │   ├── logging.py     # 日志配置
│   │   └── security.py    # 认证逻辑
│   ├── models/            # 数据模型
│   │   └── schemas.py     # Pydantic 模型
│   ├── services/          # 业务逻辑
│   │   ├── audio_processor.py  # 音频处理
│   │   └── gemini_client.py    # Gemini API 客户端
│   ├── utils/             # 工具函数
│   │   └── error_handlers.py   # 异常处理
│   └── main.py            # FastAPI 应用入口
├── scripts/               # 开发脚本
│   └── dev-setup.sh      # 开发环境设置
├── .env.example          # 环境变量模板
├── Dockerfile            # Docker 构建文件
├── Makefile             # 开发命令
├── pyproject.toml       # 项目配置和依赖
└── README.md            # 项目文档
```

### 代码质量

项目使用以下工具确保代码质量：

- **Ruff**: 代码检查和格式化
- **Pre-commit**: 提交前自动检查
- **Type hints**: 类型注解支持
- **Pydantic**: 数据验证和序列化

### 贡献指南

1. Fork 项目
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交变更：`git commit -am 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

## 🔧 故障排除

### 常见问题

#### 1. FFmpeg 未安装
```
错误：ModuleNotFoundError: No module named 'pydub'
解决：安装 FFmpeg（见安装说明）
```

#### 2. Gemini API 密钥无效
```
错误：Upstream API authentication failed
解决：检查 GEMINI_API_KEY 是否正确设置
```

#### 3. 端口占用
```
错误：Port 8000 is already in use
解决：使用其他端口或停止占用进程
```

#### 4. 音频格式不支持
```
错误：Invalid value for parameter 'response_format'
解决：使用支持的格式：mp3, wav, aac, flac, opus
```

### 日志调试

设置详细日志：

```env
LOG_LEVEL="DEBUG"
```

查看实时日志：

```bash
# Docker
docker logs -f gemini-tts

# 本地开发
make run
```

### 健康检查

```bash
# 检查服务状态
curl http://localhost:8000/health

# 检查 API 文档
curl http://localhost:8000/docs
```

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Python Web 框架
- [Google Gemini](https://ai.google.dev/) - 强大的 AI 语音合成
- [Pydub](https://pydub.com/) - 音频处理库
- [OpenAI](https://openai.com/) - API 规范参考

---

⭐ 如果这个项目对你有帮助，请考虑给它一个 star！
