#!/bin/bash

# MPAssist Web Application Launcher
# Starts the Gradio web interface

set -e

echo "🗺️  MPAssist - Starting Web Application"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Run ./setup.sh first to create the environment."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    echo "📄 Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Check if IONOS_API_TOKEN is set
if [ -z "$IONOS_API_TOKEN" ]; then
    echo ""
    echo "⚠️  WARNING: IONOS_API_TOKEN environment variable not set!"
    echo ""
    echo "Please set your IONOS API token:"
    echo "  export IONOS_API_TOKEN='your-token-here'"
    echo ""
    echo "Or create a .env file with:"
    echo "  IONOS_API_TOKEN=your-token-here"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if database exists
if [ ! -d "db" ]; then
    echo ""
    echo "⚠️  Vector database not found!"
    echo "Run 'python ingest.py' first to create the database."
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🚀 Starting MPAssist Web Application..."
echo "📍 The app will be available at: http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Gradio app
cd src
python app.py
