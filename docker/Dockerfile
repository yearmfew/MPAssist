# Step 1: Use an official Python runtime as a parent image
# Using 'slim' for a smaller image size
FROM python:3.11-slim

# Step 2: Install system dependencies (curl for health checks)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy only the requirements file first (to leverage Docker cache)
COPY requirements.txt .

# Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the application source code
COPY src /app/src
COPY ingest.py /app/ingest.py
COPY masterportal-docs /app/masterportal-docs

# Step 7: Copy and prepare the entrypoint script
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Step 8: Define the entrypoint
# This script will:
# - Wait for Ollama to be ready
# - Pull required models
# - Run ingest.py if database doesn't exist
# - Start main.py
ENTRYPOINT ["/app/entrypoint.sh"]