FROM python:3.10-slim

WORKDIR /app

# Install Java (required for tika-app.jar)
RUN apt-get update && apt-get install -y default-jre curl && apt-get clean

# Copy all server files
COPY requirements.txt .
COPY app.py .
COPY tika-server/tika-app.jar ./tika-app.jar  # <- Important: copy from subfolder

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 9998

# Run the Flask app
CMD ["python", "app.py"]
