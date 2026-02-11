FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for weasyprint (visa PDF feature) and dkimpy
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create store directory for pickle persistence
RUN mkdir -p store

EXPOSE 8114

CMD ["gunicorn", "--bind", "0.0.0.0:8114", "--workers", "1", "--preload", "app:app"]
