# Multi-stage build: Stage 1 (Builder)
FROM python:3.11-slim as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Multi-stage build: Stage 2 (Runtime)
FROM python:3.11-slim
WORKDIR /app
ENV TZ=UTC
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .
# Configure cron to log to /cron/last_code.txt every minute
COPY crontab /etc/cron.d/auth-cron
RUN chmod 0644 /etc/cron.d/auth-cron && crontab /etc/cron.d/auth-cron

EXPOSE 8080
# Start both cron service and API server
CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8080