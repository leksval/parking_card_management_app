FROM python:3.9-slim
WORKDIR /app
COPY src/parking_card_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/parking_card_app/app/ ./app/
COPY src/parking_card_app/templates/ ./templates/
COPY src/parking_card_app/static/ ./static/
COPY src/parking_card_app/main.py .
ENV DATABASE_URL=sqlite+aiosqlite:////app/data/parking.db
RUN apt-get update && apt-get install -y \
    sqlite3 \
    cron \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app/data
RUN mkdir -p /app/scripts
COPY src/parking_card_app/scripts/start.sh /app/scripts/
RUN dos2unix /app/scripts/start.sh && chmod +x /app/scripts/start.sh
CMD ["/app/scripts/start.sh"]
