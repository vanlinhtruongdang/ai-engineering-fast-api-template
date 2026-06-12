FROM python:3.12-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/fastapi-template-venv \
    LOG_DIR=/tmp/fastapi-template-logs \
    PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Install uv from official image and keep runtime minimal.
COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /bin/

FROM base AS builder

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

FROM base AS runtime

RUN groupadd --gid 10001 appgroup \
    && useradd --uid 10001 --gid appgroup --create-home --shell /usr/sbin/nologin appuser

COPY --from=builder /opt/fastapi-template-venv /opt/fastapi-template-venv
COPY app /app/app

ENV PATH="/opt/fastapi-template-venv/bin:${PATH}" \
    PYTHONPATH="/app"

RUN mkdir -p /app/logs /tmp/fastapi-template-logs \
    && chown -R appuser:appgroup /app /tmp/fastapi-template-logs
USER appuser

EXPOSE 1114

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:1114/health', timeout=3)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1114"]
