FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY static/ ./static/
COPY templates/ ./templates/
COPY tests/ ./tests/
COPY main.py .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
