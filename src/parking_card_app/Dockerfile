FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
COPY templates/ ./templates/
COPY static/ ./static/
COPY main.py .
ENV DATABASE_URL=sqlite+aiosqlite:////app/data/parking.db
RUN apt-get update && apt-get install -y \
    sqlite3 \
    cron \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app/data
RUN mkdir -p /app/scripts
COPY scripts/ /app/scripts/
RUN chmod +x /app/scripts/start.sh
CMD ["/app/scripts/start.sh"]
