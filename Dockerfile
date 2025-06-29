FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY tika-app.jar .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
