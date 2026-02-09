FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    ANONYMIZED_TELEMETRY=False 

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY project_documents /app/project_documents

COPY db /app/db

COPY src /app/src

EXPOSE 7860

CMD ["python3", "/app/src/app.py"]