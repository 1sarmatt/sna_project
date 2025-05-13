FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server /app
COPY client/templates /app/templates
COPY client/static /app/static

CMD ["python", "app.py"]
