# Multi-stage Dockerfile for FastAPI Backend with UV
# Python 3.13 base image
FROM python:3.13-slim AS builder

# Install UV package manager
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml README.md ./

# Install dependencies using UV
RUN uv sync --no-dev

# Runtime stage
FROM python:3.13-slim

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY src/ /app/src/
COPY alembic/ /app/alembic/
COPY alembic.ini /app/

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Health check (uses PORT env var, defaults to 7860)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; import os; urllib.request.urlopen(f'http://localhost:{os.getenv(\"PORT\", \"7860\")}/health')"

# Run migrations and start server on port 7860
CMD alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 7860
