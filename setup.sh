#!/bin/bash

# MPAssist - Virtual Environment Setup Script
# This script creates and configures a Python virtual environment for the project

echo "🚀 MPAssist Virtual Environment Setup"
echo "======================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists."
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf venv
    else
        echo "ℹ️  Using existing virtual environment."
    fi
fi

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to create virtual environment."
        exit 1
    fi
    echo "✅ Virtual environment created successfully."
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies."
    exit 1
fi

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. Activate the virtual environment:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Start Ollama service:"
echo "      ollama serve"
echo ""
echo "   3. Pull required models (first time only):"
echo "      ollama pull llama3"
echo "      ollama pull mxbai-embed-large"
echo ""
echo "   4. Create vector database (first time only):"
echo "      python ingest.py"
echo ""
echo "   5. Run the application:"
echo "      ./run.sh"
echo ""
