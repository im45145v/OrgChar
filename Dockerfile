FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create directories
RUN mkdir -p /app/knowledge_base /app/vector_db

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose ports
EXPOSE 8501

# Set entrypoint script as executable
RUN chmod +x /app/docker-entrypoint.sh

# Define the entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default command (override with docker run command)
CMD ["web"]
