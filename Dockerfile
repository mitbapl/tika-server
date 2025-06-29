FROM python:3.10-slim

# Install Java (OpenJDK 17)
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY tika-app.jar .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
