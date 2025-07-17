# Basis-Image mit Python 3
FROM python:3.11-slim

# Setze Arbeitsverzeichnis
WORKDIR /app

# System-Abhängigkeiten (z. B. für TLS + pip)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Kopiere requirements und installiere sie
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# Kopiere dein Skript + evtl. .env-Datei
COPY dess-mqtt.py ./
# COPY .env ./

# Starte das Skript
CMD ["python", "dess-mqtt.py"]
