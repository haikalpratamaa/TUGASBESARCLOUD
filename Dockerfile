FROM python:3.12-slim

# Avoid writing .pyc files, log in real-time, mode unbuffered.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install curl for healthcheck.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application source code.
COPY . .

# Port configuration (Cloud Run uses PORT environment variable, default 8080).
ENV PORT=8080
EXPOSE 8080

# Light healthcheck: check endpoint /healthz every 30 seconds.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -fsS http://127.0.0.1:${PORT}/healthz || exit 1

# Start the application using gunicorn.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 600 run:app
