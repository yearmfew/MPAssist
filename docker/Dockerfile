FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    ANONYMIZED_TELEMETRY=False 

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY masterportal-docs /app/masterportal-docs

COPY ingest.py /app/
RUN python3 /app/ingest.py

COPY src /app/src

EXPOSE 7860

CMD ["python3", "/app/src/app.py"]