FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire package structure
COPY app/ ./parking_card_app/app/
COPY static/ ./static/
COPY templates/ ./templates/
COPY tests/ ./tests/
COPY main.py ./parking_card_app/main.py

# Install as editable package
COPY setup.py .
RUN pip install -e .

CMD ["uvicorn", "parking_card_app.app.main:app", "--host", "0.0.0.0", "--port", "80"]
