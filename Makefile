.PHONY: help install dev-install setup run test lint format check clean docker-build docker-run pre-commit

# 默认目标
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  dev-install  - Install development dependencies"
	@echo "  setup        - One-time development environment setup"
	@echo "  run          - Run the development server"
	@echo "  test         - Run tests (placeholder)"
	@echo "  lint         - Run linting with ruff"
	@echo "  format       - Format code with ruff"
	@echo "  check        - Run both linting and formatting checks"
	@echo "  pre-commit   - Run pre-commit hooks manually"
	@echo "  clean        - Clean up cache files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"

# 安装生产依赖
install:
	uv pip sync

# 安装开发依赖
dev-install:
	uv pip install -e ".[dev]"

# 一键设置开发环境
setup:
	@if [ ! -f "scripts/dev-setup.sh" ]; then echo "❌ scripts/dev-setup.sh not found"; exit 1; fi
	bash scripts/dev-setup.sh

# 运行开发服务器
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 运行测试（占位符）
test:
	@echo "Tests not implemented yet"

# 代码检查
lint:
	ruff check app/

# 代码格式化
format:
	ruff format app/

# 检查代码（包括 lint 和 format 检查）
check:
	ruff check app/
	ruff format app/ --check

# 手动运行 pre-commit hooks
pre-commit:
	pre-commit run --all-files

# 清理缓存文件
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .ruff_cache 2>/dev/null || true

# 构建 Docker 镜像
docker-build:
	docker build -t gemini-to-openai-tts .

# 运行 Docker 容器
docker-run:
	docker run --rm -p 8000:8000 --env-file .env gemini-to-openai-tts 