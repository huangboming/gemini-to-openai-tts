#!/bin/bash
# scripts/dev-setup.sh
# 开发环境一键设置脚本

set -e  # 遇到错误立即退出

echo "🚀 正在设置 Gemini to OpenAI TTS Proxy 开发环境..."

# 检查 uv 是否已安装
if ! command -v uv &> /dev/null; then
    echo "❌ 错误：未找到 uv 命令。请先安装 uv："
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 检查 FFmpeg 是否已安装
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ 错误：未找到 ffmpeg 命令。请先安装 FFmpeg："
    echo "   macOS: brew install ffmpeg"
    echo "   Ubuntu/Debian: sudo apt-get install ffmpeg"
    exit 1
fi

# 安装开发依赖
echo "📦 安装开发依赖..."
uv sync

# 设置 pre-commit hooks
echo "🔧 设置 pre-commit hooks..."
uv run pre-commit install

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量文件..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件，填入你的实际 API 密钥"
else
    echo "✅ 环境变量文件已存在"
fi

# 运行代码检查
echo "🔍 运行代码检查..."
make check

echo ""
echo "🎉 开发环境设置完成！"
echo ""
echo "📋 接下来的步骤："
echo "   1. 编辑 .env 文件，填入你的 API 密钥"
echo "   2. 运行开发服务器：make run"
echo "   3. 访问 http://localhost:8000/docs 查看 API 文档"
echo ""
echo "🛠️  常用命令："
echo "   make help     - 查看所有可用命令"
echo "   make run      - 启动开发服务器"
echo "   make check    - 运行代码检查"
echo "   make format   - 格式化代码"
