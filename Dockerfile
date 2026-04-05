# HoloOS Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy HoloOS code
COPY holoos/ ./holoos/
COPY holoos/ ./holoos/
COPY sdk/ ./sdk/

# Expose ports
EXPOSE 8000 3000

# Run FastAPI server
CMD ["python", "-m", "holoos.api.main"]