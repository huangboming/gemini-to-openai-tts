# Stage 1: Builder - Installs dependencies
FROM python:3.12-slim as builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv pip sync --system

# Stage 2: Runner - The final, lean image
FROM python:3.12-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY app/ ./app/

RUN useradd -m -u 1000 user
USER user

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]