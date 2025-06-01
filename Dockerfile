# syntax=docker/dockerfile:1

FROM python:3.10-slim AS base

ENV POETRY_VERSION=2.1.3 \
    POETRY_CACHE_DIR=/root/.cache/pypoetry \
    PIP_CACHE_DIR=/root/.cache/pip

WORKDIR /app

# Builder stage: install poetry and dependencies
FROM base AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    pip install "poetry==${POETRY_VERSION}"

# Copy only dependency files first for better cache usage
COPY --link pyproject.toml ./
COPY --link poetry.lock ./

# Install dependencies (no dev deps, in-project venv)
RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    --mount=type=cache,target=$POETRY_CACHE_DIR \
    poetry config virtualenvs.in-project true && \
    poetry install --no-root --only main

# Copy the rest of the application code
COPY --link app ./app

# Final stage: minimal image with non-root user
FROM base AS final

# Create non-root user
RUN groupadd --system appuser && useradd --system --create-home --gid appuser appuser

WORKDIR /app

# Copy virtualenv and app code from builder
COPY --link --from=builder /app /app

# Set permissions
RUN chown -R appuser:appuser /app

USER appuser

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8050

ENTRYPOINT ["python", "app/app.py"]
