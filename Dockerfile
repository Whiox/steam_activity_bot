FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY main.py .

COPY src/ src/
COPY save.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]