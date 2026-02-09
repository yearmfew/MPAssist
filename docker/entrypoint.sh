#!/bin/bash
set -e

echo "================================================"
echo "MPAssist Docker Startup Script"
echo "================================================"

echo "================================================"
echo "MPAssist Docker Entrypoint - starting app" 
echo "================================================"

cd /app/src
exec python3 app.py
